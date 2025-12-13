#!/usr/bin/env python3
"""Generate MCP tools from OpenAPI specification.

Parses Open WebUI OpenAPI spec and generates tool implementations,
tests, and __init__.py files for all endpoints.

Usage:
    python scripts/generate_tools.py --openapi /path/to/openapi.json
    python scripts/generate_tools.py --openapi /path/to/openapi.json --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / "src" / "tools"
TESTS_DIR = PROJECT_ROOT / "tests" / "unit" / "tools"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def snake_case(name: str) -> str:
    """Convert CamelCase or operationId to snake_case."""
    # Handle common patterns
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower().replace('-', '_').replace('__', '_')


def camel_case(name: str) -> str:
    """Convert snake_case to CamelCase."""
    return ''.join(word.capitalize() for word in name.split('_'))


def extract_resource(path: str, operation_id: str) -> str:
    """Extract resource name from path or operationId."""
    # Parse path segments
    parts = path.strip('/').split('/')

    # Skip api/v1 prefix
    if parts[0] == 'api':
        parts = parts[1:]
    if parts and parts[0] == 'v1':
        parts = parts[1:]

    # Get first meaningful segment
    if parts:
        resource = parts[0].rstrip('s')  # Remove trailing 's' for singular
        # Handle special cases
        if resource in ['chat', 'model', 'user', 'file', 'folder',
                        'function', 'prompt', 'tool', 'group', 'memory',
                        'note', 'image', 'channel', 'evaluation', 'config',
                        'pipeline', 'task', 'knowledge', 'retrieval', 'audio']:
            return resource
        # Handle auth/admin/ollama/openai
        if resource in ['auth', 'admin', 'ollama', 'openai', 'util', 'misc']:
            return resource

    # Fallback: extract from operationId
    parts = operation_id.split('_')
    if parts:
        return parts[0]

    return 'misc'


def get_resource_plural(resource: str) -> str:
    """Get plural form of resource for directory name."""
    PLURALS = {
        'chat': 'chats', 'model': 'models', 'user': 'users',
        'file': 'files', 'folder': 'folders', 'function': 'functions',
        'prompt': 'prompts', 'tool': 'tools', 'group': 'groups',
        'memory': 'memories', 'note': 'notes', 'image': 'images',
        'channel': 'channels', 'evaluation': 'evaluations',
        'config': 'configs', 'pipeline': 'pipelines', 'task': 'tasks',
        'knowledge': 'knowledge', 'retrieval': 'retrieval',
        'audio': 'audio', 'auth': 'auths', 'admin': 'admin',
        'ollama': 'ollama', 'openai': 'openai', 'util': 'utils',
        'misc': 'misc', 'health': 'health', 'data': 'data',
    }
    return PLURALS.get(resource, f"{resource}s")


def classify_endpoint(endpoint: dict) -> str:
    """Classify endpoint type: standard, file_upload, or streaming."""
    request_body = endpoint.get('requestBody', {})
    content = request_body.get('content', {})

    # Check for multipart/form-data (file upload)
    if 'multipart/form-data' in content:
        return 'file_upload'

    # Check for streaming responses
    responses = endpoint.get('responses', {})
    for code, response in responses.items():
        resp_content = response.get('content', {})
        if 'text/event-stream' in resp_content:
            return 'streaming'
        if 'application/x-ndjson' in resp_content:
            return 'streaming'

    return 'standard'


def extract_parameters(endpoint: dict, method: str) -> list[dict]:
    """Extract and normalize endpoint parameters."""
    params = []

    # Path and query parameters
    for param in endpoint.get('parameters', []):
        param_info = {
            'name': param.get('name'),
            'in': param.get('in'),  # path, query, header
            'required': param.get('required', False),
            'type': 'string',  # Default
            'description': param.get('description') or '',
            'default': None,
            'minimum': None,
            'maximum': None,
        }

        # Extract type from schema
        schema = param.get('schema', {})
        if schema.get('type') == 'integer':
            param_info['type'] = 'integer'
            param_info['default'] = schema.get('default')
            if 'minimum' in schema:
                param_info['minimum'] = schema['minimum']
            if 'maximum' in schema:
                param_info['maximum'] = schema['maximum']
        elif schema.get('type') == 'boolean':
            param_info['type'] = 'boolean'
            param_info['default'] = schema.get('default', False)
        elif schema.get('type') == 'array':
            param_info['type'] = 'array'
        else:
            param_info['default'] = schema.get('default')

        params.append(param_info)

    # Request body parameters (for POST/PUT/PATCH)
    if method in ['post', 'put', 'patch']:
        request_body = endpoint.get('requestBody', {})
        content = request_body.get('content', {})

        # JSON body
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        for prop_name, prop_schema in properties.items():
            param_info = {
                'name': prop_name,
                'in': 'body',
                'required': prop_name in required,
                'type': prop_schema.get('type', 'string'),
                'description': prop_schema.get('description') or '',
                'default': prop_schema.get('default'),
                'minimum': prop_schema.get('minimum'),
                'maximum': prop_schema.get('maximum'),
            }
            params.append(param_info)

    return params


def generate_tool_name(operation_id: str, method: str, path: str) -> str:
    """Generate MCP tool name from operationId."""
    # Clean up operationId
    name = operation_id

    # Remove common suffixes
    for suffix in ['_api_v1_', '_api_', '_get', '_post', '_put', '_delete', '_patch']:
        if suffix in name.lower():
            name = name.lower().replace(suffix, '_')

    # Clean up
    name = snake_case(name)
    name = re.sub(r'_+', '_', name)  # Collapse multiple underscores
    name = name.strip('_')

    return name


def parse_openapi(openapi_path: Path) -> list[dict]:
    """Parse OpenAPI spec and extract endpoint information."""
    with open(openapi_path) as f:
        spec = json.load(f)

    endpoints = []
    paths = spec.get('paths', {})

    for path, methods in paths.items():
        for method, details in methods.items():
            if method not in ['get', 'post', 'put', 'delete', 'patch']:
                continue

            operation_id = details.get('operationId', f"{method}_{path}")
            summary = details.get('summary', '')
            description = details.get('description', summary)

            # Extract resource
            resource = extract_resource(path, operation_id)

            endpoint = {
                'path': path,
                'method': method,
                'operation_id': operation_id,
                'summary': summary[:100] if summary else '',
                'description': description[:256] if description else '',
                'resource': resource,
                'resource_plural': get_resource_plural(resource),
                'tool_name': generate_tool_name(operation_id, method, path),
                'class_name': camel_case(generate_tool_name(operation_id, method, path)) + 'Tool',
                'type': classify_endpoint(details),
                'parameters': extract_parameters(details, method),
                'responses': details.get('responses', {}),
            }

            endpoints.append(endpoint)

    return endpoints


def render_tool(endpoint: dict, env: Environment) -> str:
    """Render tool implementation from template."""
    template_name = f"tool_{endpoint['type']}.py.j2"

    # Fallback to standard template if specialized doesn't exist
    try:
        template = env.get_template(template_name)
    except Exception:
        template = env.get_template("tool_standard.py.j2")

    return template.render(**endpoint)


def render_test(endpoint: dict, env: Environment) -> str:
    """Render test file from template."""
    template = env.get_template("test_tool.py.j2")
    return template.render(**endpoint)


def write_file(path: Path, content: str, dry_run: bool = False) -> None:
    """Write file with optional dry-run mode."""
    if dry_run:
        print(f"  [DRY RUN] Would write: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Created: {path}")


def generate_init_files(resources: set[str], dry_run: bool = False) -> None:
    """Generate __init__.py files for each resource directory."""
    for resource in resources:
        resource_plural = get_resource_plural(resource)

        # Tool __init__.py
        tool_init = TOOLS_DIR / resource_plural / "__init__.py"
        if not tool_init.exists() or dry_run:
            write_file(tool_init, '"""Tools for {resource} operations."""\n'.format(resource=resource), dry_run)

        # Test __init__.py
        test_init = TESTS_DIR / resource_plural / "__init__.py"
        if not test_init.exists() or dry_run:
            write_file(test_init, '"""Tests for {resource} tools."""\n'.format(resource=resource), dry_run)


def main():
    parser = argparse.ArgumentParser(description="Generate MCP tools from OpenAPI spec")
    parser.add_argument('--openapi', required=True, help="Path to OpenAPI JSON file")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be generated")
    parser.add_argument('--skip-existing', action='store_true', help="Skip existing files")
    args = parser.parse_args()

    openapi_path = Path(args.openapi)
    if not openapi_path.exists():
        print(f"Error: OpenAPI file not found: {openapi_path}")
        sys.exit(1)

    # Check templates exist
    if not TEMPLATES_DIR.exists():
        print(f"Error: Templates directory not found: {TEMPLATES_DIR}")
        print("Creating default templates...")
        create_default_templates()

    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Add custom filter to escape newlines in strings
    def escape_newlines(value):
        """Replace newlines with spaces for single-line strings."""
        if value is None:
            return ''
        return str(value).replace('\n', ' ').replace('\r', '')

    env.filters['escape_newlines'] = escape_newlines

    # Add custom filter for Python-compatible default values
    def python_repr(value):
        """Convert value to Python representation."""
        if value is None:
            return 'None'
        if isinstance(value, bool):
            return 'True' if value else 'False'
        if isinstance(value, str):
            return repr(value)
        return repr(value)

    env.filters['python_repr'] = python_repr

    # Parse OpenAPI
    print(f"Parsing OpenAPI spec: {openapi_path}")
    endpoints = parse_openapi(openapi_path)
    print(f"Found {len(endpoints)} endpoints")

    # Track resources and stats
    resources = set()
    stats = {'tools': 0, 'tests': 0, 'skipped': 0}

    # Generate tools
    print("\nGenerating tools...")
    for endpoint in endpoints:
        resource = endpoint['resource']
        resources.add(resource)

        # Tool file path
        tool_file = TOOLS_DIR / endpoint['resource_plural'] / f"{endpoint['tool_name']}_tool.py"

        # Skip if exists and flag set
        if args.skip_existing and tool_file.exists():
            stats['skipped'] += 1
            continue

        # Render and write tool
        try:
            tool_content = render_tool(endpoint, env)
            write_file(tool_file, tool_content, args.dry_run)
            stats['tools'] += 1
        except Exception as e:
            print(f"  Error generating {endpoint['tool_name']}: {e}")

        # Render and write test
        test_file = TESTS_DIR / endpoint['resource_plural'] / f"test_{endpoint['tool_name']}_tool.py"
        try:
            test_content = render_test(endpoint, env)
            write_file(test_file, test_content, args.dry_run)
            stats['tests'] += 1
        except Exception as e:
            print(f"  Error generating test for {endpoint['tool_name']}: {e}")

    # Generate __init__.py files
    print("\nGenerating __init__.py files...")
    generate_init_files(resources, args.dry_run)

    # Summary
    print(f"\n=== Summary ===")
    print(f"Total endpoints: {len(endpoints)}")
    print(f"Tools generated: {stats['tools']}")
    print(f"Tests generated: {stats['tests']}")
    print(f"Skipped (existing): {stats['skipped']}")
    print(f"Resources: {len(resources)}")


def create_default_templates():
    """Create default Jinja2 templates."""
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Standard tool template
    standard_template = '''"""{{ summary or 'Tool for ' + path }}"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class {{ class_name }}(BaseTool):
    """{{ description or summary }}"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "{{ tool_name }}",
            "description": "{{ (description or summary)[:256] }}",
            "inputSchema": {
                "type": "object",
                "properties": {
                    {% for param in parameters %}
                    "{{ param.name }}": {
                        "type": "{{ param.type }}",
                        "description": "{{ param.description[:100] }}"{% if param.default is not none %},
                        "default": {{ param.default | tojson }}{% endif %}{% if param.minimum is not none %},
                        "minimum": {{ param.minimum }}{% endif %}{% if param.maximum is not none %},
                        "maximum": {{ param.maximum }}{% endif %}
                    }{% if not loop.last %},{% endif %}
                    {% endfor %}
                },
                "required": [{% for param in parameters if param.required %}"{{ param.name }}"{% if not loop.last %}, {% endif %}{% endfor %}]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute {{ tool_name }} operation."""
        self._log_execution_start(arguments)

        {% for param in parameters if param.in == 'path' %}
        # Validate path parameter: {{ param.name }}
        {{ param.name }} = arguments.get("{{ param.name }}")
        if {{ param.name }}:
            {{ param.name }} = ToolInputValidator.validate_id({{ param.name }}, "{{ param.name }}")
        {% endfor %}

        {% for param in parameters if param.in == 'query' %}
        # Query parameter: {{ param.name }}
        {{ param.name }} = arguments.get("{{ param.name }}"{% if param.default is not none %}, {{ param.default | tojson }}{% endif %})
        {% endfor %}

        # Build request
        {% if method == 'get' %}
        params = {}
        {% for param in parameters if param.in == 'query' %}
        if {{ param.name }} is not None:
            params["{{ param.name }}"] = {{ param.name }}
        {% endfor %}

        response = await self.client.get("{{ path }}", params=params)
        {% elif method == 'post' %}
        json_data = {}
        {% for param in parameters if param.in == 'body' %}
        if arguments.get("{{ param.name }}") is not None:
            json_data["{{ param.name }}"] = arguments["{{ param.name }}"]
        {% endfor %}

        response = await self.client.post("{{ path }}", json_data=json_data)
        {% elif method == 'put' %}
        json_data = {}
        {% for param in parameters if param.in == 'body' %}
        if arguments.get("{{ param.name }}") is not None:
            json_data["{{ param.name }}"] = arguments["{{ param.name }}"]
        {% endfor %}

        response = await self.client.put("{{ path }}", json_data=json_data)
        {% elif method == 'patch' %}
        json_data = {}
        {% for param in parameters if param.in == 'body' %}
        if arguments.get("{{ param.name }}") is not None:
            json_data["{{ param.name }}"] = arguments["{{ param.name }}"]
        {% endfor %}

        response = await self.client.patch("{{ path }}", json_data=json_data)
        {% elif method == 'delete' %}
        params = {}
        {% for param in parameters if param.in == 'query' %}
        if {{ param.name }} is not None:
            params["{{ param.name }}"] = {{ param.name }}
        {% endfor %}

        response = await self.client.delete("{{ path }}", params=params)
        {% endif %}

        self._log_execution_end(response)
        return response
