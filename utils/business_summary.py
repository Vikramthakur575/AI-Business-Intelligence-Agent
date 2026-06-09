def generate_summary(df):

    if len(df) == 0:
        return "No data available."

    first_col = df.columns[0]

    return f"""
Business Summary

• Records analyzed: {len(df)}

• Columns returned: {len(df.columns)}

• Top result: {df.iloc[0][first_col]}

• Data successfully retrieved from PostgreSQL.
"""