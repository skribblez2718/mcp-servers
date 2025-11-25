"""User-related data models."""

from pydantic import BaseModel as PydanticBaseModel, Field, EmailStr
from datetime import datetime
from src.models.base import BaseModel


class Permission(PydanticBaseModel):
    """User permission.

    Attributes:
        resource: Resource type
        action: Action (read, write, delete)
        granted: Whether granted
    """

    resource: str = Field(..., description="Resource type")
    action: str = Field(..., description="Action")
    granted: bool = Field(..., description="Whether granted")


class Role(PydanticBaseModel):
    """User role.

    Attributes:
        name: Role name
        permissions: List of permissions
    """

    name: str = Field(..., description="Role name")
    permissions: list[Permission] = Field(default_factory=list)


class UserSettings(PydanticBaseModel):
    """User settings.

    Attributes:
        theme: UI theme
        language: Preferred language
        notifications: Notification preferences
    """

    theme: str = Field("light", description="UI theme")
    language: str = Field("en", description="Preferred language")
    notifications: dict[str, bool] = Field(default_factory=dict)


class UserProfile(PydanticBaseModel):
    """User profile information.

    Attributes:
        display_name: Display name
        avatar_url: Avatar URL
        bio: User bio
    """

    display_name: str | None = Field(None, description="Display name")
    avatar_url: str | None = Field(None, description="Avatar URL")
    bio: str | None = Field(None, description="User bio")


class User(BaseModel):
    """User resource.

    Attributes:
        id: User ID
        email: Email address
        username: Username
        profile: User profile
        role: User role
        settings: User settings
        is_active: Whether account is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    email: EmailStr = Field(..., description="Email address")
    username: str = Field(..., description="Username")
    profile: UserProfile = Field(default_factory=UserProfile)
    role: str = Field("user", description="User role")
    settings: UserSettings = Field(default_factory=UserSettings)
    is_active: bool = Field(True, description="Whether account is active")
