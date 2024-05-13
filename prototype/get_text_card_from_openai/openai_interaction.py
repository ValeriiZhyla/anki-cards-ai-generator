import os
from openai import OpenAI

anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to create Anki cards from the text I provide.

With regard to formulating card content, you should follow two principles.
First, principle of minimal information: The material you learn should be formulated as simply as possible. Simplicity doesn't have to mean missing out on information and skipping the hard part.
Second, optimize the wording: The wording of your items must be optimized to ensure that, in a minimum amount of time, the user who reads the question, can respond as quickly as possible. This will reduce error rates, increase specificity, reduce response time, and help your concentration.

You can not use the word from input in the output. It should be masked with underscores.

Create Anki cards based on the text above as follows:
"""

anki_examples = {"struggle": "Something that can only be accomplished with great effort is said to be a _______. "
                             "The verb form of _______ can be used for physical or mental effort. "
                             "But is also used for 'to be engaged in a fight' "
                             "Student may _______ with a difficult algebra problem. ",
                 "jot down": "To write quickly. "
                             "You might ___ ____ a friend's email address on the back of your grocery list. "
                             "It's a good word to use when you're writing a brief note, a phone number, or a list — especially when you're doing it in a hurry. ",
                 "attitude": "An _______ is somewhere between a belief, a stance, a mood, and a pose. "
                             "If you've got an _______ about something, it can be hard to change it because you think you're right. "
                             "A complex mental state involving beliefs and feelings and values and dispositions to act in certain ways."
                             "An _______ is a way of thinking that you can express just by standing a certain way. "
                             "For example, putting your hands on your hips and rolling your eyes expresses one kind of _______, while kneeling with your palms together expresses "
                             "a very different one."}

anki_examples_strings = [f"Word: {word}; Card Example: {anki_examples[word]};\n" for word in anki_examples.keys()]

anki_full_prompt = anki_prompt_preamble + ''.join(anki_examples_strings)

print(anki_full_prompt)

temperature: float = 0.2
presence_penalty: float = 0
frequency_penalty: float = 0.1
response_number = 1

# model: str = "gpt-3.5-turbo"
model: str = "gpt-4-turbo"

max_tokens: int = 256
n: int = 1


def chat_generate_text(input_word: str) -> list[str]:
    messages = [
        {"role": "system", "content": f"{anki_full_prompt}"},
        {"role": "user", "content": input_word},
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


print(chat_generate_text("pagan"))
