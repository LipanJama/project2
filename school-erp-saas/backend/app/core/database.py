from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import redis
from .config import settings

# SQLAlchemy setup
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Metadata for the database
metadata = MetaData()

# Redis client setup
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> redis.Redis:
    """
    Redis dependency for FastAPI routes
    """
    return redis_client


# Multi-tenant database helper functions
class TenantContext:
    """Context manager for tenant-specific database operations"""
    
    def __init__(self, school_id: int):
        self.school_id = school_id
    
    def get_school_filter(self):
        """Return school_id filter for queries"""
        return {"school_id": self.school_id}
    
    def apply_school_filter(self, query, model_class):
        """Apply school filter to SQLAlchemy query"""
        if hasattr(model_class, 'school_id'):
            return query.filter(model_class.school_id == self.school_id)
        return query


def create_tenant_context(school_id: int) -> TenantContext:
    """Create a new tenant context"""
    return TenantContext(school_id)


# Cache functions
class CacheManager:
    """Cache manager for the application"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_expire = settings.TENANT_CACHE_EXPIRE
    
    def get(self, key: str):
        """Get value from cache"""
        try:
            return self.redis.get(key)
        except Exception:
            return None
    
    def set(self, key: str, value: str, expire: int = None):
        """Set value in cache"""
        try:
            expire = expire or self.default_expire
            return self.redis.setex(key, expire, value)
        except Exception:
            return False
    
    def delete(self, key: str):
        """Delete key from cache"""
        try:
            return self.redis.delete(key)
        except Exception:
            return False
    
    def get_tenant_key(self, school_id: int, key: str) -> str:
        """Generate tenant-specific cache key"""
        return f"tenant:{school_id}:{key}"
    
    def get_user_key(self, user_id: int, key: str) -> str:
        """Generate user-specific cache key"""
        return f"user:{user_id}:{key}"


# Global cache manager instance
cache_manager = CacheManager(redis_client)


# Database health check
def check_database_health() -> bool:
    """Check if database is healthy"""
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
            return True
    except Exception:
        return False


def check_redis_health() -> bool:
    """Check if Redis is healthy"""
    try:
        redis_client.ping()
        return True
    except Exception:
        return False