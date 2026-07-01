import pandas as pd

from utils.llm import generate
from utils.sql_validator import validate_sql
from utils.sql_executor import execute_sql
from agents.sql_fixer import fix_sql
from database.postgres import engine


# ==========================================
# Clean SQL
# ==========================================

def clean_sql(sql: str):

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .replace("SQL", "")
        .strip()
    )

    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    else:
        sql += ";"

    return sql


# ==========================================
# Uploaded Dataset Schema
# ==========================================

def get_uploaded_schema():

    sample = pd.read_sql(
        "SELECT * FROM uploaded_data LIMIT 5",
        engine
    )

    schema = []

    for col, dtype in zip(
        sample.columns,
        sample.dtypes
    ):

        schema.append(
            f"- {col} ({dtype})"
        )

    return "\n".join(schema)


# ==========================================
# Sample Data
# ==========================================

def get_uploaded_sample():

    sample = pd.read_sql(
        "SELECT * FROM uploaded_data LIMIT 5",
        engine
    )

    return sample.to_string(index=False)


# ==========================================
# Prompt Builder
# ==========================================

def build_prompt(question):

    schema = get_uploaded_schema()

    sample = get_uploaded_sample()

    prompt = f"""
You are an expert PostgreSQL Data Analyst.

Convert natural language into PostgreSQL SQL.

========================================
TABLE

uploaded_data

========================================
SCHEMA

{schema}

========================================
SAMPLE DATA

{sample}

========================================
RULES

1. Return ONLY SQL.

2. Never explain.

3. Never use markdown.

4. Never generate

DROP
DELETE
UPDATE
ALTER
INSERT
CREATE
TRUNCATE

5. Use ONLY table uploaded_data.

6. Use ONLY columns from schema.

7. Never invent columns.

8. Use lowercase column names.

9. LIMIT 50 unless user specifies another limit.

10. If user asks top/highest,
sort descending.

11. If user asks lowest,
sort ascending.

12. If user asks trend,
sort by date column if available.

13. Generate valid PostgreSQL only.

========================================
QUESTION

{question}

========================================
SQL
"""

    return prompt


# ==========================================
# Main Function
# ==========================================

def ask_uploaded_database(question):

    question = question.strip()

    prompt = build_prompt(question)

    last_error = ""

    for attempt in range(2):

        sql = generate(prompt)

        sql = clean_sql(sql)

        try:

            validate_sql(sql)

            success, df, error = execute_sql(sql)

            if success:
                return sql, df

            raise Exception(error)

        except Exception as e:

            last_error = str(e)

            if attempt == 0:

                try:

                    fixed_sql = fix_sql(
                        question,
                        sql,
                        last_error,
                        get_uploaded_schema()
                    )

                    fixed_sql = clean_sql(
                        fixed_sql
                    )

                    validate_sql(
                        fixed_sql
                    )

                    success, df, error = execute_sql(
                        fixed_sql
                    )

                    if success:
                        return fixed_sql, df

                    raise Exception(error)

                except Exception as retry_error:

                    last_error = str(
                        retry_error
                    )

            prompt += f"""

IMPORTANT

The previous SQL failed.

Database Error

{last_error}

Generate a completely NEW PostgreSQL query.

Return ONLY SQL.

"""

    raise Exception(
        f"Unable to generate valid SQL.\n\n{last_error}"
    )