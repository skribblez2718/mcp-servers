"""Delete Feedback By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteFeedbackByIdEvaluationsFeedbackIdTool(BaseTool):
    """Delete Feedback By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_feedback_by_id_evaluations_feedback_id",
            "description": "Delete Feedback By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_feedback_by_id_evaluations_feedback_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/evaluations/feedback/{id}", params=params)

        self._log_execution_end(response)
        return response