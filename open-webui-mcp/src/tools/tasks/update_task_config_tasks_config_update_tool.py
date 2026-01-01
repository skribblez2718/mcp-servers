"""Update Task Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateTaskConfigTasksConfigUpdateTool(BaseTool):
    """Update Task Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_task_config_tasks_config_update",
            "description": "Update Task Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "TASK_MODEL": {"type": ["string", "null"], "description": "The task model to use (nullable)"},
                    "TASK_MODEL_EXTERNAL": {"type": ["string", "null"], "description": "The external task model to use (nullable)"},
                    "ENABLE_TITLE_GENERATION": {"type": "boolean", "description": "Enable title generation"},
                    "TITLE_GENERATION_PROMPT_TEMPLATE": {"type": "string", "description": "Title generation prompt template"},
                    "IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE": {"type": "string", "description": "Image prompt generation prompt template"},
                    "ENABLE_AUTOCOMPLETE_GENERATION": {"type": "boolean", "description": "Enable autocomplete generation"},
                    "AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH": {"type": "integer", "description": "Autocomplete generation input max length"},
                    "TAGS_GENERATION_PROMPT_TEMPLATE": {"type": "string", "description": "Tags generation prompt template"},
                    "FOLLOW_UP_GENERATION_PROMPT_TEMPLATE": {"type": "string", "description": "Follow up generation prompt template"},
                    "ENABLE_FOLLOW_UP_GENERATION": {"type": "boolean", "description": "Enable follow up generation"},
                    "ENABLE_TAGS_GENERATION": {"type": "boolean", "description": "Enable tags generation"},
                    "ENABLE_SEARCH_QUERY_GENERATION": {"type": "boolean", "description": "Enable search query generation"},
                    "ENABLE_RETRIEVAL_QUERY_GENERATION": {"type": "boolean", "description": "Enable retrieval query generation"},
                    "QUERY_GENERATION_PROMPT_TEMPLATE": {"type": "string", "description": "Query generation prompt template"},
                    "TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE": {"type": "string", "description": "Tools function calling prompt template"},
                    "VOICE_MODE_PROMPT_TEMPLATE": {"type": "string", "description": "Voice mode prompt template"}
                },
                "required": ["TASK_MODEL", "TASK_MODEL_EXTERNAL", "ENABLE_TITLE_GENERATION", "TITLE_GENERATION_PROMPT_TEMPLATE", "IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE", "ENABLE_AUTOCOMPLETE_GENERATION", "AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH", "TAGS_GENERATION_PROMPT_TEMPLATE", "FOLLOW_UP_GENERATION_PROMPT_TEMPLATE", "ENABLE_FOLLOW_UP_GENERATION", "ENABLE_TAGS_GENERATION", "ENABLE_SEARCH_QUERY_GENERATION", "ENABLE_RETRIEVAL_QUERY_GENERATION", "QUERY_GENERATION_PROMPT_TEMPLATE", "TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE", "VOICE_MODE_PROMPT_TEMPLATE"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_task_config_tasks_config_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "TASK_MODEL": arguments.get("TASK_MODEL"),
            "TASK_MODEL_EXTERNAL": arguments.get("TASK_MODEL_EXTERNAL"),
            "ENABLE_TITLE_GENERATION": arguments.get("ENABLE_TITLE_GENERATION"),
            "TITLE_GENERATION_PROMPT_TEMPLATE": arguments.get("TITLE_GENERATION_PROMPT_TEMPLATE"),
            "IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE": arguments.get("IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE"),
            "ENABLE_AUTOCOMPLETE_GENERATION": arguments.get("ENABLE_AUTOCOMPLETE_GENERATION"),
            "AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH": arguments.get("AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH"),
            "TAGS_GENERATION_PROMPT_TEMPLATE": arguments.get("TAGS_GENERATION_PROMPT_TEMPLATE"),
            "FOLLOW_UP_GENERATION_PROMPT_TEMPLATE": arguments.get("FOLLOW_UP_GENERATION_PROMPT_TEMPLATE"),
            "ENABLE_FOLLOW_UP_GENERATION": arguments.get("ENABLE_FOLLOW_UP_GENERATION"),
            "ENABLE_TAGS_GENERATION": arguments.get("ENABLE_TAGS_GENERATION"),
            "ENABLE_SEARCH_QUERY_GENERATION": arguments.get("ENABLE_SEARCH_QUERY_GENERATION"),
            "ENABLE_RETRIEVAL_QUERY_GENERATION": arguments.get("ENABLE_RETRIEVAL_QUERY_GENERATION"),
            "QUERY_GENERATION_PROMPT_TEMPLATE": arguments.get("QUERY_GENERATION_PROMPT_TEMPLATE"),
            "TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE": arguments.get("TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE"),
            "VOICE_MODE_PROMPT_TEMPLATE": arguments.get("VOICE_MODE_PROMPT_TEMPLATE")
        }

        response = await self.client.post("/api/v1/tasks/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response