import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

load_dotenv()


class EnvConfig(BaseModel):
    JWT_SECRET_KEY: str
    SQLITE_PATH: Optional[str] = Field(default=None)
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: str
    BOSS_EMAIL_ADDRESS: EmailStr
    SEND_REAL_EMAILS: bool = Field(default=False)
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    DD_USER_TABLE_NAME: str
    DD_PRODUCT_TABLE_NAME: str
    model_config = ConfigDict(frozen=True)

    @field_validator("SEND_REAL_EMAILS", mode="before")
    @classmethod
    def parse_send_real_emails(cls, value: Optional[str]) -> bool:
        return value is not None

env = EnvConfig(**os.environ) # type: ignore
