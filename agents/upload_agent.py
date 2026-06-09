import pandas as pd

from database.postgres import engine
from utils.llm import generate


def ask_uploaded_database(question):

    sample = pd.read_sql(
        "SELECT * FROM uploaded_data LIMIT 5",
        engine
    )

    columns = sample.columns.tolist()

    schema = "\n".join(columns)

    prompt = f"""
You are a PostgreSQL expert.

Convert the user's question into SQL.

Rules:

- Use table uploaded_data
- Return ONLY SQL
- Use lowercase column names
- Limit results to 50 rows
- Never generate INSERT UPDATE DELETE DROP ALTER

Columns:

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

    df = pd.read_sql(
        sql,
        engine
    )

    return sql, df