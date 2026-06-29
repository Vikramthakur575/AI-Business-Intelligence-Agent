import os
import streamlit as st

from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    # Streamlit Cloud
    API_KEY = st.secrets["GOOGLE_API_KEY"]

except Exception:
    # Local Development (.env)
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception(
        "GOOGLE_API_KEY not found in Streamlit Secrets or .env"
    )

client = genai.Client(
    api_key=API_KEY
)


def generate(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text