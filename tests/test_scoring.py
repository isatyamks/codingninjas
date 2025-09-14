from src.evaluation.scoring import evaluate_answer

def test_evaluate_answer_basic():
    question = "What is 2+2 in Excel?"
    ideal = "=2+2"
    candidate = "=2+2"
    result = evaluate_answer(question, ideal, candidate)
    assert isinstance(result, dict)
    assert "score" in result
    assert "confidence" in result
    assert "feedback" in result
