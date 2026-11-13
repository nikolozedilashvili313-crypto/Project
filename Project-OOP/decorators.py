def handle_errors(func):
    def wrapper(*args):
        try:
            return func(*args)
        except Exception as e:
            print("შეცდომა:", e)
    return wrapper