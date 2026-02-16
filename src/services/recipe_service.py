from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from src.interfaces.repository import IRecipeRepository
from src.models.recipe import Recipe, ResponseRecipe


class RecipeService:
    def __init__(self, recipe_repository: IRecipeRepository) -> None:
        self.recipe_repository = recipe_repository

    async def get_recipes(self, offset: int, limit: int):
        recipes = await self.recipe_repository.get_all(offset, limit)
        return recipes

    async def get_recipe(self, id: str):
        recipe = await self.recipe_repository.get(id)
        if not recipe:
            raise HTTPException(
                detail="recipe not found", status_code=HTTPStatus.NOT_FOUND
            )
        return recipe
            
    async def get_my_recipes(
        self, current_chef_id: str, offset: int, limit: int
    ):
        recipes = await self.recipe_repository.get_recipes_from_chef(
            current_chef_id, offset, limit
        )
        return recipes

    async def add_recipe(self, recipe: Recipe, current_chef_id: str):
        iserted_id = await self.recipe_repository.add(recipe, current_chef_id)
        return ResponseRecipe(
            **recipe.model_dump(),
            recipe_id=str(iserted_id),
            chef_id=current_chef_id,
            posted_at=datetime.now(),
            updated_at=datetime.now(),
        )

    async def verify_authorization(
        self, current_chef_id: str, recipe_id: str
    ):
        recipe = await self.recipe_repository.get(recipe_id)
        if not recipe:
            raise HTTPException(
                detail="recipe not found", status_code=HTTPStatus.NOT_FOUND
            )
        if recipe["chef_id"] != current_chef_id:
            raise HTTPException(
                detail="unauthorized request",
                status_code=HTTPStatus.UNAUTHORIZED,
            )

    async def delete_recipe(self, current_chef_id: str, recipe_id: str):
        await self.verify_authorization(current_chef_id, recipe_id)
        await self.recipe_repository.delete(recipe_id)
        return {"message": "Recipe successfully excluded"}

    async def update_recipe(
        self, current_chef_id: str, recipe_id: str, recipe: Recipe
    ):
        await self.verify_authorization(current_chef_id, recipe_id)
        await self.recipe_repository.update(recipe_id, recipe)
        return {"message": "Recipe successfully updated"}
