import pandas as pd

from database.postgres import engine
from utils.llm import generate
from sqlalchemy import text


def ask_database(question):

    schema = """
    Table: financials

    Columns:
    symbol
    fiscaldateending
    totalrevenue
    grossprofit
    operatingincome
    incomebeforetax
    ebit
    ebitda
    netincome
    """

    prompt = f"""
You are a PostgreSQL expert.

Convert the user's question into SQL.

Rules:
- Use table financials
- Return ONLY SQL
- No explanations
- Use lowercase column names
- LIMIT results to 50 rows unless specified
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER

Schema:

{schema}

Question:
{question}
"""

    sql = generate(prompt)

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    dangerous_words = [
        "drop",
        "delete",
        "update",
        "alter",
        "truncate",
        "insert"
    ]

    if any(word in sql.lower() for word in dangerous_words):
        raise Exception("Unsafe SQL detected")

    try:

        with engine.connect() as conn:

            df = pd.read_sql(
                text(sql),
                conn
            )

        return sql, df

    except Exception as e:

        raise Exception(
            f"SQL Error: {str(e)}"
        )