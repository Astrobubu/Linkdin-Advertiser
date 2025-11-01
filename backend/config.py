from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str
    database_url: str = "sqlite:///./linkedin_advertiser.db"
    environment: str = "development"

    # OpenAI settings
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.7
    max_tokens: int = 4000

    # Agent settings
    max_loop_iterations: int = 3
    loop_keywords: list[str] = [
        "needs_refinement",
        "unclear_value_prop",
        "iterate",
        "needs_improvement",
        "reconsider",
        "weak_positioning"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
