"""
Configuration settings for YouTube Analysis Agent
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    gemini_api_key: str
    anthropic_api_key: str

    # Gemini Configuration
    gemini_model: str = "gemini-1.5-pro"

    # Claude Configuration
    claude_model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 8000

    # Application Settings
    log_level: str = "INFO"
    output_dir: Path = Path("./output")

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
