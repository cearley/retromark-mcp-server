# Project Context

## Purpose

Retromark is a universal MCP (Model Context Protocol) server that provides AI-assisted bookmark management for any MCP-compatible client. The project enables users to manage, categorize, and search bookmarks using natural language through their preferred AI assistant or IDE, with automatic webpage content extraction and AI-assisted organization.

**Key Goals:**
- Universal MCP server supporting Claude Desktop, Claude Code, Continue.dev, Amazon Q CLI, and other MCP clients
- Multi-profile Chrome bookmark access and import capabilities
- Automatic webpage metadata extraction and content analysis
- Cross-platform support (macOS, Windows, Linux)
- Dual operational modes: MCP server (AI-assisted) and standalone CLI
- Three distinct use cases: Desktop AI chat, IDE integration, and terminal workflows

## Tech Stack

- **Language**: Python 3.10+
- **MCP Framework**: FastMCP (v2.5.1+)
- **Database**: SQLite (for MCP server mode)
- **Web Scraping**: BeautifulSoup4, requests
- **Package Manager**: uv (recommended) or pip
- **Runtime**: FastAPI (used by FastMCP)

### Core Dependencies

- `beautifulsoup4>=4.13.4` - HTML parsing for content extraction
- `fastapi>=0.115.12` - Web framework (used by FastMCP)
- `fastmcp>=2.5.1` - MCP server framework
- `mcp>=1.9.1` - Model Context Protocol library
- `requests>=2.32.3` - HTTP client for fetching URLs

## Project Conventions

### Code Style

- **Type Hints**: Required on all function parameters and return values
  - Common types: `str`, `int`, `List[str]`, `Dict[str, Any]`, `Optional[str]`
  - Return dictionaries typed as `Dict[str, Any]`

- **Naming Conventions**:
  - Functions: `snake_case` (e.g., `get_url_data`, `list_categories`)
  - Variables: `snake_case` (e.g., `bookmark_paths`, `main_content`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `DB_PATH`, `DATA_DIR`)
  - MCP Tools: Named with underscores (e.g., `@app.tool("get_url_data")`)

- **Docstrings**: Google-style format
  - One-line summary for simple functions
  - Full docstrings with Args and Returns sections for MCP tools and public functions

- **Import Organization**:
  1. Standard library imports
  2. Third-party imports
  3. Local imports with try-except fallback pattern for optional dependencies

- **File Headers**: All Python files start with shebang and module docstring:
  ```python
  #!/usr/bin/env python3
  """
  Module/script description.
  """
  ```

### Architecture Patterns

**Dual Storage Backend Pattern:**
- MCP Server Mode: SQLite database (`~/Documents/github/retromark-mcp-server/data/bookmarks.db`)
- CLI Mode: JSON file (`~/Documents/github/retromark-mcp-server/data/url_database.json`)
- **CRITICAL**: These storage backends are completely independent and do not sync

**Error Handling Pattern:**
All public functions return dictionaries with consistent structure:
```python
# Success
{"success": True, "message": "...", ...}

# Failure
{"success": False, "error": "...", ...}
```

**URL Normalization Pattern:**
Always normalize URLs by adding `https://` if no protocol specified:
```python
if not url.startswith(('http://', 'https://')):
    url = 'https://' + url
```

**SQLite Best Practices:**
- Use `conn.row_factory = sqlite3.Row` for dictionary-like row access
- Always use parameterized queries: `cursor.execute("... WHERE url = ?", (url,))`
- Close connections explicitly: `conn.close()`
- Check column existence with `PRAGMA table_info(table)` before accessing

**Import Fallback Pattern:**
Optional dependencies handled with try-except:
```python
try:
    from utils.browser_integration import get_chrome_bookmarks
except ImportError:
    def get_chrome_bookmarks(flat=True):
        return {"success": False, "error": "Browser integration module not available"}
```

**Database Migration Pattern:**
Dynamic schema updates for backward compatibility:
```python
cursor.execute("PRAGMA table_info(bookmarks)")
columns = [col[1] for col in cursor.fetchall()]
if "notes" not in columns:
    cursor.execute("ALTER TABLE bookmarks ADD COLUMN notes TEXT")
```

### Testing Strategy

Currently, the project does not have automated tests. Testing is manual:

- **MCP Server Testing**: Integration testing through Amazon Q CLI configuration at `~/.aws/amazonq/mcp.json`
- **CLI Testing**: Manual command-line testing of all CLI commands
- **Browser Integration Testing**: Testing across different platforms (macOS, Windows, Linux)

### Git Workflow

- **Main Branch**: `main`
- **Commit Style**: Descriptive commit messages focusing on "what" and "why"
- **Workflow**: Direct commits to main branch (small project, single developer)

## Domain Context

### Model Context Protocol (MCP)

MCP is a protocol for AI assistants to interact with external tools and data sources. Retromark implements an MCP server that exposes 8 bookmark management tools to Amazon Q CLI.

