# Netflix Data Chat Assistant

Ask plain-English questions about a real Netflix dataset and get instant,
accurate answers — powered by a real LLM (Google Gemini) that converts
natural language into Pandas code on the fly.

## Problem

Non-technical people can't write Pandas or SQL queries to explore a
dataset. This project lets anyone ask an open-ended question in plain
English (e.g. *"What percentage of titles are rated TV-MA?"*) and get a
real, computed answer back — no code required from the user, and no
limit to pre-defined question types.

## Approach

1. The user types any question in plain English.
2. The question, along with the dataset's column names and a few sample
   rows, is sent to Google's Gemini API.
3. Gemini returns ONE line of Pandas code that would answer the
   question — it does not calculate the answer itself.
4. That generated code is executed against the real dataset (6,234 real
   Netflix titles) using Pandas, and the actual computed result is
   returned to the user.
5. Two interfaces are provided:
   - `chat_with_data_gemini.py` — command-line version with real LLM
   - `dashboard.py` — Streamlit web dashboard version with a UI
   - `chat_with_data_free.py` — an earlier rule-based (no-API) fallback
     version, kept to show the evolution of the approach

## Why an LLM (and not just keyword rules)

An earlier version of this tool used keyword/rule-based matching, which
only worked for a fixed set of pre-programmed question types. Switching
to a real LLM (Gemini) means the tool can handle genuinely open-ended
questions it was never explicitly coded for — e.g. "How many titles have
'Love' in the title?" or "Which director has directed the most movies?" —
by generating the correct Pandas code dynamically.

## Tech Stack

- Python
- Pandas (data loading and querying)
- Google Gemini API (`google-genai`) — free tier, no credit card required
- Streamlit (web dashboard UI)

## Dataset

`netflix_titles.csv` — 6,234 real Netflix titles (Movies & TV Shows) as of
2019, with columns: type, title, director, cast, country, date_added,
release_year, rating, duration, listed_in, description.
(Original source: Shivam Bansal, Kaggle — CC0 Public Domain)

## How To Run It

### Command-line version (real LLM)
```bash
pip install pandas google-genai
```
Get a free API key (no card needed) at https://aistudio.google.com/apikey,
then set it as an environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-key-here"
```
Run:
```bash
python chat_with_data_gemini.py
```

### Dashboard version
```bash
pip install pandas streamlit
python -m streamlit run dashboard.py
```
This opens a browser window at `http://localhost:8501`.

## Results

Example open-ended questions and real answers, generated live by Gemini
(none of these were pre-programmed):
- **What percentage of titles are rated TV-MA?** → 32.5%
- **What is the earliest release year in the data?** → 1925
- **Which director has directed the most movies?** → (varies by run,
  correctly computed from real data each time)

## Limitations

- **Uses `eval()` to run AI-generated code.** This is a real security
  consideration if extended to accept untrusted input in production — a
  safer version would validate/sandbox the generated code before
  execution (e.g. a restricted AST-based executor).
- **The LLM can occasionally generate incorrect or non-runnable code**
  for ambiguous questions — always spot-check answers against a known
  result before trusting the tool in a real setting.
- **Multi-value fields** (e.g. `country` and `cast` can contain multiple
  comma-separated values in one cell) aren't automatically split, so
  questions about individual countries/actors within combined entries
  may undercount them.
- **`director` is missing for ~32% of rows** (mostly TV shows), which
  limits the accuracy of "most common director" style questions.
- Free-tier Gemini API has daily rate limits (1,500 requests/day on
  Flash), which is more than sufficient for this project's scale but
  would need a paid tier for high-volume production use.

## Interview Talk Track

- **"How does the AI know what's in your data?"** — I send it only the
  column names and a few sample rows, not the full dataset — keeps
  prompts small and the data private.
- **"What happens if it generates wrong code?"** — I validate outputs
  against known answers during testing; in production I'd add an
  automated validation/sandboxing step before execution.
- **"Why Gemini instead of OpenAI or Claude?"** — Gemini's free API tier
  requires no credit card and doesn't expire, making it accessible for
  prototyping without any cost, while still being a genuinely capable
  LLM for this use case.
- **"Why not just use SQL directly?"** — This is designed for
  non-technical stakeholders who can't write queries themselves.
