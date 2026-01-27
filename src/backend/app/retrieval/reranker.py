from typing import List

def rerank_chunks(
    query: str,
    candidates: List[dict],
    key_terms: List[str],
    intent: str
) -> List[dict]:

    scored = []
    query_lower = query.lower()

    # --- GLOBAL SIGNALS ---
    data_seeking_signals = {
        "table", "chart", "graph", "figure", "stats", "statistics",
        "data", "number", "value", "rate", "percentage", "score",
        "metric", "result"
    }
    user_wants_data = any(s in query_lower for s in data_seeking_signals)

    explanatory_signals = {
        "defined as", "means", "consist of", "process", "mechanism",
        "method", "principle", "theory", "concept", "framework",
        "architecture", "function", "role", "purpose", "how", "why",
        "structure", "component", "step", "workflow"
    }

    reporting_signals = {
        "table", "figure", "fig.", "show", "demonstrate", "result",
        "outcome", "performance", "score", "rate", "comparison",
        "evaluation", "analysis"
    }

    math_signals = {
        "=", "+", "-", "*", "/", "\\",
        "sigma", "theta", "alpha",
        "formula", "equation"
    }

    for c in candidates:
        # ---------------------------------------------------------
        # ✅ EXTRACT FIELDS FIRST (FIX)
        # ---------------------------------------------------------
        score = c.get("score", 0.5)
        chunk_text = c.get("text", "").lower()
        concept = c.get("concept", "").lower()
        anchor = c.get("anchor_type", "")
        full_context = f"{concept} {chunk_text}"

        # ---------------------------------------------------------
# 🔒 CORE CONCEPT COVERAGE FILTER (NEW)
# ---------------------------------------------------------
        if intent in {"explain", "define"}:
            # how many key terms are actually present?
            key_term_hits = sum(1 for k in key_terms if k in full_context)
        
            # require at least 2 meaningful hits
            if key_term_hits < max(1, len(key_terms) // 2):
                continue  # 🚫 not about the asked concept

        # ---------------------------------------------------------
        # FEATURE 1: Noise reduction for generic headers
        # ---------------------------------------------------------
        is_generic_header = "text excerpt" in concept or len(concept) < 3
        if is_generic_header:
            keyword_hits = sum(1 for k in key_terms if k in full_context)
            has_math = any(m in chunk_text for m in math_signals)

            if not (keyword_hits >= 2 or has_math):
                score -= 0.15

        # ---------------------------------------------------------
        # FEATURE 2: Concept relevance
        # ---------------------------------------------------------
        term_hits = sum(1 for k in key_terms if k in concept)
        score += term_hits * 0.20

        # ---------------------------------------------------------
        # FEATURE 3: Intent-aware scoring
        # ---------------------------------------------------------
        if intent in {"explain", "define"}:
            if any(s in full_context for s in explanatory_signals):
                score += 0.2

            if any(m in chunk_text for m in math_signals):
                score += 0.15

            if not user_wants_data:
                if any(r in full_context for r in reporting_signals):
                    score -= 0.3

        elif intent == "compare":
            if "compar" in full_context or "vs" in full_context:
                score += 0.25

        elif intent == "summarize":
            if any(x in concept for x in ["introduction", "overview", "summary", "conclusion"]):
                score += 0.3

        # ---------------------------------------------------------
        # FEATURE 4: Anchor priority
        # ---------------------------------------------------------
        if intent in {"explain", "diagram"}:
            if anchor == "image":
                score += 0.25
            elif anchor == "hybrid":
                score += 0.15

        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored]
