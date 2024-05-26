import logging

import requests


def create_dwds_url_if_website_exists(word: str) -> str | None:
    # Convert the word to lowercase and remove extra spaces
    formatted_word = word.lower().strip()

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
                print(f"No DWDS dictionary entry found for '{word}'.")
                return None
            else:
                print(f"DWDS dictionary page exists for '{word}': {url}")
                return url
        else:
            print(f"No DWDS dictionary entry found for '{word}'.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while checking the dictionary page: {e}")
        return None
