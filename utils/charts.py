import plotly.express as px
import pandas as pd


def generate_chart(df):

    if len(df.columns) < 2:
        return None

    try:

        x_col = df.columns[0]
        y_col = df.columns[1]

        numeric_cols = df.select_dtypes(include="number").columns

        # Trend Chart
        if "date" in x_col.lower():

            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                markers=True,
                title=f"{y_col} Trend"
            )

            return fig

        # Scatter Plot
        if len(numeric_cols) >= 2:

            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title="Correlation Analysis"
            )

            return fig

        # Pie Chart
        if len(df) <= 10:

            fig = px.pie(
                df,
                names=x_col,
                values=y_col,
                title=f"{y_col} Distribution"
            )

            return fig

        # Default Bar Chart
        fig = px.bar(
            df.head(20),
            x=x_col,
            y=y_col,
            title=f"{y_col} by {x_col}"
        )

        fig.update_layout(
            height=550
        )

        return fig

    except Exception:
        return None