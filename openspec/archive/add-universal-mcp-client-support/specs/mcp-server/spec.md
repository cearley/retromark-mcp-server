# MCP Server Deltas

## MODIFIED Requirements

### Requirement: FastMCP Server Implementation
The system SHALL implement an MCP server using the FastMCP framework that exposes bookmark management tools to any MCP client.

#### Scenario: Server initialization
- **WHEN** the server is started via `src/server.py`
- **THEN** the FastMCP application initializes successfully
- **AND** the SQLite database is created at `~/Documents/github/retromark-mcp-server/data/bookmarks.db`
- **AND** all 8 MCP tools are registered and available

#### Scenario: Claude Desktop integration
- **WHEN** Claude Desktop is configured with the Retromark MCP server in `claude_desktop_config.json`
- **THEN** Claude can invoke any of the 8 registered tools
- **AND** tool responses are returned in a consistent dictionary format with success indicators

#### Scenario: Claude Code integration
- **WHEN** Claude Code is configured with the Retromark MCP server in its config file
- **THEN** Claude Code can invoke any of the 8 registered tools
- **AND** tool responses are returned in a consistent dictionary format with success indicators

#### Scenario: Continue.dev integration
- **WHEN** Continue.dev (VS Code or JetBrains) is configured with the Retromark MCP server
- **THEN** Continue.dev can invoke any of the 8 registered tools via the @ menu
- **AND** tool responses are returned in a consistent dictionary format with success indicators
- **AND** Retromark resources are accessible through Continue's MCP interface

#### Scenario: Amazon Q CLI integration
- **WHEN** Amazon Q CLI is configured with the Retromark MCP server in `mcp.json`
- **THEN** Amazon Q CLI can invoke any of the 8 registered tools
- **AND** tool responses are returned in a consistent dictionary format with success indicators

#### Scenario: Client-agnostic operation
- **WHEN** any standards-compliant MCP client connects to the server
- **THEN** the server responds to MCP protocol messages correctly
- **AND** all tools are accessible regardless of the client implementation

## ADDED Requirements

### Requirement: Universal MCP Client Support
The system SHALL support any MCP client that adheres to the Model Context Protocol specification.

#### Scenario: Multiple simultaneous clients
- **WHEN** the server is configured in Claude Desktop, Continue.dev, and Amazon Q CLI
- **THEN** all clients can use the server simultaneously
- **AND** each client maintains its own independent session
- **AND** database access is coordinated correctly across all clients

#### Scenario: Client-agnostic documentation
- **WHEN** viewing the server's tool documentation and comments
- **THEN** no client-specific assumptions are present
- **AND** examples reference "MCP clients" generically
- **AND** specific client names are only used in configuration examples

### Requirement: Multi-Client Configuration Examples
The system SHALL provide tested configuration examples for multiple MCP clients.

#### Scenario: Claude Desktop configuration
- **WHEN** following the Claude Desktop setup instructions
- **THEN** the configuration file path is `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- **AND** the configuration includes the correct command, args, and env settings
- **AND** the server starts successfully when Claude Desktop launches it

#### Scenario: Claude Code configuration
- **WHEN** following the Claude Code setup instructions
- **THEN** the configuration file path is `~/.config/claude/config.json`
- **AND** the configuration includes the correct MCP server settings
- **AND** the server starts successfully when Claude Code launches it

#### Scenario: Continue.dev configuration
- **WHEN** following the Continue.dev setup instructions
- **THEN** the configuration can be placed in `~/.continue/config.json` or `~/.continue/mcpServers/`
- **AND** the configuration supports both JSON and YAML formats
- **AND** the configuration includes the correct command and args for uv or python
- **AND** the server starts successfully when Continue.dev launches it
- **AND** all MCP features (Resources, Prompts, Tools, Sampling) are available

#### Scenario: Amazon Q CLI configuration
- **WHEN** following the Amazon Q CLI setup instructions
- **THEN** the configuration file path is `~/.aws/amazonq/mcp.json`
- **AND** the configuration includes the correct command, args, and autoApprove settings
- **AND** the server starts successfully when Amazon Q CLI launches it
