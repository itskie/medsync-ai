from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.core.database import SessionLocal
import json

@tool
def get_hcp_profile(hcp_id: str) -> str:
    """
    Get complete HCP profile with interaction history.
    Input: HCP ID as string.
    Returns full profile with past interactions and sentiment trend.
    """
    db: Session = SessionLocal()
    try:
        hcp_id_int = int(hcp_id)
        
        # Get HCP details
        hcp = db.query(HCP).filter(HCP.id == hcp_id_int).first()
        if not hcp:
            return json.dumps({
                "success": False,
                "error": f"HCP {hcp_id} not found"
            })
        
        # Get all interactions for this HCP
        interactions = db.query(Interaction).filter(
            Interaction.hcp_id == hcp_id_int
        ).all()
        
        # Calculate sentiment trend
        sentiments = [i.sentiment for i in interactions if i.sentiment]
        positive = sentiments.count("positive")
        neutral = sentiments.count("neutral")
        negative = sentiments.count("negative")
        
        # Build interaction history
        interaction_history = []
        for i in interactions:
            interaction_history.append({
                "id": i.id,
                "date": i.date,
                "type": i.interaction_type,
                "topics": i.topics_discussed,
                "sentiment": i.sentiment,
                "summary": i.ai_summary,
                "outcomes": i.outcomes
            })
        
        return json.dumps({
            "success": True,
            "hcp": {
                "id": hcp.id,
                "name": hcp.name,
                "specialization": hcp.specialization,
                "hospital": hcp.hospital,
                "city": hcp.city,
                "email": hcp.email,
                "phone": hcp.phone
            },
            "stats": {
                "total_interactions": len(interactions),
                "sentiment_breakdown": {
                    "positive": positive,
                    "neutral": neutral,
                    "negative": negative
                }
            },
            "interaction_history": interaction_history
        })
        
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()