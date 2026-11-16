"""დეკორატორები: შეცდომების დამუშავება."""
import functools


class ErrorHandler:
    """კლასი, რომელიც აერთიანებს შეცდომების დამმუშავებელ დეკორატორებს."""

    @staticmethod
    def handle_errors(func):
        """დეკორატორი: იჭერს შეცდომას და ბეჭდავს მას პროგრამის გაჩერების ნაცვლად."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("შეცდომა:", e)
        return wrapper