from typing import Optional
from pydantic import BaseModel


class UserRegistrationShema(BaseModel):
    id: Optional[int]=None
    userId : Optional[str] = None
    name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None

    class Config:
        orm_mode = True


class UserDeviceRegistrationSchema(BaseModel):
    id: Optional[int] = None
    device_id: Optional[str] = None
    user_id: Optional[int] = None
    block_status: Optional[str] = None
    reason: Optional[str] = None
    block_at : Optional[str] = None

    class Config:
        orm_mode = True

class PartnerRegistrationSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    name: str
    email: str
    code: Optional[str] = None

    class Config:
        orm_mode = True


class FamilyRegistrationSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    family_name: str
    code : Optional[str] = None


    class Config:
        orm_mode = True

class FamilyMemberRegistrationSchema(BaseModel):
    id: Optional[int] = None
    family_id: Optional[int] = None
    member_name: str
    relation: str
    code : Optional[str] = None
    birthdate: Optional[str] = None

    class Config:
        orm_mode = True