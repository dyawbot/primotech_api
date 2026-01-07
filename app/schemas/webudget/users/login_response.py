from typing import Optional, TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel



T = TypeVar('T')

class LoginResponse(GenericModel, Generic[T]):
    expiration: str
    token: str