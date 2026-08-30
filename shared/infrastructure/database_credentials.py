from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseCredentials:
    connection_string: str
    schema: str
