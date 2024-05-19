import json
import logging
import os

from anki import anki_importer
from generator.entities import WordWithContext, CardRawData
from generator.generate_cards import generate_card_data_path


def check_whether_deck_exists(deck_name):
    deck_exists = anki_importer.check_deck_exists(deck_name)
    if not deck_exists:
        confirmation = confirm_action(f"Deck {deck_name} does not exist. Should it be created? Otherwise the processing will be aborted.")
        if confirmation:
            anki_importer.create_deck(deck_name)
        else:
            raise Exception("Can not create deck without the confirmation")


def filter_words_are_present_in_deck(deck_name, words: list[WordWithContext]) -> list[WordWithContext]:
    words_to_skip: list[WordWithContext] = []
    for word in words:
        card_exists = anki_importer.check_card_exists(deck_name, word.word)
        if card_exists:
            confirmation = confirm_action(
                f"Card for [{word.word}] already exists in the deck [{deck_name}]. Should it be deleted from the deck? Otherwise the word will be skipped.")
            if confirmation:
                anki_importer.delete_card_from_deck(deck_name, word.word)
            else:
                words_to_skip.append(word)

    words_to_process: list[WordWithContext] = [word for word in words if word not in words_to_skip]
    if len(words_to_skip) > 0:
        logging.info(f"Words [{list(map(lambda word: word.word, words_to_skip))}] will be skipped")
        logging.info(f"Words [{list(map(lambda word: word.word, words_to_process))}] will be processed")
    else:
        logging.info(f"All words will be processed")
    return words_to_process


def confirm_action(prompt) -> bool:
    """Ask user to enter 'yes' or 'no' (or any affirmative) to confirm an action.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        bool: True if user enters a positive confirmation, False otherwise.
    """
    # Define a set of affirmative responses
    positive_responses = {"yes", "y", "ye", "ok", "true", "1"}

    # Display the prompt with a default indication
    response = input(f"{prompt} [y/N]: ").strip().lower()

    # Return True if response is in affirmative, False otherwise
    return response in positive_responses


def cards_in_directory(processing_directory: str) -> list[CardRawData]:
    return read_json_files_as_objects(processing_directory)


def list_json_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]


def read_json_files_as_objects(directory):
    files = list_json_files(directory)
    objects = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            obj = CardRawData(**data)
            objects.append(obj)
    return objects


def discard_invalid_cards(processing_directory: str, existing_cards: list[CardRawData]) -> list[CardRawData]:
    valid_cards: list[CardRawData] = []
    for card in existing_cards:
        image_path = card.image_path
        if file_exists_and_has_bytes(image_path):
            logging.info(f"Image [{image_path}] exists, card for word [{card.word}] is valid")
            valid_cards.append(card)
        else:
            logging.info(f"Image [{image_path}] does not exist, card for word [{card.word}] is not valid")
            confirmation = confirm_action(f"Card for [{card.word}] is invalid. Should the card file be deleted? Otherwise the processing will be aborted.")
            if confirmation:
                file_path = generate_card_data_path(processing_directory, card.word)
                os.remove(file_path)
    return valid_cards


def file_exists_and_has_bytes(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Check if the file is not empty (has bytes)
        if os.path.getsize(file_path) > 0:
            return True
    return False


def cards_to_dict(cards: list[CardRawData]) -> dict[WordWithContext, CardRawData]:
    cards_dict: dict[WordWithContext, CardRawData] = {}
    for card in cards:
        cards_dict[WordWithContext(card.word, "")] = card
    return cards_dict
