import os
from datetime import datetime, timedelta, timezone

from jwt import InvalidTokenError, decode, encode

from src.interfaces.repository import IChefRepository
from src.repositories.redis_repository import RedisRepository
from src.models.auth import FormData
from src.exceptions.chef_exceptions import CredentialsError


class AuthService:
    def __init__(self, chef_repository: IChefRepository, redis_repository: RedisRepository) -> None:
        self.chef_repository = chef_repository
        self.redis_repository = redis_repository

    @staticmethod
    async def create_access_token(form_data: FormData):
        to_encode = {"sub": form_data.username}
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        to_encode.update({"exp": expire})
        encoded_jwt = encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM"),
        )
        return encoded_jwt

    async def decode_token(self, token: str) -> dict:
        try:
            payload: dict = decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )
            email = payload.get("sub")
            if email is None:
                raise CredentialsError("Could not validate credentials")
        except InvalidTokenError:
            raise CredentialsError("Could not validate credentials")
        cache = await self.redis_repository.get(f"chef:{email}")
        if cache:
            return cache
        else:
            chef = await self.chef_repository.get_by_email(email=email)
            if not chef:
                raise CredentialsError("Could not validate credentials")
            await self.redis_repository.insert(f"chef:{email}",chef)
            return chef