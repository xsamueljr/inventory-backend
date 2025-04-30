import os

from pydantic import BaseModel, EmailStr


class EnvConfig(BaseModel):
    BOSS_EMAIL_ADDRESS: EmailStr

env = EnvConfig(**os.environ)