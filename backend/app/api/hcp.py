from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse

router = APIRouter(prefix="/hcps", tags=["HCPs"])

# Get all HCPs
@router.get("/", response_model=List[HCPResponse])
def get_all_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

# Get single HCP by ID
@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found"
        )
    return hcp

# Create new HCP
@router.post("/", response_model=HCPResponse)
def create_hcp(hcp_data: HCPCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    if hcp_data.email:
        existing = db.query(HCP).filter(HCP.email == hcp_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="HCP with this email already exists"
            )
    new_hcp = HCP(**hcp_data.model_dump())
    db.add(new_hcp)
    db.commit()
    db.refresh(new_hcp)
    return new_hcp

# Update HCP
@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(hcp_id: int, hcp_data: HCPUpdate, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found"
        )
    # Update only provided fields
    for key, value in hcp_data.model_dump(exclude_unset=True).items():
        setattr(hcp, key, value)
    db.commit()
    db.refresh(hcp)
    return hcp

# Delete HCP
@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found"
        )
    db.delete(hcp)
    db.commit()
    return {"message": "HCP deleted successfully"}