from fastapi import APIRouter
from fastapi.param_functions import Depends

from locations.application.get_all_locations import GetAllLocationsUseCase
from locations.infrastructure.fastapi.dependencies import get_get_all_locations_usecase

router = APIRouter(prefix="/api/locations", tags=["locations"])

@router.get("/")
def list_locations(usecase: GetAllLocationsUseCase = Depends(get_get_all_locations_usecase)):
    return {"locations": usecase.run()}
