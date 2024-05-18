import json
import logging
import os

import requests

from generator.anki import card_formatter
from generator.config import Config
from generator.entities import CardRawData, WordWithContext

logger = logging.getLogger()


class AnkiImporter:
    deck: str = ""
    anki_media_folder: str = ""
    anki_connect_url: str = "http://localhost:8765"

    # TODO check whether connect is active

    def __init__(self, deck=None, anki_media_folder=None):
        if deck is None or deck == "":
            self.deck = Config.DEFAULT_DECK
            logger.debug(f"Deck is not specified. Default deck [{self.deck}] will be used")
        else:
            self.deck = deck
        logger.info(f"Deck [{self.deck}] will be used")

        if anki_media_folder is None or anki_media_folder == "":
            self.anki_media_folder = Config.DEFAULT_ANKI_MEDIA_FOLDER
            logger.debug(f"Anki media folder is not specified. Default media folder [{self.anki_media_folder}] will be used")
        else:
            self.anki_media_folder = anki_media_folder
            logger.info(f"Anki media folder [{self.anki_media_folder}] will be used")

        if os.path.isdir(self.anki_media_folder):
            logger.debug(f"Anki media folder [{self.anki_media_folder}] exists")
        else:
            raise IOError(f"Anki media folder [{self.anki_media_folder}] does not exist")

    def import_card_collection(self, cards: dict[WordWithContext, CardRawData]):
        for word in cards:
            card_raw_data = cards[word]
            if card_raw_data is None:
                raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")
            self.format_and_import_card(card_raw_data)
            # TODO react for response
            logger.info(f"Card for word [{word.word}] imported in deck [{self.deck}]")

    def format_and_import_card(self, card_data: CardRawData):
        note = card_formatter.format(card_data)
        result = self.invoke('addNote', {'note': note})
        return result

    def invoke(self, action, params=None):
        if params is None:
            params = {}
        request = {'action': action, 'version': 6, 'params': params}
        response = requests.post(self.anki_connect_url, json=request)
        return response.json()
