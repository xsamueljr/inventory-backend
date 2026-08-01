from locations.domain.location_repository import LocationRepository


class GetAllLocationsUseCase:
    def __init__(self, repo: LocationRepository):
        self.__repo = repo

    def run(self):
        return self.__repo.get_all()
