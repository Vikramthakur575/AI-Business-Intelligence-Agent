import pandas as pd
from sqlalchemy import text

from database.postgres import engine


def execute_sql(sql):

    try:

        with engine.connect() as conn:

            df = pd.read_sql(
                text(sql),
                conn
            )

        return True, df, None

    except Exception as e:

        return False, None, str(e)