from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.database import MysqlConnectionDB
from src.repositories.chef_repository import ChefRepository
from src.services.auth_service import AuthService
from src.services.chef_service import ChefService


class ChefDependencies:
    _chef_repository = ChefRepository(MysqlConnectionDB())
    chef_service = ChefService(_chef_repository)
    auth_service = AuthService(_chef_repository)

    @classmethod
    def get_chef_service(cls) -> ChefService:
        return cls.chef_service

    @classmethod
    async def get_current_chef(
        cls, token: str = Depends(OAuth2PasswordBearer(tokenUrl="chefs/auth"))
    ) -> dict:
        return await cls.auth_service.decode_token(token)

    @classmethod
    async def get_auth_service(cls):
        return cls.auth_service
