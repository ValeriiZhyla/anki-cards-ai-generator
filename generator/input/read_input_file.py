import logging
import os

import pandas as pd

from generator.entities import WordWithContext


def normalize_columns(df):
    """Normalize all column names to lowercase."""
    df.columns = [col.lower() for col in df.columns]
    return df


def check_columns(df):
    required_columns = {'word', 'context'}
    if not required_columns.issubset(df.columns):
        missing_cols = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    logging.info("All required columns are present")


def read_from_dataframe(df) -> list[WordWithContext]:
    words_with_context = []
    df = normalize_columns(df)
    check_columns(df)
    for index, row in df.iterrows():
        if not row['word'] or row['word'].strip() == "":
            continue
        word = row['word'].strip()
        context = row['context'].strip() if 'context' in row and not pd.isna(row['context']) else ""
        words_with_context.append(WordWithContext(word, context))
    return words_with_context


def read_csv_file(file_path: str) -> list[WordWithContext]:
    df = pd.read_csv(file_path, delimiter=";")
    return read_from_dataframe(df)


def read_excel_file(file_path: str) -> list[WordWithContext]:
    df = pd.read_excel(file_path, engine='openpyxl')
    return read_from_dataframe(df)


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
