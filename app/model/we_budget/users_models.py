from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from app.db.session import BaseWeBudget
from app.model.we_budget.base import TimestampMixIn as Stamp

class Users(BaseWeBudget, Stamp):
    ___tablename__ = 'tbl_user'

    id = Column(Integer, primary_key=True, index = True)
    uid = Column(String, unique=True, index = True)
    name =Column(String, nullable = False)
    email = Column(String, unique = True, index = True)

    devices = relationship("UserDeviceModels", back_populates="User")