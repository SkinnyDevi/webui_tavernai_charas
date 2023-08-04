from pathlib import Path

import json


class ConfigHandler:
    path = Path("extensions/tavernai_charas/chara_config.json")

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
