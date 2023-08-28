import json
import requests
import shutil
import urllib.parse
from glob import glob
from pathlib import Path
from random import randint
from PIL import Image, ExifTags
from typing import Callable


API_URL = "https://tavernai.net"
CATEGORIES = f"{API_URL}/api/categories"
CHARACTERS = f"{API_URL}/api/characters"
USERS = f"{API_URL}/api/users"
RECENT_CHARAS = f"{CHARACTERS}/board"


class TavernAICard:
    """
    A character card instance for online fetched character cards.
    """

    def __init__(
        self,
        id: int,
        public_id: str,
        public_id_short: str,
        user_id: int,
        user_name: str,
        user_name_view: str,
        name: str,
        short_description: str,
        create_date: str,
        status: int,
        nsfw: bool,
    ):
        self._id: int = id
        self._public_id: str = public_id
        self._public_id_short: str = public_id_short
        self._user_id: int = user_id
        self._user_name: str = user_name
        self._user_name_view: str = user_name_view
        self._name: str = name
        self._short_description: str = short_description
        self._create_date: str = create_date
        self._status: int = status
        self._nsfw: bool = nsfw

    @property
    def id(self):
        """
        The card's ID.
        """
        return self._id

    @property
    def public_id(self):
        """
        The public card's ID.
        """
        return self._public_id

    @property
    def public_id_short(self):
        """
        The first few characters of the card's public ID.
        """
        return self._public_id_short

    @property
    def user_id(self):
        """
        ID of the author's username.
        """
        return self._user_id

    @property
    def user_name(self):
        """
        Author's username.
        """
        return self._user_name

    @property
    def user_name_view(self):
        """
        Author's username for displaying purposes.
        """
        return self._user_name_view

    @property
    def name(self):
        """
        Character name.
        """
        return self._name

    @property
    def short_description(self):
        """
        Character short description.
        """
        return self._short_description

    @property
    def create_date(self):
        """
        Creation date of the card.
        """
        return self._create_date

    @property
    def status(self):
        """
        Card's status. Not really used.
        """
        return self._status

    @property
    def nsfw(self):
        """
        If the card is SFW or not. Commonly mis-used by the community.
        """
        return self._nsfw

    @property
    def img_url(self):
        """
        The URL relevant the character's image/portrait.
        """
        return f"{API_URL}/{self.user_name}/{self.public_id_short}.webp"

    @staticmethod
    def from_dict(entry: dict):
        """
        Creates a `TavernAICard` card from a `dict`.
        """

        return TavernAICard(
            entry.get("id"),
            entry.get("public_id"),
            entry.get("public_id_short"),
            entry.get("user_id"),
            entry.get("user_name"),
            entry.get("user_name_view"),
            entry.get("name"),
            entry.get("short_description"),
            entry.get("create_date"),
            entry.get("status"),
            entry.get("nsfw") == 1,
        )

    def to_dict(self):
        """
        Convert all card information to a `dict`.
        """

        return {
            "id": self.id,
            "public_id": self.public_id,
            "public_id_short": self.public_id_short,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_name_view": self.user_name_view,
            "name": self.name,
            "short_description": self.short_description,
            "create_date": self.create_date,
            "status": self.status,
            "nsfw": 1 if self.nsfw else 0,
        }


class TavernAICategory:
    def __init__(self, id: int, name: str, name_view: str, count: int):
        self._id = id
        self._name = name
        self._name_view = name_view
        self._count = count

    @property
    def id(self):
        """
        Category's ID.
        """
        return self._id

    @property
    def name(self):
        """
        Category name.
        """
        return self._name

    @property
    def name_view(self):
        """
        Category name for displaying purposes.
        """
        return self._name_view

    @property
    def count(self):
        """
        Amount of characters this category has been linked to.
        """
        return self._count

    @staticmethod
    def from_dict(entry: dict):
        """
        Creates a `TavernAICategory` category from a `dict`.
        """

        return TavernAICategory(
            entry.get("id"),
            entry.get("name"),
            entry.get("name_view"),
            entry.get("count"),
        )

    def to_dict(self) -> dict:
        """
        Convert all category information to a `dict`.
        """

        return {
            "id": self._id,
            "name": self._name,
            "name_view": self._name_view,
            "count": self._count,
        }

    def category_url(self, nsfw=True):
        return f"{CATEGORIES}/{self._name}/characters?nsfw={'on' if nsfw else 'off'}"


