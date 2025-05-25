from functools import lru_cache

from emails.domain.emailer import Emailer
from emails.infrastructure.console_mailer import ConsoleMailer
from emails.infrastructure.smtp_gmailer import SMTPGmailer
from shared.infrastructure.env import ENV


@lru_cache
def get_mailer() -> Emailer:
    if ENV.SEND_REAL_EMAILS:
        return SMTPGmailer()
    return ConsoleMailer()
