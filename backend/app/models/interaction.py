from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Interaction(Base):
    # Logged HCP interactions table
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys — links to other tables
    # ForeignKey = "us table ki id se connected hai"
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Interaction details
    interaction_type = Column(String(50), default="meeting")  # meeting/call/email
    date = Column(String(20), nullable=False)
    time = Column(String(20))
    attendees = Column(Text)
    topics_discussed = Column(Text)
    materials_shared = Column(Text)
    samples_distributed = Column(Text)

    # AI generated fields
    sentiment = Column(String(20), default="neutral")  # positive/neutral/negative
    ai_summary = Column(Text)
    outcomes = Column(Text)
    followup_actions = Column(Text)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships — connects back to HCP and User
    hcp = relationship("HCP", back_populates="interactions")
    followups = relationship("Followup", back_populates="interaction")