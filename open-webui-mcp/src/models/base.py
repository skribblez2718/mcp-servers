"""Base models for all Open WebUI entities.

Provides common fields and generic response wrappers.
"""

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime
from typing import TypeVar, Generic


T = TypeVar('T')


class BaseModel(PydanticBaseModel):
    """Base model with common fields for all entities.

    Attributes:
        id: Unique identifier
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class PaginatedResponse(PydanticBaseModel, Generic[T]):
    """Wrapper for paginated list responses.

    Attributes:
        items: List of items
        total: Total count of items
        limit: Items per page
        offset: Offset in results
        has_next: Whether next page exists
    """

    model_config = ConfigDict(from_attributes=True)

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total count")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Offset in results")
    has_next: bool = Field(..., description="Whether next page exists")


class DetailResponse(PydanticBaseModel, Generic[T]):
    """Wrapper for single item detail responses.

    Attributes:
        data: Response data
        metadata: Additional metadata
    """

    model_config = ConfigDict(from_attributes=True)

    data: T = Field(..., description="Response data")
    metadata: dict[str, object] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
