import os

from . import anki_operations
from ..entities import CardRawDataV1


def get_front_html(card_data: CardRawDataV1) -> str:
    formatted_text = card_data.card_text.replace('. ', '.<br>')

    front_content = f"""
    <div style="text-align: center; max-width: 80%; margin: auto; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.5; padding: 10px;">
        <!-- Image -->
        <img src="{os.path.basename(card_data.image_path)}" style="max-width: 100%; max-height: 500px; height: auto; width: auto;">
        
        <!-- Delimiter -->
        <hr style="margin-top: 20px; margin-bottom: 20px;">
        
        <!-- Text -->
        <p style="text-align: justify;">{formatted_text}</p>
        
        <!-- Delimiter -->
        <hr style="margin-top: 20px; margin-bottom: 20px;">
        
        <!-- Dictionary Link and Audio Button -->
        <div>
    """

    # If there's a dictionary URL, add a link to it
    if card_data.dictionary_url:
        front_content += f"""
            <a href='{card_data.dictionary_url}' target='_blank' style='margin-right: 20px;'>Cambridge Dictionary</a>
        """

    # Add audio if exists
    if card_data.audio_path:
        audio_tag = f"[sound:{os.path.basename(card_data.audio_path)}]"
        front_content += f"{audio_tag}"

    front_content += """
        </div>
    </div>
    """
    return front_content

def get_back_html(card_data: CardRawDataV1) -> str:
    return f"""
    <div style='font-family: Arial, sans-serif; font-size: 20px; text-align: center; margin-bottom: 20px;'>
        {card_data.word}
    </div>
    """

def format(card_data: CardRawDataV1, deck_name: str):
    # Ensure sentences end with a new line in HTML and handle text styling
    # TODO make nice-looking card!
    # TODO Create HTML content for the back of the card with added CSS for styling
    # TODO Some templates
    # TODO Also use some styling for word
    front_content = get_front_html(card_data)
    back_content = get_back_html(card_data)

    # Construct the note dictionary with HTML content
    return {
        "deckName": deck_name,
        "modelName": "Basic (type in the answer)",
        "fields": {
            "Front": front_content,
            "Back": back_content
        },
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck"
        },
        "tags": [anki_operations.word_to_tag(card_data.word), "ai-generated"]
    }
