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


def get_gpu_status() -> str:
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
        return f"⚠️ nvidia-smi 조회 실패: {e}"
    if not out:
        return "⚠️ GPU 정보 없음"
    lines = []
    for row in out.splitlines():
        parts = [p.strip() for p in row.split(",")]
        if len(parts) != 5:
            continue
        name, util, mem_used, mem_total, temp = parts
        lines.append(
            f"**{name}** — 사용률 **{util}%** · VRAM **{mem_used}/{mem_total} MB** · {temp}°C"
        )
    return "🖥️ " + " | ".join(lines) if lines else "⚠️ GPU 정보 파싱 실패"


def get_live_training_log(n: int = 300) -> str:
    """Tail the currently running training process's captured stdout, if any."""
    try:
        from . import lora_gui
    except Exception as e:
        return f"(로그 모듈 로드 실패: {e})"
    exe = getattr(lora_gui, "executor", None)
    if exe is None:
        return "(학습이 아직 한 번도 시작되지 않았습니다)"
    if not exe.is_running():
        tail = exe.get_recent_log(n)
        if "로그 없음" in tail:
            return "⏹️ 실행 중인 학습 없음"
        return "⏹️ 학습 종료됨 (마지막 로그)\n\n" + tail
    return "▶️ 학습 실행 중\n\n" + exe.get_recent_log(n)


def open_folder_in_explorer(path: str) -> str:
    """Open `path` in the OS file manager. Skipped in headless/web/RunPod contexts
    (same guard used for the tkinter file/folder dialogs elsewhere in the GUI),
    where there is no local desktop to show it on."""
    path = (path or "").strip()
    if not path:
        return "⚠️ 열 폴더 경로가 없습니다."
    if not os.path.isdir(path):
        return f"❌ 폴더가 없음: `{path}`"
    if any(var in os.environ for var in ENV_EXCLUSION):
        return "⚠️ 원격/헤드리스 세션에서는 폴더 열기를 지원하지 않습니다. 원격데스크톱으로 접속해 사용하세요."
    try:
        if sys.platform == "win32":
            os.startfile(path)  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return f"📂 폴더 열림: `{path}`"
    except Exception as e:
        return f"❌ 폴더 열기 실패: {e}"


def scan_project(output_dir: str):
    """Return (status_md, checkpoints_md, gallery_items)."""
    output_dir = (output_dir or "").strip()
    if not output_dir:
        return "⚠️ Output Directory를 선택하거나 입력하세요.", "", []
    if not os.path.isdir(output_dir):
        return f"❌ 폴더가 없음: `{output_dir}`", "", []

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
        step_label = f"step {c['step']}" if c["step"] is not None else "final"
        ckpt_lines.append(f"- **{step_label}** — `{c['name']}` ({_fmt_size(c['size'])})")
    ckpt_md = (
        "### 💾 체크포인트 (" + str(len(ckpts)) + "개)\n" + "\n".join(ckpt_lines)
        if ckpts
        else "### 💾 체크포인트\n(아직 저장된 체크포인트 없음)"
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
            label = f"step {int(m.group(1))}" if m else f
            gallery.append((os.path.join(sample_dir, f), label))

    latest_step = ckpts[0]["step"] if ckpts and ckpts[0]["step"] is not None else "-"
    status = (
        f"### 📁 `{output_dir}`\n"
        f"- 체크포인트: **{len(ckpts)}**개 (최신: step {latest_step})\n"
        f"- 샘플 이미지: **{n_samples}**장 `{sample_dir}`"
    )
    if not os.path.isdir(sample_dir):
        status += "\n\n⚠️ sample 폴더 없음 (아직 샘플이 생성되지 않았거나 Sample Every N Steps가 0)"

    return status, ckpt_md, gallery


def tj_projects_tab(headless=False, config=None):
    gr.Markdown(
        "## 📁 Output\n"
        "학습을 시작할 때마다 해당 Output Directory가 자동으로 목록에 등록/갱신됩니다 "
        "(이미 있는 경로면 최근 사용 시각만 갱신, 새 경로면 추가). "
        "아래에서 선택하면 체크포인트 목록과 학습 중 생성된 샘플 이미지를 스텝 순서로 볼 수 있습니다."
    )

    with gr.Accordion("🖥️ 실시간 모니터링 (GPU / 학습 로그)", open=True):
        gr.Markdown(
            "⚠️ 학습 콘솔 로그는 **이 GUI(Start training 버튼)로 시작한 학습만** 표시됩니다. "
            "다른 창에서 직접 실행한 학습은 GPU 상태만 보이고 로그는 표시되지 않습니다."
        )
        gpu_status_md = gr.Markdown("(불러오는 중...)")
        live_log = gr.Textbox(
            label="실시간 학습 로그 (최근 300줄)",
            lines=16,
            max_lines=16,
            interactive=False,
            autoscroll=True,
        )

    with gr.Row():
        project_dropdown = gr.Dropdown(
            label="Output (등록된 Output Directory)",
            choices=_project_choices(),
            interactive=True,
            allow_custom_value=True,
            scale=4,
        )
        load_btn = gr.Button("🔍 불러오기", variant="primary", scale=1)
        refresh_btn = gr.Button("🔄 새로고침", scale=1)
        auto_refresh = gr.Checkbox(
            label="⏱️ 자동 새로고침 (10초)", value=True, scale=1
        )

    with gr.Row():
        manual_dir = gr.Textbox(
            label="또는 Output Directory 직접 입력",
            placeholder="예: C:/AI/musubi-tj-tuner/my_training/outputs",
            scale=4,
        )
        browse_btn = gr.Button(
            "📁 Browse", visible=(not headless), scale=1
        )
        register_btn = gr.Button("📌 이 경로 등록", scale=1)

    current_output_dir = gr.State("")

    status_md = gr.Markdown("")
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Row():
                open_folder_btn = gr.Button("📂 폴더 열기", scale=1)
            open_folder_status = gr.Markdown("")
            checkpoints_md = gr.Markdown("")
        with gr.Column(scale=2):
            gallery = gr.Gallery(
                label="샘플 이미지 (최신 스텝 먼저)",
                columns=4,
                height=560,
                object_fit="contain",
                show_label=True,
            )

    def load_from_dropdown(choice):
        d = _extract_dir_from_choice(choice)
        status, ckpt_md, gal = scan_project(d)
        return status, ckpt_md, gal, d

    def load_from_manual(d):
        register_project(d)
        status, ckpt_md, gal = scan_project(d)
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
        status, ckpt_md, gal = scan_project(chosen)
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
        fn=open_folder_in_explorer,
        inputs=[current_output_dir],
        outputs=[open_folder_status],
    )
    def rescan_current(d):
        # Re-scan the currently loaded output dir so new checkpoints/samples
        # written by an in-progress training run show up without re-selecting it.
        if not d or not str(d).strip():
            return gr.skip(), gr.skip(), gr.skip()
        return scan_project(d)

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
        fn=get_gpu_status,
        inputs=[],
        outputs=[gpu_status_md],
        concurrency_id="tj_monitor",
        concurrency_limit=6,
    )
    monitor_timer.tick(
        fn=get_live_training_log,
        inputs=[],
        outputs=[live_log],
        concurrency_id="tj_monitor",
        concurrency_limit=6,
    )
