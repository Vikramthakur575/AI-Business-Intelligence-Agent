from utils.llm import generate


def generate_followups(question, df):

    columns = ", ".join(df.columns.tolist())

    prompt = f"""
You are a Business Intelligence Assistant.

The user asked:

{question}

The result contains these columns:

{columns}

Suggest exactly 4 useful follow-up business questions.

Rules:

- One question per line
- No numbering
- No bullets
- Maximum 12 words each
"""

    response = generate(prompt)

    questions = []

    for line in response.split("\n"):

        line = line.strip()

        if line:
            questions.append(line)

    return questions[:4]