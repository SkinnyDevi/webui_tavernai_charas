import re
import gradio as gr

from modules.shared import gradio
from modules.github import clone_or_pull_repository
import modules.ui as ui

from extensions.webui_tavernai_charas.config.config_handler import ConfigHandler
from extensions.webui_tavernai_charas.config.update_manager import ExtUpdateManager
import extensions.webui_tavernai_charas.services.offline_chara_service as offline_chara_service
from extensions.webui_tavernai_charas.services.offline_chara_service import (
    OfflineCharaCard,
)
import extensions.webui_tavernai_charas.ui.native_fn as nfn

DELETE_CARD_INDEX = offline_chara_service.DeleteCardTracker()
CONFIG = ConfigHandler.setup()


def compile_html_downloaded_chara_cards(
    charas: list[OfflineCharaCard] | None = None,
):
    """
    Gets a list of downloaded cards and returns a list of their respective HTML format.
    """

    charas = (
        charas
        if charas is not None
        else offline_chara_service.fetch_downloaded_charas()
    )
    html_cards: list[list] = []

    chara_el = ['<div class="tavernai_chara_card">', None, "</div>"]
    for c in charas:
        image_el = f'<img src="{c.image}">'
        name_el = f"<p>{c.name}</p>"

        element = chara_el.copy()
        element[1] = image_el + name_el

        html_cards.append(["".join(element), c.name])

    return html_cards


def select_character(evt: gr.SelectData):
    """
    Returns the selected character for use.
    """

    return evt.value[1]


def on_delete_btn(
    card_dropdown: gr.Dropdown,
):
    match = re.search(r"\[(\d+)\]", card_dropdown)
    DELETE_CARD_INDEX.set_index(int(match[1]))

    return card_dropdown, gr.update(visible=True)


def on_confirm_delete_btn():
    offline_chara_service.fetch_downloaded_charas()[
        DELETE_CARD_INDEX.get_index()
    ].delete()

    return gr.update(visible=False)


def on_cancel_delete_btn():
    DELETE_CARD_INDEX.reset()
    return gr.update(visible=False)


def search_offline_charas(evt: gr.EventData):
    """
    Searches dynamically for downloaded characters by name.
    """

    search_input: str = evt._data
    if search_input is None or not search_input:
        return gr.update(samples=compile_html_downloaded_chara_cards())

    matches: list[OfflineCharaCard] = [
        chara
        for chara in offline_chara_service.fetch_downloaded_charas()
        if search_input.lower() in chara.name.lower()
    ]

    return gr.update(samples=compile_html_downloaded_chara_cards(matches))


def create_ext_updater():
    update_btn = gr.Button(
        "There is an update available. Click here to download",
        elem_classes=["tavernai_btn_primary", "tavernai-download-update-btn"],
    )
    status = gr.Markdown()
    repo = gr.Textbox(
        visible=False,
        value="https://github.com/SkinnyDevi/webui_tavernai_charas",
    )
    restart_webui = gr.Markdown(
        "Please restart your WebUI using the restart button in the Sessions tab.",
        elem_classes=["tavernai-ext-update"],
        visible=False,
    )

    update_btn.click(
        clone_or_pull_repository,
        repo,
        status,
        show_progress=True,
    ).then(
        lambda: (gr.update(visible=False), gr.update(visible=True)),
        None,
        [status, restart_webui],
    )


def confirm_delete_card():
    with gr.Box(visible=False, elem_classes="file-saver") as delete_card_box:
        delete_card_textbox = gr.Textbox(
            lines=1,
            label="You are about to delete this card:",
            interactive=False,
        )
        with gr.Row(elem_id="tavernai_delete_chara_buttons"):
            confirm_card_delete = gr.Button(
                "Delete",
                elem_classes="small-button",
                variant="stop",
            )
            cancel_card_delete = gr.Button("Cancel", elem_classes="small-button")

            confirm_card_delete.click(
                on_confirm_delete_btn,
                None,
                delete_card_box,
                _js=nfn.refresh_downloaded(),
            )

            cancel_card_delete.click(
                on_cancel_delete_btn,
                None,
                delete_card_box,
            )

    return delete_card_box, delete_card_textbox


def downloaded_ui():
    with gr.Column():
        gr.Markdown("# Downloaded Characters")
        refresh = gr.Button(
            "Refresh", elem_classes="tavernai_refresh_downloaded_charas"
        )
        get_local_cards = offline_chara_service.fetch_downloaded_charas

        confirm_delete_box = confirm_delete_card()
        delete_card_box = confirm_delete_box[0]
        delete_card_textbox = confirm_delete_box[1]

        with gr.Row(elem_id="tavernai_downloaded_handlers"):
            with gr.Column():
                with gr.Row():
                    offline_search_bar = gr.Textbox(
                        placeholder="Search",
                        show_label=False,
                        interactive=True,
                    )

            with gr.Column():
                with gr.Row():
                    all_cards = gr.Dropdown(
                        choices=[
                            f"[{i}] {c.name}" for i, c in enumerate(get_local_cards())
                        ],
                        value=f"[0] {get_local_cards()[0].name}",
                        interactive=True,
                        label="Delete a character",
                        elem_classes=["slim-dropdown tavernai_chara_dropdown_delete"],
                    )
                    all_cards.container = False
                    ui.create_refresh_button(
                        all_cards,
                        lambda: None,
                        lambda: {
                            "choices": [
                                f"[{i}] {c.name}"
                                for i, c in enumerate(get_local_cards())
                            ],
                            "value": f"[0] {get_local_cards()[0].name}",
                        },
                        [
                            "refresh-button",
                            "tavernai_refresh_downloaded_charas",
                        ],
                    )
                    delete_card_btn = gr.Button(
                        ui.delete_symbol, elem_classes=["refresh-button"]
                    )

                    delete_card_btn.click(
                        on_delete_btn,
                        all_cards,
                        [
                            delete_card_textbox,
                            delete_card_box,
                        ],
                    )

        if ExtUpdateManager.check_for_updates(CONFIG):
            create_ext_updater()

        downloaded = gr.Dataset(
            components=[gr.HTML(visible=False)],
            label="",
            samples=compile_html_downloaded_chara_cards(),
            samples_per_page=15,
            elem_classes=["tavernai_downloaded_container"],
        )

        offline_search_bar.change(search_offline_charas, None, downloaded)

        gr.Markdown(
            f"TavernAI Character Extension - Version {CONFIG.version}",
            elem_classes=["tavernai-ext-version"],
        )
        gr.Markdown(
            "Have any issues or feature request? Report them [here](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/new/choose).",
            elem_classes=["tavernai-ext-version"],
        )
        gr.Markdown(
            "Want to support my development? [Donate](https://paypal.me/skinnydevi) to me here! Thank you! :)",
            elem_classes=["tavernai-ext-version"],
        )

    refresh.click(
        lambda: gr.Dataset(samples=compile_html_downloaded_chara_cards()),
        [],
        downloaded,
    )
