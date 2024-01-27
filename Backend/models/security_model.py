from pydantic import BaseModel
from models.user_model import User

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    token: str
    user: User