**MCP Tools Exposed:**
1. `get_url_data` - Fetch and analyze webpage content
2. `store_url` - Save bookmark with metadata (title, category, tags, importance, notes)
3. `search_bookmarks` - Full-text search across all bookmark fields
4. `list_categories` - List all categories with bookmark counts
5. `list_bookmarks_by_category` - Get bookmarks in a specific category
6. `delete_bookmark` - Remove bookmark by URL
7. `list_chrome_bookmarks` - Read Chrome bookmarks from all profiles
8. `import_chrome_bookmark` - Import Chrome bookmark into Retromark

### Web Content Extraction

The `get_url_data` function implements sophisticated content extraction with multiple fallback strategies:

- **Title Extraction**: title tag → og:title → h1
- **Description**: Multiple meta tag attempts
- **Main Content**: Common selector patterns (article, main, .content, etc.)
- **Special Handling**: AWS Workshop Studio detection
- **Keyword Generation**: URL path component extraction
- **Content Limits**: Truncation at 12,000 characters

### Chrome Bookmark Integration

Cross-platform bookmark file location detection:
- **macOS**: `~/Library/Application Support/Google/Chrome/*/Bookmarks`
- **Windows**: `%LOCALAPPDATA%/Google/Chrome/User Data/*/Bookmarks`
- **Linux**: `~/.config/google-chrome/*/Bookmarks`

Features:
- Scans all Chrome profiles using glob patterns
- Recursively extracts bookmarks from nested folder structures
- Preserves folder hierarchy in path field (e.g., "Default/Bookmarks Bar/Work")

## Important Constraints

### Storage Independence

**CRITICAL**: The two storage backends (SQLite for MCP mode, JSON for CLI mode) are completely independent. Changes in one mode do not sync to the other mode. Users must be aware that bookmarks added via Amazon Q CLI will not appear when using the standalone CLI, and vice versa.

### Platform Considerations

- **Primary Development Platform**: macOS (Darwin 24.6.0)
- **Cross-Platform Support**: Code handles platform-specific paths for Chrome bookmarks
- **File Permissions**: Scripts require execute permissions (`chmod +x`)

### Database Schema Evolution

The SQLite schema includes dynamic migration logic (e.g., adding `notes` column if missing). This ensures backward compatibility when new fields are added.

### Content Extraction Limits

- **Maximum Content Size**: 12,000 characters per webpage
- **HTTP Client**: Custom User-Agent required to avoid blocking
- **Parser**: BeautifulSoup uses `html.parser` (built-in, no lxml dependency)

## External Dependencies

### MCP Clients

Retromark works with any MCP-compatible client. Below are the tested and documented clients:

#### Claude Desktop (Primary)

Configuration file: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

Example configuration:
```json
{
  "mcpServers": {
    "retromark": {
      "command": "uv",
      "args": ["--directory", "/path/to/retromark-mcp-server", "run", "src/server.py"]
    }
  }
}
```

**Use case**: General-purpose AI chat and assistance with bookmark management.

#### Continue.dev (Secondary)

Configuration file: `~/.continue/config.json` or `~/.continue/mcpServers/retromark.yaml`

Example JSON configuration:
```json
{
  "mcpServers": {
    "retromark": {
      "command": "uv",
      "args": ["--directory", "/path/to/retromark-mcp-server", "run", "src/server.py"]
    }
  }
}
```

**Use case**: IDE-integrated bookmark management while coding (VS Code/JetBrains). Access via @ menu in Continue.dev.

**Features**: First client with full MCP support (Resources, Prompts, Tools, Sampling). Supports both JSON and YAML config formats.

#### Amazon Q CLI (Tertiary)

Configuration file: `~/.aws/amazonq/mcp.json`

Example configuration:
```json
{
  "bookmark_manager": {
    "command": "uv",
    "args": ["--directory", "/path/to/retromark-mcp-server", "run", "src/server.py"],
    "env": {},
    "disabled": false,
    "autoApprove": ["get_url_data", "store_url", "search_bookmarks",
                    "list_categories", "list_bookmarks_by_category",
                    "delete_bookmark", "list_chrome_bookmarks",
                    "import_chrome_bookmark"]
  }
}
```

**Use case**: Terminal-based workflows and AWS-focused development.

### Google Chrome

Read-only dependency for bookmark import feature. The browser integration module reads Chrome's bookmark JSON files directly from the file system (no Chrome API calls).

### Web Content Sources

HTTP requests to arbitrary websites for content extraction. Requires:
- Network connectivity
- Websites allowing automated access (some may block requests)
- HTTPS support (URLs normalized to https://)

## Project History

- Previously named "LinkVault", rebranded to "Retromark"
- Initial focus: Personal bookmark management CLI
- Evolution: Added MCP server capabilities for Amazon Q CLI integration
- **v0.2.0**: Repositioned as universal MCP server supporting Claude Desktop, Claude Code, Continue.dev, Amazon Q CLI, and other MCP clients
- Current state: Dual-mode operation (MCP server + standalone CLI) with multi-client support