"""
AI Chat With Your Data — Real LLM Version (Google Gemini, FREE forever)
--------------------------------------------------------------------------
Ask plain-English questions about netflix_titles.csv. A REAL LLM (Google
Gemini) converts your question into one line of Pandas code, and THIS
SCRIPT runs that code against your real data.

This is the genuine "AI" version of the project -- Gemini's free API tier
has no credit card requirement and does not expire, unlike OpenAI/Anthropic
which require billing to be set up.

Setup:
    pip install pandas google-genai

    Get a free API key (no card needed):
    1. Go to https://aistudio.google.com/apikey
    2. Sign in with any Google account
    3. Click "Create API Key"
    4. Copy it

    Then set it as an environment variable:
        Windows PowerShell:  $env:GEMINI_API_KEY="your-key-here"
        Mac/Linux:           export GEMINI_API_KEY="your-key-here"

Run:
    python chat_with_data_gemini.py
"""

import os
import pandas as pd
from google import genai

# ---- 1. Load your dataset ----
df = pd.read_csv("netflix_titles.csv")

# ---- 2. Set up the AI client ----
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def ask(question: str):
    """
    Sends the dataset's structure + the user's question to Gemini.
    Gemini returns ONE line of Pandas code (not an answer).
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

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    code = response.text.strip().replace("```python", "").replace("```", "").strip()
    print(f"\n[Generated code]: {code}")

    # ---- 3. Run the AI-generated code against the REAL data ----
    try:
        result = eval(code)
    except Exception as e:
        return f"Could not run the generated code: {e}"

    return result


if __name__ == "__main__":
    print("Ask questions about netflix_titles.csv (type 'quit' to exit)\n")
    print("This version uses a REAL LLM (Google Gemini) -- ask ANY question,")
    print("not just pre-programmed ones:\n")
    print(" - How many Movies vs TV Shows are there?")
    print(" - What percentage of titles are rated TV-MA?")
    print(" - Which year had the most releases?")
    print(" - Show me the 5 oldest titles by release year\n")

    while True:
        question = input("Your question: ")
        if question.lower() in ("quit", "exit"):
            break
        answer = ask(question)
        print(f"\nAnswer:\n{answer}\n")
