from src.database import ISqlDBConnection
from src.interfaces.connection_db import ISqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import Recipe
from typing import List


class RecipeRepository(IRecipeRepository):
    def __init__(self,connection: ISqlDBConnection) -> None:
        self.connection = connection
    
    def get_all(self, offset: int, limit: int) -> List[Recipe]:
        ...

    def get(self, id: int) -> Recipe:
        ...

    async def add(self, data: Recipe) -> None:
        ...

    def delete(self, id: int) -> None:
        ...

    def update(self, id: int, data: Recipe) -> None:
        ...
