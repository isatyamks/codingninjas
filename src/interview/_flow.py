
def load_questions(level="entry"):
    if level == "entry":
        return [q for q in QUESTIONS if q["difficulty"] == "entry"]
    elif level == "mid":
        # mix entry + mid
        entry = [q for q in QUESTIONS if q["difficulty"] == "entry"]
        mid = [q for q in QUESTIONS if q["difficulty"] == "mid"]
        return entry + mid
    else:
        return QUESTIONS



from .questions import QUESTIONS
from .state import Session, new_session
from ..evaluation.scoring import evaluate_answer

def interview_intro(session: Session):
    return f"Hello {session.candidate_name}, I am your AI Excel interviewer. We'll ask you a series of questions to assess your skills. Please answer each to the best of your ability. Let's begin!"

def select_next_question(session: Session):
    # Adaptive: If last score < 5, pick easier; if >8, pick harder
    idx = session.current_q_idx
    if idx == 0:
        return QUESTIONS[0]
    last_score = session.scores[-1] if session.scores else 10
    if last_score < 5:
        easy = [q for q in QUESTIONS if q["difficulty"] == "entry"]
        return easy[min(idx, len(easy)-1)]
    elif last_score > 8:
        hard = [q for q in QUESTIONS if q["difficulty"] == "hard"]
        return hard[min(idx, len(hard)-1)]
    else:
        return QUESTIONS[min(idx, len(QUESTIONS)-1)]

def process_answer(session: Session, question: dict, answer: str):
    eval_result = evaluate_answer(question["question"], question["ideal"], answer)
    session.qa.append({"question": question["question"], "answer": answer, "eval": eval_result})
    session.scores.append(eval_result["score"])
    session.current_q_idx += 1
    # Log transcript turn
    session.log_turn(question["question"], answer, eval_result)
    return eval_result

def interview_step(session: Session, answer: str = None):
    """
    Orchestrates a single interview step: asks next question, processes answer, updates state.
    Returns dict with next question, evaluation, and completion status.
    """
    if session.completed:
        return {"completed": True, "summary": interview_summary(session)}
    if answer is not None:
        question = select_next_question(session)
        eval_result = process_answer(session, question, answer)
        # Check if interview is complete
        if session.current_q_idx >= len(QUESTIONS):
            session.completed = True
            return {"completed": True, "summary": interview_summary(session)}
        next_q = select_next_question(session)
        return {"completed": False, "next_question": next_q["question"], "eval": eval_result}
    else:
        next_q = select_next_question(session)
        return {"completed": False, "next_question": next_q["question"]}

def interview_summary(session: Session):
    total = sum(session.scores)
    max_score = len(session.scores) * 10
    pct = round(total / max_score * 100, 1) if max_score > 0 else 0.0
    strengths = [qa["eval"]["feedback"] for qa in session.qa if qa["eval"]["score"] > 7]
    improvements = [qa["eval"]["feedback"] for qa in session.qa if qa["eval"]["score"] < 7]
    return {
        "score": total,
        "max": max_score,
        "percent": pct,
        "strengths": strengths,
        "improvements": improvements,
        "summary": f"Thank you, {session.candidate_name}. Your total score is {total}/{max_score} ({pct}%)."
    }
