from pydantic import BaseModel
from typing import List
from datetime import datetime


class Instruction(BaseModel):
    step_number: int
    description: str


class RecipeInstruction(Instruction):
    recipe_id: int


class Ingredient(BaseModel):
    ingredient_name: str
    quantity: str


class RecipeIngredient(Ingredient):
    recipe_id: int


class Recipe(BaseModel):
    recipe_name: str
    description: str
    prep_time: str # "11:12:00"


class ChefRecipe(Recipe):
    chef_id: int


class CompleteRecipe(Recipe):
    instructions:  List[Instruction]
    ingredients: List[Ingredient]


class ResponseRecipe(Recipe):
    recipe_id: int
    chef_id: int
    posted_at: datetime
    updated_at: datetime
