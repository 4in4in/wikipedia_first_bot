from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResults:
    total: int
    results: list[str]


class Api(ABC):
    @abstractmethod
    def __init__(self, lang: str) -> None:
        ...

    @abstractmethod
    async def search(self, query: str) -> SearchResults:
        ...

    @abstractmethod
    async def get_page_link(self, title: str) -> str:
        ...
