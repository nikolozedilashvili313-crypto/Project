"""მოდელები: Student კლასი და შეყვანილი მონაცემების ვალიდაცია."""

class Student:
    """სტუდენტი: სახელი, სიის ნომერი და შეფასება."""

    def __init__(self, name, roll_number, grade):
        """ქმნის სტუდენტს და ამოწმებს სამივე მნიშვნელობას."""
        self._name = check_name(name)
        self._roll_number = check_roll(roll_number)
        self._grade = check_grade(grade)

    @property
    def name(self):
        """აბრუნებს სტუდენტის სახელს."""
        return self._name

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
        self._grade = check_grade(value)

    def to_dict(self):
        """სტუდენტს ლექსიკონად აქცევს (JSON-ში ჩასაწერად)."""
        return {"name": self.name, "roll_number": self.roll_number, "grade": self.grade}

    def __str__(self):
        """აბრუნებს სტუდენტის ტექსტურ აღწერას დასაბეჭდად."""
        return f"№{self.roll_number} | {self.name} | შეფასება: {self.grade}"


class ValidationError(Exception):
    """შეცდომა, როცა მომხმარებელმა არასწორი მონაცემი შეიყვანა."""


def check_name(value):
    """ამოწმებს სახელს: მინიმუმ 2 სიმბოლო, მხოლოდ ასოები."""
    value = value.strip()
    if len(value) < 2 or not value.replace(" ", "").isalpha():
        raise ValidationError("სახელი უნდა შეიცავდეს მხოლოდ ასოებს.")
    return value


def check_roll(value):
    """ამოწმებს სიის ნომერს: უნდა იყოს დადებითი მთელი რიცხვი."""
    if not str(value).strip().isdigit() or int(value) <= 0:
        raise ValidationError("სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი.")
    return int(value)


def check_grade(value):
    """ამოწმებს შეფასებას: ერთი ასო A-დან F-მდე."""
    value = value.strip().upper()
    if value not in ("A", "B", "C", "D", "E", "F"):
        raise ValidationError("შეფასება უნდა იყოს A-დან F-მდე.")
    return value