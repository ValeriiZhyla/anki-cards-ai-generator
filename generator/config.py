import os
import logging


class Config:
    OPENAI_API_KEY: str = None
    SECONDS_WAIT_BETWEEN_DALLE_CALLS: int = 20

    @classmethod
    def setup_openai_api_key(cls):
        if cls.OPENAI_API_KEY is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if openai_api_key is None:
                raise EnvironmentError("OPENAI_API_KEY environment variable is not set")
            cls.OPENAI_API_KEY = openai_api_key
            logging.info("OPENAI_API_KEY set from environment variable")
        else:
            logging.info("OPENAI_API_KEY set from input parameters")

    @classmethod
    def setup_logging(cls):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S'
                            )
        logging.info("Logger configured")
