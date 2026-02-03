from src.interfaces.repository import IRecipeRepository
from bson.errors import InvalidId

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

