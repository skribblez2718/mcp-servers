"""Data models for Open WebUI MCP Server."""

from src.models.base import BaseModel, PaginatedResponse, DetailResponse
from src.models.chat import Chat, Message, MessageContent
from src.models.model import Model, ModelConfig
from src.models.user import User, UserProfile
from src.models.errors import ErrorResponse

__all__ = [
    "BaseModel",
    "PaginatedResponse",
    "DetailResponse",
    "Chat",
    "Message",
    "MessageContent",
    "Model",
    "ModelConfig",
    "User",
    "UserProfile",
    "ErrorResponse",
]
