"""
PagedList - Ho tro phan trang
Tuong duong PagedList.cs trong C#
"""
from math import ceil
from typing import Generic, Iterable, List, TypeVar

T = TypeVar("T")


class PagedList(List[T], Generic[T]):
    def __init__(self, items: List[T], total_count: int, page_number: int, page_size: int):
        super().__init__(items)
        self.total_count = total_count
        self.page_size = page_size
        self.current_page = page_number
        self.total_pages = int(ceil(total_count / float(page_size))) if page_size > 0 else 1

    @property
    def has_previous(self) -> bool:
        return self.current_page > 1

    @property
    def has_next(self) -> bool:
        return self.current_page < self.total_pages

    @staticmethod
    def create(query, page_number: int, page_size: int) -> "PagedList":
        total_count = query.count()
        items = query.offset((page_number - 1) * page_size).limit(page_size).all()
        return PagedList(items, total_count, page_number, page_size)
