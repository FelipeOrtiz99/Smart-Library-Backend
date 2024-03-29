from decimal import Decimal
from typing import Union,Optional
from pydantic import BaseModel as PydanticBaseModel, validator
from pydantic import BaseModel

class Book(BaseModel):
    isbn: str
    book_title: str
    book_author: str
    year_publication: int
    publisher: str
    url_s: Union[None, str]
    url_m: Union[None, str]
    url_l: Union[None, str]


class Rating_User(BaseModel):
    id_rating:int
    isbn: str
    id_user: int
    user_rating: int

class Rating_User_Search(BaseModel):
    isbn: str
    id_user: int

class Update_Rating_User(BaseModel):
    user_rating: int