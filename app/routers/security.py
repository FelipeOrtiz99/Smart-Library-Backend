from fastapi import APIRouter, Depends, HTTPException,Response
from app.db.database import get_connection, close_connection
from app.models.security_model import UserLogin, UserLoginResponse, UserToken, Token
from app.models.user_model import User
from app.utils import bearer
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin, conn = Depends(get_connection)):
    connection,cursor = conn
    try:
        input_form = user.password
        cursor.execute("SELECT Type as type_user, Password as password,Name as name, LastName As last_name, Email as username, Password, Age as age, Active as active FROM [User] WHERE Email = ?", user.email)
        userdb = cursor.fetchone()
        user_password = userdb.password
        if not userdb or input_form != user_password:
            raise HTTPException(status_code=404, detail="email/password doesnt match")
        user_token = await get_token({"username": userdb.username})        
        response_login = {"token": user_token['access_token'],"name": userdb.name, "last_name": userdb.last_name, "username": userdb.username, "age": userdb.age, "type_user": userdb.type_user,"active" : userdb.active}
        return response_login

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)



async def get_token(user: dict):
    token = bearer.create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}

