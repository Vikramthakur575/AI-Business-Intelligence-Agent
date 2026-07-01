from utils.llm import generate


def fix_sql(
    question,
    sql,
    error,
    schema
):

    prompt = f"""
You are an expert PostgreSQL developer.

The following SQL generated an error.

Question:
{question}

Database Schema:

{schema}

Generated SQL:

{sql}

Database Error:

{error}

Fix ONLY the SQL.

Return ONLY SQL.

No explanation.
"""

    fixed_sql = generate(prompt)

    fixed_sql = (
        fixed_sql
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return fixed_sql