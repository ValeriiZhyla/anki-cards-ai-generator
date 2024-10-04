import os

from openai import OpenAI

client = OpenAI()

anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to 
"""

temperature: float = 0.2
presence_penalty: float = 0
frequency_penalty: float = 0.1
response_number = 1
model: str = "gpt-4-turbo"
max_tokens: int = 256
n: int = 1


def chat_generate_audio(word: str) -> str:
    speech_file_path = f"D:/AnkiProject/anki-cards-ai-generator/prototype/get_audio_from_openai/{word}.mp3"

    with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="nova",
            input=word
    ) as response:
        response.stream_to_file(speech_file_path)
    return speech_file_path


if __name__ == "__main__":
    path = chat_generate_audio("Rindfleischkuchen")
    print(path)
