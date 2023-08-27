import json
import gradio as gr

import modules.ui as ui

from extensions.webui_tavernai_charas.services.tavernai_service import (
    TavernAIService,
    TavernAICard,
)
from extensions.webui_tavernai_charas.config.config_handler import ConfigHandler
import extensions.webui_tavernai_charas.ui.native_fn as nfn

CONFIG = ConfigHandler.setup()


def download_character(evt: gr.SelectData):
    """
    Downloads a selected character to disk.
    """

    card = TavernAICard.from_dict(json.loads(evt.value[1]))
    TavernAIService.download_card(card)


def create_tavernai_chara_display(title: str, samples):
    """
    Creates a custom carousel for displaying fetched cards.
    """

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


def apply_checkbox(evt: gr.SelectData):
    key = str(evt.value).lower().replace(" ", "_")

    match key:
        case "allow_nsfw":
            CONFIG.set_allow_nsfw(evt.selected)

    return evt.value


def compile_html_online_chara_cards(charas: list[TavernAICard]):
    """
    Gets a list of online cards and returns a list of their respective HTML format.
    """

    html_cards: list[list] = []

    for c in charas:
        image_el = f'<img src="{c.img_url}">'
        name_el = f"<p>{c.name}</p>"

        element = f"""<div class="tavernai_chara_card" onclick="notifyCharaDownload('{c.name}')">{image_el + name_el}</div>"""

        html_cards.append(["".join(element), json.dumps(c.to_dict())])

    return html_cards


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


def next_category_section(
    selected: gr.Radio, allow_nsfw: gr.CheckboxGroup, current: gr.Label
):
    current_val = int(current.get("label")) + 1
    selected = "$recent" if selected is None else selected

    cards = TavernAIService.fetch_category_cards(
        category=selected,
        amount=-1,
        nsfw=len(allow_nsfw) > 0,
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


def reset_category_filter(allow_nsfw: gr.CheckboxGroup):
    cards = TavernAIService.fetch_recent_cards(-1, len(allow_nsfw) > 0)

    title = "Selected category: $recent"

    return (
        gr.update(value=None),
        gr.update(samples=compile_html_online_chara_cards(cards), label=title),
        gr.update(value=1),
        gr.update(value=""),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


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


def mount_fixed_categories():
    create_tavernai_chara_display(
        "Recent Charas",
        lambda: TavernAIService.fetch_recent_cards(nsfw=CONFIG.allow_nsfw),
    )

    create_tavernai_chara_display(
        "Random Characters",
        lambda: TavernAIService.fetch_random_cards(nsfw=CONFIG.allow_nsfw),
    )


def mount_random_categories():
    random_categories = TavernAIService.fetch_random_categories(5)

    cat1 = random_categories[0]
    create_tavernai_chara_display(
        f"Category - {cat1.name_view.capitalize()}",
        lambda: TavernAIService.fetch_category_cards(
            category=cat1.name, nsfw=CONFIG.allow_nsfw
        ),
    )

    cat2 = random_categories[1]
    create_tavernai_chara_display(
        f"Category - {cat2.name_view.capitalize()}",
        lambda: TavernAIService.fetch_category_cards(
            category=cat2.name, nsfw=CONFIG.allow_nsfw
        ),
    )

    cat3 = random_categories[2]
    create_tavernai_chara_display(
        f"Category - {cat3.name_view.capitalize()}",
        lambda: TavernAIService.fetch_category_cards(
            category=cat3.name, nsfw=CONFIG.allow_nsfw
        ),
    )

    cat4 = random_categories[3]
    create_tavernai_chara_display(
        f"Category - {cat4.name_view.capitalize()}",
        lambda: TavernAIService.fetch_category_cards(
            category=cat4.name, nsfw=CONFIG.allow_nsfw
        ),
    )

    cat5 = random_categories[4]
    create_tavernai_chara_display(
        f"Category - {cat5.name_view.capitalize()}",
        lambda: TavernAIService.fetch_category_cards(
            category=cat5.name, nsfw=CONFIG.allow_nsfw
        ),
    )


def define_search_events(
    allow_cat_nsfw: gr.CheckboxGroup,
    search_btn: gr.Button,
    section_next: gr.Button,
    section_previous: gr.Button,
    deselect_category: gr.Button,
    category_choices: gr.Radio,
    search_results: gr.Dataset,
    current_section: gr.Label,
    search_bar: gr.Textbox,
):
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


def featured_ui():  # sourcery skip: extract-method
    gr.Markdown("# Online Characters")

    with gr.Tabs():
        with gr.TabItem("Featured"):
            with gr.Row():
                nsfw_check = gr.CheckboxGroup(
                    ["Allow NSFW"],
                    label="Filters",
                    value=[
                        "Allow NSFW" if CONFIG.allow_nsfw else "",
                    ],
                    interactive=True,
                )
                nsfw_check.select(apply_checkbox, [], None, _js=nfn.hit_all_refreshes())

            mount_fixed_categories()
            mount_random_categories()

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
                        [cat.name for cat in TavernAIService.fetch_catergories()],
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
                        nsfw=len(allow_cat_nsfw.value) > 0,
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

            define_search_events(
                allow_cat_nsfw,
                search_btn,
                section_next,
                section_previous,
                deselect_category,
                category_choices,
                search_results,
                current_section,
                search_bar,
            )
