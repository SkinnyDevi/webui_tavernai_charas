import extensions.tavernai_charas.charas_ui as charas_ui

params = {
    "display_name": "TavernAI Characters",
    "is_tab": True,
}


def ui():
    charas_ui.mount_ui()
