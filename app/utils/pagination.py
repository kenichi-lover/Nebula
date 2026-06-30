from math import ceil
from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    skip: int
    limit: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        skip: int,
        limit: int,
    ) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            total_pages=ceil(total / limit) if total > 0 else 0,
        )
