import os

from pydantic import BaseModel, EmailStr


class EnvConfig(BaseModel):
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: EmailStr
    BOSS_EMAIL_ADDRESS: EmailStr

env = EnvConfig(**os.environ)