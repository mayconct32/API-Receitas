from http import HTTPStatus
from src.interfaces.repository import IRepository
from fastapi import HTTPException

class ChefService:

    def __init__(self,chef_repository:IRepository) -> None:
        self.chef_repository = chef_repository
    
    async def verify_credentials(self,chef_name:str,email:str):
        conflicting_chef = await self.chef_repository.get(
            chef_name = chef_name,
            email = email
        )
        if conflicting_chef:
            if conflicting_chef[""] == chef_name:
                raise HTTPException(
                    detail = "This name already exists!",
                    status_code = HTTPStatus.CONFLICT
                )
            elif conflicting_chef["email"] == email:
                raise HTTPException(
                    detail = "This email already exists!",
                    status_code = HTTPStatus.CONFLICT
                )
    
    async def get_all_the_chefs(self):
        chefs = await self.chef_repository.get_all()
        return chefs