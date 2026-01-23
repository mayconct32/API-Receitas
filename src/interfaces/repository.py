from abc import ABC, abstractmethod
from typing import List

from src.models.chef import Chef


class IRepository[T](ABC):
    @abstractmethod
    async def get_all(self, offset: int, limit: int) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: T) -> None:
        raise NotImplementedError


class IChefRepository(IRepository[Chef]):
    @abstractmethod
    async def get_by_chef_name(self, chef_name: str) -> Chef:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Chef:
        raise NotImplementedError
