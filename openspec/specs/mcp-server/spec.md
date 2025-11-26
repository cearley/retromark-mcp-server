# MCP Server

## Purpose
The MCP Server provides integration with Amazon Q CLI through the Model Context Protocol, enabling natural language bookmark management via AI assistants.

## Requirements

### Requirement: FastMCP Server Implementation
The system SHALL implement an MCP server using the FastMCP framework that exposes bookmark management tools to Amazon Q CLI.

#### Scenario: Server initialization
- **WHEN** the server is started via `src/server.py`
- **THEN** the FastMCP application initializes successfully
- **AND** the SQLite database is created at `~/Documents/github/retromark-mcp-server/data/bookmarks.db`
- **AND** all 8 MCP tools are registered and available

#### Scenario: Amazon Q CLI integration
- **WHEN** Amazon Q CLI is configured with the bookmark_manager MCP server
- **THEN** Amazon Q CLI can invoke any of the 8 registered tools
- **AND** tool responses are returned in a consistent dictionary format with success indicators

### Requirement: Tool Registration
The system SHALL expose exactly 8 bookmark management tools through MCP decorators.

#### Scenario: All tools registered
- **WHEN** the server starts
- **THEN** the following tools are available: get_url_data, store_url, search_bookmarks, list_categories, list_bookmarks_by_category, delete_bookmark, list_chrome_bookmarks, import_chrome_bookmark
- **AND** each tool is decorated with `@app.tool()` and has proper type hints

### Requirement: Consistent Response Format
All MCP tools SHALL return dictionaries with a success indicator.

#### Scenario: Successful operation
- **WHEN** an MCP tool completes successfully
- **THEN** it returns a dictionary with `{"success": True, "message": "...", ...}`
- **AND** includes relevant data fields as needed

#### Scenario: Failed operation
- **WHEN** an MCP tool encounters an error
- **THEN** it returns a dictionary with `{"success": False, "error": "..."}`
- **AND** includes the error message as a string

### Requirement: SQLite Storage Backend
The MCP server SHALL use SQLite as its exclusive storage backend.

#### Scenario: Database initialization
- **WHEN** `init_db()` is called on server start
- **THEN** the database is created with three tables: bookmarks, categories, tags
- **AND** the notes column is added dynamically if missing (migration pattern)

#### Scenario: Row factory configuration
- **WHEN** querying the database
- **THEN** `conn.row_factory = sqlite3.Row` is set
- **AND** rows can be accessed by column name like dictionaries

### Requirement: Mode Dispatcher Integration
The system SHALL be launchable through the main.py dispatcher.

#### Scenario: MCP mode launch
- **WHEN** `./main.py --mode mcp` is executed
- **THEN** the MCP server starts via `start_mcp_server()`
- **AND** the server runs continuously until terminated