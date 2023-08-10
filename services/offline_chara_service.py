from pathlib import Path
from modules.html_generator import get_image_cache


class OfflineCharaCard:
    def __init__(self, image: Path, data_file: Path):
        self._name = data_file.stem
        self._image_path = image
        self._image = f"file/{get_image_cache(image)}" if image is not None else None
        self._data_file = data_file

    @property
    def name(self):
        return self._name.replace("_", " ")

    @property
    def image(self):
        return self._image

    @property
    def data(self):
        return self._data_file

    @property
    def image_path(self):
        return self._image_path

    def to_dict(self):
        return {
            "name": self._name,
            "image": self._image,
            "data": self._data_file,
            "image_path": self._image_path,
        }

    def delete(self):
        print(f"Deleting card: {self._name}...")
        if self._image_path:
            self._image_path.unlink()
        if self._data_file:
            self._data_file.unlink()
        print("Deleted.")


def fetch_downloaded_charas():
    charas: list[OfflineCharaCard] = []
    characters = Path("characters")
    for file in sorted(characters.glob("*")):
        if file.suffix in [".json", ".yml", ".yaml"]:
            png = characters.joinpath(file.stem + ".png")
            webp = characters.joinpath(file.stem + ".webp")

            charas.append(
                OfflineCharaCard(
                    png if png.exists() else webp if webp.exists() else None, file
                )
            )

    return charas


class DeleteCardTracker:
    def __init__(self):
        self.__card_index = None

    def set_index(self, i: int):
        self.__card_index = i

    def get_index(self) -> int | None:
        return self.__card_index

    def reset(self):
        self.__card_index = None
