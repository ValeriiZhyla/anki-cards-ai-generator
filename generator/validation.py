import logging
import os

import requests

from generator.anki import anki_operations
from generator.config import Config
from generator.entities import WordWithContext, CardRawDataV1
from generator.input import file_operations
from generator.input.confirm import confirm_action
from generator.input.file_operations import generate_card_data_path


def check_anki_connect():
    try:
        response = requests.get(Config.ANKI_CONNECT_URL)
        if response.status_code == 200:
            logging.info("AnkiConnect is running")
        else:
            raise IOError("AnkiConnect is installed but returned a non-OK status code:", response.status_code)
    except requests.exceptions.ConnectionError:
        raise IOError("Failed to connect to AnkiConnect. It might be not running")


def check_whether_deck_exists():
    deck_name = Config.DECK_NAME
    deck_exists = anki_operations.check_deck_exists(deck_name)
    if not deck_exists:
        confirmation = confirm_action(f"Deck {deck_name} does not exist. Should it be created? Otherwise the processing will be aborted.")
        if confirmation:
            anki_operations.create_deck(deck_name)
        else:
            raise Exception("Can not create deck without the confirmation")


def filter_words_are_present_in_deck(deck_name, words: list[WordWithContext]) -> list[WordWithContext]:
    words_to_skip: list[WordWithContext] = []
    for word in words:
        card_exists = anki_operations.check_card_exists(deck_name, word.word)
        if card_exists:
            deletion_confirmation = confirm_action(
                f"Card for [{word.word}] already exists in the deck [{deck_name}]. Should it be deleted from the deck? Otherwise the word will be skipped.")
            if deletion_confirmation:
                deletion_successful = anki_operations.delete_card_from_deck(deck_name, word.word)
                if not deletion_successful:
                    skip_confirmation = confirm_action(
                        f"Card for [{word.word}] is not deleted. Should it be skipped? Otherwise the duplicate can be imported.")
                    if skip_confirmation:
                        words_to_skip.append(word)
            else:
                words_to_skip.append(word)

    words_to_process: list[WordWithContext] = [word for word in words if word not in words_to_skip]
    if len(words_to_skip) > 0:
        logging.info(f"Words {list(map(lambda word: word.word, words_to_skip))} will be skipped")
        logging.info(f"Words {list(map(lambda word: word.word, words_to_process))} will be processed")
    else:
        logging.info(f"All words will be processed")
    return words_to_process


def discard_invalid_cards(processing_directory: str, existing_cards: list[CardRawDataV1]) -> list[CardRawDataV1]:
    valid_cards: list[CardRawDataV1] = []
    for card in existing_cards:
        required_files: list[str] = [card.audio_path, card.image_path]
        if file_operations.all_files_exist_and_are_not_empty(required_files):
            logging.info(f"All files from {required_files} exist, card for word [{card.word}] is valid")
            valid_cards.append(card)
        else:
            logging.info(f"Some files from [{required_files}] does not exist, card for word [{card.word}] is not valid")
            confirmation = confirm_action(f"Card for [{card.word}] is invalid. Should the card file be deleted? Otherwise the processing will be aborted.")
            if confirmation:
                file_path = generate_card_data_path(processing_directory, card.word)
                os.remove(file_path)
    return valid_cards
