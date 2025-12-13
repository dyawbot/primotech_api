from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp


class PartnerModel(WeBudgetBase, Stamp):
    __tablename__ = "tbl_partner"
    
    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(String, unique=True,index=True, nullable=False)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False, index=True)
    code = Column(String, nullable=True, index=True)

    user = relationship("Users", back_populates="partners")