import pandas as pd

from database.postgres import engine


def load_uploaded_data(uploaded_file):

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(
            uploaded_file
        )

    else:

        df = pd.read_excel(
            uploaded_file
        )

    df.columns = [
        col.lower().replace(" ", "_")
        for col in df.columns
    ]

    df.to_sql(
        "uploaded_data",
        engine,
        if_exists="replace",
        index=False
    )

    return df