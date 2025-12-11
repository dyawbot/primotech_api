from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base
from app.model.declarativebase.base import PrimoUserBase



class PrimoUsers(PrimoUserBase):
    __tablename__ = "tbl_primo_users"

    id = Column(Integer, primary_key=True, index=True)

     # --- from PrimoUserInformation ---
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    company_id = Column(String, nullable=True)

    # --- from PrimoUserCredentials ---
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hash it before saving!



    # --- from PrimoUsers ---
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())