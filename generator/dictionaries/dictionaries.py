from generator.config import Config, ENGLISH, GERMAN
from generator.dictionaries import dictionary_english, dictionary_german

import logging


def create_dictionary_url_if_website_exists(word: str) -> str | None:
    if Config.LANGUAGE is ENGLISH:
        return dictionary_english.create_cambridge_url_if_website_exists(word)
    elif Config.LANGUAGE is GERMAN:
        raise dictionary_german.create_dwds_url_if_website_exists(word)
    else:
        logging.error(f"No dictionary for language [{Config.LANGUAGE}]")
        return None
