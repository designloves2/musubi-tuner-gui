import gradio as gr

from .class_gui_config import GUIConfig
from .tj_i18n import t, get_language


class MetaData:
    def __init__(
        self,
        config: GUIConfig = {},
    ) -> None:
        self.config = config
        lang = get_language(config)

        with gr.Row():
            self.metadata_title = gr.Textbox(
                label=t("md_title_label", lang),
                placeholder=t("md_title_placeholder", lang),
                interactive=True,
                value=self.config.get("metadata_title", ""),
            )
            self.metadata_author = gr.Textbox(
                label=t("md_author_label", lang),
                placeholder=t("md_author_placeholder", lang),
                interactive=True,
                value=self.config.get("metadata_author", ""),
            )
        self.metadata_description = gr.Textbox(
            label=t("md_description_label", lang),
            placeholder=t("md_description_placeholder", lang),
            interactive=True,
            value=self.config.get("metadata_description", ""),
        )
        with gr.Row():
            self.metadata_license = gr.Textbox(
                label=t("md_license_label", lang),
                placeholder=t("md_license_placeholder", lang),
                interactive=True,
                value=self.config.get("metadata_license", ""),
            )
            self.metadata_tags = gr.Textbox(
                label=t("md_tags_label", lang),
                placeholder=t("md_tags_placeholder", lang),
                interactive=True,
                value=self.config.get("metadata_tags", ""),
            )

    def run_cmd(run_cmd: list, **kwargs):
        if "metadata_title" in kwargs and kwargs.get("metadata_title") != "":
            run_cmd.append("--metadata_title")
            run_cmd.append(kwargs["metadata_title"])

        if "metadata_author" in kwargs and kwargs.get("metadata_author") != "":
            run_cmd.append("--metadata_author")
            run_cmd.append(kwargs["metadata_author"])

        if (
            "metadata_description" in kwargs
            and kwargs.get("metadata_description") != ""
        ):
            run_cmd.append("--metadata_description")
            run_cmd.append(kwargs["metadata_description"])

        if "metadata_license" in kwargs and kwargs.get("metadata_license") != "":
            run_cmd.append("--metadata_license")
            run_cmd.append(kwargs["metadata_license"])

        if "metadata_tags" in kwargs and kwargs.get("metadata_tags") != "":
            run_cmd.append("--metadata_tags")
            run_cmd.append(kwargs["metadata_tags"])

        return run_cmd
