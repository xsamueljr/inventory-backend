from functools import lru_cache

from fastapi import Depends
from locations.application.get_all_locations import GetAllLocationsUseCase
from locations.domain.location_repository import LocationRepository
from locations.infrastructure.supabase_location_repository import (
    SupabaseLocationRepository,
)


@lru_cache
def get_location_repository() -> LocationRepository:
    return SupabaseLocationRepository()


def get_get_all_locations_usecase(
    repo: LocationRepository = Depends(get_location_repository),
) -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase(repo)
