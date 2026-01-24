from pydantic import BaseModel
from typing import List
from datetime import datetime


class Instruction(BaseModel):
    step_number: int
    description: str


class Ingredient(BaseModel):
    ingredient_name: str
    quantity: str


class Recipe(BaseModel):
    recipe_name: str
    description: str
    prep_time: str
    instructions:  List[Instruction]
    ingredients: List[Ingredient]

class ResponseRecipe(Recipe):
    recipe_id: int
    chef_id: int
    posted_at: datetime
    updated_at: datetime
