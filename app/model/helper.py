from pydantic import BaseModel
from typing import Any, Optional



class StatusHelper(BaseModel):
    code: int
    status: str
    message: str
    token: Optional[str] = None
    result: Optional[Any] = None



class UserImageHelper(BaseModel):
    username: str
    image_name: str
    image_url: str