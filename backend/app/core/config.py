"""
FloxAI Configuration - Optimized for Flox environments
"""
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """FloxAI settings - Flox-environment aware"""
    
    # Flox environment information
    flox_env_name: str = Field(default="", env="FLOX_ENV_NAME")
    flox_project_dir: str = Field(default="", env="FLOX_ENV_PROJECT_DIR")
    floxai_version: str = Field(default="1.0.0", env="FLOXAI_VERSION")
    
    # API Configuration
    api_port: int = Field(default=8000, env="FLOXAI_API_PORT")
    ui_port: int = Field(default=3000, env="FLOXAI_UI_PORT")
    log_level: str = Field(default="INFO", env="FLOXAI_LOG_LEVEL")
    
    # External API Keys
    claude_api_key: str = Field(default="", env="CLAUDE_API_KEY")
    
    # Flox-managed paths (use FLOX_ENV_PROJECT_DIR)
    db_path: str = Field(default="./data/floxai.db", env="FLOXAI_DB_PATH")
    vector_db_path: str = Field(default="./data/vector_db", env="FLOXAI_VECTOR_DB_PATH")
    docs_path: str = Field(default="./data/flox_docs", env="FLOXAI_DOCS_PATH")
    project_root: str = Field(default="", env="FLOXAI_PROJECT_ROOT")
    
    # Development flags
    dev_mode: bool = Field(default=False, env="FLOXAI_DEV_MODE")
    context_mode: bool = Field(default=False, env="FLOXAI_CONTEXT_MODE")
    current_env: str = Field(default="", env="FLOXAI_CURRENT_ENV") 
    project_type: str = Field(default="", env="FLOXAI_PROJECT_TYPE")
    
    # RAG Configuration
    rag_chunk_size: int = Field(default=500, env="RAG_CHUNK_SIZE")
    rag_chunk_overlap: int = Field(default=50, env="RAG_CHUNK_OVERLAP")
    rag_max_results: int = Field(default=5, env="RAG_MAX_RESULTS")
    
    # LLM Configuration
    llm_temperature: float = Field(default=0.1, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=2000, env="LLM_MAX_TOKENS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        directories = [
            Path(self.db_path).parent,
            Path(self.vector_db_path),
            Path(self.docs_path),
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def database_url(self) -> str:
        """Get SQLite database URL"""
        return f"sqlite:///{self.db_path}"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.dev_mode or os.getenv("FLOXAI_DEV_MODE", "").lower() == "true"
    
    @property
    def is_flox_environment(self) -> bool:
        """Check if running in a Flox environment"""
        return bool(os.getenv("FLOX_ENV") or (self.flox_env_name and self.flox_project_dir))
    
    def get_flox_info(self) -> dict:
        """Get Flox environment information"""
        # Extract environment name from FLOX_ENV path if FLOX_ENV_NAME is not set
        env_name = self.flox_env_name
        if not env_name and os.getenv("FLOX_ENV"):
            # Extract from path like /path/to/project/.flox/run/aarch64-darwin.floxai.dev
            flox_env = os.getenv("FLOX_ENV", "")
            if ".floxai.dev" in flox_env:
                env_name = "floxai"
            elif ".flox" in flox_env:
                # Extract from path structure
                parts = flox_env.split("/")
                for part in parts:
                    if ".flox" in part and ".dev" in part:
                        env_name = part.split(".")[-2]  # Get the part before .dev
                        break
        
        return {
            "environment_name": env_name or "unknown",
            "project_directory": self.flox_project_dir or os.getenv("FLOX_ENV_PROJECT", ""),
            "floxai_version": self.floxai_version,
            "is_flox_env": self.is_flox_environment,
            "python_path": os.getenv("PYTHONPATH", ""),
            "context_mode": self.context_mode,
            "current_env": self.current_env,
            "project_type": self.project_type,
            "system_info": {
                "platform": os.uname().sysname if hasattr(os, 'uname') else "unknown",
                "architecture": os.uname().machine if hasattr(os, 'uname') else "unknown"
            }
        }
    
    def get_context_info(self) -> dict:
        """Get context-aware information for development mode"""
        if not self.context_mode:
            return {"mode": "standalone"}
            
        context = {
            "mode": "context-aware",
            "environment": self.current_env,
            "project_types": self.project_type.strip().split() if self.project_type else [],
            "manifest_path": None,
            "project_files": []
        }
        
        # Check for manifest file
        if self.flox_project_dir:
            manifest_path = Path(self.flox_project_dir) / ".flox" / "env" / "manifest.toml"
            if manifest_path.exists():
                context["manifest_path"] = str(manifest_path)
        
        # Detect project files in current directory
        if self.flox_project_dir:
            project_dir = Path(self.flox_project_dir)
            common_files = [
                "package.json", "requirements.txt", "pyproject.toml", 
                "Cargo.toml", "go.mod", "Dockerfile", "docker-compose.yml",
                "Makefile", "CMakeLists.txt", "build.gradle", "pom.xml"
            ]
            
            for file in common_files:
                if (project_dir / file).exists():
                    context["project_files"].append(file)
        
        return context


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
