from pathlib import Path
from modules.html_generator import get_image_cache


class CharaCard:
    def __init__(self, image: Path, data_file: Path):
        self.__name = data_file.stem
        self.__image_path = image
        self.__image = f"file/{get_image_cache(image)}" if image is not None else None
        self.__data_file = data_file

    def get_name(self):
        return self.__name.replace("_", " ")

    def get_image(self):
        return self.__image

    def get_data(self):
        return self.__data_file

    def to_dict(self):
        return {"name": self.__name, "image": self.__image, "data": self.__data_file}

    def delete(self):
        print("Deleting card: " + self.__name + "...")
        self.__image_path.unlink()
        self.__data_file.unlink()
        print("Deleted.")


def fetch_downloaded_charas():
    charas = []
    characters = Path("characters")
    for file in sorted(characters.glob("*")):
        if file.suffix in [".json", ".yml", ".yaml"]:
            png = characters.joinpath(file.stem + ".png")
            webp = characters.joinpath(file.stem + ".webp")

            charas.append(
                CharaCard(
                    png if png.exists() else webp if webp.exists() else None, file
                )
            )

    return charas
