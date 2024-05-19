import argparse
import logging

import generator.input.file_operations
from generator.entities import WordWithContext, CardRawData
from generator.input import read_input_file
from generator.anki import anki_importer
from generator.config import Config
from generator import generate_cards, entities
from generator import validation


def process_existing_cards(input_words: list[WordWithContext]):
    input_words_without_context: list[str] = list(map(lambda word_with_context: word_with_context.word, input_words))

    logging.info("Processing existing cards")
    existing_cards: list[CardRawData] = generator.input.file_operations.cards_in_directory(Config.PROCESSING_DIRECTORY_PATH)
    existing_cards_filtered: list[CardRawData] = [card for card in existing_cards if card.word in input_words_without_context]
    existing_cards_validated: list[CardRawData] = validation.discard_invalid_cards(Config.PROCESSING_DIRECTORY_PATH, existing_cards_filtered)
    existing_cards_data: dict[WordWithContext, CardRawData] = entities.cards_to_dict(existing_cards_validated)
    anki_importer.import_card_collection(existing_cards_data)
    logging.info("All existing cards processed")


def process_new_cards(input_words: list[WordWithContext]):
    generated_cards_data: dict[WordWithContext, CardRawData] = generate_cards.generate_text_and_image(input_words)
    logging.info("Card generation completed")
    anki_importer.import_card_collection(generated_cards_data)
    logging.info("Import in Anki completed")


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some data for Anki cards.")

    # Required positional arguments
    parser.add_argument('input_file', type=str, help="Path to the input file")
    parser.add_argument('processing_directory', type=str, help="Path of the directory where the data should be processed")

    # Optional arguments
    parser.add_argument('--openai_api_key', type=str, help="API key for OpenAI. If not set, the value from environment variable OPENAI_API_KEY is used", default=None)
    parser.add_argument('--deck_name', type=str, help="Name of the Anki deck. If not set, the default name is generated", default=None)
    parser.add_argument('--anki_media_directory_path', type=str, help="Path to the Anki media directory. If not set, the standard path for each OS is used", default=None)

    # Parse arguments
    args = parser.parse_args()

    # Setup config
    Config.setup_logging()
    Config.set_openai_key_or_use_default(args.openai_api_key)
    Config.set_anki_deck_name_or_use_default(args.deck_name)
    Config.set_anki_media_directory_or_use_default(args.anki_media_directory_path)
    Config.set_processing_directory_path(args.processing_directory)
    Config.check_anki_connect()

    # validate environment and read inputs
    validation.check_whether_deck_exists(Config.DECK_NAME)
    input_words: list[WordWithContext] = read_input_file.read_file_based_on_extension(args.input_file)
    filtered_words: list[WordWithContext] = validation.filter_words_are_present_in_deck(Config.DECK_NAME, input_words)

    # Processing
    process_existing_cards(filtered_words)
    logging.info("Existing cards processed")
    process_new_cards(filtered_words)
    logging.info("New cards processed")
    logging.info("Processing completed")


if __name__ == '__main__':
    main()
