# Design: Universal MCP Client Support

## Context

Retromark is currently documented and positioned as an "Amazon Q CLI extension," but the underlying FastMCP framework already supports the Model Context Protocol specification, which is inherently client-agnostic. The MCP specification defines a standard way for AI assistants (clients) to communicate with tools and data sources (servers), regardless of which AI assistant is being used.

**Current State:**
- Code is already client-agnostic (FastMCP handles all MCP clients)
- Documentation assumes Amazon Q CLI exclusively
- Configuration examples only show Amazon Q setup
- Project description and README focus on Amazon Q
- User-facing messaging mentions Amazon Q CLI specifically

**Stakeholders:**
- Existing Amazon Q CLI users (must not break their workflows)
- Potential Claude Desktop/Code users (primary new audience)
- Potential Continue.dev users (IDE/developer audience)
- Future MCP client users (general benefit)

## Goals / Non-Goals

### Goals
- Position Retromark as a universal MCP server that works with any MCP client
- Provide clear, tested configuration examples for Claude Desktop, Claude Code, and Continue.dev
- Make Claude the primary example in documentation (larger user base, better MCP integration)
- Add Continue.dev as second example (first full MCP implementation, popular among developers)
- Maintain Amazon Q CLI as a fully-supported third example
- Update all documentation to be client-agnostic in language
- Improve discoverability across different user segments (AI chat users, developers, CLI users)
- Demonstrate three distinct use cases: Desktop AI, IDE Integration, Terminal/CLI

### Non-Goals
- Not changing any server implementation code (already client-agnostic via FastMCP)
- Not deprecating Amazon Q CLI support (remains fully supported)
- Not adding client-specific features or workarounds
- Not creating separate versions or forks for different clients
- Not requiring users to choose a single client (can use multiple)

## Decisions

### Decision 1: Claude as Primary Example
**Choice:** Feature Claude Desktop/Code as the primary configuration example, with Amazon Q CLI as secondary.

**Rationale:**
- Claude has broader adoption and better MCP integration than Amazon Q CLI
- Claude Desktop has built-in MCP server management UI
- Claude Code (CLI tool) is gaining significant traction
- Most MCP servers in the ecosystem showcase Claude examples first
- Amazon Q CLI has limited MCP adoption compared to Claude

