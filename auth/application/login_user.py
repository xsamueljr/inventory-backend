from auth.application.dtos.login_attempt import LoginAttemptDTO
from auth.domain.auth_token import AuthToken
from auth.domain.exceptions.invalid_credentials import InvalidCredentialsException
from auth.domain.password_hasher import PasswordHasher
from auth.domain.token_manager import TokenManager
from users.domain.user_repository import UserRepository


class LoginUserUsecase:
    def __init__(
        self,
        user_repository: UserRepository,
        hasher: PasswordHasher,
        token_manager: TokenManager,
    ) -> None:
        self.__user_repository = user_repository
        self.__hasher = hasher
        self.__token_manager = token_manager

    def run(self, input: LoginAttemptDTO) -> AuthToken:
        user = self.__user_repository.get_by_username(input.username)
        if not user:
            print("No user found")
            raise InvalidCredentialsException()

        if not self.__hasher.compare(input.password, user.password):
            print("Incorrect password")
            raise InvalidCredentialsException()

        return self.__token_manager.encrypt(user.id)
