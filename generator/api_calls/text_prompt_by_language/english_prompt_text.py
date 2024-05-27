from generator.config import Config

anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to create Anki cards from the text I provide.

With regard to formulating card content, you should follow two principles.
1. Minimal Information: The learning material should be simple yet comprehensive, without skipping complex details.
2. Optimized Wording: Ensure the card's wording allows quick understanding and response, aiming to reduce error rates and increase focus.


Context Handling:
- Provide cards with or without context:
  - No Context: If no context is given, use or create suitable contexts.
  - With Context: Use the provided context. If the context distorts the word's conventional usage, it should be disregarded.
- Do not mix context fields in the card and ensure the context is meaningful for the card content.

Input Format:
- I can provide a word or a phrase with empty context: 
  - WORD: [target word]; CONTEXT: []
- Alternatively, I can provide a word or a phrase with a context:
  - WORD: [target word]; CONTEXT: [context]

Output Expectations:
- Exclude unrelated sentences, as the "Card Example". 
- You can not use the word from input in the output. All letters should be masked with underscores.
- Each card should contain 4-5 sentences focused solely on explaining the masked word or phrase.
- Your output should contain only the text for the card.

Masking Rules:
- Mask the target word with underscores, preserving spaces between words ("free will" becomes "____ ____").
- Number of underscores should match the number of the letters ("salvation" becomes "_________")
- Only mask the target word, not its contextual usage. For instance, "seizure" in "ship seizure" should only mask "seizure."


"""


def examples() -> str:
    examples_preamble = """
    Here are some examples, in format 
    WORD: [target word]; CONTEXT: [optional context]; RESULT: [what I expect to get as output]
    """

    anki_examples = {"struggle": ["", "Something that can only be accomplished with great effort is said to be a ________. "
                                      "The verb form of ________ can be used for physical or mental effort. "
                                      "But is also used for 'to be engaged in a fight' "
                                      "Student may ________ with a difficult algebra problem. "],
                     "jot down": ["", "To write quickly. "
                                      "You might ___ ____ a friend's email address on the back of your grocery list. "
                                      "It's a good word to use when you're writing a brief note, a phone number, or a list — especially when you're doing it in a hurry. "],
                     "attitude": ["", "An ________ is somewhere between a belief, a stance, a mood, and a pose. "
                                      "If you've got an ________ about something, it can be hard to change it because you think you're right. "
                                      "A complex mental state involving beliefs and feelings and values and dispositions to act in certain ways."
                                      "An ________ is a way of thinking that you can express just by standing a certain way. "
                                      "For example, putting your hands on your hips and rolling your eyes expresses one kind of ________, while kneeling with your palms together expresses "
                                      "a very different one."],
                     "free will": ["", "Something that allows individuals to make choices independently is known as ____ ___. "
                                       "Philosophers often debate whether ____ ___ truly exists or if our decisions are predetermined. "
                                       "The concept of ____ ___ is central to discussions about moral responsibility."
                                       "In religious contexts, ____ ___ is often linked to the ability to choose between good and evil."],
                     "seizure": ["ship seizure", "Something that involves taking control of a ship by force is known as a ship ______."
                                                 "In legal contexts, a ship ______ can occur due to violations of maritime law."
                                                 "Pirates are historically known for committing ship ______."
                                                 "Authorities may conduct a ship ______ to prevent illegal activities like smuggling."]
                     }

    anki_examples_strings = [f"WORD: [{word}]; CONTEXT: [{anki_examples[word][0]}]; RESULT:[{anki_examples[word][1]}]\n" for word in anki_examples.keys()]
    return examples_preamble + ''.join(anki_examples_strings)


def rule_language_level() -> str:
    return f"""
    Language Level:
    - A person with the language level [{Config.LEVEL}] should understand the card.
    - Words and constructions that should be familiar to a person at this level.
    - If the language level is set to C1 or C2, use words and constructions of your choice.
    """


def get_prompt() -> str:
    return anki_prompt_preamble + rule_language_level() + examples()
