from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base.timestamp_mixin import TimestampMixIn as Stamp

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class CategoryModel(WeBudgetBase, Stamp):
    __tablename__ = 'tbl_category'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    category_name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True, index=True)
    type  = Column(String, nullable=False, index=True)  # e.g., 'income' or 'expense'

    user = relationship("Users", back_populates="categories")
    transactions = relationship("TrasactionsModels", back_populates="category")
    recurring_transactions = relationship("RecurringTransactionModel", back_populates="category")