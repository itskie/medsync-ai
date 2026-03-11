from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionResponse

router = APIRouter(prefix="/interactions", tags=["Interactions"])

# Get all interactions
@router.get("/", response_model=List[InteractionResponse])
def get_all_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()

# Get single interaction
@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    return interaction

# Get all interactions for a specific HCP
@router.get("/hcp/{hcp_id}", response_model=List[InteractionResponse])
def get_hcp_interactions(hcp_id: int, db: Session = Depends(get_db)):
    return db.query(Interaction).filter(Interaction.hcp_id == hcp_id).all()

# Create new interaction
@router.post("/", response_model=InteractionResponse)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    # Verify HCP exists
    hcp = db.query(HCP).filter(HCP.id == data.hcp_id).first()
    if not hcp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found"
        )
    new_interaction = Interaction(
        **data.model_dump(),
        user_id=1  # Hardcoded for now, will use JWT later
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return new_interaction

# Update interaction
@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(interaction_id: int, data: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(interaction, key, value)
    db.commit()
    db.refresh(interaction)
    return interaction

# Delete interaction
@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    db.delete(interaction)
    db.commit()
    return {"message": "Interaction deleted successfully"}