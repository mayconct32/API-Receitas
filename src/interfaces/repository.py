from abc import ABC,abstractmethod
from typing import List


class IRepository[T](ABC):

    @abstractmethod
    def get_all(self) -> List[T]:
       raise NotImplementedError

    @abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs: object) -> None:
        raise NotImplementedError