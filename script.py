from pathlib import Path

import user_data.extensions.webui_tavernai_charas.ui.main as charas_ui
from user_data.extensions.webui_tavernai_charas.config.config_handler import (
    base_ext_path,
)

params = {
    "display_name": "TavernAI Characters",
    "is_tab": True,
}


def load_tavernai_resource(path: str):
    with base_ext_path().joinpath(path).open("r", encoding="utf-8") as f:
        f = f.read()

    return f


def custom_css():
    return load_tavernai_resource("web/tavernai_charas_styles.css")


def custom_js():
    return load_tavernai_resource("web/tavernai_notifications.js")


def ui():
    charas_ui.mount_ui()
