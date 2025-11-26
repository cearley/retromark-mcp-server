# Change: Add Universal MCP Client Support

## Why

Currently, Retromark is tightly coupled to Amazon Q CLI as its primary (and only documented) MCP client. The project documentation, configuration examples, and messaging all assume Amazon Q CLI usage. However, the Model Context Protocol is designed to be client-agnostic, and there are multiple MCP clients available including Claude Desktop, Claude Code, Continue.dev, and other tools.

This limitation prevents users of other AI assistants and development tools from leveraging Retromark's bookmark management capabilities. By making Retromark a truly universal MCP server, we can:

1. **Expand the user base** - Claude users, Continue.dev users (VS Code/JetBrains), and other AI assistant users can benefit from intelligent bookmark management
2. **Follow MCP best practices** - The MCP specification is client-agnostic by design
3. **Future-proof the project** - As more MCP clients emerge, Retromark will work with them without modification
4. **Improve documentation** - Clear examples for multiple clients help all users understand configuration
5. **Cover diverse use cases** - Desktop AI (Claude), IDE integration (Continue.dev), and CLI tools (Amazon Q) each serve different workflows

## What Changes

- Refactor documentation to position Retromark as a **universal MCP server** (client-agnostic)
- Update README.md to feature **Claude Desktop/Code as the primary example** with Continue.dev and Amazon Q as additional examples
- Add Claude Desktop/Code configuration instructions and examples
- Add Continue.dev configuration instructions (for VS Code/JetBrains IDEs)
- Update Amazon Q CLI to be positioned as third example (terminal/AWS-focused use case)
- Update all user-facing messaging to be client-agnostic (remove Amazon Q CLI assumptions)
- Add MCP client comparison guide showing three use cases: Desktop AI, IDE Integration, Terminal/CLI
- Update project description and tagline to emphasize universal MCP support
- Revise example interactions to show Claude, Continue.dev, and Amazon Q workflows
- Update architecture diagrams to be client-agnostic
- No code changes required (FastMCP already supports any MCP client)

**Note**: This is primarily a **documentation and positioning change**. The underlying FastMCP implementation already supports any MCP client. We're making the project's documentation and examples reflect this reality.

## Impact

### Affected Specs
- `mcp-server` - Update to clarify client-agnostic design
- Documentation files (README.md, CLAUDE.md, project.md)

### Affected Code
- **src/server.py** - Update docstrings and comments to be client-agnostic
- **README.md** - Major restructuring to feature Claude as primary example
- **CLAUDE.md** - Add Retromark-specific usage guidance for Claude
- **openspec/project.md** - Update external dependencies section
- **main.py** - Update comments and help text

### Breaking Changes
None - this is backwards compatible. Amazon Q CLI users will continue to work exactly as before.

### Benefits
- **Broader appeal** - Attracts Claude users, Continue.dev users (developers), and users of other MCP clients
- **Better alignment with MCP philosophy** - Embraces client-agnostic design
- **Improved discoverability** - Users searching for MCP servers across different platforms will find Retromark
- **Educational value** - Three diverse client examples help users understand MCP configuration patterns
- **Developer audience** - Continue.dev integration brings bookmark management directly into coding environments
- **Use case diversity** - Covers desktop AI chat (Claude), IDE integration (Continue.dev), and terminal workflows (Amazon Q)
- **Future-ready** - Supports upcoming MCP clients without changes

### Risks
- **Minimal risk** - This is primarily documentation changes
- **Existing users unaffected** - Amazon Q configuration remains valid
- **Testing burden is low** - Only need to verify configuration examples work
