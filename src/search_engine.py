import json
import os

def search_ayurveda_data(query: str) -> list:
    """
    Searches the classical Ayurvedic database (data/ayurveda_data.json) for matching terms.
    
    Parameters:
        query (str): Search term provided by user (e.g., 'tulsi', 'acidity', 'pitta').
        
    Returns:
        list: List of matching plant/remedy dictionaries found in the dataset.
    """
    if not query or not query.strip():
        return []

    # Resolve absolute path to data/ayurveda_data.json relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "ayurveda_data.json")

    # Return empty list if dataset file does not exist
    if not os.path.exists(json_path):
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    query_lower = query.strip().lower()
    results = []

    for item in data:
        # Extract text fields safely
        name = str(item.get("name", "")).lower()
        category = str(item.get("category", "")).lower()
        dosha = str(item.get("dosha", "")).lower()
        description = str(item.get("description", "")).lower()
        uses = str(item.get("uses", "")).lower()
        preparation = str(item.get("preparation", "")).lower()
        source_text = str(item.get("source_text", "")).lower()

        # Match query against any relevant dataset field
        if (
            query_lower in name
            or query_lower in category
            or query_lower in dosha
            or query_lower in description
            or query_lower in uses
            or query_lower in preparation
            or query_lower in source_text
        ):
            results.append(item)

    return results