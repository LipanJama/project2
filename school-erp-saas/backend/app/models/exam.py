from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class ExamType(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class ExamStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class Exam(Base):
    """Exam model"""
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ExamType), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(ExamStatus), default=ExamStatus.DRAFT, index=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    branch = relationship("Branch", back_populates="exams")
    created_by_user = relationship("User", back_populates="exams_created", foreign_keys=[created_by])
    exam_subjects = relationship("ExamSubject", back_populates="exam", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Exam(id={self.id}, name='{self.name}', type='{self.type}')>"


class ExamSubject(Base):
    """Exam subject model - Subjects within an exam"""
    __tablename__ = "exam_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    max_marks = Column(Integer, default=100)
    pass_marks = Column(Integer, default=40)
    exam_date = Column(Date)
    start_time = Column(Time)
    duration_minutes = Column(Integer, default=60)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for exam, subject, and class
    __table_args__ = (
        UniqueConstraint('exam_id', 'subject_id', 'class_id', name='unique_exam_subject_class'),
    )
    
    # Relationships
    school = relationship("School")
    exam = relationship("Exam", back_populates="exam_subjects")
    subject = relationship("Subject", back_populates="exam_subjects")
    class_ = relationship("Class", back_populates="exam_subjects")
    student_results = relationship("StudentExamResult", back_populates="exam_subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ExamSubject(id={self.id}, exam_id={self.exam_id}, subject_id={self.subject_id})>"


class StudentExamResult(Base):
    """Student exam result model"""
    __tablename__ = "student_exam_results"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_subject_id = Column(Integer, ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    marks_obtained = Column(DECIMAL(5, 2), default=0.00)
    grade = Column(String(5))
    remarks = Column(Text)
    recorded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for exam subject and student
    __table_args__ = (
        UniqueConstraint('exam_subject_id', 'student_id', name='unique_student_exam'),
    )
    
    # Relationships
    school = relationship("School")
    exam_subject = relationship("ExamSubject", back_populates="student_results")
    student = relationship("Student", back_populates="exam_results")
    recorded_by_user = relationship("User", back_populates="exam_results_recorded", foreign_keys=[recorded_by])
    
    def __repr__(self):
        return f"<StudentExamResult(id={self.id}, student_id={self.student_id}, marks={self.marks_obtained})>"