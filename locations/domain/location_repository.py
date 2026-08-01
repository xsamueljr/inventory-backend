from abc import ABC, abstractmethod

from locations.domain.location import Location


class LocationRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Location]: ...
