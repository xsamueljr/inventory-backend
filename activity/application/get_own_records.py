from typing import Dict, List

from activity.application.dtos.public_record_info import PublicRecordInfo
from activity.domain.record_repository import RecordRepository
from auth.domain.logged_user_info import LoggedUserInfo
from products.domain.product_repository import ProductRepository
from products.domain.product import Product
from products.domain.exceptions.product_not_found import ProductNotFoundException


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

        cache: Dict[str, Product] = {}
        results: List[PublicRecordInfo] = []
        for record in records:
            if cache.get(record.product_id) is None:
                product = self.__product_repo.get_by_id(record.product_id)
                if product is None:
                    raise ProductNotFoundException(record.product_id)
                cache[record.product_id] = product

            results.append(
                PublicRecordInfo(
                    kind=record.kind,
                    amount=record.amount,
                    product_name=cache[record.product_id].name,
                    user_name=user.name,
                    created_at=record.created_at,
                )
            )

        return results
