
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
    """
    More adaptive selection: considers last score, topic gaps, and follow-up needs.
    """
    idx = session.current_q_idx
    # If first question, start with entry-level
    if idx == 0:
        return QUESTIONS[0]
    last_score = session.scores[-1] if session.scores else 10
    # Identify topics where candidate scored low
    weak_topics = [qa['question'] for qa in session.qa if qa['eval'].get('score_accuracy', qa['eval'].get('score', 0)) < 7]
    # If last answer was weak, probe deeper on same topic
    if last_score < 7 and weak_topics:
        for q in QUESTIONS:
            if q['question'] == weak_topics[-1]:
                return q
    # If last score very high, ask harder or creative question
    if last_score > 8:
        hard = [q for q in QUESTIONS if q["difficulty"] == "hard"]
        if hard:
            return hard[min(idx, len(hard)-1)]
    # Otherwise, continue with next in sequence
    return QUESTIONS[min(idx, len(QUESTIONS)-1)]


def process_answer(session: Session, question: dict, answer: str):
    eval_result = evaluate_answer(question["question"], question["ideal"], answer)
    # Multi-dimensional scoring and feedback
    eval_result.setdefault("score_accuracy", eval_result.get("score", 0))
    eval_result.setdefault("score_efficiency", 8)  # Placeholder, add logic for efficiency
    eval_result.setdefault("score_clarity", 8)     # Placeholder, add logic for clarity
    eval_result.setdefault("score_creativity", 7)  # Placeholder, add logic for creativity
    eval_result.setdefault("suggestions", ["Review advanced Excel topics for improvement."])
    session.qa.append({"question": question["question"], "answer": answer, "eval": eval_result})
    session.scores.append(eval_result["score_accuracy"])
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
    # Aggregate multi-dimensional scores
    accuracy = sum(qa["eval"].get("score_accuracy", 0) for qa in session.qa)
    efficiency = sum(qa["eval"].get("score_efficiency", 0) for qa in session.qa)
    clarity = sum(qa["eval"].get("score_clarity", 0) for qa in session.qa)
    creativity = sum(qa["eval"].get("score_creativity", 0) for qa in session.qa)
    max_score = len(session.qa) * 10
    strengths = [qa["eval"].get("feedback", "") for qa in session.qa if qa["eval"].get("score_accuracy", 0) > 7]
    improvements = [qa["eval"].get("feedback", "") for qa in session.qa if qa["eval"].get("score_accuracy", 0) < 7]
    suggestions = [s for qa in session.qa for s in qa["eval"].get("suggestions", [])]
    return {
        "score_accuracy": accuracy,
        "score_efficiency": efficiency,
        "score_clarity": clarity,
        "score_creativity": creativity,
        "max": max_score,
        "strengths": strengths,
        "improvements": improvements,
        "suggestions": suggestions,
        "summary": f"Thank you, {session.candidate_name}. Your scores - Accuracy: {accuracy}, Efficiency: {efficiency}, Clarity: {clarity}, Creativity: {creativity}."
    }
