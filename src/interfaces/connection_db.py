from abc import ABC,abstractmethod


class IConnectionDB(ABC):

    @abstractmethod
    def _connection(self):
        raise NotImplementedError
    
    @abstractmethod
    def execute(self, **kwargs: object):
        raise NotImplementedError


    

