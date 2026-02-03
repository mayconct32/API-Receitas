from src.interfaces.repository import IRecipeRepository
from bson.errors import InvalidId
from src.models.recipe import Recipe, ResponseRecipe
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus


class RecipeService:
    def __init__(self,recipe_repository: IRecipeRepository) -> None:
        self.recipe_repository = recipe_repository

    async def get_recipes(self, offset: int, limit: int):
        recipes = await self.recipe_repository.get_all(offset, limit)
        if recipes:
            for c in recipes:
                c["_id"] = str(c["_id"])
        return recipes
    
    async def get_recipe(self, id: str):
        try:
            recipe = await self.recipe_repository.get(id)
        except InvalidId:
            return None
        else:
            if recipe:
                recipe["_id"] = str(recipe["_id"])
            return recipe
    
    async def get_my_recipes(self,current_chef_id: str, offset: int, limit: int):
        recipes = await self.recipe_repository.get_recipes_from_chef(current_chef_id, offset, limit)
        if recipes:
            for c in recipes:
                c["_id"] = str(c["_id"])
        return recipes

    async def add_recipe(self, recipe: Recipe, current_chef_id: str) -> ResponseRecipe:
        iserted_id = await self.recipe_repository.add(recipe, current_chef_id)
        return ResponseRecipe(
            recipe_id = iserted_id,
            chef_id = current_chef_id,
            **recipe.model_dump(),
            posted_at = datetime,
            updated_at = datetime
        )
    
    async def verify_authorization(self, current_chef_id: str, recipe_id: str):
        recipe = await self.recipe_repository.get(recipe_id)
        if recipe["chef_id"] != current_chef_id:
            raise HTTPException(
                detail="unauthorized request",
                status_code=HTTPStatus.UNAUTHORIZED
            )

    async def delete_recipe(self, current_chef_id: str, recipe_id: str):
        await self.verify_authorization(current_chef_id, recipe_id)
        await self.recipe_repository.delete(recipe_id)
        return {"message": "Recipe successfully excluded"}



