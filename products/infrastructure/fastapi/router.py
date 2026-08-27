from typing import List, TypedDict

from fastapi import APIRouter, Depends, HTTPException

from auth.domain.logged_user_info import LoggedUserInfo
from core.infrastructure.fastapi.security import get_current_user
from products.application.create_product import CreateProductUseCase
from products.application.delete_by_id import DeleteProductByIdUsecase
from products.application.dtos.public_product import PublicProductInfo
from products.application.get_all import GetAllProductsUsecase
from products.application.get_by_id import GetProductByIdUsecase
from products.application.get_local_products import GetLocalProductsUseCase
from products.application.register_arrival import RegisterArrivalUsecase
from products.application.register_sell import RegisterSaleUsecase
from products.application.search_by_name import SearchProductsByNameUsecase
from products.infrastructure.fastapi.dependencies.usecases import (
    get_all_products_usecase,
    get_create_product_usecase,
    get_delete_product_usecase,
    get_get_local_products_usecase,
    get_product_by_id_usecase,
    get_register_arrival_usecase,
    get_register_sale_usecase,
    get_search_products_by_name_usecase,
)
from products.infrastructure.fastapi.dtos import (
    CreateProductRequest,
    RegisterArrivalRequest,
    RegisterSaleRequest,
)
from shared.infrastructure.fastapi.dtos import PaginationQueryParams


class CreateProductResponse(TypedDict):
    id: str


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def get_products(
    name: str | None = None,
    pagination: PaginationQueryParams = Depends(),
    usecase: GetAllProductsUsecase = Depends(get_all_products_usecase),
    search_usecase: SearchProductsByNameUsecase = Depends(
        get_search_products_by_name_usecase
    ),
) -> List[PublicProductInfo]:
    if name:
        return search_usecase.run(name)
    return usecase.run(pagination.limit, pagination.offset)


@router.get("/{id}")
def get_by_id(
    id: str, usecase: GetProductByIdUsecase = Depends(get_product_by_id_usecase)
) -> PublicProductInfo:
    return usecase.run(id)


@router.get("/local")
def get_local_products(
    user: LoggedUserInfo = Depends(get_current_user),
    pagination: PaginationQueryParams = Depends(),
    usecase: GetLocalProductsUseCase = Depends(get_get_local_products_usecase),
) -> List[PublicProductInfo]:
    if not user.location_id:
        raise HTTPException(status_code=400, detail="Location ID is required")

    return usecase.run(user.location_id, pagination.limit, pagination.offset)


@router.post("", status_code=201)
def create(
    request: CreateProductRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: CreateProductUseCase = Depends(get_create_product_usecase),
) -> CreateProductResponse:
    input = request.map_to_domain()
    id = usecase.run(user, input)
    return {"id": id}

@router.post("/local", status_code=201)
def create_local(
    request: CreateProductRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: CreateProductUseCase = Depends(get_create_product_usecase),
) -> CreateProductResponse:
    input = request.map_to_domain()
    if not user.location_id:
        raise HTTPException(status_code=400, detail="Location ID is required")

    input.location_id = user.location_id
    id = usecase.run(user, input)
    return {"id": id}


@router.delete("/{id}", status_code=204)
def delete(
    id: str,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: DeleteProductByIdUsecase = Depends(get_delete_product_usecase),
) -> None:
    usecase.run(user, id)


@router.post("/sale", status_code=201)
def register_sale(
    request: RegisterSaleRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: RegisterSaleUsecase = Depends(get_register_sale_usecase),
) -> None:
    usecase.run(user, request.map_to_dto())


@router.post("/arrival", status_code=201)
def register_arrival(
    request: RegisterArrivalRequest,
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: RegisterArrivalUsecase = Depends(get_register_arrival_usecase),
) -> None:
    usecase.run(user, request.map_to_dto())
