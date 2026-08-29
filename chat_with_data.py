"""
AI Chat With Your Data
------------------------
Ask plain-English questions about a CSV file. An LLM converts your
question into one line of Pandas code, and THIS SCRIPT runs that
code against your real data (the AI never does the math itself).

Setup:
    pip install pandas anthropic

    Get a free API key from https://console.anthropic.com
    Then set it as an environment variable:
        Mac/Linux:  export ANTHROPIC_API_KEY="your-key-here"
        Windows:    set ANTHROPIC_API_KEY=your-key-here

Run:
    python chat_with_data.py
"""

import os
import pandas as pd
from anthropic import Anthropic

# ---- 1. Load your dataset ----
df = pd.read_csv("netflix_titles.csv")

# ---- 2. Set up the AI client ----
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def ask(question: str):
    """
    Sends the dataset's structure + the user's question to the LLM.
    The LLM returns ONE line of Pandas code (not an answer).
    We then run that code ourselves against the real dataframe.
    """
    schema_and_sample = f"""Columns: {list(df.columns)}
Sample rows: {df.head(3).to_dict(orient='records')}"""

    prompt = f"""{schema_and_sample}

Write ONE line of pandas code (the dataframe variable is named 'df')
that answers this question: "{question}"

Rules:
- Return ONLY the code, nothing else.
- No explanations, no markdown formatting, no backticks.
- The code must be a single expression that returns a value.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    code = response.content[0].text.strip()
    print(f"\n[Generated code]: {code}")

    # ---- 3. Run the AI-generated code against the REAL data ----
    try:
        result = eval(code)  # NOTE: see "Security" section in README
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
    print(" - Which director appears most often?\n")

    while True:
        question = input("Your question: ")
        if question.lower() in ("quit", "exit"):
            break
        answer = ask(question)
        print(f"\nAnswer:\n{answer}\n")
