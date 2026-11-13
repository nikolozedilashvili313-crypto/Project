import json
import os

from models import Student

FILE = "students.json"


def load():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, encoding="utf-8") as f:
            return [Student(**d) for d in json.load(f)]
    except (json.JSONDecodeError, TypeError):
        raise ValueError(f"ფაილი {FILE} დაზიანებულია.")


def save(students):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in students], f, ensure_ascii=False, indent=2)