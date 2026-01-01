"""Create Feedback"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateFeedbackEvaluationsFeedbackTool(BaseTool):
    """Create Feedback"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_feedback_evaluations_feedback",
            "description": "Create Feedback",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "The feedback type (required)"
                    },
                    "data": {
                        "type": ["object", "null"],
                        "description": "Feedback rating data - can include rating (int/string), model_id, sibling_model_ids, reason, comment",
                        "additionalProperties": True
                    },
                    "meta": {
                        "type": ["object", "null"],
                        "description": "Optional metadata for the feedback",
                        "additionalProperties": True
                    },
                    "snapshot": {
                        "type": ["object", "null"],
                        "description": "Optional snapshot data - can include chat object",
                        "additionalProperties": True
                    }
                },
                "required": ["type"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_feedback_evaluations_feedback operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "type": arguments["type"]
        }

        if "data" in arguments and arguments["data"] is not None:
            json_data["data"] = arguments["data"]
        if "meta" in arguments and arguments["meta"] is not None:
            json_data["meta"] = arguments["meta"]
        if "snapshot" in arguments and arguments["snapshot"] is not None:
            json_data["snapshot"] = arguments["snapshot"]

        response = await self.client.post("/api/v1/evaluations/feedback", json_data=json_data)

        self._log_execution_end(response)
        return response