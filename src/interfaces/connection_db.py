from abc import ABC,abstractmethod
from typing import Any


class IConnectionDB(ABC):

    @abstractmethod
    def _connection(self) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def execute(self,sql:str,data: object=None) -> Any:
        raise NotImplementedError


    

