import re
from typing import List

# guardrail rules

# paterens inicating a likely hallucination or generic answer
_GENERIC_REFUSAL_PATTERNS = [
    r"\bnot (found|enough information)\b",
    r"\bdoesn'?t know\b",
    r"\bunable to answer\b",
    r"\bnot present in\b",
]

def has_page_citation(text: str) -> bool:
    """
    Check if the answer contains at least one (Page X) citation.
    """
    # e.g. (page 5), (pages 3,4)
    return bool(re.search(r"\(Page\s+\d+", text))

def is_generic_refusal(answer: str) -> bool:
    """
    Detect if the answer is a generic refusal rather than a grounded explanation.
    """
    lower = answer.lower()
    return any(re.search(pat, lower) for pat in _GENERIC_REFUSAL_PATTERNS)

def enforce_answer_guardrails(answer: str, context_text: str) -> str:
    """
    validate or override the LLM output Based on guardrail check.
    """ 
    # 1) if answer has no citations, refuse
    if not has_page_citation(answer):
        return "Not Found in this PDF."
    
    # 2) if answer looks like generic LLM Fallback
    if is_generic_refusal(answer):
        return "Not Found in this PDF"
    
    # 3) (Optional extension) Check length vs context proportion
    # If answer much longer than context, it may be speculative.
    # But this is experimental — can be enabled later.
    return answer
