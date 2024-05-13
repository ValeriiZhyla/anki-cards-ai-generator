from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    word: str
    context: str

    def __post_init__(self):
        if self.word is None or self.context is None:
            raise ValueError("Attributes cannot be None")
