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
def analyze_sentiment(text_data: str) -> str:
    """
    Analyze sentiment of HCP interaction text.
    Input: JSON with 'text' and optional 'interaction_id'.
    Returns sentiment analysis with reasoning and updates DB if interaction_id provided.
    """
    db: Session = SessionLocal()
    try:
        data = json.loads(text_data)
        text = data.get("text", "")
        interaction_id = data.get("interaction_id")

        # Use LLM to analyze sentiment
        sentiment_prompt = f"""
        You are analyzing a pharmaceutical sales interaction.
        Analyze the sentiment of this text and return ONLY JSON:
        
        Text: "{text}"
        
        Return:
        {{
            "sentiment": "positive" or "neutral" or "negative",
            "confidence": 0.0 to 1.0,
            "reasoning": "brief explanation",
            "key_signals": ["signal1", "signal2"]
        }}
        """

        response = llm.invoke(sentiment_prompt)

        try:
            result = json.loads(response.content)
        except:
            result = {
                "sentiment": "neutral",
                "confidence": 0.5,
                "reasoning": response.content,
                "key_signals": []
            }

        # Update interaction in DB if ID provided
        if interaction_id:
            interaction = db.query(Interaction).filter(
                Interaction.id == int(interaction_id)
            ).first()
            if interaction:
                interaction.sentiment = result.get("sentiment", "neutral")
                db.commit()
                result["interaction_updated"] = True
                result["interaction_id"] = interaction_id

        return json.dumps({
            "success": True,
            "analysis": result
        })

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()