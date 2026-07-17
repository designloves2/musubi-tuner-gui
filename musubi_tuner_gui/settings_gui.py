import os
import sys
import threading

import gradio as gr

from .class_gui_config import GUIConfig
from .custom_logging import setup_logging
from .tj_i18n import t, get_language, set_language, LANGUAGES

log = setup_logging()


def restart_gui(lang: str):
    log.info("Restarting GUI process...")
    gr.Info(t("settings_restart_notice", lang))

    def _do_restart():
        os.execv(sys.executable, [sys.executable] + sys.argv)

    # Delay so the click response (and the toast) reach the browser before
    # this process image is replaced.
    threading.Timer(1.5, _do_restart).start()


def save_enable_info_tooltip(
    config: GUIConfig, config_file_path: str, enable_info_tooltip: bool
):
    config.config.setdefault("settings", {})[
        "enable_info_tooltip"
    ] = enable_info_tooltip
    config.save_config(config.config, config_file_path)
    log.info(f"Info tooltip {'enabled' if enable_info_tooltip else 'disabled'}")


def settings_tab(config: GUIConfig, config_file_path: str):
    lang = get_language(config)
    with gr.Row():
        enable_info_tooltip = gr.Checkbox(
            label=t("settings_tooltip_label", lang),
            info=t("settings_tooltip_info", lang),
            value=config.get("settings.enable_info_tooltip", True),
        )
        enable_info_tooltip.change(
            fn=lambda v: save_enable_info_tooltip(config, config_file_path, v),
            inputs=[enable_info_tooltip],
            outputs=[],
            js="(v) => { window.MUSUBI_INFO_TOOLTIP_ENABLED = v; return v; }",
        )

    with gr.Row():
        language_dropdown = gr.Dropdown(
            label=t("settings_language_label", lang),
            info=t("settings_language_info", lang),
            choices=[(label, code) for code, label in LANGUAGES.items()],
            value=lang,
        )
        language_apply_btn = gr.Button(
            t("settings_language_apply_btn", lang), scale=0
        )
        language_apply_btn.click(
            fn=lambda v: apply_language(config, config_file_path, v),
            inputs=[language_dropdown],
            outputs=[],
        )
        restart_btn = gr.Button(t("settings_restart_btn", lang), scale=0)
        restart_btn.click(fn=lambda: restart_gui(lang), inputs=[], outputs=[])


def apply_language(config: GUIConfig, config_file_path: str, lang: str):
    set_language(config, config_file_path, lang)
    gr.Info(t("settings_language_restart_notice", lang))
