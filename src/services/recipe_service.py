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

    async def add_recipe(self, recipe: CompleteRecipe, current_chef_id: int):
        await self.recipe_repository.add(
            ChefRecipe(
                recipe_name = recipe.recipe_name,
                description = recipe.description,
                prep_time = recipe.prep_time,
                chef_id = current_chef_id
            )
        )
        last_insert_id = await self.recipe_repository.select_last_insert_id()

        for instruction in recipe.instructions:
            await self.recipe_repository.add_recipe_instruction(
                RecipeInstruction(
                    step_number = instruction.step_number,
                    description = instruction.description,
                    recipe_id = last_insert_id
                )
            )
            
        for ingredient in recipe.ingredients:
            await self.recipe_repository.add_recipe_ingredient(
                RecipeIngredient(
                    ingredient_name = ingredient.ingredient_name,
                    quantity = ingredient.quantity,
                    recipe_id = last_insert_id
                )
            )
        return "teste123"