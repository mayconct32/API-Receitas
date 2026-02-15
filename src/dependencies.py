from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database import MongoDBConnection, MysqlDBConnection
from src.interfaces.connection_db import INoSqlDBConnection, ISqlDBConnection
from src.interfaces.repository import IRepository
from src.repositories.chef_repository import ChefRepository
from src.repositories.recipe_repository import RecipeRepository
from src.services.auth_service import AuthService
from src.services.chef_service import ChefService
from src.services.recipe_service import RecipeService


def get_mysql_connection() -> ISqlDBConnection:
    return MysqlDBConnection()


def get_mongodb_connection() -> INoSqlDBConnection:
    return MongoDBConnection()


# Chef Dependecies
def get_chef_repository(
    connection: ISqlDBConnection = Depends(get_mysql_connection),
) -> IRepository:
    return ChefRepository(connection)


def get_chef_service(
    repository: IRepository = Depends(get_chef_repository),
) -> ChefService:
    return ChefService(repository)


def get_auth_service(
    repository: IRepository = Depends(get_chef_repository),
) -> AuthService:
    return AuthService(repository)


async def get_current_chef(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="chefs/auth")),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    return await auth_service.decode_token(token)


# Recipes Dependencies
def get_recipe_repository(
    connection: INoSqlDBConnection = Depends(get_mongodb_connection),
) -> IRepository:
    return RecipeRepository(connection)


def get_recipe_service(
    repository: IRepository = Depends(get_recipe_repository),
) -> RecipeService:
    return RecipeService(repository)


ChefServiceDep = Annotated[ChefService, Depends(get_chef_service)]

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

CurrentChef = Annotated[dict, Depends(get_current_chef)]

AuthRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]

RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]
