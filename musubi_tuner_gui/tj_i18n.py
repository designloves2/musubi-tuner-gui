"""Lightweight i18n for the TJ-added UI strings only.

Upstream (bmaltais/musubi-tuner-gui) labels stay English always — this only
covers strings added on top (Dataset Preview, Dataset Upload, Output tab,
live monitoring, the registered-Dataset-Config quick-picks). Language is
chosen once in Settings and persisted to config.toml; because Gradio
components are built once at page load, changing it takes effect after
restarting the GUI, not live.
"""

DEFAULT_LANG = "en"
LANGUAGES = {"en": "English", "ko": "한국어 (Korean)"}

# key -> {"en": ..., "ko": ...}. Use str.format placeholders, not f-strings,
# since these are filled in later via t(key, lang, **kwargs).
_T = {
    # --- class_model.py: registered Dataset Config quick-pick -------------
    "quickpick_dataset_config_label": {
        "en": "↳ Or pick from a registered Dataset Config (no Browse dialog — safe for remote use)",
        "ko": "↳ 또는 등록된 Dataset Config에서 선택 (Browse 없이, 원격에서도 안전)",
    },
    "refresh": {"en": "🔄 Refresh", "ko": "🔄 새로고침"},

    # --- dataset_config_gui.py: upload accordion ---------------------------
    "upload_accordion_title": {
        "en": "📤 Dataset Upload (remote-friendly)",
        "ko": "📤 데이터셋 업로드 (원격 지원)",
    },
    "upload_desc": {
        "en": (
            "Uses your browser's own drag-and-drop / file picker — works fine over a remote "
            "(web) session too (unlike the 📁 Browse buttons elsewhere, this never opens a "
            "native file dialog on this PC's desktop). Uploaded files are saved to "
            "`./Dataset/<name>/images`, and a ready-to-use dataset config file is "
            "auto-generated and registered."
        ),
        "ko": (
            "브라우저의 드래그 앤 드롭 / 파일 선택창을 사용합니다 — 원격 접속(웹)에서도 정상 작동합니다 "
            "(다른 곳의 📁 Browse 버튼과 달리 이 PC 데스크톱 파일창을 띄우지 않습니다). "
            "업로드한 파일은 `./Dataset/<이름>/images` 에 저장되고, "
            "바로 쓸 수 있는 데이터셋 설정 파일이 자동으로 생성/등록됩니다."
        ),
    },
    "upload_name_label": {
        "en": "Dataset name (used as folder name)",
        "ko": "데이터셋 이름 (폴더명으로 사용)",
    },
    "upload_name_placeholder": {"en": "e.g. my_character", "ko": "예: my_character"},
    "upload_dir_label": {
        "en": "📁 Upload a folder (drag & drop or click)",
        "ko": "📁 폴더 업로드 (드래그 앤 드롭 또는 클릭)",
    },
    "upload_multi_label": {
        "en": "📄 Or select multiple files (images + caption .txt)",
        "ko": "📄 또는 파일 여러 개 선택 (이미지 + 캡션 .txt)",
    },
    "upload_btn": {
        "en": "⬆️ Upload & register dataset",
        "ko": "⬆️ 업로드 & 데이터셋 등록",
    },
    "upload_reset_btn": {
        "en": "🔄 Reset (start a new one)",
        "ko": "🔄 전체 초기화 (새로 시작)",
    },
    "upload_gallery_label": {
        "en": "Uploaded images / captions",
        "ko": "업로드된 이미지 / 캡션",
    },
    "registered_dataset_dropdown_label": {
        "en": "Registered Dataset Config",
        "ko": "등록된 Dataset Config",
    },
    "load_button": {"en": "📥 Load", "ko": "📥 불러오기"},
    "register_path_button": {
        "en": "📌 Register current path",
        "ko": "📌 현재 경로 등록",
    },
    "dataset_preview_accordion_title": {
        "en": "🖼️ Dataset Preview",
        "ko": "🖼️ Dataset Preview",
    },
    "dataset_preview_desc": {
        "en": (
            "Selecting a row above previews it automatically below. Edit Source path / "
            "Cache directory / Caption Extension and click the button to re-check."
        ),
        "ko": (
            "위에서 데이터셋 행을 선택하면 자동으로 미리보기가 뜹니다. "
            "Source path / Cache directory / Caption Extension을 수정한 뒤 새로 확인하려면 버튼을 누르세요."
        ),
    },
    "preview_this_dataset_button": {
        "en": "🔍 Preview this dataset",
        "ko": "🔍 이 데이터셋 미리보기",
    },
    "image_caption_gallery_label": {"en": "Images / captions", "ko": "이미지 / 캡션"},

    # --- tj_dataset_gui.py: scan_dataset_dirs / upload ----------------------
    "scan_no_source_path": {
        "en": "⚠️ Enter a Source path (image folder).",
        "ko": "⚠️ Source path(이미지 폴더)를 입력하세요.",
    },
    "scan_dir_missing": {
        "en": "❌ Image folder not found: `{image_dir}`",
        "ko": "❌ 이미지 폴더가 없음: `{image_dir}`",
    },
    "scan_no_images": {
        "en": "⚠️ No images found in `{image_dir}`. (supported: {exts})",
        "ko": "⚠️ `{image_dir}` 에 이미지가 없습니다. (지원: {exts})",
    },
    "caption_missing_label": {"en": "❌ no caption | {name}", "ko": "❌ 캡션없음 | {name}"},
    "caption_empty_label": {"en": "⚠️ empty caption | {name}", "ko": "⚠️ 캡션빈칸 | {name}"},
    "cache_line_generic": {
        "en": "\n- 💾 Cache files: **{n_any}** (`{cache_dir}`)",
        "ko": "\n- 💾 캐시 파일: **{n_any}**개 (`{cache_dir}`)",
    },
    "cache_line_specific": {
        "en": (
            "\n- 💾 Latent cache: **{n_latent}** / TEO cache: **{n_te}** "
            "(out of {n_images} images) `{cache_dir}`"
        ),
        "ko": (
            "\n- 💾 latent 캐시: **{n_latent}** / TEO 캐시: **{n_te}** "
            "(이미지 {n_images}개 대비) `{cache_dir}`"
        ),
    },
    "cache_line_none": {
        "en": "\n- 💾 No cache folder yet (not cached yet): `{cache_dir}`",
        "ko": "\n- 💾 캐시 폴더 없음(아직 캐싱 안 함): `{cache_dir}`",
    },
    "scan_status_header": {"en": "### 📁 `{image_dir}`\n", "ko": "### 📁 `{image_dir}`\n"},
    "scan_status_images": {"en": "- Images: **{n_images}**\n", "ko": "- 이미지: **{n_images}**개\n"},
    "scan_status_captions": {
        "en": "- ✅ OK: **{paired}** / ❌ missing: **{missing}** / ⚠️ empty: **{empty}**",
        "ko": "- ✅ 캡션 정상: **{paired}** / ❌ 캡션없음: **{missing}** / ⚠️ 빈캡션: **{empty}**",
    },
    "scan_status_missing_list": {
        "en": "\n\n❌ **Images with no caption:** {show}",
        "ko": "\n\n❌ **캡션 없는 이미지:** {show}",
    },
    "scan_status_empty_list": {
        "en": "\n\n⚠️ **Images with an empty caption:** {show}",
        "ko": "\n\n⚠️ **빈 캡션 이미지:** {show}",
    },
    "scan_status_all_ok": {
        "en": "\n\n🎉 Every image has a matching caption.",
        "ko": "\n\n🎉 모든 이미지에 캡션이 정상으로 짝지어져 있습니다.",
    },
    "toml_not_found": {
        "en": "❌ Dataset TOML not found: `{p}`",
        "ko": "❌ 데이터셋 TOML을 찾을 수 없음: `{p}`",
    },
    "toml_parse_error": {"en": "❌ TOML parse error: {e}", "ko": "❌ TOML 파싱 오류: {e}"},
    "upload_no_files": {
        "en": "⚠️ No files to upload. Select or drag a folder/files.",
        "ko": "⚠️ 업로드할 파일이 없습니다. 폴더나 파일을 선택/드래그하세요.",
    },
    "upload_done_header": {
        "en": "### ✅ Upload complete — `{dest_root}`\n",
        "ko": "### ✅ 업로드 완료 — `{dest_root}`\n",
    },
    "upload_done_counts": {
        "en": "- Uploaded: **{copied}** files → images **{n_images}** / captions(.txt) **{n_captions}**\n",
        "ko": "- 업로드된 파일: **{copied}**개 → 이미지 **{n_images}**개 / 캡션(.txt) **{n_captions}**개\n",
    },
    "upload_done_config": {
        "en": (
            "- Dataset config auto-generated: `{config_path}` (registered — load it "
            "directly from the Dataset Config dropdown)\n"
        ),
        "ko": (
            "- 데이터셋 설정 자동 생성: `{config_path}` "
            "(등록됨, Dataset Config 드롭다운에서 바로 불러오기 가능)\n"
        ),
    },
    "upload_missing_captions_warn": {
        "en": (
            "\n⚠️ {n} image(s) have no caption. Upload a matching .txt file for each."
        ),
        "ko": "\n⚠️ 캡션 없는 이미지가 {n}개 있습니다. 각 이미지와 같은 이름의 .txt 파일도 업로드하세요.",
    },
    "upload_copy_failed": {"en": "\n\n❌ Copy failed: ", "ko": "\n\n❌ 복사 실패: "},

    # --- tj_projects_gui.py: GPU status / live log --------------------------
    "gpu_query_failed": {
        "en": "⚠️ nvidia-smi query failed: {e}",
        "ko": "⚠️ nvidia-smi 조회 실패: {e}",
    },
    "gpu_no_info": {"en": "⚠️ No GPU info", "ko": "⚠️ GPU 정보 없음"},
    "gpu_line": {
        "en": "**{name}** — util **{util}%** · VRAM **{mem_used}/{mem_total} MB** · {temp}°C",
        "ko": "**{name}** — 사용률 **{util}%** · VRAM **{mem_used}/{mem_total} MB** · {temp}°C",
    },
    "gpu_parse_failed": {"en": "⚠️ Failed to parse GPU info", "ko": "⚠️ GPU 정보 파싱 실패"},
    "log_module_load_failed": {
        "en": "(log module failed to load: {e})",
        "ko": "(로그 모듈 로드 실패: {e})",
    },
    "log_never_started": {
        "en": "(Training has never been started)",
        "ko": "(학습이 아직 한 번도 시작되지 않았습니다)",
    },
    "log_no_training_running": {
        "en": "⏹️ No training running",
        "ko": "⏹️ 실행 중인 학습 없음",
    },
    "log_stopped_prefix": {
        "en": "⏹️ Training stopped (last log)\n\n",
        "ko": "⏹️ 학습 종료됨 (마지막 로그)\n\n",
    },
    "log_running_prefix": {"en": "▶️ Training running\n\n", "ko": "▶️ 학습 실행 중\n\n"},
    "folder_no_path": {
        "en": "⚠️ No folder path to open.",
        "ko": "⚠️ 열 폴더 경로가 없습니다.",
    },
    "folder_not_found": {"en": "❌ Folder not found: `{path}`", "ko": "❌ 폴더가 없음: `{path}`"},
    "folder_remote_unsupported": {
        "en": (
            "⚠️ Opening a folder isn't supported over a remote/headless session. "
            "Use Remote Desktop instead."
        ),
        "ko": "⚠️ 원격/헤드리스 세션에서는 폴더 열기를 지원하지 않습니다. 원격데스크톱으로 접속해 사용하세요.",
    },
    "folder_opened": {"en": "📂 Folder opened: `{path}`", "ko": "📂 폴더 열림: `{path}`"},
    "folder_open_failed": {
        "en": "❌ Failed to open folder: {e}",
        "ko": "❌ 폴더 열기 실패: {e}",
    },
    "output_enter_dir": {
        "en": "⚠️ Enter or select an Output Directory.",
        "ko": "⚠️ Output Directory를 선택하거나 입력하세요.",
    },
    "output_dir_missing": {
        "en": "❌ Folder not found: `{output_dir}`",
        "ko": "❌ 폴더가 없음: `{output_dir}`",
    },
    "ckpt_line": {
        "en": "- **{step_label}** — `{name}` ({size})",
        "ko": "- **{step_label}** — `{name}` ({size})",
    },
    "ckpt_header_count": {
        "en": "### 💾 Checkpoints ({n})\n",
        "ko": "### 💾 체크포인트 ({n}개)\n",
    },
    "ckpt_header_none": {
        "en": "### 💾 Checkpoints\n(none saved yet)",
        "ko": "### 💾 체크포인트\n(아직 저장된 체크포인트 없음)",
    },
    "ckpt_step_label": {"en": "step {step}", "ko": "step {step}"},
    "ckpt_final_label": {"en": "final", "ko": "final"},
    "output_status_header": {"en": "### 📁 `{output_dir}`\n", "ko": "### 📁 `{output_dir}`\n"},
    "output_status_ckpts": {
        "en": "- Checkpoints: **{n}** (latest: step {latest_step})\n",
        "ko": "- 체크포인트: **{n}**개 (최신: step {latest_step})\n",
    },
    "output_status_samples": {
        "en": "- Sample images: **{n}** `{sample_dir}`",
        "ko": "- 샘플 이미지: **{n}**장 `{sample_dir}`",
    },
    "output_status_no_sample_dir": {
        "en": (
            "\n\n⚠️ No sample folder yet (no samples generated, or Sample Every N "
            "Steps is 0)"
        ),
        "ko": "\n\n⚠️ sample 폴더 없음 (아직 샘플이 생성되지 않았거나 Sample Every N Steps가 0)",
    },
    "output_tab_title": {"en": "## 📁 Output", "ko": "## 📁 Output"},
    "output_tab_desc": {
        "en": (
            "Every time training starts, its Output Directory is automatically "
            "registered/updated here (existing path: just refreshes last-used time; "
            "new path: added). Select one below to see checkpoints and sample images "
            "in step order."
        ),
        "ko": (
            "학습을 시작할 때마다 해당 Output Directory가 자동으로 목록에 등록/갱신됩니다 "
            "(이미 있는 경로면 최근 사용 시각만 갱신, 새 경로면 추가). "
            "아래에서 선택하면 체크포인트 목록과 학습 중 생성된 샘플 이미지를 스텝 순서로 볼 수 있습니다."
        ),
    },
    "monitor_accordion_title": {
        "en": "🖥️ Live monitoring (GPU / training log)",
        "ko": "🖥️ 실시간 모니터링 (GPU / 학습 로그)",
    },
    "monitor_disclaimer": {
        "en": (
            "⚠️ The training console log only shows runs **started from this GUI's "
            "Start training button**. Training run directly from another window will "
            "only show GPU status, no log."
        ),
        "ko": (
            "⚠️ 학습 콘솔 로그는 **이 GUI(Start training 버튼)로 시작한 학습만** 표시됩니다. "
            "다른 창에서 직접 실행한 학습은 GPU 상태만 보이고 로그는 표시되지 않습니다."
        ),
    },
    "loading_placeholder": {"en": "(loading...)", "ko": "(불러오는 중...)"},
    "live_log_label": {
        "en": "Live training log (last 300 lines)",
        "ko": "실시간 학습 로그 (최근 300줄)",
    },
    "output_dropdown_label": {
        "en": "Output (registered Output Directories)",
        "ko": "Output (등록된 Output Directory)",
    },
    "output_load_button": {"en": "🔍 Load", "ko": "🔍 불러오기"},
    "auto_refresh_checkbox": {
        "en": "⏱️ Auto-refresh (10s)",
        "ko": "⏱️ 자동 새로고침 (10초)",
    },
    "manual_dir_label": {
        "en": "Or enter an Output Directory directly",
        "ko": "또는 Output Directory 직접 입력",
    },
    "manual_dir_placeholder": {
        "en": "e.g. C:/AI/musubi-tj-tuner/my_training/outputs",
        "ko": "예: C:/AI/musubi-tj-tuner/my_training/outputs",
    },
    "browse_button": {"en": "📁 Browse", "ko": "📁 Browse"},
    "register_this_path_button": {
        "en": "📌 Register this path",
        "ko": "📌 이 경로 등록",
    },
    "open_folder_button": {"en": "📂 Open folder", "ko": "📂 폴더 열기"},
    "sample_gallery_label": {
        "en": "Sample images (newest step first)",
        "ko": "샘플 이미지 (최신 스텝 먼저)",
    },

    # --- settings_gui.py: language selector ---------------------------------
    "settings_language_label": {"en": "Language / 언어", "ko": "Language / 언어"},
    "settings_language_info": {
        "en": "Applies to the TJ-added panels (Dataset Preview/Upload, Output tab, "
        "monitoring). Upstream labels stay English. Takes effect after restarting "
        "the GUI.",
        "ko": "TJ가 추가한 화면(Dataset Preview/Upload, Output 탭, 모니터링)에 적용됩니다. "
        "원본 항목은 항상 영어로 유지됩니다. GUI를 재시작해야 반영됩니다.",
    },
}


def get_language(config) -> str:
    try:
        lang = config.get("settings.language", DEFAULT_LANG)
    except Exception:
        lang = DEFAULT_LANG
    return lang if lang in LANGUAGES else DEFAULT_LANG


def set_language(config, config_file_path, lang: str):
    if lang not in LANGUAGES:
        lang = DEFAULT_LANG
    config.config.setdefault("settings", {})["language"] = lang
    config.save_config(config.config, config_file_path)


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    entry = _T.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get(DEFAULT_LANG, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
