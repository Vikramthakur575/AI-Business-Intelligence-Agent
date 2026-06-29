FORBIDDEN = [
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "grant",
    "revoke"
]


def validate_sql(sql: str):

    sql_lower = sql.lower()

    for word in FORBIDDEN:

        if word in sql_lower:
            raise Exception(
                f"Forbidden SQL keyword detected: {word}"
            )

    return True