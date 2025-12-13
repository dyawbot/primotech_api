from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base.timestamp_mixin import TimestampMixIn as Stamp

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class BankAccountsModel(WeBudgetBase, Stamp):
    __tablename__ = "tbl_bank_account"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    account_number = Column(String, nullable=False, index=True)
    bank_name = Column(String, nullable=False, index=True)
    starting_balance = Column(Integer, nullable=False, index=True)
    currency = Column(String, nullable=False, index=True)  # e.g., 'USD', 'EUR'

    user = relationship("Users", back_populates="bank_accounts")