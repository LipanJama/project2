from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class MessageType(str, enum.Enum):
    SMS = "sms"
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class MessagingProvider(Base):
    """Messaging provider model"""
    __tablename__ = "messaging_providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(Enum(MessageType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school_configs = relationship("SchoolMessagingConfig", back_populates="provider", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MessagingProvider(id={self.id}, name='{self.name}', type='{self.type}')>"


class SchoolMessagingConfig(Base):
    """School messaging configuration model"""
    __tablename__ = "school_messaging_config"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("messaging_providers.id", ondelete="CASCADE"), nullable=False, index=True)
    api_key = Column(String(500))
    sender_id = Column(String(50))
    api_secret = Column(String(500))
    webhook_url = Column(String(500))
    unit_cost = Column(DECIMAL(8, 4), default=0.0000)
    balance = Column(DECIMAL(10, 2), default=0.00)
    is_active = Column(Boolean, default=False)
    is_tested = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Unique constraint for school and provider
    __table_args__ = (
        UniqueConstraint('school_id', 'provider_id', name='unique_school_provider'),
    )
    
    # Relationships
    school = relationship("School", back_populates="messaging_configs")
    provider = relationship("MessagingProvider", back_populates="school_configs")
    message_logs = relationship("MessageLog", back_populates="messaging_config", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SchoolMessagingConfig(id={self.id}, school_id={self.school_id}, provider_id={self.provider_id})>"


class RecipientType(str, enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    EMPLOYEE = "employee"
    CUSTOM = "custom"


class MessageStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class MessageLog(Base):
    """Message log model"""
    __tablename__ = "message_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    messaging_config_id = Column(Integer, ForeignKey("school_messaging_config.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_type = Column(Enum(RecipientType), nullable=False, index=True)
    recipient_id = Column(Integer, index=True)
    recipient_phone = Column(String(20))
    recipient_email = Column(String(255))
    message_type = Column(Enum(MessageType), nullable=False)
    subject = Column(String(255))
    message = Column(Text, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING, index=True)
    cost = Column(DECIMAL(8, 4), default=0.0000)
    external_id = Column(String(255))
    error_message = Column(Text)
    sent_at = Column(DateTime(timezone=True), index=True)
    delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School")
    messaging_config = relationship("SchoolMessagingConfig", back_populates="message_logs")
    
    def __repr__(self):
        return f"<MessageLog(id={self.id}, recipient_type='{self.recipient_type}', status='{self.status}')>"