from datetime import datetime, timedelta
from turtle import st
from typing import Any, Dict

from jose.exceptions import ExpiredSignatureError
from jose import JWTError, jwt

from auth.domain.auth_token import AuthToken
from auth.domain.exceptions.expired_token import ExpiredTokenException
from auth.domain.exceptions.invalid_token import InvalidTokenException
from auth.domain.token_manager import TokenManager


class JwtTokenManager(TokenManager):
    def __init__(self) -> None:
        self.__secret_key = "GET FROM ENV LATER"

    def encrypt(self, user_id: str) -> AuthToken:
        

        expires_at = datetime.now() + timedelta(hours=1)
        expiration = int(expires_at.timestamp())

        payload = {
            "sub": user_id,
            "exp": expiration
        }

        try:
            return AuthToken(jwt.encode(payload, self.__secret_key))
        except JWTError:
            raise InvalidTokenException()
    
    def decrypt(self, token: AuthToken) -> str:
        try:
            decoded = jwt.decode(token.content, self.__secret_key)
            return decoded["sub"]
        except ExpiredSignatureError:
            raise ExpiredTokenException()
        except JWTError:
            raise InvalidTokenException()
