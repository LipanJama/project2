from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
import enum

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer
security = HTTPBearer()

# Role definitions
class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    TEACHER = "teacher"
    PARENT = "parent"
    STUDENT = "student"

# Permission definitions
class Permission(str, enum.Enum):
    # User management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # School management
    CREATE_SCHOOL = "create_school"
    READ_SCHOOL = "read_school"
    UPDATE_SCHOOL = "update_school"
    DELETE_SCHOOL = "delete_school"
    
    # Branch management
    CREATE_BRANCH = "create_branch"
    READ_BRANCH = "read_branch"
    UPDATE_BRANCH = "update_branch"
    DELETE_BRANCH = "delete_branch"
    
    # Student management
    CREATE_STUDENT = "create_student"
    READ_STUDENT = "read_student"
    UPDATE_STUDENT = "update_student"
    DELETE_STUDENT = "delete_student"
    
    # Employee management
    CREATE_EMPLOYEE = "create_employee"
    READ_EMPLOYEE = "read_employee"
    UPDATE_EMPLOYEE = "update_employee"
    DELETE_EMPLOYEE = "delete_employee"
    
    # Attendance management
    CREATE_ATTENDANCE = "create_attendance"
    READ_ATTENDANCE = "read_attendance"
    UPDATE_ATTENDANCE = "update_attendance"
    DELETE_ATTENDANCE = "delete_attendance"
    
    # Payroll management
    CREATE_PAYROLL = "create_payroll"
    READ_PAYROLL = "read_payroll"
    UPDATE_PAYROLL = "update_payroll"
    DELETE_PAYROLL = "delete_payroll"
    
    # Exam management
    CREATE_EXAM = "create_exam"
    READ_EXAM = "read_exam"
    UPDATE_EXAM = "update_exam"
    DELETE_EXAM = "delete_exam"
    
    # Messaging
    SEND_MESSAGE = "send_message"
    READ_MESSAGE = "read_message"
    
    # Reports
    GENERATE_REPORT = "generate_report"
    EXPORT_DATA = "export_data"

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.SUPERADMIN: [
        # All permissions for superadmin
        Permission.CREATE_SCHOOL, Permission.READ_SCHOOL, Permission.UPDATE_SCHOOL, Permission.DELETE_SCHOOL,
        Permission.CREATE_USER, Permission.READ_USER, Permission.UPDATE_USER, Permission.DELETE_USER,
        Permission.CREATE_BRANCH, Permission.READ_BRANCH, Permission.UPDATE_BRANCH, Permission.DELETE_BRANCH,
        Permission.CREATE_STUDENT, Permission.READ_STUDENT, Permission.UPDATE_STUDENT, Permission.DELETE_STUDENT,
        Permission.CREATE_EMPLOYEE, Permission.READ_EMPLOYEE, Permission.UPDATE_EMPLOYEE, Permission.DELETE_EMPLOYEE,
        Permission.CREATE_ATTENDANCE, Permission.READ_ATTENDANCE, Permission.UPDATE_ATTENDANCE, Permission.DELETE_ATTENDANCE,
        Permission.CREATE_PAYROLL, Permission.READ_PAYROLL, Permission.UPDATE_PAYROLL, Permission.DELETE_PAYROLL,
        Permission.CREATE_EXAM, Permission.READ_EXAM, Permission.UPDATE_EXAM, Permission.DELETE_EXAM,
        Permission.SEND_MESSAGE, Permission.READ_MESSAGE,
        Permission.GENERATE_REPORT, Permission.EXPORT_DATA,
    ],
    UserRole.ADMIN: [
        # School admin permissions
        Permission.READ_SCHOOL, Permission.UPDATE_SCHOOL,
        Permission.CREATE_USER, Permission.READ_USER, Permission.UPDATE_USER, Permission.DELETE_USER,
        Permission.CREATE_BRANCH, Permission.READ_BRANCH, Permission.UPDATE_BRANCH,
        Permission.CREATE_STUDENT, Permission.READ_STUDENT, Permission.UPDATE_STUDENT, Permission.DELETE_STUDENT,
        Permission.CREATE_EMPLOYEE, Permission.READ_EMPLOYEE, Permission.UPDATE_EMPLOYEE, Permission.DELETE_EMPLOYEE,
        Permission.CREATE_ATTENDANCE, Permission.READ_ATTENDANCE, Permission.UPDATE_ATTENDANCE, Permission.DELETE_ATTENDANCE,
        Permission.CREATE_PAYROLL, Permission.READ_PAYROLL, Permission.UPDATE_PAYROLL, Permission.DELETE_PAYROLL,
        Permission.CREATE_EXAM, Permission.READ_EXAM, Permission.UPDATE_EXAM, Permission.DELETE_EXAM,
        Permission.SEND_MESSAGE, Permission.READ_MESSAGE,
        Permission.GENERATE_REPORT, Permission.EXPORT_DATA,
    ],
    UserRole.TEACHER: [
        # Teacher permissions
        Permission.READ_USER, Permission.UPDATE_USER,  # Own profile only
        Permission.READ_STUDENT, Permission.UPDATE_STUDENT,  # Students in their classes
        Permission.CREATE_ATTENDANCE, Permission.READ_ATTENDANCE, Permission.UPDATE_ATTENDANCE,
        Permission.READ_EXAM, Permission.UPDATE_EXAM,  # Exams for their subjects
        Permission.READ_MESSAGE,
        Permission.GENERATE_REPORT,  # Limited reports
    ],
    UserRole.PARENT: [
        # Parent permissions
        Permission.READ_USER, Permission.UPDATE_USER,  # Own profile only
        Permission.READ_STUDENT,  # Own children only
        Permission.READ_ATTENDANCE,  # Own children's attendance
        Permission.READ_EXAM,  # Own children's exams
        Permission.READ_MESSAGE,
    ],
    UserRole.STUDENT: [
        # Student permissions
        Permission.READ_USER, Permission.UPDATE_USER,  # Own profile only
        Permission.READ_ATTENDANCE,  # Own attendance
        Permission.READ_EXAM,  # Own exams
        Permission.READ_MESSAGE,
    ],
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


