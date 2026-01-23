from abc import ABC, abstractmethod


class ISqlDBConnection(ABC):
    @abstractmethod
    def _connection(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, sql: str, data=None):
        raise NotImplementedError
