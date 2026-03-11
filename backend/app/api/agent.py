from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.interaction import ChatMessage
from app.agent.graph import chat_with_agent

router = APIRouter(prefix="/agent", tags=["AI Agent"])

@router.post("/chat")
def chat(message: ChatMessage, db: Session = Depends(get_db)):
    try:
        response = chat_with_agent(message.message)
        return {
            "success": True,
            "message": message.message,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools")
def get_tools():
    return {
        "tools": [
            {
                "name": "log_interaction",
                "description": "Log a new HCP interaction with AI summarization"
            },
            {
                "name": "edit_interaction",
                "description": "Edit an existing interaction using natural language"
            },
            {
                "name": "get_hcp_profile",
                "description": "Get complete HCP profile with interaction history"
            },
            {
                "name": "suggest_followup",
                "description": "Get AI-powered follow-up suggestions"
            },
            {
                "name": "analyze_sentiment",
                "description": "Analyze sentiment of interaction text"
            },
            {
                "name": "search_interactions",
                "description": "Search interactions using natural language"
            }
        ]
    }