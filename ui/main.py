import gradio as gr

from extensions.webui_tavernai_charas.ui.featured import featured_ui
from extensions.webui_tavernai_charas.ui.downloaded import downloaded_ui


def mount_ui():
    with gr.Tabs():
        with gr.TabItem("Online Characters"):
            gr.Markdown("# Online Characters")

            featured_ui()

        with gr.TabItem("Downloaded"):
            downloaded_ui()
