from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import uuid4

from auth.domain.logged_user_info import LoggedUserInfo


@dataclass
class Product:
    name: str
    stock: int
    arriving_date: Optional[date] = None

    id: str = field(default_factory=lambda: str(uuid4()))
    location_id: int | None = None

    def has_low_stock(self) -> bool:
        return self.stock <= 1

    # Technical debt (domain using a DTO from application) but at least it isn't huge logic
    def can_be_managed_by(self, user: LoggedUserInfo) -> bool:
        if self.is_global():
            return True

        if user.is_admin:
            return True

        return self.location_id == user.location_id

    def is_global(self) -> bool:
        return self.location_id is None

    def is_local(self) -> bool:
        return self.location_id is not None
