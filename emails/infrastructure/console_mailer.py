from emails.domain.email import Email
from emails.domain.emailer import Emailer


class ConsoleMailer(Emailer):
    def send(self, email: Email) -> None:
        print(email)
