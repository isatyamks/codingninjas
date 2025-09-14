import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # change if needed

TRANSCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
