from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from auth.application.dtos.login_attempt import LoginAttemptDTO
from auth.application.login_user import LoginUserUsecase
from auth.application.register_user import RegisterUserUsecase
from auth.domain.exceptions.invalid_credentials import InvalidCredentialsException
from auth.infrastructure.fastapi.dependencies import (
    get_login_usecase,
    get_register_usecase,
)
from auth.infrastructure.fastapi.dtos import RegisterRequest, TokenResponse
from shared.infrastructure.env import ENV


def normal_registration(
    request: RegisterRequest,
    usecase: RegisterUserUsecase = Depends(get_register_usecase),
) -> None:
    usecase.run(request.username, request.shop_name, request.password)


def disabled_registration() -> None:
    raise HTTPException(status_code=403, detail="Registration is disabled")


registration_handler = (
    normal_registration if ENV.ENABLE_REGISTER else disabled_registration
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

router.add_api_route(
    "/register",
    registration_handler,
    methods=["POST"],
    status_code=201,
    responses={
        201: {"description": "User registered successfully"},
        403: {"description": "Registration is disabled"},
    },
)


@router.post("/login")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    usecase: LoginUserUsecase = Depends(get_login_usecase),
) -> TokenResponse:
    input = LoginAttemptDTO(form.username, form.password)

    try:
        token = usecase.run(input)
        return TokenResponse(access_token=token.content, token_type="bearer")
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
