from pydantic import BaseModel
from models.user_model import User

class UserLoginResponse(BaseModel):
    token: str
    user: User

class UserLogin(BaseModel):
    email: str
    password: str