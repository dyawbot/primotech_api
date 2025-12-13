from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp

class Users(WeBudgetBase, Stamp):
    __tablename__ = 'tbl_user'

    id = Column(Integer, primary_key=True, index = True)
    uid = Column(String, unique=True, index = True)
    name =Column(String, nullable = False)
    email = Column(String, unique = True, index = True)

    devices = relationship("UserDeviceModels", back_populates="user")
    partners = relationship("PartnerModel", back_populates="user")
    families = relationship("FamilyModels", back_populates="user")
    sync_logs = relationship("SyncLogModels", back_populates="user")