import logging
import time

from generator.config import Config
from generator.entities import WordWithContext, CardRawData, serialize_to_json
from generator.input.file_operations import save_text, generate_image_path, generate_card_data_path, download_and_save_image
from generator.openai_api import image, text
from generator.input.confirm import confirm_action


def generate_text_and_image(input_words: list[WordWithContext]) -> dict[WordWithContext, CardRawData]:
    words_total = len(input_words)
    words_remaining = words_total

    logging.info(f"Starting generation of text and images for {words_total} words {list(map(lambda entry: entry.word, input_words))}")

    words_cards: dict[WordWithContext, CardRawData] = {}

    for word_with_context in input_words:
        try:
            card_raw = create_card_for_word(word_with_context)
            words_cards[word_with_context] = card_raw
            logging.info(f"Word [{word_with_context.word}] processed")
        except Exception as e:
            logging.error(f"Failed to process word [{word_with_context.word}] due to {e}")
            abort = confirm_action("Do you want to abort processing? If no, the processing will be resumed and this card will be skipped")
            if abort:
                raise Exception(f"Aborting processing after error: [{e}]")
            else:
                logging.warning(f"Word [{word_with_context.word}] will be skipped")
        words_remaining -= 1
        if words_remaining > 0:
            wait_after_word_processing()
    return words_cards


def create_card_for_word(word_with_context) -> CardRawData:
    card_text = text.chat_generate_text(word_with_context)
    logging.info("Card text is created")

    image_prompt = image.chat_generate_dalle_prompt(word_with_context, card_text)
    image_url = image.chat_generate_image(image_prompt)
    logging.info("Card Image is created")

    image_path = generate_image_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    download_and_save_image(image_url, image_path)
    logging.info(f"Card image is saved as [{image_path}]")

    card_raw: CardRawData = CardRawData(word=word_with_context.word, card_text=card_text, image_prompt=image_prompt, image_url=image_url, image_path=image_path)
    card_data_path = generate_card_data_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    save_text(serialize_to_json(card_raw), card_data_path)
    logging.info(f"Card data is saved as [{card_data_path}]")
    return card_raw


def wait_after_word_processing():
    sleep_seconds = Config.SECONDS_WAIT_BETWEEN_DALLE_CALLS
    logging.info(f"Waiting [{sleep_seconds}] seconds after word processing (API RPM)")
    time.sleep(sleep_seconds)