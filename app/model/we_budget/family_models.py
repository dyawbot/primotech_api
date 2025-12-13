from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp
from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.orm import relationship

class FamilyModels(WeBudgetBase, Stamp):
    __tablename__ = "tbl_family"
    
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String,ForeignKey("tbl_user.uid"),  nullable=False, index=True)
    family_name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    
    user = relationship("Users", back_populates="families")
    members = relationship("FamilyMemberModels", back_populates="family")