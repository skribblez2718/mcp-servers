# Open WebUI MCP Server

A Model Context Protocol (MCP) server providing programmatic access to Open WebUI's REST API. Built with Python 3.10+ and HTTP SSE transport.

## Features

- **329 MCP Tools** - Complete coverage of Open WebUI's REST API
- **HTTP SSE Transport** - Works with Claude Code, Claude Desktop, Cursor, Windsurf
- **Security Hardened** - Input validation, rate limiting, error sanitization
- **Modern Python** - Type hints, Pydantic validation, uv-based dependency management

## Prerequisites

- **Python 3.10+**
- **uv** package manager ([install](https://github.com/astral-sh/uv))
- **Open WebUI** instance (local or remote)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start

```bash
# Clone and install
cd /path/to/open-webui-mcp
uv sync

# Configure
cp .env.example .env
# Edit .env with your Open WebUI URL and API key

# Start server
uv run python -m src.server
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENWEBUI_BASE_URL` | **Yes** | - | Open WebUI instance URL (e.g., `http://localhost:8080`) |
| `OPENWEBUI_API_KEY` | **Yes** | - | API key from Open WebUI → Settings → Account → API Keys |
| `HOST` | No | `127.0.0.1` | Server bind address |
| `PORT` | No | `8000` | Server port |
| `OPENWEBUI_TIMEOUT` | No | `30` | Request timeout (seconds) |
| `OPENWEBUI_RATE_LIMIT` | No | `10` | Requests per second |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## MCP Client Setup

Start the server first, then configure your client:

### Claude Code

```bash
claude mcp add open-webui --transport sse http://127.0.0.1:8000/sse
```

### Claude Desktop / Cursor / Windsurf

Add to your MCP config file:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Config locations:**
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Cursor: `~/Library/Application Support/Cursor/mcp_settings.json`
- Windsurf: `~/Library/Application Support/Windsurf/mcp_config.json`

## Available Tools

329 tools organized by category:

### Chats (39 tools)
`chat_list`, `chat_get`, `create_new_chat_chats_new`, `update_chat_by_id_chats_id`, `delete_chat_by_id_chats_id`, `clone_chat_by_id_chats_id_clone`, `archive_chat_by_id_chats_id_archive`, `archive_all_chats_chats_archive_all`, `share_chat_by_id_chats_id_share`, `delete_shared_chat_by_id_chats_id_share`, `clone_shared_chat_by_id_chats_id_clone_shared`, `get_shared_chat_by_id_chats_share_share_id`, `pin_chat_by_id_chats_id_pin`, `get_pinned_status_by_id_chats_id_pinned`, `get_user_pinned_chats_chats_pinned`, `import_chat_chats_import`, `get_chat_by_id_chats_id`, `get_chat_tags_by_id_chats_id_tags`, `add_tag_by_id_and_tag_name_chats_id_tags`, `delete_tag_by_id_and_tag_name_chats_id_tags`, `delete_all_tags_by_id_chats_id_tags_all`, `get_all_user_tags_chats_all_tags`, `get_user_chat_list_by_tag_name_chats_tags`, `search_user_chats_chats_search`, `get_session_user_chat_list_chats`, `get_session_user_chat_list_chats_list`, `get_archived_session_user_chat_list_chats_archived`, `get_user_archived_chats_chats_all_archived`, `get_user_chats_chats_all`, `get_all_user_chats_in_db_chats_all_db`, `delete_all_user_chats_chats`, `get_user_chat_list_by_user_id_chats_list_user_user_id`, `get_chats_by_folder_id_chats_folder_folder_id`, `update_chat_folder_id_by_id_chats_id_folder`, `update_chat_message_by_id_chats_id_messages_message_id`, `send_chat_message_event_by_id_chats_id_messages_message_id_event`, `chat_action_chat_actions_action_id`, `chat_completed_chat_completed`, `chat_completion_chat_completions`

### Ollama (39 tools)
`get_status_ollama`, `get_config_ollama_config`, `update_config_ollama_config_update`, `verify_connection_ollama_verify`, `get_ollama_tags_ollama_tags`, `get_ollama_tags_ollama_tags_url_idx`, `get_ollama_versions_ollama_version`, `get_ollama_versions_ollama_version_url_idx`, `get_ollama_loaded_models_ollama_ps`, `pull_model_ollama_pull`, `pull_model_ollama_pull_url_idx`, `push_model_ollama_push`, `push_model_ollama_push_url_idx`, `create_model_ollama_create`, `create_model_ollama_create_url_idx`, `copy_model_ollama_copy`, `copy_model_ollama_copy_url_idx`, `delete_model_ollama`, `delete_model_ollama_url_idx`, `show_model_info_ollama_show`, `download_model_ollama_models_download`, `download_model_ollama_models_download_url_idx`, `upload_model_ollama_models_upload`, `upload_model_ollama_models_upload_url_idx`, `unload_model_ollama_unload`, `generate_completion_ollama_generate`, `generate_completion_ollama_generate_url_idx`, `generate_chat_completion_ollama_chat`, `generate_chat_completion_ollama_chat_url_idx`, `generate_openai_chat_completion_ollama_v1_chat_completions`, `generate_openai_chat_completion_ollama_v1_chat_completions_url_idx`, `generate_openai_completion_ollama_v1_completions`, `generate_openai_completion_ollama_v1_completions_url_idx`, `get_openai_models_ollama_v1_models`, `get_openai_models_ollama_v1_models_url_idx`, `embed_ollama_embed`, `embed_ollama_embed_url_idx`, `embeddings_ollama_embeddings`, `embeddings_ollama_embeddings_url_idx`

### Authentication (18 tools)
`get_session_user_auths`, `signin_auths_signin`, `signup_auths_signup`, `signout_auths_signout`, `add_user_auths_add`, `update_profile_auths_update_profile`, `update_password_auths_update_password`, `get_key_auths_key`, `generate_key_auths_key`, `delete_key_auths_key`, `get_admin_config_auths_admin_config`, `update_admin_config_auths_admin_config`, `get_admin_details_auths_admin_details`, `get_ldap_config_auths_admin_config_ldap`, `update_ldap_config_auths_admin_config_ldap`, `get_ldap_server_auths_admin_config_ldap_server`, `update_ldap_server_auths_admin_config_ldap_server`, `ldap_auth_auths_ldap`

### RAG/Retrieval (17 tools)
`get_status_retrieval`, `get_rag_config_retrieval_config`, `update_rag_config_retrieval_config_update`, `get_embedding_config_retrieval_embedding`, `update_embedding_config_retrieval_embedding_update`, `get_embeddings_retrieval_ef_text`, `process_file_retrieval_process_file`, `process_files_batch_retrieval_process_files_batch`, `process_text_retrieval_process_text`, `process_web_retrieval_process_web`, `process_web_search_retrieval_process_web_search`, `process_youtube_video_retrieval_process_youtube`, `query_doc_handler_retrieval_query_doc`, `query_collection_handler_retrieval_query_collection`, `delete_entries_from_collection_retrieval`, `reset_vector_db_retrieval_reset_db`, `reset_upload_dir_retrieval_reset_uploads`

### Users (16 tools)
`user_list`, `get_users_users`, `get_all_users_users_all`, `get_active_users_users_active`, `get_user_by_id_users_user_id`, `update_user_by_id_users_user_id_update`, `delete_user_by_id_users_user_id`, `get_user_active_status_by_id_users_user_id_active`, `get_user_groups_users_groups`, `get_user_permissisions_users_permissions`, `get_default_user_permissions_users_default_permissions`, `update_default_user_permissions_users_default_permissions`, `get_user_info_by_session_user_users_user_info`, `update_user_info_by_session_user_users_user_info_update`, `get_user_settings_by_session_user_users_user_settings`, `update_user_settings_by_session_user_users_user_settings_update`

### Functions (16 tools)
`get_functions_functions`, `get_functions_functions_export`, `create_new_function_functions_create`, `get_function_by_id_functions_id_id`, `update_function_by_id_functions_id_id_update`, `delete_function_by_id_functions_id_id`, `toggle_function_by_id_functions_id_id_toggle`, `toggle_global_by_id_functions_id_id_toggle_global`, `get_function_valves_by_id_functions_id_id_valves`, `get_function_valves_spec_by_id_functions_id_id_valves_spec`, `update_function_valves_by_id_functions_id_id_valves_update`, `get_function_user_valves_by_id_functions_id_id_valves_user`, `get_function_user_valves_spec_by_id_functions_id_id_valves_user_spec`, `update_function_user_valves_by_id_functions_id_id_valves_user_update`, `sync_functions_functions_sync`, `load_function_from_url_functions_load_url`

### Configuration (15 tools)
`get_app_config_config`, `get_app_version_version`, `get_app_latest_release_version_version_updates`, `get_app_changelog_changelog`, `export_config_configs_export`, `import_config_configs_import`, `get_banners_configs_banners`, `set_banners_configs_banners`, `get_connections_config_configs_connections`, `set_connections_config_configs_connections`, `get_models_config_configs_models`, `set_models_config_configs_models`, `get_code_execution_config_configs_code_execution`, `set_code_execution_config_configs_code_execution`, `set_default_suggestions_configs_suggestions`

### Channels (14 tools)
`get_channels_channels`, `get_all_channels_channels_list`, `create_new_channel_channels_create`, `get_channel_by_id_channels_id`, `update_channel_by_id_channels_id_update`, `delete_channel_by_id_channels_id`, `get_channel_messages_channels_id_messages`, `post_new_message_channels_id_messages`, `get_channel_message_channels_id_messages_message_id`, `update_message_by_id_channels_id_messages_message_id_update`, `delete_message_by_id_channels_id_messages_message_id`, `get_channel_thread_messages_channels_id_messages_message_id_thread`, `add_reaction_to_message_channels_id_messages_message_id_reactions_add`, `remove_reaction_by_id_and_user_id_and_name_channels_id_messages_message_id_reactions_remove`

### Tools (14 tools)
`get_tools_tools`, `get_tool_list_tools_list`, `export_tools_tools_export`, `create_new_tools_tools_create`, `get_tools_by_id_tools_id_id`, `update_tools_by_id_tools_id_id_update`, `delete_tools_by_id_tools_id_id`, `get_tools_valves_by_id_tools_id_id_valves`, `get_tools_valves_spec_by_id_tools_id_id_valves_spec`, `update_tools_valves_by_id_tools_id_id_valves_update`, `get_tools_user_valves_by_id_tools_id_id_valves_user`, `get_tools_user_valves_spec_by_id_tools_id_id_valves_user_spec`, `update_tools_user_valves_by_id_tools_id_id_valves_user_update`, `load_tool_from_url_tools_load_url`

### Tasks (13 tools)
`list_tasks_endpoint_tasks`, `list_tasks_by_chat_id_endpoint_tasks_chat_chat_id`, `stop_task_endpoint_tasks_stop_task_id`, `get_task_config_tasks_config`, `update_task_config_tasks_config_update`, `generate_title_tasks_title_completions`, `generate_chat_tags_tasks_tags_completions`, `generate_emoji_tasks_emoji_completions`, `generate_autocompletion_tasks_auto_completions`, `generate_queries_tasks_queries_completions`, `generate_follow_ups_tasks_follow_up_completions`, `generate_image_prompt_tasks_image_prompt_completions`, `generate_moa_response_tasks_moa_completions`

### Knowledge (12 tools)
`get_knowledge_knowledge`, `get_knowledge_list_knowledge_list`, `create_new_knowledge_knowledge_create`, `get_knowledge_by_id_knowledge_id`, `update_knowledge_by_id_knowledge_id_update`, `delete_knowledge_by_id_knowledge_id`, `reset_knowledge_by_id_knowledge_id_reset`, `add_file_to_knowledge_by_id_knowledge_id_file_add`, `add_files_to_knowledge_batch_knowledge_id_files_batch_add`, `update_file_from_knowledge_by_id_knowledge_id_file_update`, `remove_file_from_knowledge_by_id_knowledge_id_file_remove`, `reindex_knowledge_files_knowledge_reindex`

### Files (11 tools)
`list_files_files`, `upload_file_files`, `get_file_by_id_files_id`, `delete_file_by_id_files_id`, `get_file_content_by_id_files_id_content`, `get_file_content_by_id_files_id_content_file_name`, `get_file_data_content_by_id_files_id_data_content`, `update_file_data_content_by_id_files_id_data_content_update`, `get_html_file_content_by_id_files_id_content_html`, `search_files_files_search`, `delete_all_files_files_all`

### Evaluations/Feedback (11 tools)
`get_config_evaluations_config`, `update_config_evaluations_config`, `get_feedbacks_evaluations_feedbacks_user`, `get_all_feedbacks_evaluations_feedbacks_all`, `get_all_feedbacks_evaluations_feedbacks_all_export`, `create_feedback_evaluations_feedback`, `get_feedback_by_id_evaluations_feedback_id`, `update_feedback_by_id_evaluations_feedback_id`, `delete_feedback_by_id_evaluations_feedback_id`, `delete_feedbacks_evaluations_feedbacks`, `delete_all_feedbacks_evaluations_feedbacks_all`

### Models (9 tools)
`model_list`, `get_models_models`, `get_base_models_models_base`, `create_new_model_models_create`, `get_model_by_id_models_model`, `update_model_by_id_models_model_update`, `delete_model_by_id_models_model`, `toggle_model_by_id_models_model_toggle`, `delete_all_models_models_all`

### OpenAI (8 tools)
`get_config_openai_config`, `update_config_openai_config_update`, `verify_connection_openai_verify`, `get_models_openai_models`, `get_models_openai_models_url_idx`, `generate_chat_completion_openai_chat_completions`, `proxy_openai_path`, `speech_openai_audio_speech`

### Pipelines (8 tools)
`get_pipelines_pipelines`, `get_pipelines_list_pipelines_list`, `add_pipeline_pipelines_add`, `delete_pipeline_pipelines`, `upload_pipeline_pipelines_upload`, `get_pipeline_valves_pipelines_pipeline_id_valves`, `get_pipeline_valves_spec_pipelines_pipeline_id_valves_spec`, `update_pipeline_valves_pipelines_pipeline_id_valves_update`

### Images (7 tools)
`get_config_images_config`, `update_config_images_config_update`, `get_image_config_images_image_config`, `update_image_config_images_image_config_update`, `get_models_images_models`, `image_generations_images_generations`, `verify_url_images_config_url_verify`

### Groups (7 tools)
`get_groups_groups`, `create_new_group_groups_create`, `get_group_by_id_groups_id_id`, `update_group_by_id_groups_id_id_update`, `delete_group_by_id_groups_id_id`, `add_user_to_group_groups_id_id_users_add`, `remove_users_from_group_groups_id_id_users_remove`

### Folders (7 tools)
`get_folders_folders`, `create_folder_folders`, `get_folder_by_id_folders_id`, `delete_folder_by_id_folders_id`, `update_folder_name_by_id_folders_id_update`, `update_folder_parent_id_by_id_folders_id_update_parent`, `update_folder_is_expanded_by_id_folders_id_update_expanded`

### Utilities (7 tools)
`download_chat_as_pdf_utils_pdf`, `get_html_from_markdown_utils_markdown`, `get_gravatar_utils_gravatar`, `execute_code_utils_code_execute`, `format_code_utils_code_format`, `download_db_utils_db_download`, `download_litellm_config_yaml_utils_litellm_config`

### Audio (6 tools)
`get_audio_config_audio_config`, `update_audio_config_audio_config_update`, `get_models_audio_models`, `get_voices_audio_voices`, `speech_audio_speech`, `transcription_audio_transcriptions`

### Prompts (6 tools)
`get_prompts_prompts`, `get_prompt_list_prompts_list`, `create_new_prompt_prompts_create`, `get_prompt_by_command_prompts_command_command`, `update_prompt_by_command_prompts_command_command_update`, `delete_prompt_by_command_prompts_command_command`

### Notes (6 tools)
`get_notes_notes`, `get_note_list_notes_list`, `create_new_note_notes_create`, `get_note_by_id_notes_id`, `update_note_by_id_notes_id_update`, `delete_note_by_id_notes_id`

### Memory (6 tools)
`get_memories_memories`, `add_memory_memories_add`, `query_memory_memories_query`, `get_embeddings_memories_ef`, `update_memory_by_id_memories_memory_id_update`, `delete_memory_by_id_memories_memory_id`, `delete_memory_by_user_id_memories_user`, `reset_memory_from_vector_db_memories_reset`

### Tool Servers (3 tools)
`get_tool_servers_config_configs_tool_servers`, `set_tool_servers_config_configs_tool_servers`, `verify_tool_servers_config_configs_tool_servers_verify`

### Other (7 tools)
`admin_health`, `healthcheck_health`, `healthcheck_with_db_health_db`, `get_webhook_url_webhook`, `update_webhook_url_webhook`, `oauth_login_oauth_provider_login`, `oauth_callback_oauth_provider_callback`, `get_manifest_json_manifest_json`, `get_opensearch_xml_opensearch_xml`, `get_current_usage_usage`, `serve_cache_file_cache_path`, `embeddings_embeddings`

## Verify Installation

```bash
# Check server is running
curl http://127.0.0.1:8000/sse

# In Claude: "Check Open WebUI health status"
# Should invoke admin_health tool
```

## License

MIT License - see [LICENSE](LICENSE) file.
