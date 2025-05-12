from smtplib import SMTP
from email.mime.text import MIMEText

from shared.infrastructure.env import env
from emails.domain.email import Email
from emails.domain.emailer import Emailer


class SMTPGmailer(Emailer):

    def __init__(self) -> None:
        self.__server = SMTP(
            host="smtp.gmail.com",
            port=587
        )

        self.__server.starttls()
        self.__server.login(env.GMAIL_ADDRESS, env.GMAIL_PASSWORD)
        self.__address = env.GMAIL_ADDRESS
    
    def close(self) -> None:
        self.__server.close()
    
    def __enter__(self) -> None: ...

    def __close__(self) -> None:
        self.close()

    def send(self, email: Email) -> None:
        mime = MIMEText(email.body)
        mime["Subject"] = email.subject
        mime["From"] = self.__address
        mime["To"] = env.BOSS_EMAIL_ADDRESS

        self.__server.sendmail(self.__address, env.BOSS_EMAIL_ADDRESS, mime.as_string())
