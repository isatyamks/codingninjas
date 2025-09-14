"""
Session model for interview state and persistence.
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class Session:
    session_id: str
    candidate_name: str
    level: str
    started_at: str
    current_q_idx: int = 0
    qa: List[Dict] = field(default_factory=list)
    scores: List[int] = field(default_factory=list)
    final_report: Dict = field(default_factory=dict)
    transcript: List[Dict] = field(default_factory=list)
    progress: float = 0.0
    completed: bool = False

    def log_turn(self, question: str, answer: str, eval_result: Dict):
        self.transcript.append({
            "question": question,
            "answer": answer,
            "eval": eval_result,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.progress = round(len(self.scores) / max(1, self.current_q_idx+1), 2)
        if self.current_q_idx >= 9:
            self.completed = True
