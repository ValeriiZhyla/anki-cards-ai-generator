import logging
from openai import OpenAI

from ..config import Config
from ..entities import WordWithContext

client = OpenAI()


def chat_generate_image(prompt: str) -> str:
    logging.debug(f"DALLE image generation prompt [{prompt}]")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    logging.debug(f"DALLE generated image URL: {image_url}")
    return image_url
