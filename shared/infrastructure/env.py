import os

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr

load_dotenv()


class EnvConfig(BaseModel):
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: str
    BOSS_EMAIL_ADDRESS: EmailStr

env = EnvConfig(**os.environ)