from site import execsitecustomize
from typing import List, TypedDict

from fastapi import APIRouter, Depends, HTTPException

from auth.domain.logged_user_info import LoggedUserInfo
from core.infrastructure.fastapi.security import get_current_user
from products.application.create_product import CreateProductUseCase
from products.application.dtos.public_product import PublicProductInfo
from products.application.get_all import GetAllProductsUsecase
from products.application.get_by_id import GetProductByIdUsecase
from products.application.register_arrival import RegisterArrivalUsecase
from products.application.register_sell import RegisterSaleUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.infrastructure.fastapi.dependencies import get_all_products_usecase, get_create_product_usecase, get_product_by_id_usecase, get_product_repository, get_register_arrival_usecase, get_register_sale_usecase
from products.infrastructure.fastapi.dtos import CreateProductRequest, RegisterArrivalRequest, RegisterSaleRequest
from users.domain.user import User


class CreateProductResponse(TypedDict):
    id: str

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
def get_all(usecase: GetAllProductsUsecase = Depends(get_all_products_usecase)) -> List[PublicProductInfo]:
    return usecase.run()


@router.get("/{id}")
def get_by_id(
    id: str,
    usecase: GetProductByIdUsecase = Depends(get_product_by_id_usecase)
) -> PublicProductInfo:
    try:
        return usecase.run(id)
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")

@router.post("", status_code=201)
def create(
    request: CreateProductRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: CreateProductUseCase = Depends(get_create_product_usecase)
) -> CreateProductResponse:
    input = request.map_to_domain()
    id = usecase.run(input)
    return {"id": id}


@router.post("/sale", status_code=201)
def register_sale(
    request: RegisterSaleRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: RegisterSaleUsecase = Depends(get_register_sale_usecase)
) -> None:
    try:
        usecase.run(request.map_to_dto())
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/arrival", status_code=201)
def register_arrival(
    request: RegisterArrivalRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: RegisterArrivalUsecase = Depends(get_register_arrival_usecase)
) -> None:
    try:
        usecase.run(request.map_to_dto())
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail="Product not found")
