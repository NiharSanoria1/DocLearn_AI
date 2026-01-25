SYSTEM_PROMPT = """
You are an educational teaching assistant.
You explain diagrams to students clearly and faithfully.

Rules:
- Do NOT use knowledge outside the provided image and context.
- Do NOT guess unseen details.
- If something is not visible, say it is not shown.
- Focus on relationships, flow, and meaning.
- Use simple, student-friendly language.
"""

USER_PROMPT_TEMPLATE = """
Task:
Explain this educational diagram.

Context from PDF page:
{page_text}

Explain:
- What the diagram represents
- How components relate to each other
- What a student should learn from it

Return the explanation in this format:

Visual Description:
Explanation:
Key Concepts:
Teaching Notes:
Limitations:
"""
