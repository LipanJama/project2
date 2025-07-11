from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta, date

from ..core.database import get_db, create_tenant_context
from ..core.security import get_current_user, CurrentUser, require_permission, Permission
from ..models import *

router = APIRouter()

# Pydantic models for responses
class DashboardStats(BaseModel):
    total_students: int
    total_teachers: int
    total_employees: int
    total_classes: int
    attendance_rate: float
    recent_activities: List[Dict[str, Any]]

class SuperAdminDashboard(BaseModel):
    total_schools: int
    active_schools: int
    total_users: int
    monthly_revenue: float
    top_schools: List[Dict[str, Any]]
    recent_registrations: List[Dict[str, Any]]

class AttendanceStats(BaseModel):
    present: int
    absent: int
    late: int
    total: int
    percentage: float

class PayrollStats(BaseModel):
    current_month_payroll: float
    pending_payments: int
    total_employees: int
    average_salary: float


@router.get("/stats")
async def get_dashboard_stats(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get role-based dashboard statistics
    """
    tenant_context = create_tenant_context(current_user.school_id)
    
    if current_user.is_superadmin():
        return await get_superadmin_dashboard(db)
    elif current_user.is_admin():
        return await get_admin_dashboard(db, current_user)
    elif current_user.is_teacher():
        return await get_teacher_dashboard(db, current_user)
    elif current_user.is_parent():
        return await get_parent_dashboard(db, current_user)
    elif current_user.is_student():
        return await get_student_dashboard(db, current_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


async def get_superadmin_dashboard(db: Session) -> SuperAdminDashboard:
    """SuperAdmin dashboard with system-wide statistics"""
    
    # Total schools
    total_schools = db.query(func.count(School.id)).scalar()
    
    # Active schools
    active_schools = db.query(func.count(School.id)).filter(
        School.subscription_status == "active"
    ).scalar()
    
    # Total users across all schools
    total_users = db.query(func.count(User.id)).scalar()
    
    # Monthly revenue (current month)
    current_month = datetime.now().replace(day=1)
    monthly_revenue = db.query(func.sum(SchoolBilling.total_amount)).filter(
        and_(
            SchoolBilling.billing_period_start >= current_month,
            SchoolBilling.status == "paid"
        )
    ).scalar() or 0.0
    
    # Top performing schools (by user count)
    top_schools_query = db.query(
        School.name,
        School.subdomain,
        func.count(User.id).label("user_count")
    ).join(User).filter(
        School.subscription_status == "active"
    ).group_by(School.id).order_by(func.count(User.id).desc()).limit(5)
    
    top_schools = [
        {
            "name": school.name,
            "subdomain": school.subdomain,
            "user_count": school.user_count
        }
        for school in top_schools_query
    ]
    
    # Recent school registrations
    recent_registrations_query = db.query(School).filter(
        School.created_at >= datetime.now() - timedelta(days=30)
    ).order_by(School.created_at.desc()).limit(10)
    
    recent_registrations = [
        {
            "name": school.name,
            "subdomain": school.subdomain,
            "subscription_plan": school.subscription_plan.value,
            "created_at": school.created_at.isoformat()
        }
        for school in recent_registrations_query
    ]
    
    return SuperAdminDashboard(
        total_schools=total_schools,
        active_schools=active_schools,
        total_users=total_users,
        monthly_revenue=float(monthly_revenue),
        top_schools=top_schools,
        recent_registrations=recent_registrations
    )


async def get_admin_dashboard(db: Session, current_user: CurrentUser) -> DashboardStats:
    """Admin dashboard with school-wide statistics"""
    
    school_filter = {"school_id": current_user.school_id}
    
    # Total students
    total_students = db.query(func.count(Student.id)).filter(
        Student.school_id == current_user.school_id,
        Student.status == "active"
    ).scalar()
    
    # Total teachers
    total_teachers = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.role == "teacher",
        User.status == "active"
    ).scalar()
    
    # Total employees
    total_employees = db.query(func.count(Employee.id)).filter(
        Employee.school_id == current_user.school_id,
        Employee.status == "active"
    ).scalar()
    
    # Total classes
    total_classes = db.query(func.count(Class.id)).filter(
        Class.school_id == current_user.school_id,
        Class.status == "active"
    ).scalar()
    
    # Calculate attendance rate for current month
    current_month_start = datetime.now().replace(day=1).date()
    
    total_attendance_records = db.query(func.count(StudentAttendance.id)).filter(
        StudentAttendance.school_id == current_user.school_id,
        StudentAttendance.date >= current_month_start
    ).scalar()
    
    present_records = db.query(func.count(StudentAttendance.id)).filter(
        StudentAttendance.school_id == current_user.school_id,
        StudentAttendance.date >= current_month_start,
        StudentAttendance.status == "present"
    ).scalar()
    
    attendance_rate = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0.0
    
    # Recent activities (last 10)
    recent_activities = []
    
    # Recent student enrollments
    recent_enrollments = db.query(StudentEnrollment).filter(
        StudentEnrollment.school_id == current_user.school_id
    ).order_by(StudentEnrollment.created_at.desc()).limit(5)
    
    for enrollment in recent_enrollments:
        recent_activities.append({
            "type": "enrollment",
            "message": f"Student enrolled in {enrollment.section.class_.name}-{enrollment.section.section_name}",
            "timestamp": enrollment.created_at.isoformat()
        })
    
    return DashboardStats(
        total_students=total_students,
        total_teachers=total_teachers,
        total_employees=total_employees,
        total_classes=total_classes,
        attendance_rate=round(attendance_rate, 2),
        recent_activities=recent_activities
    )


async def get_teacher_dashboard(db: Session, current_user: CurrentUser) -> Dict[str, Any]:
    """Teacher dashboard with class and student statistics"""
    
    # Get teacher's sections
    teacher_sections = db.query(Section).filter(
        Section.school_id == current_user.school_id,
        Section.teacher_id == current_user.user_id,
        Section.status == "active"
    ).all()
    
    # Get students in teacher's sections
    section_ids = [section.id for section in teacher_sections]
    
    total_students = db.query(func.count(StudentEnrollment.student_id)).filter(
        StudentEnrollment.section_id.in_(section_ids),
        StudentEnrollment.status == "active"
    ).scalar() if section_ids else 0
    
    # Today's attendance summary
    today = date.today()
    todays_attendance = db.query(
        StudentAttendance.status,
        func.count(StudentAttendance.id).label("count")
    ).filter(
        StudentAttendance.school_id == current_user.school_id,
        StudentAttendance.section_id.in_(section_ids),
        StudentAttendance.date == today
    ).group_by(StudentAttendance.status).all() if section_ids else []
    
    attendance_summary = {status: 0 for status in ["present", "absent", "late", "excused"]}
    for attendance in todays_attendance:
        attendance_summary[attendance.status] = attendance.count
    
    return {
        "total_sections": len(teacher_sections),
        "total_students": total_students,
        "sections": [
            {
                "id": section.id,
                "name": f"{section.class_.name}-{section.section_name}",
                "student_count": len(section.enrollments)
            }
            for section in teacher_sections
        ],
        "todays_attendance": attendance_summary
    }


async def get_parent_dashboard(db: Session, current_user: CurrentUser) -> Dict[str, Any]:
    """Parent dashboard with children's information"""
    
    # Get parent record
    parent = db.query(Parent).filter(
        Parent.school_id == current_user.school_id,
        Parent.user_id == current_user.user_id
    ).first()
    
    if not parent:
        return {"message": "Parent record not found"}
    
    # Get children
    children = db.query(Student).join(StudentParent).filter(
        StudentParent.parent_id == parent.id,
        Student.status == "active"
    ).all()
    
    children_info = []
    for child in children:
        # Get current enrollment
        current_enrollment = db.query(StudentEnrollment).filter(
            StudentEnrollment.student_id == child.id,
            StudentEnrollment.status == "active"
        ).first()
        
        # Get recent attendance
        recent_attendance = db.query(StudentAttendance).filter(
            StudentAttendance.student_id == child.id
        ).order_by(StudentAttendance.date.desc()).limit(5).all()
        
        children_info.append({
            "student_id": child.id,
            "name": child.user.full_name,
            "class": f"{current_enrollment.section.class_.name}-{current_enrollment.section.section_name}" if current_enrollment else "Not enrolled",
            "recent_attendance": [
                {
                    "date": att.date.isoformat(),
                    "status": att.status
                }
                for att in recent_attendance
            ]
        })
    
    return {
        "children_count": len(children),
        "children": children_info
    }


async def get_student_dashboard(db: Session, current_user: CurrentUser) -> Dict[str, Any]:
    """Student dashboard with academic information"""
    
    # Get student record
    student = db.query(Student).filter(
        Student.school_id == current_user.school_id,
        Student.user_id == current_user.user_id
    ).first()
    
    if not student:
        return {"message": "Student record not found"}
    
    # Get current enrollment
    current_enrollment = db.query(StudentEnrollment).filter(
        StudentEnrollment.student_id == student.id,
        StudentEnrollment.status == "active"
    ).first()
    
    # Get attendance summary for current month
    current_month_start = datetime.now().replace(day=1).date()
    
    attendance_stats = db.query(
        StudentAttendance.status,
        func.count(StudentAttendance.id).label("count")
    ).filter(
        StudentAttendance.student_id == student.id,
        StudentAttendance.date >= current_month_start
    ).group_by(StudentAttendance.status).all()
    
    attendance_summary = {status: 0 for status in ["present", "absent", "late", "excused"]}
    total_days = 0
    for attendance in attendance_stats:
        attendance_summary[attendance.status] = attendance.count
        total_days += attendance.count
    
    attendance_percentage = (attendance_summary["present"] / total_days * 100) if total_days > 0 else 0
    
    # Get recent exam results
    recent_results = db.query(StudentExamResult).filter(
        StudentExamResult.student_id == student.id
    ).order_by(StudentExamResult.created_at.desc()).limit(5).all()
    
    return {
        "student_info": {
            "name": student.user.full_name,
            "student_id": student.student_id,
            "class": f"{current_enrollment.section.class_.name}-{current_enrollment.section.section_name}" if current_enrollment else "Not enrolled",
            "admission_date": student.admission_date.isoformat() if student.admission_date else None
        },
        "attendance_summary": {
            "percentage": round(attendance_percentage, 2),
            "total_days": total_days,
            "present_days": attendance_summary["present"],
            "absent_days": attendance_summary["absent"]
        },
        "recent_exam_results": [
            {
                "subject": result.exam_subject.subject.name,
                "exam": result.exam_subject.exam.name,
                "marks": float(result.marks_obtained),
                "max_marks": result.exam_subject.max_marks,
                "percentage": round(float(result.marks_obtained) / result.exam_subject.max_marks * 100, 2),
                "grade": result.grade
            }
            for result in recent_results
        ]
    }


@router.get("/attendance-summary")
async def get_attendance_summary(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attendance summary for today"""
    
    if not current_user.has_permission(Permission.READ_ATTENDANCE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    today = date.today()
    
    # Get today's attendance stats
    attendance_stats = db.query(
        StudentAttendance.status,
        func.count(StudentAttendance.id).label("count")
    ).filter(
        StudentAttendance.school_id == current_user.school_id,
        StudentAttendance.date == today
    ).group_by(StudentAttendance.status).all()
    
    stats = {status: 0 for status in ["present", "absent", "late", "excused"]}
    total = 0
    
    for stat in attendance_stats:
        stats[stat.status] = stat.count
        total += stat.count
    
    percentage = (stats["present"] / total * 100) if total > 0 else 0
    
    return AttendanceStats(
        present=stats["present"],
        absent=stats["absent"],
        late=stats["late"],
        total=total,
        percentage=round(percentage, 2)
    )