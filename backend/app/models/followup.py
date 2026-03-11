from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Followup(Base):
    # AI suggested followup actions table
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)

    # Followup details
    suggested_action = Column(Text, nullable=False)
    due_date = Column(String(20))
    status = Column(String(20), default="pending")  # pending/done/cancelled
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship — connects back to Interaction
    interaction = relationship("Interaction", back_populates="followups")