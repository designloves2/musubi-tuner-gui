"""Lightweight i18n for the whole GUI (upstream kohya/musubi labels included).

Language is chosen once in Settings and persisted to config.toml; because
Gradio components are built once at page load, changing it takes effect
after restarting the GUI, not live.
"""

DEFAULT_LANG = "en"
LANGUAGES = {"en": "English", "ko": "한국어 (Korean)"}

# key -> {"en": ..., "ko": ...}. Use str.format placeholders, not f-strings,
# since these are filled in later via t(key, lang, **kwargs).
_T = {
    # --- class_model.py: Model tab -------------------------------------------
    "m_architecture_label": {"en": "Architecture", "ko": "아키텍처"},
    "m_architecture_info": {
        "en": "Model architecture to train",
        "ko": "학습할 모델 아키텍처",
    },
    "m_dataset_config_label": {"en": "Dataset Config", "ko": "Dataset Config"},
    "m_dataset_config_placeholder": {
        "en": "Path to the dataset config file",
        "ko": "데이터셋 config 파일 경로",
    },
    "m_dit_label": {"en": "DiT Checkpoint Path", "ko": "DiT 체크포인트 경로"},
    "m_dit_placeholder": {"en": "Path to DiT checkpoint", "ko": "DiT 체크포인트 경로"},
    "m_vae_label": {"en": "VAE Checkpoint Path", "ko": "VAE 체크포인트 경로"},
    "m_vae_placeholder": {"en": "Path to VAE checkpoint", "ko": "VAE 체크포인트 경로"},
    "m_vae_dtype_label": {"en": "VAE Data Type", "ko": "VAE 데이터 타입"},
    "m_vae_dtype_info": {
        "en": "Select the data type for VAE",
        "ko": "VAE에 사용할 데이터 타입을 선택하세요",
    },
    "m_dit_dtype_label": {"en": "DiT Data Type", "ko": "DiT 데이터 타입"},
    "m_dit_dtype_info": {
        "en": "Select the data type for DiT",
        "ko": "DiT에 사용할 데이터 타입을 선택하세요",
    },
    "m_vae_tiling_label": {
        "en": "Enable VAE Spatial Tiling",
        "ko": "VAE Spatial Tiling 사용",
    },
    "m_vae_chunk_size_label": {"en": "VAE Chunk Size", "ko": "VAE Chunk Size"},
    "m_vae_chunk_size_info": {
        "en": "Chunk size for CausalConv3d in VAE",
        "ko": "VAE의 CausalConv3d에 사용할 청크 크기",
    },
    "m_vae_spatial_tile_sample_min_size_label": {
        "en": "VAE Spatial Tile Sample Min Size",
        "ko": "VAE Spatial Tile Sample 최소 크기",
    },
    "m_vae_spatial_tile_sample_min_size_info": {
        "en": "Spatial tile sample min size for VAE (default: 256)",
        "ko": "VAE의 spatial tile sample 최소 크기 (기본값: 256)",
    },
    "m_text_encoder_dtype_label": {
        "en": "Text Encoder Data Type",
        "ko": "Text Encoder 데이터 타입",
    },
    "m_text_encoder_dtype_info": {
        "en": "Select the data type for Text Encoder",
        "ko": "Text Encoder에 사용할 데이터 타입을 선택하세요",
    },
    "m_fp8_llm_label": {"en": "Use FP8 for LLM", "ko": "LLM에 FP8 사용"},
    "m_text_encoder1_label": {
        "en": "Text Encoder 1 Directory/file",
        "ko": "Text Encoder 1 디렉토리/파일",
    },
    "m_text_encoder1_placeholder": {
        "en": "Path to Text Encoder 1 directory or file",
        "ko": "Text Encoder 1 디렉토리 또는 파일 경로",
    },
    "m_text_encoder2_label": {
        "en": "Text Encoder 2 Directory/file",
        "ko": "Text Encoder 2 디렉토리/파일",
    },
    "m_text_encoder2_placeholder": {
        "en": "Path to Text Encoder 2 directory or file",
        "ko": "Text Encoder 2 디렉토리 또는 파일 경로",
    },
    "m_fp8_base_label": {"en": "Use FP8 for Base Model", "ko": "Base Model에 FP8 사용"},
    "m_fp8_scaled_label": {"en": "Use scaled FP8 for DiT", "ko": "DiT에 scaled FP8 사용"},
    "m_fp8_t5_label": {"en": "Use FP8 for T5", "ko": "T5에 FP8 사용"},
    "m_wan_task_label": {"en": "Wan Task", "ko": "Wan Task"},
    "m_wan_task_info": {"en": "The Wan task to run", "ko": "실행할 Wan task"},
    "m_timestep_boundary_label": {
        "en": "Timestep Boundary",
        "ko": "Timestep Boundary",
    },
    "m_timestep_boundary_info": {
        "en": "Timestep boundary for switching between high and low noise models (Wan2.2)",
        "ko": "고노이즈/저노이즈 모델을 전환하는 timestep 경계값 (Wan2.2)",
    },
    "m_dit_high_noise_label": {
        "en": "DiT High Noise Checkpoint Path (Wan2.2)",
        "ko": "DiT High Noise 체크포인트 경로 (Wan2.2)",
    },
    "m_dit_high_noise_placeholder": {
        "en": "Path to the high-noise DiT checkpoint (Wan2.2 only)",
        "ko": "high-noise DiT 체크포인트 경로 (Wan2.2 전용)",
    },
    "m_t5_label": {"en": "T5 Checkpoint Path", "ko": "T5 체크포인트 경로"},
    "m_t5_placeholder": {
        "en": "Path to the T5 text encoder checkpoint",
        "ko": "T5 text encoder 체크포인트 경로",
    },
    "m_clip_label": {
        "en": "CLIP Checkpoint Path (Wan2.1 I2V only)",
        "ko": "CLIP 체크포인트 경로 (Wan2.1 I2V 전용)",
    },
    "m_clip_placeholder": {
        "en": "Path to the CLIP text encoder checkpoint, required for Wan2.1 I2V",
        "ko": "CLIP text encoder 체크포인트 경로 (Wan2.1 I2V 필수)",
    },
    "m_vae_cache_cpu_label": {
        "en": "Cache VAE features on CPU",
        "ko": "VAE 특징을 CPU에 캐시",
    },
    "m_text_encoder_label": {"en": "Text Encoder Path", "ko": "Text Encoder 경로"},
    "m_text_encoder_placeholder": {
        "en": "Path to the text encoder checkpoint",
        "ko": "text encoder 체크포인트 경로",
    },
    "m_model_version_label": {"en": "Model Version", "ko": "모델 버전"},
    "m_model_version_info": {
        "en": "Model variant to train",
        "ko": "학습할 모델 변형",
    },
    "m_fp8_vl_label": {"en": "Use FP8 for Text Encoder", "ko": "Text Encoder에 FP8 사용"},
    "m_num_layers_label": {"en": "Number of DiT Layers", "ko": "DiT 레이어 수"},
    "m_num_layers_info": {"en": "Default is None (60)", "ko": "기본값은 None (60)"},
    "m_remove_first_image_from_target_label": {
        "en": "Remove First Image From Target (layered model)",
        "ko": "타겟에서 첫 이미지 제거 (layered 모델)",
    },
    "m_fp8_text_encoder_label": {
        "en": "Use FP8 for Text Encoder",
        "ko": "Text Encoder에 FP8 사용",
    },
    "m_image_encoder_label": {
        "en": "Image Encoder Path (i2v)",
        "ko": "Image Encoder 경로 (i2v)",
    },
    "m_image_encoder_placeholder": {
        "en": "Path to the image encoder checkpoint, required for i2v",
        "ko": "image encoder 체크포인트 경로 (i2v 필수)",
    },
    "m_hv15_task_label": {"en": "Task", "ko": "Task"},
    "m_hv15_task_info": {
        "en": "Text-to-video (t2v) or image-to-video (i2v)",
        "ko": "텍스트-영상 (t2v) 또는 이미지-영상 (i2v)",
    },
    "m_byt5_label": {"en": "ByT5 Checkpoint Path", "ko": "ByT5 체크포인트 경로"},
    "m_byt5_placeholder": {
        "en": "Path to the ByT5 text encoder checkpoint",
        "ko": "ByT5 text encoder 체크포인트 경로",
    },
    "m_vae_enable_patch_conv_label": {
        "en": "Enable VAE Patch Conv",
        "ko": "VAE Patch Conv 사용",
    },
    "m_vae_sample_size_label": {"en": "VAE Sample Size", "ko": "VAE Sample Size"},
    "m_latent_window_size_label": {
        "en": "Latent Window Size",
        "ko": "Latent Window Size",
    },
    "m_f1_label": {"en": "Use F1 Sampling", "ko": "F1 샘플링 사용"},
    "m_bulk_decode_label": {"en": "Bulk Decode", "ko": "Bulk Decode"},
    "m_one_frame_label": {"en": "One Frame Training", "ko": "One Frame 학습"},
    "m_kandinsky5_task_label": {"en": "Task", "ko": "Task"},
    "m_kandinsky5_task_placeholder": {
        "en": "Required task identifier, see musubi-tuner docs",
        "ko": "필수 task 식별자, musubi-tuner 문서 참고",
    },
    "m_text_encoder_clip_label": {
        "en": "CLIP Text Encoder Path",
        "ko": "CLIP Text Encoder 경로",
    },
    "m_text_encoder_clip_placeholder": {
        "en": "Path to the CLIP text encoder checkpoint",
        "ko": "CLIP text encoder 체크포인트 경로",
    },
    "m_text_encoder_qwen_label": {
        "en": "Qwen Text Encoder Path",
        "ko": "Qwen Text Encoder 경로",
    },
    "m_text_encoder_qwen_placeholder": {
        "en": "Path to the Qwen text encoder checkpoint",
        "ko": "Qwen text encoder 체크포인트 경로",
    },
    "m_hidream_task_label": {"en": "Task", "ko": "Task"},
    "m_hidream_task_info": {
        "en": "Text-to-image (t2i) or image-to-image (i2i)",
        "ko": "텍스트-이미지 (t2i) 또는 이미지-이미지 (i2i)",
    },
    "m_hidream_model_type_label": {"en": "Model Type", "ko": "모델 타입"},
    "m_fp8_te_label": {"en": "Use FP8 for Text Encoder", "ko": "Text Encoder에 FP8 사용"},
    "m_dino_loss_weight_label": {
        "en": "DINOv3 Auxiliary Loss Weight",
        "ko": "DINOv3 보조 손실 가중치",
    },
    "m_dino_loss_weight_info": {
        "en": "0 disables the DINOv3 auxiliary loss",
        "ko": "0으로 설정하면 DINOv3 보조 손실을 비활성화합니다",
    },
    "m_unconditional_dit_label": {
        "en": "Unconditional DiT Path",
        "ko": "Unconditional DiT 경로",
    },
    "m_unconditional_dit_placeholder": {
        "en": "Path to the unconditional Ideogram 4 DiT checkpoint",
        "ko": "unconditional Ideogram 4 DiT 체크포인트 경로",
    },
    "m_sampler_preset_label": {"en": "Sampler Preset", "ko": "Sampler Preset"},
    "m_initial_sigma_label": {"en": "Initial Sigma", "ko": "Initial Sigma"},
    "m_initial_sigma_info": {
        "en": "Override the first denoising sigma for sampling",
        "ko": "샘플링 시 첫 denoising sigma 값을 재정의합니다",
    },
    "m_use_unconditional_dit_for_lora_sampling_label": {
        "en": "Use Unconditional DiT for LoRA Sampling",
        "ko": "LoRA 샘플링에 Unconditional DiT 사용",
    },
    "m_validate_caption_structure_label": {
        "en": "Validate Caption Structure",
        "ko": "캡션 구조 검증",
    },
    "m_warn_on_caption_issues_label": {
        "en": "Warn on Caption Issues",
        "ko": "캡션 문제 경고",
    },
    "m_turbo_dit_label": {"en": "Turbo DiT Path", "ko": "Turbo DiT 경로"},
    "m_turbo_dit_placeholder": {
        "en": "Distilled Turbo DiT checkpoint path (for sample generation)",
        "ko": "distilled Turbo DiT 체크포인트 경로 (샘플 생성용)",
    },
    "m_turbo_dit_cache_label": {"en": "Cache Turbo DiT", "ko": "Turbo DiT 캐시"},
    "m_blocks_to_swap_label": {"en": "Blocks to Swap", "ko": "Swap할 블록 수"},
    "m_blocks_to_swap_info": {
        "en": "Number of blocks to swap in the model (max XXX)",
        "ko": "모델에서 swap할 블록 수 (최대 XXX)",
    },
    "m_img_in_txt_in_offloading_label": {
        "en": "Offload img_in and txt_in to CPU",
        "ko": "img_in / txt_in을 CPU로 오프로드",
    },
    "m_guidance_scale_label": {"en": "Guidance Scale", "ko": "Guidance Scale"},
    "m_guidance_scale_info": {
        "en": "Embedded classifier-free guidance scale",
        "ko": "내장 classifier-free guidance 스케일",
    },
    "m_use_pinned_memory_for_block_swap_label": {
        "en": "Use Pinned Memory for Block Swap",
        "ko": "Block Swap에 Pinned Memory 사용",
    },
    "m_use_pinned_memory_for_block_swap_info": {
        "en": "Speeds up block swap at the cost of extra host RAM",
        "ko": "호스트 RAM을 추가로 사용하는 대신 block swap 속도를 높입니다",
    },
    "m_block_swap_h2d_only_label": {
        "en": "Block Swap H2D Only",
        "ko": "Block Swap H2D 전용",
    },
    "m_block_swap_h2d_only_info": {
        "en": "Only swap host-to-device, skipping the device-to-host copy",
        "ko": "host-to-device swap만 수행하고 device-to-host 복사는 건너뜁니다",
    },
    "m_block_swap_ring_size_label": {
        "en": "Block Swap Ring Size",
        "ko": "Block Swap Ring Size",
    },
    "m_timestep_sampling_label": {
        "en": "Timestep Sampling Method",
        "ko": "Timestep 샘플링 방식",
    },
    "m_timestep_sampling_info": {
        "en": (
            "krea2_shift / flux2_shift / flux_shift reproduce that model's own "
            "resolution-aware inference time-shift per sample -- use these instead of "
            "'shift' + a fixed Discrete Flow Shift when training at a non-square or "
            "varying resolution (a fixed shift tuned for one resolution, e.g. 1024x1024, "
            "mismatches the noise schedule at other resolutions and can cause duplicated/"
            "tiled-subject artifacts in samples)."
        ),
        "ko": (
            "krea2_shift / flux2_shift / flux_shift는 각 모델의 해상도 인식 추론 "
            "time-shift를 샘플별로 재현합니다 -- 정사각형이 아니거나 다양한 해상도로 "
            "학습할 때는 'shift' + 고정 Discrete Flow Shift 대신 이 옵션들을 사용하세요 "
            "(예: 1024x1024 기준으로 튜닝된 고정 shift는 다른 해상도에서 노이즈 스케줄과 "
            "맞지 않아 샘플에서 피사체가 중복/타일링되는 결함을 유발할 수 있습니다)."
        ),
    },
    "m_discrete_flow_shift_label": {
        "en": "Discrete Flow Shift",
        "ko": "Discrete Flow Shift",
    },
    "m_discrete_flow_shift_info": {
        "en": "Discrete flow shift for the Euler Discrete Scheduler (default: 1.0)",
        "ko": "Euler Discrete Scheduler의 discrete flow shift (기본값: 1.0)",
    },
    "m_sigmoid_scale_label": {"en": "Sigmoid Scale", "ko": "Sigmoid Scale"},
    "m_sigmoid_scale_info": {
        "en": "Scale factor for sigmoid timestep sampling",
        "ko": "sigmoid timestep 샘플링의 스케일 계수",
    },
    "m_weighting_scheme_label": {"en": "Weighting Scheme", "ko": "가중치 방식"},
    "m_logit_mean_label": {"en": "Logit Mean", "ko": "Logit Mean"},
    "m_logit_mean_info": {
        "en": "Mean for 'logit_normal' weighting scheme",
        "ko": "'logit_normal' 가중치 방식의 평균값",
    },
    "m_logit_std_label": {"en": "Logit Std", "ko": "Logit Std"},
    "m_logit_std_info": {
        "en": "Standard deviation for 'logit_normal' weighting scheme",
        "ko": "'logit_normal' 가중치 방식의 표준편차",
    },
    "m_mode_scale_label": {"en": "Mode Scale", "ko": "Mode Scale"},
    "m_mode_scale_info": {
        "en": "Scale of mode weighting scheme",
        "ko": "mode 가중치 방식의 스케일",
    },
    "m_min_timestep_label": {"en": "Min Timestep", "ko": "최소 Timestep"},
    "m_min_timestep_info": {
        "en": "Minimum timestep for training (0-999)",
        "ko": "학습에 사용할 최소 timestep (0-999)",
    },
    "m_max_timestep_label": {"en": "Max Timestep", "ko": "최대 Timestep"},
    "m_max_timestep_info": {
        "en": "Maximum timestep for training (1-1000)",
        "ko": "학습에 사용할 최대 timestep (1-1000)",
    },
    "m_show_timesteps_label": {"en": "Show Timesteps", "ko": "Timestep 표시"},

    # --- class_training.py: Training tab -------------------------------------
    "tr_sdpa_label": {"en": "Use SDPA for CrossAttention", "ko": "CrossAttention에 SDPA 사용"},
    "tr_flash_attn_label": {"en": "FlashAttention", "ko": "FlashAttention"},
    "tr_flash_attn_info": {
        "en": "Use FlashAttention for CrossAttention",
        "ko": "CrossAttention에 FlashAttention 사용",
    },
    "tr_sage_attn_label": {"en": "SageAttention", "ko": "SageAttention"},
    "tr_sage_attn_info": {
        "en": "Use SageAttention for CrossAttention",
        "ko": "CrossAttention에 SageAttention 사용",
    },
    "tr_xformers_label": {"en": "xformers", "ko": "xformers"},
    "tr_xformers_info": {
        "en": "Use xformers for CrossAttention",
        "ko": "CrossAttention에 xformers 사용",
    },
    "tr_split_attn_label": {"en": "Split Attention", "ko": "Split Attention"},
    "tr_split_attn_info": {
        "en": "Use Split Attention for CrossAttention",
        "ko": "CrossAttention에 Split Attention 사용",
    },
    "tr_compile_label": {"en": "Use torch.compile", "ko": "torch.compile 사용"},
    "tr_compile_backend_label": {"en": "Compile Backend", "ko": "Compile Backend"},
    "tr_compile_backend_placeholder": {
        "en": "e.g. inductor (default if left empty)",
        "ko": "예: inductor (비워두면 기본값)",
    },
    "tr_compile_mode_label": {"en": "Compile Mode", "ko": "Compile Mode"},
    "tr_max_train_steps_label": {
        "en": "Max Training Steps",
        "ko": "최대 학습 스텝 수",
    },
    "tr_max_train_steps_info": {
        "en": "Maximum number of training steps",
        "ko": "학습을 진행할 최대 스텝 수",
    },
    "tr_max_train_epochs_label": {
        "en": "Max Training Epochs",
        "ko": "최대 학습 에포크 수",
    },
    "tr_max_train_epochs_info": {
        "en": "Overrides max_train_steps",
        "ko": "설정하면 max_train_steps보다 우선합니다",
    },
    "tr_max_data_loader_n_workers_label": {
        "en": "Max DataLoader Workers",
        "ko": "최대 DataLoader Worker 수",
    },
    "tr_max_data_loader_n_workers_info": {
        "en": "Lower values reduce RAM usage and speed up epoch start",
        "ko": "값을 낮추면 RAM 사용량이 줄고 에포크 시작 속도가 빨라집니다",
    },
    "tr_persistent_data_loader_workers_label": {
        "en": "Persistent DataLoader Workers",
        "ko": "DataLoader Worker 유지",
    },
    "tr_persistent_data_loader_workers_info": {
        "en": "Keep DataLoader workers alive between epochs",
        "ko": "에포크 사이에도 DataLoader worker를 유지합니다",
    },
    "tr_seed_label": {"en": "Random Seed for Training", "ko": "학습용 랜덤 시드"},
    "tr_seed_info": {
        "en": "Optional: set a fixed seed for reproducibility",
        "ko": "선택 사항: 재현성을 위해 고정 시드를 설정합니다",
    },
    "tr_gradient_checkpointing_label": {
        "en": "Enable Gradient Checkpointing",
        "ko": "Gradient Checkpointing 사용",
    },
    "tr_gradient_checkpointing_info": {
        "en": "Enable gradient checkpointing for memory savings",
        "ko": "메모리 절약을 위해 gradient checkpointing을 사용합니다",
    },
    "tr_gradient_accumulation_steps_label": {
        "en": "Gradient Accumulation Steps",
        "ko": "Gradient 누적 스텝 수",
    },
    "tr_gradient_accumulation_steps_info": {
        "en": "Number of steps to accumulate gradients before backward pass",
        "ko": "backward pass 이전에 gradient를 누적할 스텝 수",
    },
    "tr_logging_dir_label": {"en": "Logging Directory", "ko": "로그 디렉토리"},
    "tr_logging_dir_placeholder": {
        "en": "Directory for TensorBoard logs",
        "ko": "TensorBoard 로그를 저장할 디렉토리",
    },
    "tr_log_with_label": {"en": "Logging Tool", "ko": "로깅 도구"},
    "tr_log_with_info": {
        "en": "Select the logging tool to use",
        "ko": "사용할 로깅 도구를 선택하세요",
    },
    "tr_log_prefix_label": {"en": "Log Directory Prefix", "ko": "로그 디렉토리 접두사"},
    "tr_log_prefix_placeholder": {
        "en": "Prefix for each log directory",
        "ko": "각 로그 디렉토리의 접두사",
    },
    "tr_log_tracker_name_label": {"en": "Log Tracker Name", "ko": "Log Tracker 이름"},
    "tr_log_tracker_name_placeholder": {
        "en": "Name of the tracker used for logging",
        "ko": "로깅에 사용할 tracker 이름",
    },
    "tr_wandb_run_name_label": {"en": "WandB Run Name", "ko": "WandB Run 이름"},
    "tr_wandb_run_name_placeholder": {
        "en": "Name of the specific WandB session",
        "ko": "특정 WandB 세션의 이름",
    },
    "tr_wandb_api_key_label": {"en": "WandB API Key", "ko": "WandB API 키"},
    "tr_wandb_api_key_placeholder": {
        "en": "Optional: Specify WandB API key to log in before training",
        "ko": "선택 사항: 학습 전 로그인할 WandB API 키",
    },
    "tr_log_tracker_config_label": {
        "en": "Log Tracker Config",
        "ko": "Log Tracker Config",
    },
    "tr_log_tracker_config_placeholder": {
        "en": "Path to the tracker config file for logging",
        "ko": "로깅용 tracker config 파일 경로",
    },
    "tr_log_config_label": {
        "en": "Log Training Configuration",
        "ko": "학습 설정 로깅",
    },
    "tr_log_config_info": {
        "en": "Log the training configuration to the logging directory",
        "ko": "학습 설정을 로그 디렉토리에 기록합니다",
    },
    "tr_ddp_timeout_label": {"en": "DDP Timeout (minutes)", "ko": "DDP 타임아웃 (분)"},
    "tr_ddp_timeout_info": {
        "en": "Set DDP timeout in minutes (None for default)",
        "ko": "DDP 타임아웃을 분 단위로 설정 (기본값은 None)",
    },
    "tr_ddp_gradient_as_bucket_view_label": {
        "en": "Enable Gradient as Bucket View for DDP",
        "ko": "DDP에 Gradient as Bucket View 사용",
    },
    "tr_ddp_static_graph_label": {
        "en": "Enable Static Graph for DDP",
        "ko": "DDP에 Static Graph 사용",
    },
    "tr_sample_every_n_steps_label": {
        "en": "Sample Every N Steps",
        "ko": "N 스텝마다 샘플 생성",
    },
    "tr_sample_every_n_steps_info": {
        "en": "Generate sample images every N steps",
        "ko": "N 스텝마다 샘플 이미지를 생성합니다",
    },
    "tr_sample_at_first_label": {
        "en": "Sample Before Training",
        "ko": "학습 시작 전 샘플 생성",
    },
    "tr_sample_every_n_epochs_label": {
        "en": "Sample Every N Epochs",
        "ko": "N 에포크마다 샘플 생성",
    },
    "tr_sample_every_n_epochs_info": {
        "en": "Generate sample images every N epochs (overrides N steps)",
        "ko": "N 에포크마다 샘플 이미지를 생성합니다 (N 스텝 설정보다 우선)",
    },
    "tr_sample_prompts_label": {"en": "Sample Prompts", "ko": "샘플 프롬프트"},
    "tr_sample_prompts_placeholder": {
        "en": "File containing prompts to generate sample images",
        "ko": "샘플 이미지 생성용 프롬프트가 담긴 파일",
    },

    # --- class_latent_caching.py / class_text_encoder_outputs_caching.py ----
    "lc_device_label": {"en": "Device", "ko": "Device"},
    "lc_device_placeholder": {
        "en": "Device to use (default is CUDA if available)",
        "ko": "사용할 장치 (CUDA 사용 가능 시 기본값)",
    },
    "lc_batch_size_label": {"en": "Batch Size", "ko": "배치 크기"},
    "lc_batch_size_info": {
        "en": "Override dataset config if dataset batch size > this",
        "ko": "데이터셋 config의 배치 크기가 이보다 크면 이 값으로 재정의",
    },
    "lc_num_workers_label": {"en": "Number of Workers", "ko": "Worker 수"},
    "lc_num_workers_info": {
        "en": "Default is CPU count - 1",
        "ko": "기본값은 CPU 코어 수 - 1",
    },
    "lc_skip_existing_label": {"en": "Skip Existing", "ko": "기존 캐시 건너뛰기"},
    "lc_skip_existing_info": {
        "en": "Skip existing cache files",
        "ko": "이미 존재하는 캐시 파일은 건너뜁니다",
    },
    "lc_keep_cache_label": {"en": "Keep Cache", "ko": "캐시 유지"},
    "lc_keep_cache_info": {
        "en": "Keep cache files not in dataset",
        "ko": "데이터셋에 없는 캐시 파일도 유지합니다",
    },
    "lc_debug_mode_label": {"en": "Debug Mode", "ko": "디버그 모드"},
    "lc_console_width_label": {"en": "Console Width", "ko": "콘솔 너비"},
    "lc_console_width_info": {
        "en": "Console width for debug mode",
        "ko": "디버그 모드에서 콘솔 너비",
    },
    "lc_console_back_label": {
        "en": "Console Background Color",
        "ko": "콘솔 배경색",
    },
    "lc_console_back_placeholder": {
        "en": "Background color for debug console",
        "ko": "디버그 콘솔의 배경색",
    },
    "lc_console_num_images_label": {"en": "Number of Images", "ko": "이미지 개수"},
    "lc_console_num_images_info": {
        "en": "Number of images to show for each dataset in debug mode",
        "ko": "디버그 모드에서 각 데이터셋마다 표시할 이미지 개수",
    },
    "teo_text_encoder1_label": {
        "en": "Text Encoder 1 Directory",
        "ko": "Text Encoder 1 디렉토리",
    },
    "teo_text_encoder1_placeholder": {
        "en": "Path to Text Encoder 1 directory",
        "ko": "Text Encoder 1 디렉토리 경로",
    },
    "teo_text_encoder2_label": {
        "en": "Text Encoder 2 Directory",
        "ko": "Text Encoder 2 디렉토리",
    },
    "teo_text_encoder2_placeholder": {
        "en": "Path to Text Encoder 2 directory",
        "ko": "Text Encoder 2 디렉토리 경로",
    },
    "teo_text_encoder_dtype_label": {
        "en": "Text Encoder Data Type",
        "ko": "Text Encoder 데이터 타입",
    },
    "teo_text_encoder_dtype_info": {
        "en": "Default is float16",
        "ko": "기본값은 float16",
    },
    "teo_fp8_llm_info": {
        "en": "Enable FP8 for Text Encoder 1",
        "ko": "Text Encoder 1에 FP8 사용",
    },

    # --- class_network.py: Network tab ---------------------------------------
    "net_network_module_label": {"en": "Network Module", "ko": "Network Module"},
    "net_network_module_placeholder": {
        "en": "Module of the network to train",
        "ko": "학습할 network의 module",
    },
    "net_dim_from_weights_label": {
        "en": "Determine Dimensions from Network Weights",
        "ko": "Network Weights에서 차원 자동 결정",
    },
    "net_network_weights_label": {"en": "Network Weights", "ko": "Network Weights"},
    "net_network_weights_placeholder": {
        "en": "Path to pretrained weights for network",
        "ko": "network의 사전학습 가중치 경로",
    },
    "net_network_dim_label": {"en": "Network Dimensions", "ko": "Network 차원 수"},
    "net_network_dim_info": {
        "en": "Specify dimensions for the network (depends on the module)",
        "ko": "network의 차원 수를 지정합니다 (module에 따라 다름)",
    },
    "net_network_alpha_label": {"en": "Network Alpha", "ko": "Network Alpha"},
    "net_network_alpha_info": {
        "en": "Alpha value for LoRA weight scaling (default: 1)",
        "ko": "LoRA 가중치 스케일링용 alpha 값 (기본값: 1)",
    },
    "net_network_dropout_label": {"en": "Network Dropout", "ko": "Network Dropout"},
    "net_network_dropout_info": {
        "en": "Dropout rate (0 or None for no dropout, 1 drops all neurons)",
        "ko": "Dropout 비율 (0 또는 None은 dropout 없음, 1은 모든 뉴런 제거)",
    },
    "net_scale_weight_norms_label": {
        "en": "Scale Weight Norms",
        "ko": "가중치 노름(Norm) 스케일링",
    },
    "net_scale_weight_norms_info": {
        "en": "Scaling factor for weights (1 is a good starting point)",
        "ko": "가중치 스케일링 계수 (1이 적당한 시작값)",
    },
    "net_network_args_label": {"en": "Network Arguments", "ko": "Network 추가 인자"},
    "net_network_args_placeholder": {
        "en": "Additional network arguments (key=value)",
        "ko": "추가 network 인자 (key=value 형식)",
    },
    "net_base_weights_label": {"en": "Base Weights", "ko": "Base Weights"},
    "net_base_weights_placeholder": {
        "en": "Paths to network weights to merge into the model before training",
        "ko": "학습 전 모델에 병합할 network 가중치 경로",
    },
    "net_base_weights_multiplier_label": {
        "en": "Base Weights Multiplier",
        "ko": "Base Weights 배율",
    },
    "net_base_weights_multiplier_placeholder": {
        "en": "Multipliers for network weights to merge into the model before training",
        "ko": "학습 전 모델에 병합할 network 가중치의 배율",
    },
    "net_training_comment_label": {"en": "Training Comment", "ko": "학습 코멘트"},
    "net_training_comment_placeholder": {
        "en": "Arbitrary comment string to store in metadata",
        "ko": "메타데이터에 저장할 임의의 코멘트 문자열",
    },
    "net_no_metadata_label": {
        "en": "Do Not Save Metadata",
        "ko": "메타데이터 저장 안 함",
    },

    # --- class_optimizer_and_scheduler.py -------------------------------------
    "opt_learning_rate_label": {"en": "Learning Rate", "ko": "학습률"},
    "opt_learning_rate_info": {
        "en": "Specify the learning rate (e.g., 2.0e-6)",
        "ko": "학습률을 지정하세요 (예: 2.0e-6)",
    },
    "opt_optimizer_type_label": {"en": "Optimizer Type", "ko": "Optimizer 종류"},
    "opt_optimizer_type_info": {
        "en": "Select the optimizer to use",
        "ko": "사용할 optimizer를 선택하세요",
    },
    "opt_optimizer_args_label": {"en": "Optimizer Arguments", "ko": "Optimizer 추가 인자"},
    "opt_optimizer_args_placeholder": {
        "en": 'Additional arguments for optimizer (e.g., "weight_decay=0.01 betas=0.9,0.999")',
        "ko": '추가 optimizer 인자 (예: "weight_decay=0.01 betas=0.9,0.999")',
    },
    "opt_max_grad_norm_label": {"en": "Max Gradient Norm", "ko": "최대 Gradient Norm"},
    "opt_max_grad_norm_info": {
        "en": "Maximum gradient norm (0 for no clipping)",
        "ko": "최대 gradient norm (0이면 clipping 없음)",
    },
    "opt_lr_scheduler_label": {
        "en": "Learning Rate Scheduler",
        "ko": "학습률 스케줄러",
    },
    "opt_lr_scheduler_info": {
        "en": "Select the learning rate scheduler to use",
        "ko": "사용할 학습률 스케줄러를 선택하세요",
    },
    "opt_lr_warmup_steps_label": {"en": "LR Warmup Steps", "ko": "LR Warmup 스텝 수"},
    "opt_lr_warmup_steps_info": {
        "en": "Number of warmup steps or ratio of train steps (e.g., 0.1 for 10%)",
        "ko": "Warmup 스텝 수 또는 전체 학습 스텝 대비 비율 (예: 0.1 = 10%)",
    },
    "opt_lr_decay_steps_label": {"en": "LR Decay Steps", "ko": "LR Decay 스텝 수"},
    "opt_lr_decay_steps_info": {
        "en": "Number of decay steps or ratio of train steps (e.g., 0.1 for 10%)",
        "ko": "Decay 스텝 수 또는 전체 학습 스텝 대비 비율 (예: 0.1 = 10%)",
    },
    "opt_lr_scheduler_num_cycles_label": {
        "en": "LR Scheduler Num Cycles",
        "ko": "LR Scheduler 반복 횟수",
    },
    "opt_lr_scheduler_num_cycles_info": {
        "en": "Number of restarts for cosine scheduler with restarts",
        "ko": "재시작 포함 cosine 스케줄러의 재시작 횟수",
    },
    "opt_lr_scheduler_power_label": {
        "en": "LR Scheduler Polynomial Power",
        "ko": "LR Scheduler 다항식 지수",
    },
    "opt_lr_scheduler_power_info": {
        "en": "Polynomial power for polynomial scheduler",
        "ko": "polynomial 스케줄러의 다항식 지수",
    },
    "opt_lr_scheduler_timescale_label": {
        "en": "LR Scheduler Timescale",
        "ko": "LR Scheduler Timescale",
    },
    "opt_lr_scheduler_timescale_info": {
        "en": "Timescale for inverse sqrt scheduler (defaults to num_warmup_steps)",
        "ko": "inverse sqrt 스케줄러의 timescale (기본값은 num_warmup_steps)",
    },
    "opt_lr_scheduler_min_lr_ratio_label": {
        "en": "LR Scheduler Min LR Ratio",
        "ko": "LR Scheduler 최소 LR 비율",
    },
    "opt_lr_scheduler_min_lr_ratio_info": {
        "en": "Minimum LR as a ratio of initial LR for cosine with min LR scheduler",
        "ko": "최소 LR 포함 cosine 스케줄러에서 초기 LR 대비 최소 LR 비율",
    },
    "opt_lr_scheduler_type_label": {"en": "LR Scheduler Type", "ko": "LR Scheduler 타입"},
    "opt_lr_scheduler_type_placeholder": {
        "en": "Specify custom scheduler module",
        "ko": "사용자 지정 스케줄러 module을 입력하세요",
    },
    "opt_lr_scheduler_args_label": {
        "en": "LR Scheduler Arguments",
        "ko": "LR Scheduler 추가 인자",
    },
    "opt_lr_scheduler_args_placeholder": {
        "en": 'Additional arguments for scheduler (e.g., "T_max=100")',
        "ko": '추가 스케줄러 인자 (예: "T_max=100")',
    },

    # --- class_save_load.py: Save/Load tab ------------------------------------
    "sl_output_dir_label": {"en": "Output Directory", "ko": "출력 디렉토리"},
    "sl_output_dir_placeholder": {
        "en": "Directory to save the trained model",
        "ko": "학습된 모델을 저장할 디렉토리",
    },
    "sl_output_name_label": {"en": "Output Name", "ko": "출력 이름"},
    "sl_output_name_placeholder": {
        "en": "Base name of the trained model file (excluding extension)",
        "ko": "학습된 모델 파일의 기본 이름 (확장자 제외)",
    },
    "sl_save_precision_label": {"en": "Save Precision", "ko": "저장 정밀도"},
    "sl_save_precision_info": {
        "en": "Precision for saved network weights (default: fp32)",
        "ko": "저장할 network 가중치의 정밀도 (기본값: fp32)",
    },
    "sl_resume_label": {"en": "Resume Training State", "ko": "학습 상태 재개"},
    "sl_resume_placeholder": {
        "en": "Path to saved state to resume training",
        "ko": "학습을 재개할 저장된 상태 경로",
    },
    "sl_save_every_n_epochs_label": {
        "en": "Save Every N Epochs",
        "ko": "N 에포크마다 저장",
    },
    "sl_save_every_n_epochs_info": {
        "en": "Save a checkpoint every N epochs",
        "ko": "N 에포크마다 체크포인트를 저장합니다",
    },
    "sl_save_last_n_epochs_label": {
        "en": "Save Last N Epochs",
        "ko": "최근 N 에포크만 저장",
    },
    "sl_save_last_n_epochs_info": {
        "en": "Save only the last N checkpoints when saving every N epochs",
        "ko": "N 에포크마다 저장 시 최근 N개의 체크포인트만 유지합니다",
    },
    "sl_save_every_n_steps_label": {
        "en": "Save Every N Steps",
        "ko": "N 스텝마다 저장",
    },
    "sl_save_every_n_steps_info": {
        "en": "Save a checkpoint every N steps",
        "ko": "N 스텝마다 체크포인트를 저장합니다",
    },
    "sl_save_last_n_steps_label": {
        "en": "Save Last N Steps",
        "ko": "최근 N 스텝만 저장",
    },
    "sl_save_last_n_steps_info": {
        "en": "Save checkpoints until N steps elapsed (remove older ones afterward)",
        "ko": "N 스텝이 지날 때까지 체크포인트를 저장하고 이후 오래된 것은 삭제합니다",
    },
    "sl_save_last_n_epochs_state_label": {
        "en": "Save Last N Epochs State",
        "ko": "최근 N 에포크 상태 저장",
    },
    "sl_save_last_n_epochs_state_info": {
        "en": "Save states of the last N epochs (overrides save_last_n_epochs)",
        "ko": "최근 N 에포크의 상태를 저장합니다 (save_last_n_epochs보다 우선)",
    },
    "sl_save_last_n_steps_state_label": {
        "en": "Save Last N Steps State",
        "ko": "최근 N 스텝 상태 저장",
    },
    "sl_save_last_n_steps_state_info": {
        "en": "Save states until N steps elapsed (overrides save_last_n_steps)",
        "ko": "N 스텝이 지날 때까지 상태를 저장합니다 (save_last_n_steps보다 우선)",
    },
    "sl_save_state_label": {"en": "Save Training State", "ko": "학습 상태 저장"},
    "sl_save_state_on_train_end_label": {
        "en": "Save State on Train End",
        "ko": "학습 종료 시 상태 저장",
    },

    # --- class_metadata.py: Metadata tab --------------------------------------
    "md_title_label": {"en": "Metadata title", "ko": "메타데이터 제목"},
    "md_title_placeholder": {
        "en": "(optional) title for model metadata (default is output_name)",
        "ko": "(선택) 모델 메타데이터 제목 (기본값은 output_name)",
    },
    "md_author_label": {"en": "Metadata author", "ko": "메타데이터 작성자"},
    "md_author_placeholder": {
        "en": "(optional) author name for model metadata",
        "ko": "(선택) 모델 메타데이터의 작성자 이름",
    },
    "md_description_label": {"en": "Metadata description", "ko": "메타데이터 설명"},
    "md_description_placeholder": {
        "en": "(optional) description for model metadata",
        "ko": "(선택) 모델 메타데이터 설명",
    },
    "md_license_label": {"en": "Metadata license", "ko": "메타데이터 라이선스"},
    "md_license_placeholder": {
        "en": "(optional) license for model metadata",
        "ko": "(선택) 모델 메타데이터 라이선스",
    },
    "md_tags_label": {"en": "Metadata tags", "ko": "메타데이터 태그"},
    "md_tags_placeholder": {
        "en": "(optional) tags for model metadata, separated by comma",
        "ko": "(선택) 모델 메타데이터 태그 (쉼표로 구분)",
    },

    # --- class_huggingface.py: HuggingFace tab --------------------------------
    "hf_repo_id_label": {"en": "Huggingface repo id", "ko": "Huggingface repo id"},
    "hf_repo_id_placeholder": {
        "en": "huggingface repo id",
        "ko": "huggingface repo id",
    },
    "hf_token_label": {"en": "Huggingface token", "ko": "Huggingface 토큰"},
    "hf_token_placeholder": {"en": "huggingface token", "ko": "huggingface 토큰"},
    "hf_repo_type_label": {"en": "Huggingface repo type", "ko": "Huggingface repo 타입"},
    "hf_repo_type_placeholder": {
        "en": "huggingface repo type",
        "ko": "huggingface repo 타입",
    },
    "hf_repo_visibility_label": {
        "en": "Huggingface repo visibility",
        "ko": "Huggingface repo 공개 설정",
    },
    "hf_repo_visibility_placeholder": {
        "en": "huggingface repo visibility",
        "ko": "huggingface repo 공개 설정",
    },
    "hf_path_in_repo_label": {
        "en": "Huggingface path in repo",
        "ko": "Huggingface repo 내 경로",
    },
    "hf_path_in_repo_placeholder": {
        "en": "huggingface path in repo",
        "ko": "huggingface repo 내 경로",
    },
    "hf_save_state_label": {
        "en": "Save state to huggingface",
        "ko": "Huggingface에 상태 저장",
    },
    "hf_resume_label": {"en": "Resume from huggingface", "ko": "Huggingface에서 재개"},
    "hf_resume_placeholder": {
        "en": "resume from huggingface",
        "ko": "huggingface에서 재개",
    },
    "hf_async_upload_label": {"en": "Async upload", "ko": "비동기 업로드"},

    # --- class_accelerate_launch.py -------------------------------------------
    "al_resource_selection_title": {
        "en": "Resource Selection",
        "ko": "리소스 선택",
    },
    "al_mixed_precision_label": {"en": "Mixed precision", "ko": "혼합 정밀도"},
    "al_mixed_precision_info": {
        "en": "Whether or not to use mixed precision training.",
        "ko": "혼합 정밀도 학습을 사용할지 여부입니다.",
    },
    "al_num_processes_label": {"en": "Number of processes", "ko": "프로세스 수"},
    "al_num_processes_info": {
        "en": "The total number of processes to be launched in parallel.",
        "ko": "병렬로 실행할 전체 프로세스 수입니다.",
    },
    "al_num_machines_label": {"en": "Number of machines", "ko": "머신 수"},
    "al_num_machines_info": {
        "en": "The total number of machines used in this training.",
        "ko": "이 학습에 사용할 전체 머신 수입니다.",
    },
    "al_num_cpu_threads_per_process_label": {
        "en": "Number of CPU threads per core",
        "ko": "코어당 CPU 스레드 수",
    },
    "al_num_cpu_threads_per_process_info": {
        "en": "The number of CPU threads per process.",
        "ko": "프로세스당 CPU 스레드 수입니다.",
    },
    "al_dynamo_backend_label": {"en": "Dynamo backend", "ko": "Dynamo backend"},
    "al_dynamo_backend_info": {
        "en": "The backend to use for the dynamo JIT compiler.",
        "ko": "dynamo JIT 컴파일러에 사용할 backend입니다.",
    },
    "al_dynamo_mode_label": {"en": "Dynamo mode", "ko": "Dynamo mode"},
    "al_dynamo_mode_info": {
        "en": "Choose a mode to optimize your training with dynamo.",
        "ko": "dynamo로 학습을 최적화할 모드를 선택하세요.",
    },
    "al_dynamo_use_fullgraph_label": {
        "en": "Dynamo use fullgraph",
        "ko": "Dynamo fullgraph 사용",
    },
    "al_dynamo_use_fullgraph_info": {
        "en": "Whether to use full graph mode for dynamo or it is ok to break model into several subgraphs",
        "ko": "dynamo에서 full graph 모드를 사용할지, 모델을 여러 subgraph로 나눠도 되는지 여부",
    },
    "al_dynamo_use_dynamic_label": {
        "en": "Dynamo use dynamic",
        "ko": "Dynamo dynamic 사용",
    },
    "al_dynamo_use_dynamic_info": {
        "en": "Whether to enable dynamic shape tracing.",
        "ko": "dynamic shape tracing을 활성화할지 여부입니다.",
    },
    "al_hardware_selection_title": {
        "en": "Hardware Selection",
        "ko": "하드웨어 선택",
    },
    "al_multi_gpu_label": {"en": "Multi GPU", "ko": "Multi GPU"},
    "al_multi_gpu_info": {
        "en": "Whether or not this should launch a distributed GPU training.",
        "ko": "분산 GPU 학습을 실행할지 여부입니다.",
    },
    "al_distributed_gpus_title": {"en": "Distributed GPUs", "ko": "분산 GPU"},
    "al_gpu_ids_label": {"en": "GPU IDs", "ko": "GPU ID"},
    "al_gpu_ids_placeholder": {"en": "example: 0,1", "ko": "예: 0,1"},
    "al_gpu_ids_info": {
        "en": "What GPUs (by id) should be used for training on this machine as a comma-separated list",
        "ko": "이 머신에서 학습에 사용할 GPU를 id로 쉼표 구분하여 지정하세요",
    },
    "al_main_process_port_label": {
        "en": "Main process port",
        "ko": "Main process 포트",
    },
    "al_main_process_port_info": {
        "en": "The port to use to communicate with the machine of rank 0.",
        "ko": "rank 0 머신과 통신할 포트입니다.",
    },
    "al_extra_args_label": {
        "en": "Extra accelerate launch arguments",
        "ko": "추가 accelerate launch 인자",
    },
    "al_extra_args_placeholder": {
        "en": "example: --same_network --machine_rank 4",
        "ko": "예: --same_network --machine_rank 4",
    },
    "al_extra_args_info": {
        "en": "List of extra parameters to pass to accelerate launch",
        "ko": "accelerate launch에 전달할 추가 파라미터 목록",
    },

    # --- class_advanced_training.py -------------------------------------------
    "adv_additional_parameters_label": {
        "en": "Additional parameters",
        "ko": "추가 파라미터",
    },
    "adv_additional_parameters_placeholder": {
        "en": '(Optional) Use to provide additional parameters not handled by the GUI. Eg: --some_parameters "value"',
        "ko": '(선택) GUI에서 다루지 않는 추가 파라미터를 입력하세요. 예: --some_parameters "value"',
    },

    # --- class_tensorboard.py --------------------------------------------------
    "tb_start_button": {"en": "Start tensorboard", "ko": "Tensorboard 시작"},
    "tb_stop_button": {"en": "Stop tensorboard", "ko": "Tensorboard 중지"},
    "tb_open_button": {"en": "Open tensorboard", "ko": "Tensorboard 열기"},

    # --- gui.py: top-level tabs -----------------------------------------------
    "tab_musubi_tuner": {"en": "Musubi Tuner", "ko": "Musubi Tuner"},
    "tab_dataset_config": {"en": "Dataset Config", "ko": "Dataset Config"},
    "tab_output": {"en": "📁 Output", "ko": "📁 Output"},
    "tab_settings": {"en": "Settings", "ko": "Settings"},
    "tab_about": {"en": "About", "ko": "About"},
    "tab_readme": {"en": "README", "ko": "README"},

    # --- lora_gui.py: accordion / tab titles -----------------------------------
    "lora_print_command_button": {
        "en": "🖨️ Print training command",
        "ko": "🖨️ 학습 명령어 출력",
    },
    "lora_config_file_settings_title": {
        "en": "⚙️ Configuration File Settings",
        "ko": "⚙️ Configuration File 설정",
    },
    "lora_accelerate_launch_settings_title": {
        "en": "🚀 Accelerate Launch Settings",
        "ko": "🚀 Accelerate Launch 설정",
    },
    "lora_model_settings_title": {"en": "🧠 Model Settings", "ko": "🧠 Model 설정"},
    "lora_caching_title": {"en": "💾 Caching", "ko": "💾 Caching (캐싱)"},
    "lora_latent_caching_tab": {"en": "🖼️ Latent caching", "ko": "🖼️ Latent 캐싱"},
    "lora_text_encoder_caching_tab": {
        "en": "📝 Text encoder caching",
        "ko": "📝 Text Encoder 캐싱",
    },
    "lora_network_settings_title": {
        "en": "🕸️ Network Settings",
        "ko": "🕸️ Network 설정",
    },
    "lora_optimizer_settings_title": {
        "en": "📉 Optimizer and Scheduler Settings",
        "ko": "📉 Optimizer / Scheduler 설정",
    },
    "lora_training_settings_title": {
        "en": "🏋️ Training Settings",
        "ko": "🏋️ Training 설정",
    },
    "lora_advanced_settings_title": {
        "en": "🧪 Advanced Settings",
        "ko": "🧪 고급 설정",
    },
    "lora_save_load_settings_title": {
        "en": "📦 Save / Load Settings",
        "ko": "📦 Save / Load 설정",
    },
    "lora_metadata_settings_title": {
        "en": "🏷️ Metadata Settings",
        "ko": "🏷️ Metadata 설정",
    },
    "lora_huggingface_settings_title": {
        "en": "☁️ HuggingFace Settings",
        "ko": "☁️ HuggingFace 설정",
    },
    "ce_start_training_button": {"en": "▶️ Start training", "ko": "▶️ 학습 시작"},
    "ce_stop_training_button": {"en": "⏹️ Stop training", "ko": "⏹️ 학습 중지"},

    # --- class_configuration_file.py -------------------------------------------
    "cf_load_save_label": {
        "en": "Load/Save Config file",
        "ko": "Config 파일 불러오기/저장",
    },
    "cf_browse_button": {"en": "📂 Browse…", "ko": "📂 찾아보기…"},

    # --- lora_gui.py: Musubi Tuner tab intro --------------------------------
    "lora_tab_intro": {
        "en": (
            "Configure and launch a musubi-tuner training run. Sections follow the "
            "workflow top to bottom:\n\n"
            "1. **Model** — pick the architecture and its checkpoints.\n"
            "2. **Caching** — precompute latents and text encoder outputs.\n"
            "3. **Network**, **Optimizer**, and **Training** — the training recipe.\n"
            "4. **Save / Load**, **Metadata**, and **HuggingFace** — what gets written out.\n\n"
            "When ready, use the bar below to print the command or start training."
        ),
        "ko": (
            "musubi-tuner 학습 실행을 설정하고 시작합니다. 각 섹션은 위에서 아래로 "
            "다음 순서를 따릅니다:\n\n"
            "1. **Model** — 아키텍처와 체크포인트를 선택합니다.\n"
            "2. **Caching** — latent와 text encoder 출력을 미리 계산합니다.\n"
            "3. **Network**, **Optimizer**, **Training** — 학습 레시피입니다.\n"
            "4. **Save / Load**, **Metadata**, **HuggingFace** — 저장되는 항목입니다.\n\n"
            "준비되면 아래 바에서 명령어를 출력하거나 학습을 시작하세요."
        ),
    },

    # --- dataset_config_gui.py: tab intro -----------------------------------
    "dataset_config_tab_intro": {
        "en": (
            "Create, open, edit, validate, and save a musubi-tuner dataset TOML file. "
            "Comments in hand-written files are not preserved on save; unknown/advanced "
            "keys are preserved untouched.\n\n"
            "**How to build a dataset from scratch:**\n"
            "1. Set defaults in **General** below (they apply to every dataset unless overridden per-dataset).\n"
            "2. Pick a *Dataset type* under **Selected dataset**, then click **Browse** next to *Source path* "
            "and choose your image/video folder (or jsonl file) — this creates a new row in **Datasets** for you.\n"
            "3. Fill in the rest of the fields for that dataset (cache directory, caption extension, etc.), then click "
            "**Apply changes** to save them into the row.\n"
            "4. Repeat step 2-3 for more datasets, or click a row in the **Datasets** table to switch which one you're editing.\n"
            "5. Check **Validation** — ERRORs block saving, WARNINGs don't — then click **Save** or **Save as**."
        ),
        "ko": (
            "musubi-tuner 데이터셋 TOML 파일을 만들고, 열고, 편집하고, 검증하고, 저장합니다. "
            "직접 작성한 파일의 주석은 저장 시 유지되지 않습니다. 알 수 없는/고급 키는 "
            "그대로 보존됩니다.\n\n"
            "**처음부터 데이터셋 만드는 방법:**\n"
            "1. 아래 **General**에서 기본값을 설정합니다 (데이터셋별로 재정의하지 않는 한 모든 데이터셋에 적용됩니다).\n"
            "2. **Selected dataset**에서 *Dataset type*을 선택한 뒤, *Source path* 옆 **Browse**를 클릭해 "
            "이미지/영상 폴더(또는 jsonl 파일)를 선택합니다 — **Datasets**에 새 행이 생성됩니다.\n"
            "3. 해당 데이터셋의 나머지 필드(cache directory, caption extension 등)를 채운 뒤, "
            "**Apply changes**를 클릭해 행에 저장합니다.\n"
            "4. 데이터셋을 더 추가하려면 2-3단계를 반복하거나, **Datasets** 표의 행을 클릭해 편집 대상을 바꿉니다.\n"
            "5. **Validation**을 확인하세요 — ERROR는 저장을 막고 WARNING은 막지 않습니다 — 그 후 "
            "**Save** 또는 **Save as**를 클릭합니다."
        ),
    },

    # --- class_model.py: registered Dataset Config quick-pick -------------
    "quickpick_dataset_config_label": {
        "en": "↳ Or pick from a registered Dataset Config (no Browse dialog — safe for remote use)",
        "ko": "↳ 또는 등록된 Dataset Config에서 선택 (Browse 없이, 원격에서도 안전)",
    },
    "refresh": {"en": "🔄 Refresh", "ko": "🔄 새로고침"},

    # --- dataset_config_gui.py: upload accordion ---------------------------
    "upload_accordion_title": {
        "en": "📤 Dataset Upload (remote-friendly)",
        "ko": "📤 데이터셋 업로드 (원격 지원)",
    },
    "upload_desc": {
        "en": (
            "Uses your browser's own drag-and-drop / file picker — works fine over a remote "
            "(web) session too (unlike the 📁 Browse buttons elsewhere, this never opens a "
            "native file dialog on this PC's desktop). Uploaded files are saved to "
            "`./Dataset/<name>/images`, and a ready-to-use dataset config file is "
            "auto-generated and registered."
        ),
        "ko": (
            "브라우저의 드래그 앤 드롭 / 파일 선택창을 사용합니다 — 원격 접속(웹)에서도 정상 작동합니다 "
            "(다른 곳의 📁 Browse 버튼과 달리 이 PC 데스크톱 파일창을 띄우지 않습니다). "
            "업로드한 파일은 `./Dataset/<이름>/images` 에 저장되고, "
            "바로 쓸 수 있는 데이터셋 설정 파일이 자동으로 생성/등록됩니다."
        ),
    },
    "upload_name_label": {
        "en": "Dataset name (used as folder name)",
        "ko": "데이터셋 이름 (폴더명으로 사용)",
    },
    "upload_name_placeholder": {"en": "e.g. my_character", "ko": "예: my_character"},
    "upload_dir_label": {
        "en": "📁 Upload a folder (drag & drop or click)",
        "ko": "📁 폴더 업로드 (드래그 앤 드롭 또는 클릭)",
    },
    "upload_multi_label": {
        "en": "📄 Or select multiple files (images + caption .txt)",
        "ko": "📄 또는 파일 여러 개 선택 (이미지 + 캡션 .txt)",
    },
    "upload_btn": {
        "en": "⬆️ Upload & register dataset",
        "ko": "⬆️ 업로드 & 데이터셋 등록",
    },
    "upload_reset_btn": {
        "en": "🔄 Reset (start a new one)",
        "ko": "🔄 전체 초기화 (새로 시작)",
    },
    "upload_gallery_label": {
        "en": "Uploaded images / captions",
        "ko": "업로드된 이미지 / 캡션",
    },
    "registered_dataset_dropdown_label": {
        "en": "Registered Dataset Config",
        "ko": "등록된 Dataset Config",
    },
    "load_button": {"en": "📥 Load", "ko": "📥 불러오기"},
    "register_path_button": {
        "en": "📌 Register current path",
        "ko": "📌 현재 경로 등록",
    },
    "dataset_preview_accordion_title": {
        "en": "🖼️ Dataset Preview",
        "ko": "🖼️ Dataset Preview",
    },
    "dataset_preview_desc": {
        "en": (
            "Selecting a row above previews it automatically below. Edit Source path / "
            "Cache directory / Caption Extension and click the button to re-check."
        ),
        "ko": (
            "위에서 데이터셋 행을 선택하면 자동으로 미리보기가 뜹니다. "
            "Source path / Cache directory / Caption Extension을 수정한 뒤 새로 확인하려면 버튼을 누르세요."
        ),
    },
    "preview_this_dataset_button": {
        "en": "🔍 Preview this dataset",
        "ko": "🔍 이 데이터셋 미리보기",
    },
    "image_caption_gallery_label": {"en": "Images / captions", "ko": "이미지 / 캡션"},

    # --- dataset_config_gui.py: dataset builder editor ----------------------
    "dataset_file_label": {"en": "Dataset Config File", "ko": "Dataset Config 파일"},
    "dataset_file_placeholder": {
        "en": "Path to the dataset TOML file",
        "ko": "데이터셋 TOML 파일 경로",
    },
    "open_button": {"en": "📂 Open…", "ko": "📂 열기…"},
    "save_button": {"en": "💾 Save", "ko": "💾 저장"},
    "save_as_button": {"en": "💾 Save as…", "ko": "💾 다른 이름으로 저장…"},
    "general_accordion_title": {"en": "⚙️ General", "ko": "⚙️ General (기본값)"},
    "general_resolution_label": {"en": "Resolution (W,H)", "ko": "해상도 (W,H)"},
    "general_caption_ext_label": {
        "en": "Caption Extension",
        "ko": "캡션 확장자",
    },
    "general_batch_size_label": {"en": "Batch Size", "ko": "배치 크기"},
    "general_num_repeats_label": {"en": "Num Repeats", "ko": "반복 횟수"},
    "general_enable_bucket_label": {"en": "Enable Bucket", "ko": "Bucket 사용"},
    "general_bucket_no_upscale_label": {
        "en": "Bucket No Upscale",
        "ko": "Bucket 업스케일 안 함",
    },
    "datasets_accordion_title": {"en": "📚 Datasets", "ko": "📚 Datasets (데이터셋 목록)"},
    "datasets_accordion_desc": {
        "en": (
            "One row per `[[datasets]]` entry that will be written to the file. "
            "Select a row below to edit it in **Selected dataset**."
        ),
        "ko": (
            "파일에 기록될 `[[datasets]]` 항목마다 한 행씩 표시됩니다. "
            "아래에서 행을 선택하면 **Selected dataset**에서 편집할 수 있습니다."
        ),
    },
    "add_image_dataset_button": {
        "en": "🖼️ Add image dataset",
        "ko": "🖼️ 이미지 데이터셋 추가",
    },
    "add_video_dataset_button": {
        "en": "🎬 Add video dataset",
        "ko": "🎬 영상 데이터셋 추가",
    },
    "duplicate_selected_button": {
        "en": "📄 Duplicate selected",
        "ko": "📄 선택 항목 복제",
    },
    "remove_selected_button": {"en": "🗑️ Remove selected", "ko": "🗑️ 선택 항목 삭제"},
    "datasets_table_header_index": {"en": "#", "ko": "#"},
    "datasets_table_header_type": {"en": "Type", "ko": "종류"},
    "datasets_table_header_source": {"en": "Source", "ko": "Source"},
    "datasets_table_header_cache_dir": {"en": "Cache dir", "ko": "Cache dir"},
    "datasets_table_header_repeats": {"en": "Repeats", "ko": "반복"},
    "selected_dataset_accordion_title": {
        "en": "✏️ Selected dataset",
        "ko": "✏️ 선택된 데이터셋",
    },
    "dataset_type_label": {"en": "Dataset type", "ko": "데이터셋 종류"},
    "dataset_type_image_directory": {"en": "Image directory", "ko": "이미지 폴더"},
    "dataset_type_image_jsonl": {"en": "Image JSONL file", "ko": "이미지 JSONL 파일"},
    "dataset_type_video_directory": {"en": "Video directory", "ko": "영상 폴더"},
    "dataset_type_video_jsonl": {"en": "Video JSONL file", "ko": "영상 JSONL 파일"},
    "paths_header": {"en": "**Paths**", "ko": "**Paths (경로)**"},
    "source_path_label": {"en": "Source path", "ko": "Source path (원본 경로)"},
    "cache_directory_label": {"en": "Cache directory", "ko": "Cache directory (캐시 경로)"},
    "control_directory_label": {
        "en": "Control directory",
        "ko": "Control directory (제어 이미지 경로)",
    },
    "overrides_header": {
        "en": "**Overrides** (blank = use the General default above)",
        "ko": "**Overrides (재정의)** (비워두면 위 General 기본값 사용)",
    },
    "caption_ext_override_label": {
        "en": "Caption Extension (override)",
        "ko": "캡션 확장자 (재정의)",
    },
    "resolution_override_label": {
        "en": "Resolution override (W,H)",
        "ko": "해상도 재정의 (W,H)",
    },
    "batch_size_override_label": {
        "en": "Batch Size override",
        "ko": "배치 크기 재정의",
    },
    "num_repeats_override_label": {
        "en": "Num Repeats",
        "ko": "반복 횟수 재정의",
    },
    "enable_bucket_override_label": {
        "en": "Enable Bucket override",
        "ko": "Bucket 사용 재정의",
    },
    "bucket_no_upscale_override_label": {
        "en": "Bucket No Upscale override",
        "ko": "Bucket 업스케일 안 함 재정의",
    },
    "no_resize_control_label": {
        "en": "No Resize Control",
        "ko": "Control 리사이즈 안 함",
    },
    "control_resolution_label": {
        "en": "Control Resolution (W,H)",
        "ko": "Control 해상도 (W,H)",
    },
    "video_only_header": {"en": "**Video-only fields**", "ko": "**영상 전용 필드**"},
    "target_frames_label": {"en": "Target Frames", "ko": "대상 프레임"},
    "frame_extraction_label": {"en": "Frame Extraction", "ko": "프레임 추출 방식"},
    "frame_stride_label": {"en": "Frame Stride", "ko": "프레임 간격"},
    "frame_sample_label": {"en": "Frame Sample", "ko": "프레임 샘플"},
    "max_frames_label": {"en": "Max Frames", "ko": "최대 프레임 수"},
    "source_fps_label": {"en": "Source FPS", "ko": "원본 FPS"},
    "apply_changes_button": {
        "en": "✅ Apply changes to selected dataset",
        "ko": "✅ 선택한 데이터셋에 변경사항 적용",
    },
    "validation_header": {"en": "### 🔍 Validation", "ko": "### 🔍 Validation (검증)"},

    # --- tj_dataset_gui.py: scan_dataset_dirs / upload ----------------------
    "scan_no_source_path": {
        "en": "⚠️ Enter a Source path (image folder).",
        "ko": "⚠️ Source path(이미지 폴더)를 입력하세요.",
    },
    "scan_dir_missing": {
        "en": "❌ Image folder not found: `{image_dir}`",
        "ko": "❌ 이미지 폴더가 없음: `{image_dir}`",
    },
    "scan_no_images": {
        "en": "⚠️ No images found in `{image_dir}`. (supported: {exts})",
        "ko": "⚠️ `{image_dir}` 에 이미지가 없습니다. (지원: {exts})",
    },
    "caption_missing_label": {"en": "❌ no caption | {name}", "ko": "❌ 캡션없음 | {name}"},
    "caption_empty_label": {"en": "⚠️ empty caption | {name}", "ko": "⚠️ 캡션빈칸 | {name}"},
    "cache_line_generic": {
        "en": "\n- 💾 Cache files: **{n_any}** (`{cache_dir}`)",
        "ko": "\n- 💾 캐시 파일: **{n_any}**개 (`{cache_dir}`)",
    },
    "cache_line_specific": {
        "en": (
            "\n- 💾 Latent cache: **{n_latent}** / TEO cache: **{n_te}** "
            "(out of {n_images} images) `{cache_dir}`"
        ),
        "ko": (
            "\n- 💾 latent 캐시: **{n_latent}** / TEO 캐시: **{n_te}** "
            "(이미지 {n_images}개 대비) `{cache_dir}`"
        ),
    },
    "cache_line_none": {
        "en": "\n- 💾 No cache folder yet (not cached yet): `{cache_dir}`",
        "ko": "\n- 💾 캐시 폴더 없음(아직 캐싱 안 함): `{cache_dir}`",
    },
    "scan_status_header": {"en": "### 📁 `{image_dir}`\n", "ko": "### 📁 `{image_dir}`\n"},
    "scan_status_images": {"en": "- Images: **{n_images}**\n", "ko": "- 이미지: **{n_images}**개\n"},
    "scan_status_captions": {
        "en": "- ✅ OK: **{paired}** / ❌ missing: **{missing}** / ⚠️ empty: **{empty}**",
        "ko": "- ✅ 캡션 정상: **{paired}** / ❌ 캡션없음: **{missing}** / ⚠️ 빈캡션: **{empty}**",
    },
    "scan_status_missing_list": {
        "en": "\n\n❌ **Images with no caption:** {show}",
        "ko": "\n\n❌ **캡션 없는 이미지:** {show}",
    },
    "scan_status_empty_list": {
        "en": "\n\n⚠️ **Images with an empty caption:** {show}",
        "ko": "\n\n⚠️ **빈 캡션 이미지:** {show}",
    },
    "scan_status_all_ok": {
        "en": "\n\n🎉 Every image has a matching caption.",
        "ko": "\n\n🎉 모든 이미지에 캡션이 정상으로 짝지어져 있습니다.",
    },
    "toml_not_found": {
        "en": "❌ Dataset TOML not found: `{p}`",
        "ko": "❌ 데이터셋 TOML을 찾을 수 없음: `{p}`",
    },
    "toml_parse_error": {"en": "❌ TOML parse error: {e}", "ko": "❌ TOML 파싱 오류: {e}"},
    "upload_no_files": {
        "en": "⚠️ No files to upload. Select or drag a folder/files.",
        "ko": "⚠️ 업로드할 파일이 없습니다. 폴더나 파일을 선택/드래그하세요.",
    },
    "upload_done_header": {
        "en": "### ✅ Upload complete — `{dest_root}`\n",
        "ko": "### ✅ 업로드 완료 — `{dest_root}`\n",
    },
    "upload_done_counts": {
        "en": "- Uploaded: **{copied}** files → images **{n_images}** / captions(.txt) **{n_captions}**\n",
        "ko": "- 업로드된 파일: **{copied}**개 → 이미지 **{n_images}**개 / 캡션(.txt) **{n_captions}**개\n",
    },
    "upload_done_config": {
        "en": (
            "- Dataset config auto-generated: `{config_path}` (registered — load it "
            "directly from the Dataset Config dropdown)\n"
        ),
        "ko": (
            "- 데이터셋 설정 자동 생성: `{config_path}` "
            "(등록됨, Dataset Config 드롭다운에서 바로 불러오기 가능)\n"
        ),
    },
    "upload_missing_captions_warn": {
        "en": (
            "\n⚠️ {n} image(s) have no caption. Upload a matching .txt file for each."
        ),
        "ko": "\n⚠️ 캡션 없는 이미지가 {n}개 있습니다. 각 이미지와 같은 이름의 .txt 파일도 업로드하세요.",
    },
    "upload_copy_failed": {"en": "\n\n❌ Copy failed: ", "ko": "\n\n❌ 복사 실패: "},

    # --- tj_projects_gui.py: GPU status / live log --------------------------
    "gpu_query_failed": {
        "en": "⚠️ nvidia-smi query failed: {e}",
        "ko": "⚠️ nvidia-smi 조회 실패: {e}",
    },
    "gpu_no_info": {"en": "⚠️ No GPU info", "ko": "⚠️ GPU 정보 없음"},
    "gpu_line": {
        "en": "**{name}** — util **{util}%** · VRAM **{mem_used}/{mem_total} MB** · {temp}°C",
        "ko": "**{name}** — 사용률 **{util}%** · VRAM **{mem_used}/{mem_total} MB** · {temp}°C",
    },
    "gpu_parse_failed": {"en": "⚠️ Failed to parse GPU info", "ko": "⚠️ GPU 정보 파싱 실패"},
    "log_module_load_failed": {
        "en": "(log module failed to load: {e})",
        "ko": "(로그 모듈 로드 실패: {e})",
    },
    "log_never_started": {
        "en": "(Training has never been started)",
        "ko": "(학습이 아직 한 번도 시작되지 않았습니다)",
    },
    "log_no_training_running": {
        "en": "⏹️ No training running",
        "ko": "⏹️ 실행 중인 학습 없음",
    },
    "log_stopped_prefix": {
        "en": "⏹️ Training stopped (last log)\n\n",
        "ko": "⏹️ 학습 종료됨 (마지막 로그)\n\n",
    },
    "log_running_prefix": {"en": "▶️ Training running\n\n", "ko": "▶️ 학습 실행 중\n\n"},
    "folder_no_path": {
        "en": "⚠️ No folder path to open.",
        "ko": "⚠️ 열 폴더 경로가 없습니다.",
    },
    "folder_not_found": {"en": "❌ Folder not found: `{path}`", "ko": "❌ 폴더가 없음: `{path}`"},
    "folder_remote_unsupported": {
        "en": (
            "⚠️ Opening a folder isn't supported over a remote/headless session. "
            "Use Remote Desktop instead."
        ),
        "ko": "⚠️ 원격/헤드리스 세션에서는 폴더 열기를 지원하지 않습니다. 원격데스크톱으로 접속해 사용하세요.",
    },
    "folder_opened": {"en": "📂 Folder opened: `{path}`", "ko": "📂 폴더 열림: `{path}`"},
    "folder_open_failed": {
        "en": "❌ Failed to open folder: {e}",
        "ko": "❌ 폴더 열기 실패: {e}",
    },
    "output_enter_dir": {
        "en": "⚠️ Enter or select an Output Directory.",
        "ko": "⚠️ Output Directory를 선택하거나 입력하세요.",
    },
    "output_dir_missing": {
        "en": "❌ Folder not found: `{output_dir}`",
        "ko": "❌ 폴더가 없음: `{output_dir}`",
    },
    "ckpt_line": {
        "en": "- **{step_label}** — `{name}` ({size})",
        "ko": "- **{step_label}** — `{name}` ({size})",
    },
    "ckpt_header_count": {
        "en": "### 💾 Checkpoints ({n})\n",
        "ko": "### 💾 체크포인트 ({n}개)\n",
    },
    "ckpt_header_none": {
        "en": "### 💾 Checkpoints\n(none saved yet)",
        "ko": "### 💾 체크포인트\n(아직 저장된 체크포인트 없음)",
    },
    "ckpt_step_label": {"en": "step {step}", "ko": "step {step}"},
    "ckpt_final_label": {"en": "final", "ko": "final"},
    "output_status_header": {"en": "### 📁 `{output_dir}`\n", "ko": "### 📁 `{output_dir}`\n"},
    "output_status_ckpts": {
        "en": "- Checkpoints: **{n}** (latest: step {latest_step})\n",
        "ko": "- 체크포인트: **{n}**개 (최신: step {latest_step})\n",
    },
    "output_status_samples": {
        "en": "- Sample images: **{n}** `{sample_dir}`",
        "ko": "- 샘플 이미지: **{n}**장 `{sample_dir}`",
    },
    "output_status_no_sample_dir": {
        "en": (
            "\n\n⚠️ No sample folder yet (no samples generated, or Sample Every N "
            "Steps is 0)"
        ),
        "ko": "\n\n⚠️ sample 폴더 없음 (아직 샘플이 생성되지 않았거나 Sample Every N Steps가 0)",
    },
    "output_tab_title": {"en": "## 📁 Output", "ko": "## 📁 Output"},
    "output_tab_desc": {
        "en": (
            "Every time training starts, its Output Directory is automatically "
            "registered/updated here (existing path: just refreshes last-used time; "
            "new path: added). Select one below to see checkpoints and sample images "
            "in step order."
        ),
        "ko": (
            "학습을 시작할 때마다 해당 Output Directory가 자동으로 목록에 등록/갱신됩니다 "
            "(이미 있는 경로면 최근 사용 시각만 갱신, 새 경로면 추가). "
            "아래에서 선택하면 체크포인트 목록과 학습 중 생성된 샘플 이미지를 스텝 순서로 볼 수 있습니다."
        ),
    },
    "monitor_accordion_title": {
        "en": "🖥️ Live monitoring (GPU / training log)",
        "ko": "🖥️ 실시간 모니터링 (GPU / 학습 로그)",
    },
    "monitor_disclaimer": {
        "en": (
            "⚠️ The training console log only shows runs **started from this GUI's "
            "Start training button**. Training run directly from another window will "
            "only show GPU status, no log."
        ),
        "ko": (
            "⚠️ 학습 콘솔 로그는 **이 GUI(Start training 버튼)로 시작한 학습만** 표시됩니다. "
            "다른 창에서 직접 실행한 학습은 GPU 상태만 보이고 로그는 표시되지 않습니다."
        ),
    },
    "loading_placeholder": {"en": "(loading...)", "ko": "(불러오는 중...)"},
    "live_log_label": {
        "en": "Live training log (last 300 lines)",
        "ko": "실시간 학습 로그 (최근 300줄)",
    },
    "output_dropdown_label": {
        "en": "Output (registered Output Directories)",
        "ko": "Output (등록된 Output Directory)",
    },
    "output_load_button": {"en": "🔍 Load", "ko": "🔍 불러오기"},
    "auto_refresh_checkbox": {
        "en": "⏱️ Auto-refresh (10s)",
        "ko": "⏱️ 자동 새로고침 (10초)",
    },
    "manual_dir_label": {
        "en": "Or enter an Output Directory directly",
        "ko": "또는 Output Directory 직접 입력",
    },
    "manual_dir_placeholder": {
        "en": "e.g. C:/AI/musubi-tj-tuner/my_training/outputs",
        "ko": "예: C:/AI/musubi-tj-tuner/my_training/outputs",
    },
    "browse_button": {"en": "📁 Browse", "ko": "📁 찾아보기"},
    "register_this_path_button": {
        "en": "📌 Register this path",
        "ko": "📌 이 경로 등록",
    },
    "open_folder_button": {"en": "📂 Open folder", "ko": "📂 폴더 열기"},
    "sample_gallery_label": {
        "en": "Sample images (newest step first)",
        "ko": "샘플 이미지 (최신 스텝 먼저)",
    },
    "sample_gallery_accordion_title": {
        "en": "🖼️ Sample Images (click to expand — may be sensitive)",
        "ko": "🖼️ 샘플 이미지 (클릭해서 펼치기 — 민감할 수 있음)",
    },

    # --- class_training.py: sample prompts file editor ----------------------
    "prompts_quickpick_label": {
        "en": "↳ Write/edit the prompt file's content directly (no Browse dialog — safe for remote use)",
        "ko": "↳ 프롬프트 파일 내용을 직접 작성/수정 (Browse 없이, 원격에서도 안전)",
    },
    "prompts_textbox_label": {
        "en": "Prompts (one per line; optional --w --h --s --d --g flags)",
        "ko": "프롬프트 (한 줄에 하나씩, --w --h --s --d --g 옵션 사용 가능)",
    },
    "prompts_textbox_placeholder": {
        "en": (
            "a photo of a woman with red hair, smiling --w 768 --h 1024 --s 20 --d 42 --g 4\n"
            "another prompt on its own line ..."
        ),
        "ko": (
            "a photo of a woman with red hair, smiling --w 768 --h 1024 --s 20 --d 42 --g 4\n"
            "다른 프롬프트는 새 줄에 ..."
        ),
    },
    "prompts_load_button": {"en": "📂 Load from file", "ko": "📂 파일에서 불러오기"},
    "prompts_save_button": {"en": "💾 Save to file", "ko": "💾 파일로 저장"},
    "prompts_no_path": {
        "en": "⚠️ Enter a path in the Sample Prompts field above first (e.g. `./my_training/sample_prompts.txt`), then Save.",
        "ko": "⚠️ 위 Sample Prompts 칸에 경로를 먼저 입력하세요 (예: `./my_training/sample_prompts.txt`), 그다음 저장하세요.",
    },
    "prompts_load_not_found": {
        "en": "⚠️ File not found yet: `{path}` — write your prompts below and click Save to create it.",
        "ko": "⚠️ 아직 파일이 없습니다: `{path}` — 아래에 프롬프트를 작성하고 저장을 누르면 새로 만들어집니다.",
    },
    "prompts_load_ok": {"en": "📂 Loaded from `{path}`", "ko": "📂 `{path}` 에서 불러왔습니다"},
    "prompts_load_failed": {
        "en": "❌ Failed to read file: {e}",
        "ko": "❌ 파일 읽기 실패: {e}",
    },
    "prompts_save_ok": {"en": "✅ Saved to `{path}`", "ko": "✅ `{path}` 에 저장했습니다"},
    "prompts_save_failed": {
        "en": "❌ Failed to save file: {e}",
        "ko": "❌ 파일 저장 실패: {e}",
    },

    # --- class_model.py: resolution / shift mismatch check ------------------
    "resolution_shift_warning": {
        "en": (
            "⚠️ Training resolution is **{w}x{h}** (not the 1024x1024 this fixed Discrete "
            "Flow Shift is calibrated for), but Timestep Sampling Method is `shift` with a "
            "fixed value. This mismatch can cause duplicated/tiled-subject artifacts in "
            "samples. Switch to `krea2_shift` / `flux2_shift` / `flux_shift` above, which "
            "computes the correct shift for this resolution automatically."
        ),
        "ko": (
            "⚠️ 학습 해상도가 **{w}x{h}** 인데(고정 Discrete Flow Shift는 1024x1024 기준으로 캘리브레이션됨), "
            "Timestep Sampling Method가 고정값 `shift`로 되어 있습니다. 이 불일치는 샘플 이미지에서 "
            "인물이 겹쳐 그려지는 등의 결함을 유발할 수 있습니다. 위에서 `krea2_shift` / `flux2_shift` / "
            "`flux_shift`로 바꾸면 이 해상도에 맞는 shift를 자동으로 계산합니다."
        ),
    },

    # --- settings_gui.py: language selector ---------------------------------
    "settings_language_label": {"en": "Language / 언어", "ko": "Language / 언어"},
    "settings_language_info": {
        "en": "Applies to the TJ-added panels (Dataset Preview/Upload, Output tab, "
        "monitoring). Upstream labels stay English. Pick a language and click Apply, "
        "then restart the GUI.",
        "ko": "TJ가 추가한 화면(Dataset Preview/Upload, Output 탭, 모니터링)에 적용됩니다. "
        "원본 항목은 항상 영어로 유지됩니다. 언어를 선택하고 적용 버튼을 누른 뒤 "
        "GUI를 재시작하세요.",
    },
    "settings_tooltip_label": {
        "en": "Enable info tooltips on hover",
        "ko": "마우스 오버 시 안내 툴팁 표시",
    },
    "settings_tooltip_info": {
        "en": "Shows a tooltip with each field's description when hovering its name. Takes effect immediately, no restart needed.",
        "ko": "필드 이름에 마우스를 올리면 설명 툴팁을 표시합니다. 즉시 적용되며 재시작이 필요 없습니다.",
    },
    "settings_language_apply_btn": {"en": "✅ Apply", "ko": "✅ 적용"},
    "settings_language_restart_notice": {
        "en": "Language saved. Click 🔄 Restart GUI (or restart manually) for it to take effect.",
        "ko": "언어가 저장되었습니다. 🔄 GUI 재시작 버튼을 누르거나 수동으로 재시작해주세요.",
    },
    "settings_restart_btn": {"en": "🔄 Restart GUI", "ko": "🔄 GUI 재시작"},
    "settings_restart_notice": {
        "en": "Restarting the GUI process... reload this page in a few seconds.",
        "ko": "GUI를 재시작하는 중입니다... 몇 초 후 이 페이지를 새로고침 해주세요.",
    },
}


def get_language(config) -> str:
    try:
        lang = config.get("settings.language", DEFAULT_LANG)
    except Exception:
        lang = DEFAULT_LANG
    return lang if lang in LANGUAGES else DEFAULT_LANG


def set_language(config, config_file_path, lang: str):
    if lang not in LANGUAGES:
        lang = DEFAULT_LANG
    config.config.setdefault("settings", {})["language"] = lang
    config.save_config(config.config, config_file_path)


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    entry = _T.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get(DEFAULT_LANG, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
