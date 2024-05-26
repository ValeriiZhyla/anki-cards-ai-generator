import logging

from generator.api_calls.text_prompt_by_language import english_prompt_text, german_prompt_text
from generator.config import Config, ENGLISH, GERMAN


def get_system_prompt_by_language():
    if Config.LANGUAGE == ENGLISH:
        return english_prompt_text.get_prompt()
    elif Config.LANGUAGE == GERMAN:
        return german_prompt_text.get_prompt()
    else:
        logging.error(f"No text prompt for language [{Config.LANGUAGE}]")
        return None
