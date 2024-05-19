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


def check_deck_exists(deck_name: str) -> bool:
    # Check existing decks
    result = invoke('deckNames')
    if deck_name not in result['result']:
        logger.info(f"Anki deck '{deck_name}' does not exist")
        return False
    else:
        logger.debug(f"Anki deck '{deck_name}' exists")
        return True


def create_deck(deck_name):
    result = invoke('createDeck', {'deck': deck_name})
    if result.get('error') is None:
        logging.info(f"Deck '{deck_name}' created successfully.")
        return True
    else:
        error_msg = result.get('error')
        logging.error(f"Failed to create deck '{deck_name}': {error_msg}")
        raise Exception(f"An error occurred: {error_msg}")


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


def delete_card_from_deck(deck_name, search_term):
    query = f'"deck:{deck_name}" "{search_term}"'
    card_ids = find_cards(query)
    if not card_ids:
        logger.warning("No cards found with the specified term in the given deck.")
        return False

    delete_result = delete_cards(card_ids)
    if delete_result.get('error') is None:
        logger.info(f"Successfully deleted card for {search_term}")
        return True
    else:
        logger.error(f"Failed to delete cards: {delete_result.get('error')}")
        return False


def find_cards(query):
    return invoke('findCards', {'query': query})['result']


def delete_cards(card_ids):
    return invoke('deleteCards', {'cards': card_ids})


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
