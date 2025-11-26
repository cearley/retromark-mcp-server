# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Retromark is an MCP (Model Context Protocol) server that provides AI-assisted bookmark management through Amazon Q CLI. The project has two operational modes:

1. **MCP Server Mode**: Integrates with Amazon Q CLI for natural language bookmark management
2. **CLI Mode**: Standalone command-line interface for direct bookmark management

## Architecture

### Dual Storage System

The project maintains **two separate storage backends** for the different modes:

- **MCP Mode**: SQLite database at `~/Documents/github/retromark-mcp-server/data/bookmarks.db`
  - Tables: `bookmarks`, `categories`, `tags`
  - Full-featured with importance ratings, notes, timestamps
  - Used by `src/server.py`

- **CLI Mode**: JSON file at `~/Documents/github/retromark-mcp-server/data/url_database.json`
  - Simple category-based structure
  - Used by `src/url_manager.py`

**IMPORTANT**: These two storage backends are completely independent and do not sync with each other.

### Core Components

- **`main.py`**: Entry point that dispatches to either MCP server or CLI mode based on `--mode` flag
- **`src/server.py`**: FastMCP server implementation with 8 MCP tools for bookmark management
- **`src/url_manager.py`**: Standalone CLI implementation with argparse-based commands
- **`src/utils/browser_integration.py`**: Cross-platform Chrome bookmark reader (macOS, Windows, Linux)

### MCP Tools

The MCP server exposes 8 tools (defined with `@app.tool()` decorators):

1. `get_url_data` - Fetch and analyze webpage content
2. `store_url` - Save bookmark with metadata
3. `search_bookmarks` - Full-text search across bookmarks
4. `list_categories` - List all categories with counts
5. `list_bookmarks_by_category` - Get bookmarks in a category
6. `delete_bookmark` - Remove bookmark by URL
7. `list_chrome_bookmarks` - Read Chrome bookmarks from all profiles
8. `import_chrome_bookmark` - Import Chrome bookmark into LinkVault

### Web Scraping Logic

The `get_url_data` function (`src/server.py:86-239`) implements sophisticated content extraction:

- Multiple fallback strategies for title extraction (title tag → og:title → h1)
- Meta description with multiple attribute attempts
- Main content detection with common selector patterns
- AWS Workshop Studio special handling
- URL path component extraction for keyword generation
- Content truncation at 12,000 characters

## Development Commands

### Running the Project

```bash
# MCP Server mode (for Amazon Q CLI integration)
uv run src/server.py
# OR
./main.py --mode mcp

# CLI mode
./main.py --mode cli
# OR
./src/url_manager.py <command> [options]
```

### Installation

```bash
# Install dependencies using uv (recommended)
uv sync

# OR using pip
pip install -r requirements.txt

# Make scripts executable
chmod +x main.py src/url_manager.py src/server.py
```

### Testing the MCP Server

The MCP server can be tested by adding it to Amazon Q CLI's configuration at `~/.aws/amazonq/mcp.json`:

```json
"bookmark_manager": {
  "command": "uv",
  "args": ["--directory", "/path/to/retromark-mcp-server", "run", "src/server.py"],
  "env": {},
  "disabled": false,
  "autoApprove": ["get_url_data", "store_url", "search_bookmarks", "list_categories", "list_bookmarks_by_category", "delete_bookmark", "list_chrome_bookmarks", "import_chrome_bookmark"]
}
```

## Database Schema

### SQLite Schema (MCP Mode)

```sql
-- bookmarks table
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    category TEXT,
    tags TEXT,  -- JSON array as string
    description TEXT,
    importance INTEGER,
    created_at TEXT,
    last_accessed TEXT,
    notes TEXT  -- Added dynamically if missing
);

-- categories table
CREATE TABLE categories (
    name TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0
);

-- tags table
CREATE TABLE tags (
    name TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0
);
```

### Database Migration Pattern

The code includes a pattern for adding columns dynamically:

```python
cursor.execute("PRAGMA table_info(bookmarks)")
columns = [col[1] for col in cursor.fetchall()]
if "notes" not in columns:
    cursor.execute("ALTER TABLE bookmarks ADD COLUMN notes TEXT")
```

This pattern is used in `init_db()` and in `store_url()` to ensure the `notes` column exists.

## Browser Integration

The `browser_integration.py` module supports reading Chrome bookmarks across all platforms:

- **macOS**: `~/Library/Application Support/Google/Chrome/*/Bookmarks`
- **Windows**: `%LOCALAPPDATA%/Google/Chrome/User Data/*/Bookmarks`
- **Linux**: `~/.config/google-chrome/*/Bookmarks`

The integration:
- Scans all Chrome profiles using glob patterns
- Recursively extracts bookmarks from nested folder structures
- Preserves folder hierarchy in the `path` field
- Includes profile name in paths (e.g., "Default/Bookmarks Bar/Work")

## Code Patterns

### Error Handling

All MCP tools and CLI functions return dictionaries with `success` boolean:

```python
return {"success": True, "message": "...", ...}
# OR
return {"success": False, "error": "...", ...}
```

### URL Normalization

Both storage systems normalize URLs by adding `https://` if no protocol is specified:

```python
if not url.startswith(('http://', 'https://')):
    url = 'https://' + url
```

### Import Fallback Pattern

The codebase uses a try/except pattern for optional imports:

```python
try:
    from utils.browser_integration import get_chrome_bookmarks
except ImportError:
    def get_chrome_bookmarks(flat=True):
        return {"success": False, "error": "Browser integration module not available"}
```

This allows the code to function even if browser integration is unavailable.

## Key Implementation Details

1. **SQLite row_factory**: When reading from SQLite, `conn.row_factory = sqlite3.Row` is used to access columns by name
2. **Tag/Category Counts**: Maintained in separate tables and updated on bookmark add/delete operations
3. **JSON in SQLite**: Tags are stored as JSON strings and parsed with `json.loads(row["tags"])`
4. **BeautifulSoup Parsing**: Uses `html.parser` (built-in, no lxml required)
5. **Request Headers**: Custom User-Agent and headers in `get_url_data` to avoid blocking
6. **ISOFormat Timestamps**: All timestamps use `datetime.now().isoformat()`

## Dependencies

From `pyproject.toml`:
- `beautifulsoup4` - HTML parsing for content extraction
- `fastapi` - Web framework (used by FastMCP)
- `fastmcp` - MCP server framework
- `mcp` - Model Context Protocol library
- `requests` - HTTP client for fetching URLs

Minimum Python version: 3.10