import gradio as gr
from .class_gui_config import GUIConfig
from .class_architecture import architecture_choices, DEFAULT_ARCHITECTURE
from .common_gui import path_field
from .tj_dataset_gui import dataset_config_choices, check_resolution_shift_mismatch
from .tj_i18n import t, get_language


class Model:
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
            self.architecture = gr.Dropdown(
                label=t("m_architecture_label", lang),
                info=t("m_architecture_info", lang),
                choices=architecture_choices(),
                value=self.config.get("architecture", DEFAULT_ARCHITECTURE),
                interactive=True,
            )

        self.dataset_config = path_field(
            lang=lang,
            label=t("m_dataset_config_label", lang),
            placeholder=t("m_dataset_config_placeholder", lang),
            value=str(self.config.get("dataset_config", "")),
            default_extension=".toml",
            extension_name="TOML files (*.toml)",
        )
        with gr.Row(elem_classes="tj_quickpick"):
            self.dataset_config_registered = gr.Dropdown(
                label=t("quickpick_dataset_config_label", self.lang),
                choices=dataset_config_choices(),
                interactive=True,
                allow_custom_value=True,
                scale=4,
            )
            self.dataset_config_refresh = gr.Button(t("refresh", self.lang), scale=1)
        self.dataset_config_registered.change(
            fn=lambda v: v,
            inputs=[self.dataset_config_registered],
            outputs=[self.dataset_config],
            show_progress=False,
        )
        self.dataset_config_refresh.click(
            fn=lambda: gr.Dropdown(choices=dataset_config_choices()),
            inputs=[],
            outputs=[self.dataset_config_registered],
            show_progress=False,
        )
        # Also refresh on open/focus so entries registered from the Dataset
        # Config File tab (a separate dropdown/registry read) show up here
        # without needing the manual Refresh button.
        self.dataset_config_registered.focus(
            fn=lambda: gr.Dropdown(choices=dataset_config_choices()),
            inputs=[],
            outputs=[self.dataset_config_registered],
            show_progress=False,
        )

        self.group_dit_vae = gr.Column(visible=True)
        with self.group_dit_vae:
            self._initialize_dit_vae_fields()

        self.group_dit_dtype = gr.Column(visible=True)
        with self.group_dit_dtype:
            self._initialize_dit_dtype_fields()

        self.group_hv_extras = gr.Column(visible=True)
        with self.group_hv_extras:
            self._initialize_hv_extras_fields()

        self.group_dual_text_encoder = gr.Column(visible=True)
        with self.group_dual_text_encoder:
            self._initialize_dual_text_encoder_fields()

        self.group_fp8_common = gr.Column(visible=True)
        with self.group_fp8_common:
            self._initialize_fp8_common_fields()

        self.group_wan_extras = gr.Column(visible=True)
        with self.group_wan_extras:
            self._initialize_wan_extras_fields()

        self.group_single_text_encoder = gr.Column(visible=True)
        with self.group_single_text_encoder:
            self._initialize_single_text_encoder_fields()

        self.group_model_version = gr.Column(visible=True)
        with self.group_model_version:
            self._initialize_model_version_fields()

        self.group_fp8_vl = gr.Column(visible=True)
        with self.group_fp8_vl:
            self._initialize_fp8_vl_fields()

        self.group_qwen_image_extras = gr.Column(visible=True)
        with self.group_qwen_image_extras:
            self._initialize_qwen_image_extras_fields()

        self.group_flux_2_extras = gr.Column(visible=True)
        with self.group_flux_2_extras:
            self._initialize_flux_2_extras_fields()

        self.group_image_encoder = gr.Column(visible=True)
        with self.group_image_encoder:
            self._initialize_image_encoder_fields()

        self.group_hv_1_5_extras = gr.Column(visible=True)
        with self.group_hv_1_5_extras:
            self._initialize_hv_1_5_extras_fields()

        self.group_framepack_extras = gr.Column(visible=True)
        with self.group_framepack_extras:
            self._initialize_framepack_extras_fields()

        self.group_kandinsky5_extras = gr.Column(visible=True)
        with self.group_kandinsky5_extras:
            self._initialize_kandinsky5_extras_fields()

        self.group_hidream_o1_extras = gr.Column(visible=True)
        with self.group_hidream_o1_extras:
            self._initialize_hidream_o1_extras_fields()

        self.group_ideogram4_extras = gr.Column(visible=True)
        with self.group_ideogram4_extras:
            self._initialize_ideogram4_extras_fields()

        self.group_krea2_extras = gr.Column(visible=True)
        with self.group_krea2_extras:
            self._initialize_krea2_extras_fields()

        self.group_perf = gr.Column(visible=True)
        with self.group_perf:
            self._initialize_perf_fields()

        self.group_flow_matching = gr.Column(visible=True)
        with self.group_flow_matching:
            self._initialize_flow_matching_fields()

    def _initialize_dit_vae_fields(self) -> None:
        """Fields shared by every architecture that follows the DiT+VAE shape."""
        lang = self.lang
        self.dit = path_field(
            lang=lang,
            label=t("m_dit_label", lang),
            placeholder=t("m_dit_placeholder", lang),
            value=self.config.get("dit", ""),
        )
        self.vae = path_field(
            lang=lang,
            label=t("m_vae_label", lang),
            placeholder=t("m_vae_placeholder", lang),
            value=self.config.get("vae", ""),
        )
        with gr.Row():
            self.vae_dtype = gr.Dropdown(
                label=t("m_vae_dtype_label", lang),
                info=t("m_vae_dtype_info", lang),
                choices=["float16", "bfloat16"],
                value=self.config.get("vae_dtype", "float16"),
                interactive=True,
            )

    def _initialize_dit_dtype_fields(self) -> None:
        """Shared by architectures with a DiT dtype selector (HunyuanVideo, HunyuanVideo 1.5)."""
        lang = self.lang
        with gr.Row():
            self.dit_dtype = gr.Dropdown(
                label=t("m_dit_dtype_label", lang),
                info=t("m_dit_dtype_info", lang),
                choices=["float16", "bfloat16"],
                value=self.config.get("dit_dtype", "bfloat16"),
                interactive=True,
            )

    def _initialize_hv_extras_fields(self) -> None:
        """HunyuanVideo-only model fields (VAE tiling, text encoder dtype/fp8)."""
        lang = self.lang
        with gr.Row():
            self.vae_tiling = gr.Checkbox(
                label=t("m_vae_tiling_label", lang),
                value=self.config.get("vae_tiling", False),
                interactive=True,
            )

            self.vae_chunk_size = gr.Number(
                label=t("m_vae_chunk_size_label", lang),
                info=t("m_vae_chunk_size_info", lang),
                value=self.config.get("vae_chunk_size", None),
                step=1,
                interactive=True,
            )

            self.vae_spatial_tile_sample_min_size = gr.Number(
                label=t("m_vae_spatial_tile_sample_min_size_label", lang),
                info=t("m_vae_spatial_tile_sample_min_size_info", lang),
                value=self.config.get("vae_spatial_tile_sample_min_size", 256),
                interactive=True,
            )

        with gr.Row():
            self.text_encoder_dtype = gr.Dropdown(
                label=t("m_text_encoder_dtype_label", lang),
                info=t("m_text_encoder_dtype_info", lang),
                choices=["float16", "bfloat16"],
                value=self.config.get("text_encoder_dtype", "float16"),
                interactive=True,
            )

            self.fp8_llm = gr.Checkbox(
                label=t("m_fp8_llm_label", lang),
                value=self.config.get("fp8_llm", False),
            )

    def _initialize_dual_text_encoder_fields(self) -> None:
        """Shared by architectures with two text encoder paths (HunyuanVideo, FLUX Kontext)."""
        lang = self.lang
        self.text_encoder1 = path_field(
            lang=lang,
            label=t("m_text_encoder1_label", lang),
            placeholder=t("m_text_encoder1_placeholder", lang),
            value=self.config.get("text_encoder1", ""),
        )
        self.text_encoder2 = path_field(
            lang=lang,
            label=t("m_text_encoder2_label", lang),
            placeholder=t("m_text_encoder2_placeholder", lang),
            value=self.config.get("text_encoder2", ""),
        )

    def _initialize_fp8_common_fields(self) -> None:
        """fp8_base and fp8_scaled are supported by every architecture seen so
        far; fp8_t5 is shared by Wan and FLUX Kontext specifically."""
        lang = self.lang
        with gr.Row():
            self.fp8_base = gr.Checkbox(
                label=t("m_fp8_base_label", lang),
                value=self.config.get("fp8_base", False),
            )

            self.fp8_scaled = gr.Checkbox(
                label=t("m_fp8_scaled_label", lang),
                value=self.config.get("fp8_scaled", False),
            )

            self.fp8_t5 = gr.Checkbox(
                label=t("m_fp8_t5_label", lang),
                value=self.config.get("fp8_t5", False),
            )

    def _initialize_wan_extras_fields(self) -> None:
        """Wan 2.1/2.2-only model fields (task selector, T5/CLIP, dual DiT)."""
        lang = self.lang
        with gr.Row():
            self.task = gr.Dropdown(
                label=t("m_wan_task_label", lang),
                info=t("m_wan_task_info", lang),
                choices=[
                    "t2v-14B",
                    "t2v-1.3B",
                    "i2v-14B",
                    "t2i-14B",
                    "flf2v-14B",
                    "t2v-1.3B-FC",
                    "t2v-14B-FC",
                    "i2v-14B-FC",
                    "i2v-A14B",
                    "t2v-A14B",
                ],
                value=self.config.get("task", "t2v-14B"),
                interactive=True,
            )

            self.timestep_boundary = gr.Number(
                label=t("m_timestep_boundary_label", lang),
                info=t("m_timestep_boundary_info", lang),
                value=self.config.get("timestep_boundary", None),
                interactive=True,
            )

        self.dit_high_noise = path_field(
            lang=lang,
            label=t("m_dit_high_noise_label", lang),
            placeholder=t("m_dit_high_noise_placeholder", lang),
            value=self.config.get("dit_high_noise", ""),
        )
        self.t5 = path_field(
            lang=lang,
            label=t("m_t5_label", lang),
            placeholder=t("m_t5_placeholder", lang),
            value=self.config.get("t5", ""),
        )
        self.clip = path_field(
            lang=lang,
            label=t("m_clip_label", lang),
            placeholder=t("m_clip_placeholder", lang),
            value=self.config.get("clip", ""),
        )

        with gr.Row():
            self.vae_cache_cpu = gr.Checkbox(
                label=t("m_vae_cache_cpu_label", lang),
                value=self.config.get("vae_cache_cpu", False),
            )

    def _initialize_single_text_encoder_fields(self) -> None:
        """Shared by every architecture with exactly one text encoder path
        (Qwen-Image, Z-Image, FLUX.2, and likely most remaining image archs)."""
        lang = self.lang
        self.text_encoder = path_field(
            lang=lang,
            label=t("m_text_encoder_label", lang),
            placeholder=t("m_text_encoder_placeholder", lang),
            value=self.config.get("text_encoder", ""),
        )

    def _initialize_model_version_fields(self) -> None:
        """Shared by architectures with a model-version selector (Qwen-Image, FLUX.2)."""
        lang = self.lang
        with gr.Row():
            self.model_version = gr.Dropdown(
                label=t("m_model_version_label", lang),
                info=t("m_model_version_info", lang),
                choices=["original", "layered", "edit", "edit-2509"],
                value=self.config.get("model_version", "original"),
                interactive=True,
                allow_custom_value=True,
            )

    def _initialize_fp8_vl_fields(self) -> None:
        """Shared by architectures with a VL/vision-language text encoder fp8
        toggle (Qwen-Image, HunyuanVideo 1.5)."""
        lang = self.lang
        with gr.Row():
            self.fp8_vl = gr.Checkbox(
                label=t("m_fp8_vl_label", lang),
                value=self.config.get("fp8_vl", False),
            )

    def _initialize_qwen_image_extras_fields(self) -> None:
        """Qwen-Image-only model fields (layered mode)."""
        lang = self.lang
        with gr.Row():
            self.num_layers = gr.Number(
                label=t("m_num_layers_label", lang),
                info=t("m_num_layers_info", lang),
                value=self.config.get("num_layers", None),
                step=1,
                interactive=True,
            )

            self.remove_first_image_from_target = gr.Checkbox(
                label=t("m_remove_first_image_from_target_label", lang),
                value=self.config.get("remove_first_image_from_target", False),
            )

    def _initialize_flux_2_extras_fields(self) -> None:
        """FLUX.2-only model fields."""
        lang = self.lang
        with gr.Row():
            self.fp8_text_encoder = gr.Checkbox(
                label=t("m_fp8_text_encoder_label", lang),
                value=self.config.get("fp8_text_encoder", False),
            )

    def _initialize_image_encoder_fields(self) -> None:
        """Shared by architectures with an image encoder for i2v
        (HunyuanVideo 1.5, FramePack)."""
        lang = self.lang
        self.image_encoder = path_field(
            lang=lang,
            label=t("m_image_encoder_label", lang),
            placeholder=t("m_image_encoder_placeholder", lang),
            value=self.config.get("image_encoder", ""),
        )

    def _initialize_hv_1_5_extras_fields(self) -> None:
        """HunyuanVideo 1.5-only model fields (t2v/i2v task, ByT5, VAE patch conv)."""
        lang = self.lang
        with gr.Row():
            self.hv15_task = gr.Dropdown(
                label=t("m_hv15_task_label", lang),
                info=t("m_hv15_task_info", lang),
                choices=["t2v", "i2v"],
                value=self.config.get("hv15_task", "t2v"),
                interactive=True,
            )

        self.byt5 = path_field(
            lang=lang,
            label=t("m_byt5_label", lang),
            placeholder=t("m_byt5_placeholder", lang),
            value=self.config.get("byt5", ""),
        )

        with gr.Row():
            self.vae_enable_patch_conv = gr.Checkbox(
                label=t("m_vae_enable_patch_conv_label", lang),
                value=self.config.get("vae_enable_patch_conv", False),
            )

            self.vae_sample_size = gr.Number(
                label=t("m_vae_sample_size_label", lang),
                value=self.config.get("vae_sample_size", None),
                step=1,
                interactive=True,
            )

    def _initialize_framepack_extras_fields(self) -> None:
        """FramePack-only model fields."""
        lang = self.lang
        with gr.Row():
            self.latent_window_size = gr.Number(
                label=t("m_latent_window_size_label", lang),
                value=self.config.get("latent_window_size", None),
                step=1,
                interactive=True,
            )

            self.f1 = gr.Checkbox(
                label=t("m_f1_label", lang),
                value=self.config.get("f1", False),
            )

            self.bulk_decode = gr.Checkbox(
                label=t("m_bulk_decode_label", lang),
                value=self.config.get("bulk_decode", False),
            )

            self.one_frame = gr.Checkbox(
                label=t("m_one_frame_label", lang),
                value=self.config.get("one_frame", False),
            )

    def _initialize_kandinsky5_extras_fields(self) -> None:
        """Kandinsky 5-only model fields. --task is a required free-form
        string upstream (no fixed choices), unlike Wan/HunyuanVideo 1.5's
        --task enums, so it keeps its own field name rather than sharing
        theirs; more esoteric nabla-attention tuning flags (nabla_P,
        nabla_wH/wT/wW, nabla_method, etc.) are left to the existing
        Additional Parameters passthrough rather than getting dedicated
        widgets."""
        lang = self.lang
        with gr.Row():
            self.kandinsky5_task = gr.Textbox(
                label=t("m_kandinsky5_task_label", lang),
                placeholder=t("m_kandinsky5_task_placeholder", lang),
                value=self.config.get("kandinsky5_task", ""),
            )

        self.text_encoder_clip = path_field(
            lang=lang,
            label=t("m_text_encoder_clip_label", lang),
            placeholder=t("m_text_encoder_clip_placeholder", lang),
            value=self.config.get("text_encoder_clip", ""),
        )
        self.text_encoder_qwen = path_field(
            lang=lang,
            label=t("m_text_encoder_qwen_label", lang),
            placeholder=t("m_text_encoder_qwen_placeholder", lang),
            value=self.config.get("text_encoder_qwen", ""),
        )

    def _initialize_hidream_o1_extras_fields(self) -> None:
        """HiDream-O1-only model fields. Has no separate text-encoder
        checkpoint path -- its text encoder is derived from --dit itself
        during caching. Only dino_loss_weight (0 disables the optional
        DINOv3 auxiliary loss) gets a dedicated widget; the remaining
        DINOv3 tuning flags (layer, feature_mode, model_type, backend,
        etc.) are left to Additional Parameters."""
        lang = self.lang
        with gr.Row():
            self.hidream_task = gr.Dropdown(
                label=t("m_hidream_task_label", lang),
                info=t("m_hidream_task_info", lang),
                choices=["t2i", "i2i"],
                value=self.config.get("hidream_task", "t2i"),
                interactive=True,
            )

            self.hidream_model_type = gr.Dropdown(
                label=t("m_hidream_model_type_label", lang),
                choices=["full", "dev"],
                value=self.config.get("hidream_model_type", "full"),
                interactive=True,
            )

            self.fp8_te = gr.Checkbox(
                label=t("m_fp8_te_label", lang),
                value=self.config.get("fp8_te", False),
            )

        with gr.Row():
            self.dino_loss_weight = gr.Number(
                label=t("m_dino_loss_weight_label", lang),
                info=t("m_dino_loss_weight_info", lang),
                value=self.config.get("dino_loss_weight", 0),
                step=0.001,
                interactive=True,
            )

    def _initialize_ideogram4_extras_fields(self) -> None:
        """Ideogram4-only model fields. log_loss_stats (a debug diagnostics
        flag) is left to Additional Parameters rather than getting a
        dedicated widget."""
        lang = self.lang
        self.unconditional_dit = path_field(
            lang=lang,
            label=t("m_unconditional_dit_label", lang),
            placeholder=t("m_unconditional_dit_placeholder", lang),
            value=self.config.get("unconditional_dit", ""),
        )

        with gr.Row():
            self.sampler_preset = gr.Dropdown(
                label=t("m_sampler_preset_label", lang),
                choices=["V4_DEFAULT_20", "V4_QUALITY_48", "V4_TURBO_12"],
                value=self.config.get("sampler_preset", None),
                interactive=True,
            )

            self.initial_sigma = gr.Number(
                label=t("m_initial_sigma_label", lang),
                info=t("m_initial_sigma_info", lang),
                value=self.config.get("initial_sigma", None),
                step=0.001,
                interactive=True,
            )

        with gr.Row():
            self.use_unconditional_dit_for_lora_sampling = gr.Checkbox(
                label=t("m_use_unconditional_dit_for_lora_sampling_label", lang),
                value=self.config.get("use_unconditional_dit_for_lora_sampling", False),
            )

            self.validate_caption_structure = gr.Checkbox(
                label=t("m_validate_caption_structure_label", lang),
                value=self.config.get("validate_caption_structure", False),
            )

            self.warn_on_caption_issues = gr.Checkbox(
                label=t("m_warn_on_caption_issues_label", lang),
                value=self.config.get("warn_on_caption_issues", False),
            )

    def _initialize_krea2_extras_fields(self) -> None:
        """Krea 2-only model fields."""
        lang = self.lang
        self.turbo_dit = path_field(
            lang=lang,
            label=t("m_turbo_dit_label", lang),
            placeholder=t("m_turbo_dit_placeholder", lang),
            value=self.config.get("turbo_dit", ""),
        )

        with gr.Row():
            self.turbo_dit_cache = gr.Checkbox(
                label=t("m_turbo_dit_cache_label", lang),
                value=self.config.get("turbo_dit_cache", False),
            )

    def _initialize_perf_fields(self) -> None:
        lang = self.lang
        with gr.Row():
            self.blocks_to_swap = gr.Number(
                label=t("m_blocks_to_swap_label", lang),
                info=t("m_blocks_to_swap_info", lang),
                value=self.config.get("blocks_to_swap", None),
                step=1,
                interactive=True,
            )

            self.img_in_txt_in_offloading = gr.Checkbox(
                label=t("m_img_in_txt_in_offloading_label", lang),
                value=self.config.get("img_in_txt_in_offloading", False),
            )

            self.guidance_scale = gr.Number(
                label=t("m_guidance_scale_label", lang),
                info=t("m_guidance_scale_info", lang),
                value=self.config.get("guidance_scale", 1.0),
                step=0.001,
                interactive=True,
            )

        with gr.Row():
            self.use_pinned_memory_for_block_swap = gr.Checkbox(
                label=t("m_use_pinned_memory_for_block_swap_label", lang),
                info=t("m_use_pinned_memory_for_block_swap_info", lang),
                value=self.config.get("use_pinned_memory_for_block_swap", False),
            )

            self.block_swap_h2d_only = gr.Checkbox(
                label=t("m_block_swap_h2d_only_label", lang),
                info=t("m_block_swap_h2d_only_info", lang),
                value=self.config.get("block_swap_h2d_only", False),
            )

            self.block_swap_ring_size = gr.Number(
                label=t("m_block_swap_ring_size_label", lang),
                value=self.config.get("block_swap_ring_size", None),
                step=1,
                interactive=True,
            )

    def _initialize_flow_matching_fields(self) -> None:
        lang = self.lang
        with gr.Row():
            self.timestep_sampling = gr.Dropdown(
                label=t("m_timestep_sampling_label", lang),
                info=t("m_timestep_sampling_info", lang),
                choices=[
                    "sigma",
                    "uniform",
                    "sigmoid",
                    "shift",
                    "krea2_shift",
                    "flux2_shift",
                    "flux_shift",
                ],
                value=self.config.get("timestep_sampling", "sigma"),
                interactive=True,
                allow_custom_value=True,
            )

        self.resolution_shift_warning = gr.Markdown("", elem_classes="tj_quickpick")

        def _refresh_resolution_shift_warning(dataset_config_path, timestep_sampling, architecture):
            return check_resolution_shift_mismatch(
                dataset_config_path, timestep_sampling, architecture, lang=self.lang
            )

        for trigger in (self.timestep_sampling, self.dataset_config, self.architecture):
            trigger.change(
                fn=_refresh_resolution_shift_warning,
                inputs=[self.dataset_config, self.timestep_sampling, self.architecture],
                outputs=[self.resolution_shift_warning],
                show_progress=False,
            )

        with gr.Row():
            self.discrete_flow_shift = gr.Number(
                label=t("m_discrete_flow_shift_label", lang),
                info=t("m_discrete_flow_shift_info", lang),
                value=self.config.get("discrete_flow_shift", 1.0),
                step=0.001,
                interactive=True,
            )

            self.sigmoid_scale = gr.Number(
                label=t("m_sigmoid_scale_label", lang),
                info=t("m_sigmoid_scale_info", lang),
                value=self.config.get("sigmoid_scale", 1.0),
                step=0.001,
                interactive=True,
            )

            self.weighting_scheme = gr.Dropdown(
                label=t("m_weighting_scheme_label", lang),
                choices=["logit_normal", "mode", "cosmap", "sigma_sqrt", "none"],
                value=self.config.get("weighting_scheme", "none"),
                interactive=True,
            )

        with gr.Row():
            self.logit_mean = gr.Number(
                label=t("m_logit_mean_label", lang),
                info=t("m_logit_mean_info", lang),
                value=self.config.get("logit_mean", 0.0),
                step=0.001,
                interactive=True,
            )

            self.logit_std = gr.Number(
                label=t("m_logit_std_label", lang),
                info=t("m_logit_std_info", lang),
                value=self.config.get("logit_std", 1.0),
                step=0.001,
                interactive=True,
            )

            self.mode_scale = gr.Number(
                label=t("m_mode_scale_label", lang),
                info=t("m_mode_scale_info", lang),
                value=self.config.get("mode_scale", 1.29),
                step=0.001,
                interactive=True,
            )

        with gr.Row():
            self.min_timestep = gr.Number(
                label=t("m_min_timestep_label", lang),
                info=t("m_min_timestep_info", lang),
                value=self.config.get("min_timestep", 0),
                step=1,
                minimum=0,
                maximum=999,
                interactive=True,
            )

            self.max_timestep = gr.Number(
                label=t("m_max_timestep_label", lang),
                info=t("m_max_timestep_info", lang),
                value=self.config.get("max_timestep", 1000),
                minimum=1,
                maximum=1000,
                step=1,
                interactive=True,
            )

            self.show_timesteps = gr.Dropdown(
                label=t("m_show_timesteps_label", lang),
                choices=["image", "console"],
                allow_custom_value=True,
                value=self.config.get("show_timesteps", None),
                interactive=True,
            )
