from http import HTTPStatus
from datetime import datetime,timezone,timedelta
import os
from src.interfaces.repository import IRepository
from pwdlib import PasswordHash
from src.models.chef import Chef
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)
from fastapi import HTTPException
import jwt


class ChefSecurityService:

    def __init__(self,chef_repository:IRepository) -> None:
        self.chef_repository = chef_repository
        self.password_hash = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="chefs/auth")

    def hash(self,password: str) -> str:
        return self.password_hash.hash(password)
    
    def verify_password(self,password, hash) -> bool:
        return self.password_hash.verify(password, hash)
    
    async def _verify_credentials(self,chef_name:str,email:str):
        conflicting_chef = await self.chef_repository.get(
            chef_name = chef_name,
            email = email
        )
        if conflicting_chef:
            if conflicting_chef["chef_name"] == chef_name:
                raise HTTPException(
                    detail = "This name already exists!",
                    status_code = HTTPStatus.CONFLICT
                )
            elif conflicting_chef["email"] == email:
                raise HTTPException(
                    detail = "This email already exists!",
                    status_code = HTTPStatus.CONFLICT
                )
    
    def check_authorization(self,chef_id,authenticated_chef_id):
        if chef_id != authenticated_chef_id:
            raise HTTPException(
                status_code = HTTPStatus.UNAUTHORIZED,
                detail = "unauthorized request"
            )
    
    async def check_authentication(self,form_data:OAuth2PasswordRequestForm):
        chef = await self.chef_repository.get(email=form_data.username)
        if not chef or not self.verify_password(form_data.password,chef["password_hash"]):
            raise HTTPException(
                detail = "Incorrect username or password!",
                status_code = HTTPStatus.FORBIDDEN
            )
        
    async def create_access_token(self,form_data:OAuth2PasswordRequestForm):
        await self.check_authentication(form_data)
        to_encode = {"sub":form_data.username}
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM")
        )
        return encoded_jwt

class ChefService:

    def __init__(
        self,
        chef_repository:IRepository,
        chef_sec_service:ChefSecurityService
    ) -> None:
        self.chef_repository = chef_repository
        self.chef_sec_service = chef_sec_service
    
    async def get_all_the_chefs(self):
        chefs = await self.chef_repository.get_all()
        return chefs

    async def add_chef(self,chef:Chef):
        await self.chef_sec_service._verify_credentials(
            chef_name = chef.chef_name,
            email = chef.email
        )
        await self.chef_repository.add(
            (
                chef.chef_name,
                chef.email,
                self.chef_sec_service.hash(chef.password)
            )
        )
        chef = await self.chef_repository.get(
            chef_name = chef.chef_name,
            email = chef.email
        )
        return chef

