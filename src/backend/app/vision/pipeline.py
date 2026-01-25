from app.vision.explanation_parser import parse_sections
from app.vision.schemas import ImageExplanation
from app.vision.storage import store_image_explanation

parsed = parse_sections(result["raw_explanation"])

validated = ImageExplanation(
    image_id=result["image_id"],
    page_number=result["page_number"],
    **parsed
)

store_image_explanation(
    base_dir="data/processed/test_user",
    pdf_id="80f241f5-f098-4d93-b79b-f15a933b4f7a",
    explanation_data=validated.model_dump()
)