from smtplib import SMTP, SMTPServerDisconnected
from email.mime.text import MIMEText

from shared.infrastructure.env import ENV
from emails.domain.email import Email
from emails.domain.emailer import Emailer


class SMTPGmailer(Emailer):
    def __init__(self) -> None:
        self.__address = ENV.GMAIL_ADDRESS
        self.__connect_and_login()

    def __connect_and_login(self) -> None:
        self.__server = SMTP(host="smtp.gmail.com", port=587)
        self.__server.starttls()
        self.__server.login(ENV.GMAIL_ADDRESS, ENV.GMAIL_PASSWORD)

    def close(self) -> None:
        self.__server.close()

    def send(self, email: Email) -> None:
        mime = MIMEText(email.body)
        mime["Subject"] = email.subject
        mime["From"] = self.__address
        mime["To"] = ENV.BOSS_EMAIL_ADDRESS

        try:
            self.__server.sendmail(
                self.__address, ENV.BOSS_EMAIL_ADDRESS, mime.as_string()
            )
        except SMTPServerDisconnected:
            self.__connect_and_login()
            self.__server.sendmail(
                self.__address, ENV.BOSS_EMAIL_ADDRESS, mime.as_string()
            )

    def __enter__(self) -> "SMTPGmailer":
        return self

    def __close__(self) -> None:
        self.close()
