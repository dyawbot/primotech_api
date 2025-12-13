from app.model.declarativebase.base import WeBudgetBase
from app.model.we_budget.base import TimestampMixIn as Stamp
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class AnalyticCacheModel(WeBudgetBase, Stamp):
    __tablename__ = "tbl_analytic_cache"

    id = Column(Integer, primary_key=True, index=True)
    analytic_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("tbl_user.uid"), nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    total_expense = Column(Float, nullable=False)
    total_income = Column(Float, nullable=False)
    top_category = Column(String, nullable=True)  # JSON string of top categories
    top_merchant = Column(String, nullable=True)  # JSON string of top merchants
    overspent_categories = Column(String, nullable=True)  # JSON string of overspent categories
    favorite_spending_time = Column(String, nullable=True)  # e.g., 'Evening', 'Morning'
    favorite_merchant = Column(String, nullable=True)
    prediction_next_month_expense = Column(Float, nullable=True)
    saving_rate = Column(Float, nullable=True)
    

    # cache_key = Column(String, nullable=False, index=True)
    # cache_data = Column(String, nullable=False)

    user = relationship("Users", back_populates="analytic_caches")