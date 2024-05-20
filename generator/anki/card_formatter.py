import os

from ..entities import CardRawDataV1


def format(card_data: CardRawDataV1, deck_name: str):
    # Ensure sentences end with a new line in HTML and handle text styling
    formatted_text = card_data.card_text.replace('. ', '.<br>')
    # TODO make nice-looking card!
    # TODO Create HTML content for the back of the card with added CSS for styling
    # TODO Some templates
    # TODO Also use some styling for word
    back_content = f"""
    <div style="text-align: left; max-width: 80%; margin: auto; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.5; padding: 10px;">
        <p style="text-align: justify; margin-bottom: 20px;">{formatted_text}</p>
        <div style="text-align: center;">
            <img src="{os.path.basename(card_data.image_path)}" style="max-width: 100%; max-height: 500px; height: auto; width: auto;">
        </div>
    </div>
    """

    # Construct the note dictionary with HTML content
    return {
        # TODO flip card? Show first text, and the word; But also adjust search
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": card_data.word,
            "Back": back_content
        },
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck"
        },
        "tags": []
    }
