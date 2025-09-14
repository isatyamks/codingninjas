

# questions.py
# -----------------------------
# Loads the advanced question bank from questions_db.json and provides query utilities.

import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/questions_db.json')

def load_questions_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

QUESTIONS = load_questions_db()

def get_questions_by_difficulty(difficulty):
    return [q for q in QUESTIONS if q.get('difficulty') == difficulty]

def get_questions_by_skill(skill):
    return [q for q in QUESTIONS if skill in q.get('skills', [])]

def get_questions_by_tag(tag):
    return [q for q in QUESTIONS if tag in q.get('tags', [])]

def get_question_by_id(qid):
    for q in QUESTIONS:
        if q.get('id') == qid:
            return q
    return None

def get_follow_up_questions(qid):
    q = get_question_by_id(qid)
    if q:
        return [get_question_by_id(fid) for fid in q.get('follow_ups', [])]
    return []
