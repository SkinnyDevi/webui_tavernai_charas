from pathlib import Path

import extensions.webui_tavernai_charas.charas_ui as charas_ui

params = {
    "display_name": "TavernAI Characters",
    "is_tab": True,
}


def custom_css():
    with Path("extensions/webui_tavernai_charas/tavernai_charas_styles.css").open(
        "r", encoding="utf-8"
    ) as css_file:
        css = css_file.read()

    return css


def ui():
    charas_ui.mount_ui()
