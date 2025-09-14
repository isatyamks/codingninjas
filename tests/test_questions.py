import pytest
from src.interview.questions import QUESTIONS

def test_questions_structure():
    for q in QUESTIONS:
        assert "id" in q
        assert "difficulty" in q
        assert "question" in q
        assert "ideal" in q
