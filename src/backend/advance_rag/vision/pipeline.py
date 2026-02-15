from app.vision.explanation_parser import parse_sections
from app.vision.schemas import ImageExplanation
from app.vision.storage import store_image_explanation


def process_single_image_explanation(
    result: dict,
    base_dir: str,
    pdf_id: str,
):
    """
    Phase 5.2 pipeline:
    - Parse raw image explanation
    - Validate with schema
    - Persist to disk
    - Return validated object
    """

    parsed = parse_sections(result["raw_explanation"])

    validated = ImageExplanation(
        image_id=result["image_id"],
        page_number=result["page_number"],
        **parsed
    )

    store_image_explanation(
        base_dir=base_dir,
        pdf_id=pdf_id,
        explanation_data=validated.model_dump()
    )

    return validated
