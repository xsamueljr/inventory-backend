import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

load_dotenv()

TRUTHY_VALUES = {"true", "1", "yes", "y"}

class EnvConfig(BaseModel):
    JWT_SECRET_KEY: str
    SQLITE_PATH: Optional[str] = Field(default=None)
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: str
    BOSS_EMAIL_ADDRESS: EmailStr
    SEND_REAL_EMAILS: bool = Field(default=False)
    SUPABASE_PG_CONN: str
    PG_SCHEMA: str

    ENABLE_REGISTER: bool = Field(default=False)

    model_config = ConfigDict(frozen=True)

    @field_validator("SEND_REAL_EMAILS", mode="before")
    @classmethod
    def parse_send_real_emails(cls, value: Optional[str]) -> bool:
        return value in TRUTHY_VALUES
    
    @field_validator("ENABLE_REGISTER", mode="before")
    @classmethod
    def parse_enable_register(cls, value: Optional[str]) -> bool:
        return value in TRUTHY_VALUES

env = EnvConfig(**os.environ) # type: ignore
