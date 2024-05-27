import datetime
import logging
import os

ENGLISH = "english"
GERMAN = "german"

A1 = "A1"
A2 = "A2"
B1 = "B1"
B2 = "B2"
C1 = "C1"
C2 = "C2"


class Config:
    OPENAI_API_KEY: str = None
    SECONDS_WAIT_BETWEEN_DALLE_CALLS: int = 20
    DECK_NAME: str = None
    ANKI_MEDIA_DIRECTORY: str = None
    PROCESSING_DIRECTORY_PATH: str = None

    ANKI_CONNECT_URL: str = "http://localhost:8765"

    SUPPORTED_LANGUAGES: list[str] = [ENGLISH, GERMAN]
    DEFAULT_LANGUAGE: str = ENGLISH
    LANGUAGE: str = None

    SUPPORTED_LEVELS: list[str] = [A1, A2, B1, B2, C1, C2]
    DEFAULT_LEVEL: str = C1
    LEVEL: str = None

    @classmethod
    def set_processing_directory_path(cls, path: str):
        if path is None:
            raise ValueError("Processing directory path must be set")
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise NotADirectoryError(f"The path {path} exists but is not a directory.")
        else:
            os.makedirs(path)
            logging.info(f"Directory created at {path}")
        cls.PROCESSING_DIRECTORY_PATH = path
        logging.info(f"Processing directory path set to [{path}]")

    @classmethod
    def set_anki_deck_name_or_use_default(cls, deck_name: str):
        if deck_name is None:
            cls.DECK_NAME = "ai-generated-cards_" + datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            cls.DECK_NAME = deck_name
        logging.info(f"Using anki deck name: {cls.DECK_NAME}")

    @classmethod
    def set_anki_media_directory_or_use_default(cls, anki_media_directory: str):
        if anki_media_directory is None:
            cls.setup_default_anki_media_directory()
        else:
            cls.ANKI_MEDIA_DIRECTORY = anki_media_directory

        if os.path.isdir(cls.ANKI_MEDIA_DIRECTORY):
            logging.debug(f"Anki media directory [{cls.ANKI_MEDIA_DIRECTORY}] exists")
        else:
            raise IOError(f"Anki media directory [{cls.ANKI_MEDIA_DIRECTORY}] does not exist")
        logging.info(f"Using anki media directory: {cls.ANKI_MEDIA_DIRECTORY}")

    @classmethod
    def set_openai_key_or_use_default(cls, api_key: str):
        if api_key is None:
            cls.setup_openai_api_key_from_environment()
        else:
            cls.OPENAI_API_KEY = api_key

    @classmethod
    def set_language_or_use_default(cls, language: str):
        if language is None:
            cls.LANGUAGE = cls.DEFAULT_LANGUAGE
        elif language.lower() in cls.SUPPORTED_LANGUAGES:
            cls.LANGUAGE = language.lower()
        else:
            raise Exception(f"Language [{language}] not supported. Supported languages: {cls.SUPPORTED_LANGUAGES}")
        logging.info(f"Language set to [{cls.LANGUAGE}]")

    @classmethod
    def set_level_or_use_default(cls, level):
        if level is None:
            cls.LEVEL = cls.DEFAULT_LEVEL
        elif level.upper() in cls.SUPPORTED_LEVELS:
            cls.LEVEL = level.upper()
        else:
            raise Exception(f"Language level [{level}] not supported. Supported language levels: {cls.SUPPORTED_LEVELS}")
        logging.info(f"Language level set to [{cls.LEVEL}]")

    @classmethod
    def setup_openai_api_key_from_environment(cls):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key is None:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set")
        cls.OPENAI_API_KEY = openai_api_key
        logging.info("OPENAI_API_KEY set from environment variable")

    @classmethod
    def setup_logging(cls):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S'
                            )
        logging.info("Logger configured")

    @classmethod
    def setup_default_anki_media_directory(cls):
        if os.name == "nt":
            user_profile = os.getenv('USERPROFILE', 'C:\\Users\\Default')
            cls.ANKI_MEDIA_DIRECTORY = os.path.join(user_profile, 'AppData', 'Roaming', 'Anki2', 'User 1', 'collection.media')
        elif os.name == 'posix':
            home_path = os.path.expanduser('~')
            cls.ANKI_MEDIA_DIRECTORY = os.path.join(home_path, '.local', 'share', 'Anki2', 'User 1', 'collection.media')
        else:
            raise EnvironmentError(f"Unknown OS [{os.name}]")
        logging.info(f"Use default anki media directory [{cls.ANKI_MEDIA_DIRECTORY}]")
