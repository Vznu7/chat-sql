# Chat with SQL (SQLite / MySQL) using Streamlit + LangChain + Groq

A small Streamlit app that lets you ask questions in natural language and get answers from a SQL database.

- **SQLite mode**: uses the included `student.db` demo database (read-only connection).
- **MySQL mode**: connect to your own MySQL database from the sidebar.

## Demo

The app uses a LangChain SQL agent and a Groq-hosted LLM to:
- inspect the database schema,
- generate SQL queries,
- run them against your database,
- and return the result as a conversational answer.

## Project structure

- `app.py` — Streamlit UI + LangChain SQL agent
- `sqlite.py` — creates and seeds `student.db` with a `STUDENT` table

## Requirements

- Python 3.10+ recommended
- A **Groq API key**

Python packages (installed via pip):
- `streamlit`
- `sqlalchemy`
- `langchain-community`
- `langchain-groq`
- (optional, for MySQL) `mysql-connector-python`

## Setup

### 1) Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install streamlit sqlalchemy langchain-community langchain-groq
# Optional: only needed if you want to connect to MySQL
pip install mysql-connector-python
```

### 3) (SQLite demo) Create the sample database

This generates `student.db` in the project folder:

```powershell
python sqlite.py
```

## Run the app

```powershell
streamlit run app.py
```

Then in the Streamlit sidebar:

1. Paste your **Groq API key**.
2. Choose **SQLite** (demo) or **MySQL**.
3. If using MySQL, fill in host/user/password/database.

## Example questions

Try asking:

- "Show all students with marks above 90"
- "What is the average marks by class?"
- "Who scored the highest marks in section A?"
- "Count students by class and section"

## Notes / Security

- LLM-driven SQL agents can be vulnerable to **prompt injection**. Treat this as a demo and use least-privileged DB credentials.
- In SQLite mode, the app opens the database in **read-only** mode (`mode=ro`).
- For MySQL, consider using a dedicated DB user with read-only permissions.

## Troubleshooting

- **`student.db` not found**: run `python sqlite.py` and make sure `student.db` is in the same folder as `app.py`.
- **MySQL connection errors**: verify host/user/password/db name and ensure `mysql-connector-python` is installed.
- **Groq auth errors**: confirm the API key is correct and active.

## License

No license is included yet. If you plan to publish this publicly, add a `LICENSE` file (for example: MIT).
