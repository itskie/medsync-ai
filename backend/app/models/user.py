from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    # Actual MySQL table name
    __tablename__ = "users"

    # Primary key — auto increment
    id = Column(Integer, primary_key=True, index=True)
    
    # User details
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="sales_rep")
    is_active = Column(Boolean, default=True)
    
    # Timestamps — auto set by database
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())