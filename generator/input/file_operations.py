import json
import logging
import os
import shutil

import requests

from generator.config import Config

from generator.entities import CardRawData, WordWithContext, word_to_filename


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


def save_text(content: str, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    logging.debug(f"Text saved as {path}")


def generate_image_path(processing_directory_path: str, word: WordWithContext):
    return os.path.join(processing_directory_path, word_to_filename(word) + ".png")


def generate_card_data_path(processing_directory_path, word):
    return os.path.join(processing_directory_path, word_to_filename(word) + ".json")


def download_and_save_image(url, image_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Image saved as {image_path}")
    else:
        raise IOError(f"Failed to retrieve image from URL: {url}. Status code: {response.status_code}")


def copy_image_to_media_directory(image_path):
    image_filename = os.path.basename(image_path)
    target_image_path = os.path.join(Config.ANKI_MEDIA_DIRECTORY, image_filename)
    shutil.copy(image_path, target_image_path)
    logging.info(f"Image [{image_filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")
