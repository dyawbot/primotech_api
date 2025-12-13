from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base.timestamp_mixin import TimestampMixIn as Stamp

class Users(WeBudgetBase, Stamp):
    __tablename__ = 'tbl_user'

    id = Column(Integer, primary_key=True, index = True)
    uid = Column(String, unique=True, index = True)
    name =Column(String, nullable = False)
    email = Column(String, unique = True, index = True)
    password = Column(String, nullable = False)

    devices = relationship("UserDeviceModels", back_populates="user")
    partners = relationship("PartnerModel", back_populates="user")
    families = relationship("FamilyModels", back_populates="user")
    sync_logs = relationship("SyncLogModels", back_populates="user")
    categories = relationship("CategoryModel", back_populates="user")
    bank_accounts = relationship("BankAccountsModel", back_populates="user")
    transactions = relationship("TrasactionsModels", back_populates="user")
    recurring_transactions = relationship("RecurringTransactionModel", back_populates="user")
    analytic_caches = relationship("AnalyticCacheModels", back_populates="user")