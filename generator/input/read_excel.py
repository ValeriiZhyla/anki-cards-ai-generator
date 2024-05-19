import pandas as pd


def read_words_with_context_from_excel(filename):
    words_with_context = []
    # Load the Excel file
    df = pd.read_excel(filename, engine='openpyxl')  # Ensure you use the correct engine for file type

    # Iterate through DataFrame rows
    for index, row in df.iterrows():
        # Assuming your columns are named 'Word' and 'Context'
        if pd.isna(row['Word']):
            continue  # Skip rows where the word column is empty
        word = str(row['Word']).strip()
        context = str(row['Context']).strip() if not pd.isna(row['Context']) else ""  # Handle missing or empty context

        try:
            word_with_context = WordWithContext(word, context)
            words_with_context.append(word_with_context)
        except ValueError as e:
            print(f"Error: {e} (word: '{word}', context: '{context}')")
            continue  # Optionally handle or log error, and skip to the next row

    return words_with_context