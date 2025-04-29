from abc import ABC, abstractmethod

from emails.application.dtos.email_config import EmailConfig
from emails.domain.email import Email


class EmailSender(ABC):

    def __init__(self, config: EmailConfig) -> None:
        self.__config = config

    @abstractmethod
    def send(self, email: Email) -> None: ...