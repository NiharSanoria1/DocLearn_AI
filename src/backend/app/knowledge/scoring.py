from re import findall

def extract_candidate_concepts(text: str, image_concepts: list[str]) -> list[str]:
    """
    Merge text keywords and image concepts into a candidate list.
    Simple placeholder: union for now.
    Later you might add clustering / dedup.
    """
    
    # simple text keyword extraction (e.g., uppercase tokens, nouns, known concepts)
    tokens = findall(r"\b[A-Z][a-zA-Z0-9_]+\b", text)
    text_concepts = list(set(tokens))
    
    all_concepts = sorted(set(text_concepts + image_concepts))
    
    return all_concepts

def text_strength(text: str) -> float:
    """
    Simple heuristic: length + keyword density
    """
    return len(text.split()) / 100.0  # coarse

def image_strength(image_explanation: str) -> float:
    """
    Simple proxy: explanation length
    """
    return len(image_explanation.split()) / 100.0  # coarse