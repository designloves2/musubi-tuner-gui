"""TJ Output tab: output-directory-based management + sample image viewer.

An "output" entry = one output_dir (+ output_name). Every time training is
started from the Musubi Tuner tab, its output_dir/output_name is
auto-registered here (see register_project(), called from
lora_gui.train_model) — updated in place if that output_dir is already known,
added as new otherwise. You can also add any output_dir manually.

For the selected project, shows:
  - checkpoint list (step number, size, modified time), sorted newest-first
  - sample image gallery from <output_dir>/sample, sorted newest-first
"""

import os
import re
import json
import time
import subprocess
import sys
import toml
import gradio as gr

from .common_gui import get_folder_path, ENV_EXCLUSION
from .tj_i18n import t, get_language, DEFAULT_LANG

REGISTRY_FILENAME = "tj_projects.json"
CHECKPOINT_STEP_RE = re.compile(r"-step(\d+)\.safetensors$", re.IGNORECASE)
SAMPLE_STEP_RE = re.compile(r"_(\d{6})_\d+_\d{14}_")


def _registry_path():
    return os.path.join(os.getcwd(), REGISTRY_FILENAME)


def _load_registry():
    p = _registry_path()
    if os.path.isfile(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_registry(entries):
    try:
        with open(_registry_path(), "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def register_project(output_dir: str, output_name: str = ""):
    """Add/update a project entry. Safe to call on every training start."""
    if not output_dir or not str(output_dir).strip():
        return
    output_dir = str(output_dir).strip()
    entries = _load_registry()
    now = time.time()
    for e in entries:
        if os.path.normpath(e.get("output_dir", "")) == os.path.normpath(output_dir):
            e["output_name"] = output_name or e.get("output_name", "")
            e["last_used"] = now
            _save_registry(entries)
            return
    entries.append(
        {"output_dir": output_dir, "output_name": output_name or "", "last_used": now}
    )
    _save_registry(entries)


def _project_choices():
    entries = sorted(_load_registry(), key=lambda e: -e.get("last_used", 0))
    choices = []
    for e in entries:
        label = e.get("output_name") or os.path.basename(e["output_dir"].rstrip("/\\"))
        choices.append(f"{label}  —  {e['output_dir']}")
    return choices


def _extract_dir_from_choice(choice: str) -> str:
    if not choice:
        return ""
    if "—" in choice:
        return choice.split("—", 1)[1].strip()
    return choice.strip()


def _fmt_size(n_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.0f}{unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f}TB"


def get_gpu_status(lang: str = DEFAULT_LANG) -> str:
    """Query nvidia-smi for a quick 'is training actually running' snapshot."""
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=5,
        ).strip()
    except Exception as e:
        return t("gpu_query_failed", lang, e=e)
    if not out:
        return t("gpu_no_info", lang)
    lines = []
    for row in out.splitlines():
        parts = [p.strip() for p in row.split(",")]
        if len(parts) != 5:
            continue
        name, util, mem_used, mem_total, temp = parts
        lines.append(
            t(
                "gpu_line",
                lang,
                name=name,
                util=util,
                mem_used=mem_used,
                mem_total=mem_total,
                temp=temp,
            )
        )
    return "🖥️ " + " | ".join(lines) if lines else t("gpu_parse_failed", lang)


def get_live_training_log(n: int = 300, lang: str = DEFAULT_LANG) -> str:
    """Tail the currently running training process's captured stdout, if any."""
    try:
        from . import lora_gui
    except Exception as e:
        return t("log_module_load_failed", lang, e=e)
    exe = getattr(lora_gui, "executor", None)
    if exe is None:
        return t("log_never_started", lang)
    tail = exe.get_recent_log(n)
    if not exe.is_running():
        if not tail:
            return t("log_no_training_running", lang)
        return t("log_stopped_prefix", lang) + tail
    return t("log_running_prefix", lang) + tail


def open_folder_in_explorer(path: str, lang: str = DEFAULT_LANG) -> str:
    """Open `path` in the OS file manager. Skipped in headless/web/RunPod contexts
    (same guard used for the tkinter file/folder dialogs elsewhere in the GUI),
    where there is no local desktop to show it on."""
    path = (path or "").strip()
    if not path:
        return t("folder_no_path", lang)
    if not os.path.isdir(path):
        return t("folder_not_found", lang, path=path)
    if any(var in os.environ for var in ENV_EXCLUSION):
        return t("folder_remote_unsupported", lang)
    try:
        if sys.platform == "win32":
            os.startfile(path)  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return t("folder_opened", lang, path=path)
    except Exception as e:
        return t("folder_open_failed", lang, e=e)


def scan_project(output_dir: str, lang: str = DEFAULT_LANG):
    """Return (status_md, checkpoints_md, gallery_items)."""
    output_dir = (output_dir or "").strip()
    if not output_dir:
        return t("output_enter_dir", lang), "", []
    if not os.path.isdir(output_dir):
        return t("output_dir_missing", lang, output_dir=output_dir), "", []

    # Checkpoints
    ckpts = []
    for name in os.listdir(output_dir):
        if not name.lower().endswith(".safetensors"):
            continue
        full = os.path.join(output_dir, name)
        m = CHECKPOINT_STEP_RE.search(name)
        step = int(m.group(1)) if m else None
        ckpts.append(
            {
                "name": name,
                "step": step,
                "size": os.path.getsize(full),
                "mtime": os.path.getmtime(full),
            }
        )
    ckpts.sort(key=lambda c: (c["step"] if c["step"] is not None else -1), reverse=True)

    ckpt_lines = []
    for c in ckpts:
        step_label = (
            t("ckpt_step_label", lang, step=c["step"])
            if c["step"] is not None
            else t("ckpt_final_label", lang)
        )
        ckpt_lines.append(
            t("ckpt_line", lang, step_label=step_label, name=c["name"], size=_fmt_size(c["size"]))
        )
    ckpt_md = (
        t("ckpt_header_count", lang, n=len(ckpts)) + "\n".join(ckpt_lines)
        if ckpts
        else t("ckpt_header_none", lang)
    )

    # Sample images
    sample_dir = os.path.join(output_dir, "sample")
    gallery = []
    n_samples = 0
    if os.path.isdir(sample_dir):
        files = [
            f
            for f in os.listdir(sample_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]

        def sort_key(fname):
            m = SAMPLE_STEP_RE.search(fname)
            return int(m.group(1)) if m else 0

        files.sort(key=sort_key, reverse=True)
        n_samples = len(files)
        for f in files:
            m = SAMPLE_STEP_RE.search(f)
            label = t("ckpt_step_label", lang, step=int(m.group(1))) if m else f
            gallery.append((os.path.join(sample_dir, f), label))

    latest_step = ckpts[0]["step"] if ckpts and ckpts[0]["step"] is not None else "-"
    status = (
        t("output_status_header", lang, output_dir=output_dir)
        + t("output_status_ckpts", lang, n=len(ckpts), latest_step=latest_step)
        + t("output_status_samples", lang, n=n_samples, sample_dir=sample_dir)
    )
    if not os.path.isdir(sample_dir):
        status += t("output_status_no_sample_dir", lang)

    return status, ckpt_md, gallery


def tj_projects_tab(headless=False, config=None):
    lang = get_language(config)
    gr.Markdown(t("output_tab_title", lang) + "\n" + t("output_tab_desc", lang))

    with gr.Accordion(t("monitor_accordion_title", lang), open=True):
        gr.Markdown(t("monitor_disclaimer", lang))
        gpu_status_md = gr.Markdown(t("loading_placeholder", lang))
        live_log = gr.Textbox(
            label=t("live_log_label", lang),
            lines=16,
            max_lines=16,
            interactive=False,
            autoscroll=True,
        )

    with gr.Row():
        project_dropdown = gr.Dropdown(
            label=t("output_dropdown_label", lang),
            choices=_project_choices(),
            interactive=True,
            allow_custom_value=True,
            scale=4,
        )
        load_btn = gr.Button(t("output_load_button", lang), variant="primary", scale=1)
        refresh_btn = gr.Button(t("refresh", lang), scale=1)
        auto_refresh = gr.Checkbox(
            label=t("auto_refresh_checkbox", lang), value=True, scale=1
        )

    with gr.Row():
        manual_dir = gr.Textbox(
            label=t("manual_dir_label", lang),
            placeholder=t("manual_dir_placeholder", lang),
            scale=4,
        )
        browse_btn = gr.Button(
            t("browse_button", lang), visible=(not headless), scale=1
        )
        register_btn = gr.Button(t("register_this_path_button", lang), scale=1)

    current_output_dir = gr.State("")

    status_md = gr.Markdown("")
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Row():
                open_folder_btn = gr.Button(t("open_folder_button", lang), scale=1)
            open_folder_status = gr.Markdown("")
            checkpoints_md = gr.Markdown("")
        with gr.Column(scale=2):
            gallery = gr.Gallery(
                label=t("sample_gallery_label", lang),
                columns=4,
                height=560,
                object_fit="contain",
                show_label=True,
            )

    def load_from_dropdown(choice):
        d = _extract_dir_from_choice(choice)
        status, ckpt_md, gal = scan_project(d, lang=lang)
        return status, ckpt_md, gal, d

    def load_from_manual(d):
        register_project(d)
        status, ckpt_md, gal = scan_project(d, lang=lang)
        return (
            status,
            ckpt_md,
            gal,
            gr.Dropdown(choices=_project_choices()),
            d,
        )

    load_btn.click(
        fn=load_from_dropdown,
        inputs=[project_dropdown],
        outputs=[status_md, checkpoints_md, gallery, current_output_dir],
    )
    project_dropdown.change(
        fn=load_from_dropdown,
        inputs=[project_dropdown],
        outputs=[status_md, checkpoints_md, gallery, current_output_dir],
    )
    register_btn.click(
        fn=load_from_manual,
        inputs=[manual_dir],
        outputs=[status_md, checkpoints_md, gallery, project_dropdown, current_output_dir],
    )

    def browse_and_load(current_dir):
        chosen = get_folder_path(folder_path=current_dir)
        if not chosen:
            return (
                gr.skip(),
                gr.skip(),
                gr.skip(),
                gr.skip(),
                gr.skip(),
                gr.skip(),
            )
        status, ckpt_md, gal = scan_project(chosen, lang=lang)
        register_project(chosen)
        return (
            chosen,
            status,
            ckpt_md,
            gal,
            gr.Dropdown(choices=_project_choices()),
            chosen,
        )

    browse_btn.click(
        fn=browse_and_load,
        inputs=[manual_dir],
        outputs=[
            manual_dir,
            status_md,
            checkpoints_md,
            gallery,
            project_dropdown,
            current_output_dir,
        ],
    )

    open_folder_btn.click(
        fn=lambda d: open_folder_in_explorer(d, lang=lang),
        inputs=[current_output_dir],
        outputs=[open_folder_status],
    )

    def rescan_current(d):
        # Re-scan the currently loaded output dir so new checkpoints/samples
        # written by an in-progress training run show up without re-selecting it.
        if not d or not str(d).strip():
            return gr.skip(), gr.skip(), gr.skip()
        return scan_project(d, lang=lang)

    refresh_btn.click(
        fn=lambda: gr.Dropdown(choices=_project_choices()),
        inputs=[],
        outputs=[project_dropdown],
    ).then(
        fn=rescan_current,
        inputs=[current_output_dir],
        outputs=[status_md, checkpoints_md, gallery],
    )

    # Auto-refresh: re-scan the currently loaded output dir every 10s while
    # training is running, so new checkpoints/sample images show up without
    # a manual click. Toggle off via the checkbox if it's disruptive.
    auto_refresh_timer = gr.Timer(10, active=True)
    auto_refresh_timer.tick(
        fn=rescan_current,
        inputs=[current_output_dir],
        outputs=[status_md, checkpoints_md, gallery],
        # Dedicated lane so this keeps ticking even while a long-running
        # training-wait handler (see lora_gui.py) holds the default queue slot.
        concurrency_id="tj_monitor",
        concurrency_limit=6,
    )
    auto_refresh.change(
        fn=lambda active: gr.Timer(active=active),
        inputs=[auto_refresh],
        outputs=[auto_refresh_timer],
    )

    # Monitoring: GPU status + live training console log, polled independently
    # (faster, cheap) so they stay live even while auto-refresh above is off.
    monitor_timer = gr.Timer(3, active=True)
    monitor_timer.tick(
        fn=lambda: get_gpu_status(lang=lang),
        inputs=[],
        outputs=[gpu_status_md],
        concurrency_id="tj_monitor",
        concurrency_limit=6,
    )
    monitor_timer.tick(
        fn=lambda: get_live_training_log(lang=lang),
        inputs=[],
        outputs=[live_log],
        concurrency_id="tj_monitor",
        concurrency_limit=6,
    )
