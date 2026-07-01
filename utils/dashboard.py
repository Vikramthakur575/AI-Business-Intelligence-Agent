import pandas as pd
import streamlit as st


def show_kpis(df):

    numeric = df.select_dtypes(include="number")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📄 Rows",
            len(df)
        )

    with c2:

        st.metric(
            "📑 Columns",
            len(df.columns)
        )

    if len(numeric.columns):

        col = numeric.columns[0]

        with c3:

            st.metric(
                f"📈 Max {col}",
                f"{numeric[col].max():,.2f}"
            )

        with c4:

            st.metric(
                f"📊 Avg {col}",
                f"{numeric[col].mean():,.2f}"
            )

    c5, c6, c7 = st.columns(3)

    if len(numeric.columns):

        with c5:

            st.metric(
                "📉 Minimum",
                f"{numeric[col].min():,.2f}"
            )

        with c6:

            st.metric(
                "📌 Median",
                f"{numeric[col].median():,.2f}"
            )

        with c7:

            st.metric(
                "📏 Std Dev",
                f"{numeric[col].std():,.2f}"
            )