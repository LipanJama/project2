from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class PayrollStatus(str, enum.Enum):
    DRAFT = "draft"
    PROCESSED = "processed"
    PAID = "paid"


class PayrollPeriod(Base):
    """Payroll period model"""
    __tablename__ = "payroll_periods"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(PayrollStatus), default=PayrollStatus.DRAFT, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    payroll_records = relationship("PayrollRecord", back_populates="payroll_period", cascade="all, delete-orphan")
    employee_bonuses = relationship("EmployeeBonus", back_populates="payroll_period")
    
    def __repr__(self):
        return f"<PayrollPeriod(id={self.id}, name='{self.name}', status='{self.status}')>"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class PayrollRecord(Base):
    """Payroll record model"""
    __tablename__ = "payroll_records"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    basic_salary = Column(DECIMAL(10, 2), nullable=False)
    days_worked = Column(Integer, default=0)
    total_days = Column(Integer, default=0)
    overtime_hours = Column(DECIMAL(4, 2), default=0.00)
    overtime_rate = Column(DECIMAL(6, 2), default=0.00)
    gross_salary = Column(DECIMAL(10, 2), default=0.00)
    deductions = Column(DECIMAL(10, 2), default=0.00)
    bonuses = Column(DECIMAL(10, 2), default=0.00)
    paye_tax = Column(DECIMAL(10, 2), default=0.00)
    net_salary = Column(DECIMAL(10, 2), default=0.00)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for payroll period and employee
    __table_args__ = (
        UniqueConstraint('payroll_period_id', 'employee_id', name='unique_payroll_employee'),
    )
    
    # Relationships
    school = relationship("School")
    payroll_period = relationship("PayrollPeriod", back_populates="payroll_records")
    employee = relationship("Employee", back_populates="payroll_records")
    
    def __repr__(self):
        return f"<PayrollRecord(id={self.id}, employee_id={self.employee_id}, net_salary={self.net_salary})>"


class DeductionType(str, enum.Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class DeductionStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class EmployeeDeduction(Base):
    """Employee deduction model"""
    __tablename__ = "employee_deductions"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    type = Column(Enum(DeductionType), default=DeductionType.FIXED)
    is_recurring = Column(Boolean, default=True)
    effective_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(DeductionStatus), default=DeductionStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    employee = relationship("Employee", back_populates="deductions")
    
    def __repr__(self):
        return f"<EmployeeDeduction(id={self.id}, employee_id={self.employee_id}, name='{self.name}')>"


class BonusType(str, enum.Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class BonusStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"


class EmployeeBonus(Base):
    """Employee bonus model"""
    __tablename__ = "employee_bonuses"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    type = Column(Enum(BonusType), default=BonusType.FIXED)
    award_date = Column(Date)
    payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id", ondelete="SET NULL"), index=True)
    status = Column(Enum(BonusStatus), default=BonusStatus.PENDING, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    employee = relationship("Employee", back_populates="bonuses")
    payroll_period = relationship("PayrollPeriod", back_populates="employee_bonuses")
    
    def __repr__(self):
        return f"<EmployeeBonus(id={self.id}, employee_id={self.employee_id}, name='{self.name}')>"