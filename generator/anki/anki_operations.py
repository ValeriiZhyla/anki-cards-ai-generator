import logging

import requests

from generator.config import Config


def check_deck_exists(deck_name: str) -> bool:
    # Check existing decks
    result = invoke('deckNames')
    if deck_name not in result['result']:
        logging.info(f"Anki deck '{deck_name}' does not exist")
        return False
    else:
        logging.debug(f"Anki deck '{deck_name}' exists")
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


def check_card_exists(deck_name, word):
    tag = word_to_tag(word)
    existing_cards = find_all_cards_with_tag(deck_name, tag)
    if len(existing_cards) >= 1:
        logging.info(f"Card with tag [{tag}] exists in deck [{deck_name}]")
        return True
    else:
        logging.debug(f"Card with tag [{tag}] does not exist in deck [{deck_name}]")
        return False


def delete_card_from_deck(deck_name: str, word: str) -> bool:
    tag = word_to_tag(word)
    logging.info(f"Deleting card [{word}] from deck [{deck_name}] using tag [{tag}]")
    card_ids = find_all_cards_with_tag(deck_name, tag)
    if not card_ids:
        logging.warning("No cards found with the specified term in the given deck.")
        return True
    delete_result = delete_cards_by_id(card_ids)
    if delete_result.get('error') is None:
        # sometimes cards are not deleted -> retry
        remaining_cards = find_all_cards_with_tag(deck_name, tag)
        if len(remaining_cards) == 0:
            logging.info(f"Successfully deleted card for [{word}]")
            return True
        else:
            logging.error(f"Deletion returned no error, but some cards with tag [{tag}] are still in the deck - {remaining_cards}."
                          f" This happens, if a card is in review process. Restart Anki and try again.")
            return False

    else:
        logging.error(f"Failed to delete cards: {delete_result.get('error')}")
        return False


def find_all_cards_with_tag(deck_name, tag):
    card_ids = find_cards(f'"deck:{deck_name}" tag:"{tag}"')
    logging.info(f"Found [{len(card_ids)}] cards with tag [{tag}] in deck [{deck_name}]")
    logging.debug(f"Found cards with tag {tag} in deck [{deck_name}]: [{card_ids}]")
    return card_ids


def find_cards(query):
    return invoke('findCards', {'query': query})['result']


def delete_cards_by_id(card_ids):
    result = invoke('deleteNotes', {'notes': card_ids})
    logging.info(f"Deletion performed for cards with ids {card_ids}")
    return result


def get_all_card_ids_from_deck(deck_name: str):
    return invoke('findCards', {'query': f'deck:"{deck_name}"'})


def get_card_info(card_ids):
    return invoke('cardsInfo', {'cards': card_ids})


def get_all_words_from_deck(deck_name) -> list[str]:
    card_ids = get_all_card_ids_from_deck(deck_name)['result']
    if not card_ids:
        logging.info(f"No cards found in deck '{deck_name}'.")
        return []

    cards_info = get_card_info(card_ids)['result']
    words = [card['fields']['Front']['value'] for card in cards_info]
    return words


def invoke(action, params=None):
    if params is None:
        params = {}
    request = {'action': action, 'version': 6, 'params': params}
    response = requests.post(Config.ANKI_CONNECT_URL, json=request)
    return response.json()


def word_to_tag(word: str) -> str:
    formatted_word = word.replace(' ', '_').lower()  # Format word for consistent tagging
    return formatted_word
