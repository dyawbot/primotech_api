import datetime
from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class SyncLogModels(WeBudgetBase, Stamp):
    __tablename__ = "sync_logs_we_budget"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False)
    last_sync_at = Column(DateTime, default=datetime.utcnow)
    checksum = Column(String, nullable=True)
    status = Column(String, nullable=True)
    details = Column(String)

    user = relationship("Users", back_populates="sync_logs")