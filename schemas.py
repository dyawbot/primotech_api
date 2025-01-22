from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int]=None
    userId = Optional[str] = None
    userName = Optional[str] = None

    class Config:
        orm_mode = True


    