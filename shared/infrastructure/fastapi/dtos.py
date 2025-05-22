from pydantic import BaseModel, Field


class PaginationQueryParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
