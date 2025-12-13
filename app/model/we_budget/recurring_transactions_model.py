from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class RecurringTransactionModel(WeBudgetBase, Stamp):
    __tablename__ = "tbl_recurring_transaction"

    id = Column(Integer, primary_key=True, index=True)
    recurring_id = Column(String, unique=True, index=True, nullable=False)
    category_id = Column(String, ForeignKey("tbl_category.category_id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    frequency = Column(String, nullable=False)
    next_due_date = Column(DateTime(timezone=True), nullable=True)
    description = Column(String, nullable=True)

    user = relationship("Users", back_populates="recurring_transactions")
    category = relationship("CategoryModel", back_populates="recurring_transactions")