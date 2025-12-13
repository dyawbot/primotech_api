
from sqlalchemy import Column, DateTime, func, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

# from app.db.session import BaseWeBudget
from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base.timestamp_mixin import TimestampMixIn as Stamp


class UserDeviceModels(WeBudgetBase, Stamp):
    __tablename__ = "tbl_user_device"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable = False, index =True)
    user_id = Column(String,ForeignKey("tbl_user.uid"), nullable = False, index=True) ## in my ERD this is ForeignKey, how to implement
    blocked_status = Column(String,nullable =False, index=True)
    blocked_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    reason = Column(String, nullable=False, index=True)

    user = relationship("Users", back_populates="devices")