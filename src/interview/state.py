
# state.py
# -----------------------------
# Interview session state management for the Excel Mock Interviewer.
# Tracks candidate progress, answers, scores, transcript, and completion status.


# state.py
# -----------------------------
# Interview session state management for the Excel Mock Interviewer.
# Tracks candidate progress, answers, scores, transcript, and completion status.

import uuid
from datetime import datetime
from src.models.session import Session

def new_session(name: str = "Candidate", level: str = "entry") -> Session:
    """
    Create a new interview session for a candidate.
    """
    sid = uuid.uuid4().hex[:8]
    return Session(session_id=sid, candidate_name=name, level=level, started_at=datetime.utcnow().isoformat())
