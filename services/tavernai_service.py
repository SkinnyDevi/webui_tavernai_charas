from pathlib import Path
from random import randint
import urllib.parse

import json
import requests

from PIL import Image, ExifTags

API_URL = "https://tavernai.net"
CATEGORIES = f"{API_URL}/api/categories"
CHARACTERS = f"{API_URL}/api/characters"
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

        return [TavernAICategory.from_dict(entry) for entry in response]

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
            exif = TavernAIService.__disect_exif(card.name)

            exif["char_name"] = card.name
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
    def __disect_exif(card_name) -> dict:
        img = Image.open(Path("characters").joinpath(f"{card_name}.webp"))

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
