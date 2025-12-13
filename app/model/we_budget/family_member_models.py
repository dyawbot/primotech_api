from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base.timestamp_mixin import TimestampMixIn as Stamp

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
class FamilyMemberModels(WeBudgetBase, Stamp):
    __tablename__ = "tbl_family_member"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String, ForeignKey("tbl_family.family_id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    member_name = Column(String, nullable=False, index=True)
    birthdate = Column(String, nullable=True, index=True)
    family_relationship = Column(String, nullable=False, index=True)


    family = relationship("FamilyModels", back_populates="members")