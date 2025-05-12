from fastapi import FastAPI
import uvicorn

from auth.infrastructure.fastapi.router import create_auth_router
from products.infrastructure.fastapi.router import router as products_router


def main():    
    app = FastAPI()

    app.include_router(create_auth_router())
    app.include_router(products_router)

    uvicorn.run(app)

if __name__ == "__main__":
    main()
