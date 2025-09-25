"""
FloxAI Chat API - Flox-aware conversation endpoints
"""
import time
import uuid
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.db.database import save_chat_message, get_chat_history, save_feedback, get_flox_stats
from app.services.learning_service import FloxLearningService
from app.core.config import get_settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    mode: str = "flox_expert"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    message_id: int
    sources: List[dict] = []
    model: str = "claude-3-sonnet-20240229"
    response_time: float
    flox_info: dict = {}

class FeedbackRequest(BaseModel):
    message_id: int
    session_id: str
    worked: bool = False

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest, app_request: Request):
    """Main chat endpoint with Flox awareness"""
    start_time = time.time()
    
    try:
        settings = get_settings()
        
        # Get services from app state
        rag_service = getattr(app_request.app.state, 'rag_service', None)
        llm_service = getattr(app_request.app.state, 'llm_service', None)
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Save user message
        save_chat_message(session_id, "user", request.message)
        
        # Get context from RAG if available
        context = ""
        sources = []
        if rag_service and rag_service.is_ready:
            context, sources = await rag_service.get_context_for_query(request.message)
        
        # Generate response
        if llm_service and llm_service.is_ready:
            llm_response = await llm_service.chat_with_context(
                user_message=request.message,
                context=context
            )
            response_text = llm_response["response"]
            model = llm_response.get("model", "claude-3-sonnet-20240229")
        else:
            response_text = """FloxAI is starting up! 🚀

I'm your Flox development co-pilot, designed to help you master Flox and showcase its incredible capabilities.

**To get started:**
1. Make sure you have set your CLAUDE_API_KEY: `export CLAUDE_API_KEY=your_key_here`
2. Restart FloxAI: `floxybotdev`

**What I can help with:**
- 🔧 Creating and optimizing manifest.toml files
- 🌍 Cross-platform environment setup
- 📦 Package management and dependencies  
- 🚀 Service orchestration
- 🐳 Converting from Docker to Flox
- 💡 Flox best practices and troubleshooting

**Current Flox Environment:**
- Name: {settings.flox_env_name}
- Project: {settings.flox_project_dir}
- Platform: Running on Flox! 🎉

Try asking me: "How do I add Python packages to my Flox environment?" or "Show me a manifest.toml example for a web app"
            """.format(settings=settings)
            model = "floxai-local"
        
        response_time = time.time() - start_time
        
        # Save assistant message
        message_id = save_chat_message(
            session_id, "assistant", response_text, model, response_time
        )
        
        # Get Flox environment info
        flox_info = settings.get_flox_info()
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            message_id=message_id,
            sources=sources[:3],
            model=model,
            response_time=response_time,
            flox_info=flox_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FloxAI chat error: {str(e)}")

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for learning"""
    try:
        save_feedback(
            session_id=feedback.session_id,
            message_id=feedback.message_id,
            query_text="",  # Simplified for MVP
            response_text="",  # Simplified for MVP  
            worked=feedback.worked
        )
        return {"status": "success", "message": "Feedback recorded! FloxAI learns from your input."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_session_history(session_id: str):
    """Get chat history"""
    try:
        history = get_chat_history(session_id)
        return {"session_id": session_id, "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/flox-stats")
async def get_flox_environment_stats():
    """Get Flox-specific statistics and environment info"""
    try:
        return get_flox_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning/insights")
async def get_learning_insights():
    """Get learning insights from user feedback"""
    try:
        learning_service = FloxLearningService()
        insights = learning_service.generate_learning_insights()
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/learning/update")
async def update_knowledge_from_feedback():
    """Update knowledge base based on feedback patterns"""
    try:
        learning_service = FloxLearningService()
        summary = learning_service.update_knowledge_base_from_feedback()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning/stats")
async def get_learning_stats():
    """Get learning statistics"""
    try:
        learning_service = FloxLearningService()
        stats = learning_service.get_learning_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
