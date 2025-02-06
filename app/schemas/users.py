from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from fastapi import Form
from pydantic.generics import GenericModel


T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int]=None
    userId : Optional[str] = None
    username : Optional[str] = None

    class Config:
        orm_mode = True



class ImagesUsersSchema(BaseModel):
    id: Optional[int] = None
    image_name: Optional[str] = None
    image_page: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

    


class RequestUser(BaseModel):
    parameter: UserSchema= Field(...)


# class RequestImage(BaseModel):
#     parameter: ImagesUsersSchema = Form(...)

class Response(GenericModel, Generic[T]):
    code : int
    status: str
    message: str
    result: Optional[T]