import logging

import requests


def create_cambridge_link_if_exists(word_or_phrase: str) -> str | None:
    # Convert spaces to hyphens and lowercase the word for the URL
    formatted_word = '-'.join(word_or_phrase.lower().split())

    # Create the URL
    url = f"https://dictionary.cambridge.org/dictionary/english/{formatted_word}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Cambridge Dictionary Page exists for '{word_or_phrase}': {url}")
            return url
        else:
            logging.warning(f"No Cambridge Dictionary entry found for '{word_or_phrase}'.")
            return None
    except requests.RequestException as e:
        logging.error(f"An error occurred while checking the dictionary page: {e}")
        return None
