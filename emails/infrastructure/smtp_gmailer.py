from smtplib import SMTP
from email.mime.text import MIMEText

from shared.infrastructure.env import env
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from emails.infrastructure.dtos.smtp_credentials import SMTPCredentialsDTO

class SMTPGmailer(Emailer):

    def __init__(self, credentials: SMTPCredentialsDTO) -> None:
        self.__server = SMTP(
            host="smtp.gmail.com",
            port=467
        )

        self.__server.login(credentials.address, credentials.password)
        self.__address = credentials.address
    
    def __enter__(self) -> None: ...

    def __close__(self) -> None:
        self.__server.close()
        

    def send(self, email: Email) -> None:
        mime = MIMEText(email.body)
        mime["Subject"] = email.subject
        mime["From"] = self.__address
        mime["To"] = env.BOSS_EMAIL_ADDRESS

        self.__server.send_message(mime)
