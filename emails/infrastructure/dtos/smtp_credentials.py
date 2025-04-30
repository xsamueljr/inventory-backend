from dataclasses import dataclass


@dataclass
class SMTPCredentialsDTO:
    address: str
    password: str
