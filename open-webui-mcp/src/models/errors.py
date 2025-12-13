"""Error response models."""

from pydantic import BaseModel as PydanticBaseModel, Field


class ErrorDetail(PydanticBaseModel):
    """Error detail.

    Attributes:
        field: Field name (for validation errors)
        message: Error message
        code: Error code
    """

    field: str | None = Field(None, description="Field name")
    message: str = Field(..., description="Error message")
    code: str | None = Field(None, description="Error code")


class ErrorResponse(PydanticBaseModel):
    """Error response model.

    Attributes:
        error: Main error message
        status_code: HTTP status code
        details: List of error details
        request_id: Request ID for tracing
    """

    error: str = Field(..., description="Main error message")
    status_code: int = Field(..., description="HTTP status code")
    details: list[ErrorDetail] = Field(default_factory=list)
    request_id: str | None = Field(None, description="Request ID")
