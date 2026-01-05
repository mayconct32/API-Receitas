from src.interfaces.repository import IRepository
from src.interfaces.service import IService

class ChefService(IService):

    def __init__(self,chef_repository:IRepository) -> None:
        self.chef_repository = chef_repository
    
    