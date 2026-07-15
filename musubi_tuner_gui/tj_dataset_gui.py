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


def scan_dataset_dirs(image_dir: str, cache_dir: str = "", caption_ext: str = ".txt"):
    """Scan a plain image folder (+ optional cache folder) and return (gallery_items, status_markdown)."""
    image_dir = (image_dir or "").strip()
    cache_dir = (cache_dir or "").strip()
    ext = (caption_ext or ".txt").strip() or ".txt"

    if not image_dir:
        return [], "⚠️ Source path(이미지 폴더)를 입력하세요."
    if not os.path.isdir(image_dir):
        return [], f"❌ 이미지 폴더가 없음: `{image_dir}`"

    images = _list_images(image_dir)
    if not images:
        return [], f"⚠️ `{image_dir}` 에 이미지가 없습니다. (지원: {', '.join(IMAGE_EXTS)})"

    gallery = []
    missing = []
    empty_caption = []
    paired = 0
    for img in images:
        cap = _read_caption(img, ext)
        name = os.path.basename(img)
        if cap is None:
            label = f"❌ 캡션없음 | {name}"
            missing.append(name)
        elif cap == "":
            label = f"⚠️ 캡션빈칸 | {name}"
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
            cache_line = f"\n- 💾 캐시 파일: **{n_any}**개 (`{cache_dir}`)"
        else:
            cache_line = (
                f"\n- 💾 latent 캐시: **{n_latent}** / TEO 캐시: **{n_te}** "
                f"(이미지 {len(images)}개 대비) `{cache_dir}`"
            )
    elif cache_dir:
        cache_line = f"\n- 💾 캐시 폴더 없음(아직 캐싱 안 함): `{cache_dir}`"

    status = (
        f"### 📁 `{image_dir}`\n"
        f"- 이미지: **{len(images)}**개\n"
        f"- ✅ 캡션 정상: **{paired}** / ❌ 캡션없음: **{len(missing)}** / ⚠️ 빈캡션: **{len(empty_caption)}**"
        f"{cache_line}"
    )
    if missing:
        show = ", ".join(missing[:10]) + (" …" if len(missing) > 10 else "")
        status += f"\n\n❌ **캡션 없는 이미지:** {show}"
    if empty_caption:
        show = ", ".join(empty_caption[:10]) + (" …" if len(empty_caption) > 10 else "")
        status += f"\n\n⚠️ **빈 캡션 이미지:** {show}"
    if not missing and not empty_caption:
        status += "\n\n🎉 모든 이미지에 캡션이 정상으로 짝지어져 있습니다."

    return gallery, status


def scan_dataset_toml(dataset_toml: str, image_dir_override: str = "", caption_ext: str = ""):
    """Scan using a dataset TOML's first [[datasets]] entry (standalone/manual use)."""
    image_dir = (image_dir_override or "").strip()
    cache_dir = ""
    ext = caption_ext or ".txt"

    if dataset_toml and dataset_toml.strip():
        p = dataset_toml.strip()
        if not os.path.isfile(p):
            return [], f"❌ 데이터셋 TOML을 찾을 수 없음: `{p}`"
        try:
            data = toml.load(p)
        except Exception as e:
            return [], f"❌ TOML 파싱 오류: {e}"
        general = data.get("general", {})
        ds_list = data.get("datasets", [])
        if ds_list:
            ds0 = ds_list[0]
            if not image_dir:
                image_dir = ds0.get("image_directory", "") or ""
            cache_dir = ds0.get("cache_directory", "") or ""
            ext = ds0.get("caption_extension", general.get("caption_extension", ext)) or ext

    return scan_dataset_dirs(image_dir, cache_dir, ext)


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


def upload_dataset_files(dataset_name: str, dir_files, multi_files):
    """Copy browser-uploaded files into Dataset/<name>/images, generate a ready
    dataset_config.toml next to it, and register that config. Returns
    (status_md, gallery_items, dataset_config_path, updated_dropdown_choices)."""
    all_files = list(dir_files or []) + list(multi_files or [])
    if not all_files:
        return (
            "⚠️ 업로드할 파일이 없습니다. 폴더나 파일을 선택/드래그하세요.",
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
        f"### ✅ 업로드 완료 — `{dest_root}`\n"
        f"- 업로드된 파일: **{copied}**개 → 이미지 **{n_images}**개 / 캡션(.txt) **{n_captions}**개\n"
        f"- 데이터셋 설정 자동 생성: `{config_path}` (등록됨, Dataset Config 드롭다운에서 바로 불러오기 가능)\n"
    )
    if n_images and n_captions < n_images:
        status += f"\n⚠️ 캡션 없는 이미지가 {n_images - n_captions}개 있습니다. 각 이미지와 같은 이름의 .txt 파일도 업로드하세요."
    if skipped:
        status += "\n\n❌ 복사 실패: " + ", ".join(skipped[:10])

    gallery, _ = scan_dataset_dirs(images_dir, cache_dir, ".txt")
    return status, gallery, config_path, dataset_config_choices()
