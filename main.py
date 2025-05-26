from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth.infrastructure.fastapi.router import router as auth_router
from products.infrastructure.fastapi.router import router as products_router
from shared.infrastructure.env import ENV


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(ENV.FRONTEND_URL)],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(products_router)

    return app


def main():
    app = create_app()

    uvicorn.run(app)


if __name__ == "__main__":
    main()
