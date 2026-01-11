from src.services.chef_service import ChefService
from src.repositories.chef_repository import ChefRepository
from src.database import MysqlConnectionDB


def get_chef_service() -> ChefService:
    return ChefService(
        ChefRepository(
            MysqlConnectionDB()
        )
    )