from src.interfaces.connection_db import INoSqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    Recipe,
    ResponseRecipe
)
from typing import List
from datetime import datetime
from uuid import uuid4

class RecipeRepository(IRecipeRepository):
    def __init__(self,connection: INoSqlDBConnection) -> None:
        self.connection = connection.get_db_connection()
        self.collection_name = "Recipe"
    
    async def get_all(self, offset: int, limit: int) -> List[ResponseRecipe]:
        collection = self.connection.get_collection(self.collection_name)
        cursor = collection.find().limit(limit).skip(offset)
        recipes = [recipe async for recipe in cursor]
        return recipes
    
    async def get(self, id: str):
        collection = self.connection.get_collection(self.collection_name)
        recipe = await collection.find_one({"recipe_id": id})
        return recipe
    
    async def get_recipes_from_chef(self, current_chef_id: str, offset: int, limit: int):
        collection = self.connection.get_collection(self.collection_name)
        cursor = collection.find({"chef_id": current_chef_id}).limit(limit).skip(offset)
        recipes = [recipe async for recipe in cursor]
        return recipes

    async def add(self, recipe: Recipe, current_chef_id: str):
        collection = self.connection.get_collection(self.collection_name)
        unique_id = uuid4()
        db_recipe = {
            "recipe_id": str(unique_id),
            "chef_id": current_chef_id,
            **recipe.model_dump(),
            "posted_at": datetime.now(),
            "updated_at": datetime.now()
        }
        await collection.insert_one(db_recipe)
        return unique_id

    async def delete(self, recipe_id: str):
        collection = self.connection.get_collection(self.collection_name)
        await collection.delete_one({"recipe_id": recipe_id})

    async def update(self, recipe_id: str, recipe: Recipe):
        collection = self.connection.get_collection(self.collection_name)
        await collection.update_one({"recipe_id": recipe_id},{"$set": recipe.model_dump()})




    