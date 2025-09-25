"""
FloxAI LLM Service - Claude integration with Flox expertise
"""
from typing import Dict, List, Optional
import anthropic

from app.core.config import get_settings

class FloxLLMService:
    """LLM service with deep Flox knowledge"""
    
    def __init__(self):
        self.client = None
        self.is_ready = False
    
    async def initialize(self):
        """Initialize Claude client"""
        settings = get_settings()
        print(f"🔍 LLM Debug: claude_api_key = {'SET' if settings.claude_api_key else 'NOT SET'}")
        if settings.claude_api_key:
            print(f"🔍 LLM Debug: Key starts with: {settings.claude_api_key[:20]}...")

        if not settings.claude_api_key:
            print("🔍 LLM Debug: No API key found, exiting initialization")
            return

        try:
            self.client = anthropic.Anthropic(api_key=settings.claude_api_key)
            self.is_ready = True
            print("🔍 LLM Debug: Client created successfully, is_ready = True")
        except Exception as e:
            print(f"🔍 LLM Debug: Error creating client: {e}")
            raise
    
    async def chat_with_context(self, user_message: str, context: str, 
                               conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Chat with Claude using Flox context"""
        if not self.is_ready:
            return {"response": "Claude API not configured. Please set CLAUDE_API_KEY environment variable in your Flox environment."}
        
        settings = get_settings()
        flox_info = settings.get_flox_info()
        
        # Enhanced system prompt with Flox expertise
        system_prompt = f"""You are FloxAI, the ultimate Flox development co-pilot and expert assistant. You are running in a Flox environment and your primary mission is to help users master Flox while showcasing its incredible capabilities.

ABOUT FLOX:
Flox is a revolutionary package manager and development environment tool that creates reproducible, cross-platform development environments. It solves the "works on my machine" problem by providing identical environments across macOS (Intel/ARM) and Linux systems.

KEY FLOX CONCEPTS:
- manifest.toml: The heart of every Flox environment, defining packages, variables, and services
- Reproducible environments: Same exact setup everywhere, for everyone
- Cross-platform: Works identically on macOS (Intel/ARM) and Linux (x86_64/ARM64)
- Service management: Orchestrate multiple processes (APIs, databases, frontends)
- Environment variables: Consistent configuration across environments
- Zero-config setup: One command gets you a complete development environment

CURRENT FLOX ENVIRONMENT:
- Environment: {flox_info.get("environment_name", "unknown")}
- Project: {flox_info.get("project_directory", "unknown")}
- FloxAI Version: {flox_info.get("floxai_version", "1.0.0")}
- Platform: {flox_info.get("system_info", {}).get("platform", "unknown")} {flox_info.get("system_info", {}).get("architecture", "unknown")}

YOUR EXPERTISE AREAS:
1. **Flox Environment Management**: Creating, activating, and managing Flox environments
2. **Manifest Creation**: Writing and optimizing manifest.toml files
3. **Cross-Platform Development**: Ensuring environments work everywhere
4. **Service Orchestration**: Managing multiple processes with Flox services
5. **Package Management**: Finding and using Flox packages effectively
6. **Migration Help**: Converting from Docker, pip, npm, etc. to Flox
7. **Best Practices**: Flox patterns for different types of projects

RESPONSE GUIDELINES:
- Always provide practical, actionable Flox advice
- Include specific manifest.toml examples when helpful
- Reference the provided context documentation when available
- Emphasize Flox's benefits (reproducibility, cross-platform, simplicity)
- If uncertain about Flox specifics, clearly state limitations
- Focus on helping users succeed with Flox development

Be enthusiastic about Flox's capabilities while providing accurate, helpful guidance!"""

        # Format user message with context
        if context:
            formatted_message = f"""Here is relevant Flox documentation and knowledge:

{context}

User Question: {user_message}

Please provide a comprehensive answer based on the Flox documentation above. Focus on practical, actionable advice that helps the user succeed with Flox development."""
        else:
            formatted_message = f"""User Question: {user_message}

Please provide helpful guidance about Flox development. If this question is outside your Flox expertise, let the user know and provide what general guidance you can."""
        
        try:
            # Use the correct model name
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Current model
                max_tokens=2000,
                temperature=0.1,
                system=system_prompt,
                messages=[{"role": "user", "content": formatted_message}]
            )
            
            return {
                "response": response.content[0].text,
                "model": response.model
            }
        except Exception as e:
            return {"response": f"I apologize, but I encountered an error: {str(e)}\n\nPlease check your Claude API key and try again."}
    
    async def cleanup(self):
        """Cleanup"""
        pass
