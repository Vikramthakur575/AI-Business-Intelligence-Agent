from utils.llm import generate
from utils.schema import get_schema, get_sample_data
from utils.sql_examples import SQL_EXAMPLES
from utils.sql_validator import validate_sql
from utils.sql_executor import execute_sql
from utils.business_dictionary import BUSINESS_DICTIONARY
from agents.sql_fixer import fix_sql


def clean_sql(sql: str):
    """
    Cleans SQL returned by Gemini.
    """

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .replace("SQL", "")
        .replace("Sql", "")
        .replace("sql", "")
        .strip()
    )

    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    else:
        sql += ";"

    return sql


def build_prompt(question):

    schema = get_schema()

    sample_data = get_sample_data()

    prompt = f"""
You are an expert PostgreSQL Business Intelligence Analyst.

Your job is to convert natural language into PostgreSQL SQL.

====================================================
DATABASE
====================================================

Table Name

financials

====================================================
SCHEMA
====================================================

{schema}

====================================================
SAMPLE DATA
====================================================

{sample_data}

====================================================
BUSINESS VOCABULARY
====================================================

{BUSINESS_DICTIONARY}

====================================================
EXAMPLES
====================================================

{SQL_EXAMPLES}

====================================================
RULES
====================================================

You MUST follow every rule.

1. Return ONLY SQL.

2. Never explain anything.

3. Never use markdown.

4. Never wrap SQL inside ```sql.

5. Never generate

DROP
DELETE
UPDATE
ALTER
TRUNCATE
INSERT
CREATE
GRANT
REVOKE

6. Use ONLY table financials.

7. Use ONLY columns from the schema.

8. Never invent column names.

9. Use lowercase column names.

10. Use LIMIT 50 unless user specifies another limit.

11. "top", "highest", "largest", "best"

→ ORDER BY metric DESC

12. "lowest", "least", "smallest"

→ ORDER BY metric ASC

13. Revenue trend

→ ORDER BY fiscaldateending ASC

14. If user asks

sales

turnover

revenue

Use totalrevenue.

15. If user asks

profit

income

earnings

Use netincome unless another profit metric is specified.

16. Convert company names into stock symbols.

Apple → AAPL

Microsoft → MSFT

Nvidia → NVDA

Tesla → TSLA

AMD → AMD

Amazon → AMZN

Google → GOOGL

Meta → META

Intel → INTC

Netflix → NFLX

17. Never use SELECT * unless explicitly requested.

18. If question is ambiguous, make the best reasonable assumption.

19. Generate valid PostgreSQL only.

====================================================
QUESTION
====================================================

{question}

====================================================
SQL
====================================================
"""

    return prompt


def ask_database(question):

    question = question.strip()

    question = " ".join(question.split())

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
                        get_schema()
                    )

                    fixed_sql = clean_sql(fixed_sql)

                    validate_sql(fixed_sql)

                    success, df, error = execute_sql(
                        fixed_sql
                    )

                    if success:

                        return fixed_sql, df

                    raise Exception(error)

                except Exception as retry_error:

                    last_error = str(retry_error)

            prompt += f"""

IMPORTANT

The previous SQL failed.

Database Error

{last_error}

Generate a completely NEW PostgreSQL query.

Do NOT repeat the same mistake.

Return ONLY SQL.

"""

    raise Exception(
        f"Unable to generate valid SQL.\n\nDatabase Error:\n{last_error}"
    )