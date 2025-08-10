import gradio as gr

import user_data.extensions.webui_tavernai_charas.ui.native_fn as nfn
from user_data.extensions.webui_tavernai_charas.ui.featured import featured_ui
from user_data.extensions.webui_tavernai_charas.ui.downloaded import downloaded_ui
from user_data.extensions.webui_tavernai_charas.ui.previewer import previewer_ui
from user_data.extensions.webui_tavernai_charas.ui.shared import components
from user_data.extensions.webui_tavernai_charas.services.tavernai_service import (
    DownloadCardTracker,
)

DOWNLOAD_CARD_TRACKER = DownloadCardTracker()


def on_download_preview_btn():
    card = DOWNLOAD_CARD_TRACKER.get_card()
    return gr.update(value=card.img_url), gr.update(visible=False)


def mount_ui():
    with gr.Tabs(elem_id="tavernai_ext_tabs"):
        with gr.TabItem("Online Characters"):
            featured_ui()

        with gr.TabItem("Card Previewer"):
            previewer_ui()

        with gr.TabItem("Downloaded"):
            downloaded_ui()

    preview_alert_btn: gr.Button = components["preview_card_download"]
    preview_alert_btn.click(
        on_download_preview_btn,
        None,
        [components["preview_url_searcher"], components["download_card_box"]],
        _js=nfn.change_and_search_preview(),
    )
