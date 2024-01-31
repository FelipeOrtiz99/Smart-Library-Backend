from fastapi import APIRouter, Depends, HTTPException,Response
from app.db.database import get_connection, close_connection
from app.models.user_model import User
from fastapi.security import OAuth2PasswordBearer
from app.utils import bearer

router = APIRouter()

@router.get("/get", response_model=list[User])
async def get_user(
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)
):
    connection, cursor = conn
    try:
        cursor.execute("SELECT Id as id, Type as type, Name as name, LastName as last_name, Email as email, Password as password, Age as age, Active as active FROM [User]")
        users = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)


@router.get("/get/{id_user}", response_model=User)
async def get_user_id(user_id: int, conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("SELECT Id as id, Type as type, Name as name, LastName as last_name, Email as email, Password as password, Age as age, Active as active FROM [User] WHERE Id = ?", user_id)
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return User(**dict(zip([column[0] for column in cursor.description], user)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.post("/create")
async def create_user(user: User, conn = Depends(get_connection)):
    connection,cursor = conn
    try:
        cursor.execute("INSERT INTO User (Type, Name, LastName As last_name, Email, Password, Age, Active) VALUES (?,?,?,?,?,?,?)", user.type, user.name, user.last_name, user.email, user.password, user.age, user.active)
        connection.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)

@router.put("/update/{id_user}/")
async def update_user(id_user: int, user: User, conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("UPDATE [User] SET Type = ?, Name = ?, LastName = ?, Email = ?, Password = ?, Age = ?, Active = ? WHERE Id = ?", user.type, user.name, user.last_name, user.email, user.password, user.age, user.active,id_user)
        connection.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)


@router.delete("/delete/{id_user}/")
async def delete_user(id_user: int, conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("DELETE FROM [User] WHERE Id = ?", id_user)
        connection.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)
