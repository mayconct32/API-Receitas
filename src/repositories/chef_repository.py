from src.database import MysqlConnection


class ChefRepository:

    def __init__(self):
        self.connection = MysqlConnection()
    
    async def get_chefs(self) -> None:
        pass
    
    async def add_chef(self) -> None:
        pass
    
    async def delete_chef(self) -> None:
        pass

    async def update_chef(self) -> None:
        pass
    