import gradio as gr
import toml
import time
from .class_gui_config import GUIConfig
from .class_command_executor import CommandExecutor
from .tj_i18n import t, get_language

train_state_value = time.time()


class LatentCaching:
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
            self.caching_latent_device = gr.Textbox(
                label=t("lc_device_label", lang),
                placeholder=t("lc_device_placeholder", lang),
                value=self.config.get("caching_latent_device", "cuda"),
                interactive=True,
            )
            self.caching_latent_batch_size = gr.Number(
                label=t("lc_batch_size_label", lang),
                value=self.config.get("caching_latent_batch_size", None),
                step=1,
                interactive=True,
                info=t("lc_batch_size_info", lang),
            )
            self.caching_latent_num_workers = gr.Number(
                label=t("lc_num_workers_label", lang),
                value=self.config.get("caching_latent_num_workers", None),
                step=1,
                interactive=True,
                info=t("lc_num_workers_info", lang),
            )

        with gr.Row():
            self.caching_latent_skip_existing = gr.Checkbox(
                label=t("lc_skip_existing_label", lang),
                value=self.config.get("caching_latent_skip_existing", False),
                interactive=True,
                info=t("lc_skip_existing_info", lang),
            )
            self.caching_latent_keep_cache = gr.Checkbox(
                label=t("lc_keep_cache_label", lang),
                value=self.config.get("caching_latent_keep_cache", False),
                interactive=True,
                info=t("lc_keep_cache_info", lang),
            )

        with gr.Row():
            self.caching_latent_debug_mode = gr.Dropdown(
                label=t("lc_debug_mode_label", lang),
                choices=["image", "console"],
                allow_custom_value=True,
                value=self.config.get("caching_latent_debug_mode", None),
                interactive=True,
            )
            self.caching_latent_console_width = gr.Number(
                label=t("lc_console_width_label", lang),
                value=self.config.get("caching_latent_console_width", 80),
                step=1,
                interactive=True,
                info=t("lc_console_width_info", lang),
            )
            self.caching_latent_console_back = gr.Textbox(
                label=t("lc_console_back_label", lang),
                placeholder=t("lc_console_back_placeholder", lang),
                value=self.config.get("caching_latent_console_back", None),
                interactive=True,
            )

        with gr.Row():
            self.caching_latent_console_num_images = gr.Number(
                label=t("lc_console_num_images_label", lang),
                value=self.config.get("caching_latent_console_num_images", None),
                step=1,
                interactive=True,
                info=t("lc_console_num_images_info", lang),
            )
