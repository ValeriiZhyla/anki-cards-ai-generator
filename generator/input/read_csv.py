import csv

from ..entities import WordWithContext


def read_words_with_context(filename):
    words_with_context = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            if row[0].strip().lower() == "word" and row[1].strip().lower() == "context":
                continue  # Skip header
            if not row or row[0].strip() == "":
                continue  # Skip rows where the word column is empty
            word = row[0].strip()
            context = row[1].strip() if len(row) > 1 else ""  # Handle missing or empty context
            try:
                word_with_context = WordWithContext(word, context)
                words_with_context.append(word_with_context)
            except ValueError as e:
                print(f"Error: {e} (word: '{word}', context: '{context}')")
                continue  # Optionally handle or log error, and skip to the next row

    return words_with_context
