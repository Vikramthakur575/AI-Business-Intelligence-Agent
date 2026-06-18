import streamlit as st
import pandas as pd
from io import BytesIO
from utils.data_loader import load_uploaded_data
from agents.upload_agent import ask_uploaded_database
from agents.sql_agent import ask_database
from agents.insight_agent import generate_insights
from utils.charts import generate_chart
from utils.business_summary import generate_summary

st.set_page_config(
    page_title="AI Business Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

# =====================================
# Session State
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_history" not in st.session_state:
    st.session_state.query_history = []

# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.title("📈 AI BI Dashboard")

    st.markdown("---")

    st.subheader("Example Questions")

    st.markdown("""
- Top 10 companies by revenue
- Top 10 companies by net income
- Revenue for NVDA
- Top EBITDA companies
- Companies with highest gross profit
""")

    st.markdown("---")

    st.subheader("Recent Queries")

    if st.session_state.query_history:

        for q in reversed(st.session_state.query_history[-10:]):
            st.write(f"• {q}")

    else:
        st.caption("No queries yet")

    st.markdown("---")

    st.subheader("📊 Analytics")

    st.write(
        f"Total Queries: {len(st.session_state.query_history)}"
    )

    if st.session_state.query_history:

        st.write("Last Query:")

        st.caption(
            st.session_state.query_history[-1]
        )

    st.markdown("---")

    st.subheader("🗄 Database")

    st.write("Table: financials")
    st.write("Rows: 1750")
    st.write("Columns: 27")

# =====================================
# Main Header
# =====================================

st.title("📊 AI Business Intelligence Agent")

st.caption(
    "Ask business questions in natural language and get SQL, charts, and business insights."
)
st.markdown("---")

st.subheader("📂 Data Source")

data_source = st.radio(
    "Choose Dataset",
    [
        "Built-in Financial Dataset",
        "Upload My Dataset"
    ]
)

uploaded_file = None

if data_source == "Upload My Dataset":

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"]
    )
# =====================================
# Quick Questions
# =====================================

st.subheader("🚀 Quick Questions")

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "🏆 Top Revenue Companies",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "Top 10 companies by revenue"
        )

    if st.button(
        "💰 Revenue for NVDA",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "Revenue for NVDA"
        )

with c2:

    if st.button(
        "📈 Top Net Income",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "Top 10 companies by net income"
        )

    if st.button(
        "🚀 Top EBITDA",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "Top 10 companies by ebitda"
        )

st.markdown("---")

# =====================================
# Chat History
# =====================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================
# User Input
# =====================================

question = st.chat_input(
    "Ask a business question..."
)

if "quick_question" in st.session_state:

    question = st.session_state.quick_question

    del st.session_state.quick_question

# =====================================
# Query Execution
# =====================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.query_history.append(question)

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🧠 AI is analyzing data..."
            ):

                if data_source == "Built-in Financial Dataset":

                    sql, df = ask_database(question)

                else:

                    if uploaded_file is None:

                        st.warning(
                            "Please upload a CSV or Excel file."
                        )

                        st.stop()

                    load_uploaded_data(uploaded_file)

                    sql, df = ask_uploaded_database(
                        question
                    )

            if df is None or df.empty:

                st.warning(
                    "No data returned."
                )

                st.stop()

            st.success(
                "Analysis completed successfully."
            )

            # KPI Dashboard

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Rows",
                    len(df)
                )

            with c2:
                st.metric(
                    "Columns",
                    len(df.columns)
                )

            if len(numeric_cols) > 0:

                metric_col = numeric_cols[0]

                with c3:
                    st.metric(
                        "Maximum",
                        f"{df[metric_col].max():,.0f}"
                    )

                with c4:
                    st.metric(
                        "Average",
                        f"{df[metric_col].mean():,.0f}"
                    )

            # SQL

            st.subheader(
                "📝 Generated SQL"
            )

            st.code(
                sql,
                language="sql"
            )

            # Results

            st.subheader(
                "📋 Query Results"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # Executive Summary

            st.subheader(
                "📌 Executive Summary"
            )

            st.info(
                generate_summary(df)
            )

            # Visualization

            chart = generate_chart(df)

            if chart:

                st.subheader(
                    "📊 Visualization"
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )

            # Business Insights

            insights = generate_insights(
                question,
                df
            )

            st.subheader(
                "🧠 Business Insights"
            )

            st.markdown(
                insights
            )

            # Downloads

            st.subheader(
                "⬇ Export Results"
            )

            d1, d2 = st.columns(2)

            csv = df.to_csv(
                index=False
            )

            with d1:

                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name="results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            buffer = BytesIO()

            with pd.ExcelWriter(
                buffer,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Results"
                )

            with d2:

                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name="results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Analysis completed successfully."
                }
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

            st.stop()
            # =====================================
            # KPI Dashboard
            # =====================================

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Rows",
                    len(df)
                )

            with c2:
                st.metric(
                    "Columns",
                    len(df.columns)
                )

            if len(numeric_cols) > 0:

                metric_col = numeric_cols[0]

                with c3:
                    st.metric(
                        "Maximum",
                        f"{df[metric_col].max():,.0f}"
                    )

                with c4:
                    st.metric(
                        "Average",
                        f"{df[metric_col].mean():,.0f}"
                    )

            # =====================================
            # SQL
            # =====================================

            st.subheader(
                "📝 Generated SQL"
            )

            st.code(
                sql,
                language="sql"
            )

            # =====================================
            # Results
            # =====================================

            st.subheader(
                "📋 Query Results"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # =====================================
            # Executive Summary
            # =====================================

            st.subheader(
                "📌 Executive Summary"
            )

            st.info(
                generate_summary(df)
            )

            # =====================================
            # Visualization
            # =====================================

            chart = generate_chart(df)

            if chart:

                st.subheader(
                    "📊 Visualization"
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )

            # =====================================
            # Business Insights
            # =====================================

            insights = generate_insights(
                question,
                df
            )

            st.subheader(
                "🧠 Business Insights"
            )

            st.markdown(
                insights
            )

            # =====================================
            # Downloads
            # =====================================

            st.subheader(
                "⬇ Export Results"
            )

            d1, d2 = st.columns(2)

            csv = df.to_csv(
                index=False
            )

            with d1:

                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name="results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            buffer = BytesIO()

            with pd.ExcelWriter(
                buffer,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Results"
                )

            with d2:

                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name="results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Analysis completed successfully."
                }
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )