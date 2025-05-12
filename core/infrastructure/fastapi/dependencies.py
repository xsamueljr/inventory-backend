from functools import lru_cache

from emails.domain.emailer import Emailer
from emails.infrastructure.console_mailer import ConsoleMailer
from emails.infrastructure.smtp_gmailer import SMTPGmailer
from shared.infrastructure.env import env

@lru_cache
def get_mailer() -> Emailer:
    if env.SEND_REAL_EMAILS:
        return SMTPGmailer()
    return ConsoleMailer()
