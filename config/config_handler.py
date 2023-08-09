from pathlib import Path

import json


class ConfigHandler:
    path = Path("extensions/webui_tavernai_charas/config/chara_config.json")

    def __init__(self, json_data: dict):
        self._allow_nsfw: bool = json_data.get("allow_nsfw")

    @staticmethod
    def setup():
        if ConfigHandler.path.exists():
            with open(ConfigHandler.path, "r", encoding="utf-8") as f:
                return ConfigHandler(json.load(f))

        new_config = ConfigHandler({"allow_nsfw": True})
        new_config.save()

        return new_config

    @property
    def allow_nsfw(self):
        return self._allow_nsfw

    def set_allow_nsfw(self, allow: bool):
        self._allow_nsfw = allow
        self.save()

    def save(self):
        with open(ConfigHandler.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_dict()))

    def to_dict(self):
        return {"allow_nsfw": self._allow_nsfw}
