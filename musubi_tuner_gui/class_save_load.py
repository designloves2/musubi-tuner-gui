import gradio as gr
import toml
from .class_gui_config import GUIConfig
from .common_gui import path_field
from .tj_i18n import t, get_language


class SaveLoadSettings:
    def __init__(
        self,
        headless: bool,
        config: GUIConfig,
    ) -> None:
        self.config = config
        self.headless = headless
        self.lang = get_language(config)

        # Initialize the UI components
        self.initialize_ui_components()

    def initialize_ui_components(self) -> None:
        lang = self.lang
        self.output_dir = path_field(
            lang=lang,
            label=t("sl_output_dir_label", lang),
            placeholder=t("sl_output_dir_placeholder", lang),
            value=self.config.get("output_dir", None),
            is_folder=True,
        )

        with gr.Row():
            self.output_name = gr.Textbox(
                label=t("sl_output_name_label", lang),
                placeholder=t("sl_output_name_placeholder", lang),
                value=self.config.get("output_name", "lora"),
                interactive=True,
            )

            self.save_precision = gr.Dropdown(
                label=t("sl_save_precision_label", lang),
                info=t("sl_save_precision_info", lang),
                choices=["float", "fp32", "fp16", "bf16"],
                value=self.config.get("save_precision", "fp32"),
                interactive=True,
            )

        self.resume = path_field(
            lang=lang,
            label=t("sl_resume_label", lang),
            placeholder=t("sl_resume_placeholder", lang),
            value=self.config.get("resume", None),
            is_folder=True,
        )

        with gr.Row():
            self.save_every_n_epochs = gr.Number(
                label=t("sl_save_every_n_epochs_label", lang),
                info=t("sl_save_every_n_epochs_info", lang),
                value=self.config.get("save_every_n_epochs", None),
                step=1,
                interactive=True,
            )

            self.save_last_n_epochs = gr.Number(
                label=t("sl_save_last_n_epochs_label", lang),
                info=t("sl_save_last_n_epochs_info", lang),
                value=self.config.get("save_last_n_epochs", None),
                step=1,
                interactive=True,
            )

            self.save_every_n_steps = gr.Number(
                label=t("sl_save_every_n_steps_label", lang),
                info=t("sl_save_every_n_steps_info", lang),
                value=self.config.get("save_every_n_steps", None),
                interactive=True,
                step=1,
            )

            self.save_last_n_steps = gr.Number(
                label=t("sl_save_last_n_steps_label", lang),
                info=t("sl_save_last_n_steps_info", lang),
                value=self.config.get("save_last_n_steps", None),
                step=1,
                interactive=True,
            )

        with gr.Row():
            self.save_last_n_epochs_state = gr.Number(
                label=t("sl_save_last_n_epochs_state_label", lang),
                info=t("sl_save_last_n_epochs_state_info", lang),
                value=self.config.get("save_last_n_epochs_state", None),
                step=1,
                interactive=True,
            )

            self.save_last_n_steps_state = gr.Number(
                label=t("sl_save_last_n_steps_state_label", lang),
                info=t("sl_save_last_n_steps_state_info", lang),
                value=self.config.get("save_last_n_steps_state", None),
                step=1,
                interactive=True,
            )

            self.save_state = gr.Checkbox(
                label=t("sl_save_state_label", lang),
                value=self.config.get("save_state", False),
            )

            self.save_state_on_train_end = gr.Checkbox(
                label=t("sl_save_state_on_train_end_label", lang),
                value=self.config.get("save_state_on_train_end", False),
                interactive=True,
            )
