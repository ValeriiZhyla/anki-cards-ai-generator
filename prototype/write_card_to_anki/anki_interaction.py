import base64
import os
import shutil

import requests
import json


def invoke(action, params={}):
    request = {'action': action, 'version': 6, 'params': params}
    response = requests.post('http://localhost:8765', json=request)
    return response.json()


def add_note_with_image(deck_name, front, back, image_filename):
    anki_media_folder = 'C:\\Users\\User\\AppData\\Roaming\\Anki2\\User 1\\collection.media'

    target_image_path = os.path.join(anki_media_folder, image_filename)

    shutil.copy(image_filename, target_image_path)

    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back + f'<img src="{os.path.basename(image_filename)}">'
        },
        "options": {
            "allowDuplicate": False,
            "duplicateScope": "deck"
        },
        "tags": []
    }
    result = invoke('addNote', {'note': note})
    return result


# Example usage
deck = "TestDeck"
front_text = "Question or Term"
back_text = "Definition or Answer"
image_file_path = "./testimage.jpg"

if __name__ == "__main__":
    response = add_note_with_image(deck, front_text, back_text, image_file_path)
    print(response)
