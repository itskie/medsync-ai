from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class HCP(Base):
    # Healthcare Professional table
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    
    # HCP personal details
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    hospital = Column(String(200))
    city = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # One HCP can have many interactions
    # relationship() links HCP to Interaction model
    interactions = relationship("Interaction", back_populates="hcp")