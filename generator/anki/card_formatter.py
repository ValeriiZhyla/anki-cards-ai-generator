import os

from ..entities import CardRawData


def format(card_data: CardRawData, deck_name: str):
    # Ensure sentences end with a new line in HTML
    formatted_text = card_data.card_text.replace('. ', '.<br>')

    # Create HTML content for the back of the card with added space
    back_content = f"""
    {formatted_text}<br>
    <div style='text-align: center; margin-top: 20px;'> <!-- Add margin-top for spacing -->
        <img src="{os.path.basename(card_data.image_path)}" style="max-width: 100%; height: auto;">
    </div>
    """

    # Construct the note dictionary with HTML content
    return {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": card_data.word,
            "Back": back_content
        },
        "options": {
            "allowDuplicate": False,
            "duplicateScope": "deck"
        },
        "tags": []
    }