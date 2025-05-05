from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    password: str
    shop_name: str
