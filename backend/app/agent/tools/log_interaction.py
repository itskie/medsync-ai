from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.core.database import SessionLocal
from langchain_groq import ChatGroq
from app.core.config import settings
import json

# Initialize Groq LLM
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

@tool
def log_interaction(interaction_data: str) -> str:
    """
    Log a new HCP interaction. 
    Input: JSON string with interaction details.
    Uses LLM to extract and summarize key information.
    """
    db: Session = SessionLocal()
    try:
        # Parse input data
        data = json.loads(interaction_data)
        
        # Use LLM to generate AI summary of the interaction
        summary_prompt = f"""
        Summarize this HCP interaction in 2-3 sentences:
        HCP ID: {data.get('hcp_id')}
        Type: {data.get('interaction_type', 'meeting')}
        Topics: {data.get('topics_discussed', '')}
        Outcomes: {data.get('outcomes', '')}
        
        Also detect sentiment: positive, neutral, or negative.
        Return as JSON: {{"summary": "...", "sentiment": "..."}}
        """
        
        response = llm.invoke(summary_prompt)
        
        # Parse LLM response
        try:
            ai_result = json.loads(response.content)
            ai_summary = ai_result.get("summary", "")
            sentiment = ai_result.get("sentiment", "neutral")
        except:
            ai_summary = response.content
            sentiment = data.get("sentiment", "neutral")
        
        # Create interaction in database
        new_interaction = Interaction(
            hcp_id=data.get("hcp_id"),
            user_id=data.get("user_id", 1),
            interaction_type=data.get("interaction_type", "meeting"),
            date=data.get("date"),
            time=data.get("time"),
            attendees=data.get("attendees"),
            topics_discussed=data.get("topics_discussed"),
            materials_shared=data.get("materials_shared"),
            samples_distributed=data.get("samples_distributed"),
            sentiment=sentiment,
            ai_summary=ai_summary,
            outcomes=data.get("outcomes"),
            followup_actions=data.get("followup_actions")
        )
        
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        
        return json.dumps({
            "success": True,
            "interaction_id": new_interaction.id,
            "ai_summary": ai_summary,
            "sentiment": sentiment,
            "message": f"Interaction logged successfully with ID {new_interaction.id}"
        })
        
    except Exception as e:
        db.rollback()
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()