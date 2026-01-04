from src.interfaces.repository import IRepository
from src.interfaces.connection_db import IConnectionDB
from typing import List


class ChefRepository(IRepository[dict]):

    def __init__(self,connection:IConnectionDB) -> None:
        self.connection = connection

    async def get_all(self) -> List[dict]:
        chefs = await self.connection.execute(
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
        chef = await self.connection.execute(
        """
            SELECT id,
                chef_name,
                email
            FROM chef
            WHERE id = %s
        """,(id,)
        )
        return chef
    
    async def add(self, data: tuple) -> None:
        await self.connection.execute(
        """
            INSERT INTO chef(
                chef_name,
                email,
                password_hash
            )
            VALUES (%s,%s,%s);
        """,data
        )
    
    async def delete(self, id: int) -> None:
        await self.connection.execute(
        """
            DELETE FROM chef WHERE id = %s;
        """,(id,)
        )
    
    async def update(self, data: tuple) -> None:
        await self.connection._execute(
        """
            UPDATE chef SET
                chef_name = %s,
                email = %s,
                password_hash = %s
            WHERE id = %s;
        """,data
        )
    

            