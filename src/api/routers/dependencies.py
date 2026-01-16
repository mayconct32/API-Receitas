from src.database import MysqlConnectionDB
from src.repositories.chef_repository import ChefRepository
from src.services.chef_service import ChefSecurityService, ChefService


chef_repository = ChefRepository(MysqlConnectionDB())

chef_sec_service = ChefSecurityService(chef_repository)


def get_chef_service() -> ChefService:
    return ChefService(chef_repository, chef_sec_service)


def get_chef_sec_service() -> ChefSecurityService:
    return ChefSecurityService(chef_repository)
