import gradio as gr
import toml
from .class_gui_config import GUIConfig
from .common_gui import path_field
from .tj_i18n import t, get_language


class TextEncoderOutputsCaching:
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
        self.caching_teo_text_encoder1 = path_field(
            lang=lang,
            label=t("teo_text_encoder1_label", lang),
            placeholder=t("teo_text_encoder1_placeholder", lang),
            value=self.config.get("caching_teo_text_encoder1", ""),
            is_folder=True,
        )
        self.caching_teo_text_encoder2 = path_field(
            lang=lang,
            label=t("teo_text_encoder2_label", lang),
            placeholder=t("teo_text_encoder2_placeholder", lang),
            value=self.config.get("caching_teo_text_encoder2", ""),
            is_folder=True,
        )

        with gr.Row():
            self.caching_teo_text_encoder_dtype = gr.Dropdown(
                label=t("teo_text_encoder_dtype_label", lang),
                choices=["float16", "bfloat16"],
                value=self.config.get("caching_teo_text_encoder_dtype", "float16"),
                interactive=True,
                info=t("teo_text_encoder_dtype_info", lang),
            )

        with gr.Row():
            self.caching_teo_device = gr.Textbox(
                label=t("lc_device_label", lang),
                placeholder=t("lc_device_placeholder", lang),
                value=self.config.get("caching_teo_device", "cuda"),
                interactive=True,
            )
            self.caching_teo_fp8_llm = gr.Checkbox(
                label=t("m_fp8_llm_label", lang),
                value=self.config.get("caching_teo_fp8_llm", False),
                interactive=True,
                info=t("teo_fp8_llm_info", lang),
            )
            self.caching_teo_batch_size = gr.Number(
                label=t("lc_batch_size_label", lang),
                value=self.config.get("caching_teo_batch_size", None),
                step=1,
                interactive=True,
                info=t("lc_batch_size_info", lang),
            )
            self.caching_teo_num_workers = gr.Number(
                label=t("lc_num_workers_label", lang),
                value=self.config.get("caching_teo_num_workers", None),
                step=1,
                interactive=True,
                info=t("lc_num_workers_info", lang),
            )

        with gr.Row():
            self.caching_teo_skip_existing = gr.Checkbox(
                label=t("lc_skip_existing_label", lang),
                value=self.config.get("caching_teo_skip_existing", False),
                interactive=True,
                info=t("lc_skip_existing_info", lang),
            )
            self.caching_teo_keep_cache = gr.Checkbox(
                label=t("lc_keep_cache_label", lang),
                value=self.config.get("caching_teo_keep_cache", False),
                interactive=True,
                info=t("lc_keep_cache_info", lang),
            )
