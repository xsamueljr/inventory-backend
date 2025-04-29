from logging import config
from smtplib import SMTP
from email.mime.text import MIMEText

from emails.application.dtos.email_config import EmailConfig
from shared.infrastructure.env import env
from emails.domain.email import Email
from emails.domain.email_sender import EmailSender


class SMTPGmailer(EmailSender):

    def __init__(self, config: EmailConfig) -> None:
        super().__init__(config)
        
        self.__server = SMTP(
            host="smtp.gmail.com",
            port=467
        )

        self.__server.login(env.GMAIL_ADDRESS, env.GMAIL_PASSWORD)
    
    def __enter__(self) -> None: ...

    def __close__(self) -> None:
        self.__server.close()
        

    def send(self, email: Email) -> None:
        mime = MIMEText(email.body)
        mime["Subject"] = email.subject
        mime["From"] = self.__config.gmail_address
        mime["To"] = self.__config.boss_email

        self.__server.send_message(mime)
