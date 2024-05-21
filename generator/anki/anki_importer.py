import json
import logging

from .anki_operations import invoke
from ..anki import card_formatter
from ..config import Config
from ..entities import CardRawDataV1, WordWithContext
from ..input.confirm import confirm_action
from ..input.file_operations import copy_to_media_directory


def import_card_collection(cards: dict[WordWithContext, CardRawDataV1]):
    for word in cards:
        card_raw_data = cards[word]
        if card_raw_data is None:
            raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")
        import_result = format_and_import_card(card_raw_data)
        if import_result['error']:
            logging.error(f"Error occurred during import of card for word [{word.word}]. Import error: [{import_result['error']}]")
            abort = confirm_action("Do you want to abort processing? If no, the processing will be resumed and this card will be skipped")
            if abort:
                raise Exception(f"Aborting processing after error: [{import_result['error']}]")
            else:
                continue
        logging.info(f"Card for word [{word.word}] imported in deck [{Config.DECK_NAME}]")


def format_and_import_card(card_data: CardRawDataV1):
    note = card_formatter.format(card_data, Config.DECK_NAME)
    copy_to_media_directory(card_data.image_path)
    copy_to_media_directory(card_data.audio_path)
    result = invoke('addNote', {'note': note})
    return result
