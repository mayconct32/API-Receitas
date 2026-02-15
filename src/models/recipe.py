from datetime import datetime
from typing import List

from pydantic import BaseModel


class Instruction(BaseModel):
    step_number: int
    description: str


class Ingredient(BaseModel):
    ingredient_name: str
    quantity: str


class Recipe(BaseModel):
    recipe_name: str
    description: str
    prep_time: str  # "11:12:00"
    instructions: List[Instruction]
    ingredients: List[Ingredient]


class DBRecipe(BaseModel):
    recipe_id: str
    chef_id: int
    posted_at: datetime
    updated_at: datetime


class ResponseRecipe(Recipe, DBRecipe): ...
