from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class SubscriptionPlan(str, enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class School(Base):
    """School model - Tenant entity"""
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(String(500))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.BASIC)
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, index=True)
    subscription_start_date = Column(Date)
    subscription_end_date = Column(Date)
    monthly_fee = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    branches = relationship("Branch", back_populates="school", cascade="all, delete-orphan")
    users = relationship("User", back_populates="school", cascade="all, delete-orphan")
    academic_years = relationship("AcademicYear", back_populates="school", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="school", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="school", cascade="all, delete-orphan")
    parents = relationship("Parent", back_populates="school", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="school", cascade="all, delete-orphan")
    messaging_configs = relationship("SchoolMessagingConfig", back_populates="school", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="school", cascade="all, delete-orphan")
    billing_records = relationship("SchoolBilling", back_populates="school", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<School(id={self.id}, name='{self.name}', subdomain='{self.subdomain}')>"


class BranchStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Branch(Base):
    """Branch model - School branches"""
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    is_main_branch = Column(Boolean, default=False)
    status = Column(Enum(BranchStatus), default=BranchStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="branches")
    users = relationship("User", back_populates="branch")
    classes = relationship("Class", back_populates="branch", cascade="all, delete-orphan")
    sections = relationship("Section", back_populates="branch", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="branch", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="branch", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="branch", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Branch(id={self.id}, name='{self.name}', school_id={self.school_id})>"