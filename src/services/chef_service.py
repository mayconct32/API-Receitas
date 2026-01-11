from http import HTTPStatus
from datetime import datetime
from src.interfaces.repository import IRepository
from pwdlib import PasswordHash
from fastapi import HTTPException
from src.models.chef import Chef


class ChefService:

    def __init__(self,chef_repository:IRepository) -> None:
        self.password_hash = PasswordHash.recommended()
        self.chef_repository = chef_repository
    
    def hash(self,password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self,password, hash) -> bool:
        return self.password_hash.verify(password, hash)
    
    async def _verify_credentials(self,chef_name:str,email:str):
        conflicting_chef = await self.chef_repository.get(
            chef_name = chef_name,
            email = email
        )
        if conflicting_chef:
            if conflicting_chef["chef_name"] == chef_name:
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

    async def add_chef(self,chef:Chef):
        await self._verify_credentials(
            chef_name = chef.chef_name,
            email = chef.email
        )
        await self.chef_repository.add(
            (
                chef.chef_name,
                chef.email,
                self.hash(chef.password),
                datetime.now(),
                datetime.now()
            )
        )
        chef = await self.chef_repository.get(
            chef_name = chef.chef_name,
            email = chef.email
        )
        return chef

