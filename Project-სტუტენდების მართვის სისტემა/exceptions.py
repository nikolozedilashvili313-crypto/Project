"""საკუთარი exception-ების იერარქია სტუდენტების მართვის სისტემისთვის."""


class StudentError(Exception):
    """ყველა საკუთარი შეცდომის ძირითადი კლასი."""


class ValidationError(StudentError):
    """მომხმარებელმა (ან ფაილმა) არასწორი მონაცემი მოგვცა."""


class DuplicateRollError(ValidationError):
    """სიის ასეთი ნომერი უკვე არსებობს."""


class StudentNotFoundError(StudentError):
    """სტუდენტი ვერ მოიძებნა."""


class StorageError(StudentError):
    """ფაილთან მუშაობის პრობლემა."""