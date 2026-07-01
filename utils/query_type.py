def detect_query(question):

    q = question.lower()

    if "trend" in q:
        return "trend"

    if "compare" in q:
        return "comparison"

    if "distribution" in q:
        return "distribution"

    if "relationship" in q:
        return "correlation"

    if "top" in q:
        return "ranking"

    return "general"