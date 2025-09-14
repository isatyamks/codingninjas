
def looks_like_formula(text: str) -> bool:
    if not text:
        return False
    t = text.strip()
    return t.startswith("=")

def simple_formula_check(formula: str) -> dict:
    """
    Basic checks:
      - starts with '='
      - parentheses balanced
      - simple keyword checks (VLOOKUP, COUNTIF, INDEX)
    Returns dict with summary info for scoring.
    """
    out = {"is_formula": False, "balanced": True, "keywords": [], "error": None}
    if not formula:
        return out
    s = formula.strip()
    if not s.startswith("="):
        out["error"] = "Formula does not start with ="
        return out
    out["is_formula"] = True
    # parentheses balance
    if s.count("(") != s.count(")"):
        out["balanced"] = False
    # keywords
    kws = ["VLOOKUP", "COUNTIF", "INDEX", "MATCH", "SUMIFS", "XLOOKUP"]
    present = [k for k in kws if k in s.upper()]
    out["keywords"] = present
    return out

# regex_rules.py
# -----------------------------
# Utility functions for basic Excel formula validation using regex and string checks.
# Used for rule-based evaluation before LLM semantic analysis.
