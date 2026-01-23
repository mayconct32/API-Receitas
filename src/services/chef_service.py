from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.interfaces.repository import IChefrepository
from src.models.chef import Chef, ResponseChef
from src.utils import verify_password


class ChefService:
    def __init__(self, chef_repository: IChefrepository) -> None:
        self.chef_repository = chef_repository

    async def check_authentication(
        self, form_data: OAuth2PasswordRequestForm
    ):
        chef = await self.chef_repository.get_by_email(
            email=form_data.username
        )
        if not chef or not verify_password(
            form_data.password, chef["password_hash"]
        ):
            raise HTTPException(
                detail="Incorrect username or password!",
                status_code=HTTPStatus.FORBIDDEN,
            )

    async def _verify_credentials(self, chef_name: str, email: str):
        conflicting_name = await self.chef_repository.get_by_chef_name(
            chef_name=chef_name
        )
        if conflicting_name:
            raise HTTPException(
                detail="This name already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
        else:
            conflicting_email = await self.chef_repository.get_by_email(
                email=email
            )
            if conflicting_email:
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
        await self.chef_repository.add(chef)
        chef = await self.chef_repository.get_by_email(email=chef.email)
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
        await self.chef_repository.update(
            updated_chef, current_chef["chef_id"]
        )
        updated_chef = await self.chef_repository.get_by_email(
            email=updated_chef.email
        )
        return updated_chef
