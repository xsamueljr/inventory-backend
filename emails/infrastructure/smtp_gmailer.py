from smtplib import SMTP
from email.mime.text import MIMEText

from shared.infrastructure.env import ENV
from emails.domain.email import Email
from emails.domain.emailer import Emailer


class SMTPGmailer(Emailer):
    def __init__(self) -> None:
        self.__server = SMTP(host="smtp.gmail.com", port=587)

        self.__server.starttls()
        self.__server.login(ENV.GMAIL_ADDRESS, ENV.GMAIL_PASSWORD)
        self.__address = ENV.GMAIL_ADDRESS

    def close(self) -> None:
        self.__server.close()

    def __enter__(self) -> None: ...

    def __close__(self) -> None:
        self.close()

    def send(self, email: Email) -> None:
        mime = MIMEText(email.body)
        mime["Subject"] = email.subject
        mime["From"] = self.__address
        mime["To"] = ENV.BOSS_EMAIL_ADDRESS

        self.__server.sendmail(self.__address, ENV.BOSS_EMAIL_ADDRESS, mime.as_string())
