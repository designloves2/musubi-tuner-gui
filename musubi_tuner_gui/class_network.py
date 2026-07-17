import gradio as gr
import toml
from .class_gui_config import GUIConfig
from .common_gui import path_field
from .tj_i18n import t, get_language


class Network:
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
            self.network_module = gr.Textbox(
                label=t("net_network_module_label", lang),
                placeholder=t("net_network_module_placeholder", lang),
                value=self.config.get("network_module", None),
            )

            self.dim_from_weights = gr.Checkbox(
                label=t("net_dim_from_weights_label", lang),
                value=self.config.get("dim_from_weights", False),
            )

        self.network_weights = path_field(
            lang=lang,
            label=t("net_network_weights_label", lang),
            placeholder=t("net_network_weights_placeholder", lang),
            value=self.config.get("network_weights", None),
        )

        with gr.Row():
            self.network_dim = gr.Number(
                label=t("net_network_dim_label", lang),
                info=t("net_network_dim_info", lang),
                value=self.config.get("network_dim", 32),
                step=1,
                interactive=True,
            )

            self.network_alpha = gr.Number(
                label=t("net_network_alpha_label", lang),
                info=t("net_network_alpha_info", lang),
                value=self.config.get("network_alpha", 1),
                step=1,
                interactive=True,
            )

            self.network_dropout = gr.Number(
                label=t("net_network_dropout_label", lang),
                info=t("net_network_dropout_info", lang),
                value=self.config.get("network_dropout", 0),
                step=0.01,
                minimum=0,
                maximum=1,
                interactive=True,
            )

            self.scale_weight_norms = gr.Number(
                label=t("net_scale_weight_norms_label", lang),
                info=t("net_scale_weight_norms_info", lang),
                value=self.config.get("scale_weight_norms", None),
                step=0.001,
                interactive=True,
                minimum=0,
            )

        with gr.Row():
            self.network_args = gr.Textbox(
                label=t("net_network_args_label", lang),
                placeholder=t("net_network_args_placeholder", lang),
                value=self.config.get("network_args", ""),
                interactive=True,
            )

        self.base_weights = path_field(
            lang=lang,
            label=t("net_base_weights_label", lang),
            placeholder=t("net_base_weights_placeholder", lang),
            value=self.config.get("base_weights", ""),
        )

        with gr.Row():
            self.base_weights_multiplier = gr.Textbox(
                label=t("net_base_weights_multiplier_label", lang),
                placeholder=t("net_base_weights_multiplier_placeholder", lang),
                value=self.config.get("base_weights_multiplier", ""),
            )

        with gr.Row():
            self.training_comment = gr.Textbox(
                label=t("net_training_comment_label", lang),
                placeholder=t("net_training_comment_placeholder", lang),
                value=self.config.get("training_comment", None),
            )

            self.no_metadata = gr.Checkbox(
                label=t("net_no_metadata_label", lang),
                value=self.config.get("no_metadata", False),
            )
