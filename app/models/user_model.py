from typing import Union
from pydantic import BaseModel as PydanticBaseModel, validator
from pydantic import BaseModel


class User(BaseModel):
    id: int
    type: int
    name: str
    last_name: Union[None,str]
    email: str
    password: str
    age: Union[None, int]
    active: bool
