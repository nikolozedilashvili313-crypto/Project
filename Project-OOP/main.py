"""სტუდენტების მართვის სისტემა: მენიუ, ოპერაციები და პროგრამის გაშვება."""
from decorators import ErrorHandler
from models import Student, ValidationError
from storage import Storage


class StudentManager:
    """მართავს სტუდენტების სიას: მენიუ, დამატება, ძებნა, განახლება."""

    def __init__(self, storage):
        """იღებს Storage ობიექტს და ქმნის ცარიელ სიას."""
        self.storage = storage
        self.students = []

    def show_menu(self):
        """აჩვენებს მენიუს."""
        print(" ---მენიუ---  \n1. ახალი სტუდენტის დამატება")
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

    def find(self, roll):
        """აბრუნებს სტუდენტს სიის ნომრით, თუ ვერ იპოვა, ისვრის შეცდომას."""
        for s in self.students:
            if s.roll_number == roll:
                return s
        raise ValueError("სტუდენტი ვერ მოიძებნა.")

    @ErrorHandler.handle_errors
    def add_student(self):
        """ითხოვს სახელს, ნომერს და შეფასებას, ქმნის სტუდენტს და ინახავს."""
        name = self.ask("სახელი: ", Student.check_name)
        roll = self.ask("სიის ნომერი: ", Student.check_roll)
        grade = self.ask("შეფასება (A-F): ", Student.check_grade)
        if any(s.roll_number == roll for s in self.students):
            raise ValueError("ასეთი სიის ნომერი უკვე არსებობს.")
        self.students.append(Student(name, roll, grade))
        self.storage.save(self.students)
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
        student.grade = self.ask("ახალი შეფასება (A-F): ", Student.check_grade)
        self.storage.save(self.students)
        print("განახლდა:", student)

    def run(self):
        """პროგრამის მთავარი ციკლი: ტვირთავს მონაცემებს და ამუშავებს მენიუს არჩევანს."""
        try:
            self.students.extend(self.storage.load())
        except ValueError as e:
            print("შეცდომა:", e)
            return
        actions = {
            "1": self.add_student,
            "2": self.show_all,
            "3": self.search_student,
            "4": self.update_grade,
        }
        while True:
            self.show_menu()
            choice = input("არჩევანი: ").strip()
            if choice == "5":
                break
            if choice in actions:
                actions[choice]()
            else:
                print("არასწორი არჩევანი.")


if __name__ == "__main__":
    StudentManager(Storage()).run()