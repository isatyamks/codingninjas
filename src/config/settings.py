"""
Centralized configuration for the Excel Mock Interviewer.
Use environment variables for secrets and API keys in production.
"""
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
TRANSCRIPTS_DIR = os.getenv("TRANSCRIPTS_DIR", os.path.join(os.path.dirname(__file__), "../../data/"))
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "../../data/poc_store.db"))
QUESTIONS_DB_PATH = os.getenv("QUESTIONS_DB_PATH", os.path.join(os.path.dirname(__file__), "../../data/questions_db.json"))
