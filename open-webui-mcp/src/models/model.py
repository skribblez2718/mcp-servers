"""Model-related data models."""

from pydantic import BaseModel as PydanticBaseModel, Field
from src.models.base import BaseModel


class ModelParameters(PydanticBaseModel):
    """Model parameters.

    Attributes:
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        max_tokens: Maximum tokens
        stop: Stop sequences
    """

    temperature: float | None = Field(0.7, description="Sampling temperature")
    top_p: float | None = Field(0.9, description="Nucleus sampling parameter")
    max_tokens: int | None = Field(2000, description="Maximum tokens")
    stop: list[str] | None = Field(None, description="Stop sequences")


class ModelCapabilities(PydanticBaseModel):
    """Model capabilities.

    Attributes:
        chat: Supports chat
        completion: Supports completion
        embedding: Supports embedding
        vision: Supports vision
    """

    chat: bool = Field(False, description="Supports chat")
    completion: bool = Field(False, description="Supports completion")
    embedding: bool = Field(False, description="Supports embedding")
    vision: bool = Field(False, description="Supports vision")


class ModelConfig(PydanticBaseModel):
    """Model configuration.

    Attributes:
        parameters: Default parameters
        capabilities: Model capabilities
        context_length: Context window length
    """

    parameters: ModelParameters = Field(default_factory=ModelParameters)
    capabilities: ModelCapabilities = Field(default_factory=ModelCapabilities)
    context_length: int = Field(4096, description="Context window length")


class Model(BaseModel):
    """Model resource.

    Attributes:
        id: Model ID
        name: Model name
        description: Model description
        provider: Provider (e.g., openai, anthropic)
        config: Model configuration
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    name: str = Field(..., description="Model name")
    description: str | None = Field(None, description="Model description")
    provider: str = Field(..., description="Provider")
    config: ModelConfig = Field(default_factory=ModelConfig)
