import pandas as pd

from sqlalchemy import text

from database.postgres import engine
from utils.llm import generate
from utils.schema import (
    get_schema,
    get_sample_data
)
from utils.sql_examples import SQL_EXAMPLES
from utils.sql_validator import validate_sql


def clean_sql(sql: str):

    """
    Removes markdown formatting if Gemini returns it.
    """

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return sql


def build_prompt(question):

    schema = get_schema()

    sample_data = get_sample_data()

    prompt = f"""
You are an expert PostgreSQL Data Analyst.

Your job is to convert natural language questions into PostgreSQL SQL queries.

======================================================
DATABASE INFORMATION
======================================================

Table Name:

financials

======================================================
SCHEMA
======================================================

{schema}

======================================================
SAMPLE DATA
======================================================

{sample_data}

======================================================
EXAMPLES
======================================================

{SQL_EXAMPLES}

======================================================
IMPORTANT RULES
======================================================

1. Return ONLY SQL.

2. Never explain anything.

3. Never use markdown.

4. Never use ```sql.

5. Never generate:

DROP
DELETE
INSERT
UPDATE
ALTER
TRUNCATE
GRANT
REVOKE

6. Use ONLY table financials.

7. Use lowercase column names.

8. LIMIT 50 rows unless user specifies another limit.

9. If user asks Top Companies,
sort in descending order.

10. If user asks Revenue Trend,
sort by fiscaldateending.

11. Always generate valid PostgreSQL SQL.

======================================================
USER QUESTION
======================================================

{question}

======================================================
SQL
======================================================
"""

    return prompt


def execute_sql(sql):

    validate_sql(sql)

    with engine.connect() as conn:

        df = pd.read_sql(
            text(sql),
            conn
        )

    return df


def ask_database(question):

    prompt = build_prompt(question)

    last_error = ""

    for attempt in range(2):

        sql = generate(prompt)

        sql = clean_sql(sql)

        try:

            df = execute_sql(sql)

            return sql, df

        except Exception as e:

            last_error = str(e)

            prompt += f"""

The previous SQL produced this PostgreSQL error:

{last_error}

Please fix the SQL.

Return ONLY corrected SQL.
"""

    raise Exception(
        f"""
Unable to generate valid SQL.

Last database error:

{last_error}
"""
    )