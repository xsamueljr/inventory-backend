from auth.domain.logged_user_info import LoggedUserInfo
from products.domain.product_repository import ProductRepository
from shared.domain.logger import Logger


class DeleteProductByIdUsecase:
    def __init__(
            self,
            logger: Logger,
            product_repository: ProductRepository
    ) -> None:
        self.__logger = logger
        self.__repo = product_repository

    def run(self, user: LoggedUserInfo, id: str) -> None:
        self.__repo.delete(id)
        self.__logger.info(f"{user.name} ha borrado el producto con ID {id}")
