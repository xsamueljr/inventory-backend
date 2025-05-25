from pydantic import BaseModel, Field

from auth.application.dtos.login_attempt import LoginAttemptDTO


name_field = Field(min_length=2, max_length=20)
password_field = Field(min_length=4, max_length=16)


class LoginRequest(BaseModel):
    username: str = name_field
    password: str = password_field

    def map_to_domain(self) -> LoginAttemptDTO:
        return LoginAttemptDTO(self.username, self.password)


class RegisterRequest(BaseModel):
    username: str = name_field
    password: str = password_field
    shop_name: str = name_field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
