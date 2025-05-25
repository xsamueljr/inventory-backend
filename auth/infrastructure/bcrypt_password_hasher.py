import bcrypt

from auth.domain.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, salt_rounds: int = 10) -> None:
        if salt_rounds not in range(5, 21):
            raise RuntimeError("Forbidden salt rounds amount")

        self.__salt = bcrypt.gensalt(salt_rounds)

    def hash(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), self.__salt).decode()

    def compare(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
