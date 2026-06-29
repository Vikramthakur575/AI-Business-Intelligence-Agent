import pandas as pd
import plotly.express as px


# ==========================================
# Detect column types
# ==========================================

def detect_columns(df):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = []

    date_cols = []

    for col in df.columns:

        if col in numeric_cols:
            continue

        try:
            pd.to_datetime(df[col])
            date_cols.append(col)

        except Exception:
            categorical_cols.append(col)

    return numeric_cols, categorical_cols, date_cols


# ==========================================
# Auto Chart Recommendation
# ==========================================

def recommend_chart(df):

    numeric, categorical, dates = detect_columns(df)

    if len(dates) >= 1 and len(numeric) >= 1:
        return "Line"

    if len(categorical) >= 1 and len(numeric) >= 1:
        return "Bar"

    if len(numeric) >= 2:
        return "Scatter"

    if len(numeric) == 1:
        return "Histogram"

    return None


# ==========================================
# Generate Chart
# ==========================================

def generate_chart(df, chart_type="Auto"):

    if df.empty:
        return None

    numeric, categorical, dates = detect_columns(df)

    if chart_type == "Auto":
        chart_type = recommend_chart(df)

    if chart_type is None:
        return None

    try:

        # ---------------- BAR ----------------

        if chart_type == "Bar":

            x = categorical[0] if categorical else df.columns[0]
            y = numeric[0]

            fig = px.bar(
                df.head(20),
                x=x,
                y=y,
                text_auto=".2s",
                template="plotly_white"
            )

        # ---------------- LINE ----------------

        elif chart_type == "Line":

            x = dates[0]
            y = numeric[0]

            temp = df.copy()

            temp[x] = pd.to_datetime(temp[x])

            fig = px.line(
                temp.sort_values(x),
                x=x,
                y=y,
                markers=True,
                template="plotly_white"
            )

        # ---------------- SCATTER ----------------

        elif chart_type == "Scatter":

            fig = px.scatter(
                df,
                x=numeric[0],
                y=numeric[1],
                template="plotly_white"
            )

        # ---------------- PIE ----------------

        elif chart_type == "Pie":

            if len(categorical) == 0:
                return None

            fig = px.pie(
                df.head(15),
                names=categorical[0],
                values=numeric[0],
                hole=0.45
            )

        # ---------------- HISTOGRAM ----------------

        elif chart_type == "Histogram":

            fig = px.histogram(
                df,
                x=numeric[0],
                nbins=25,
                template="plotly_white"
            )

        # ---------------- BOX ----------------

        elif chart_type == "Box":

            fig = px.box(
                df,
                y=numeric[0],
                template="plotly_white"
            )

        else:
            return None

        fig.update_layout(

            height=550,

            title=dict(
                text=f"{chart_type} Chart",
                x=0.5
            ),

            hovermode="closest",

            margin=dict(
                l=30,
                r=30,
                t=60,
                b=30
            )
        )

        return fig

    except Exception:

        return None