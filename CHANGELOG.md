# Changelog

## [Unreleased]

### Added - Universal MCP Client Support
- **Claude Desktop & Claude Code support** (Primary)
  - Configuration guide for macOS, Windows, and Linux
  - Example workflows for desktop AI chat and research
  - Natural language bookmark management through Claude

- **Continue.dev support** (Secondary - IDE Integration)
  - VS Code and JetBrains IDE integration
  - Bookmark management via @ menu while coding
  - Full MCP feature support (Resources, Prompts, Tools, Sampling)
  - JSON and YAML configuration formats

- **Amazon Q CLI support** (Tertiary - Terminal Workflows)
  - Repositioned as one of several supported clients
  - Terminal-based bookmark management
  - Auto-approve configuration for scripting
  - AWS-focused documentation workflows

### Changed
- **Repositioned as universal MCP server** (breaking change in positioning, not functionality)
  - Updated all documentation to be client-agnostic
  - Removed Amazon Q CLI-specific assumptions
  - Updated project tagline and description
  - Version bumped from 0.1.0 to 0.2.0

- **Documentation restructure**
  - Created `/docs` directory with client-specific guides
  - Split README into modular documentation
  - Added comprehensive setup guides for each client
  - Added client comparison guide
  - Added troubleshooting guide

- **Code updates**
  - Updated `src/server.py` module docstring to mention all clients
  - Updated `main.py` help text to be client-agnostic
  - Updated `pyproject.toml` description and keywords
  - Updated `openspec/project.md` with multi-client documentation

### New Documentation
- `docs/claude-setup.md` - Complete Claude Desktop/Code setup and workflows
- `docs/continue-setup.md` - Complete Continue.dev setup for IDE integration
- `docs/amazonq-setup.md` - Complete Amazon Q CLI setup (updated from main README)
- `docs/client-comparison.md` - Decision guide for choosing the right client
- `docs/troubleshooting.md` - Common issues and solutions for all clients

### Improved
- README.md now focuses on quick start with links to detailed guides
- Better separation of concerns in documentation
- Clearer use case definitions for each client
- Enhanced configuration examples with platform-specific paths
- Added architecture diagram showing multi-client support

### Backward Compatibility
- ✅ **Fully backward compatible** - Existing Amazon Q CLI configurations continue to work
- All existing tools and functionality unchanged
- Same database format and storage locations
- No breaking API changes

## [Unreleased]

### Changed
- Rebranded from LinkVault to Retromark
- Updated all documentation and code references
- Changed package name to retromark-mcp-server
- Updated database paths to use retromark-mcp-server directory
- Configured as a proper uv project with Python 3.13 support

## [1.1.0] - 2025-05-28

### Added
- Chrome bookmark integration
  - Support for listing Chrome bookmarks across all profiles
  - Import Chrome bookmarks into LinkVault
  - Filter bookmarks by folder path
  - Cross-platform support (macOS, Windows, Linux)

### Improvements
- Multi-profile support for Chrome bookmarks
- Enhanced folder structure preservation
- Robust error handling for browser integration

## [Unreleased]

### Planned Features
- Browser integration support
  - Safari bookmark listing and selective import
  - Edge bookmark listing and selective import
- Import bookmarks from browser bookmark files
- Batch processing for large bookmark collections
- Progress tracking for import operations
- Resume capability for interrupted imports

## [1.0.0] - 2025-05-28

### Added
- Initial release of LinkVault MCP Server
- CLI interface with JSON storage
- MCP server with SQLite storage
- Content extraction from web pages
- Intelligent categorization and tagging
- Main entry point supporting both CLI and MCP modes

### Features
- CLI Commands:
  - Add URLs with categories and tags
  - List categories and URLs
  - Search URLs by query
  - List and filter by tags
  - Delete URLs and categories
  - Rename categories

- MCP Tools:
  - get_url_data: Extract data from URLs
  - store_url: Store URLs with metadata
  - search_bookmarks: Search for bookmarks
  - list_categories: List all categories
  - list_bookmarks_by_category: List bookmarks in a category
  - delete_bookmark: Delete bookmarks by URL

### Improvements
- Enhanced URL content extraction with multiple fallbacks
- Support for notes in bookmarks
- Robust error handling for database operations
- Automatic schema migration for adding new fields

### Technical
- Python 3.10+ compatibility
- SQLite database for MCP server
- JSON file storage for CLI
- BeautifulSoup for web scraping
- FastMCP for MCP server implementation
