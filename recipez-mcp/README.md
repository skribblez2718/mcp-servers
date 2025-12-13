# Recipez MCP Server

Model Context Protocol (MCP) server for the [Recipez](https://github.com/recipez) recipe management API. Provides 12 tools for recipe CRUD operations, AI-powered recipe generation, grocery list management, and email operations.

## Features

- **Recipe Management**: Full CRUD operations for recipes, categories, ingredients, and steps
- **AI Operations**: Generate recipes from prompts, modify existing recipes, speech-to-text transcription
- **Grocery Lists**: AI-organized shopping lists from selected recipes (max 50 recipes)
- **Email Operations**: Send invitations, share recipe links, share complete recipes
- **Profile Management**: Get/update user profile and profile images
- **API Key Management**: Create, list, and delete managed API keys
- **Image Management**: Upload base64-encoded images, delete images
- **Health Checks**: Monitor API availability and readiness

## Requirements

- **Python**: 3.10 or higher
- **uv**: Package manager ([installation guide](https://github.com/astral-sh/uv))
- **Recipez API**: Live instance with JWT authentication
- **Environment**: Linux, macOS, or Windows with Python support

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/recipez/mcp-server.git
cd mcp-server/recipez
```

### 2. Initialize Python Project with uv

```bash
# Initialize project (creates pyproject.toml if not exists)
uv init

# Create virtual environment
uv venv

# Sync dependencies
uv sync
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required variables:
- `RECIPEZ_BASE_URL`: Recipez API base URL (HTTPS required)
- `RECIPEZ_JWT_TOKEN`: JWT token for authentication

Optional variables:
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `CORS_ORIGINS`: CORS origins, comma-separated (default: `*`)

### 4. Obtain JWT Token

To get a JWT token from the Recipez API:

1. **Authenticate with Recipez**: Use your email to authenticate through the Recipez frontend or authentication endpoint
2. **Retrieve Token**: The API returns a JWT token with format: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. **Configure Token**: Add token to `.env` file:
   ```bash
   RECIPEZ_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

**Token Scopes Required**:
- `recipe:*` - Full recipe access
- `category:*` - Category management
- `ingredient:*` - Ingredient management
- `step:*` - Step management
- `image:*` - Image upload/delete
- `ai:*` - AI operations
- `email:*` - Email sending

Token expires after 12 hours (default Recipez API configuration).

## Running the Server

### Development

```bash
# Run server directly
uv run python -m recipez_mcp

# With specific port
PORT=9000 uv run python -m recipez_mcp
```

Server will start on `http://0.0.0.0:8000` (default) and provide:
- SSE endpoint: `GET /sse` (MCP client connection)
- Messages endpoint: `POST /messages` (tool execution)
- Health check: `GET /health` (monitoring)

### Production (systemd)

1. **Create Service User**:
   ```bash
   sudo useradd -r -s /bin/false recipez
   ```

2. **Install to /opt**:
   ```bash
   sudo mkdir -p /opt/recipez-mcp
   sudo cp -r . /opt/recipez-mcp/
   sudo chown -R recipez:recipez /opt/recipez-mcp
   ```

3. **Configure Secrets**:
   ```bash
   sudo mkdir -p /etc/recipez-mcp
   sudo cp .env /etc/recipez-mcp/secrets.env
   sudo chown recipez:recipez /etc/recipez-mcp/secrets.env
   sudo chmod 600 /etc/recipez-mcp/secrets.env
   ```

4. **Install systemd Service**:
   ```bash
   sudo cp recipez-mcp.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable recipez-mcp
   sudo systemctl start recipez-mcp
   ```

5. **Check Status**:
   ```bash
   sudo systemctl status recipez-mcp
   sudo journalctl -u recipez-mcp -f
   ```

## MCP Client Setup

This server uses HTTP/SSE transport, allowing remote connections. Configure your MCP client to connect to the server.

### Claude Desktop / Claude Code

Add to your MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "recipez": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

For remote servers, replace `localhost:8000` with your server address.

Restart Claude Desktop after updating configuration.

### Cursor

Add to your Cursor MCP configuration (Settings > MCP):

```json
{
  "mcpServers": {
    "recipez": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

Or add via Cursor's MCP panel:
1. Open Cursor Settings
2. Navigate to MCP section
3. Add new server with URL: `http://localhost:8000/sse`
4. Set transport to SSE

### Windsurf

Add to your Windsurf MCP configuration:

```json
{
  "mcpServers": {
    "recipez": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

### Remote Server Configuration

For remote deployments (e.g., running on a dedicated server):

1. **Update Host/Port**: Configure environment variables:
   ```bash
   HOST=0.0.0.0  # Bind to all interfaces
   PORT=8000     # Your chosen port
   ```

2. **Update Client Config**: Use your server's address:
   ```json
   {
     "mcpServers": {
       "recipez": {
         "url": "http://your-server-ip:8000/sse",
         "transport": "sse"
       }
     }
   }
   ```

3. **Firewall**: Ensure port 8000 is accessible

4. **HTTPS (recommended for production)**: Use a reverse proxy (nginx/caddy) for TLS termination

## Tool Reference

### 1. recipez_health_check

Check Recipez API health and readiness status.

**Parameters**:
- `check_type` (optional): `"health"` (default) or `"ready"`

**Example**:
```json
{"check_type": "ready"}
```

### 2. recipez_profile_get

Get authenticated user's profile information.

**Parameters**: None

### 3. recipez_profile_update_image

Update authenticated user's profile image URL.

**Parameters**:
- `image_url` (required): URL to new profile image

### 4. recipez_api_keys_manage

Manage managed API keys: create, list, delete.

**Parameters**:
- `operation` (required): `"create"`, `"list"`, or `"delete"`
- For `create`: `name`, `scopes`, optional `expires_at`, `never_expires`
- For `delete`: `api_key_id`

**Example** (create):
```json
{
  "operation": "create",
  "name": "My API Key",
  "scopes": ["recipe:read", "recipe:create"],
  "never_expires": true
}
```

### 5. recipez_recipes

Manage recipes with full CRUD operations.

**Parameters**:
- `operation` (required): `"create"`, `"get"`, `"list"`, `"update"`, `"delete"`, `"batch_update_category"`
- For `create`: `recipe_name`, `recipe_description`, `recipe_category_id`, `recipe_image_id`, `recipe_author_id`
- For `get`/`update`/`delete`: `recipe_id`
- For `batch_update_category`: `updates` (array of `{recipe_id, category_id}`)

**Example** (create):
```json
{
  "operation": "create",
  "recipe_name": "Chocolate Chip Cookies",
  "recipe_description": "Classic homemade cookies",
  "recipe_category_id": "550e8400-e29b-41d4-a716-446655440000",
  "recipe_image_id": "660e8400-e29b-41d4-a716-446655440000",
  "recipe_author_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

### 6. recipez_categories

Manage recipe categories with CRUD operations and deletion preview.

**Parameters**:
- `operation` (required): `"create"`, `"get"`, `"list"`, `"update"`, `"delete"`, `"preview_delete"`
- For `create`: `category_name`, `author_id`
- For `update`: `category_id`, `category_name`
- For `get`/`delete`/`preview_delete`: `category_id`

### 7. recipez_ingredients

Manage recipe ingredients with batch operations.

**Parameters**:
- `operation` (required): `"batch_create"`, `"get"`, `"update"`, `"delete"`
- For `batch_create`: `recipe_id`, `author_id`, `ingredients` (array)
- For `update`: `ingredient_id`, `ingredient_name`, `ingredient_quantity`, `ingredient_measurement`
- For `get`/`delete`: `ingredient_id`

**Example** (batch_create):
```json
{
  "operation": "batch_create",
  "recipe_id": "550e8400-e29b-41d4-a716-446655440000",
  "author_id": "770e8400-e29b-41d4-a716-446655440000",
  "ingredients": [
    {
      "ingredient_name": "Flour",
      "ingredient_quantity": "2",
      "ingredient_measurement": "cup"
    },
    {
      "ingredient_name": "Sugar",
      "ingredient_quantity": "1",
      "ingredient_measurement": "cup"
    }
  ]
}
```

### 8. recipez_steps

Manage recipe steps/instructions with batch operations.

**Parameters**:
- `operation` (required): `"batch_create"`, `"get_by_recipe"`, `"update"`, `"delete"`
- For `batch_create`: `recipe_id`, `author_id`, `steps` (array of `{step_description}`)
- For `get_by_recipe`: `recipe_id`
- For `update`: `step_id`, `step_description`
- For `delete`: `step_id`

### 9. recipez_images

Manage recipe images: upload base64-encoded images and delete.

**Parameters**:
- `operation` (required): `"upload"` or `"delete"`
- For `upload`: `image_data` (base64), `image_path`, `author_id`
- For `delete`: `image_id`

**Note**: Maximum upload size is 10MB (API limit).

### 10. recipez_ai

AI-powered recipe operations: create, modify, speech-to-text.

**Parameters**:
- `operation` (required): `"create"`, `"modify"`, or `"stt"`
- For `create`: `message` (recipe prompt)
- For `modify`: `message` (modification instructions), `recipe_id`
- For `stt`: `audio_file_path` (path to audio file)

**Example** (create):
```json
{
  "operation": "create",
  "message": "Create a healthy pasta recipe with vegetables"
}
```

**Example** (stt):
```json
{
  "operation": "stt",
  "audio_file_path": "/path/to/audio.mp3"
}
```

Supported audio formats: MP3, WAV, MP4, M4A, WEBM, FLAC (max 25MB).

### 11. recipez_grocery

Generate AI-organized grocery list from selected recipes.

**Parameters**:
- `recipe_ids` (required): Array of recipe UUIDs (1-50 recipes)

**Example**:
```json
{
  "recipe_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660e8400-e29b-41d4-a716-446655440000"
  ]
}
```

Grocery list is emailed to the authenticated user.

### 12. recipez_email

Send emails: invitations, recipe link sharing, full recipe sharing.

**Parameters**:
- `operation` (required): `"invite"`, `"share_link"`, or `"share_full"`
- `email` (required): Recipient email
- `sender_name` (required): Sender name
- For `invite`: `invite_link`
- For `share_link`: `recipe_name`, `recipe_link`
- For `share_full`: `recipe_name`, `recipe_ingredients`, `recipe_steps`, optional `recipe_description`

**Example** (share_full):
```json
{
  "operation": "share_full",
  "email": "friend@example.com",
  "sender_name": "John Doe",
  "recipe_name": "Chocolate Chip Cookies",
  "recipe_description": "Classic homemade cookies",
  "recipe_ingredients": [
    {"ingredient_name": "Flour", "ingredient_quantity": "2", "ingredient_measurement": "cup"}
  ],
  "recipe_steps": ["Mix dry ingredients", "Add wet ingredients", "Bake at 350°F"]
}
```

## Development

### Code Quality

```bash
# Format code
uv run black src/

# Lint
uv run ruff check src/

# Type check
uv run mypy src/
```

### Testing

```bash
# Run all tests (excludes requires_api marker)
uv run pytest

# Run specific test file
uv run pytest tests/test_specific.py

# Run with coverage
uv run pytest --cov=recipez_mcp --cov-report=html
```

**Note**: Tests requiring live API are marked with `@pytest.mark.requires_api` and skipped by default.

## Troubleshooting

### Server Won't Start

**Problem**: `Failed to start server: [Errno 98] Address already in use`

**Solution**: Change port in `.env` file:
```bash
PORT=9000
```

### Authentication Errors

**Problem**: `401 Unauthorized - missing or invalid JWT token`

**Solutions**:
1. Verify token is set in `.env`: `RECIPEZ_JWT_TOKEN=your_token_here`
2. Check token hasn't expired (12 hour default expiration)
3. Verify token has required scopes for the operation
4. Re-authenticate with Recipez API to get new token

### API Connectivity Issues

**Problem**: `Connection refused` or `Timeout`

**Solutions**:
1. Verify `RECIPEZ_BASE_URL` is correct and accessible
2. Check API is running: `curl https://api.recipez.example.com/health`
3. Verify network connectivity and firewall rules
4. Check API logs for errors

### Tool Not Found

**Problem**: `Tool 'recipez_xyz' not found in registry`

**Solution**: Verify tool name matches exactly (case-sensitive). Use `recipez_health_check` to test connectivity.

### Rate Limiting

**Problem**: `429 Too Many Requests`

**Solution**: API implements rate limiting. Wait for cooldown period (typically 1 minute) and retry.

## Architecture

```
recipez_mcp/
├── models/          # Pydantic models (API and MCP)
├── utils/           # Validation, errors, logging
├── config/          # Settings management
├── client/          # HTTP client with retry logic
├── tools/           # MCP tool implementations (12 tools)
├── factory.py       # Tool registration and dependency injection
├── server.py        # Starlette ASGI app with SSE transport
└── __main__.py      # CLI entry point
```

**Design Principles**:
- **Absolute imports**: `from recipez_mcp.module import Item` (never relative)
- **Dependency injection**: HTTPClient injected via factory
- **Type safety**: 100% type hints with Pydantic v2
- **Error handling**: Custom MCP exceptions mapping HTTP status codes
- **Structured logging**: JSON logs with tool execution context
- **Async-first**: All I/O operations use asyncio

## Security

- **JWT Authentication**: All protected endpoints require valid JWT token
- **HTTPS Required**: Recipez API URL must use HTTPS
- **No Secrets in Code**: All sensitive data from environment variables
- **Token Expiration**: Tokens expire after 12 hours (API default)
- **Rate Limiting**: API enforces rate limits (handled automatically with retries)
- **Input Validation**: Pydantic models validate all tool inputs
- **Error Sanitization**: API error messages passed through without leaking sensitive data

## License

Proprietary - See LICENSE file for details.

## Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Follow code style (black, ruff, mypy)
4. Add tests for new features
5. Submit pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/recipez/mcp-server/issues)
- **Documentation**: [Recipez API Docs](https://docs.recipez.example.com)
- **MCP Protocol**: [Model Context Protocol](https://github.com/anthropics/model-context-protocol)

## Version

Current version: **0.1.0**

## Changelog

### 0.1.0 (Initial Release)
- 12 MCP tools for Recipez API
- HTTP/SSE transport with Starlette
- JWT authentication with auto-retry
- Structured logging
- Claude Desktop integration
- systemd service configuration
