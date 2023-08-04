import gradio as gr
import json

from modules.shared import gradio
import modules.ui as ui

import extensions.tavernai_charas.chara_handler as chara_handler
from extensions.tavernai_charas.tavernai_service import TavernAIService, TavernAICard
from extensions.tavernai_charas.config_handler import ConfigHandler


CONFIG = ConfigHandler.setup()


def mount_ui():
    gr.HTML(value=mount_chara_cards_css())
    with gr.Tabs():
        with gr.TabItem("Online Characters"):
            gr.Markdown("# Online Characters")

            with gr.Tabs():
                with gr.TabItem("Featured"):
                    with gr.Row():
                        nsfw_check = gr.CheckboxGroup(
                            ["Allow NSFW"],
                            label="Filters",
                            value=[
                                "Allow NSFW" if CONFIG.get_allow_nsfw() else "",
                            ],
                            interactive=True,
                        )
                        nsfw_check.select(
                            apply_checkbox, [], None, _js=hit_all_refreshes()
                        )

                    recent_charas = create_tavernai_chara_display(
                        "Recent Charas",
                        lambda: TavernAIService.fetch_recent_cards(
                            nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    random_charas = create_tavernai_chara_display(
                        "Random Characters",
                        lambda: TavernAIService.fetch_random_cards(
                            nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    random_categories = TavernAIService.fetch_random_categories(5)

                    cat1 = random_categories[0]
                    create_tavernai_chara_display(
                        f"Category: {cat1.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat1, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat2 = random_categories[1]
                    create_tavernai_chara_display(
                        f"Category: {cat2.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat2, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat3 = random_categories[2]
                    create_tavernai_chara_display(
                        f"Category: {cat3.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat3, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat4 = random_categories[3]
                    create_tavernai_chara_display(
                        f"Category: {cat4.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat4, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat5 = random_categories[4]
                    create_tavernai_chara_display(
                        f"Category: {cat5.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat5, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                with gr.TabItem("Search"):
                    with gr.Row(elem_id="tavernai_search_bar"):
                        search_bar = gr.Textbox(
                            placeholder="Search",
                            show_label=False,
                        )
                        search_btn = gr.Button("Search")

        with gr.TabItem("Downloaded"):
            with gr.Column():
                gr.Markdown("# Downloaded Characters")
                refresh = gr.Button("Refresh")
                with gr.Row(elem_id="tavernai_search_bar"):
                    search_bar = gr.Textbox(
                        placeholder="Search",
                        show_label=False,
                    )
                    search_btn = gr.Button("Search")

                downloaded = gr.Dataset(
                    components=[gr.HTML(visible=False)],
                    label="",
                    samples=compile_html_downloaded_chara_cards(),
                    elem_classes=["tavernai_downloaded_container"],
                )

            refresh.click(
                compile_html_downloaded_chara_cards,
                [],
                downloaded,
            )
            downloaded.select(
                select_character, None, gradio["character_menu"], _js=change_tab()
            )


def apply_checkbox(evt: gr.SelectData):
    key = str(evt.value).lower().replace(" ", "_")

    match key:
        case "allow_nsfw":
            CONFIG.set_allow_nsfw(evt.selected)

    return evt.value


def select_character(evt: gr.SelectData):
    return evt.value[1]


def mount_chara_cards_css():
    css = """
    #tavernai_search_bar > div{
        min-width: 60vw;
    }

    .tavernai_downloaded_container > div:nth-child(2) {
        justify-content: center;
    }

    .tavernai_downloaded_container > div:nth-child(2)::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    .tavernai_downloaded_container > div:nth-child(2)::-webkit-scrollbar-track {
        border-radius: 100vh;
        background: #1f2937;
    }

    .tavernai_downloaded_container > div:nth-child(2)::-webkit-scrollbar-thumb {
        background: var(--body-background-fill);
        border-radius: 100vh;
    }

    .tavernai_downloaded_container > div:nth-child(2)::-webkit-scrollbar-thumb:hover {
        background: var(--table-row-focus);
    }

    .tavernai_downloaded_container > div.label,
    .tavernai_card_display > div.label {
        display: none !important;
    }

    .tavernai_card_display {
        padding: 5px;
        background-color: #1f2937;
        border-radius: 8px;
        border: var(--block-border-width) solid var(--border-color-primary);
    }

    /* aka: tavern_card_slider */
    .tavernai_card_display > div:nth-child(2) {
        display: block !important;
        height: 320px !important;
        overflow-x: scroll !important;
        white-space: nowrap !important;
    }

    .tavernai_chara_card {
        width: 250px;
        height: 265px;
    }

    .tavernai_chara_card>img {
        width: 225px;
        height: 225px;
        background-color: gray;
        object-fit: cover;
        margin: 0 auto;
        border-radius: 1rem;
        margin-bottom: 10px;
        border: 3px solid #354091f9;
    }

    .tavernai_chara_card>p {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-weight: bold;
        font-size: 20px;
    }
    """
    return f"<style>{css}</style>"


def change_tab():
    return """
    () => {
        var tabButtons = document.evaluate("//button[contains(., 'Text generation')]", document, null, XPathResult.ANY_TYPE, null );
        var chatTab = tabButtons.iterateNext();

        chatTab.click();
    }
    """


def hit_all_refreshes():
    return """
    () => {
        var refreshes = document.querySelectorAll(".tavernai_slider_refresh");
        for (let r of refreshes) {
            setTimeout(() => r.click(), 250);
        }
    }
    """


def create_tavernai_chara_display(title, samples):
    with gr.Row():
        gr.Markdown(f"## {title}")
        refresh_button = ui.ToolButton(
            value=ui.refresh_symbol,
            elem_classes=[
                "refresh-button",
                "refresh-button-medium",
                "tavernai_slider_refresh",
            ],
        )

    slider = gr.Dataset(
        components=[gr.HTML(visible=False)],
        label="",
        samples=compile_html_online_chara_cards(samples()),
        elem_classes=["tavernai_downloaded_container tavernai_card_display"],
        samples_per_page=30,
    )

    def download_character(evt: gr.SelectData):
        card = TavernAICard.from_dict(json.loads(evt.value[1]))
        TavernAICard.download_card(card)
        gr.Error(f"Successfully downloaded {card.name} card")

    slider.select(download_character, None, None)

    # copied from ui.create_refresh_button method
    def refresh():
        def refreshed_args():
            return {"samples": compile_html_online_chara_cards(samples())}

        args = refreshed_args() if callable(refreshed_args) else refreshed_args

        for k, v in args.items():
            setattr(slider, k, v)

        return gr.update(**(args or {}))

    refresh_button.click(fn=refresh, inputs=[], outputs=[slider])

    return slider


def compile_html_downloaded_chara_cards():
    charas = chara_handler.fetch_downloaded_charas()
    html_cards = []

    chara_el = ['<div class="tavernai_chara_card">', None, "</div>"]
    for c in charas:
        image_el = f'<img src="{c.get_image()}">'
        name_el = f"<p>{c.get_name()}</p>"

        element = chara_el.copy()
        element[1] = image_el + name_el

        html_cards.append(["".join(element), c.get_name()])

    return html_cards


def compile_html_online_chara_cards(charas):
    html_cards = []

    chara_el = ['<div class="tavernai_chara_card">', None, "</div>"]
    for c in charas:
        image_el = f'<img src="{c.img_url()}">'
        name_el = f"<p>{c.name}</p>"

        element = chara_el.copy()
        element[1] = image_el + name_el

        html_cards.append(["".join(element), json.dumps(c.to_dict())])

    return html_cards
