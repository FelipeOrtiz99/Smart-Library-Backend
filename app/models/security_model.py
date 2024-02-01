from pydantic import BaseModel, ValidationError
from typing import Union, Optional
from datetime import datetime
from app.models.user_model import User

class UserLoginResponse(BaseModel):
    token: str
    name: str
    last_name: Union[None,str]
    username: str
    age: Union[None, int]
    type_user: int
    active: bool

class UserLogin(BaseModel):
    email: str
    password: str

class UserToken(BaseModel):
    username: str

class Token(BaseModel):
    access_token:str
    token_type: str = "bearer"
