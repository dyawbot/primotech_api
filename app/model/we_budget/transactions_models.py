from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

class TrasactionsModels(WeBudgetBase, Stamp):
    __tablename__ = "tbl_transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    category_id = Column(String, ForeignKey("tbl_category.category_id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    amount = Column(Float, nullable=False, index=True)
    merchant_name = Column(String, nullable=True, index=True)
    transaction_type = Column(String, nullable=False, index=True)  # e.g., 'debit' or 'credit'
    transaction_date = Column(DateTime, nullable=False, index=True)
    notes = Column(String, nullable=True, index=True)

    user = relationship("Users", back_populates="transactions")
    category = relationship("CategoryModel", back_populates="transactions")