import json
import logging
import os
import shutil

import requests

from generator.anki import card_formatter
from generator.config import Config
from generator.entities import CardRawData, WordWithContext

logger = logging.getLogger()

def import_card_collection(cards: dict[WordWithContext, CardRawData]):
    for word in cards:
        card_raw_data = cards[word]
        if card_raw_data is None:
            raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")
        import_result = format_and_import_card(card_raw_data)
        # TODO react to anki response
        logger.info(f"Card for word [{word.word}] imported in deck [{Config.DECK_NAME}]")

def format_and_import_card(card_data: CardRawData):
    note = card_formatter.format(card_data, Config.DECK_NAME)
    copy_image_to_media_directory(card_data.image_path)
    result = invoke('addNote', {'note': note})
    return result

def invoke(action, params):
    request = {'action': action, 'version': 6, 'params': params}
    response = requests.post(Config.ANKI_CONNECT_URL, json=request)
    return response.json()

def copy_image_to_media_directory(image_path):
    image_filename = os.path.basename(image_path)
    target_image_path = os.path.join(Config.ANKI_MEDIA_DIRECTORY, image_filename)
    shutil.copy(image_path, target_image_path)
    logger.info(f"Image [{image_filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")
