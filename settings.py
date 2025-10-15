# settings.py
import os
from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        extra="ignore",      # ignore unknown env vars
        env_file=".env",     # load environment variables from .env
        env_file_encoding="utf-8"
    )

    # App info
    APP_NAME: str = "RAG Service"
    DATABASE_URL: str = "sqlite:///./ragdb.sqlite"

    # Chroma vector store
    CHROMA_DIR: ClassVar[str] = "./chroma_db"  # ClassVar avoids being treated as a model field

    # Document processing limits
    MAX_DOCS: int = 20
    MAX_PAGES_PER_DOC: int = 1000
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

    # LLM / API keys
    LLM_PROVIDER: str = "gemini"   # or "openai"
    GEMINI_API_KEY: str            # required
    OPENAI_API_KEY: str = ""       # optional if using OpenAI
    HUGGINGFACE_API_KEY: str       # required for embeddings

    # Query / retrieval settings
    MAX_RETRIEVALS: int = 5

# Instantiate settings
settings = Settings()
