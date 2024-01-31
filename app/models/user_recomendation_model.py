from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, validator
from pydantic import BaseModel

class UserRecomendation(BaseModel):
    user_id: int
    date: datetime 
