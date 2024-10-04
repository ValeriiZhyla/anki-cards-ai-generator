import logging

import replicate
from openai import OpenAI

from ..config import Config
from ..entities import WordWithContext

client = OpenAI()


def replicate_generate_image(prompt: str) -> str:
    logging.debug(f"Replicate image generation prompt [{prompt}]")

    replicate_client = replicate.Client(api_token=Config.REPLICATE_API_KEY)

    input = {
        "prompt": prompt
    }

    logging.info("Using Replicate model for image generation: " + Config.REPLICATE_MODEL_URL)

    output = replicate_client.run(
        Config.REPLICATE_MODEL_URL,
        input=input
    )

    print(output)

    image_url = output[0]
    logging.debug(f"Replicate generated image URL: {image_url}")
    return image_url
