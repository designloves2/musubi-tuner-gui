import gradio as gr
import toml
from .class_gui_config import GUIConfig
from .tj_i18n import t, get_language


class HuggingFace:
    def __init__(
        self,
        config: GUIConfig,
    ) -> None:
        self.config = config
        self.lang = get_language(config)

        # Initialize the UI components
        self.initialize_ui_components()

    def initialize_ui_components(self) -> None:
        lang = self.lang
        with gr.Row():
            self.huggingface_repo_id = gr.Textbox(
                label=t("hf_repo_id_label", lang),
                placeholder=t("hf_repo_id_placeholder", lang),
                value=self.config.get("huggingface_repo_id", ""),
            )

            self.huggingface_token = gr.Textbox(
                label=t("hf_token_label", lang),
                placeholder=t("hf_token_placeholder", lang),
                value=self.config.get("huggingface_token", ""),
            )

        with gr.Row():
            # Repository settings
            self.huggingface_repo_type = gr.Textbox(
                label=t("hf_repo_type_label", lang),
                placeholder=t("hf_repo_type_placeholder", lang),
                value=self.config.get("huggingface_repo_type", ""),
            )

            self.huggingface_repo_visibility = gr.Textbox(
                label=t("hf_repo_visibility_label", lang),
                placeholder=t("hf_repo_visibility_placeholder", lang),
                value=self.config.get("huggingface_repo_visibility", ""),
            )

        with gr.Row():
            # File location in the repository
            self.huggingface_path_in_repo = gr.Textbox(
                label=t("hf_path_in_repo_label", lang),
                placeholder=t("hf_path_in_repo_placeholder", lang),
                value=self.config.get("huggingface_path_in_repo", ""),
            )

        with gr.Row():
            # Functions
            self.save_state_to_huggingface = gr.Checkbox(
                label=t("hf_save_state_label", lang),
                value=self.config.get("huggingface_save_state_to_huggingface", False),
            )

            self.resume_from_huggingface = gr.Textbox(
                label=t("hf_resume_label", lang),
                placeholder=t("hf_resume_placeholder", lang),
                value=self.config.get("huggingface_resume_from_huggingface", ""),
            )

            self.async_upload = gr.Checkbox(
                label=t("hf_async_upload_label", lang),
                value=self.config.get("huggingface_async_upload", False),
            )
