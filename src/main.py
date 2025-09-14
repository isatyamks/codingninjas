import streamlit as st
from src.interview.state import new_session
from src.interview._flow import load_questions
from src.evaluation.scoring import evaluate_answer
from src.reporting.report_gen import generate_simple_pdf, save_transcript_json
from src.utils.db import init_db, save_session
from src.config import OPENAI_API_KEY
import os

# initialize
init_db()

st.set_page_config(page_title="Excel Mock Interviewer (PoC)", layout="centered")
st.title("AI-Powered Excel Mock Interviewer — PoC")

if "session" not in st.session_state:
    st.session_state.session = None

if st.session_state.session is None:
    with st.form("start_form"):
        name = st.text_input("Candidate name", value="Candidate")
        level = st.selectbox("Target level", ["entry", "mid"])
        start = st.form_submit_button("Start Interview")
    if start:
        session = new_session(name, level)
        # store minimal structure in dict
        st.session_state.session = {
            "session_id": session.session_id,
            "candidate_name": session.candidate_name,
            "level": session.level,
            "started_at": session.started_at,
            "current_q_idx": 0,
            "qa": [],
            "scores": []
        }
        st.experimental_rerun()
else:
    session = st.session_state.session
    st.markdown(f"**Session ID:** `{session['session_id']}`  •  **Candidate:** {session['candidate_name']}  •  **Level:** {session['level']}")
    questions = load_questions(session["level"])
    idx = session["current_q_idx"]

    if idx < len(questions):
        q = questions[idx]
        st.subheader(f"Question {idx+1}: {q['title']}")
        st.write(q["question"])
        ans = st.text_area("Your answer (explain your reasoning; paste a formula if needed)", value="", height=140, key=f"ans_{idx}")
        col1, col2 = st.columns([1,1])
        with col1:
            submit = st.button("Submit Answer", key=f"submit_{idx}")
        with col2:
            skip = st.button("Skip / Next", key=f"skip_{idx}")

        if submit:
            if not ans.strip():
                st.warning("Please enter an answer or press Skip.")
            else:
                with st.spinner("Evaluating answer..."):
                    ev = evaluate_answer(q["question"], q["ideal"], ans)
                    qa_item = {
                        "question_id": q["id"],
                        "question": q["question"],
                        "ideal": q["ideal"],
                        "answer": ans,
                        "eval": ev
                    }
                    session["qa"].append(qa_item)
                    session["scores"].append(ev.get("score", 0))
                    session["current_q_idx"] += 1
                    st.session_state.session = session
                    # persist to DB & transcripts folder
                    save_session(session)
                    save_transcript_json(session)
                    st.success(f"Answer evaluated — score {ev.get('score')}/10")
                    st.markdown("**Feedback:**")
                    st.write(ev.get("feedback"))
                    if ev.get("extracted_formula"):
                        st.info(f"Detected formula: `{ev.get('extracted_formula')}`")
                    st.experimental_rerun()

        if skip:
            qa_item = {
                "question_id": q["id"],
                "question": q["question"],
                "ideal": q["ideal"],
                "answer": None,
                "eval": {"score": 0, "confidence": 0.0, "feedback": "Skipped by candidate", "missed_points": [], "extracted_formula": ""}
            }
            session["qa"].append(qa_item)
            session["scores"].append(0)
            session["current_q_idx"] += 1
            st.session_state.session = session
            save_session(session)
            save_transcript_json(session)
            st.experimental_rerun()

    else:
        # done
        total = sum(session["scores"])
        max_score = len(session["scores"]) * 10
        pct = round(total / max_score * 100, 1) if max_score > 0 else 0.0
        st.success("Interview complete!")
        st.write(f"**Total score:** {total}/{max_score} ({pct}%)")
        if "final_report_generated" not in st.session_state:
            # generate a concise textual summary using LLM if API key exists,
            # otherwise use simple template
            if OPENAI_API_KEY:
                try:
                    from src.evaluation.semantic_eval import call_llm_evaluator
                    # prepare quick prompt to ask for summary
                    summary_text = "Session summary:\n"
                    for i, qa in enumerate(session["qa"], 1):
                        summary_text += f"Q{i}: {qa['question']}\nAnswer: {qa.get('answer')}\nScore: {qa.get('eval',{}).get('score')}\nFeedback: {qa.get('eval',{}).get('feedback')}\n\n"
                    # call LLM to get polished summary (here reuse evaluator but ask for summary)
                    resp = call_llm_evaluator("Generate final summary", "Provide strengths and weaknesses", summary_text)
                    final_text = resp.get("feedback") or "Summary generated."
                except Exception:
                    final_text = "Summary generator unavailable."
            else:
                final_text = "No LLM key — final summary not generated. See per-question feedback above."
            session["final_report"] = {
                "text": final_text,
                "total_score": total,
                "pct": pct
            }
            st.session_state.session = session
            save_session(session)
            save_transcript_json(session)
            st.session_state.final_report_generated = True

        st.markdown("### Final Report")
        st.write(session["final_report"].get("text", ""))
        if st.button("Download PDF report"):
            pdf_path = generate_simple_pdf(session)
            with open(pdf_path, "rb") as f:
                st.download_button("Download report PDF", f, file_name=f"report_{session['session_id']}.pdf")
        if st.button("Start new session"):
            st.session_state.session = None
            st.experimental_rerun()
