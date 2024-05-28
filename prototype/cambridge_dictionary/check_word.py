import requests


def create_cambridge_link_if_exists(word_or_phrase: str) -> str | None:
    # Convert spaces to hyphens and lowercase the word for the URL
    formatted_word = '-'.join(word_or_phrase.lower().split())

    # Create the URL
    base_url: str = "https://dictionary.cambridge.org/dictionary/english/"
    url = f"{base_url}{formatted_word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if response.url == base_url:
                print(f"No Cambridge Dictionary entry found for '{word_or_phrase}'.")
                return None
            print(f"Cambridge Dictionary page exists for '{word_or_phrase}': {url}")
            return url
        else:
            print(f"No Cambridge Dictionary entry found for '{word_or_phrase}'.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while checking the dictionary page: {e}")
        return None

print(create_cambridge_link_if_exists("affecting"))
print(create_cambridge_link_if_exists("aaaxxxzzz"))
print("")
