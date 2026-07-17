import os
import gradio as gr
import toml
from .class_gui_config import GUIConfig
from .common_gui import path_field
from .tj_i18n import t, get_language


class TrainingSettings:
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
        with gr.Row():
            self.sdpa = gr.Checkbox(
                label=t("tr_sdpa_label", lang),
                value=self.config.get("sdpa", False),
            )

            self.flash_attn = gr.Checkbox(
                label=t("tr_flash_attn_label", lang),
                info=t("tr_flash_attn_info", lang),
                value=self.config.get("flash_attn", False),
            )

            self.sage_attn = gr.Checkbox(
                label=t("tr_sage_attn_label", lang),
                info=t("tr_sage_attn_info", lang),
                value=self.config.get("sage_attn", False),
            )

            self.xformers = gr.Checkbox(
                label=t("tr_xformers_label", lang),
                info=t("tr_xformers_info", lang),
                value=self.config.get("xformers", False),
            )

            self.split_attn = gr.Checkbox(
                label=t("tr_split_attn_label", lang),
                info=t("tr_split_attn_info", lang),
                value=self.config.get("split_attn", False),
            )

        with gr.Row():
            self.compile = gr.Checkbox(
                label=t("tr_compile_label", lang),
                value=self.config.get("compile", False),
            )

            self.compile_backend = gr.Textbox(
                label=t("tr_compile_backend_label", lang),
                placeholder=t("tr_compile_backend_placeholder", lang),
                value=self.config.get("compile_backend", ""),
            )

            self.compile_mode = gr.Dropdown(
                label=t("tr_compile_mode_label", lang),
                choices=[
                    "default",
                    "reduce-overhead",
                    "max-autotune",
                    "max-autotune-no-cudagraphs",
                ],
                value=self.config.get("compile_mode", None),
                interactive=True,
            )

        with gr.Row():
            self.max_train_steps = gr.Number(
                label=t("tr_max_train_steps_label", lang),
                info=t("tr_max_train_steps_info", lang),
                value=self.config.get("max_train_steps", 1600),
                interactive=True,
            )

            self.max_train_epochs = gr.Number(
                label=t("tr_max_train_epochs_label", lang),
                info=t("tr_max_train_epochs_info", lang),
                value=self.config.get("max_train_epochs", None),
            )

            self.max_data_loader_n_workers = gr.Number(
                label=t("tr_max_data_loader_n_workers_label", lang),
                info=t("tr_max_data_loader_n_workers_info", lang),
                value=self.config.get("max_data_loader_n_workers", 8),
                interactive=True,
            )

            self.persistent_data_loader_workers = gr.Checkbox(
                label=t("tr_persistent_data_loader_workers_label", lang),
                info=t("tr_persistent_data_loader_workers_info", lang),
                value=self.config.get("persistent_data_loader_workers", False),
            )

        with gr.Row():
            self.seed = gr.Number(
                label=t("tr_seed_label", lang),
                info=t("tr_seed_info", lang),
                value=self.config.get("seed", None),
            )

            self.gradient_checkpointing = gr.Checkbox(
                label=t("tr_gradient_checkpointing_label", lang),
                info=t("tr_gradient_checkpointing_info", lang),
                value=self.config.get("gradient_checkpointing", False),
            )

            self.gradient_accumulation_steps = gr.Number(
                label=t("tr_gradient_accumulation_steps_label", lang),
                info=t("tr_gradient_accumulation_steps_info", lang),
                value=self.config.get("gradient_accumulation_steps", 1),
                interactive=True,
            )

        self.logging_dir = path_field(
            lang=lang,
            label=t("tr_logging_dir_label", lang),
            placeholder=t("tr_logging_dir_placeholder", lang),
            value=self.config.get("logging_dir", ""),
            is_folder=True,
        )

        with gr.Row():
            self.log_with = gr.Dropdown(
                label=t("tr_log_with_label", lang),
                info=t("tr_log_with_info", lang),
                choices=["tensorboard", "wandb", "all"],
                allow_custom_value=True,
                value=self.config.get("log_with", ""),
                interactive=True,
            )

        with gr.Row():
            self.log_prefix = gr.Textbox(
                label=t("tr_log_prefix_label", lang),
                placeholder=t("tr_log_prefix_placeholder", lang),
                value=self.config.get("log_prefix", ""),
            )

            self.log_tracker_name = gr.Textbox(
                label=t("tr_log_tracker_name_label", lang),
                placeholder=t("tr_log_tracker_name_placeholder", lang),
                value=self.config.get("log_tracker_name", ""),
            )

        with gr.Row():
            self.wandb_run_name = gr.Textbox(
                label=t("tr_wandb_run_name_label", lang),
                placeholder=t("tr_wandb_run_name_placeholder", lang),
                value=self.config.get("wandb_run_name", ""),
            )

            self.wandb_api_key = gr.Textbox(
                label=t("tr_wandb_api_key_label", lang),
                placeholder=t("tr_wandb_api_key_placeholder", lang),
                value=self.config.get("wandb_api_key", ""),
            )

        self.log_tracker_config = path_field(
            lang=lang,
            label=t("tr_log_tracker_config_label", lang),
            placeholder=t("tr_log_tracker_config_placeholder", lang),
            value=self.config.get("log_tracker_config", ""),
        )

        with gr.Row():
            self.log_config = gr.Checkbox(
                label=t("tr_log_config_label", lang),
                info=t("tr_log_config_info", lang),
                value=self.config.get("log_config", False),
            )

        with gr.Row():
            self.ddp_timeout = gr.Number(
                label=t("tr_ddp_timeout_label", lang),
                info=t("tr_ddp_timeout_info", lang),
                value=self.config.get("ddp_timeout", None),
            )

            self.ddp_gradient_as_bucket_view = gr.Checkbox(
                label=t("tr_ddp_gradient_as_bucket_view_label", lang),
                value=self.config.get("ddp_gradient_as_bucket_view", False),
            )

            self.ddp_static_graph = gr.Checkbox(
                label=t("tr_ddp_static_graph_label", lang),
                value=self.config.get("ddp_static_graph", False),
            )

        with gr.Row():
            self.sample_every_n_steps = gr.Number(
                label=t("tr_sample_every_n_steps_label", lang),
                info=t("tr_sample_every_n_steps_info", lang),
                value=self.config.get("sample_every_n_steps", None),
            )

            self.sample_at_first = gr.Checkbox(
                label=t("tr_sample_at_first_label", lang),
                value=self.config.get("sample_at_first", False),
            )

            self.sample_every_n_epochs = gr.Number(
                label=t("tr_sample_every_n_epochs_label", lang),
                info=t("tr_sample_every_n_epochs_info", lang),
                value=self.config.get("sample_every_n_epochs", None),
            )

        self.sample_prompts = path_field(
            lang=lang,
            label=t("tr_sample_prompts_label", lang),
            placeholder=t("tr_sample_prompts_placeholder", lang),
            value=self.config.get("sample_prompts", ""),
        )

        with gr.Column(elem_classes="tj_quickpick"):
            gr.Markdown(t("prompts_quickpick_label", self.lang))
            self.sample_prompts_editor = gr.Textbox(
                label=t("prompts_textbox_label", self.lang),
                placeholder=t("prompts_textbox_placeholder", self.lang),
                lines=6,
                max_lines=12,
            )
            with gr.Row():
                self.sample_prompts_load_btn = gr.Button(
                    t("prompts_load_button", self.lang), scale=1
                )
                self.sample_prompts_save_btn = gr.Button(
                    t("prompts_save_button", self.lang), variant="primary", scale=1
                )
            self.sample_prompts_status = gr.Markdown("")

            def load_prompts_file(path):
                path = (path or "").strip()
                if not path:
                    return "", t("prompts_no_path", self.lang)
                if not os.path.isfile(path):
                    return "", t("prompts_load_not_found", self.lang, path=path)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read(), t("prompts_load_ok", self.lang, path=path)
                except Exception as e:
                    return "", t("prompts_load_failed", self.lang, e=e)

            def save_prompts_file(path, content):
                path = (path or "").strip()
                if not path:
                    return t("prompts_no_path", self.lang)
                try:
                    parent = os.path.dirname(path)
                    if parent:
                        os.makedirs(parent, exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content or "")
                    return t("prompts_save_ok", self.lang, path=path)
                except Exception as e:
                    return t("prompts_save_failed", self.lang, e=e)

            self.sample_prompts_load_btn.click(
                fn=load_prompts_file,
                inputs=[self.sample_prompts],
                outputs=[self.sample_prompts_editor, self.sample_prompts_status],
            )
            self.sample_prompts_save_btn.click(
                fn=save_prompts_file,
                inputs=[self.sample_prompts, self.sample_prompts_editor],
                outputs=[self.sample_prompts_status],
            )
