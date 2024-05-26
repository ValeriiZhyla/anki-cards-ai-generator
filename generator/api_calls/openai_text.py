import logging
from openai import OpenAI

from ..config import Config
from ..entities import WordWithContext
from .text_prompt_by_language import prompt_by_language



def chat_generate_text(word_with_context: WordWithContext) -> str:
    logging.info(f"ChatGPT card text: processing word [{word_with_context.word}] with context [{word_with_context.context}] in language [{Config.LANGUAGE}]")

    system_prompt = prompt_by_language.get_system_prompt_by_language()

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"WORD: [{word_with_context.word}]; CONTEXT: [{word_with_context.context}]"},
    ]

    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )

    logging.debug(f"ChatGPT card generation messages {messages}")

    response = client.chat.completions.create(
        # input prompt
        messages=messages,
        # model parameters
        model="gpt-4o",
        temperature=0.2,  # keep low for conservative answers
        max_tokens=512,
        n=1,
        presence_penalty=0,
        frequency_penalty=0.1,
    )

    generated_text = response.choices[0].message.content
    logging.debug(f"ChatGPT generated card text for word {word_with_context.word}")
    logging.debug(f"ChatGPT card text: {generated_text}")
    return generated_text
