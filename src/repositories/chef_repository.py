from src.database import MysqlConnection
from src.interfaces.repository import IRepository
from typing import List


class ChefRepository(IRepository[dict]):

    def __init__(self) -> None:
        self.connection = MysqlConnection() 

    async def get_all(self) -> List[dict]:
        chefs = await self.connection._query(
        """
            SELECT id,
                chef_name,
                email
            FROM chef
            LIMIT 20;
        """
        )
        return chefs

    async def get(self, id: int) -> dict:
        chef = await self.connection._query(
        """
            SELECT id,
                chef_name,
                email
            FROM chef
            WHERE id = %s
        """,(id,)
        )
        return chef
        

            