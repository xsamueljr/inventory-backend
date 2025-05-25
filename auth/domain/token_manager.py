from abc import ABC, abstractmethod

from auth.domain.auth_token import AuthToken


class TokenManager(ABC):
    @abstractmethod
    def encrypt(self, user_id: str) -> AuthToken: ...

    @abstractmethod
    def decrypt(self, token: AuthToken) -> str: ...
