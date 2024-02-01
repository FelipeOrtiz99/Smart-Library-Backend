from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.database import get_connection, close_connection
from app.models.book_model import Book
from app.utils import bearer

router = APIRouter()

@router.get("/get/", response_model=list[Book])
async def get_books(
    skip: int = Query(0, alias="offset", ge=0),
    limit: int = Query(10, le=100),
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)
):
    connection, cursor = conn
    try:
        query = "SELECT ISBN As isbn, BookTitle As book_title, BookAuthor As book_author, YearOfPublication As year_publication, Publisher as publisher, ImageURLS As url_s, ImageURLM As url_m, ImageURLL as url_l FROM Book ORDER BY ISBN OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, skip, limit)
        books = cursor.fetchall()
        list_books = [dict(zip([column[0] for column in cursor.description], row)) for row in books]
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.get("/get/{isbn}", response_model=Book)
async def get_book_isbn(
    isbn: str, 
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)
):
    connection, cursor = conn
    try:
        cursor.execute("SELECT ISBN As isbn, BookTitle As book_title, BookAuthor As book_author, YearOfPublication As year_publication, Publisher as publisher, ImageURLS As url_s, ImageURLM As url_m, ImageURLL as url_l FROM Book WHERE ISBN = ?", isbn)
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Book not found")

        return Book(**dict(zip([column[0] for column in cursor.description], user)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.post("/create")
async def create_user(
    book: Book, 
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)):
    connection,cursor = conn
    try:
        cursor.execute("INSERT INTO User (ISBN, BookTitle, BookAuthor, YearOfPublication, Publisher, ImageURLS, ImageURLM, ImageURLL) VALUES (?,?,?,?,?,?,?,?)", book.isbn, book.book_title, book.book_author, book.year_publication, book.publisher, book.url_s, book.url_m, book.url_l)
        connection.commit()
        return {"message": "Book created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection,cursor)

@router.put("/update/{isbn}/")
async def update_book(
    isbn: str, 
    book: Book, 
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("UPDATE [Book] SET BookTitle = ?, BookAuthor = ?, YearOfPublication = ?, Publisher = ?, ImageURLS = ?, ImageURLM = ?, ImageURLL = ? WHERE ISBN = ?", book.book_title, book.book_author, book.year_publication, book.publisher, book.url_s, book.url_m, book.url_l, isbn)
        connection.commit()
        return {"message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)


@router.delete("/delete/{isbn}/")
async def delete_isbn(
    isbn: str, 
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        cursor.execute("DELETE FROM [Book] WHERE ISBN = ?", isbn)
        connection.commit()
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.post("/get/book/search/title", response_model=list[Book])
async def search_title(
    title: str,
    skip: int = Query(0, alias="offset", ge=0),
    limit: int = Query(10, le=100),
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)):
    connection, cursor = conn
    try:
        query = "Select * FROM Book WHERE BookTitle Like '%?%' ORDER BY ISBN OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, skip, limit)
        books = cursor.fetchall()
        list_books = [dict(zip([column[0] for column in cursor.description], row)) for row in books]
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.post("/get/book/search/author", response_model=list[Book])
async def search_title(
    author: str,
    skip: int = Query(0, alias="offset", ge=0),
    limit: int = Query(10, le=100),
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)
):
    connection, cursor = conn
    try:
        query = "Select * FROM Book WHERE BookAuthor Like '%?%' ORDER BY ISBN OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, skip, limit)
        books = cursor.fetchall()
        list_books = [dict(zip([column[0] for column in cursor.description], row)) for row in books]
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)

@router.get("/get/book/raiting")
async def get_raiting(
    isbn: str, 
    current_user: dict = Depends(bearer.decode_jwt_token),
    conn = Depends(get_connection)
):
    connection, cursor = conn
    try:
        cursor.execute("Select AVG(BookRating) As Raiting from Rating Where ISBN = ?", isbn)
        raiting = cursor.fetchone["Raiting"]
        return raiting
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(connection, cursor)