'''

    # Test template
    test_template = '''"""Tests for {{ class_name }}."""

import pytest
from unittest.mock import AsyncMock, Mock
from src.tools.{{ resource_plural }}.{{ tool_name }}_tool import {{ class_name }}
from src.exceptions import ValidationError, NotFoundError, HTTPError


class Test{{ class_name }}:
    """Tests for {{ tool_name }}."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HTTP client."""
        client = Mock()
        {% if method == 'get' %}
        client.get = AsyncMock(return_value={})
        {% elif method == 'post' %}
        client.post = AsyncMock(return_value={})
        {% elif method == 'put' %}
        client.put = AsyncMock(return_value={})
        {% elif method == 'patch' %}
        client.patch = AsyncMock(return_value={})
        {% elif method == 'delete' %}
        client.delete = AsyncMock(return_value={})
        {% endif %}
        return client

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = Mock()
        return config

    @pytest.fixture
    def tool(self, mock_client, mock_config):
        """Create tool instance."""
        return {{ class_name }}(client=mock_client, config=mock_config)

    def test_get_definition(self, tool):
        """Test tool definition structure."""
        definition = tool.get_definition()

        assert definition["name"] == "{{ tool_name }}"
        assert "description" in definition
        assert "inputSchema" in definition
        assert definition["inputSchema"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_execute_success(self, tool, mock_client):
        """Test successful execution."""
        {% if method == 'get' %}
        mock_client.get.return_value = {"status": "ok"}
        {% elif method == 'post' %}
        mock_client.post.return_value = {"status": "ok"}
        {% elif method == 'put' %}
        mock_client.put.return_value = {"status": "ok"}
        {% elif method == 'patch' %}
        mock_client.patch.return_value = {"status": "ok"}
        {% elif method == 'delete' %}
        mock_client.delete.return_value = {"status": "ok"}
        {% endif %}

        result = await tool.execute({})

        assert result is not None
        {% if method == 'get' %}
        mock_client.get.assert_called_once()
        {% elif method == 'post' %}
        mock_client.post.assert_called_once()
        {% elif method == 'put' %}
        mock_client.put.assert_called_once()
        {% elif method == 'patch' %}
        mock_client.patch.assert_called_once()
        {% elif method == 'delete' %}
        mock_client.delete.assert_called_once()
        {% endif %}

    @pytest.mark.asyncio
    async def test_execute_not_found(self, tool, mock_client):
        """Test handling of 404 errors."""
        {% if method == 'get' %}
        mock_client.get.side_effect = NotFoundError("Not found")
        {% elif method == 'post' %}
        mock_client.post.side_effect = NotFoundError("Not found")
        {% elif method == 'put' %}
        mock_client.put.side_effect = NotFoundError("Not found")
        {% elif method == 'patch' %}
        mock_client.patch.side_effect = NotFoundError("Not found")
        {% elif method == 'delete' %}
        mock_client.delete.side_effect = NotFoundError("Not found")
        {% endif %}

        with pytest.raises(NotFoundError):
            await tool.execute({})

    @pytest.mark.asyncio
    async def test_execute_http_error(self, tool, mock_client):
        """Test handling of HTTP errors."""
        {% if method == 'get' %}
        mock_client.get.side_effect = HTTPError("Server error", status_code=500)
        {% elif method == 'post' %}
        mock_client.post.side_effect = HTTPError("Server error", status_code=500)
        {% elif method == 'put' %}
        mock_client.put.side_effect = HTTPError("Server error", status_code=500)
        {% elif method == 'patch' %}
        mock_client.patch.side_effect = HTTPError("Server error", status_code=500)
        {% elif method == 'delete' %}
        mock_client.delete.side_effect = HTTPError("Server error", status_code=500)
        {% endif %}

        with pytest.raises(HTTPError):
            await tool.execute({})
'''

    # Write templates
    (TEMPLATES_DIR / "tool_standard.py.j2").write_text(standard_template)
    (TEMPLATES_DIR / "test_tool.py.j2").write_text(test_template)

    print(f"Created templates in {TEMPLATES_DIR}")


if __name__ == "__main__":
    main()
