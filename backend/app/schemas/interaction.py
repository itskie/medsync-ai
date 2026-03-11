from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Data received when creating a new interaction
class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_type: Optional[str] = "meeting"
    date: str
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = "neutral"
    outcomes: Optional[str] = None
    followup_actions: Optional[str] = None

# Data received when updating an interaction
class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup_actions: Optional[str] = None
    ai_summary: Optional[str] = None

# Data returned in API response
class InteractionResponse(BaseModel):
    id: int
    hcp_id: int
    user_id: int
    interaction_type: str
    date: str
    time: Optional[str]
    attendees: Optional[str]
    topics_discussed: Optional[str]
    materials_shared: Optional[str]
    samples_distributed: Optional[str]
    sentiment: str
    ai_summary: Optional[str]
    outcomes: Optional[str]
    followup_actions: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# AI Chat message schema
class ChatMessage(BaseModel):
    message: str
    interaction_id: Optional[int] = None