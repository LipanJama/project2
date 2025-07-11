from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from ..core.security import UserRole
import enum


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(Base):
    """User model - Multi-role user entity"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="SET NULL"), index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    avatar_url = Column(String(500))
    role = Column(Enum(UserRole), nullable=False, index=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, index=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="users")
    branch = relationship("Branch", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent = relationship("Parent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    employee = relationship("Employee", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Teaching relationships
    sections_taught = relationship("Section", back_populates="teacher")
    class_subjects_taught = relationship("ClassSubject", back_populates="teacher")
    
    # Created entities
    exams_created = relationship("Exam", back_populates="created_by_user", foreign_keys="Exam.created_by")
    notifications_created = relationship("Notification", back_populates="created_by_user")
    user_notifications = relationship("UserNotification", back_populates="user", cascade="all, delete-orphan")
    
    # Attendance recorded
    student_attendances_recorded = relationship("StudentAttendance", back_populates="recorded_by_user", foreign_keys="StudentAttendance.recorded_by")
    employee_attendances_approved = relationship("EmployeeAttendance", back_populates="approved_by_user", foreign_keys="EmployeeAttendance.approved_by")
    exam_results_recorded = relationship("StudentExamResult", back_populates="recorded_by_user", foreign_keys="StudentExamResult.recorded_by")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class StudentStatus(str, enum.Enum):
    ACTIVE = "active"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"
    DROPPED = "dropped"


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    admission_date = Column(Date)
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    blood_group = Column(String(5))
    address = Column(Text)
    emergency_contact = Column(String(20))
    medical_conditions = Column(Text)
    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="students")
    branch = relationship("Branch", back_populates="students")
    user = relationship("User", back_populates="student")
    
    # Academic relationships
    enrollments = relationship("StudentEnrollment", back_populates="student", cascade="all, delete-orphan")
    attendances = relationship("StudentAttendance", back_populates="student", cascade="all, delete-orphan")
    exam_results = relationship("StudentExamResult", back_populates="student", cascade="all, delete-orphan")
    
    # Parent relationships
    parent_relationships = relationship("StudentParent", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(id={self.id}, student_id='{self.student_id}', user_id={self.user_id})>"


class ParentRelationship(str, enum.Enum):
    FATHER = "father"
    MOTHER = "mother"
    GUARDIAN = "guardian"
    OTHER = "other"


class Parent(Base):
    """Parent model"""
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    relationship = Column(Enum(ParentRelationship), nullable=False)
    occupation = Column(String(255))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="parents")
    user = relationship("User", back_populates="parent")
    
    # Student relationships
    student_relationships = relationship("StudentParent", back_populates="parent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Parent(id={self.id}, relationship='{self.relationship}', user_id={self.user_id})>"


class StudentParent(Base):
    """Student-Parent relationship model"""
    __tablename__ = "student_parents"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False, index=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="parent_relationships")
    parent = relationship("Parent", back_populates="student_relationships")
    
    def __repr__(self):
        return f"<StudentParent(student_id={self.student_id}, parent_id={self.parent_id})>"


class SalaryType(str, enum.Enum):
    MONTHLY = "monthly"
    HOURLY = "hourly"
    DAILY = "daily"


class AccountType(str, enum.Enum):
    BANK = "bank"
    EVC = "evc"
    CASH = "cash"


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    designation = Column(String(255))
    department = Column(String(255))
    hire_date = Column(Date)
    salary = Column(DECIMAL(10, 2), default=0.00)
    salary_type = Column(Enum(SalaryType), default=SalaryType.MONTHLY)
    bank_account = Column(String(50))
    account_type = Column(Enum(AccountType), default=AccountType.BANK)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="employees")
    branch = relationship("Branch", back_populates="employees")
    user = relationship("User", back_populates="employee")
    
    # Payroll relationships
    attendances = relationship("EmployeeAttendance", back_populates="employee", cascade="all, delete-orphan")
    payroll_records = relationship("PayrollRecord", back_populates="employee", cascade="all, delete-orphan")
    deductions = relationship("EmployeeDeduction", back_populates="employee", cascade="all, delete-orphan")
    bonuses = relationship("EmployeeBonus", back_populates="employee", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', user_id={self.user_id})>"