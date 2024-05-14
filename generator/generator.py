import logging
import os
import re

import requests

from generator.entities import Word
from openai_api import picture, text

logger = logging.getLogger()

class Generator:
    def generate_text_and_picture(self, input_words: list[Word], processing_folder_path: str):
        logger.info(f"Starting generation of text and pictures for words: {input_words}")
        logger.debug(f"Using the folder {processing_folder_path} for processing")

        for word in input_words:
            card_text = text.chat_generate_text(word)
            picture_prompt = picture.chat_generate_dalle_prompt(word, card_text)
            picture_url = picture.chat_generate_image(picture_prompt)
            self.download_and_save_image(picture_url, self.generate_picture_path(processing_folder_path, word))
            self.save_card_text(card_text, self.generate_text_path(processing_folder_path, word))

    def download_and_save_image(self, url, image_path):
        # Send a GET request to the image URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a binary file in write mode and save the image content
            with open(image_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Image saved as {image_path}")
        else:
            raise IOError(f"Failed to retrieve image from URL: {url}. Status code: {response.status_code}")

    def save_card_text(self, card_text, text_path):
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(card_text)
        logger.info(f"Text saved as {text_path}")



    def generate_picture_path(self, processing_folder_path: str, word: Word):
        return os.path.join(processing_folder_path, self.word_to_filename(word) + ".png")

    def generate_text_path(self, processing_folder_path, word):
        return os.path.join(processing_folder_path, self.word_to_filename(word) + ".txt")

    def word_to_filename(self, word: Word) -> str:
        # convert to lower case
        word_cleaned = str.lower(word.word)
        # Replace all spaces with underscores
        word_cleaned = re.sub(r"\s+", "_", word_cleaned)
        # Remove all non-alphanumeric characters (except underscores)
        word_cleaned = re.sub(r"[^\w\s]", "", word_cleaned)
        return word_cleaned

    # TODO for each file
    # TODO save each file data in a json: word, context, prompt, text, status
    # TODO create checkpoint system and semi-manual retry mode
    # TODO prompt importable from files
