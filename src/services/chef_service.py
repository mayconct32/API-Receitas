from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from src.interfaces.repository import IRepository
from src.models.chef import Chef, ResponseChef
import os
from jwt import encode,decode,InvalidTokenError


class ChefSecurityService:
    def __init__(self, chef_repository: IRepository) -> None:
        self.chef_repository = chef_repository
        self.password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)
    
    async def check_authentication(self, form_data: OAuth2PasswordRequestForm):
        chef = await self.chef_repository.get(email=form_data.username)
        if not chef or not self.verify_password(
            form_data.password, chef["password_hash"]
        ):
            raise HTTPException(
                detail="Incorrect username or password!",
                status_code=HTTPStatus.FORBIDDEN,
            )

    def verify_password(self, password, hash) -> bool:
        return self.password_hash.verify(password, hash)

    async def _verify_credentials(self, chef_name: str, email: str):
        conflicting_chef = await self.chef_repository.get(
            chef_name=chef_name, email=email
        )
        if conflicting_chef:
            if conflicting_chef["chef_name"] == chef_name:
                raise HTTPException(
                    detail="This name already exists!",
                    status_code=HTTPStatus.CONFLICT,
                )
            elif conflicting_chef["email"] == email:
                raise HTTPException(
                    detail="This email already exists!",
                    status_code=HTTPStatus.CONFLICT,
                )

    def check_authorization(self, chef_id, authenticated_chef_id):
        if chef_id != authenticated_chef_id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="unauthorized request",
            )
        
    async def create_access_token(self, form_data: OAuth2PasswordRequestForm):
        await self.check_authentication(form_data)
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
    

    async def get_current_user(self, token: str) -> dict:
        credentials_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload:dict = decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")])
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        chef = await self.chef_repository.get(email=email)
        if chef is None:
            raise credentials_exception
        return chef
        

class ChefService:
    def __init__(
        self,
        chef_repository: IRepository,
    ) -> None:
        self.chef_repository = chef_repository
        self.chef_sec_service = ChefSecurityService(chef_repository)

    async def get_all_the_chefs(self, offset, limit):
        chefs = await self.chef_repository.get_all(offset, limit)
        return chefs

    async def get_chef(self, id: int):
        chef = await self.chef_repository.get(id=id)
        return chef

    async def add_chef(self, chef: Chef):
        await self.chef_sec_service._verify_credentials(
            chef_name=chef.chef_name, email=chef.email
        )
        await self.chef_repository.add((
            chef.chef_name,
            chef.email,
            self.chef_sec_service.hash(chef.password),
        ))
        chef = await self.chef_repository.get(
            chef_name=chef.chef_name, email=chef.email
        )
        return chef

    async def delete_chef(self, chef_id, current_chef):
        self.chef_sec_service.check_authorization(
            chef_id, current_chef["chef_id"]
        )
        await self.chef_repository.delete(current_chef["chef_id"])
        return {"message": "Chef successfully excluded"}

    async def update_chef(
        self, updated_chef: Chef, chef_id, current_chef
    ) -> ResponseChef:
        self.chef_sec_service.check_authorization(
            chef_id, current_chef["chef_id"]
        )
        await self.chef_sec_service._verify_credentials(
            updated_chef.chef_name, updated_chef.email
        )
        await self.chef_repository.update((
            updated_chef.chef_name,
            updated_chef.email,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.chef_sec_service.hash(updated_chef.password),
            current_chef["chef_id"],
        ))
        updated_chef = await self.chef_repository.get(
            chef_name=updated_chef.chef_name, email=updated_chef.email
        )
        return updated_chef
