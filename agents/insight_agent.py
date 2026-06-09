def generate_insights(question, df):

    insights = []

    insights.append(
        f"Dataset contains {len(df)} records."
    )

    insights.append(
        f"Returned {len(df.columns)} columns."
    )

    if len(df.columns) >= 2:

        metric = df.columns[1]

        try:

            max_value = df[metric].max()
            min_value = df[metric].min()
            avg_value = df[metric].mean()

            insights.append(
                f"Highest {metric}: {max_value:,.0f}"
            )

            insights.append(
                f"Lowest {metric}: {min_value:,.0f}"
            )

            insights.append(
                f"Average {metric}: {avg_value:,.0f}"
            )

            if len(df) > 0:

                top_entity = df.iloc[0][df.columns[0]]

                insights.append(
                    f"Top performer: {top_entity}"
                )

        except Exception:
            pass

    return "\n\n".join(
        f"✅ {item}" for item in insights
    )