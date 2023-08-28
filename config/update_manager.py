import requests

from extensions.webui_tavernai_charas.config.config_handler import ConfigHandler


class ExtUpdateManager:
    __JSON_CHECKER_URL = "https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/config/chara_config.json"

    @staticmethod
    def check_for_updates(config: ConfigHandler):
        online_config: dict = requests.get(ExtUpdateManager.__JSON_CHECKER_URL).json()

        online_version = online_config.get("version")
        local_version = config.version

        return True if online_version is None else local_version != online_version
