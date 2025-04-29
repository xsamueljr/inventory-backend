from dataclasses import dataclass


@dataclass
class EmailConfig:
    gmail_address: str
    boss_email: str