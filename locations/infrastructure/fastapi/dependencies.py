from functools import lru_cache

from fastapi import Depends
from locations.application.get_all_locations import GetAllLocationsUseCase
from locations.domain.location_repository import LocationRepository
from locations.infrastructure.supabase_location_repository import (
    SupabaseLocationRepository,
)


from shared.infrastructure.database_credentials import DatabaseCredentials
from shared.infrastructure.env import ENV


@lru_cache
def get_location_repository() -> LocationRepository:
    return SupabaseLocationRepository(
        DatabaseCredentials(
            connection_string=ENV.SUPABASE_PG_CONN,
            schema=ENV.PG_SCHEMA,
        )
    )


def get_get_all_locations_usecase(
    repo: LocationRepository = Depends(get_location_repository),
) -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase(repo)
