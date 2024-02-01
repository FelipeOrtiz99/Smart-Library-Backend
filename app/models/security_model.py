from pydantic import BaseModel, ValidationError
from typing import Union, Optional
from datetime import datetime
from app.models.user_model import User

class Token(BaseModel):
    access_token:str
    token_type: str = "bearer"
    expire_date : datetime

class UserLoginResponse(BaseModel):
    token: Token
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
