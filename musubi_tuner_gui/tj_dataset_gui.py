"""TJ dataset preview helpers.

An ai-toolkit-style dataset inspector for Musubi Tuner: given an image folder
(+ optional cache folder / caption extension), returns a thumbnail gallery
labelled with each image's caption, plus a status summary covering:
  - image / caption pairing (which images are missing a .txt caption)
  - latent + text-encoder cache status for the dataset's cache directory

Used by the "📚 Datasets" section of the Dataset Config tab (dataset_config_gui.py):
selecting a row there previews that row's own source/cache/caption fields here.
"""

import os
import re
import json
import shutil
import time
import toml

from .tj_i18n import t, DEFAULT_LANG

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".avif")

# --- Registered dataset config files (bookmarks), mirroring tj_projects_gui's
# Output registry. Lets you pick a previously used dataset TOML from a
# dropdown instead of Browse/Open, which is what breaks over a remote/web
# session (native file dialog opens on the host desktop, not the browser).
DATASET_REGISTRY_FILENAME = "tj_dataset_configs.json"


def _dataset_registry_path():
    return os.path.join(os.getcwd(), DATASET_REGISTRY_FILENAME)


def _load_dataset_registry():
    p = _dataset_registry_path()
    if os.path.isfile(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_dataset_registry(entries):
    try:
        with open(_dataset_registry_path(), "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def register_dataset_config(path: str):
    """Add/update a dataset config bookmark. Safe to call on every save/load."""
    if not path or not str(path).strip():
        return
    path = str(path).strip()
    entries = _load_dataset_registry()
    now = time.time()
    for e in entries:
        if os.path.normpath(e.get("path", "")) == os.path.normpath(path):
            e["last_used"] = now
            _save_dataset_registry(entries)
            return
    entries.append({"path": path, "last_used": now})
    _save_dataset_registry(entries)


def dataset_config_choices():
    entries = sorted(_load_dataset_registry(), key=lambda e: -e.get("last_used", 0))
    return [e["path"] for e in entries if e.get("path")]


def _list_images(image_dir: str):
    files = []
    if image_dir and os.path.isdir(image_dir):
        for name in sorted(os.listdir(image_dir)):
            if name.lower().endswith(IMAGE_EXTS):
                files.append(os.path.join(image_dir, name))
    return files


def _caption_path(image_path: str, ext: str = ".txt"):
    base = os.path.splitext(image_path)[0]
    return base + ext


def _read_caption(image_path: str, ext: str = ".txt"):
    cap = _caption_path(image_path, ext)
    if os.path.isfile(cap):
        try:
            with open(cap, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return ""
    return None  # None = caption file missing


def scan_dataset_dirs(
    image_dir: str, cache_dir: str = "", caption_ext: str = ".txt", lang: str = DEFAULT_LANG
):
    """Scan a plain image folder (+ optional cache folder) and return (gallery_items, status_markdown)."""
    image_dir = (image_dir or "").strip()
    cache_dir = (cache_dir or "").strip()
    ext = (caption_ext or ".txt").strip() or ".txt"

    if not image_dir:
        return [], t("scan_no_source_path", lang)
    if not os.path.isdir(image_dir):
        return [], t("scan_dir_missing", lang, image_dir=image_dir)

    images = _list_images(image_dir)
    if not images:
        return [], t(
            "scan_no_images", lang, image_dir=image_dir, exts=", ".join(IMAGE_EXTS)
        )

    gallery = []
    missing = []
    empty_caption = []
    paired = 0
    for img in images:
        cap = _read_caption(img, ext)
        name = os.path.basename(img)
        if cap is None:
            label = t("caption_missing_label", lang, name=name)
            missing.append(name)
        elif cap == "":
            label = t("caption_empty_label", lang, name=name)
            empty_caption.append(name)
        else:
            preview = cap if len(cap) <= 80 else cap[:80] + "…"
            label = f"✅ {preview}"
            paired += 1
        gallery.append((img, label))

    cache_line = ""
    if cache_dir and os.path.isdir(cache_dir):
        cache_files = os.listdir(cache_dir)
        n_latent = sum(1 for f in cache_files if f.endswith("_kr2.safetensors"))
        n_te = sum(1 for f in cache_files if f.endswith("_te.safetensors"))
        if n_latent == 0 and n_te == 0:
            n_any = sum(1 for f in cache_files if f.endswith(".safetensors"))
            cache_line = t("cache_line_generic", lang, n_any=n_any, cache_dir=cache_dir)
        else:
            cache_line = t(
                "cache_line_specific",
                lang,
                n_latent=n_latent,
                n_te=n_te,
                n_images=len(images),
                cache_dir=cache_dir,
            )
    elif cache_dir:
        cache_line = t("cache_line_none", lang, cache_dir=cache_dir)

    status = (
        t("scan_status_header", lang, image_dir=image_dir)
        + t("scan_status_images", lang, n_images=len(images))
        + t(
            "scan_status_captions",
            lang,
            paired=paired,
            missing=len(missing),
            empty=len(empty_caption),
        )
        + cache_line
    )
    if missing:
        show = ", ".join(missing[:10]) + (" …" if len(missing) > 10 else "")
        status += t("scan_status_missing_list", lang, show=show)
    if empty_caption:
        show = ", ".join(empty_caption[:10]) + (" …" if len(empty_caption) > 10 else "")
        status += t("scan_status_empty_list", lang, show=show)
    if not missing and not empty_caption:
        status += t("scan_status_all_ok", lang)

    return gallery, status


def scan_dataset_toml(
    dataset_toml: str,
    image_dir_override: str = "",
    caption_ext: str = "",
    lang: str = DEFAULT_LANG,
):
    """Scan using a dataset TOML's first [[datasets]] entry (standalone/manual use)."""
    image_dir = (image_dir_override or "").strip()
    cache_dir = ""
    ext = caption_ext or ".txt"

    if dataset_toml and dataset_toml.strip():
        p = dataset_toml.strip()
        if not os.path.isfile(p):
            return [], t("toml_not_found", lang, p=p)
        try:
            data = toml.load(p)
        except Exception as e:
            return [], t("toml_parse_error", lang, e=e)
        general = data.get("general", {})
        ds_list = data.get("datasets", [])
        if ds_list:
            ds0 = ds_list[0]
            if not image_dir:
                image_dir = ds0.get("image_directory", "") or ""
            cache_dir = ds0.get("cache_directory", "") or ""
            ext = ds0.get("caption_extension", general.get("caption_extension", ext)) or ext

    return scan_dataset_dirs(image_dir, cache_dir, ext, lang=lang)


# --- Remote-friendly dataset upload -----------------------------------------
# Uses gr.File(file_count="directory"/"multiple"), which is a pure browser
# upload (drag-and-drop or the browser's own file picker) — unlike the
# Browse buttons elsewhere in this GUI, it never opens a native tkinter
# dialog on the host desktop, so it works fine over a remote/web session.

DATASET_ROOT_DIRNAME = "Dataset"


def dataset_root_dir() -> str:
    return os.path.join(os.getcwd(), DATASET_ROOT_DIRNAME)


def _sanitize_dataset_name(name: str) -> str:
    name = (name or "").strip()
    if not name:
        name = time.strftime("dataset_%Y%m%d_%H%M%S")
    # Keep it a single path segment: strip path separators and other
    # characters that are invalid/awkward in Windows folder names.
    name = re.sub(r'[\/:*?"<>|]', "_", name)
    name = name.strip(" .") or time.strftime("dataset_%Y%m%d_%H%M%S")
    return name


def list_uploaded_datasets():
    root = dataset_root_dir()
    if not os.path.isdir(root):
        return []
    return sorted(
        d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))
    )


def upload_dataset_files(dataset_name: str, dir_files, multi_files, lang: str = DEFAULT_LANG):
    """Copy browser-uploaded files into Dataset/<name>/images, generate a ready
    dataset_config.toml next to it, and register that config. Returns
    (status_md, gallery_items, dataset_config_path, updated_dropdown_choices)."""
    all_files = list(dir_files or []) + list(multi_files or [])
    if not all_files:
        return (
            t("upload_no_files", lang),
            [],
            "",
            dataset_config_choices(),
        )

    name = _sanitize_dataset_name(dataset_name)
    dest_root = os.path.join(dataset_root_dir(), name)
    images_dir = os.path.join(dest_root, "images")
    cache_dir = os.path.join(dest_root, "cache")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)

    copied = 0
    skipped = []
    for f in all_files:
        src = f if isinstance(f, str) else getattr(f, "name", None)
        if not src or not os.path.isfile(src):
            continue
        basename = os.path.basename(src)
        dst = os.path.join(images_dir, basename)
        if os.path.exists(dst):
            # Same filename uploaded twice (e.g. re-upload) — overwrite, that's
            # the expected behavior for "upload again to replace".
            pass
        try:
            shutil.copyfile(src, dst)
            copied += 1
        except Exception as e:
            skipped.append(f"{basename} ({e})")

    n_images = sum(
        1 for f in os.listdir(images_dir) if f.lower().endswith(IMAGE_EXTS)
    )
    n_captions = sum(1 for f in os.listdir(images_dir) if f.lower().endswith(".txt"))

    # Auto-generate a ready-to-use dataset config next to the uploaded images.
    config_path = os.path.join(dest_root, "dataset_config.toml")
    config_data = {
        "general": {
            "resolution": [1024, 1024],
            "caption_extension": ".txt",
            "batch_size": 1,
            "enable_bucket": True,
            "bucket_no_upscale": False,
        },
        "datasets": [
            {
                "image_directory": images_dir.replace("\\", "/"),
                "cache_directory": cache_dir.replace("\\", "/"),
                "num_repeats": 1,
            }
        ],
    }
    with open(config_path, "w", encoding="utf-8") as fh:
        toml.dump(config_data, fh)
    register_dataset_config(config_path)

    status = (
        t("upload_done_header", lang, dest_root=dest_root)
        + t("upload_done_counts", lang, copied=copied, n_images=n_images, n_captions=n_captions)
        + t("upload_done_config", lang, config_path=config_path)
    )
    if n_images and n_captions < n_images:
        status += t("upload_missing_captions_warn", lang, n=n_images - n_captions)
    if skipped:
        status += t("upload_copy_failed", lang) + ", ".join(skipped[:10])

    gallery, _ = scan_dataset_dirs(images_dir, cache_dir, ".txt", lang=lang)
    return status, gallery, config_path, dataset_config_choices()
