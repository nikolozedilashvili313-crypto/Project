"""შენახვა: აბსტრაქტული BaseStorage და მისი JSON/CSV რეალიზაციები."""
import csv
import json
import os
from abc import ABC, abstractmethod

from exceptions import StorageError, ValidationError
from models import Student


class BaseStorage(ABC):
    """აბსტრაქტული საბაზო კლასი: განსაზღვრავს, რა უნდა შეეძლოს ნებისმიერ შენახვის ტიპს."""

    def __init__(self, file):
        """ინახავს ფაილის სახელს."""
        self.file = file

    @abstractmethod
    def load(self):
        """აბრუნებს Student-ების სიას."""

    @abstractmethod
    def save(self, students):
        """წერს Student-ების სიას ფაილში."""

    def _corrupted(self):
        """აბრუნებს შეცდომას დაზიანებული ფაილისთვის."""
        return StorageError(f"ფაილი {self.file} დაზიანებულია.")

    def _check_unique(self, students):
        """ამოწმებს, რომ ჩატვირთულ სიაში სიის ნომრები არ მეორდება."""
        rolls = [s.roll_number for s in students]
        if len(rolls) != len(set(rolls)):
            raise StorageError(f"ფაილში {self.file} სიის ნომრები მეორდება.")
        return students

    def _atomic_write(self, write_func):
        """წერს დროებით ფაილში და შემდეგ ანაცვლებს ძირითადს.

        ასე ჩაწერის შეწყვეტის შემთხვევაშიც ძველი ფაილი არ ზიანდება.
        """
        tmp_path = self.file + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8", newline="") as f:
                write_func(f)
            os.replace(tmp_path, self.file)
        except OSError as e:
            raise StorageError(f"შენახვა ვერ მოხერხდა: {e}")


class JsonStorage(BaseStorage):
    """ინახავს სტუდენტებს JSON ფაილში."""

    def load(self):
        """კითხულობს JSON ფაილს."""
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise self._corrupted()
            students = [Student(**d) for d in data]
        except (json.JSONDecodeError, TypeError, ValidationError):
            raise self._corrupted()
        except OSError as e:
            raise StorageError(f"ფაილის წაკითხვა ვერ მოხერხდა: {e}")
        return self._check_unique(students)

    def save(self, students):
        """წერს JSON ფაილში."""
        self._atomic_write(
            lambda f: json.dump([s.to_dict() for s in students], f,
                                ensure_ascii=False, indent=2)
        )


class CsvStorage(BaseStorage):
    """ინახავს სტუდენტებს CSV ფაილში."""

    FIELDS = ["name", "roll_number", "grade"]

    def load(self):
        """კითხულობს CSV ფაილს."""
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, encoding="utf-8", newline="") as f:
                students = [Student(**row) for row in csv.DictReader(f)]
        except (TypeError, ValidationError, csv.Error):
            raise self._corrupted()
        except OSError as e:
            raise StorageError(f"ფაილის წაკითხვა ვერ მოხერხდა: {e}")
        return self._check_unique(students)

    def save(self, students):
        """წერს CSV ფაილში."""
        def write(f):
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(s.to_dict() for s in students)

        self._atomic_write(write)