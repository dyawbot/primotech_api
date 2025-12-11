from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr





class PrimoUsers(BaseModel):
    id: Optional[int]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



class PrimoUserCredentials(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True



class PrimoUserInformation(BaseModel):

    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    company_id: Optional[str]

    class Config:
        orm_mode = True


class PrimoUserFullInfo(BaseModel):
    user: PrimoUsers
    credentials: PrimoUserCredentials
    information: Optional[PrimoUserInformation] = None