class TavernAIService:
    """
    Service regarding all available functions related to the TavernAI API.
    """

    @staticmethod
    def fetch_recent_cards(amount=30, nsfw=True):
        """
        Requests the most recent cards.

        Default:
        - amount = 30
        - nsfw = `True`
        """

        params = TavernAIService.__encode_params(nsfw=nsfw)
        response = requests.get(
            f"{CATEGORIES}/{TavernAIService.__category(recent=True)}{params}"
        ).json()

        return TavernAIService.__parseAmount(amount=amount, decoded=response)

    @staticmethod
    def fetch_random_cards(amount=30, nsfw=True):
        """
        Requests random cards.

        Default:
        - amount = 30
        - nsfw = `True`
        """

        params = TavernAIService.__encode_params(nsfw=nsfw)
        response = requests.get(
            f"{CATEGORIES}/{TavernAIService.__category(random=True)}{params}"
        ).json()

        return TavernAIService.__parseAmount(amount=amount, decoded=response)

    @staticmethod
    def fetch_category_cards(category: str | None = None, amount=30, nsfw=True, page=1):
        """
        Requests cards from a designated category.

        Default:
        - category = None (will throw error)
        - amount = 30
        - nsfw = `True`
        - page = 1
        """

        params = TavernAIService.__encode_params(nsfw=nsfw, page=page)
        response = requests.get(
            f"{CATEGORIES}/{TavernAIService.__category(category=category)}{params}"
        ).json()

        return TavernAIService.__parseAmount(amount=amount, decoded=response)

    @staticmethod
    def fetch_catergories():
        """
        Requests all available categories
        """

        response = requests.get(CATEGORIES).json()
        categories = [TavernAICategory.from_dict(entry) for entry in response]
        return sorted(categories, key=lambda cat: cat.name)

    @staticmethod
    def fetch_category(name: str):
        """
        Requests a category.
        """

        params = TavernAIService.__encode_params(q=name)
        response = requests.get(CHARACTERS + params).json().get("categories")
        fetched_categories = [TavernAICategory.from_dict(c) for c in response]

        # sourcery skip: use-next
        for cat in fetched_categories:
            if name == cat.name:
                return cat

        return None

    @staticmethod
    def fetch_query(query: str, nsfw=True):
        """
        Requests a search query.

        Default:
        - nsfw = `True`
        """

        params = TavernAIService.__encode_params(nsfw=nsfw, q=query)
        response = requests.get(CHARACTERS + params).json().get("characters")

        return TavernAIService.__parseAmount(response, -1)

    @staticmethod
    def fetch_random_categories(amount=5):
        """
        Requests random categories.

        Default:
        - amount = 5
        """

        response = TavernAIService.fetch_catergories()

        categories: list[TavernAICategory] = []
        counter = 0

        while counter < amount:
            index = randint(1, len(response)) - 1
            if response[index].count > 4:
                categories.append(response[index])
                counter += 1

        return categories

    @staticmethod
    def download_card(card: TavernAICard):
        """
        Downloads a card from the API to the disk.
        """

        image = requests.get(card.img_url)
        image_path = Path("characters").joinpath(f"{card.name}.webp")
        data_path = Path("characters").joinpath(f"{card.name}.json")

        with image_path.open("wb") as f:
            f.write(image.content)

        with data_path.open("w") as data_file:
            exif = TavernAIService.__disect_exif(card)

            exif["short_description"] = exif.pop("personality", "")
            exif["char_name"] = exif.pop("name")
            exif["char_persona"] = exif.pop("description")
            exif["world_scenario"] = exif.pop("scenario")
            exif["char_greeting"] = exif.pop("first_mes")
            exif["example_dialogue"] = exif.pop("mes_example")

            data_file.write(json.dumps(exif))

        # convert to PNG for chat profile display (ooga booga doesn't accept .webp's as profile images)
        Image.open(image_path).convert("RGBA").save(
            Path("characters").joinpath(f"{card.name}.png"),
        )
        # delete original .webp (although it contains the original EXIF data) to not clutter the character folder
        image_path.unlink()

    @staticmethod
    def __disect_exif(card: TavernAICard) -> dict:
        img = Image.open(Path("characters").joinpath(f"{card.name}.webp"))

        exif = {
            ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS
        }

        img_bytes: bytes = exif.get("UserComment")
        hex_bytes = list(map(lambda x: hex(int(x))[2:], img_bytes[8:].split(b",")))

        chara_data = bytearray.fromhex(" ".join(hex_bytes).upper()).decode("utf-8")
        return json.loads(chara_data)

    @staticmethod
    def __category(recent=False, random=False, category: str | None = None):
        if recent or random:
            return f"${'recent' if recent else 'random'}/characters"

        if category is None:
            raise ValueError("Category cannot be None")

        return f"{TavernAIService.__url_encode(category)}/characters"

    @staticmethod
    def __parseAmount(decoded, amount):
        if amount == -1:
            return [TavernAICard.from_dict(entry) for entry in decoded]

        cards: list[TavernAICard] = []
        count = 0

        for entry in decoded:
            if count >= amount:
                break

            cards.append(TavernAICard.from_dict(entry))
            count += 1

        return cards

    @staticmethod
    def __url_encode(s: str):
        return urllib.parse.quote(s, safe="")

    @staticmethod
    def __encode_params(**kwargs):
        if "nsfw" in kwargs:
            kwargs["nsfw"] = "on" if kwargs.get("nsfw") else "off"

        return f"?{urllib.parse.urlencode(kwargs, quote_via=urllib.parse.quote)}"


