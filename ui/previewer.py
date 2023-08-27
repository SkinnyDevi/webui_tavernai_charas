import gradio as gr
from urllib import parse

from extensions.webui_tavernai_charas.services.tavernai_service import (
    TavernAIPreviewService,
    PreviewCardTracker,
)
from extensions.webui_tavernai_charas.ui.shared import components


CURRENT_PREVIEW_TRACKER = PreviewCardTracker()


def get_card_fields():
    name: gr.Textbox = components["preview_card_name"]
    nsfw: gr.Textbox = components["preview_card_is_nsfw"]
    author: gr.Textbox = components["preview_card_author"]
    short_description: gr.Textbox = components["preview_card_short_description"]
    description: gr.Textbox = components["preview_card_description"]
    world_scenario: gr.Textbox = components["preview_card_world_scenario"]
    greeting: gr.Textbox = components["preview_card_greeting"]
    example_dialogue: gr.Textbox = components["preview_card_example_dialogue"]
    short_id: gr.Textbox = components["preview_card_short_id"]
    long_id: gr.Textbox = components["preview_card_long_id"]
    creation_date: gr.Textbox = components["preview_card_creation_date"]
    image_field: gr.Image = components["preview_card_image"]

    return (
        name,
        author,
        nsfw,
        short_description,
        description,
        world_scenario,
        greeting,
        example_dialogue,
        short_id,
        long_id,
        creation_date,
        image_field,
    )


def search_by_url(url: gr.Textbox):
    url: str = url
    preview = TavernAIPreviewService.preview_from_img_url(url)
    CURRENT_PREVIEW_TRACKER.set_card(preview)
    card = CURRENT_PREVIEW_TRACKER.get_card()

    return (
        gr.update(value=card.name),
        gr.update(value=card.user_name_view),
        gr.update(value="Yes" if card.nsfw else "No"),
        gr.update(value=card.short_description),
        gr.update(value=card.description),
        gr.update(value=card.world_scenario),
        gr.update(value=card.greeting),
        gr.update(value=card.example_dialogue),
        gr.update(value=card.public_id_short),
        gr.update(value=card.public_id),
        gr.update(value=card.create_date),
        gr.update(value=card.img_url),
    )


def clear_preview():
    TavernAIPreviewService.clear_temp()
    CURRENT_PREVIEW_TRACKER.reset()

    updates = [gr.update(value=None) for _ in get_card_fields()]
    return tuple(updates)


def download_preview(chara_name: gr.Textbox):
    TavernAIPreviewService.save_temp_card(CURRENT_PREVIEW_TRACKER.get_card())

    return clear_preview()


def define_card_details():
    components["preview_card_name"] = gr.Textbox(
        interactive=False,
        lines=1,
        label="Name",
    )

    components["preview_card_author"] = gr.Textbox(
        interactive=False, lines=1, label="Author"
    )

    components["preview_card_is_nsfw"] = gr.Textbox(
        interactive=False,
        lines=1,
        label="NSFW",
    )

    components["preview_card_short_description"] = gr.Textbox(
        interactive=False,
        lines=3,
        label="Short description",
    )

    components["preview_card_description"] = gr.Textbox(
        interactive=False,
        lines=7,
        label="Description",
    )

    components["preview_card_world_scenario"] = gr.Textbox(
        interactive=False,
        lines=7,
        label="World Scenario",
    )

    components["preview_card_greeting"] = gr.Textbox(
        interactive=False,
        lines=7,
        label="Greeting",
    )

    components["preview_card_example_dialogue"] = gr.Textbox(
        interactive=False,
        lines=7,
        label="Example dialogue",
    )

    components["preview_card_short_id"] = gr.Textbox(
        interactive=False, lines=1, label="Short id"
    )

    components["preview_card_long_id"] = gr.Textbox(
        interactive=False, lines=1, label="Long id"
    )

    components["preview_card_creation_date"] = gr.Textbox(
        interactive=False, lines=1, label="Creation date"
    )


def previewer_ui():
    gr.Markdown("# Card Previwer")

    with gr.Column():
        with gr.Row(elem_id="tavernai_search_bar"):
            components["preview_url_searcher"] = gr.Textbox(
                placeholder="Search by card image URL",
                show_label=False,
                interactive=True,
            )

            components["preview_search_button"] = gr.Button(
                "Search", elem_id="tavernai_preview_search_button"
            )
            components["preview_download_button"] = gr.Button("Download")
            components["preview_clear_button"] = gr.Button("Clear stored previews")

        with gr.Row():
            with gr.Column(scale=5):
                define_card_details()

            with gr.Column():
                components["preview_card_image"] = gr.Image(
                    label="Card Image", interactive=False
                )

        components["preview_search_button"].click(
            search_by_url, components["preview_url_searcher"], list(get_card_fields())
        )

        components["preview_download_button"].click(
            download_preview,
            components["preview_card_name"],
            list(get_card_fields()),
            _js="(name) => notifyCharaDownload(name)",
        )

        components["preview_clear_button"].click(
            clear_preview, None, list(get_card_fields())
        )
