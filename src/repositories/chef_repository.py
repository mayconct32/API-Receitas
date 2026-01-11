from src.interfaces.repository import IRepository
from src.interfaces.connection_db import IConnectionDB
from typing import List


class ChefRepository(IRepository[dict]):

    def __init__(self,connection:IConnectionDB) -> None:
        self.connection = connection

    async def get_all(self) -> List[dict]:
        chefs = await self.connection.execute(
        """
            SELECT chef_id,
                chef_name,
                email,
                create_at,
                updated_at
            FROM chef
            LIMIT 20;
        """
        )
        return chefs

    async def get(
        self, 
        id: int = None,
        chef_name: str = None,
        email: str = None
    )-> dict:
        chef = await self.connection.execute(
        """
            SELECT chef_id,
                chef_name,
                email,
                create_at,
                updated_at
            FROM chef
            WHERE chef_id = %s or 
            chef_name = %s or 
            email = %s
        """,(id,chef_name,email)
        )
        return chef
    
    async def add(self, data: tuple) -> None:
        await self.connection.execute(
        """
            INSERT INTO chef(
                chef_name,
                email,
                password_hash,
                create_at,
                updated_at
            )
            VALUES (%s,%s,%s,%s,%s);
        """,data
        )
    
    async def delete(self, id: int) -> None:
        await self.connection.execute(
        """
            DELETE FROM chef WHERE chef_id = %s;
        """,(id,)
        )
    
    async def update(self, data: tuple) -> None:
        await self.connection.execute(
        """
            UPDATE chef SET
                chef_name = %s,
                email = %s,
                password_hash = %s
            WHERE chef_id = %s;
        """,data
        )
    

            