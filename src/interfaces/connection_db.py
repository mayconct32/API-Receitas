from abc import ABC, abstractmethod

from pymongo.asynchronous.database import AsyncDatabase


class ISqlDBConnection(ABC):
    @abstractmethod
    def _connection(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, sql: str, data=None):
        raise NotImplementedError


class INoSqlDBConnection(ABC):
    @abstractmethod
    def connection_to_db(self):
        raise NotImplementedError

    @abstractmethod
    def get_db_connection(self) -> AsyncDatabase:
        raise NotImplementedError
