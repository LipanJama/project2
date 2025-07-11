from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class NotificationType(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"


class TargetType(str, enum.Enum):
    ALL = "all"
    ROLE = "role"
    SPECIFIC_USERS = "specific_users"
    CLASS = "class"
    BRANCH = "branch"


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.INFO)
    target_type = Column(Enum(TargetType), nullable=False, index=True)
    target_value = Column(String(255), index=True)  # role name, user IDs, class ID, branch ID
    is_read = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="notifications")
    created_by_user = relationship("User", back_populates="notifications_created")
    user_notifications = relationship("UserNotification", back_populates="notification", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title='{self.title}', target_type='{self.target_type}')>"


class UserNotification(Base):
    """User notification model - for tracking read status"""
    __tablename__ = "user_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for notification and user
    __table_args__ = (
        UniqueConstraint('notification_id', 'user_id', name='unique_user_notification'),
    )
    
    # Relationships
    notification = relationship("Notification", back_populates="user_notifications")
    user = relationship("User", back_populates="user_notifications")
    
    def __repr__(self):
        return f"<UserNotification(notification_id={self.notification_id}, user_id={self.user_id}, is_read={self.is_read})>"