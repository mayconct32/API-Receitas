from src.services.chef_service import ChefService
from src.repositories.chef_repository import ChefRepository


def get_chef_service() -> ChefService:
    return ChefService(ChefRepository)