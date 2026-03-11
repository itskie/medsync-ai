from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.core.database import SessionLocal
from langchain_groq import ChatGroq
from app.core.config import settings
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

@tool
def edit_interaction(edit_data: str) -> str:
    """
    Edit an existing HCP interaction.
    Input: JSON string with interaction_id and fields to update.
    Uses LLM to understand natural language edit requests.
    """
    db: Session = SessionLocal()
    try:
        data = json.loads(edit_data)
        interaction_id = data.get("interaction_id")
        
        # Find interaction
        interaction = db.query(Interaction).filter(
            Interaction.id == interaction_id
        ).first()
        
        if not interaction:
            return json.dumps({
                "success": False,
                "error": f"Interaction {interaction_id} not found"
            })
        
        # Use LLM to understand what needs to be updated
        if data.get("natural_language_request"):
            update_prompt = f"""
            Current interaction data:
            - Topics: {interaction.topics_discussed}
            - Outcomes: {interaction.outcomes}
            - Sentiment: {interaction.sentiment}
            - Followup: {interaction.followup_actions}
            
            User wants to: {data.get('natural_language_request')}
            
            Return updated fields as JSON only. Example:
            {{"topics_discussed": "...", "outcomes": "..."}}
            """
            response = llm.invoke(update_prompt)
            try:
                updates = json.loads(response.content)
            except:
                updates = {}
        else:
            updates = {k: v for k, v in data.items() 
                      if k != "interaction_id" and v is not None}
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(interaction, key):
                setattr(interaction, key, value)
        
        db.commit()
        db.refresh(interaction)
        
        return json.dumps({
            "success": True,
            "interaction_id": interaction_id,
            "updated_fields": list(updates.keys()),
            "message": f"Interaction {interaction_id} updated successfully"
        })
        
    except Exception as e:
        db.rollback()
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()