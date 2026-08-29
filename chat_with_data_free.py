"""
AI Chat With Your Data (Free / No API Key Version)
----------------------------------------------------
Ask plain-English questions about netflix_titles.csv and get real answers.

This version works completely FREE, with no API key, no billing, and no
internet connection required. Instead of sending your question to a paid
LLM (like Claude or GPT), this script uses simple keyword matching to
recognize common question patterns and convert them into Pandas code.

This still demonstrates the CORE CONCEPT of the project:
    English question --> Pandas code --> real answer from real data

For your portfolio, you can describe this as: "Built a rule-based natural
language query layer over a Pandas dataset, with an optional upgrade path
to a full LLM (Claude/GPT) for more complex questions."

Run:
    python chat_with_data.py
"""

import pandas as pd

# ---- 1. Load your dataset ----
df = pd.read_csv("netflix_titles.csv")


def ask(question: str):
    """
    Looks for keywords in the question and matches it to a pre-built
    Pandas query. This is a simplified stand-in for what an LLM would do:
    turn an English question into runnable Pandas code.
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
        return (
            "Sorry, I don't recognize that question pattern yet.\n"
            "Try one of the example questions shown above, or add a new "
            "rule to the ask() function to handle it."
        )

    print(f"\n[Generated code]: {code}")

    # ---- 2. Run the matched code against the REAL data ----
    try:
        result = eval(code)
    except Exception as e:
        return f"Could not run the generated code: {e}"

    return result


if __name__ == "__main__":
    print("Ask questions about netflix_titles.csv (type 'quit' to exit)\n")
    print("Try things like:")
    print(" - How many Movies vs TV Shows are there?")
    print(" - Which country has the most titles?")
    print(" - What is the most common rating?")
    print(" - How many titles were released in 2018?")
    print(" - Which director appears most often?")
    print(" - What are the most common genres?\n")

    while True:
        question = input("Your question: ")
        if question.lower() in ("quit", "exit"):
            break
        answer = ask(question)
        print(f"\nAnswer:\n{answer}\n")
