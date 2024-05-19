import json
import logging

from .anki_operations import invoke
from ..anki import card_formatter
from ..config import Config
from ..entities import CardRawData, WordWithContext
from ..input.confirm import confirm_action
from ..input.file_operations import copy_image_to_media_directory

logger = logging.getLogger()


def import_card_collection(cards: dict[WordWithContext, CardRawData]):
    for word in cards:
        card_raw_data = cards[word]
        if card_raw_data is None:
            raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")
        import_result = format_and_import_card(card_raw_data)
        if 'error' in import_result:
            logger.error(f"Error occurred during import of card for word [{word.word}]. Import error: [{import_result['error']}]")
            abort = confirm_action("Do you want to abort processing? If no, the processing will be resumed and this card will be skipped")
            if abort:
                raise Exception(f"Aborting processing after error: [{import_result['error']}]")
            else:
                continue
        logger.info(f"Card for word [{word.word}] imported in deck [{Config.DECK_NAME}]")


def format_and_import_card(card_data: CardRawData):
    note = card_formatter.format(card_data, Config.DECK_NAME)
    copy_image_to_media_directory(card_data.image_path)
    result = invoke('addNote', {'note': note})
    return result
