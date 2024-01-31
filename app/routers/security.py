from fastapi import APIRouter, Depends, HTTPException,Response
from db.database import get_connection, close_connection
from models.security_model import UserLogin, UserLoginResponse
from models.user_model import User
from utils import bearer

router = APIRouter()

@router.post("/login", response_model=User)
async def login(user: UserLogin, conn = Depends(get_connection)):
    connection,cursor = conn
    try:
        input_form = user.password
        cursor.execute("SELECT Id,Type, Name, LastName As last_name, Email, Password, Age, Active FROM User WHERE Email = ?", user.email)
        userdb = cursor.fetchone()
        user_password = user.password
        if not userdb or input_form != user_password:
            raise HTTPException(status_code=404, detail="email/password doesnt match")
        
        return userdb

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)

@router.post("/get/token", response_model=UserLoginResponse)
async def get_token(user: UserLogin):
    token = bearer.create_jwt_token(user, 120)
    return token

