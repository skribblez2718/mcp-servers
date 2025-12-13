"""Delete Feedbacks"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteFeedbacksEvaluationsFeedbacksTool(BaseTool):
    """Delete Feedbacks"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_feedbacks_evaluations_feedbacks",
            "description": "Delete Feedbacks",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_feedbacks_evaluations_feedbacks operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.delete("/api/v1/evaluations/feedbacks", params=params)

        self._log_execution_end(response)
        return response