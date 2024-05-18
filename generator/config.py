import datetime
import os
import logging


class Config:
    OPENAI_API_KEY: str = None
    SECONDS_WAIT_BETWEEN_DALLE_CALLS: int = 20
    DEFAULT_DECK: str = "ai-generated-cards_" + datetime.datetime.now().strftime("%Y-%m-%d")
    DEFAULT_ANKI_MEDIA_FOLDER: str = None

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
    def setup_default_anki_media_folder(cls):
        if os.name == "nt":
            user_profile = os.getenv('USERPROFILE', 'C:\\Users\\Default')
            cls.DEFAULT_ANKI_MEDIA_FOLDER = os.path.join(user_profile, 'AppData', 'Roaming', 'Anki2', 'User 1', 'collection.media')
        elif os.name == 'posix':
            home_path = os.path.expanduser('~')
            cls.DEFAULT_ANKI_MEDIA_FOLDER = os.path.join(home_path, '.local', 'share', 'Anki2', 'User 1', 'collection.media')
        else:
            raise EnvironmentError(f"Unknown OS [{os.name}]")
