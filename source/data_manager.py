import json
from pathlib import Path

app_root = Path(__file__).resolve().parent.parent

def write_data_to_file(data, filename):
    path = Path(filename)
    if not path.is_absolute(): path = app_root / path
    with open(path, "w") as json_file:
        json.dump(data, json_file)

def read_data_from_file(filename):
    path = Path(filename)
    if not path.is_absolute(): path = app_root / path
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data
