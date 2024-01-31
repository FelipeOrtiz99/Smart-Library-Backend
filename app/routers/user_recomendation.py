from fastapi import APIRouter, Depends, HTTPException, Query
from db.database import get_connection, close_connection
from models.user_recomendation_model import UserRecomendation
from models.book_model import Book

router = APIRouter()

@router.post("/get/", response_model=list[Book])
async def get_user_recomendation(recomendation : UserRecomendation,conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("EXEC dbo.Recomendation_Books_Month ?, ?", recomendation.user_id, recomendation.date)
        books = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)
