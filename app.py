from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared.domain.exception import AppException, ErrorType
from shared.infrastructure.env import ENV
from auth.infrastructure.fastapi.router import router as auth_router
from products.infrastructure.fastapi.router import router as products_router
from activity.infrastructure.fastapi.router import router as activity_router

app = FastAPI()

@app.exception_handler(AppException)
async def app_exception_handler(_request, exc: AppException):
    status_code_map: dict[ErrorType, int] = {
        ErrorType.NOT_FOUND: 404,
        ErrorType.CONFLICT: 409,
        ErrorType.UNAUTHORIZED: 401,
        ErrorType.VALIDATION: 400,
        ErrorType.INTERNAL: 500,
    }

    status = status_code_map.get(exc.type, 500)
    
    return JSONResponse(
        status_code=status,
        content={"error": str(exc) if status != 500 else "Internal Server Error"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(ENV.FRONTEND_URL).rstrip("/")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(activity_router)
