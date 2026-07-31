from typing import Dict, List

from activity.application.dtos.public_record_info import PublicRecordInfo
from activity.domain.record_repository import RecordRepository
from auth.domain.logged_user_info import LoggedUserInfo
from products.domain.product_repository import ProductRepository


class GetOwnRecordsUseCase:
    def __init__(
        self, record_repo: RecordRepository, product_repo: ProductRepository
    ) -> None:
        self.__record_repo = record_repo
        self.__product_repo = product_repo

    def run(
        self, user: LoggedUserInfo, limit: int, offset: int
    ) -> List[PublicRecordInfo]:
        records = self.__record_repo.get_by_user_id(user.id, limit, offset)

        cache: Dict[str, str] = {}
        results: List[PublicRecordInfo] = []
        for record in records:
            if cache.get(record.product_id) is None:
                product = self.__product_repo.get_by_id(record.product_id)

                cache[record.product_id] = (
                    product.name
                    if product is not None
                    else "Producto borrado"
                )

            results.append(PublicRecordInfo.from_domain(record, cache[record.product_id], user.name))

        return results
