"""API data models mirroring OpenAPI specification schemas.

These models represent the exact structure returned by the Recipez API.
All field names match the OpenAPI schema exactly (snake_case format).
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== USER MODELS ====================

class User(BaseModel):
    """User model matching API response."""

    user_id: UUID
    user_sub: UUID
    user_email: str
    user_name: str
    user_created_at: Optional[datetime] = None
    user_profile_image_url: Optional[str] = None


class ProfileData(BaseModel):
    """Profile data model."""

    user_id: UUID
    user_name: str
    user_email: str
    profile_image_url: str


# ==================== CATEGORY MODELS ====================

class Category(BaseModel):
    """Category model matching API response."""

    category_id: UUID
    category_name: str
    category_author_id: UUID
    created_at: datetime


# ==================== IMAGE MODELS ====================

class Image(BaseModel):
    """Image model matching API response."""

    image_id: UUID
    image_url: str
    image_author_id: UUID
    created_at: datetime


# ==================== INGREDIENT MODELS ====================

class Ingredient(BaseModel):
    """Ingredient model matching API response."""

    ingredient_id: UUID
    ingredient_name: str
    ingredient_quantity: str
    ingredient_measurement: str
    ingredient_author_id: UUID
    ingredient_recipe_id: UUID
    created_at: datetime


# ==================== STEP MODELS ====================

class Step(BaseModel):
    """Recipe step model matching API response."""

    step_id: UUID
    step_text: str
    step_author_id: UUID
    step_recipe_id: UUID
    created_at: datetime


# ==================== RECIPE MODELS ====================

class Recipe(BaseModel):
    """Base recipe model matching API response."""

    recipe_id: UUID
    recipe_name: str
    recipe_description: str
    recipe_category_id: UUID
    recipe_image_id: Optional[UUID] = None
    recipe_author_id: UUID
    created_at: datetime


class RecipeWithRelations(Recipe):
    """Recipe model with nested relations."""

    recipe_category: Optional[Category] = None
    recipe_image: Optional[Image] = None
    recipe_author: Optional[User] = None
    author: Optional[User] = None  # Alias for recipe_author
    recipe_ingredients: List[Ingredient] = Field(default_factory=list)
    recipe_steps: List[Step] = Field(default_factory=list)


# ==================== API KEY MODELS ====================

class ApiKeyMetadata(BaseModel):
    """API key metadata (never includes actual token)."""

    api_key_id: UUID
    api_key_name: str
    api_key_scopes: List[str]
    api_key_expires_at: Optional[datetime] = None
    api_key_created_at: datetime
    is_expired: bool


# ==================== HEALTH MODELS ====================

class HealthChecks(BaseModel):
    """Health check status details."""

    app: str
    database: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    checks: HealthChecks


class ReadinessChecks(BaseModel):
    """Readiness check status details."""

    database: str
    schema: str


class ReadinessResponse(BaseModel):
    """Readiness check response."""

    ready: bool
    checks: ReadinessChecks


# ==================== RESPONSE WRAPPERS ====================

class ResponseWrapper(BaseModel):
    """Generic response wrapper with 'response' field."""

    response: dict


class ProfileResponse(BaseModel):
    """Profile response wrapper."""

    response: ProfileData


class RecipeResponse(BaseModel):
    """Single recipe response wrapper."""

    response: dict  # Contains 'recipe' key


class RecipeDetailResponse(BaseModel):
    """Recipe detail response wrapper."""

    response: RecipeWithRelations


class RecipesListResponse(BaseModel):
    """Recipe list response wrapper."""

    response: List[RecipeWithRelations]


class CategoryResponse(BaseModel):
    """Category response wrapper."""

    response: dict  # Contains 'category' key


class CategoriesListResponse(BaseModel):
    """Categories list response wrapper."""

    response: List[Category]


class IngredientResponse(BaseModel):
    """Ingredient response wrapper."""

    response: dict  # Contains 'ingredient' key


class IngredientsResponse(BaseModel):
    """Ingredients response wrapper."""

    response: dict  # Contains 'ingredients' key


class StepsResponse(BaseModel):
    """Steps response wrapper."""

    response: dict  # Contains 'steps' key


class ImageResponse(BaseModel):
    """Image response wrapper."""

    response: dict  # Contains 'image' key


class CreateApiKeyResponse(BaseModel):
    """API key creation response."""

    response: dict  # Contains 'api_key', 'token', 'warning'


class ListApiKeysResponse(BaseModel):
    """API keys list response."""

    response: dict  # Contains 'api_keys', 'available_scopes'


class MessageResponse(BaseModel):
    """Generic message response."""

    response: dict  # Contains 'message' key


class SuccessResponse(BaseModel):
    """Generic success response."""

    response: dict  # Contains 'success' key


class ErrorResponse(BaseModel):
    """Generic error response."""

    response: dict  # Contains 'error' key


class BatchUpdateCategoryResponse(BaseModel):
    """Batch category update response."""

    response: dict  # Contains 'success', 'updated_count', 'failed_count', 'updated', 'failed'


class CategoryDeletePreviewResponse(BaseModel):
    """Category deletion preview response."""

    response: dict  # Contains 'can_delete', 'reason', 'affected_recipes', 'affected_count', 'message'


class AIRecipeResponse(BaseModel):
    """AI recipe generation response."""

    response: dict  # Contains 'recipe' key


class AISTTResponse(BaseModel):
    """AI speech-to-text response."""

    response: dict  # Contains 'transcription' key
