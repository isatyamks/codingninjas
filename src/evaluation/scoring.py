
def evaluate_answer(question: str, ideal: str, candidate: str):
    """
    Hybrid evaluation:
      - rule checks for formula syntax
      - call LLM for semantic scoring
      - combine into final score object
    """
    rule = simple_formula_check(candidate) if looks_like_formula(candidate) else {"is_formula": False}
    llm_result = call_llm_evaluator(question, ideal, candidate)

    # Heuristic combination:
    score = llm_result.get("score", 0)
    confidence = llm_result.get("confidence", 0.0)

    # if it's a formula and parentheses unbalanced, penalize
    if rule.get("is_formula") and not rule.get("balanced"):
        score = max(0, score - 3)
        llm_result["feedback"] = (llm_result.get("feedback", "") + " Note: formula parentheses appear unbalanced.").strip()
        confidence = min(0.6, confidence)

    # If formula detected, preserve extracted formula
    extracted = llm_result.get("extracted_formula") or (candidate.strip() if rule.get("is_formula") else "")

    result = {
        "score": int(score),
        "confidence": float(confidence),
        "feedback": llm_result.get("feedback", ""),
        "missed_points": llm_result.get("missed_points", []),
        "extracted_formula": extracted
    }
    return result

# scoring.py
# -----------------------------
# Hybrid answer evaluation logic for Excel Mock Interviewer.
# Combines rule-based formula checks and LLM semantic analysis for robust scoring.
