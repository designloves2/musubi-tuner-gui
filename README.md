# musubi-tuner-gui (TJ fork)

GUI for [musubi-tuner](https://github.com/kohya-ss/musubi-tuner), tracking upstream release v0.3.4.

This is a fork of [bmaltais/musubi-tuner-gui](https://github.com/bmaltais/musubi-tuner-gui) with a set of usability additions layered on top (see below) — all credit for the base GUI goes to [@bmaltais](https://github.com/bmaltais). Licensed GPL-3.0, same as upstream; see [LICENSE](LICENSE).

Contributions to the GUI code are welcome. This project uses [uv](https://github.com/astral-sh/uv) as the Python package manager to facilitate cross-platform use. The aim is to support Linux and Windows, with potential MacOS support pending contributions.

## What this fork adds

Built for training remotely (over a web session / Cloudflare tunnel / similar), where the native OS file-picker dialogs upstream relies on for "Browse" buttons don't work — they try to open on the host machine's desktop, not your browser.

- **Dataset Preview** (Dataset Config tab) — selecting a dataset row shows an inline thumbnail gallery labelled with each image's caption, plus counts of missing/empty captions and latent/text-encoder cache status. No more guessing whether a folder actually loaded.
- **Dataset Upload** (Dataset Config tab) — drag-and-drop a folder or select files straight from your browser to `./Dataset/<name>/images`; a ready-to-use dataset config is auto-generated and registered. Pure browser upload, so it works over a remote/web session where the native folder dialog can't.
- **Registered Dataset Config bookmarks** — save dataset config paths you've used before and pick them from a dropdown (Dataset Config tab, and a quick-pick shortcut right under the Dataset Config field on the Musubi Tuner tab) instead of clicking Browse.
- **📁 Output tab** — every output directory used by a training run is auto-tracked here. Pick one to see its checkpoints (by step, sorted newest-first) and sample images in a gallery, with a folder-open shortcut and 10s auto-refresh.
- **Live monitoring** — GPU utilization/VRAM/temperature, and (for runs started from this GUI's Start training button) a tailable training console log, both refreshed every few seconds without stalling the rest of the UI while training runs.
- **English default + Korean toggle** — all of the above ships in English by default; a Language setting (Settings tab) switches the added panels to Korean (upstream's own labels stay English either way). Takes effect after restarting the GUI.
- **Fixes**: Configuration File Settings dropdown was filtering for `*.json` when presets are `*.toml` (nothing ever showed up); training could crash on CJK characters in log output on non-UTF-8 Windows locales; Krea2/Qwen-Image latent caching rejects `--vae_dtype` but the GUI always sent it; `--network_args` was sent to musubi as one string instead of the list it expects; Gradio's default concurrency limit of 1 meant a running training job froze every other UI event (including the monitoring above) until it finished.

## Supported architectures

An "Architecture" dropdown at the top of Model Settings selects between the following, each with its own training/caching scripts and model fields:

| Architecture | Notes |
|---|---|
| HunyuanVideo | dual text encoder, VAE tiling |
| Wan 2.1/2.2 | task selector, T5/CLIP text encoders, dual DiT for 2.2 |
| Qwen-Image | VL text encoder, model version (original/layered/edit/edit-2509) |
| Z-Image | single text encoder |
| FLUX.2 | single text encoder, model version |
| FLUX.1 Kontext | dual text encoder |
| HunyuanVideo 1.5 | t2v/i2v task, ByT5 text encoder, image encoder |
| FramePack | image encoder, F1/one-frame sampling modes |
| Kandinsky 5 | CLIP+Qwen dual text encoder |
| HiDream-O1-Image | DINOv3 auxiliary loss (weight only; full tuning via Additional Parameters) |
| Ideogram4 | unconditional DiT, sampler presets, caption validation |
| Krea 2 | distilled Turbo DiT for sample generation |

Shared across every architecture: LoRA training, `save_precision`, torch.compile (`compile`/`compile_backend`/`compile_mode`), and block-swap performance options (pinned memory, H2D-only, ring size).

Some architecture-specific tuning flags with many rarely-changed sub-options (Kandinsky 5's nabla-attention params, HiDream-O1's DINOv3 loss internals, etc.) are intentionally left to the **Additional Parameters** free-text field rather than getting dedicated widgets — check the [musubi-tuner docs](https://github.com/kohya-ss/musubi-tuner/tree/main/docs) for the full flag reference per architecture.

## Settings

A **Settings** tab holds GUI-wide preferences, persisted to `config.toml` under a `[settings]` table:

| Setting | Default | Effect |
|---|---|---|
| Enable info tooltips on hover | On | Shows each field's description as a floating tooltip when you hover or focus its name, instead of always-on static hint text. Toggling it applies immediately in the browser, no restart needed. |

## Dataset Config tab

The **Dataset Config** tab creates, opens, edits, validates, and saves the dataset TOML file (`[general]` + `[[datasets]]`) that the *Musubi Tuner* tab's "Dataset Config" field points at. It models the fields documented in [musubi-tuner's dataset config docs](https://github.com/kohya-ss/musubi-tuner/blob/main/docs/dataset_config.md); unknown/advanced keys in a hand-edited file (e.g. `fp_1f_*`, `multiple_target`) are preserved untouched when you open and re-save it. Comments are **not** preserved on save.

The tab has two parts:

- **Datasets** — the list of `[[datasets]]` entries that will be written to the file. Starts empty.
- **Selected dataset** — an editor for whichever row is currently selected in the Datasets list. It's a detail view, not a separate thing: nothing you type here is saved until you commit it.

To build a dataset config from scratch:

1. Set defaults under **General** (resolution, caption extension, batch size, bucket options) — they apply to every dataset unless overridden per-dataset below.
2. Under **Selected dataset**, pick a *Dataset type* (image/video, directory or JSONL), then click **Browse** next to *Source path* and choose your folder or file. If nothing was selected, this automatically creates a new row in **Datasets** for you and selects it — no need to click "Add" first. For directory sources, the GUI also scans the folder for caption files sharing a basename with an image/video (e.g. `foo.jpg` + `foo.txt`) and fills in *Caption Extension (override)* automatically if it's still blank and differs from the General default.
3. Fill in the rest of the fields for that dataset (a `cache_directory` is required; `caption_extension` is required somewhere — dataset or General — for directory sources; video datasets need `target_frames`). Then click **Apply changes to selected dataset** — this is what actually writes the editor's fields into the row.
4. To add another dataset, repeat step 2 (Browse with nothing selected starts a fresh row), or click **Add image dataset** / **Add video dataset** for a blank row. Click any row in the **Datasets** table to switch which one you're editing — the status line above the editor always shows which row you're on.
5. Check the **Validation** panel: `ERROR:` lines block Save, `WARNING:` lines don't.
6. Click **Save** (writes to the path shown in the top textbox) or **Save as** (choose a new file). **Use this file in training tab** copies the saved path into the Musubi Tuner tab's Dataset Config field.

## Documentation about musubi-tuner

Have a read of the documentation posted on https://github.com/kohya-ss/musubi-tuner for the full dataset TOML schema and CLI flag reference. The GUI's Dataset Config tab covers the documented fields; anything it doesn't model can still be hand-edited in the file and will round-trip untouched.

## Requirements

- Python 3.10, 3.11, or 3.12
- An NVIDIA GPU with CUDA 12.4, 12.8, or 13.0 drivers (select the matching extra below)

## Installation (optional, you can skip this section if you prefer to use the provided uv code in the repo)

The installation process will be improved and automated in the future. For now, follow these steps:

1. Install uv (if not already present on your OS).

### Linux/MacOS

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

To add `C:\Users\berna\.local\bin` to your PATH, either restart your system or run:

#### CMD

```cmd
set Path=C:\Users\berna\.local\bin;%Path%
```

#### Powershell

```powershell
$env:Path = "C:\Users\berna\.local\bin;$env:Path"
```

## Starting the GUI
### With uv installation

```shell
git clone --recursive https://github.com/designloves2/musubi-tuner-gui.git
cd musubi-tuner-gui
uv run gui.py
```

### With repo based uv version
#### Windows

```shell
git clone --recursive https://github.com/designloves2/musubi-tuner-gui.git
cd musubi-tuner-gui
.\gui.bat
```

#### Linux

```shell
git clone --recursive https://github.com/designloves2/musubi-tuner-gui.git
cd musubi-tuner-gui
./gui.sh
```

### Selecting a CUDA version

`pyproject.toml` pins the `musubi-tuner` dependency to the `cu128` extra by default (CUDA 12.8, matching torch ≥2.7.1). If your driver supports a different CUDA version, edit the `musubi-tuner[cu128]` line to `cu124` (CUDA 12.4, torch ≥2.5.1) or `cu130` (CUDA 13.0, torch ≥2.9.1), then re-run `uv sync`.

## Running tests

```shell
uv run pytest test/ -v
```

This runs the registry regression suite (one architecture's fields/scripts/caching commands validated per test) and the backward-compatibility suite (pre-refactor `config.toml` files still load correctly). Some tests run the real musubi-tuner caching scripts against the bundled test dataset fixture and are expected to fail past argument parsing on placeholder model paths — that's the pass condition, not a bug.
