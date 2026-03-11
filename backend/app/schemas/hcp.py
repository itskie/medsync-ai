from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Data received when creating a new HCP
class HCPCreate(BaseModel):
    name: str
    specialization: str
    hospital: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# Data received when updating an HCP
class HCPUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# Data returned in API response
class HCPResponse(BaseModel):
    id: int
    name: str
    specialization: str
    hospital: Optional[str]
    city: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True