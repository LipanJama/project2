from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class StudentAttendance(Base):
    """Student attendance model"""
    __tablename__ = "student_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(Enum(AttendanceStatus), nullable=False)
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    remarks = Column(Text)
    recorded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for student and date (one attendance record per day)
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='unique_student_date'),
    )
    
    # Relationships
    school = relationship("School")
    student = relationship("Student", back_populates="attendances")
    section = relationship("Section", back_populates="student_attendances")
    recorded_by_user = relationship("User", back_populates="student_attendances_recorded", foreign_keys=[recorded_by])
    
    def __repr__(self):
        return f"<StudentAttendance(student_id={self.student_id}, date='{self.date}', status='{self.status}')>"


class EmployeeAttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    SICK_LEAVE = "sick_leave"
    VACATION = "vacation"


class EmployeeAttendance(Base):
    """Employee attendance model"""
    __tablename__ = "employee_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(Enum(EmployeeAttendanceStatus), nullable=False)
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    total_hours = Column(DECIMAL(4, 2), default=0.00)
    overtime_hours = Column(DECIMAL(4, 2), default=0.00)
    remarks = Column(Text)
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for employee and date (one attendance record per day)
    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
    )
    
    # Relationships
    school = relationship("School")
    employee = relationship("Employee", back_populates="attendances")
    approved_by_user = relationship("User", back_populates="employee_attendances_approved", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<EmployeeAttendance(employee_id={self.employee_id}, date='{self.date}', status='{self.status}')>"