class TavernAICardPreview(TavernAICard):
    """
    A card instance made specifically for previews.
    """

    def __init__(
        self,
        public_id: str,
        public_id_short: str,
        user_name: str,
        user_name_view: str,
        name: str,
        description: str,
        short_description: str,
        create_date: str,
        nsfw: bool,
        world_scenario: str,
        greeting: str,
        example_dialogue: str,
    ):
        super().__init__(
            -1,
            public_id,
            public_id_short,
            -1,
            user_name,
            user_name_view,
            name,
            short_description,
            create_date,
            -1,
            nsfw,
        )
        self._description = description
        self._world_scenario = world_scenario
        self._greeting = greeting
        self._example_dialogue = example_dialogue

    @property
    def description(self):
        """
        Character's behaviour description.
        """
        return self._description

    @property
    def world_scenario(self):
        """
        Character's scenario.
        """
        return self._world_scenario

    @property
    def greeting(self):
        """
        Character's greeting.
        """
        return self._greeting

    @property
    def example_dialogue(self):
        """
        Character's example dialogue.
        """
        return self._example_dialogue

    def to_dict(self):
        d = super().to_dict()
        d["description"] = self._description
        d["world_scenario"] = self._world_scenario
        d["greeting"] = self._greeting
        d["example_dialogue"] = self._example_dialogue

        return d

    @staticmethod
    def from_dict(entry: dict):
        """
        Creates a `TavernAICardPreview` card from a `dict`.
        """

        return TavernAICardPreview(
            entry.get("public_id"),
            entry.get("public_id_short"),
            entry.get("user_name"),
            entry.get("user_name_view"),
            entry.get("char_name"),
            entry.get("char_persona"),
            entry.get("short_description"),
            entry.get("create_date_online"),
            entry.get("nsfw"),
            entry.get("world_scenario"),
            entry.get("char_greeting"),
            entry.get("example_dialogue"),
        )


