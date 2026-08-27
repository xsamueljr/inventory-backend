from typing import List

from locations.domain.location import Location
from locations.domain.location_repository import LocationRepository


class InMemoryLocationRepository(LocationRepository):
    def __init__(self):
        self._locations: List[Location] = []

    def get_all(self) -> List[Location]:
        return self._locations
