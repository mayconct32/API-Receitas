from src.database import ISqlDBConnection
from src.interfaces.connection_db import ISqlDBConnection
from src.interfaces.repository import IRecipeRepository
from src.models.recipe import (
    Recipe,
    ChefRecipe,
    RecipeInstruction,
    RecipeIngredient
)
from typing import List


class RecipeRepository(IRecipeRepository):
    def __init__(self,connection: ISqlDBConnection) -> None:
        self.connection = connection
    
    def get_all(self, offset: int, limit: int) -> List[Recipe]:
        ...

    def get(self, id: int) -> Recipe:
        ...

    async def add(self, data: ChefRecipe) -> None:
        await self.connection.execute(
            """
            INSERT INTO recipe(
                recipe_name,
                description,
                prep_time,
                chef_id
            ) 
            VALUES (%s,%s,%s,%s)
        """,
            (
                data.recipe_name,
                data.description,
                data.prep_time,
                data.chef_id
            )
        )

    async def add_recipe_instruction(self,data: RecipeInstruction) -> None:
        await self.connection.execute(
            """
            INSERT INTO instruction(
                step_number,
                description,
                recipe_id
            )
            VALUES (%s,%s,%s)
        """,
            (
                data.step_number,
                data.description,
                data.recipe_id
            )
        )
    
    async def add_recipe_ingredient(self,data: RecipeIngredient) -> None:
        await self.connection.execute(
            """
            INSERT INTO ingredient(
                ingredient_name,
                quantity,
                recipe_id
            )
            VALUES (%s,%s,%s)
        """,
            (
                data.ingredient_name,
                data.quantity,
                data.recipe_id
            )
        )

    async def select_last_insert_id(self):
        last_insert_id = await self.connection.execute(
            """
            SELECT LAST_INSERT_ID();
        """
        )
        return last_insert_id[0]["LAST_INSERT_ID()"]


    def delete(self, id: int) -> None:
        ...

    def update(self, id: int, data: Recipe) -> None:
        ...
