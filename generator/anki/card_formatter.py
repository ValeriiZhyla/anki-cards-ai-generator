import os

from ..entities import CardRawData


def format(card_data: CardRawData, deck_name: str):
    return {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": card_data.word,
            "Back": card_data.card_text + f'<img src="{os.path.basename(card_data.image_path)}">'
        },
        "options": {
            "allowDuplicate": False,
            "duplicateScope": "deck"
        },
        "tags": []
    }