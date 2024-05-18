import uuid
from dataclasses import dataclass


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
    card_text_path: str
    picture_prompt: str
    picture_url: str
    picture_path: str

    def __post_init__(self):
        if self.word is None or self.card_text is None or self.card_text_path is None or self.picture_url is None or self.picture_path is None:
            raise ValueError("Attributes cannot be None")
        if self.word == "":
            raise ValueError("Word cannot be empty")
        if self.card_text == "":
            raise ValueError("Card text cannot be empty")
        if self.picture_url == "":
            raise ValueError("Picture URL cannot be empty")
        if self.card_text_path == "" or self.picture_path == "":
            raise ValueError("Paths cannot be empty")