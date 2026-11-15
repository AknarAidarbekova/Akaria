import json
from pathlib import Path



def load_research_data(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f'File {file_path} does not exist')

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def load_research_registry(file_path="data/metadata/research_registry.json"):
    registry = load_research_data(file_path)

    investigations = registry.get("investigations", [])
    return investigations

def get_research_by_id(research_id):
    investigations = load_research_registry()

    for investigation in investigations:
        if investigation["id"].upper() == research_id.upper():
            return investigation

    return None
