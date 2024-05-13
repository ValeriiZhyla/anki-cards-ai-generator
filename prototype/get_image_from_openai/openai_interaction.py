import os

from openai import OpenAI

client = OpenAI()

anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to create DALLE 3 prompts for the words I provide.
Each image prompt should be detailed and specific to ensure that the resulting image accurately represents the concept or item you need to portray. 

For instance, if you need an image to help explain the concept of photosynthesis, the prompt should clearly mention key components like sunlight, plants, and perhaps the process of turning sunlight into energy.

Ensure that the images are directly relevant to the learning objectives. The visuals should support or enhance the understanding of the card’s content, not distract from it.

The image should not directly label or highlight the keyword unless it’s crucial for understanding. Instead, the focus should be on illustrating the context or environment related to the keyword.

Your prompt will be directly used as DALLE-3 input, do not include any explanations or further text, only prompt.
Avoid anything that can be construed as violent, explicit, or that depicts harmful or illegal activities.
Do not include any real personal data or identifiable information about individuals, whether they are public figures or private persons.
Avoid content that could be seen as derogatory, discriminatory, or offensive towards any group based on race, gender, ethnicity, religion, or any other protected characteristic.
Steer clear of creating content that could be used to spread misinformation or depict historical events inaccurately.
Do not use copyrighted characters, logos, or any specific recognizable branding elements.
Exclude any sexual or suggestive content, especially those involving minors.
You have to create a prompt, which will be accepted by DALLE-3.

I will send you a word and the card, generated for this word.
"""

temperature: float = 0.2
presence_penalty: float = 0
frequency_penalty: float = 0.1
response_number = 1
model: str = "gpt-4-turbo"
max_tokens: int = 256
n: int = 1


def chat_generate_prompt(word: str, card_text) -> str:
    messages = [
        {"role": "system", "content": f"{anki_prompt_preamble}"},
        {"role": "user", "content": f"Word: {word}; Text: {card_text}"},
    ]
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key == None:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set")
    client = OpenAI(
        api_key=openai_api_key
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
    )

    generated_text = response.choices[0].message.content
    return generated_text


def chat_generate_image(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url


prompt = chat_generate_prompt("pagan",
                              "A person who follows a polytheistic or pre-Christian religion (not a follower of one of the world's main religions) is referred to as a ______. Ancient Romans might have considered the Norse or the Celts as ______s. This term can also describe someone who has little or no religion and delights in sensual pleasures and material goods.")
print(prompt)

image_url = chat_generate_image(prompt)
print(image_url)
