from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.core.database import SessionLocal
from langchain_groq import ChatGroq
from app.core.config import settings
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

@tool
def search_interactions(query: str) -> str:
    """
    Search interactions using natural language.
    Input: Natural language query like 'Show all meetings with Dr. Sharma last month'
    Returns matching interactions from database.
    """
    db: Session = SessionLocal()
    try:
        # Get all interactions with HCP details
        interactions = db.query(Interaction, HCP).join(
            HCP, Interaction.hcp_id == HCP.id
        ).all()

        # Build context for LLM
        interactions_data = []
        for interaction, hcp in interactions:
            interactions_data.append({
                "id": interaction.id,
                "hcp_name": hcp.name,
                "hcp_specialization": hcp.specialization,
                "type": interaction.interaction_type,
                "date": interaction.date,
                "topics": interaction.topics_discussed,
                "sentiment": interaction.sentiment,
                "outcomes": interaction.outcomes,
                "summary": interaction.ai_summary
            })

        # Use LLM to filter relevant interactions
        search_prompt = f"""
        You are searching through HCP interaction records.
        
        User Query: "{query}"
        
        Available Interactions:
        {json.dumps(interactions_data, indent=2)}
        
        Return ONLY a JSON array of matching interaction IDs and brief reasons:
        [
            {{"id": 1, "reason": "matches because..."}},
        ]
        If no matches, return empty array: []
        """

        response = llm.invoke(search_prompt)

        try:
            matches = json.loads(response.content)
        except:
            matches = []

        # Get full details of matched interactions
        matched_ids = [m.get("id") for m in matches]
        results = []
        for interaction, hcp in interactions:
            if interaction.id in matched_ids:
                reason = next(
                    (m.get("reason") for m in matches if m.get("id") == interaction.id), ""
                )
                results.append({
                    "id": interaction.id,
                    "hcp_name": hcp.name,
                    "date": interaction.date,
                    "type": interaction.interaction_type,
                    "topics": interaction.topics_discussed,
                    "sentiment": interaction.sentiment,
                    "summary": interaction.ai_summary,
                    "match_reason": reason
                })

        return json.dumps({
            "success": True,
            "query": query,
            "total_results": len(results),
            "results": results
        })

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()