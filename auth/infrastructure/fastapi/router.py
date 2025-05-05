from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from auth.application.dtos.login_attempt import LoginAttemptDTO
from auth.application.login_user import LoginUserUsecase
from auth.application.register_user import RegisterUserUsecase
from auth.domain.exceptions.invalid_credentials import InvalidCredentialsException
from auth.domain.password_hasher import PasswordHasher
from auth.domain.token_manager import TokenManager
from auth.infrastructure.fastapi.dependencies import get_login_usecase, get_password_hasher, get_register_usecase, get_token_manager
from auth.infrastructure.fastapi.dtos import LoginRequest, RegisterRequest, TokenResponse
from users.domain.user_repository import UserRepository
from users.infrastructure.fastapi.dependencies import get_user_repository


def create_auth_router() -> APIRouter:
    router = APIRouter(prefix="/api/auth", tags=["auth"])

    @router.post("/register", status_code=201)
    def register(
        request: RegisterRequest,
        usecase: RegisterUserUsecase = Depends(get_register_usecase)
    ) -> None:
        usecase.run(
            request.username,
            request.shop_name,
            request.password
        )
    
    @router.post("/login")
    def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        usecase: LoginUserUsecase = Depends(get_login_usecase)
    ) -> TokenResponse:
        input = LoginAttemptDTO(form.username, form.password)
        
        try:
            token = usecase.run(input)
            return TokenResponse(access_token=token.content, token_type="bearer")
        except InvalidCredentialsException:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    return router