**Alternatives Considered:**
- Keep Amazon Q CLI as primary (rejected: limits audience, doesn't reflect MCP ecosystem reality)
- Show both equally without priority (rejected: confusing for new users, dilutes messaging)
- Generic examples without specific clients (rejected: users need concrete configuration examples)

### Decision 2: Triple Configuration Approach
**Choice:** Provide complete, copy-paste-ready configuration for Claude, Continue.dev, and Amazon Q CLI.

**Rationale:**
- Users need working examples, not abstract instructions
- Different clients have different configuration formats (JSON files, different paths)
- Testing all three ensures they actually work
- Three diverse examples help users understand MCP configuration patterns
- Each example represents a different use case/workflow

**Configuration Locations:**
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- **Claude Code**: `~/.config/claude/config.json`
- **Continue.dev**: `~/.continue/config.json` or `~/.continue/mcpServers/`
- **Amazon Q CLI**: `~/.aws/amazonq/mcp.json`

**Use Case Mapping:**
- **Claude Desktop/Code**: General-purpose AI chat and assistance
- **Continue.dev**: IDE-integrated coding assistance (VS Code/JetBrains)
- **Amazon Q CLI**: Terminal-based workflows and AWS-focused tasks

### Decision 3: Client-Agnostic Language Throughout
**Choice:** Remove all Amazon Q CLI-specific assumptions from documentation and code comments.

**Examples:**
- ❌ "Amazon Q CLI integration"
- ✅ "MCP client integration"
- ❌ "Amazon Q CLI can invoke tools"
- ✅ "MCP clients can invoke tools"
- ❌ "Extends Amazon Q CLI with bookmark management"
- ✅ "Provides bookmark management to AI assistants via MCP"

**Rationale:**
- Makes documentation applicable to all current and future MCP clients
- Follows MCP best practices and specification language
- Reduces maintenance burden (one set of docs for all clients)

### Decision 4: Architecture Diagram Updates
**Choice:** Update Mermaid diagrams to show "MCP Client" instead of "Amazon Q CLI" with examples.

**New Diagram Pattern:**
```
User → MCP Client (Claude/Continue.dev/Amazon Q/etc.) → Retromark MCP Server → Resources
```

**Rationale:**
- Visual clarity that any MCP client works
- Helps users understand the abstraction layer
- Educational value for users learning MCP

### Decision 5: Preserve Amazon Q Examples
**Choice:** Keep Amazon Q CLI examples and configuration, just reposition as third example.

**Rationale:**
- Existing users depend on these examples
- Amazon Q CLI is still a valid use case (terminal/AWS-focused)
- Demonstrates multi-client support
- Honors the project's origin (forked from Amazon Q-focused project)

### Decision 6: Add Continue.dev as IDE Use Case
**Choice:** Feature Continue.dev as the second example, positioned as "MCP in Your IDE."

**Rationale:**
- Continue.dev is the first client with full MCP support (Resources, Prompts, Tools, Sampling)
- Large developer user base (popular VS Code and JetBrains extension)
- Different use case from Claude (IDE integration vs desktop chat)
- Brings bookmark management into coding environments where developers need it
- Supports both JSON and YAML config formats for flexibility
- Active development and strong MCP commitment

**Alternatives Considered:**
- Cursor (rejected: similar to Continue but less mature MCP support)
- Zed (rejected: smaller user base, still growing)
- Codeium/Windsurf (rejected: less mature MCP integration than Continue)

## Risks / Trade-offs

### Risk: Confusion for Existing Users
**Mitigation:**
- Add clear migration note: "Existing Amazon Q CLI users: your configuration still works!"
- Keep Amazon Q examples visible and complete
- Update CHANGELOG with clear explanation of changes

### Risk: Testing Burden Across Clients
**Mitigation:**
- Document primary test client (Claude Desktop) in CLAUDE.md
- Note that FastMCP handles client compatibility automatically
- Provide troubleshooting section for common client-specific issues

### Trade-off: Documentation Complexity
**Trade-off:** More examples = more documentation to maintain
**Acceptance:** Worth it for accessibility and user choice

### Trade-off: Repositioning Away from Amazon Q
**Trade-off:** May reduce visibility among Amazon Q CLI users
**Acceptance:** Claude's larger ecosystem provides net positive reach

## Migration Plan

### Phase 1: Documentation Updates (This Change)
1. Update README.md with new structure:
   - Universal MCP server positioning
   - Claude Desktop/Code configuration first
   - Amazon Q CLI configuration second
   - Client comparison table
2. Update CLAUDE.md with Retromark-specific usage guide
3. Update openspec/project.md to reflect multi-client support
4. Update src/server.py docstrings to be client-agnostic
5. Update architecture diagrams

### Phase 2: Testing & Validation
1. Test Claude Desktop configuration on macOS
2. Test Claude Code configuration
3. Verify Amazon Q CLI configuration still works
4. Update examples with actual tested output

### Phase 3: Community Outreach
1. Update GitHub description and tags
2. Submit to Claude MCP server directory (if one exists)
3. Update blog post/announcement with new positioning

### Rollback Plan
If issues arise:
1. Git revert to previous documentation version
2. All code remains unchanged (no rollback needed)
3. Configuration examples are additive (no breaking changes)

## Open Questions

1. **Q:** Should we create client-specific troubleshooting guides?
   **A:** Start with one general troubleshooting section. Add client-specific sections only if patterns emerge.

2. **Q:** Should we test other MCP clients (Zed, Continue, etc.)?
   **A:** Document Claude and Amazon Q as tested. Note that other MCP clients should work per spec.

3. **Q:** Should the project be renamed to remove "mcp-server" suffix?
   **A:** No. The suffix clarifies that this is an MCP server, not a standalone app. Common pattern in MCP ecosystem.

4. **Q:** Should we add a "getting started" wizard for client selection?
   **A:** Out of scope for this change. Could be future enhancement.
