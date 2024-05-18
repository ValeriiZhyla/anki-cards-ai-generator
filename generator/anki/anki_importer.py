import json
import logging
import os
import shutil

import requests

from ..anki import card_formatter
from ..config import Config
from ..entities import CardRawData, WordWithContext

logger = logging.getLogger()


def import_card_collection(cards: dict[WordWithContext, CardRawData]):
    for word in cards:
        card_raw_data = cards[word]
        if card_raw_data is None:
            raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")
        import_result = format_and_import_card(card_raw_data)
        print(import_result)
        # TODO react to anki response
        # TODO unit tests for anki interaction
        logger.info(f"Card for word [{word.word}] imported in deck [{Config.DECK_NAME}]")


def format_and_import_card(card_data: CardRawData):
    note = card_formatter.format(card_data, Config.DECK_NAME)
    # TODO add if card exists in deck then generate new name (e.g with (Copy) and number)
    copy_image_to_media_directory(card_data.image_path)
    result = invoke('addNote', {'note': note})
    return result


def check_and_create_deck_if_not_exists(deck_name):
    # Check existing decks
    result = invoke('deckNames')
    if deck_name not in result['result']:
        # Deck does not exist, create it
        invoke('createDeck', params={'deck': deck_name})
        logger.info(f"Anki deck '{deck_name}' created")
    else:
        logger.info(f"Anki deck '{deck_name}' exists")


def check_card_exists(deck_name, search_term):
    query = f'"deck:{deck_name}" "{search_term}"'
    # Use the invoke method to send a request to AnkiConnect
    result = invoke("findCards", {"query": query})
    if result['result']:
        logger.info(f"Card with name term [{search_term}] exists in deck [{deck_name}]")
        return True
    else:
        logger.debug(f"Card with name term [{search_term}] does not exist in deck [{deck_name}]")
        return False


def invoke(action, params=None):
    if params is None:
        params = {}
    request = {'action': action, 'version': 6, 'params': params}
    response = requests.post(Config.ANKI_CONNECT_URL, json=request)
    return response.json()


def copy_image_to_media_directory(image_path):
    image_filename = os.path.basename(image_path)
    target_image_path = os.path.join(Config.ANKI_MEDIA_DIRECTORY, image_filename)
    shutil.copy(image_path, target_image_path)
    logger.info(f"Image [{image_filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")
