import logging

from openai import OpenAI

from generator.config import Config
from generator.entities import WordWithContext


def chat_generate_and_save_audio(word: str, target_file_path: str):
    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )

    with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="nova",
            input=word
    ) as response:
        response.stream_to_file(target_file_path)
