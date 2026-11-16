"""შენახვა: სტუდენტების ჩატვირთვა და ჩაწერა JSON ფაილში."""
import json
import os

from models import Student, ValidationError


class Storage:
    """პასუხისმგებელია სტუდენტების JSON ფაილში შენახვასა და ჩატვირთვაზე."""

    def __init__(self, file="students.json"):
        """ინახავს ფაილის სახელს."""
        self.file = file

    def load(self):
        """კითხულობს ფაილს და აბრუნებს Student-ების სიას."""
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, encoding="utf-8") as f:
                return [Student(**d) for d in json.load(f)]
        except (json.JSONDecodeError, TypeError, ValidationError):
            raise ValueError(f"ფაილი {self.file} დაზიანებულია.")

    def save(self, students):
        """წერს სტუდენტების სიას ფაილში."""
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students], f, ensure_ascii=False, indent=2)