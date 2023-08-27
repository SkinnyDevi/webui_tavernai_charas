from pathlib import Path

import extensions.webui_tavernai_charas.ui.main as charas_ui

params = {
    "display_name": "TavernAI Characters",
    "is_tab": True,
}


def load_tavernai_resource(path: str):
    with Path(f"extensions/webui_tavernai_charas{path}").open(
        "r", encoding="utf-8"
    ) as f:
        f = f.read()

    return f


def custom_css():
    return load_tavernai_resource("/web/tavernai_charas_styles.css")


def custom_js():
    return load_tavernai_resource("/web/tavernai_notifications.js")


def ui():
    charas_ui.mount_ui()
