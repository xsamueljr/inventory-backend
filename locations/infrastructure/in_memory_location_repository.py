from locations.domain.location import Location
from locations.domain.location_repository import LocationRepository


class InMemoryLocationRepository(LocationRepository):
    def __init__(self):
        self._locations: list[Location] = []

    def get_all(self) -> list[Location]:
        return self._locations
