from src.interfaces.repository import IRepository


class ChefService:

    def __init__(self,chef_repository:IRepository) -> None:
        self.chef_repository = chef_repository
    
    async def get_all_the_chefs(self):
        chefs = await self.chef_repository.get_all()
        return chefs