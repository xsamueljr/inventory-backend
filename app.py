from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.infrastructure.env import ENV
from auth.infrastructure.fastapi.router import router as auth_router
from products.infrastructure.fastapi.router import router as products_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(ENV.FRONTEND_URL).rstrip("/")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
