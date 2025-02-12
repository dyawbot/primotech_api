from pydantic import BaseModel
from typing import Any, Optional



class StatusHelper(BaseModel):
    code: int
    status: str
    message: str
    result: Optional[Any] = None



class UserImageHelper(BaseModel):
    username: str
    image_name: str
    image_url: str