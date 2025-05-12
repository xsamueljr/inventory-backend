import os

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, EmailStr

load_dotenv()


class EnvConfig(BaseModel):
    JWT_SECRET_KEY: str
    GMAIL_ADDRESS: EmailStr
    GMAIL_PASSWORD: str
    BOSS_EMAIL_ADDRESS: EmailStr

    model_config = ConfigDict(frozen=True)

env = EnvConfig(**os.environ)