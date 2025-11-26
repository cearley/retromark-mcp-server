# CLI Mode

## Purpose
Standalone command-line interface for direct bookmark management using JSON file storage, independent of the MCP server mode.

## Requirements

### Requirement: JSON Storage Backend
The CLI mode SHALL use a separate JSON file as its storage backend, independent from the MCP server's SQLite database.

#### Scenario: JSON database location
- **WHEN** CLI mode is used
- **THEN** the database file is located at `~/Documents/github/retromark-mcp-server/data/url_database.json`
- **AND** the storage is completely independent from the SQLite database used by MCP mode

#### Scenario: Database structure
- **WHEN** the JSON database is loaded
- **THEN** it has the structure `{"categories": {"category_name": [bookmark_objects]}}`
- **AND** each bookmark object contains url, title, description, tags, date_added, and last_accessed fields

#### Scenario: Create database if missing
- **WHEN** the JSON database file doesn't exist
- **THEN** `load_database()` creates a new file with empty structure `{"categories": {}}`
- **AND** the file is created in the data directory

### Requirement: Argparse Command Interface
The CLI SHALL use argparse for command-line argument parsing and command dispatch.

#### Scenario: Command dispatch
- **WHEN** a CLI command is executed (e.g., `./src/url_manager.py add <url> <category>`)
- **THEN** argparse parses the command and arguments
- **AND** the appropriate function is called based on the command
- **AND** results are printed to stdout

### Requirement: Add Bookmark via CLI
The CLI SHALL support adding bookmarks with category and optional metadata.

#### Scenario: Add bookmark with minimal info
- **WHEN** `add` command is executed with url and category
- **THEN** the URL is normalized (https:// prefix added if needed)
- **AND** the bookmark is added to the specified category in the JSON database
- **AND** timestamp fields are set using `datetime.now().isoformat()`

#### Scenario: Add bookmark with full metadata
- **WHEN** `add` command includes title, description, and tags
- **THEN** all metadata is stored with the bookmark
- **AND** tags are stored as a list of strings

### Requirement: List CLI Categories
The CLI SHALL list all categories with bookmark counts.

#### Scenario: List all categories
- **WHEN** `list-categories` command is executed
- **THEN** all categories are displayed with their bookmark counts
- **AND** results are sorted alphabetically

### Requirement: List Bookmarks in Category
The CLI SHALL retrieve bookmarks for a specific category.

#### Scenario: List category bookmarks
- **WHEN** `list` command is executed with a category name
- **THEN** all bookmarks in that category are displayed
- **AND** each bookmark shows url, title, description, and tags

#### Scenario: Non-existent category
- **WHEN** listing a category that doesn't exist
- **THEN** an appropriate message is shown
- **AND** the command exits gracefully

### Requirement: Search Bookmarks via CLI
The CLI SHALL support searching bookmarks by query term.

#### Scenario: Search across fields
- **WHEN** `search` command is executed with a query
- **THEN** results include bookmarks where the query matches url, title, description, category, or tags
- **AND** search is case-insensitive
- **AND** results show which category each bookmark is in

### Requirement: Tag Operations
The CLI SHALL support listing tags and finding bookmarks by tag.

#### Scenario: List all tags
- **WHEN** `list-tags` command is executed
- **THEN** all unique tags across all bookmarks are displayed
- **AND** tag counts are shown

#### Scenario: Find bookmarks by tag
- **WHEN** `list-by-tag` command is executed with a tag name
- **THEN** all bookmarks containing that tag are displayed
- **AND** results show the category for each bookmark

### Requirement: Delete Bookmark via CLI
The CLI SHALL support removing bookmarks by URL.

#### Scenario: Delete existing bookmark
- **WHEN** `delete` command is executed with a URL
- **THEN** the bookmark is removed from the JSON database
- **AND** the database is saved
- **AND** a confirmation message is displayed

#### Scenario: Delete non-existent bookmark
- **WHEN** deleting a URL that doesn't exist
- **THEN** an appropriate error message is shown

### Requirement: Category Management
The CLI SHALL support renaming and deleting categories.

#### Scenario: Rename category
- **WHEN** `rename-category` command is executed with old and new names
- **THEN** the category is renamed in the JSON database
- **AND** all bookmarks in that category are preserved
- **AND** the database is saved

#### Scenario: Delete category
- **WHEN** `delete-category` command is executed
- **THEN** the entire category and all its bookmarks are removed
- **AND** a confirmation is requested before deletion

### Requirement: Chrome Bookmark Integration in CLI
The CLI SHALL support listing and importing Chrome bookmarks.

#### Scenario: List Chrome bookmarks via CLI
- **WHEN** `list-chrome` command is executed
- **THEN** Chrome bookmarks from all profiles are displayed
- **AND** folder paths are shown for each bookmark

#### Scenario: Import Chrome bookmark to CLI
- **WHEN** `import-chrome` command is executed with a URL and category
- **THEN** the bookmark is located in Chrome bookmarks
- **AND** it's imported into the JSON database under the specified category
- **AND** Chrome folder path and metadata are preserved

### Requirement: Mode Dispatcher Integration for CLI
The CLI SHALL be launchable through the main.py dispatcher.

#### Scenario: CLI mode launch
- **WHEN** `./main.py --mode cli` is executed (or no mode specified, as CLI is default)
- **THEN** the CLI interface starts via `start_cli()`
- **AND** the argparse help message is displayed if no command is given

### Requirement: Storage Independence
The CLI mode storage SHALL remain completely separate from MCP mode storage.

#### Scenario: No synchronization between modes
- **WHEN** bookmarks are added via CLI mode
- **THEN** they do NOT appear in MCP mode's SQLite database
- **WHEN** bookmarks are added via MCP mode
- **THEN** they do NOT appear in CLI mode's JSON database
- **AND** users must be aware of this storage separation
