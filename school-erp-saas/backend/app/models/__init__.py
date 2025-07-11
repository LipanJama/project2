# Import all models here for easy access
from .school import School, Branch
from .user import User, Student, Parent, StudentParent, Employee
from .academic import AcademicYear, Class, Section, Subject, ClassSubject, StudentEnrollment
from .attendance import StudentAttendance, EmployeeAttendance
from .payroll import PayrollPeriod, PayrollRecord, EmployeeDeduction, EmployeeBonus
from .exam import Exam, ExamSubject, StudentExamResult
from .messaging import MessagingProvider, SchoolMessagingConfig, MessageLog
from .notification import Notification, UserNotification
from .billing import SchoolBilling

# Export all models
__all__ = [
    "School",
    "Branch", 
    "User",
    "Student",
    "Parent",
    "StudentParent",
    "Employee",
    "AcademicYear",
    "Class",
    "Section",
    "Subject",
    "ClassSubject",
    "StudentEnrollment",
    "StudentAttendance",
    "EmployeeAttendance",
    "PayrollPeriod",
    "PayrollRecord",
    "EmployeeDeduction",
    "EmployeeBonus",
    "Exam",
    "ExamSubject",
    "StudentExamResult",
    "MessagingProvider",
    "SchoolMessagingConfig",
    "MessageLog",
    "Notification",
    "UserNotification",
    "SchoolBilling",
]