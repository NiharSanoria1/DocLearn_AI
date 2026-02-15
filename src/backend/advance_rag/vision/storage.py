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
            
    
def load_image_explanations(
    base_dir: str, pdf_id: str
) -> list[dict]:
    """
    Loads all stored image explanations from disk
    (the file created by store_image_explanation).
    Returns a list of dicts.
    """
    
    file_path = Path(base_dir) /pdf_id / "image_explanations.json"
    
    
    with open(file_path, "r") as f:
        data = json.load(f)

    #validating shape to be a list
    
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {file_path}, got {type(data)}")
    
    return data    