from src.database import MongoDBConnection
from src.interfaces.connection_db import INoSqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    Recipe,
    ResponseRecipe
)
from typing import List
from bson import ObjectId
from datetime import datetime

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
        recipe = await collection.find_one({"_id": ObjectId(id)})
        return recipe
    
    async def get_recipes_from_chef(self, current_chef_id: str, offset: int, limit: int):
        collection = self.connection.get_collection(self.collection_name)
        cursor = collection.find({"chef_id": current_chef_id}).limit(limit).skip(offset)
        recipes = [recipe async for recipe in cursor]
        return recipes

    async def add(self, recipe: Recipe, current_chef_id: str):
        collection = self.connection.get_collection(self.collection_name)
        db_recipe = {
            "chef_id": current_chef_id,
            **recipe.model_dump(),
            "posted_at": datetime,
            "updated_at": datetime
        }
        result = await collection.insert_one(db_recipe)
        return result.inserted_id

    async def delete(self, recipe_id: str):
        collection = self.connection.get_collection(self.collection_name)
        await collection.delete_one({"_id": ObjectId(recipe_id)})





    