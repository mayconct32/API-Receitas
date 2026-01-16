from datetime import datetime
from pydantic import BaseModel, EmailStr


class Chef(BaseModel):
    chef_name: str
    email: EmailStr
    password: str


class ResponseChef(BaseModel):
    chef_id: int
    chef_name: str
    email: EmailStr
    create_at: datetime
    updated_at: datetime
