"""Chat-related data models."""

from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime
from src.models.base import BaseModel


class MessageContent(PydanticBaseModel):
    """Content of a chat message.

    Attributes:
        text: Message text
        type: Content type (text, image, etc.)
    """

    text: str = Field(..., description="Message text")
    type: str = Field(default="text", description="Content type")


class Message(BaseModel):
    """Chat message model.

    Attributes:
        id: Message ID
        chat_id: Parent chat ID
        role: Message role (user, assistant, system)
        content: Message content
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    chat_id: str = Field(..., description="Parent chat ID")
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    metadata: dict[str, object] = Field(default_factory=dict)


class Participant(PydanticBaseModel):
    """Chat participant.

    Attributes:
        user_id: User ID
        role: Participant role
        joined_at: Join timestamp
    """

    user_id: str = Field(..., description="User ID")
    role: str = Field(default="member", description="Participant role")
    joined_at: datetime = Field(..., description="Join timestamp")


class ChatSettings(PydanticBaseModel):
    """Chat-specific settings.

    Attributes:
        model: Model to use
        temperature: Sampling temperature
        max_tokens: Maximum tokens
        system_prompt: System prompt
    """

    model: str | None = Field(None, description="Model to use")
    temperature: float | None = Field(0.7, description="Sampling temperature")
    max_tokens: int | None = Field(2000, description="Maximum tokens")
    system_prompt: str | None = Field(None, description="System prompt")


class ChatMetadata(PydanticBaseModel):
    """Chat metadata.

    Attributes:
        title: Chat title
        description: Chat description
        tags: Tags
        archived: Whether archived
        shared: Whether shared
    """

    title: str | None = Field(None, description="Chat title")
    description: str | None = Field(None, description="Chat description")
    tags: list[str] = Field(default_factory=list, description="Tags")
    archived: bool = Field(False, description="Whether archived")
    shared: bool = Field(False, description="Whether shared")


class Chat(BaseModel):
    """Chat resource model.

    Attributes:
        id: Chat ID
        user_id: Owner user ID
        title: Chat title
        messages: List of messages
        participants: List of participants
        settings: Chat settings
        metadata: Chat metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    user_id: str = Field(..., description="Owner user ID")
    title: str = Field(..., description="Chat title")
    messages: list[Message] = Field(default_factory=list)
    participants: list[Participant] = Field(default_factory=list)
    settings: ChatSettings = Field(default_factory=ChatSettings)
    metadata: ChatMetadata = Field(default_factory=ChatMetadata)
