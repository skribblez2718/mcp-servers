"""Get Feedbacks"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetFeedbacksEvaluationsFeedbacksUserTool(BaseTool):
    """Get Feedbacks"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_feedbacks_evaluations_feedbacks_user",
            "description": "Get Feedbacks",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_feedbacks_evaluations_feedbacks_user operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/evaluations/feedbacks/user", params=params)

        self._log_execution_end(response)
        return response