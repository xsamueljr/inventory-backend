from uuid import uuid4

from auth.domain.password_hasher import PasswordHasher
from users.domain.user import User
from users.domain.user_repository import UserRepository


class RegisterUserUsecase:
    def __init__(self, user_repository: UserRepository, hasher: PasswordHasher) -> None:
        self.__user_repository = user_repository
        self.__hasher = hasher

    def run(self, name: str, shop_name: str, password: str) -> None:
        hashed_password = self.__hasher.hash(password)
        user = User(str(uuid4()), name, hashed_password, shop_name)

        self.__user_repository.save(user)
