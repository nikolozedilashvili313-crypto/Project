"""მოდელები: Person (საბაზო), Student (შვილობილი) და ვალიდაცია."""
from abc import ABC, abstractmethod

from exceptions import ValidationError


class Person(ABC):
    """აბსტრაქტული საბაზო კლასი: ადამიანი სახელით."""

    def __init__(self, name):
        """ქმნის ადამიანს და ამოწმებს სახელს."""
        self._name = self.check_name(name)

    @staticmethod
    def check_name(value):
        """ამოწმებს სახელს: მინიმუმ 2 სიმბოლო; ასოები, ინტერვალი და დეფისი."""
        if not isinstance(value, str):
            raise ValidationError("სახელი უნდა იყოს ტექსტი.")
        value = value.strip()
        if len(value) < 2:
            raise ValidationError("სახელი უნდა შეიცავდეს მინიმუმ 2 სიმბოლოს.")
        if not value.replace(" ", "").replace("-", "").isalpha():
            raise ValidationError(
                "სახელი უნდა შეიცავდეს მხოლოდ ასოებს (დაშვებულია ინტერვალი და დეფისი)."
            )
        return value

    @property
    def name(self):
        """აბრუნებს სახელს."""
        return self._name

    @abstractmethod
    def describe(self):
        """აბრუნებს აღწერას. თითოეული შვილობილი კლასი თავისებურად ახორციელებს."""

    def to_dict(self):
        """ლექსიკონად აქცევს (JSON/CSV-ში ჩასაწერად)."""
        return {"name": self.name}

    def __str__(self):
        """ბეჭდვისას იძახებს describe-ს (პოლიმორფიზმი)."""
        return self.describe()


class Student(Person):
    """სტუდენტი: Person + სიის ნომერი და შეფასება."""

    GRADES = ("A", "B", "C", "D", "E", "F")

    def __init__(self, name, roll_number, grade):
        """ქმნის სტუდენტს; სახელს ამოწმებს მშობელი კლასი."""
        super().__init__(name)
        self._roll_number = self.check_roll(roll_number)
        self._grade = self.check_grade(grade)

    @staticmethod
    def check_roll(value):
        """ამოწმებს სიის ნომერს: უნდა იყოს დადებითი მთელი რიცხვი."""
        text = str(value).strip()
        if not text.isdecimal() or int(text) <= 0:
            raise ValidationError("სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი.")
        return int(text)

    @staticmethod
    def check_grade(value):
        """ამოწმებს შეფასებას: ერთი ასო A-დან F-მდე."""
        if not isinstance(value, str):
            raise ValidationError("შეფასება უნდა იყოს A-დან F-მდე.")
        value = value.strip().upper()
        if value not in Student.GRADES:
            raise ValidationError("შეფასება უნდა იყოს A-დან F-მდე.")
        return value

    @property
    def roll_number(self):
        """აბრუნებს სიის ნომერს."""
        return self._roll_number

    @property
    def grade(self):
        """აბრუნებს შეფასებას."""
        return self._grade

    @grade.setter
    def grade(self, value):
        """ცვლის შეფასებას, ახალ მნიშვნელობას ვალიდაციით ამოწმებს."""
        self._grade = self.check_grade(value)

    def describe(self):
        """სტუდენტის ტექსტური აღწერა (ცვლის Person.describe-ს)."""
        return f"№{self.roll_number} | {self.name} | შეფასება: {self.grade}"

    def to_dict(self):
        """აფართოებს Person.to_dict-ს სტუდენტის ველებით."""
        data = super().to_dict()
        data.update({"roll_number": self.roll_number, "grade": self.grade})
        return data