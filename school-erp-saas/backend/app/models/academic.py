from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class AcademicStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AcademicYear(Base):
    """Academic Year model"""
    __tablename__ = "academic_years"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False, index=True)
    status = Column(Enum(AcademicStatus), default=AcademicStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="academic_years")
    sections = relationship("Section", back_populates="academic_year", cascade="all, delete-orphan")
    enrollments = relationship("StudentEnrollment", back_populates="academic_year", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AcademicYear(id={self.id}, name='{self.name}', school_id={self.school_id})>"


class ClassStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Class(Base):
    """Class model"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    grade_level = Column(Integer, nullable=False)
    capacity = Column(Integer, default=30)
    status = Column(Enum(ClassStatus), default=ClassStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    branch = relationship("Branch", back_populates="classes")
    sections = relationship("Section", back_populates="class_", cascade="all, delete-orphan")
    class_subjects = relationship("ClassSubject", back_populates="class_", cascade="all, delete-orphan")
    exam_subjects = relationship("ExamSubject", back_populates="class_", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}', grade_level={self.grade_level})>"


class SectionStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Section(Base):
    """Section model - Class sections per academic year"""
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False, index=True)
    section_name = Column(String(10), nullable=False)  # A, B, C, etc.
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    max_students = Column(Integer, default=30)
    status = Column(Enum(SectionStatus), default=SectionStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for class, academic year, and section name
    __table_args__ = (
        UniqueConstraint('class_id', 'academic_year_id', 'section_name', name='unique_section'),
    )
    
    # Relationships
    school = relationship("School")
    branch = relationship("Branch", back_populates="sections")
    class_ = relationship("Class", back_populates="sections")
    academic_year = relationship("AcademicYear", back_populates="sections")
    teacher = relationship("User", back_populates="sections_taught")
    
    # Student relationships
    enrollments = relationship("StudentEnrollment", back_populates="section", cascade="all, delete-orphan")
    student_attendances = relationship("StudentAttendance", back_populates="section", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Section(id={self.id}, class_id={self.class_id}, section_name='{self.section_name}')>"


class SubjectStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Subject(Base):
    """Subject model"""
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20))
    description = Column(Text)
    status = Column(Enum(SubjectStatus), default=SubjectStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="subjects")
    class_subjects = relationship("ClassSubject", back_populates="subject", cascade="all, delete-orphan")
    exam_subjects = relationship("ExamSubject", back_populates="subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', code='{self.code}')>"


class ClassSubject(Base):
    """Class-Subject relationship model (Many-to-many with teacher assignment)"""
    __tablename__ = "class_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for class and subject
    __table_args__ = (
        UniqueConstraint('class_id', 'subject_id', name='unique_class_subject'),
    )
    
    # Relationships
    school = relationship("School")
    class_ = relationship("Class", back_populates="class_subjects")
    subject = relationship("Subject", back_populates="class_subjects")
    teacher = relationship("User", back_populates="class_subjects_taught")
    
    def __repr__(self):
        return f"<ClassSubject(class_id={self.class_id}, subject_id={self.subject_id})>"


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    TRANSFERRED = "transferred"
    DROPPED = "dropped"


class StudentEnrollment(Base):
    """Student enrollment in sections"""
    __tablename__ = "student_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False, index=True)
    enrollment_date = Column(Date, nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for student and academic year (one enrollment per year)
    __table_args__ = (
        UniqueConstraint('student_id', 'academic_year_id', name='unique_student_year'),
    )
    
    # Relationships
    school = relationship("School")
    student = relationship("Student", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")
    academic_year = relationship("AcademicYear", back_populates="enrollments")
    
    def __repr__(self):
        return f"<StudentEnrollment(student_id={self.student_id}, section_id={self.section_id})>"