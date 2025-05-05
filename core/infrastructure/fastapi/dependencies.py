from functools import lru_cache

from emails.domain.emailer import Emailer
from emails.infrastructure.console_mailer import ConsoleMailer


@lru_cache
def get_mailer() -> Emailer:
    return ConsoleMailer()
