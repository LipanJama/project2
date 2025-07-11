from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class BillingStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class SchoolBilling(Base):
    """School billing model"""
    __tablename__ = "school_billing"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    subscription_fee = Column(DECIMAL(10, 2), nullable=False)
    messaging_cost = Column(DECIMAL(10, 2), default=0.00)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(BillingStatus), default=BillingStatus.PENDING, index=True)
    due_date = Column(Date, index=True)
    paid_date = Column(Date)
    payment_method = Column(String(100))
    transaction_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="billing_records")
    
    def __repr__(self):
        return f"<SchoolBilling(id={self.id}, school_id={self.school_id}, total_amount={self.total_amount})>"