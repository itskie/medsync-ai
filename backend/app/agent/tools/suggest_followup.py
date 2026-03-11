from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.models.followup import Followup
from app.core.database import SessionLocal
from langchain_groq import ChatGroq
from app.core.config import settings
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

@tool
def suggest_followup(interaction_id: str) -> str:
    """
    Suggest AI-powered follow-up actions for an interaction.
    Input: Interaction ID as string.
    Returns 3 actionable follow-up suggestions and saves them to DB.
    """
    db: Session = SessionLocal()
    try:
        interaction_id_int = int(interaction_id)
        
        # Get interaction details
        interaction = db.query(Interaction).filter(
            Interaction.id == interaction_id_int
        ).first()
        
        if not interaction:
            return json.dumps({
                "success": False,
                "error": f"Interaction {interaction_id} not found"
            })
        
        # Get HCP details
        hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
        
        # Use LLM to generate followup suggestions
        followup_prompt = f"""
        You are a pharmaceutical sales expert.
        Based on this HCP interaction, suggest 3 specific follow-up actions.
        
        HCP: {hcp.name if hcp else 'Unknown'} ({hcp.specialization if hcp else ''})
        Interaction Type: {interaction.interaction_type}
        Topics Discussed: {interaction.topics_discussed}
        Sentiment: {interaction.sentiment}
        Outcomes: {interaction.outcomes}
        Materials Shared: {interaction.materials_shared}
        
        Return ONLY a JSON array with 3 suggestions:
        [
            {{"action": "...", "due_days": 7, "priority": "high"}},
            {{"action": "...", "due_days": 14, "priority": "medium"}},
            {{"action": "...", "due_days": 30, "priority": "low"}}
        ]
        """
        
        response = llm.invoke(followup_prompt)
        
        try:
            suggestions = json.loads(response.content)
        except:
            suggestions = [
                {"action": "Schedule follow-up meeting", "due_days": 7, "priority": "high"},
                {"action": "Send product brochure", "due_days": 14, "priority": "medium"},
                {"action": "Check on sample usage", "due_days": 30, "priority": "low"}
            ]
        
        # Save followups to database
        saved_followups = []
        for suggestion in suggestions:
            followup = Followup(
                interaction_id=interaction_id_int,
                hcp_id=interaction.hcp_id,
                suggested_action=suggestion.get("action"),
                status="pending"
            )
            db.add(followup)
            saved_followups.append(suggestion)
        
        db.commit()
        
        return json.dumps({
            "success": True,
            "interaction_id": interaction_id_int,
            "suggestions": saved_followups,
            "message": f"3 follow-up actions suggested and saved!"
        })
        
    except Exception as e:
        db.rollback()
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()