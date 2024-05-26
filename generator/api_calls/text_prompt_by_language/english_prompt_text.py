anki_prompt_preamble = """I want you to act like a professional Anki card maker, able to create Anki cards from the text I provide.

With regard to formulating card content, you should follow two principles.
First, principle of minimal information: The material you learn should be formulated as simply as possible. Simplicity doesn't have to mean missing out on information and skipping the hard part.
Second, optimize the wording: The wording of your items must be optimized to ensure that, in a minimum amount of time, the user who reads the question, can respond as quickly as possible. This will reduce error rates, increase specificity, reduce response time, and help your concentration.

You can not use the word from input in the output. All letters should be masked with underscores.
If the input contains several words, the letters should be masked with underscores, and spaces remain spaces.
For example, "free will" should be masked as "____ ___", and "attitude" should be masked as "________".

I can provide a word or a phrase with empty context
WORD: [target word]; CONTEXT: []
In this case, use most likely context or different contexts of your choice.

Alternatively, I can provide a word or a phrase with a context:
WORD: [target word]; CONTEXT: [context]
In this case, use the given context for card generation.
Context can be a sentence with this word, but it can also be a single or several fields related to this word. 
You should not mix the fields in the card, and use the context only if it is meaningful for the card.
It the context of combinations of contexts violated from conventional word usage, ignore this context.
If there are several important contexts, write the main context first. 

Do not put any unrelated sentences in the card, as the "Card Example". Your output should contain only the text for the card.

I expect 4-5 sentences in every card.

Create Anki cards based on the text above as follows:
"""

anki_examples = {"struggle": "Something that can only be accomplished with great effort is said to be a ________. "
                             "The verb form of ________ can be used for physical or mental effort. "
                             "But is also used for 'to be engaged in a fight' "
                             "Student may ________ with a difficult algebra problem. ",
                 "jot down": "To write quickly. "
                             "You might ___ ____ a friend's email address on the back of your grocery list. "
                             "It's a good word to use when you're writing a brief note, a phone number, or a list — especially when you're doing it in a hurry. ",
                 "attitude": "An ________ is somewhere between a belief, a stance, a mood, and a pose. "
                             "If you've got an ________ about something, it can be hard to change it because you think you're right. "
                             "A complex mental state involving beliefs and feelings and values and dispositions to act in certain ways."
                             "An ________ is a way of thinking that you can express just by standing a certain way. "
                             "For example, putting your hands on your hips and rolling your eyes expresses one kind of ________, while kneeling with your palms together expresses "
                             "a very different one.",
                 "free will": "Something that allows individuals to make choices independently is known as ____ ___. "
                              "Philosophers often debate whether ____ ___ truly exists or if our decisions are predetermined. "
                              "The concept of ____ ___ is central to discussions about moral responsibility."
                              "In religious contexts, ____ ___ is often linked to the ability to choose between good and evil."
                 }

anki_examples_strings = [f"Word: {word}; Card Example: {anki_examples[word]};\n" for word in anki_examples.keys()]

anki_full_prompt = anki_prompt_preamble + ''.join(anki_examples_strings)


def get_prompt():
    return anki_full_prompt
