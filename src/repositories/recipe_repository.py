from src.database import MongoDBConnection
from src.interfaces.connection_db import INoSqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    Recipe,
    ResponseRecipe
)
from typing import List


class RecipeRepository(IRecipeRepository):
    def __init__(self,connection: INoSqlDBConnection) -> None:
        self.connection = connection.get_db_connection()
        self.collection_name = "Recipe"
    
    async def get_all(self, offset: int, limit: int) -> List[ResponseRecipe]:
        collection = self.connection.get_collection(self.collection_name)
        cursor = collection.find().limit(limit).skip(offset)
        recipes = [recipe async for recipe in cursor]
        return recipes

    