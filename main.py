from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth.infrastructure.fastapi.router import router as auth_router
from products.infrastructure.fastapi.router import router as products_router


def main():    
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(auth_router)
    app.include_router(products_router)

    uvicorn.run(app)

if __name__ == "__main__":
    main()
