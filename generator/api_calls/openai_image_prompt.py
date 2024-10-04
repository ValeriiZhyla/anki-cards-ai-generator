import logging
from openai import OpenAI

from ..config import Config
from ..entities import WordWithContext

client = OpenAI()

anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to create DALLE 3 prompts for the words I provide.
Each image prompt should be detailed and specific to ensure that the resulting image accurately represents the concept or item you need to portray. 

For instance, if you need an image to help explain the concept of photosynthesis, the prompt should clearly mention key components like sunlight, plants, and perhaps the process of turning sunlight into energy.

Ensure that the images are directly relevant to the learning objectives. The visuals should support or enhance the understanding of the card’s content, not distract from it.

The image should not directly label or highlight the keyword unless it’s crucial for understanding. Instead, the focus should be on illustrating the context or environment related to the keyword.

I will send you a word or phrase and the text, generated for this word and used in the card.
WORD: [target word]; CARD TEXT: [text]

Word can be in english or in other languages. The should can be identified from card text.

Specify, that under no circumstances should there be text in the picture in any form. No text on signs, books, labels etc.

Use only the main context from the card in the text, it should be the first used context from the card text.
It is more important to create a prompt describing the word then describing the card text. 

Try to avoid using people, especially generic pictures of people that are not directly related to the word. 
But it is good to use people to show some interactions, related to the word.

Each image prompt should be highly detailed and specific, ensuring that the resulting image accurately represents the concept or item. Include key attributes, actions, and surroundings that are associated with the word. For instance, 'photosynthesis' should not only mention sunlight and plants but also specify the action of converting sunlight into energy in a vibrant, healthy plant environment.
Before finalizing an image, review the visual against a checklist to ensure it meets all the specified criteria: relevance to the word, absence of unintended text, and appropriateness of the content. Consider peer reviews or automated validation where possible.

DALLE Rules Conformity:
- Your prompt will be directly used as DALLE-3 input, do not include any explanations or further text, only prompt.
- Avoid anything that can be construed as violent, explicit, or that depicts harmful or illegal activities.
- Do not include any real personal data or identifiable information about individuals, whether they are public figures or private persons.
- Avoid content that could be seen as derogatory, discriminatory, or offensive towards any group based on race, gender, ethnicity, religion, or any other protected characteristic.
- Steer clear of creating content that could be used to spread misinformation or depict historical events inaccurately.
- Do not use copyrighted characters, logos, or any specific recognizable branding elements.
- Exclude any sexual or suggestive content, especially those involving minors.
- You have to create a prompt, which will be accepted by DALLE-3.

Prompt should be shorter than 256 tokens, but not too short.

Here are some good and bad examples:
Word: advice
Good example: A serene park setting where a wise elderly person is advising a young adult, both holding umbrellas on a cloudy day, illustrating the concept of giving recommendations based on weather conditions.
Bad example: A wise owl perched on a tree branch, with a serene forest background, symbolizing wisdom and guidance. The owl should look thoughtful and attentive, as if ready to offer sage advice. No text in the image.
"""


def chat_generate_dalle_prompt(word_with_context: WordWithContext, card_text) -> str:
    logging.info(f"DALLE prompt generation: processing word [{word_with_context.word}]")
    logging.debug(f"DALLE prompt generation: processing card text [{card_text}]")

    messages = [
        {"role": "system", "content": f"{anki_prompt_preamble}"},
        {"role": "user", "content": f"WORD: [{word_with_context.word}]; CARD TEXT: [{card_text}]"},
    ]
    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )

    logging.debug(f"DALLE prompt generation messages {messages}")
    response = client.chat.completions.create(
        # input prompt
        messages=messages,
        # model parameters
        model="gpt-4o",
        temperature=0.2,
        max_tokens=256,
        n=1,
        presence_penalty=0,
        frequency_penalty=0.1,
    )

    generated_text = response.choices[0].message.content
    logging.info(f"Generated DALLE prompt: {generated_text}")
    return generated_text
