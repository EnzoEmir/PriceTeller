from typing import Generic, List, Sequence, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagina(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int

    @classmethod
    def criar(cls, items: Sequence, total: int, page: int, limit: int) -> "Pagina":
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
        )
