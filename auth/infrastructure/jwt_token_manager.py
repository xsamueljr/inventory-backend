from datetime import datetime, timedelta

from jose.exceptions import ExpiredSignatureError
from jose import JWTError, jwt

from auth.domain.auth_token import AuthToken
from auth.domain.exceptions.expired_token import ExpiredTokenException
from auth.domain.exceptions.invalid_token import InvalidTokenException
from auth.domain.token_manager import TokenManager
from shared.infrastructure.env import env


class JwtTokenManager(TokenManager):
    def __init__(self) -> None:
        self.__secret_key = env.JWT_SECRET_KEY

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
            print("decrypting")
            decoded = jwt.decode(token.content, self.__secret_key)
            print(decoded)
            print(decoded["sub"])
            return decoded["sub"]
        except ExpiredSignatureError:
            print("already expired")
            raise ExpiredTokenException()
        except JWTError as e:
            print(f"weird error: {e}")
            raise InvalidTokenException()
