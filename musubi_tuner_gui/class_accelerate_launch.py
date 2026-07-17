import gradio as gr
import os
import shlex

from .class_gui_config import GUIConfig
from .custom_logging import setup_logging
from .tj_i18n import t, get_language

# Set up logging
log = setup_logging()


class AccelerateLaunch:
    def __init__(
        self,
        config: GUIConfig = {},
    ) -> None:
        self.config = config
        lang = get_language(config)

        with gr.Accordion(t("al_resource_selection_title", lang), open=True):
            with gr.Row():
                self.mixed_precision = gr.Dropdown(
                    label=t("al_mixed_precision_label", lang),
                    choices=["no", "fp16", "bf16", "fp8"],
                    value=self.config.get("mixed_precision", "fp16"),
                    info=t("al_mixed_precision_info", lang),
                )
                self.num_processes = gr.Number(
                    label=t("al_num_processes_label", lang),
                    value=self.config.get("num_processes", 1),
                    # precision=0,
                    step=1,
                    minimum=1,
                    info=t("al_num_processes_info", lang),
                )
                self.num_machines = gr.Number(
                    label=t("al_num_machines_label", lang),
                    value=self.config.get("num_machines", 1),
                    # precision=0,
                    step=1,
                    minimum=1,
                    info=t("al_num_machines_info", lang),
                )
                self.num_cpu_threads_per_process = gr.Slider(
                    minimum=1,
                    maximum=os.cpu_count(),
                    step=1,
                    label=t("al_num_cpu_threads_per_process_label", lang),
                    value=self.config.get("num_cpu_threads_per_process", 2),
                    info=t("al_num_cpu_threads_per_process_info", lang),
                )
            with gr.Row():
                self.dynamo_backend = gr.Dropdown(
                    label=t("al_dynamo_backend_label", lang),
                    choices=[
                        "no",
                        "eager",
                        "aot_eager",
                        "inductor",
                        "aot_ts_nvfuser",
                        "nvprims_nvfuser",
                        "cudagraphs",
                        "ofi",
                        "fx2trt",
                        "onnxrt",
                        "tensorrt",
                        "ipex",
                        "tvm",
                    ],
                    value=self.config.get("dynamo_backend", "no"),
                    info=t("al_dynamo_backend_info", lang),
                )
                self.dynamo_mode = gr.Dropdown(
                    label=t("al_dynamo_mode_label", lang),
                    choices=[
                        "default",
                        "reduce-overhead",
                        "max-autotune",
                    ],
                    value=self.config.get("dynamo_mode", "default"),
                    info=t("al_dynamo_mode_info", lang),
                )
                self.dynamo_use_fullgraph = gr.Checkbox(
                    label=t("al_dynamo_use_fullgraph_label", lang),
                    value=self.config.get("dynamo_use_fullgraph", False),
                    info=t("al_dynamo_use_fullgraph_info", lang),
                )
                self.dynamo_use_dynamic = gr.Checkbox(
                    label=t("al_dynamo_use_dynamic_label", lang),
                    value=self.config.get("dynamo_use_dynamic", False),
                    info=t("al_dynamo_use_dynamic_info", lang),
                )

        with gr.Accordion(t("al_hardware_selection_title", lang), open=True):
            with gr.Row():
                self.multi_gpu = gr.Checkbox(
                    label=t("al_multi_gpu_label", lang),
                    value=self.config.get("multi_gpu", False),
                    info=t("al_multi_gpu_info", lang),
                )
        with gr.Accordion(t("al_distributed_gpus_title", lang), open=True):
            with gr.Row():
                self.gpu_ids = gr.Textbox(
                    label=t("al_gpu_ids_label", lang),
                    value=self.config.get("gpu_ids", ""),
                    placeholder=t("al_gpu_ids_placeholder", lang),
                    info=t("al_gpu_ids_info", lang),
                )

                def validate_gpu_ids(value):
                    if value == "":
                        return
                    if not (value.isdigit() and int(value) >= 0 and int(value) <= 128):
                        log.error("GPU IDs must be an integer between 0 and 128")
                        return
                    else:
                        for id in value.split(","):
                            if not id.isdigit() or int(id) < 0 or int(id) > 128:
                                log.error(
                                    "GPU IDs must be an integer between 0 and 128"
                                )

                self.gpu_ids.blur(fn=validate_gpu_ids, inputs=self.gpu_ids)

                self.main_process_port = gr.Number(
                    label=t("al_main_process_port_label", lang),
                    value=self.config.get("main_process_port", 0),
                    # precision=1,
                    step=1,
                    minimum=0,
                    maximum=65535,
                    info=t("al_main_process_port_info", lang),
                )
        with gr.Row():
            self.extra_accelerate_launch_args = gr.Textbox(
                label=t("al_extra_args_label", lang),
                value=self.config.get("extra_accelerate_launch_args", ""),
                placeholder=t("al_extra_args_placeholder", lang),
                info=t("al_extra_args_info", lang),
            )

    def run_cmd(run_cmd: list, **kwargs):
        if "dynamo_backend" in kwargs and kwargs.get("dynamo_backend"):
            run_cmd.append("--dynamo_backend")
            run_cmd.append(kwargs["dynamo_backend"])

        if "dynamo_mode" in kwargs and kwargs.get("dynamo_mode"):
            run_cmd.append("--dynamo_mode")
            run_cmd.append(kwargs["dynamo_mode"])

        if "dynamo_use_fullgraph" in kwargs and kwargs.get("dynamo_use_fullgraph"):
            run_cmd.append("--dynamo_use_fullgraph")

        if "dynamo_use_dynamic" in kwargs and kwargs.get("dynamo_use_dynamic"):
            run_cmd.append("--dynamo_use_dynamic")

        if (
            "extra_accelerate_launch_args" in kwargs
            and kwargs["extra_accelerate_launch_args"] != ""
        ):
            extra_accelerate_launch_args = kwargs[
                "extra_accelerate_launch_args"
            ].replace('"', "")
            for arg in extra_accelerate_launch_args.split():
                run_cmd.append(shlex.quote(arg))

        if "gpu_ids" in kwargs and kwargs.get("gpu_ids") != "":
            run_cmd.append("--gpu_ids")
            run_cmd.append(shlex.quote(kwargs["gpu_ids"]))

        if "main_process_port" in kwargs and kwargs.get("main_process_port", 0) > 0:
            run_cmd.append("--main_process_port")
            run_cmd.append(str(int(kwargs["main_process_port"])))

        if "mixed_precision" in kwargs and kwargs.get("mixed_precision"):
            run_cmd.append("--mixed_precision")
            run_cmd.append(shlex.quote(kwargs["mixed_precision"]))

        if "multi_gpu" in kwargs and kwargs.get("multi_gpu"):
            run_cmd.append("--multi_gpu")

        if "num_processes" in kwargs and int(kwargs.get("num_processes", 0)) > 0:
            run_cmd.append("--num_processes")
            run_cmd.append(str(int(kwargs["num_processes"])))

        if "num_machines" in kwargs and int(kwargs.get("num_machines", 0)) > 0:
            run_cmd.append("--num_machines")
            run_cmd.append(str(int(kwargs["num_machines"])))

        if (
            "num_cpu_threads_per_process" in kwargs
            and int(kwargs.get("num_cpu_threads_per_process", 0)) > 0
        ):
            run_cmd.append("--num_cpu_threads_per_process")
            run_cmd.append(str(int(kwargs["num_cpu_threads_per_process"])))

        return run_cmd
