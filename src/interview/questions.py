
# questions.py
# -----------------------------
# This module contains the question bank for the Excel Mock Interviewer.
# Each question is a dictionary with metadata, the question text, and the ideal answer.
# Extend this list to add more questions or support more difficulty levels.

QUESTIONS = [
    {
        "id": "q1",
        "difficulty": "entry",
        "title": "Absolute vs Relative Reference",
        "question": "What is an absolute cell reference in Excel, and when would you use it? Give an example.",
        "ideal": "An absolute reference uses $ to lock a row/column (e.g. $A$1). Use when copying formulas but you need a fixed reference (e.g. fixed tax rate cell). Example: =A2*$B$1 where $B$1 is tax rate."
    },
    {
        "id": "q2",
        "difficulty": "entry",
        "title": "Find Duplicates",
        "question": "How can you identify duplicate values in a single column? Provide at least two methods (GUI or formula).",
        "ideal": "Methods: Conditional Formatting -> Highlight Duplicates, or formula: =COUNTIF(A:A, A2) > 1 which returns TRUE if duplicate. Also Remove Duplicates or PivotTable counts."
    },
    {
        "id": "q3",
        "difficulty": "entry",
        "title": "VLOOKUP basics",
        "question": "How does VLOOKUP work and what's a common pitfall? Give a small example formula.",
        "ideal": "VLOOKUP(value, table_range, col_index, [range_lookup]). Pitfall: if range_lookup omitted or TRUE it expects sorted table; use FALSE for exact match. Example: =VLOOKUP(B2, $F$2:$G$100, 2, FALSE)."
    },
    {
        "id": "q4",
        "difficulty": "mid",
        "title": "PivotTable Summarize",
        "question": "You have transaction-level sales data (Date, Region, Product, Amount). How would you quickly produce total sales by Region and Month? Describe steps.",
        "ideal": "Create PivotTable: Rows -> Region; Columns -> Month (or Group by Month on Date); Values -> Sum of Amount. Alternatively use SUMIFS with helper columns."
    }
]
