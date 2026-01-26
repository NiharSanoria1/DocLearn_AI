from pathlib import Path

# ----------------------------
# Imports
# ----------------------------
from app.parsing.structure_analyzer import analyze_pdf_structure
from app.parsing.text_normalizer import normalize_text_pages
from app.parsing.image_extractor import extract_images_from_pdf

from app.vision.image_filter import should_explain_image
from app.vision.image_explainer import explain_image
from app.vision.storage import load_image_explanations
from app.vision.pipeline import process_single_image_explanation

from app.knowledge.pipeline import run_phase6
from app.chunking.pipeline import run_phase7


# ----------------------------
# Config
# ----------------------------
pdf_id = "77573c06-3e83-4ab6-a3fb-f62987065c5a"

raw_base = Path("data/raw/test_user")
processed_base = Path("data/processed/test_user")

pdf_path = raw_base / pdf_id / "original.pdf"
processed_dir = processed_base / pdf_id
processed_dir.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Phase 2
# ----------------------------
print("▶ Phase 2: Analyzing PDF structure")
phase2_output = analyze_pdf_structure(str(pdf_path))


# ----------------------------
# Phase 3
# ----------------------------
print("▶ Phase 3: Normalizing text")
raw_pages = normalize_text_pages(phase2_output)


# ----------------------------
# Phase 4
# ----------------------------
print("▶ Phase 4: Extracting images")
images_metadata = extract_images_from_pdf(
    pdf_path=str(pdf_path),
    output_dir=str(processed_dir / "images")
)


# ----------------------------
# Phase 5
# ----------------------------
print("▶ Phase 5: Image explanations")

image_explanations_path = processed_dir / "image_explanations.json"


def is_valid_phase5_output(data: list[dict]) -> bool:
    """
    Phase 5.2 output MUST contain 'explanation'
    """
    if not data:
        return False
    return all("explanation" in img for img in data)


image_explanations = []

if image_explanations_path.exists() and image_explanations_path.stat().st_size > 0:
    print("  ▶ Found existing image explanations, validating")
    loaded = load_image_explanations(str(processed_base), pdf_id)

    if is_valid_phase5_output(loaded):
        print("  ✔ Phase 5.2 data valid, using cached explanations")
        image_explanations = loaded
    else:
        print("  ⚠ Old Phase 5 data detected, regenerating")

if not image_explanations:
    print("  ▶ Generating image explanations")

    for img in images_metadata:
        page_number = img["page_number"]

        page_text = next(
            (p["clean_text"] for p in raw_pages if p["page_number"] == page_number),
            ""
        )

        if not should_explain_image(img, page_text):
            continue

        result = explain_image(
            image_path=img["file_path"],
            page_text=page_text,
            image_id=f"page_{page_number}_img_{img['image_index']}",
            page_number=page_number,
        )

        validated = process_single_image_explanation(
            result=result,
            base_dir=str(processed_base),
            pdf_id=pdf_id,
        )

        image_explanations.append(validated.model_dump())


# ----------------------------
# Phase 6
# ----------------------------
print("▶ Phase 6: Knowledge merging")
units = run_phase6(raw_pages, image_explanations, pdf_id)


# ----------------------------
# Phase 7
# ----------------------------
print("▶ Phase 7: Chunking")
chunks = run_phase7(units, use_llm=True)


# ----------------------------
# Output
# ----------------------------
print("\n✅ FINAL CHUNKS\n")
for c in chunks:
    print(
        f"{c.chunk_id} | {c.unit_id} | {c.concept} | words={len(c.text.split())}"
    )
