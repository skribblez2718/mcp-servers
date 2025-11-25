# Open WebUI MCP Server - Tools API Reference

Comprehensive API reference for all implemented MCP tools.

## Table of Contents

- [Overview](#overview)
- [Common Patterns](#common-patterns)
- [Chat Tools](#chat-tools)
- [Model Tools](#model-tools)
- [User Tools](#user-tools)
- [Admin Tools](#admin-tools)
- [Error Codes](#error-codes)
- [Rate Limiting](#rate-limiting)

## Overview

### Current Implementation Status

**Implemented**: 6 of 138 tools (4.3%)

| Category | Implemented | Remaining | Total |
|----------|-------------|-----------|-------|
| Tier 1 (Core) | 6 | 0 | 6 |
| Tier 2 (Knowledge/Files) | 0 | 30 | 30 |
| Tier 3 (Functions) | 0 | 12 | 12 |
| Tier 4 (Misc) | 0 | 90 | 90 |
| **Total** | **6** | **132** | **138** |

### Tool Naming Convention

- **Format**: `{resource}_{action}` (snake_case)
- **Examples**: `chat_list`, `model_get`, `user_create`
- **MCP Client Usage**: Tools invoked via natural language or direct tool calls

### Authentication

All tools require valid API key authentication:

- **Required**: Set `OPENWEBUI_API_KEY` environment variable (format: `sk-xxxxx...`)
- **Header Injection**: Client automatically adds `Authorization: Bearer {api_key}` header to all API requests
- **Scope-Based Access**: Admin tools require admin-level API key
- **Get API Key**: Open WebUI → Settings → Account → API Keys
- **JWT Token Support**: Both API keys and JWT tokens work with Bearer header format

**401 Unauthorized Response**: Missing or invalid API key
- Verify `OPENWEBUI_API_KEY` is set in `.env`
- Check API key format (should start with `sk-`)
- Confirm API key is active in Open WebUI (Settings → Account → API Keys)
- Try regenerating key if previously issued

## Common Patterns

### Pagination

All list tools support pagination:

**Input Parameters**:
- `limit` (integer, optional): Items per page (1-1000, default varies by tool)
- `offset` (integer, optional): Pagination offset (≥0, default 0)

**Output Fields**:
```json
{
  "items": [...],        // Array of resources (field name varies: chats, models, users, etc.)
  "total": 100,          // Total items available
  "limit": 20,           // Items per page
  "offset": 0,           // Current offset
  "has_next": true       // Whether more pages exist
}
```

**Example Usage**:
```
"Show me chats 20-40" → {"limit": 20, "offset": 20}
"Get first 100 models" → {"limit": 100, "offset": 0}
```

### Error Handling

All tools return errors in consistent format:

**Error Response**:
```json
{
  "error": "Validation failed: limit must be between 1 and 1000",
  "code": "VALIDATION_ERROR"
}
```

**Common Error Codes** (see [Error Codes](#error-codes) section):
- `VALIDATION_ERROR`: Invalid input parameters
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `AUTH_ERROR`: Authentication required/failed
- `SERVER_ERROR`: Internal server error

### Input Validation

All tools validate inputs:

- **ID Format**: Alphanumeric + `_-` only, max 255 characters
- **Pagination**: `limit` 1-1000, `offset` ≥0
- **String Length**: Max 1000 characters for text fields (configurable per field)
- **Enum Values**: Only allowed values accepted

**Validation Errors**: Return immediately with `VALIDATION_ERROR` code

## Chat Tools

### chat_list

**Description**: List all chats with pagination support

**MCP Tool Name**: `chat_list`

**Input Schema**:
```typescript
{
  limit?: number;      // Items per page (1-1000, default: 10)
  offset?: number;     // Pagination offset (≥0, default: 0)
  archived?: boolean;  // Show only archived chats (default: false)
}
```

**Output Schema**:
```typescript
{
  chats: Array<{
    id: string;                 // Chat identifier
    user_id: string;            // Owner user ID
    title: string;              // Chat title
    created_at: string;         // ISO 8601 timestamp
    updated_at: string;         // ISO 8601 timestamp
    messages?: Array<Message>;  // Optional messages array
    metadata?: object;          // Optional metadata
    archived?: boolean;         // Archive status
  }>;
  total: number;                // Total chats available
  limit: number;                // Items per page
  offset: number;               // Current offset
  has_next: boolean;            // More pages available
}
```

**Example Usage**:

```
Natural Language:
- "List all chats"
- "Show me the last 20 chats"
- "Get archived chats only"

Direct Tool Call:
{
  "name": "chat_list",
  "arguments": {
    "limit": 20,
    "offset": 0,
    "archived": false
  }
}
```

**Error Cases**:
- `VALIDATION_ERROR`: Invalid limit or offset
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SERVER_ERROR`: Open WebUI API unavailable

---

### chat_get

**Description**: Get specific chat by ID with full details

**MCP Tool Name**: `chat_get`

**Input Schema**:
```typescript
{
  chat_id: string;     // Chat identifier (required, alphanumeric + _-)
}
```

**Output Schema**:
```typescript
{
  chat: {
    id: string;
    user_id: string;
    title: string;
    created_at: string;      // ISO 8601
    updated_at: string;      // ISO 8601
    messages: Array<{
      id: string;
      role: "user" | "assistant" | "system";
      content: string | object;
      created_at: string;
    }>;
    metadata?: {
      model?: string;
      temperature?: number;
      [key: string]: any;
    };
    archived?: boolean;
    shared?: boolean;
    tags?: string[];
  }
}
```

**Example Usage**:

```
Natural Language:
- "Show me chat abc123"
- "Get details for chat xyz789"

Direct Tool Call:
{
  "name": "chat_get",
  "arguments": {
    "chat_id": "abc123"
  }
}
```

**Error Cases**:
- `VALIDATION_ERROR`: Invalid chat_id format (non-alphanumeric, >255 chars)
- `NOT_FOUND`: Chat does not exist
- `AUTH_ERROR`: Chat belongs to another user (if auth enabled)
- `SERVER_ERROR`: API error

---

## Model Tools

### model_list

**Description**: List available models with pagination

**MCP Tool Name**: `model_list`

**Input Schema**:
```typescript
{
  limit?: number;      // Items per page (1-1000, default: 20)
  offset?: number;     // Pagination offset (≥0, default: 0)
}
```

**Output Schema**:
```typescript
{
  models: Array<{
    id: string;                    // Model identifier
    name: string;                  // Display name
    description?: string;          // Model description
    size?: number;                 // Model size in bytes
    digest?: string;               // Model digest/hash
    created_at: string;            // ISO 8601
    capabilities?: {
      completion?: boolean;
      chat?: boolean;
      embedding?: boolean;
    };
    parameters?: {
      context_length?: number;
      temperature?: number;
      top_p?: number;
      [key: string]: any;
    };
  }>;
  total: number;
  limit: number;
  offset: number;
  has_next: boolean;
}
```

**Example Usage**:

```
Natural Language:
- "What models are available?"
- "List all AI models"
- "Show models 10-30"

Direct Tool Call:
{
  "name": "model_list",
  "arguments": {
    "limit": 50,
    "offset": 0
  }
}
```

**Error Cases**:
- `VALIDATION_ERROR`: Invalid pagination parameters
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SERVER_ERROR`: Open WebUI API unavailable

---

## User Tools

### user_list

**Description**: List users (requires admin privileges)

**MCP Tool Name**: `user_list`

**Authentication**: Requires admin-level API key

**Input Schema**:
```typescript
{
  limit?: number;      // Items per page (1-1000, default: 20)
  offset?: number;     // Pagination offset (≥0, default: 0)
}
```

**Output Schema**:
```typescript
{
  users: Array<{
    id: string;                // User identifier
    email: string;             // User email
    name: string;              // Display name
    role: "admin" | "user";    // User role
    created_at: string;        // ISO 8601
    last_active?: string;      // ISO 8601
    profile?: {
      avatar?: string;
      bio?: string;
      [key: string]: any;
    };
    settings?: object;
  }>;
  total: number;
  limit: number;
  offset: number;
  has_next: boolean;
}
```

**Example Usage**:

```
Natural Language:
- "Show all users"
- "List users with admin role"

Direct Tool Call:
{
  "name": "user_list",
  "arguments": {
    "limit": 100,
    "offset": 0
  }
}
```

**Error Cases**:
- `VALIDATION_ERROR`: Invalid pagination
- `AUTH_ERROR`: Missing or invalid API key, insufficient permissions
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SERVER_ERROR`: API error

**Note**: This tool requires `OPENWEBUI_API_KEY` environment variable with admin privileges.

---

## Admin Tools

### admin_health

**Description**: Check Open WebUI instance health status

**MCP Tool Name**: `admin_health`

**Input Schema**:
```typescript
{}  // No parameters required
```

**Output Schema**:
```typescript
{
  status: "healthy" | "unhealthy" | "degraded";
  version?: string;              // Open WebUI version
  uptime?: number;               // Uptime in seconds
  database?: {
    status: "connected" | "disconnected";
    type?: string;               // Database type (e.g., "postgresql")
  };
  api?: {
    status: "available" | "unavailable";
  };
  timestamp: string;             // ISO 8601 timestamp of check
}
```

**Example Usage**:

```
Natural Language:
- "Is Open WebUI healthy?"
- "Check system status"
- "What's the uptime?"

Direct Tool Call:
{
  "name": "admin_health",
  "arguments": {}
}
```

**Error Cases**:
- `SERVER_ERROR`: Health endpoint unavailable (indicates unhealthy system)

**Note**: No authentication required for health checks.

---

## Error Codes

### Error Code Reference

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Invalid input parameters | Check parameter types, ranges, formats |
| `NOT_FOUND` | Resource not found | Verify resource ID exists |
| `AUTH_ERROR` / `401 Unauthorized` | Authentication failed (missing/invalid API key) | Set `OPENWEBUI_API_KEY` environment variable with valid API key from Open WebUI Settings |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait before retry, check `OPENWEBUI_RATE_LIMIT` |
| `SERVER_ERROR` | Internal server error | Check Open WebUI logs, verify API reachable |
| `TIMEOUT_ERROR` | Request timeout | Increase `OPENWEBUI_TIMEOUT`, check network |
| `CONNECTION_ERROR` | Connection failed | Verify `OPENWEBUI_BASE_URL`, check Open WebUI running |

### Error Response Format

**Standard Error**:
```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "parameter_name",
    "reason": "specific reason"
  }
}
```

**Validation Error Example**:
```json
{
  "error": "Validation failed: limit must be between 1 and 1000",
  "code": "VALIDATION_ERROR",
  "details": {
    "field": "limit",
    "value": 2000,
    "constraint": "maximum: 1000"
  }
}
```

**Not Found Example**:
```json
{
  "error": "Chat not found: abc123",
  "code": "NOT_FOUND",
  "details": {
    "resource": "chat",
    "id": "abc123"
  }
}
```

**Rate Limit Example**:
```json
{
  "error": "Rate limit exceeded. Retry after 10 seconds",
  "code": "RATE_LIMIT_EXCEEDED",
  "details": {
    "retry_after": 10,
    "limit": 10,
    "window": "per_second"
  }
}
```

## Rate Limiting

### Configuration

Rate limiting configured via `OPENWEBUI_RATE_LIMIT` environment variable:

```bash
# Default: 10 requests per second
OPENWEBUI_RATE_LIMIT=10

# High traffic: 50 requests per second
OPENWEBUI_RATE_LIMIT=50

# Conservative: 5 requests per second
OPENWEBUI_RATE_LIMIT=5
```

### Algorithm

**Token Bucket**:
- Capacity: `OPENWEBUI_RATE_LIMIT` tokens
- Refill Rate: 1 token per (1/rate) seconds
- Burst Handling: Up to `rate` concurrent requests allowed
- Blocking: Requests wait for token availability (no 429 errors to MCP client)

### Behavior

**Normal Operation**:
1. Tool call acquires token
2. If token available: proceeds immediately
3. If no token: waits until refill
4. MCP client experiences slight delay (transparent)

**Under High Load**:
1. Requests queue for tokens
2. Server logs rate limiter state
3. Requests processed at configured rate
4. No errors surfaced to MCP client (graceful throttling)

### Monitoring

**Enable Debug Logging**:
```bash
# .env
LOG_LEVEL=DEBUG
LOG_FORMAT=text
```

**Debug Output**:
```
[DEBUG] Rate limiter: tokens=7.3/10, request=chat_list
[DEBUG] Rate limiter: acquired token, remaining=6.3/10
[DEBUG] Rate limiter: waiting 0.2s for token refill
```

### Tuning

**Factors to Consider**:
- Open WebUI server capacity
- Number of concurrent MCP clients
- Tool complexity (simple vs. complex queries)
- Network latency

**Recommended Settings**:
- **Single user, local Open WebUI**: 10-20 req/s
- **Multiple users, local Open WebUI**: 5-10 req/s
- **Remote Open WebUI**: 5 req/s (network latency)
- **Shared Open WebUI server**: 1-5 req/s (conservative)

---

## Future Tools (Not Yet Implemented)

### Tier 2: Knowledge & Files (30 tools)

**Knowledge Management** (8 tools):
- `knowledge_list`, `knowledge_get`, `knowledge_create`, `knowledge_update`, `knowledge_delete`
- `knowledge_items`, `knowledge_add_item`, `knowledge_remove_item`

**File Management** (6 tools):
- `file_list`, `file_get`, `file_upload`, `file_delete`, `file_content`, `file_metadata`

**Retrieval** (7 tools):
- `retrieval_query`, `retrieval_hybrid_search`, `retrieval_vector_search`
- `retrieval_config_get`, `retrieval_config_update`, `retrieval_collections`, `retrieval_documents`

### Tier 3: Functions (12 tools)

- `function_list`, `function_get`, `function_create`, `function_update`, `function_delete`
- `function_valves`, `function_user_valves`, `function_toggle`, `function_export`, `function_import`
- `function_test`, `function_call`

### Tier 4: Miscellaneous (90 tools)

- Prompts (8 tools)
- Tags (5 tools)
- Folders (6 tools)
- Evaluations (5 tools)
- Tasks (7 tools)
- Channels (5 tools)
- Memories (6 tools)
- Others (48 tools)

**Contributions Welcome!** See [CONTRIBUTING.md](CONTRIBUTING.md) for tool addition guide.

---

## Version

**API Version**: v1 (Open WebUI API v1)
**MCP Server Version**: 0.1.0 (MVP)
**Last Updated**: 2025-11-24
