import gradio as gr

from .class_gui_config import GUIConfig
from .custom_logging import setup_logging
from .tj_i18n import t, get_language, set_language, LANGUAGES

log = setup_logging()


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
            label="Enable info tooltips on hover",
            info="Shows a tooltip with each field's description when hovering its name. Takes effect immediately, no restart needed.",
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
        language_dropdown.change(
            fn=lambda v: set_language(config, config_file_path, v),
            inputs=[language_dropdown],
            outputs=[],
        )
