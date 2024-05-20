import json
import logging
import os
import shutil

import requests

from generator.config import Config

from generator.entities import CardRawDataV1, WordWithContext, word_to_filename


def cards_in_directory(processing_directory: str) -> list[CardRawDataV1]:
    return read_json_files_as_objects(processing_directory)


def list_json_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]


def read_json_files_as_objects(directory):
    files = list_json_files(directory)
    objects = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            obj = CardRawDataV1(**data)
            objects.append(obj)
    return objects


def save_text(content: str, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    logging.debug(f"Text saved as {path}")


def generate_image_path(processing_directory_path: str, word: WordWithContext) -> str:
    return os.path.join(processing_directory_path, word_to_filename(word) + ".png")


def generate_card_data_path(processing_directory_path, word) -> str:
    return os.path.join(processing_directory_path, word_to_filename(word) + ".json")


def generate_audio_path(processing_directory_path: str, word: WordWithContext) -> str:
    return os.path.join(processing_directory_path, word_to_filename(word) + ".mp3")


def download_and_save_image(url, image_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Image saved as {image_path}")
    else:
        raise IOError(f"Failed to retrieve image from URL: {url}. Status code: {response.status_code}")


def copy_to_media_directory(file_path):
    filename = os.path.basename(file_path)
    target_file_path = os.path.join(Config.ANKI_MEDIA_DIRECTORY, filename)
    shutil.copy(file_path, target_file_path)
    if filename.endswith(".png"):
        logging.info(f"Image [{filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")
    elif filename.endswith(".mp3"):
        logging.info(f"Audio file [{filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")
    else:
        logging.info(f"File [{filename}] copied to [{Config.ANKI_MEDIA_DIRECTORY}]")


def all_files_exist_and_are_not_empty(required_files: list[str]) -> bool:
    present_required_files: int = 0
    for required_file in required_files:
        if file_exists_and_has_bytes(required_file):
            logging.info(f"File [{required_file}] exists")
            present_required_files += 1
        else:
            logging.warning(f"File [{required_file}] does not exist or is empty")
    return present_required_files == len(required_files)


def file_exists_and_has_bytes(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Check if the file is not empty (has bytes)
        if os.path.getsize(file_path) > 0:
            return True
    return False
