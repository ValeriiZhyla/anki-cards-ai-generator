import argparse
import logging

from generator.entities import WordWithContext, CardRawData
from generator.input import read_csv
from generator.anki import anki_importer
from generator.config import Config
from generator import generate_cards


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

    logger = logging.getLogger()

    input_words: list[WordWithContext] = read_csv.read_words_with_context(args.input_file)
    logger.info("Input file processed")
    card_data: dict[WordWithContext, CardRawData] = generate_cards.generate_text_and_image(input_words)
    logger.info("Card generation completed")
    anki_importer.import_card_collection(card_data)
    logger.info("Import in Anki completed")

    logger.info("Processing completed")


if __name__ == '__main__':
    main()
