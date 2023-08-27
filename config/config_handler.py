from pathlib import Path

import json


class ConfigHandler:
    """
    Config class for any configurations needed for the extension.
    """

    path = Path("extensions/webui_tavernai_charas/config/chara_config.json")
    __instance = None

    def __init__(self, json_data: dict):
        self._allow_nsfw: bool = json_data.get("allow_nsfw")

    @staticmethod
    def setup():
        """
        Returna a Singleton instance of this extension's config.
        """

        return ConfigHandler.__instance or ConfigHandler.__setup()

    @staticmethod
    def __setup():
        if ConfigHandler.path.exists():
            with open(ConfigHandler.path, "r", encoding="utf-8") as f:
                return ConfigHandler(json.load(f))

        new_config = ConfigHandler({"allow_nsfw": True})
        new_config.save()

        return new_config

    @property
    def allow_nsfw(self):
        """
        Allow NSFW.
        """
        return self._allow_nsfw

    def set_allow_nsfw(self, allow: bool):
        """
        Change `allow_nsfw`'s value in config.
        """

        self._allow_nsfw = allow
        self.save()

    def save(self):
        """
        Save the config with the existing values to disk.
        """

        with open(ConfigHandler.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_dict()))

    def to_dict(self):
        """
        Returns all available configs as a `dict`.
        """

        return {"allow_nsfw": self._allow_nsfw}
