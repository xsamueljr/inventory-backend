from fastapi import APIRouter, Depends

from core.infrastructure.fastapi.security import get_current_user
from products.application.create_product import CreateProductUseCase
from products.domain.product_repository import ProductRepository
from products.infrastructure.fastapi.dependencies import get_create_product_usecase, get_product_repository
from products.infrastructure.fastapi.dtos import CreateProductRequest
from users.domain.user import User


router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("/", status_code=201)
def create(
    request: CreateProductRequest,
    user: User = Depends(get_current_user),
    usecase: CreateProductUseCase = Depends(get_create_product_usecase)
):
    input = request.map_to_domain()
    id = usecase.run(input)
    return {"id": id}