class TavernAIPreviewService:
    temp_path = Path("extensions/webui_tavernai_charas/temp")
    """
    Path used to download and examine cards that are not yet to be downloaded.
    """

    def __temp_exists_check(func: Callable):
        def wrapper(*args, **kwargs):
            if not TavernAIPreviewService.temp_path.exists():
                TavernAIPreviewService.temp_path.mkdir()

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    @__temp_exists_check
    def clear_temp():
        all_caches = glob(
            str(TavernAIPreviewService.temp_path.joinpath("*").absolute())
        )
        for c in all_caches:
            shutil.rmtree(c)

    @staticmethod
    @__temp_exists_check
    def preview_from_img_url(img_url: str):
        parsed = urllib.parse.urlparse(img_url)
        user, short_id = parsed.path.split("/")[1:]
        short_id = short_id.split(".webp")[0]

        response = requests.get(img_url).content

        return TavernAIPreviewService.__create_temp_entry(user, short_id, response)

    @staticmethod
    @__temp_exists_check
    def save_temp_card(card: TavernAICard):
        entry_folder = TavernAIPreviewService.temp_path.joinpath(
            f"{card.user_name}_{card.public_id_short}"
        )

        image_path = entry_folder.joinpath(f"{card.public_id_short}.webp")
        data_path = entry_folder.joinpath(f"{card.name}.json")

        # convert to PNG for chat profile display (ooga booga doesn't accept .webp's as profile images)
        Image.open(image_path).convert("RGBA").save(
            Path("characters").joinpath(f"{card.name}.png"),
        )
        image_path.unlink()

        shutil.move(
            str(data_path.absolute()),
            str(Path(f"characters/{card.name}.json").absolute()),
        )

        entry_folder.rmdir()

    @staticmethod
    def __create_temp_entry(username: str, short_id: str, image: bytes):
        entry_folder = TavernAIPreviewService.temp_path.joinpath(
            f"{username}_{short_id}"
        )

        if not entry_folder.exists():
            entry_folder.mkdir()

        temp_image_path = entry_folder.joinpath(f"{short_id}.webp")
        with open(temp_image_path, "wb") as webp_file:
            webp_file.write(image)

        temp_info = TavernAIPreviewService.__format_exif(temp_image_path)
        temp_info_path = entry_folder.joinpath(f"{temp_info['char_name']}.json")
        with open(temp_info_path, "w") as data_file:
            data_file.write(json.dumps(temp_info))

        return TavernAICardPreview.from_dict(temp_info)

    @staticmethod
    def __format_exif(temp_image_path: Path):
        temp_info = TavernAIPreviewService.__disect_exif(temp_image_path)
        temp_info["short_description"] = temp_info.pop(
            "short_description"
        ) or temp_info.pop("personality")
        temp_info["char_name"] = temp_info.pop("name")
        temp_info["char_persona"] = temp_info.pop("description")
        temp_info["world_scenario"] = temp_info.pop("scenario")
        temp_info["char_greeting"] = temp_info.pop("first_mes")
        temp_info["example_dialogue"] = temp_info.pop("mes_example")

        return temp_info

    @staticmethod
    def __disect_exif(path: Path) -> dict:
        img = Image.open(path)

        exif = {
            ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS
        }

        img_bytes: bytes = exif.get("UserComment")
        hex_bytes = list(map(lambda x: hex(int(x))[2:], img_bytes[8:].split(b",")))

        chara_data = bytearray.fromhex(" ".join(hex_bytes).upper()).decode("utf-8")
        return json.loads(chara_data)


class PreviewCardTracker:
    def __init__(self):
        self.__card: TavernAICardPreview = None

    def set_card(self, c: TavernAICardPreview):
        self.__card = c

    def get_card(self) -> TavernAICardPreview | None:
        return self.__card

    def reset(self):
        self.__card = None


class DownloadCardTracker:
    def __init__(self):
        self.__card: TavernAICard = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DownloadCardTracker, cls).__new__(cls)

        return cls.instance

    def set_card(self, c: TavernAICard):
        self.__card = c

    def get_card(self) -> TavernAICard | None:
        return self.__card

    def reset(self):
        self.__card = None
