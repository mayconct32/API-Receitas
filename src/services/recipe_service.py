from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    CompleteRecipe,
    ChefRecipe,
    RecipeInstruction,
    RecipeIngredient
)


class RecipeService:
    def __init__(self,recipe_repository: IRecipeRepository) -> None:
        self.recipe_repository = recipe_repository

    async def get_recipes(self, offset: int, limit: int):
        recipes = await self.recipe_repository.get_all(offset, limit)
        if recipes:
            for c in recipes:
                c["_id"] = str(c["_id"])
        return recipes
