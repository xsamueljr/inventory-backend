class InvalidCredentialsException(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")
