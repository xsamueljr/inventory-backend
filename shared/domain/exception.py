class AppException(Exception):
    def __init__(self, *args: object, is_operational: bool) -> None:
        super().__init__(*args)
        self.is_operational = is_operational
