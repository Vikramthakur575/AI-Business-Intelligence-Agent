import pandas as pd
from sqlalchemy import text

from database.postgres import engine


def get_schema():

    """
    Reads database schema dynamically.
    """

    query = """
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_name='financials'
    ORDER BY ordinal_position;
    """

    with engine.connect() as conn:

        schema_df = pd.read_sql(
            text(query),
            conn
        )

    schema = ""

    for _, row in schema_df.iterrows():

        schema += (
            f"- {row['column_name']} "
            f"({row['data_type']})\n"
        )

    return schema


def get_sample_data():

    """
    Gives Gemini sample rows.
    """

    query = """
    SELECT *
    FROM financials
    LIMIT 5;
    """

    with engine.connect() as conn:

        df = pd.read_sql(
            text(query),
            conn
        )

    return df.to_string(index=False)