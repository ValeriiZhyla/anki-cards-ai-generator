import logging
import re

import requests


def remove_german_articles(text):
    # Define a regular expression pattern for German articles
    pattern = r'\b(der|die|das|ein|eine|eines|einem|einer|den|dem|des)\b'

    # Use re.sub() to replace the articles with an empty string
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Strip leading/trailing whitespace that might have been left
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Replace multiple spaces with one
    return cleaned_text.strip()


def create_dwds_url_if_website_exists(word: str) -> str | None:
    word = remove_german_articles(word)
    formatted_word = '-'.join(word.lower().split())

    # Create the URL for DWDS
    base_url = "https://www.dwds.de/wb/"
    url = f"{base_url}{formatted_word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Check if the specific error message is in the response text
            error_message = f"Es tut uns leid, Ihre Anfrage <strong>{formatted_word}</strong> ist nicht in unseren gegenwartssprachlichen lexikalischen Quellen vorhanden."
            if error_message in response.text:
                logging.warning(f"No DWDS dictionary entry found for '{word}'.")
                return None
            else:
                logging.info(f"DWDS dictionary page exists for '{word}': {url}")
                return url
        else:
            logging.warning(f"No DWDS dictionary entry found for '{word}'.")
            return None
    except requests.RequestException as e:
        logging.error(f"An error occurred while checking the dictionary page: {e}")
        return None
