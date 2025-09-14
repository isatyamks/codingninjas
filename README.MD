
# AI-Powered Excel Mock Interviewer

## Overview

This project is an automated system for assessing candidates' Microsoft Excel skills, designed to streamline and standardize the technical interview process for Finance, Operations, and Data Analytics roles. It simulates a real interview, evaluates answers using both rule-based and AI-driven methods, and generates detailed feedback reports.


## Features

- **Structured Interview Flow:** Multi-turn, adaptive Q&A with topic-based follow-ups and progress tracking.
- **Adaptive Questioning:** Questions adapt in difficulty and topic based on candidate performance and detected gaps.
- **Hybrid & Multi-Dimensional Evaluation:** Combines formula parsing, rule-based checks, and LLM (GPT-4.1) semantic analysis. Scores answers for accuracy, efficiency, clarity, and creativity.
- **Agentic State Management:** Tracks candidate progress, answers, scores, transcript, and adapts questioning strategy.
- **Automated Reporting:** Generates PDF and JSON reports with strengths, weaknesses, improvement suggestions, and personalized feedback.
- **Advanced Analytics:** Supports performance dashboards, trend analysis, and comparative insights for candidates and HR.
- **Scalable Backend:** Designed for cloud deployment and extensibility.

## Architecture

```
Frontend (to be implemented)
  |
Backend (FastAPI, Python)
  |-- Interview Orchestration (src/interview/_flow.py)
  |-- State Management (src/interview/state.py)
  |-- Question Bank (src/interview/questions.py)
  |-- Evaluation Layer (src/evaluation/regex_rules.py, scoring.py, semantic_eval.py)
  |-- Reporting (src/reporting/report_gen.py)
  |-- Persistence (src/utils/db.py)
```

## File Structure

- `src/interview/` - Interview flow, state, and questions
- `src/evaluation/` - Formula validation, scoring, and LLM integration
- `src/reporting/` - PDF and JSON report generation
- `src/utils/` - Database utilities
- `data/` - Stores candidate transcripts and session data
- `requirements.txt` - Python dependencies

## Setup

1. **Clone the repository**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Configure API keys:**
	- Set your OpenAI API key and model in `src/config.py`
4. **Initialize the database:**
	```bash
	python -c "from src.utils.db import init_db; init_db()"
	```

## Usage

1. **Run the backend (example):**
	- Integrate with FastAPI or Flask for API endpoints.
	- Use `Session` and interview flow functions to orchestrate interviews.
2. **Answer Evaluation:**
	- Answers are checked for formula syntax and scored by LLM for correctness and clarity.
3. **Reporting:**
	- After the interview, generate a PDF report using `report_gen.py`.

## Extending the System

- **Add More Questions:** Edit `src/interview/questions.py`.
- **Improve Formula Parsing:** Integrate ANTLR or DuckDB for advanced validation.
- **Frontend:** Build a chat interface and Excel-like grid using Next.js and Handsontable.js.
- **Cloud Deployment:** Containerize and deploy on AWS/GCP for scalability.


## Example Interview Flow

1. Candidate logs in and is greeted by the AI interviewer.
2. System asks a series of Excel questions, adapting difficulty and topic based on performance and detected gaps.
3. The agent probes for deeper understanding with follow-up questions if needed.
4. Each answer is evaluated on multiple dimensions and logged.
5. At the end, a detailed feedback report is generated, including strengths, weaknesses, suggestions, and analytics.

## License

MIT License
