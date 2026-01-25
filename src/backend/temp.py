from app.parsing.structure_analyzer import analyze_pdf_structure
from app.parsing.text_normalizer import normalize_text_pages
from app.vision.storage import load_image_explanations
from app.knowledge.pipeline import run_phase6

pdf_id = "80f241f5-f098-4d93-b79b-f15a933b4f7a"

pdf_path = f"data/raw/test_user/{pdf_id}/original.pdf"
base_dir = "data/processed/test_user"

# Phase 2
phase2_output = analyze_pdf_structure(pdf_path)

# Phase 3
raw_pages = normalize_text_pages(phase2_output)

# Phase 5
image_explanations = load_image_explanations(base_dir, pdf_id)

# Phase 6
units = run_phase6(raw_pages, image_explanations, pdf_id)

for u in units:
    print(u.unit_id, u.anchor_type, u.concepts)
