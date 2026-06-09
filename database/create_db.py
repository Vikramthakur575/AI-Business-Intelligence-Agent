import pandas as pd
from postgres import engine

df = pd.read_csv("data/corporate_income_statement.csv")

df.columns = [col.lower() for col in df.columns]

df.to_sql(
    "financials",
    engine,
    if_exists="replace",
    index=False
)

print("Database Created Successfully")