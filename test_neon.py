from database.postgres import engine
import pandas as pd

query = "SELECT version();"

df = pd.read_sql(query, engine)

print(df)