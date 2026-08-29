"""
AI Chat With Your Data — Streamlit Dashboard Version
------------------------------------------------------
A web-based UI for asking plain-English questions about netflix_titles.csv.

This turns the terminal script into an actual visual dashboard you can
screen-record or share as a live demo link.

Setup:
    pip install pandas streamlit

Run:
    streamlit run dashboard.py

This will open a browser window automatically at http://localhost:8501
"""

import pandas as pd
import streamlit as st

# ---- Page setup ----
st.set_page_config(page_title="Netflix Data Chat Assistant", page_icon="🎬", layout="centered")

# ---- Load dataset (cached so it doesn't reload on every question) ----
@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()


def ask(question: str):
    """
    Matches the question to a pre-built Pandas query based on keywords,
    then runs that query against the real dataset.
    """
    q = question.lower()

    if "movies vs" in q or ("movie" in q and "tv show" in q and "how many" in q):
        code = 'df["type"].value_counts()'

    elif "country" in q and ("most" in q or "top" in q):
        code = 'df["country"].value_counts().head(5)'

    elif "rating" in q and "common" in q:
        code = 'df["rating"].value_counts().head(1)'

    elif "released" in q and any(char.isdigit() for char in q):
        year = "".join(filter(str.isdigit, q))[:4]
        code = f'df[df["release_year"] == {year}].shape[0]'

    elif "director" in q and ("most" in q or "appears" in q):
        code = 'df["director"].value_counts().head(5)'

    elif "genre" in q or "listed_in" in q or "category" in q:
        code = 'df["listed_in"].value_counts().head(5)'

    elif "how many" in q and "movie" in q:
        code = 'df[df["type"] == "Movie"].shape[0]'

    elif "how many" in q and "tv show" in q:
        code = 'df[df["type"] == "TV Show"].shape[0]'

    else:
        return None, "Sorry, I don't recognize that question pattern yet. Try one of the examples below."

    try:
        result = eval(code)
    except Exception as e:
        return code, f"Could not run the generated code: {e}"

    return code, result


# ---- UI ----
st.title("🎬 Netflix Data Chat Assistant")
st.caption("Ask a plain-English question about Netflix titles — no SQL or Pandas needed.")

with st.expander("📊 Preview the dataset"):
    st.write(f"**{len(df):,} titles** loaded — {df['type'].value_counts().get('Movie', 0):,} Movies, "
             f"{df['type'].value_counts().get('TV Show', 0):,} TV Shows")
    st.dataframe(df.head(10))

st.subheader("Ask a question")

example_questions = [
    "How many Movies vs TV Shows are there?",
    "Which country has the most titles?",
    "What is the most common rating?",
    "How many titles were released in 2018?",
    "Which director appears most often?",
    "What are the most common genres?",
]

selected_example = st.selectbox(
    "Try an example, or type your own below:",
    ["-- Type your own question --"] + example_questions,
)

if selected_example != "-- Type your own question --":
    question = st.text_input("Your question:", value=selected_example)
else:
    question = st.text_input("Your question:", placeholder="e.g. Which country has the most titles?")

if st.button("Get Answer") and question:
    code, answer = ask(question)

    if code:
        st.code(code, language="python")

    st.subheader("Answer")
    st.write(answer)

st.divider()
st.caption(
    "⚙️ How it works: your question is matched to a pre-built Pandas query "
    "using keyword rules, which is then run against the real dataset above. "
    "This is a rule-based version — a planned upgrade uses an LLM (Claude/GPT) "
    "to handle open-ended questions instead of fixed keyword rules."
)
