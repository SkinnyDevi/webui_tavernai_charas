__version__ = "1.2.4"
"""
This extension's version.
"""


import json
from pathlib import Path


class ConfigHandler:
    """
    Config class for any configurations needed for the extension.
    """

    path = Path("extensions/webui_tavernai_charas/config/chara_config.json")
    __instance = None

    def __local_version_fixer(self, json_data: dict):
        """
        Check and updates the local version in the config file.
        """

        local_version: str | None = json_data.get("version")

        if local_version is None:
            return __version__

        if __version__ == local_version:
            return __version__

        with open(ConfigHandler.path, "w", encoding="utf-8") as f:
            json_data["version"] = __version__
            f.write(json.dumps(json_data))

        return __version__

    def __init__(self, json_data: dict):
        self._allow_nsfw: bool = json_data.get("allow_nsfw")
        self._version = self.__local_version_fixer(json_data)

    @staticmethod
    def setup():
        """
        Returns a Singleton instance of this extension's config.
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

    @property
    def version(self):
        """
        The extension's version.
        """
        return self._version

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

        return {"allow_nsfw": self._allow_nsfw, "version": self._version}
