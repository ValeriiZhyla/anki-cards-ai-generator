import logging
import os
import re
import time

import requests

from generator.config import Config
from generator.entities import WordWithContext, CardRawData
from openai_api import picture, text

logger = logging.getLogger()


def generate_text_and_picture(input_words: list[WordWithContext], processing_folder_path: str) -> dict[WordWithContext, CardRawData]:
    logger.info(f"Starting generation of text and pictures for words: {input_words}")
    logger.info(f"Using the folder {processing_folder_path} for processing")

    words_cards: dict[WordWithContext, CardRawData] = {}

    for word_with_context in input_words:
        card_raw = create_card_for_word(word_with_context, processing_folder_path)
        words_cards[word_with_context] = card_raw
        logger.info("[{}] processed")
        wait_after_word_processing()

    return words_cards


def create_card_for_word(word_with_context, processing_folder_path) -> CardRawData:
    card_text = text.chat_generate_text(word_with_context)
    logger.info("Card text is created")

    picture_prompt = picture.chat_generate_dalle_prompt(word_with_context, card_text)
    picture_url = picture.chat_generate_image(picture_prompt)
    logger.info("Picture is created")

    logger.info("Card text and picture will be saved")
    card_text_path = generate_text_path(processing_folder_path, word_with_context)
    save_card_text(card_text, card_text_path)
    picture_path = generate_picture_path(processing_folder_path, word_with_context)
    download_and_save_image(picture_url, picture_path)
    logger.info(f"Card text and picture are saved in [{processing_folder_path}]")

    card_raw: CardRawData = CardRawData(word=word_with_context.word, card_text=card_text, card_text_path=card_text_path,
                                        picture_prompt=picture_prompt, picture_url=picture_url, picture_path=picture_path)
    return card_raw


def wait_after_word_processing():
    sleep_seconds = Config.SECONDS_WAIT_BETWEEN_DALLE_CALLS
    logger.info(f"Waiting [{sleep_seconds}] seconds after word processing (API RPM)")
    time.sleep(sleep_seconds)


def download_and_save_image(url, image_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Image saved as {image_path}")
    else:
        raise IOError(f"Failed to retrieve image from URL: {url}. Status code: {response.status_code}")


def save_card_text(card_text, text_path):
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(card_text)
    logger.info(f"Card text saved as {text_path}")


def generate_picture_path(processing_folder_path: str, word: WordWithContext):
    return os.path.join(processing_folder_path, word_to_filename(word) + ".png")


def generate_text_path(processing_folder_path, word):
    return os.path.join(processing_folder_path, word_to_filename(word) + ".txt")


def word_to_filename(word: WordWithContext) -> str:
    # convert to lower case
    word_cleaned = str.lower(word.word)
    # Replace all spaces with underscores
    word_cleaned = re.sub(r"\s+", "_", word_cleaned)
    # Remove all non-alphanumeric characters (except underscores)
    word_cleaned = re.sub(r"[^\w\s]", "", word_cleaned)
    return word_cleaned
