"""სტუდენტების მართვის სისტემა: მენიუ, ოპერაციები და პროგრამის გაშვება."""
from decorators import ErrorHandler
from exceptions import (DuplicateRollError, StorageError, StudentError,
                        StudentNotFoundError, ValidationError)
from models import Student
from storage import JsonStorage


class StudentManager:
    """მართავს სტუდენტების სიას: მენიუ, დამატება, ძებნა, განახლება."""

    def __init__(self, storage):
        """იღებს BaseStorage-ის ნებისმიერ შთამომავალს (JsonStorage, CsvStorage) და ქმნის ცარიელ სიას."""
        self.storage = storage
        self.students = []

    def show_menu(self):
        """აჩვენებს მენიუს."""
        print("\n--- მენიუ ---")
        print("1. ახალი სტუდენტის დამატება")
        print("2. ყველა სტუდენტის ნახვა")
        print("3. სტუდენტის ძებნა ნომრით")
        print("4. შეფასების განახლება")
        print("5. გასვლა")

    def ask(self, text, check):
        """სანამ სწორ მნიშვნელობას არ შეიყვანს, ისევ ეკითხება."""
        while True:
            try:
                return check(input(text))
            except ValidationError as e:
                print("შეცდომა:", e)

    def check_new_roll(self, value):
        """ამოწმებს სიის ნომერს და იმას, რომ ის ჯერ არავის აქვს."""
        roll = Student.check_roll(value)
        if any(s.roll_number == roll for s in self.students):
            raise DuplicateRollError("ასეთი სიის ნომერი უკვე არსებობს.")
        return roll

    def find(self, roll):
        """აბრუნებს სტუდენტს სიის ნომრით, თუ ვერ იპოვა, ისვრის შეცდომას."""
        for s in self.students:
            if s.roll_number == roll:
                return s
        raise StudentNotFoundError("სტუდენტი ვერ მოიძებნა.")

    @ErrorHandler.handle_errors
    def add_student(self):
        """ითხოვს სახელს, ნომერს და შეფასებას, ქმნის სტუდენტს და ინახავს."""
        name = self.ask("სახელი: ", Student.check_name)
        roll = self.ask("სიის ნომერი: ", self.check_new_roll)
        grade = self.ask("შეფასება (A-F): ", Student.check_grade)
        self.students.append(Student(name, roll, grade))
        try:
            self.storage.save(self.students)
        except StorageError:
            self.students.pop()  
            raise
        print("დაემატა.")

    @ErrorHandler.handle_errors
    def show_all(self):
        """აჩვენებს ყველა სტუდენტს."""
        for s in self.students:
            print(s)
        if not self.students:
            print("სია ცარიელია.")

    @ErrorHandler.handle_errors
    def search_student(self):
        """ეძებს სტუდენტს სიის ნომრით და აჩვენებს მის დეტალებს."""
        print(self.find(self.ask("სიის ნომერი: ", Student.check_roll)))

    @ErrorHandler.handle_errors
    def update_grade(self):
        """ცვლის მითითებული სტუდენტის შეფასებას და ინახავს."""
        student = self.find(self.ask("სიის ნომერი: ", Student.check_roll))
        old_grade = student.grade
        student.grade = self.ask("ახალი შეფასება (A-F): ", Student.check_grade)
        try:
            self.storage.save(self.students)
        except StorageError:
            student.grade = old_grade  
            raise
        print("განახლდა:", student)

    def run(self):
        """პროგრამის მთავარი ციკლი: ტვირთავს მონაცემებს და ამუშავებს მენიუს არჩევანს."""
        try:
            self.students.extend(self.storage.load())
        except StudentError as e:
            print("შეცდომა:", e)
            return
        actions = {
            "1": self.add_student,
            "2": self.show_all,
            "3": self.search_student,
            "4": self.update_grade,
        }
        try:
            while True:
                self.show_menu()
                choice = input("არჩევანი: ").strip()
                if choice == "5":
                    break
                if choice in actions:
                    actions[choice]()
                else:
                    print("არასწორი არჩევანი.")
        except (KeyboardInterrupt, EOFError):
            print()
        print("ნახვამდის!")


if __name__ == "__main__":
    StudentManager(JsonStorage("students.json")).run()