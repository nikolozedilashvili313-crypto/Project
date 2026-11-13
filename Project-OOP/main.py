"""სტუდენტების მართვის სისტემა: მენიუ, ოპერაციები და პროგრამის გაშვება."""
import storage
from decorators import handle_errors
from models import Student, ValidationError, check_grade, check_name, check_roll

students = []



def show_menu():
    """აჩვენებს მენიუს."""
    print("\n1. ახალი სტუდენტის დამატება")
    print("2. ყველა სტუდენტის ნახვა")
    print("3. სტუდენტის ძებნა ნომრით")
    print("4. შეფასების განახლება")
    print("5. გასვლა")



@handle_errors
def add_student():
    """ითხოვს სახელს, ნომერს და შეფასებას, ქმნის სტუდენტს და ინახავს."""
    name = ask("სახელი: ", check_name)
    roll = ask("სიის ნომერი: ", check_roll)
    grade = ask("შეფასება (A-F): ", check_grade)
    if any(s.roll_number == roll for s in students):
        raise ValueError("ასეთი სიის ნომერი უკვე არსებობს.")
    students.append(Student(name, roll, grade))
    storage.save(students)
    print("დაემატა.")


@handle_errors
def show_all():
    """აჩვენებს ყველა სტუდენტს."""
    for s in students:
        print(s)
    if not students:
        print("სია ცარიელია.")


@handle_errors
def search_student():
    """ეძებს სტუდენტს სიის ნომრით და აჩვენებს მის დეტალებს."""
    print(find(ask("სიის ნომერი: ", check_roll)))


@handle_errors
def update_grade():
    """ცვლის მითითებული სტუდენტის შეფასებას და ინახავს."""
    student = find(ask("სიის ნომერი: ", check_roll))
    student.grade = ask("ახალი შეფასება (A-F): ", check_grade)
    storage.save(students)
    print("განახლდა:", student)


def find(roll):
    """აბრუნებს სტუდენტს სიის ნომრით, თუ ვერ იპოვა, ისვრის შეცდომას."""
    for s in students:
        if s.roll_number == roll:
            return s
    raise ValueError("სტუდენტი ვერ მოიძებნა.")



def ask(text, check):
    """სანამ სწორ მნიშვნელობას არ შეიყვანს, ისევ ეკითხება."""
    while True:
        try:
            return check(input(text))
        except ValidationError as e:
            print("შეცდომა:", e)



def main():
    """პროგრამის მთავარი ციკლი: ტვირთავს მონაცემებს და ამუშავებს მენიუს არჩევანს."""
    try:
        students.extend(storage.load())
    except ValueError as e:
        print("შეცდომა:", e)
        return
    actions = {"1": add_student, "2": show_all, "3": search_student, "4": update_grade}
    while True:
        show_menu()
        choice = input("არჩევანი: ").strip()
        if choice == "5": 
            break
        if choice in actions:
            actions[choice]()
        else:
            print("არასწორი არჩევანი.")


if __name__ == "__main__":
    main()