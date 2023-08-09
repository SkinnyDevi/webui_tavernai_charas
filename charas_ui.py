import gradio as gr
import json
import re

from modules.shared import gradio
import modules.ui as ui

import extensions.webui_tavernai_charas.services.offline_chara_service as offline_chara_service
from extensions.webui_tavernai_charas.services.tavernai_service import (
    TavernAIService,
    TavernAICard,
)
from extensions.webui_tavernai_charas.config.config_handler import ConfigHandler


CONFIG = ConfigHandler.setup()
DELETE_CARD_INDEX = offline_chara_service.DeleteCardTracker()


def mount_ui():
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
                        f"Category - {cat1.name_view.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat1.name, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat2 = random_categories[1]
                    create_tavernai_chara_display(
                        f"Category - {cat2.name_view.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat2.name, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat3 = random_categories[2]
                    create_tavernai_chara_display(
                        f"Category - {cat3.name_view.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat3.name, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat4 = random_categories[3]
                    create_tavernai_chara_display(
                        f"Category - {cat4.name_view.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat4.name, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    cat5 = random_categories[4]
                    create_tavernai_chara_display(
                        f"Category - {cat5.name_view.capitalize()}",
                        lambda: TavernAIService.fetch_category_cards(
                            category=cat5.name, nsfw=CONFIG.get_allow_nsfw()
                        ),
                    )

                    gr.Markdown(
                        """*Disclaimer*: As TavernAI is a community supported character database, characters may often be mis-categorized,
                            or may be NSFW when they are marked as not being NSFW."""
                    )

                with gr.TabItem("Search"):
                    with gr.Row(elem_id="tavernai_search_bar"):
                        search_bar = gr.Textbox(
                            placeholder="Search (searching omits category filtering)",
                            show_label=False,
                        )
                        search_btn = gr.Button("Search")
                        deselect_category = gr.Button("Clear search filters")

                    gr.Markdown(
                        """**Note**: Searching text and filtering by category is not possible due to the API's limitations.
                        Make sure you clear your search filters before using one or the other for a better experience."""
                    )

                    with gr.Accordion("Category Filters", open=False):
                        allow_cat_nsfw = gr.CheckboxGroup(
                            ["Allow NSFW"],
                            label="Filters",
                            interactive=True,
                        )

                        with gr.Accordion("Categories", open=False):
                            category_choices = gr.Radio(
                                [
                                    cat.name
                                    for cat in TavernAIService.fetch_catergories()
                                ],
                                elem_classes=["tavernai_categories"],
                                label="",
                            )

                    with gr.Row(variant="panel", elem_id="tavernai_result_pages"):
                        section_previous = gr.Button("Previous section")
                        current_section = gr.Label(1, label="Current Section")
                        section_next = gr.Button("Next section")

                    search_results = gr.Dataset(
                        components=[gr.HTML(visible=True)],
                        label="Selected category: $recent",
                        samples=compile_html_online_chara_cards(
                            TavernAIService.fetch_recent_cards(
                                amount=-1,
                                nsfw=True if len(allow_cat_nsfw.value) > 0 else False,
                            )
                        ),
                        elem_classes=[
                            "tavernai_downloaded_container",
                            "tavernai_result_set",
                        ],
                        samples_per_page=10,
                    )

                    gr.Markdown(
                        """*Disclaimer*: As TavernAI is a community supported character database, characters may often be mis-categorized,
                            or may be NSFW when they are marked as not being NSFW."""
                    )

                    allow_cat_nsfw.select(
                        toggle_category_nsfw,
                        [category_choices, current_section, search_bar],
                        search_results,
                    )

                    search_btn.click(
                        apply_input_search,
                        [search_bar, allow_cat_nsfw],
                        [search_results, section_next, section_previous],
                    )

                    section_next.click(
                        next_category_section,
                        [category_choices, allow_cat_nsfw, current_section],
                        [current_section, search_results],
                    )

                    section_previous.click(
                        previous_category_section,
                        [category_choices, allow_cat_nsfw, current_section],
                        [current_section, search_results],
                    )

                    deselect_category.click(
                        reset_category_filter,
                        allow_cat_nsfw,
                        [
                            category_choices,
                            search_results,
                            current_section,
                            search_bar,
                            section_next,
                            section_previous,
                        ],
                    )

                    category_choices.input(
                        filter_by_category,
                        [category_choices, allow_cat_nsfw],
                        [
                            search_results,
                            current_section,
                            section_next,
                            section_previous,
                        ],
                    )

                    search_results.select(download_character, None, None)

        with gr.TabItem("Downloaded"):
            with gr.Column():
                gr.Markdown("# Downloaded Characters")
                refresh = gr.Button(
                    "Refresh", elem_classes="tavernai_refresh_downloaded_charas"
                )
                get_local_cards = offline_chara_service.fetch_downloaded_charas

                with gr.Box(
                    visible=False, elem_classes="file-saver"
                ) as delete_card_box:
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
                        cancel_card_delete = gr.Button(
                            "Cancel", elem_classes="small-button"
                        )

                        confirm_card_delete.click(
                            on_confirm_delete_btn,
                            None,
                            delete_card_box,
                            _js=refresh_downloaded(),
                        )

                        cancel_card_delete.click(
                            on_cancel_delete_btn,
                            None,
                            delete_card_box,
                        )

                with gr.Row(elem_id="tavernai_downloaded_handlers"):
                    with gr.Column():
                        with gr.Row():
                            search_bar = gr.Textbox(
                                placeholder="Search",
                                show_label=False,
                            )
                            search_btn = gr.Button("Search")

                    with gr.Column():
                        with gr.Row():
                            all_cards = gr.Dropdown(
                                choices=[
                                    f"[{i}] {c.get_name()}"
                                    for i, c in enumerate(get_local_cards())
                                ],
                                value=f"[0] {get_local_cards()[0].get_name()}",
                                interactive=True,
                                label="Delete a character",
                                elem_classes=["slim-dropdown"],
                            )
                            all_cards.container = False
                            refresh_delete_cards = ui.create_refresh_button(
                                all_cards,
                                lambda: None,
                                lambda: {
                                    "choices": [
                                        f"[{i}] {c.get_name()}"
                                        for i, c in enumerate(get_local_cards())
                                    ],
                                    "value": f"[0] {get_local_cards()[0].get_name()}",
                                },
                                [
                                    "refresh-button",
                                    "tavernai_refresh_downloaded_charas",
                                ],
                            )
                            delete_card_btn = ui.create_delete_button(
                                elem_classes=["refresh-button"]
                            )

                            delete_card_btn.click(
                                on_delete_btn,
                                all_cards,
                                [
                                    delete_card_textbox,
                                    delete_card_box,
                                ],
                            )

                downloaded = gr.Dataset(
                    components=[gr.HTML(visible=False)],
                    label="",
                    samples=compile_html_downloaded_chara_cards(),
                    samples_per_page=15,
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


def download_character(evt: gr.SelectData):
    card = TavernAICard.from_dict(json.loads(evt.value[1]))
    TavernAICard.download_card(card)


def on_delete_btn(
    card_dropdown: gr.Dropdown,
):
    match = re.search(r"\[(\d+)\]", card_dropdown)
    DELETE_CARD_INDEX.set_index(int(match.group(1)))

    return card_dropdown, gr.update(visible=True)


def on_confirm_delete_btn():
    offline_chara_service.fetch_downloaded_charas()[
        DELETE_CARD_INDEX.get_index()
    ].delete()

    return gr.update(visible=False)


def on_cancel_delete_btn():
    DELETE_CARD_INDEX.reset()
    return gr.update(visible=False)


def filter_by_category(selected: gr.Radio, allow_nsfw: gr.CheckboxGroup):
    cards = TavernAIService.fetch_category_cards(
        category=selected, amount=-1, nsfw=len(allow_nsfw) > 0
    )

    title = f"Selected category: {selected}"

    return (
        gr.update(samples=compile_html_online_chara_cards(cards), label=title),
        gr.update(value=1),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


def reset_category_filter(allow_nsfw: gr.CheckboxGroup):
    cards = TavernAIService.fetch_recent_cards(-1, len(allow_nsfw) > 0)

    title = f"Selected category: $recent"

    return (
        gr.update(value=None),
        gr.update(samples=compile_html_online_chara_cards(cards), label=title),
        gr.update(value=1),
        gr.update(value=""),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


def next_category_section(
    selected: gr.Radio, allow_nsfw: gr.CheckboxGroup, current: gr.Label
):
    current_val = int(current.get("label")) + 1
    selected = "$recent" if selected is None else selected

    cards = TavernAIService.fetch_category_cards(
        category=selected,
        amount=-1,
        nsfw=True if len(allow_nsfw) > 0 else False,
        page=current_val,
    )

    return gr.update(value=current_val), gr.update(
        samples=compile_html_online_chara_cards(cards)
    )


def previous_category_section(
    selected: gr.Radio, allow_nsfw: gr.CheckboxGroup, current: gr.Label
):
    current_val = int(current.get("label"))
    selected = "$recent" if selected is None else selected

    if current_val > 1:
        current_val -= 1

        cards = TavernAIService.fetch_category_cards(
            category=selected,
            amount=-1,
            nsfw=len(allow_nsfw) > 0,
            page=current_val,
        )

        return gr.update(value=current_val), gr.update(
            samples=compile_html_online_chara_cards(cards)
        )

    return gr.update(value=1), lambda: None


def toggle_category_nsfw(
    evt: gr.SelectData,
    selected_cat: gr.Radio,
    current_section: gr.Label,
    search_input: gr.Textbox,
):
    allow = evt.selected
    selected_cat = "$recent" if selected_cat is None else selected_cat

    if search_input is None or search_input == "":
        cards = TavernAIService.fetch_category_cards(
            category=selected_cat,
            amount=-1,
            nsfw=allow,
            page=int(current_section.get("label")),
        )
    else:
        cards = TavernAIService.fetch_query(search_input, allow)

    return gr.update(samples=compile_html_online_chara_cards(cards))


def apply_input_search(search_input: gr.Textbox, allow_nsfw: gr.CheckboxGroup):
    if search_input is None or search_input == "":
        cards = TavernAIService.fetch_recent_cards(-1, len(allow_nsfw) > 0)
    else:
        cards = TavernAIService.fetch_query(search_input, len(allow_nsfw) > 0)

    return (
        gr.update(
            samples=compile_html_online_chara_cards(cards),
            label="Displaying search results",
        ),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )


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
        setTimeout(() => {
            for (let r of refreshes) {
                setTimeout(() => r.click(), 250);
            }
        }, 500)
    }
    """


def refresh_downloaded():
    return """
    () => {
        var refreshes = document.querySelectorAll(".tavernai_refresh_downloaded_charas");
        for (let r of refreshes) {
            setTimeout(() => r.click(), 250);
        }
    }
    """


def create_tavernai_chara_display(title: str, samples):
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

    slider.select(download_character, None, None)

    # copied from ui.create_refresh_button method
    def refresh():
        return gr.update(samples=compile_html_online_chara_cards(samples()))

    refresh_button.click(refresh, [], [slider])

    return slider


def compile_html_downloaded_chara_cards():
    charas = offline_chara_service.fetch_downloaded_charas()
    html_cards = []

    chara_el = ['<div class="tavernai_chara_card">', None, "</div>"]
    for c in charas:
        image_el = f'<img src="{c.get_image()}">'
        name_el = f"<p>{c.get_name()}</p>"

        element = chara_el.copy()
        element[1] = image_el + name_el

        html_cards.append(["".join(element), c.get_name()])

    return html_cards


def compile_html_online_chara_cards(charas: list[TavernAICard]):
    html_cards = []

    chara_el = ['<div class="tavernai_chara_card">', None, "</div>"]
    for c in charas:
        image_el = f'<img src="{c.img_url()}">'
        name_el = f"<p>{c.name}</p>"

        element = chara_el.copy()
        element[1] = image_el + name_el

        html_cards.append(["".join(element), json.dumps(c.to_dict())])

    return html_cards
