from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    shop_name: str