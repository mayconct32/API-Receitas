from src.interfaces.repository import IRepository


class ChefService:

    def __init__(self,chef_repository:IRepository) -> None:
        self.chef_repository = chef_repository
    
    