def parse_sections(raw_text: str) -> dict:
    sections = {
        "visual_description": "",
        "explanation": "",
        "concepts": [],
        "teaching_notes": [],
        "limitations": ""
    }

    current_section = None

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        def extract_inline(header: str, target: str):
            content = line[len(header):].strip()
            if content:
                sections[target] += content + " "

        if lower.startswith("visual description"):
            current_section = "visual_description"
            extract_inline("Visual Description:", "visual_description")
            continue

        elif lower.startswith("explanation"):
            current_section = "explanation"
            extract_inline("Explanation:", "explanation")
            continue

        elif lower.startswith("key concepts"):
            current_section = "concepts"
            continue

        elif lower.startswith("teaching notes"):
            current_section = "teaching_notes"
            continue

        elif lower.startswith("limitations"):
            current_section = "limitations"
            extract_inline("Limitations:", "limitations")
            continue

        # Content handling
        if current_section == "concepts":
            cleaned = line.lstrip("-• ").strip()
            if cleaned:
                sections["concepts"].append(cleaned)

        elif current_section == "teaching_notes":
            cleaned = line.lstrip("-• ").strip()
            if cleaned:
                sections["teaching_notes"].append(cleaned)

        elif current_section:
            sections[current_section] += line + " "

    # Final cleanup
    for key in ["visual_description", "explanation", "limitations"]:
        sections[key] = sections[key].strip()

    return sections
