from typing import List, Optional
from pydantic import BaseSettings, EmailStr, validator
import os
from decouple import config


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = config("API_V1_STR", default="/api/v1")
    PROJECT_NAME: str = config("PROJECT_NAME", default="SaaS School ERP")
    VERSION: str = config("VERSION", default="1.0.0")
    DESCRIPTION: str = config("DESCRIPTION", default="Multi-tenant School ERP System")
    
    # Security
    SECRET_KEY: str = config("SECRET_KEY", default="your-super-secret-key-here-change-this-in-production")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # JWT Configuration
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", default="your-jwt-secret-key-here")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = config("JWT_REFRESH_TOKEN_EXPIRE_DAYS", default=7, cast=int)
    
    # Database Configuration
    DATABASE_URL: str = config("DATABASE_URL", default="mysql+mysqlconnector://username:password@localhost:3306/school_erp_saas")
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: int = config("DB_PORT", default=3306, cast=int)
    DB_USER: str = config("DB_USER", default="username")
    DB_PASSWORD: str = config("DB_PASSWORD", default="password")
    DB_NAME: str = config("DB_NAME", default="school_erp_saas")
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Redis Configuration
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")
    REDIS_HOST: str = config("REDIS_HOST", default="localhost")
    REDIS_PORT: int = config("REDIS_PORT", default=6379, cast=int)
    REDIS_DB: int = config("REDIS_DB", default=0, cast=int)
    
    # Celery Configuration
    CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", default="redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/2")
    
    # File Upload Settings
    UPLOAD_DIR: str = config("UPLOAD_DIR", default="./uploads")
    MAX_FILE_SIZE: int = config("MAX_FILE_SIZE", default=10485760, cast=int)  # 10MB
    ALLOWED_EXTENSIONS: List[str] = config("ALLOWED_EXTENSIONS", default="jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx").split(",")
    
    # Email Configuration
    SMTP_HOST: str = config("SMTP_HOST", default="smtp.gmail.com")
    SMTP_PORT: int = config("SMTP_PORT", default=587, cast=int)
    SMTP_USERNAME: str = config("SMTP_USERNAME", default="")
    SMTP_PASSWORD: str = config("SMTP_PASSWORD", default="")
    SMTP_FROM_EMAIL: EmailStr = config("SMTP_FROM_EMAIL", default="noreply@yourschoolerp.com")
    SMTP_FROM_NAME: str = config("SMTP_FROM_NAME", default="School ERP System")
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str = config("TWILIO_ACCOUNT_SID", default="")
    TWILIO_AUTH_TOKEN: str = config("TWILIO_AUTH_TOKEN", default="")
    TWILIO_PHONE_NUMBER: str = config("TWILIO_PHONE_NUMBER", default="")
    
    # SendGrid Configuration
    SENDGRID_API_KEY: str = config("SENDGRID_API_KEY", default="")
    SENDGRID_FROM_EMAIL: EmailStr = config("SENDGRID_FROM_EMAIL", default="noreply@yourschoolerp.com")
    
    # WhatsApp Configuration
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = config("WHATSAPP_BUSINESS_ACCOUNT_ID", default="")
    WHATSAPP_ACCESS_TOKEN: str = config("WHATSAPP_ACCESS_TOKEN", default="")
    WHATSAPP_PHONE_NUMBER_ID: str = config("WHATSAPP_PHONE_NUMBER_ID", default="")
    
    # Hormuud SMS Configuration
    HORMUUD_API_URL: str = config("HORMUUD_API_URL", default="https://api.hormuud.com/sms")
    HORMUUD_API_KEY: str = config("HORMUUD_API_KEY", default="")
    HORMUUD_SENDER_ID: str = config("HORMUUD_SENDER_ID", default="")
    
    # Logging
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
    LOG_FILE: str = config("LOG_FILE", default="./logs/app.log")
    
    # Environment
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")
    
    # Superadmin Configuration
    SUPERADMIN_EMAIL: EmailStr = config("SUPERADMIN_EMAIL", default="admin@myerpsaas.com")
    SUPERADMIN_PASSWORD: str = config("SUPERADMIN_PASSWORD", default="admin123")
    SUPERADMIN_FIRST_NAME: str = config("SUPERADMIN_FIRST_NAME", default="Super")
    SUPERADMIN_LAST_NAME: str = config("SUPERADMIN_LAST_NAME", default="Admin")
    
    # Multi-tenant Configuration
    DEFAULT_SUBDOMAIN: str = config("DEFAULT_SUBDOMAIN", default="admin")
    MAIN_DOMAIN: str = config("MAIN_DOMAIN", default="myerpsaas.com")
    TENANT_CACHE_EXPIRE: int = config("TENANT_CACHE_EXPIRE", default=3600, cast=int)
    
    # Payment Gateway (Optional)
    STRIPE_PUBLIC_KEY: str = config("STRIPE_PUBLIC_KEY", default="")
    STRIPE_SECRET_KEY: str = config("STRIPE_SECRET_KEY", default="")
    STRIPE_WEBHOOK_SECRET: str = config("STRIPE_WEBHOOK_SECRET", default="")
    
    # AWS S3 Configuration (Optional)
    AWS_ACCESS_KEY_ID: str = config("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY: str = config("AWS_SECRET_ACCESS_KEY", default="")
    AWS_S3_BUCKET_NAME: str = config("AWS_S3_BUCKET_NAME", default="")
    AWS_REGION: str = config("AWS_REGION", default="us-east-1")
    
    # Certificate Generation
    CERTIFICATE_TEMPLATE_PATH: str = config("CERTIFICATE_TEMPLATE_PATH", default="./templates/certificate_template.pdf")
    QR_CODE_BASE_URL: str = config("QR_CODE_BASE_URL", default="https://verify.yourschoolerp.com")
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("./logs", exist_ok=True)