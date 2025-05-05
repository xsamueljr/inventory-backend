from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from auth.domain.auth_token import AuthToken
from auth.domain.exceptions.invalid_token import InvalidTokenException
from auth.domain.token_manager import TokenManager
from auth.infrastructure.fastapi.dependencies import get_token_manager
from users.domain.user import User
from users.domain.user_repository import UserRepository
from users.infrastructure.fastapi.dependencies import get_user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_repository: UserRepository = Depends(get_user_repository),
        token_manager: TokenManager = Depends(get_token_manager)
) -> User:
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")

    auth_token = AuthToken(token)
    try:
        user_id = token_manager.decrypt(auth_token)
    except InvalidTokenException:
        raise credentials_exception
    
    user = user_repository.get_by_id(user_id)
    if not user:
        raise credentials_exception
    
    return user
