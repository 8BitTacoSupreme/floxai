"""
FloxAI Backend - Showcasing Flox's Power for Development Environments
"""
import os
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import chat
from app.db.database import init_db
from app.services.rag_service import FloxRAGService
from app.services.llm_service import FloxLLMService
from app.core.config import get_settings

# Global services
rag_service = None
llm_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global rag_service, llm_service
    
    settings = get_settings()
    flox_info = settings.get_flox_info()
    context_info = settings.get_context_info()
    
    mode_label = "Context-Aware Development" if context_info["mode"] == "context-aware" else "Standalone"
    print(f"🌟 Starting FloxAI Backend - The Flox Development Co-pilot ({mode_label} Mode)")
    print("=" * 70)
    print(f"🔧 Flox Environment: {flox_info['environment_name']}")
    print(f"📁 Project Directory: {flox_info['project_directory']}")
    print(f"🏗️  Platform: {flox_info['system_info'].get('platform', 'unknown')} {flox_info['system_info'].get('architecture', 'unknown')}")
    print(f"🚀 FloxAI Version: {flox_info['floxai_version']}")
    print(f"🎯 Mode: {mode_label}")
    
    if context_info["mode"] == "context-aware":
        print(f"   📦 Project Types: {', '.join(context_info['project_types']) if context_info['project_types'] else 'None detected'}")
        print(f"   📄 Project Files: {', '.join(context_info['project_files']) if context_info['project_files'] else 'None detected'}")
        if context_info["manifest_path"]:
            print("   ✅ Flox manifest found - environment analysis enabled")
    
    print("=" * 70)
    
    # Initialize database
    init_db()
    print("📚 Database initialized with Flox environment tracking")
    
    # Initialize services
    try:
        rag_service = FloxRAGService()
        await rag_service.initialize()
        print("🧠 Flox RAG service initialized - ready to help with Flox questions!")

        print("🔍 Debug: About to create FloxLLMService...")
        llm_service = FloxLLMService()
        print("🔍 Debug: FloxLLMService created, about to initialize...")
        await llm_service.initialize()
        print(f"🔍 Debug: LLM initialization complete, is_ready = {llm_service.is_ready}")

        if llm_service.is_ready:
            print("🤖 Claude integration ready - FloxAI co-pilot online!")
        else:
            print("⚠️  Claude API not configured - set CLAUDE_API_KEY for full functionality")

    except Exception as e:
        print(f"⚠️  Service initialization warning: {e}")
        import traceback
        traceback.print_exc()
    
    # Store services in app state
    app.state.rag_service = rag_service
    app.state.llm_service = llm_service
    
    print("")
    print("✅ FloxAI Backend Ready!")
    print(f"   🌐 API Server: http://localhost:{settings.api_port}")
    print(f"   📖 API Docs: http://localhost:{settings.api_port}/docs")
    print(f"   ❤️  Health Check: http://localhost:{settings.api_port}/health")
    print("")
    print("🎯 FloxAI showcases Flox's power for reproducible development environments!")
    print("")
    
    yield
    
    # Cleanup
    print("🛑 Shutting down FloxAI backend...")
    if rag_service:
        await rag_service.cleanup()
    if llm_service:
        await llm_service.cleanup()
    print("👋 FloxAI backend stopped cleanly")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="FloxAI API - The Flox Development Co-pilot",
        description="Showcasing Flox's power for reproducible, cross-platform development environments", 
        version=settings.floxai_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000", 
            "http://127.0.0.1:3000", 
            "http://localhost:4173",
            "http://127.0.0.1:4173"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(chat.router, prefix="/api/chat", tags=["FloxAI Chat"])
    
    # Enhanced health check with Flox information
    @app.get("/health", tags=["System"])
    async def health_check():
        """Health check with Flox environment details"""
        flox_info = settings.get_flox_info()
        context_info = settings.get_context_info()
        
        return {
            "status": "healthy",
            "service": "FloxAI - The Flox Development Co-pilot",
            "version": settings.floxai_version,
            "mode": context_info["mode"],
            "flox_environment": {
                "name": flox_info["environment_name"],
                "is_flox_env": flox_info["is_flox_env"],
                "platform": f"{flox_info['system_info'].get('platform', 'unknown')} {flox_info['system_info'].get('architecture', 'unknown')}"
            },
            "context": context_info if context_info["mode"] == "context-aware" else None,
            "services": {
                "rag": rag_service is not None and rag_service.is_ready,
                "llm": llm_service is not None and llm_service.is_ready,
            },
            "endpoints": {
                "chat": "/api/chat/query",
                "docs": "/docs",
                "flox_stats": "/api/chat/flox-stats"
            }
        }
    
    # Root endpoint with Flox branding
    @app.get("/", tags=["System"])
    async def root():
        """Root endpoint showcasing Flox integration"""
        flox_info = settings.get_flox_info()
        
        return {
            "service": "FloxAI - The Flox Development Co-pilot",
            "version": settings.floxai_version,
            "description": "Showcasing Flox's power for reproducible, cross-platform development environments",
            "flox_environment": flox_info["environment_name"],
            "platform": f"{flox_info['system_info'].get('platform', 'unknown')} {flox_info['system_info'].get('architecture', 'unknown')}",
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "chat": "/api/chat/query",
                "flox_stats": "/api/chat/flox-stats"
            },
            "message": "Welcome to FloxAI! Ask me anything about Flox development. 🚀"
        }
    
    return app

def main():
    """Main entry point"""
    settings = get_settings()
    
    if not settings.is_flox_environment:
        print("⚠️  Warning: FloxAI is designed to run in a Flox environment")
        print("   For the best experience, run: flox activate")
        print("")
    
    app = create_app()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.is_development,
        log_level=settings.log_level.lower()
    )

# Create the app instance for uvicorn
app = create_app()

if __name__ == "__main__":
    main()
