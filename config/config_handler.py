from pathlib import Path

import json


class ConfigHandler:
    path = Path("extensions/webui_tavernai_charas/config/chara_config.json")

    def __init__(self, json_data):
        self.__allow_nsfw = json_data.get("allow_nsfw")

    @staticmethod
    def setup():
        if ConfigHandler.path.exists():
            with open(ConfigHandler.path, "r", encoding="utf-8") as f:
                return ConfigHandler(json.load(f))

        new_config = ConfigHandler({"allow_nsfw": True})
        new_config.save()

        return new_config

    def get_allow_nsfw(self):
        return self.__allow_nsfw

    def set_allow_nsfw(self, allow: bool):
        self.__allow_nsfw = allow
        self.save()

    def save(self):
        with open(ConfigHandler.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_dict()))

    def to_dict(self):
        return {"allow_nsfw": self.__allow_nsfw}


class DeleteCardTracker:
    def __init__(self):
        self.__card_index = None

    def set_index(self, i: int):
        self.__card_index = i

    def get_index(self) -> int:
        return self.__card_index

    def reset(self):
        self.__card_index = None
