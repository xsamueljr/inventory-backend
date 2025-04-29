import os

from pydantic import BaseModel


class EnvConfig(BaseModel):
    GMAIL_ADDRESS: str
    GMAIL_PASSWORD: str

env = EnvConfig(**os.environ)