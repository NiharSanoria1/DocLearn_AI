import json
from pathlib import Path

def store_image_explanation(
    base_dir: str,
    pdf_id: str,
    explanation_data: dict
):
    """
    Stores image explanations in image_explanations.json
    """
    
    output_dir = Path(base_dir) / pdf_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "image_explanations.json"
    
    if file_path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
        
    data.append(explanation_data)
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
            
    