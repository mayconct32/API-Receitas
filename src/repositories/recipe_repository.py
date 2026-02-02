from src.database import MongoDBConnection
from src.interfaces.connection_db import INoSqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    Recipe,
    ChefRecipe,
    RecipeInstruction,
    RecipeIngredient
)
from typing import List


class RecipeRepository(IRecipeRepository):
    def __init__(self,connection: INoSqlDBConnection) -> None:
        self.connection = connection.get_db_connection()
        self.collection_name = "Recipe"