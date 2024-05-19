import json
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
    version: int = 1

    def __post_init__(self):
            if self.word is None or self.card_text is None or self.image_url is None or self.image_path is None:
                raise ValueError("Attributes cannot be None")
            if self.word == "":
                raise ValueError("Word cannot be empty")
            if self.card_text == "":
                raise ValueError("Card text cannot be empty")
            if self.image_url == "":
                raise ValueError("Image URL cannot be empty")
            if self.image_path == "":
                raise ValueError("Paths cannot be empty")


def serialize_to_json(data):
    # Convert dataclass to dictionary
    data_dict = asdict(data)
    # Serialize dictionary to JSON
    return json.dumps(data_dict, indent=4)
