from dataclasses import dataclass


@dataclass
class Email:
    subject: str
    body: str
