


# semantic_eval.py
# -----------------------------
# LLM-based semantic evaluation for candidate answers.
# Uses OpenAI API to score and provide feedback on Excel interview responses.

import openai
import json
from ..config import OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY

EVAL_PROMPT_SYSTEM = """
You are an objective Excel interviewer & grader. Input:
- Question
- Ideal (short ideal answer/rubric)
- Candidate (answer text or formula)

Return a JSON object exactly with keys:
{
 "score": int (0-10),
 "confidence": float (0.0-1.0),
 "feedback": "1-3 short sentences",
 "missed_points": ["list", "of", "missed"],
 "extracted_formula": "if detected"
}
Scoring guidance:
- 10: fully correct + example/formula when appropriate.
- 7-9: mostly correct, minor omissions.
- 4-6: partial.
- 0-3: incorrect/irrelevant.
Be concise.
"""

def call_llm_evaluator(question: str, ideal: str, candidate: str) -> dict:
    """
    Call OpenAI ChatCompletion to evaluate and return parsed JSON.
    Minimal temperature, deterministic.
    """
    if OPENAI_API_KEY is None:
        # fallback if no API key - return neutral low confidence
        return {"score": 5, "confidence": 0.2, "feedback": "LLM not available. Please configure OPENAI_API_KEY.", "missed_points": [], "extracted_formula": ""}
    try:
        prompt = f"Question:\n{question}\n\nIdeal:\n{ideal}\n\nCandidate:\n{candidate}\n\nReturn the JSON described in the system instruction."
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": EVAL_PROMPT_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=400
        )
        text = resp["choices"][0]["message"]["content"].strip()
        # parse json substring
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except Exception as e:
        return {"score": 0, "confidence": 0.0, "feedback": f"Evaluation error: {e}", "missed_points": [], "extracted_formula": ""}
