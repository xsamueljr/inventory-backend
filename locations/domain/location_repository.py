from abc import ABC, abstractmethod
from typing import List

from locations.domain.location import Location


class LocationRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Location]: ...
