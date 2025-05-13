import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

load_dotenv()


class EnvConfig(BaseModel):
    JWT_SECRET_KEY: str
    SQLITE_PATH: Optional[str]
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: str
    BOSS_EMAIL_ADDRESS: EmailStr
    SEND_REAL_EMAILS: bool = Field(default=False)

    model_config = ConfigDict(frozen=True)

    @field_validator("SEND_REAL_EMAILS", mode="before")
    @classmethod
    def parse_send_real_emails(cls, value: Optional[str]) -> bool:
        return value is not None

env = EnvConfig(**os.environ) # type: ignore
