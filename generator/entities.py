import json
import re
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class WordWithContext:
    word: str
    context: str

    def __post_init__(self):
        if self.word is None or self.context is None:
            raise ValueError("Attributes cannot be None")
        if self.word == "":
            raise ValueError("Word cannot be empty")


@dataclass(frozen=True)
class CardRawData:
    word: str
    card_text: str
    image_prompt: str
    image_url: str
    image_path: str
    audio_path: str
    dictionary_url: str = None
    version: int = 1

    def __post_init__(self):
        not_nullable = [self.word, self.card_text, self.image_url, self.image_path]
        if None in not_nullable:
            raise ValueError(f"Attributes cannot be None: {serialize_to_json(self)}")
        if self.word == "":
            raise ValueError("Word cannot be empty")
        if self.card_text == "":
            raise ValueError("Card text cannot be empty")
        if self.image_url == "":
            raise ValueError("Image URL cannot be empty")
        if self.audio_path == "" or self.image_path == "":
            raise ValueError("Paths cannot be empty")


def serialize_to_json(data):
    # Convert dataclass to dictionary
    data_dict = asdict(data)
    # Serialize dictionary to JSON
    return json.dumps(data_dict, indent=4)


def word_to_filename(word: WordWithContext) -> str:
    # convert to lower case
    word_cleaned = str.lower(word.word)
    # Replace all spaces with underscores
    word_cleaned = re.sub(r"\s+", "_", word_cleaned)
    # Remove all non-alphanumeric characters (except underscores)
    word_cleaned = re.sub(r"[^\w\s]", "", word_cleaned)
    return word_cleaned


def cards_to_dict(cards: list[CardRawData]) -> dict[WordWithContext, CardRawData]:
    cards_dict: dict[WordWithContext, CardRawData] = {}
    for card in cards:
        cards_dict[WordWithContext(card.word, "")] = card
    return cards_dict
