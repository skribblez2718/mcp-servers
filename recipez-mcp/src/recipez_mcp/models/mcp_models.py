"""MCP tool input models with Python-idiomatic snake_case parameters.

These models define the user-facing interface for MCP tools.
Parameters use snake_case (Python convention) and are transformed to camelCase for API calls.
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


# ==================== PROFILE MODELS ====================

class UpdateProfileImageInput(BaseModel):
    """Input for updating profile image."""

    image_url: str = Field(..., description="URL to the new profile image")


class CreateApiKeyInput(BaseModel):
    """Input for creating a managed API key."""

    name: str = Field(..., min_length=1, max_length=100, description="User-provided name for the API key")
    scopes: List[str] = Field(..., min_items=1, description="Permission scopes for the API key")
    expires_at: Optional[str] = Field(None, description="Expiration timestamp (ISO 8601 format)")
    never_expires: bool = Field(False, description="Set to true for keys that never expire")


class DeleteApiKeyInput(BaseModel):
    """Input for deleting an API key."""

    api_key_id: str = Field(..., description="UUID of the API key to delete")

    @field_validator("api_key_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


# ==================== RECIPE MODELS ====================

class CreateRecipeInput(BaseModel):
    """Input for creating a recipe."""

    recipe_name: str = Field(..., min_length=2, max_length=50)
    recipe_description: str = Field(..., min_length=2, max_length=500)
    recipe_category_id: str = Field(..., description="Category UUID")
    recipe_image_id: str = Field(..., description="Image UUID")
    recipe_author_id: str = Field(..., description="Author UUID")

    @field_validator("recipe_category_id", "recipe_image_id", "recipe_author_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class UpdateRecipeInput(BaseModel):
    """Input for updating a recipe."""

    recipe_id: str = Field(..., description="Recipe UUID to update")
    recipe_name: Optional[str] = Field(None, min_length=2, max_length=50)
    recipe_description: Optional[str] = Field(None, min_length=2, max_length=500)
    recipe_category_id: Optional[str] = Field(None, description="Category UUID")
    recipe_image_id: Optional[str] = Field(None, description="Image UUID")

    @field_validator("recipe_id", "recipe_category_id", "recipe_image_id")
    @classmethod
    def validate_uuid(cls, v: Optional[str]) -> Optional[str]:
        """Validate UUID format."""
        if v is None:
            return v
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class GetRecipeInput(BaseModel):
    """Input for getting a single recipe."""

    recipe_id: str = Field(..., description="Recipe UUID")

    @field_validator("recipe_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class DeleteRecipeInput(BaseModel):
    """Input for deleting a recipe."""

    recipe_id: str = Field(..., description="Recipe UUID to delete")

    @field_validator("recipe_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class BatchUpdateCategoryInput(BaseModel):
    """Input for batch updating recipe categories."""

    updates: List[dict] = Field(..., min_items=1, description="List of {recipe_id, category_id} pairs")


# ==================== CATEGORY MODELS ====================

class CreateCategoryInput(BaseModel):
    """Input for creating a category."""

    category_name: str = Field(..., min_length=2, max_length=50)
    author_id: str = Field(..., description="Author UUID")

    @field_validator("author_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class GetCategoryInput(BaseModel):
    """Input for getting a category."""

    category_id: str = Field(..., description="Category UUID")

    @field_validator("category_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class UpdateCategoryInput(BaseModel):
    """Input for updating a category."""

    category_id: str = Field(..., description="Category UUID")
    category_name: str = Field(..., min_length=2, max_length=50)

    @field_validator("category_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class DeleteCategoryInput(BaseModel):
    """Input for deleting a category."""

    category_id: str = Field(..., description="Category UUID to delete")
    preview: bool = Field(False, description="If true, only preview deletion effects")

    @field_validator("category_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


# ==================== INGREDIENT MODELS ====================

class IngredientInput(BaseModel):
    """Single ingredient input."""

    ingredient_name: str = Field(..., min_length=2, max_length=50)
    ingredient_quantity: str = Field(..., description="Numeric quantity (e.g., '1', '1.5', '1/2', '1-2')")
    ingredient_measurement: str = Field(..., description="Measurement unit")


class CreateIngredientsInput(BaseModel):
    """Input for batch creating ingredients."""

    recipe_id: str = Field(..., description="Recipe UUID")
    author_id: str = Field(..., description="Author UUID")
    ingredients: List[IngredientInput] = Field(..., min_items=1)

    @field_validator("recipe_id", "author_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class GetIngredientInput(BaseModel):
    """Input for getting an ingredient."""

    ingredient_id: str = Field(..., description="Ingredient UUID")

    @field_validator("ingredient_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class UpdateIngredientInput(BaseModel):
    """Input for updating an ingredient."""

    ingredient_id: str = Field(..., description="Ingredient UUID")
    ingredient_name: str = Field(..., min_length=2, max_length=50)
    ingredient_quantity: str = Field(..., description="Numeric quantity")
    ingredient_measurement: str = Field(..., description="Measurement unit")

    @field_validator("ingredient_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class DeleteIngredientInput(BaseModel):
    """Input for deleting an ingredient."""

    ingredient_id: str = Field(..., description="Ingredient UUID to delete")

    @field_validator("ingredient_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


# ==================== STEP MODELS ====================

class StepInput(BaseModel):
    """Single step input."""

    step_description: str = Field(..., min_length=2, description="Step instruction text")


class CreateStepsInput(BaseModel):
    """Input for batch creating steps."""

    recipe_id: str = Field(..., description="Recipe UUID")
    author_id: str = Field(..., description="Author UUID")
    steps: List[StepInput] = Field(..., min_items=1)

    @field_validator("recipe_id", "author_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class GetStepsByRecipeInput(BaseModel):
    """Input for getting steps by recipe ID."""

    recipe_id: str = Field(..., description="Recipe UUID")

    @field_validator("recipe_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class UpdateStepInput(BaseModel):
    """Input for updating a step."""

    step_id: str = Field(..., description="Step UUID")
    step_description: str = Field(..., min_length=2)

    @field_validator("step_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class DeleteStepInput(BaseModel):
    """Input for deleting a step."""

    step_id: str = Field(..., description="Step UUID to delete")

    @field_validator("step_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


# ==================== IMAGE MODELS ====================

class CreateImageInput(BaseModel):
    """Input for uploading an image."""

    image_data: str = Field(..., description="Base64-encoded image data")
    image_path: str = Field(..., description="File path where image will be stored")
    author_id: str = Field(..., description="Author UUID")

    @field_validator("author_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class DeleteImageInput(BaseModel):
    """Input for deleting an image."""

    image_id: str = Field(..., description="Image UUID to delete")

    @field_validator("image_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


# ==================== AI MODELS ====================

class AICreateRecipeInput(BaseModel):
    """Input for AI recipe generation."""

    message: str = Field(..., min_length=2, max_length=500, description="Recipe generation prompt")


class AIModifyRecipeInput(BaseModel):
    """Input for AI recipe modification."""

    message: str = Field(..., min_length=2, max_length=500, description="Modification instructions")
    recipe_id: str = Field(..., description="Recipe UUID to modify")

    @field_validator("recipe_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            UUID(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {v}") from e


class AISTTInput(BaseModel):
    """Input for speech-to-text transcription."""

    audio_file_path: str = Field(..., description="Path to audio file to transcribe")


# ==================== GROCERY MODELS ====================

class GroceryListInput(BaseModel):
    """Input for grocery list generation."""

    recipe_ids: List[str] = Field(..., min_items=1, max_items=50, description="List of recipe UUIDs (1-50)")

    @field_validator("recipe_ids")
    @classmethod
    def validate_uuids(cls, v: List[str]) -> List[str]:
        """Validate all UUIDs in list."""
        for recipe_id in v:
            try:
                UUID(recipe_id)
            except ValueError as e:
                raise ValueError(f"Invalid UUID format: {recipe_id}") from e
        return v


# ==================== EMAIL MODELS ====================

class EmailInviteInput(BaseModel):
    """Input for sending invitation email."""

    email: str = Field(..., description="Recipient email address")
    invite_link: str = Field(..., description="Invitation URL")
    sender_name: str = Field(..., min_length=2, max_length=50, description="Sender's name")


class EmailRecipeShareInput(BaseModel):
    """Input for sending recipe link email."""

    email: str = Field(..., description="Recipient email address")
    recipe_name: str = Field(..., min_length=2, max_length=100)
    recipe_link: str = Field(..., description="Recipe URL")
    sender_name: str = Field(..., min_length=2, max_length=50)


class EmailRecipeShareFullInput(BaseModel):
    """Input for sending full recipe content email."""

    email: str = Field(..., description="Recipient email address")
    recipe_name: str = Field(..., min_length=2, max_length=100)
    recipe_description: Optional[str] = Field(None, max_length=500)
    recipe_ingredients: List[dict] = Field(..., description="List of ingredient objects")
    recipe_steps: List[str] = Field(..., description="List of step instructions")
    sender_name: str = Field(..., min_length=2, max_length=50)