class CurrentUser:
    """Current user information"""
    def __init__(self, user_id: int, email: str, role: UserRole, school_id: int, branch_id: Optional[int] = None):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.school_id = school_id
        self.branch_id = branch_id
        self.permissions = ROLE_PERMISSIONS.get(role, [])
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in self.permissions
    
    def is_superadmin(self) -> bool:
        """Check if user is superadmin."""
        return self.role == UserRole.SUPERADMIN
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRole.ADMIN
    
    def is_teacher(self) -> bool:
        """Check if user is teacher."""
        return self.role == UserRole.TEACHER
    
    def is_parent(self) -> bool:
        """Check if user is parent."""
        return self.role == UserRole.PARENT
    
    def is_student(self) -> bool:
        """Check if user is student."""
        return self.role == UserRole.STUDENT


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        school_id: int = payload.get("school_id")
        branch_id: Optional[int] = payload.get("branch_id")
        
        if user_id is None or email is None or role is None or school_id is None:
            raise credentials_exception
        
        # Additional validation can be added here (e.g., check if user exists in DB)
        
        return CurrentUser(
            user_id=user_id,
            email=email,
            role=UserRole(role),
            school_id=school_id,
            branch_id=branch_id
        )
    except (JWTError, ValueError):
        raise credentials_exception


def require_permission(permission: Permission):
    """Decorator to require specific permission."""
    def permission_dependency(current_user: CurrentUser = Depends(get_current_user)):
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_dependency


def require_role(required_role: UserRole):
    """Decorator to require specific role."""
    def role_dependency(current_user: CurrentUser = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role.value}"
            )
        return current_user
    return role_dependency


def require_superadmin():
    """Decorator to require superadmin role."""
    return require_role(UserRole.SUPERADMIN)


def require_admin_or_superadmin():
    """Decorator to require admin or superadmin role."""
    def role_dependency(current_user: CurrentUser = Depends(get_current_user)):
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Required role: admin or superadmin"
            )
        return current_user
    return role_dependency


async def get_tenant_from_subdomain(request: Request) -> Optional[str]:
    """Extract tenant (subdomain) from request."""
    host = request.headers.get("host")
    if not host:
        return None
    
    # Extract subdomain
    parts = host.split(".")
    if len(parts) >= 3:  # subdomain.domain.tld
        return parts[0]
    
    return None


class TenantMiddleware:
    """Middleware to handle multi-tenant requests based on subdomain."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            subdomain = await get_tenant_from_subdomain(request)
            
            # Add tenant info to request state
            if subdomain:
                scope["state"] = getattr(scope, "state", {})
                scope["state"]["tenant"] = subdomain
        
        await self.app(scope, receive, send)