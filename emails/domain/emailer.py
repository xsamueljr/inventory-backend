from abc import ABC, abstractmethod

from emails.domain.email import Email


class Emailer(ABC):
    @abstractmethod
    def send(self, email: Email) -> None: ...
