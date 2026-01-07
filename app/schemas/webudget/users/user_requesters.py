from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: Optional[str] =None
    password: Optional[str] =None
    token: Optional[str] = None

