from functools import lru_cache

from fastapi import Depends

from auth.application.login_user import LoginUserUsecase
from auth.application.register_user import RegisterUserUsecase
from auth.domain.password_hasher import PasswordHasher
from auth.domain.token_manager import TokenManager
from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher
from auth.infrastructure.jwt_token_manager import JwtTokenManager
from users.domain.user_repository import UserRepository
from users.infrastructure.fastapi.dependencies import get_user_repository


@lru_cache
def get_token_manager() -> TokenManager:
    return JwtTokenManager()


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()

@lru_cache
def get_register_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher)
) -> RegisterUserUsecase:
    return RegisterUserUsecase(
        user_repository,
        hasher
    )

@lru_cache
def get_login_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_manager: TokenManager = Depends(get_token_manager)
) -> LoginUserUsecase:
    return LoginUserUsecase(
        user_repository,
        hasher,
        token_manager
    )