from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from src.interfaces.repository import IRepository
from src.models.chef import Chef, ResponseChef


class ChefService:
    def __init__(
        self,
        chef_repository: IRepository,
    ) -> None:
        self.password_hash = PasswordHash.recommended()
        self.chef_repository = chef_repository

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    async def check_authentication(
        self, form_data: OAuth2PasswordRequestForm
    ):
        chef = await self.chef_repository.get(email=form_data.username)
        if not chef or not self.verify_password(
            form_data.password, chef["password_hash"]
        ):
            raise HTTPException(
                detail="Incorrect username or password!",
                status_code=HTTPStatus.FORBIDDEN,
            )

    def verify_password(self, password, hash) -> bool:
        return self.password_hash.verify(password, hash)

    async def _verify_credentials(self, chef_name: str, email: str):
        conflicting_chef = await self.chef_repository.get(
            chef_name=chef_name, email=email
        )
        if conflicting_chef:
            if conflicting_chef["chef_name"] == chef_name:
                raise HTTPException(
                    detail="This name already exists!",
                    status_code=HTTPStatus.CONFLICT,
                )
            elif conflicting_chef["email"] == email:
                raise HTTPException(
                    detail="This email already exists!",
                    status_code=HTTPStatus.CONFLICT,
                )

    @staticmethod
    def check_authorization(chef_id, authenticated_chef_id):
        if chef_id != authenticated_chef_id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="unauthorized request",
            )

    async def get_all_the_chefs(self, offset, limit):
        chefs = await self.chef_repository.get_all(offset, limit)
        return chefs

    async def get_chef(self, id: int):
        chef = await self.chef_repository.get(id=id)
        return chef

    async def add_chef(self, chef: Chef):
        await self._verify_credentials(
            chef_name=chef.chef_name, email=chef.email
        )
        await self.chef_repository.add((
            chef.chef_name,
            chef.email,
            self.hash(chef.password),
        ))
        chef = await self.chef_repository.get(
            chef_name=chef.chef_name, email=chef.email
        )
        return chef

    async def delete_chef(self, chef_id, current_chef):
        self.check_authorization(chef_id, current_chef["chef_id"])
        await self.chef_repository.delete(current_chef["chef_id"])
        return {"message": "Chef successfully excluded"}

    async def update_chef(
        self, updated_chef: Chef, chef_id, current_chef
    ) -> ResponseChef:
        self.check_authorization(chef_id, current_chef["chef_id"])
        await self._verify_credentials(
            updated_chef.chef_name, updated_chef.email
        )
        await self.chef_repository.update((
            updated_chef.chef_name,
            updated_chef.email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.hash(updated_chef.password),
            current_chef["chef_id"],
        ))
        updated_chef = await self.chef_repository.get(
            chef_name=updated_chef.chef_name, email=updated_chef.email
        )
        return updated_chef
