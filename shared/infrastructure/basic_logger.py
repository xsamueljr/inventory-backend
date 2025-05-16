import logging

from shared.domain.logger import Logger


class BasicLogger(Logger):
    
    def __init__(self) -> None:
        self.__logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        self.__logger.setLevel(logging.INFO)
    
    def info(self, message: str) -> None:
        self.__logger.info(message)
    
    def warning(self, message: str) -> None:
        self.__logger.warning(message)
    
    def error(self, message: str) -> None:
        self.__logger.error(message)


basic_logger = BasicLogger()
