"""Set Code Execution Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetCodeExecutionConfigConfigsCodeExecutionTool(BaseTool):
    """Set Code Execution Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_code_execution_config_configs_code_execution",
            "description": "Set Code Execution Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ENABLE_CODE_EXECUTION": {
                        "type": "boolean",
                        "description": "Enable code execution"
                    },
                    "CODE_EXECUTION_ENGINE": {
                        "type": "string",
                        "description": "Code execution engine to use"
                    },
                    "CODE_EXECUTION_JUPYTER_URL": {
                        "type": ["string", "null"],
                        "description": "Jupyter URL for code execution"
                    },
                    "CODE_EXECUTION_JUPYTER_AUTH": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication method"
                    },
                    "CODE_EXECUTION_JUPYTER_AUTH_TOKEN": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication token"
                    },
                    "CODE_EXECUTION_JUPYTER_AUTH_PASSWORD": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication password"
                    },
                    "CODE_EXECUTION_JUPYTER_TIMEOUT": {
                        "type": ["integer", "null"],
                        "description": "Jupyter execution timeout in seconds"
                    },
                    "ENABLE_CODE_INTERPRETER": {
                        "type": "boolean",
                        "description": "Enable code interpreter"
                    },
                    "CODE_INTERPRETER_ENGINE": {
                        "type": "string",
                        "description": "Code interpreter engine to use"
                    },
                    "CODE_INTERPRETER_PROMPT_TEMPLATE": {
                        "type": ["string", "null"],
                        "description": "Prompt template for code interpreter"
                    },
                    "CODE_INTERPRETER_JUPYTER_URL": {
                        "type": ["string", "null"],
                        "description": "Jupyter URL for code interpreter"
                    },
                    "CODE_INTERPRETER_JUPYTER_AUTH": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication method for interpreter"
                    },
                    "CODE_INTERPRETER_JUPYTER_AUTH_TOKEN": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication token for interpreter"
                    },
                    "CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD": {
                        "type": ["string", "null"],
                        "description": "Jupyter authentication password for interpreter"
                    },
                    "CODE_INTERPRETER_JUPYTER_TIMEOUT": {
                        "type": ["integer", "null"],
                        "description": "Jupyter execution timeout for interpreter"
                    }
                },
                "required": [
                    "ENABLE_CODE_EXECUTION", "CODE_EXECUTION_ENGINE", "CODE_EXECUTION_JUPYTER_URL",
                    "CODE_EXECUTION_JUPYTER_AUTH", "CODE_EXECUTION_JUPYTER_AUTH_TOKEN",
                    "CODE_EXECUTION_JUPYTER_AUTH_PASSWORD", "CODE_EXECUTION_JUPYTER_TIMEOUT",
                    "ENABLE_CODE_INTERPRETER", "CODE_INTERPRETER_ENGINE", "CODE_INTERPRETER_PROMPT_TEMPLATE",
                    "CODE_INTERPRETER_JUPYTER_URL", "CODE_INTERPRETER_JUPYTER_AUTH",
                    "CODE_INTERPRETER_JUPYTER_AUTH_TOKEN", "CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD",
                    "CODE_INTERPRETER_JUPYTER_TIMEOUT"
                ]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_code_execution_config_configs_code_execution operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "ENABLE_CODE_EXECUTION": arguments.get("ENABLE_CODE_EXECUTION"),
            "CODE_EXECUTION_ENGINE": arguments.get("CODE_EXECUTION_ENGINE"),
            "CODE_EXECUTION_JUPYTER_URL": arguments.get("CODE_EXECUTION_JUPYTER_URL"),
            "CODE_EXECUTION_JUPYTER_AUTH": arguments.get("CODE_EXECUTION_JUPYTER_AUTH"),
            "CODE_EXECUTION_JUPYTER_AUTH_TOKEN": arguments.get("CODE_EXECUTION_JUPYTER_AUTH_TOKEN"),
            "CODE_EXECUTION_JUPYTER_AUTH_PASSWORD": arguments.get("CODE_EXECUTION_JUPYTER_AUTH_PASSWORD"),
            "CODE_EXECUTION_JUPYTER_TIMEOUT": arguments.get("CODE_EXECUTION_JUPYTER_TIMEOUT"),
            "ENABLE_CODE_INTERPRETER": arguments.get("ENABLE_CODE_INTERPRETER"),
            "CODE_INTERPRETER_ENGINE": arguments.get("CODE_INTERPRETER_ENGINE"),
            "CODE_INTERPRETER_PROMPT_TEMPLATE": arguments.get("CODE_INTERPRETER_PROMPT_TEMPLATE"),
            "CODE_INTERPRETER_JUPYTER_URL": arguments.get("CODE_INTERPRETER_JUPYTER_URL"),
            "CODE_INTERPRETER_JUPYTER_AUTH": arguments.get("CODE_INTERPRETER_JUPYTER_AUTH"),
            "CODE_INTERPRETER_JUPYTER_AUTH_TOKEN": arguments.get("CODE_INTERPRETER_JUPYTER_AUTH_TOKEN"),
            "CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD": arguments.get("CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD"),
            "CODE_INTERPRETER_JUPYTER_TIMEOUT": arguments.get("CODE_INTERPRETER_JUPYTER_TIMEOUT")
        }

        response = await self.client.post("/api/v1/configs/code_execution", json_data=json_data)

        self._log_execution_end(response)
        return response