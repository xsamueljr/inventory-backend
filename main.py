from fastapi import FastAPI
import uvicorn

from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher
from auth.infrastructure.fastapi.router import create_auth_router
from auth.infrastructure.jwt_token_manager import JwtTokenManager
from users.infrastructure.in_memory_user_repository import InMemoryUserRepository
from products.infrastructure.fastapi.router import router as products_router


def main():    
    app = FastAPI()

    app.include_router(create_auth_router())
    app.include_router(products_router)

    uvicorn.run(app)

if __name__ == "__main__":
    main()
