"""დეკორატორები: შეცდომების დამუშავება."""
import functools

from exceptions import StudentError


class ErrorHandler:
    """კლასი, რომელიც აერთიანებს შეცდომების დამმუშავებელ დეკორატორებს."""

    @staticmethod
    def handle_errors(func):
        """დეკორატორი: იჭერს აპლიკაციის შეცდომებს და ბეჭდავს მათ პროგრამის გაჩერების ნაცვლად.

        იჭერს მხოლოდ StudentError-ის შთამომავლებს, ამიტომ პროგრამირების
        შეცდომები (ბაგები) არ იმალება.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except StudentError as e:
                print("შეცდომა:", e)
        return wrapper