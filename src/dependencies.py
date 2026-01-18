from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.database import MysqlConnectionDB
from src.repositories.chef_repository import ChefRepository
from src.services.chef_service import ChefService


class ChefDependencies:
    chef_service = ChefService(ChefRepository(MysqlConnectionDB()))

    @classmethod
    def get_chef_service(cls) -> ChefService:
        return cls.chef_service

    @classmethod
    async def get_auth_service(
        cls, token: str = Depends(OAuth2PasswordBearer(tokenUrl="chefs/auth"))
    ) -> dict:
        return await cls.chef_service.get_current_user(token)
