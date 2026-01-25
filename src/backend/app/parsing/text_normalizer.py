import re


def basic_cleanup(text: str) -> str:
    # Replace multiple spaces with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize newlines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Strip leading/trailing whitespace
    return text.strip()

def normalize_bullets(text: str) -> str:
    bullet_chars = ["•", "–", "▪", "●", "○"]

    for ch in bullet_chars:
        text = text.replace(ch, "-")

    return text

def consolidate_lines(text: str) -> str:
    lines = text.split("\n")
    consolidated = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # If first line, just add
        if not consolidated:
            consolidated.append(line)
            continue

        prev = consolidated[-1]

        # Heuristics to decide merge
        should_merge = (
            len(prev) > 40 and                 # not a short heading
            not prev.startswith("-") and       # not a bullet
            not line.startswith("-") and       # not a bullet
            line[0].islower()                   # continuation of sentence
        )

        if should_merge:
            consolidated[-1] = prev + " " + line
        else:
            consolidated.append(line)

    return "\n".join(consolidated)

def split_inline_bullets(text: str) -> str:
    """
    Splits cases where multiple bullets appear on the same line.
    """
    lines = text.split("\n")
    fixed_lines = []

    for line in lines:
        if line.count("- ") > 1:
            parts = re.split(r"(?=- )", line)
            for part in parts:
                fixed_lines.append(part.strip())
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)

def merge_short_headings(text: str) -> str:
    lines = text.split("\n")
    merged = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if (
            i + 1 < len(lines)
            and len(line.split()) <= 3
            and len(lines[i + 1].split()) <= 3
            and not line.startswith("-")
            and not lines[i + 1].startswith("-")
        ):
            merged.append(line + " " + lines[i + 1].strip())
            i += 2
        else:
            merged.append(line)
            i += 1

    return "\n".join(merged)


def normalize_text_pages(pages_structure: list):
    
    """ 
    Takes Phase 2 page wise structure 
    Returns cleaned , structured text per page
    """
    
    normalized_pages = []
    
    for page in pages_structure:
        
        page_number = page["page_number"]
        raw_text = page["text"] or ""
        
        clean_text = basic_cleanup(raw_text)
        clean_text = normalize_bullets(clean_text)
        clean_text = split_inline_bullets(clean_text)
        clean_text = consolidate_lines(clean_text)
        clean_text = merge_short_headings(clean_text)
        
        normalized_pages.append({
            "page_number": page_number,
            "clean_text" : clean_text
        })
        
    return normalized_pages