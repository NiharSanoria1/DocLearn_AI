STOPWORDS = {
     "and", "or", "is", "are", "the", "a", "an"
}

def clean_key_terms(key_terms: list[str]) -> list[str]:
    return [
        t.lower()
        for t in key_terms
        if t.lower() not in STOPWORDS and len(t) > 2
    ]