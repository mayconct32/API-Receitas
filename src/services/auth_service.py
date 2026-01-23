import os
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError, decode, encode

from src.interfaces.repository import IChefrepository


class AuthService:
    def __init__(self, chef_repository: IChefrepository) -> None:
        self.chef_repository = chef_repository

    @staticmethod
    async def create_access_token(form_data: OAuth2PasswordRequestForm):
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
        credentials_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        chef = await self.chef_repository.get_by_email(email=email)
        if not chef:
            raise credentials_exception
        return chef
