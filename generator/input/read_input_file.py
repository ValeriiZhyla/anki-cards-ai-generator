import logging
import os

import pandas as pd

from generator.entities import WordWithContext


def read_csv_file(file_path: str) -> list[WordWithContext]:
    words_with_context = []
    df = pd.read_csv(file_path, delimiter=";")
    for index, row in df.iterrows():
        if not row['Word'] or row['Word'].strip() == "":
            continue
        word = row['Word'].strip()
        context = row['Context'].strip() if 'Context' in row and not pd.isna(row['Context']) else ""
        words_with_context.append(WordWithContext(word, context))
    return words_with_context


def read_excel_file(file_path: str) -> list[WordWithContext]:
    words_with_context = []
    df = pd.read_excel(file_path, engine='openpyxl')
    for index, row in df.iterrows():
        if not row['Word'] or row['Word'].strip() == "":
            continue
        word = row['Word'].strip()
        context = row['Context'].strip() if 'Context' in row and not pd.isna(row['Context']) else ""
        words_with_context.append(WordWithContext(word, context))
    return words_with_context

def read_file_based_on_extension(file_path: str) -> list[WordWithContext]:
    # Check if file exists before proceeding
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file found at the specified path: {file_path}")

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() in ['.csv']:
        logging.info("Reading CSV file")
        return read_csv_file(file_path)
    elif file_extension.lower() in ['.xls', '.xlsx']:
        logging.info("Reading Excel file")
        return read_excel_file(file_path)
    else:
        raise ValueError("Unsupported file format")
