from pathlib import Path
from random import randint
import urllib.parse

import json
import requests

from PIL import Image
from PIL.ExifTags import TAGS

API_URL = "https://tavernai.net"
CATEGORIES = API_URL + "/api/categories"
CHARACTERS = API_URL + "/api/characters"
RECENT_CHARAS = CHARACTERS + "/board"


class TavernAIService:
    @staticmethod
    def fetch_recent_cards(amount=30, nsfw=True):
        params = TavernAIService.__encode_params(nsfw=nsfw)
        response = requests.get(
            CATEGORIES + f"/{TavernAIService.__category(recent=True)}{params}"
        )
        decoded = response.json()

        return TavernAIService.__parseAmount(amount=amount, decoded=decoded)

    @staticmethod
    def fetch_random_cards(amount=30, nsfw=True):
        params = TavernAIService.__encode_params(nsfw=nsfw)
        response = requests.get(
            CATEGORIES + f"/{TavernAIService.__category(random=True)}{params}"
        )
        decoded = response.json()

        return TavernAIService.__parseAmount(amount=amount, decoded=decoded)

    @staticmethod
    def fetch_category_cards(category=None, amount=30, nsfw=True, page=1):
        params = TavernAIService.__encode_params(nsfw=nsfw, page=page)
        response = requests.get(
            CATEGORIES + f"/{TavernAIService.__category(category=category)}{params}"
        )
        decoded = response.json()

        return TavernAIService.__parseAmount(amount=amount, decoded=decoded)

    @staticmethod
    def fetch_catergories():
        response = requests.get(CATEGORIES).json()

        return [TavernAICategory.from_dict(entry) for entry in response]

    @staticmethod
    def fetch_category(name: str):
        response = TavernAIService.fetch_catergories()

        for cat in response:
            if name == cat.name:
                return cat

        return None

    @staticmethod
    def fetch_query(query: str, nsfw=True):
        params = TavernAIService.__encode_params(nsfw=nsfw, q=query)
        response = requests.get(CHARACTERS + params).json()
        print("Fetching query:" + query)
        print("Result:", response)

    @staticmethod
    def fetch_random_categories(amount=5):
        response = requests.get(CATEGORIES).json()

        categories = []
        counter = 0

        while counter < amount:
            index = randint(1, len(response)) - 1
            if response[index].get("count") > 4:
                categories.append(response[index].get("name"))
                counter += 1

        return categories

    @staticmethod
    def __category(recent=False, random=False, category=None):
        if recent or random:
            return f"${'recent' if recent else 'random'}/characters"

        if category is None:
            raise Exception("Category cannot be None")

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


class TavernAICard:
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
        self.id: int = id
        self.public_id: str = public_id
        self.public_id_short: str = public_id_short
        self.user_id: int = user_id
        self.user_name: str = user_name
        self.user_name_view: str = user_name_view
        self.name: str = name
        self.short_description: str = short_description
        self.create_date: str = create_date
        self.status: int = status
        self.nsfw: bool = nsfw

    @staticmethod
    def from_dict(entry: dict):
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
            True if entry.get("nsfw") == 1 else False,
        )

    def to_dict(self):
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

    def img_url(self):
        return API_URL + f"/{self.user_name}/{self.public_id_short}.webp"

    @staticmethod
    def download_card(card):
        image = requests.get(card.img_url())
        image_path = Path("characters").joinpath(card.name + ".webp")
        data_path = Path("characters").joinpath(card.name + ".json")

        with image_path.open("wb") as f:
            f.write(image.content)

        with data_path.open("w") as data_file:
            exif = TavernAICard.__disect_exif(card.name)

            exif["char_name"] = card.name
            exif["char_persona"] = exif.get("description")
            exif["world_scenario"] = exif.get("scenario")
            exif["char_greeting"] = exif.get("first_mes")
            exif["example_dialogue"] = exif.get("mes_example")

            data_file.write(json.dumps(exif))

        # convert to PNG for chat profile display (ooga booga doesn't accept .webp's as profile images)
        Image.open(image_path).convert("RGBA").save(
            Path("characters").joinpath(card.name + ".png"),
        )
        # delete original .webp (although it contains the original EXIF data) to not clutter the character folder
        image_path.unlink()

    @staticmethod
    def __disect_exif(card_name, get_bytes=False) -> dict:
        ret = {}
        i = Image.open(Path("characters").joinpath(card_name + ".webp"))
        info = i.getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        if get_bytes:
            return ret

        usercomment = ret.get("UserComment")
        stringbytes = ""
        for val in usercomment:
            stringbytes = stringbytes + chr(val)

        stringbytes = stringbytes.split(",")
        stringbytes[0] = "123"
        stringbytes = [int(b) for b in stringbytes]

        chara_data = ""
        for val in stringbytes:
            chara_data = chara_data + chr(val)

        return json.loads(chara_data)


class TavernAICategory:
    def __init__(self, id: int, name: str, name_view: str, count: int):
        self.id = id
        self.name = name
        self.name_view = name_view
        self.count = count

    @staticmethod
    def from_dict(entry: dict):
        return TavernAICategory(
            entry.get("id"),
            entry.get("name"),
            entry.get("name_view"),
            entry.get("count"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_view": self.name_view,
            "count": self.count,
        }

    def category_url(self, nsfw=True):
        return CATEGORIES + f"/{self.name}/characters?nsfw={'on' if nsfw else'off'}"
