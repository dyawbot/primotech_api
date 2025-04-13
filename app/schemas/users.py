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

    


# class RequestUser(BaseModel):
#     parameter: UserSchema= Field(...)

class RequestUser:
    def __init__(self, username: str = Form(...), 
                 password: str = Form(...),
                 first_name: Optional[str] = Form(None),
                 last_name: Optional[str] =Form(None),
                 phone_number: Optional[str] = Form(None)):
        
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number 
        self.password = password
        


class RequestLoginUser:
    def __init__(self, username: Optional[str] = Form(None), password: Optional[str] = Form(None), token: Optional[str] = Form(None)):
        self.username = username
        self.password = password
        self.token = token

# class RequestImage(BaseModel):
#     parameter: ImagesUsersSchema = Form(...)

class Response(GenericModel, Generic[T]):
    code : int
    status: str
    message: str
    result: Optional[T]