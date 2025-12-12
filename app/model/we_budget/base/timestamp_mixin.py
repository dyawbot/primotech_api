from sqlalchemy import Column, DateTime, func

class TimestampMixIn:
    created_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now(), nullable=True)

