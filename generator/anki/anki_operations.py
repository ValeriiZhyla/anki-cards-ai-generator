import logging

import requests

from generator.anki.anki_importer import logger
from generator.config import Config


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
