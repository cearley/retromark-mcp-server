# Continue.dev Setup

Complete guide for using Retromark with Continue.dev in VS Code or JetBrains IDEs.

## Overview

Continue.dev is an AI coding assistant that integrates directly into your IDE. It's the first MCP client to support all MCP features (Resources, Prompts, Tools, and Sampling), making it perfect for bookmark management while coding.

**Use Case**: Access documentation links, save useful resources, and search bookmarks without leaving your coding environment.

## Prerequisites

- Python 3.10+ installed
- Retromark installed (see main [README.md](../README.md#installation))
- VS Code or JetBrains IDE
- Continue.dev extension installed

## Installing Continue.dev

### VS Code

1. Open VS Code
2. Go to Extensions (Cmd+Shift+X / Ctrl+Shift+X)
3. Search for "Continue"
4. Install the Continue extension
5. Reload VS Code

### JetBrains IDEs

1. Open your JetBrains IDE (IntelliJ, PyCharm, WebStorm, etc.)
2. Go to Settings → Plugins
3. Search for "Continue"
4. Install and restart IDE

## Configuration

Continue.dev supports two configuration methods:

### Method 1: Single config.json File

**Location**: `~/.continue/config.json`

Add Retromark to your configuration:

```json
{
  "models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "apiKey": "your-api-key"
    }
  ],
  "mcpServers": {
    "retromark": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/retromark-mcp-server",
        "run",
        "src/server.py"
      ]
    }
  }
}
```

### Method 2: Separate MCP Servers Directory (Recommended)

**Location**: `~/.continue/mcpServers/`

Create a dedicated file for Retromark:

**JSON Format** (`~/.continue/mcpServers/retromark.json`):
```json
{
  "command": "uv",
  "args": [
    "--directory",
    "/absolute/path/to/retromark-mcp-server",
    "run",
    "src/server.py"
  ]
}
```

**YAML Format** (`~/.continue/mcpServers/retromark.yaml`):
```yaml
command: uv
args:
  - --directory
  - /absolute/path/to/retromark-mcp-server
  - run
  - src/server.py
```

**Note**: Continue.dev automatically picks up all files in `mcpServers/` directory.

### Alternative: Using Python Directly

If you don't have `uv`:

```json
{
  "command": "python3",
  "args": [
    "/absolute/path/to/retromark-mcp-server/src/server.py"
  ]
}
```

## Using Retromark in Continue.dev

### Accessing MCP Tools

1. Open the Continue.dev sidebar in your IDE
2. Type `@` in the chat input
3. Select "MCP" from the dropdown
4. Choose Retromark tools or resources

### Example IDE Workflows

#### Saving Documentation While Coding

```
# You're working on a Python file and find useful docs

You: @MCP Save this Python asyncio guide: https://realpython.com/async-io-python/

Continue: I'll save that for you. Let me analyze the content...

[Analyzes page]

Continue: Saved!
- Title: Async IO in Python: A Complete Walkthrough
- Category: Python
- Tags: python, asyncio, concurrency, async-await
- Importance: 5
```

#### Quick Bookmark Search

```
# You need to find that article about Docker you saved

You: @MCP Search my bookmarks for Docker networking

Continue: Found 3 bookmarks:

1. Docker Network Deep Dive
   URL: https://example.com/docker-networking
   Tags: docker, networking, containers

2. Docker Compose Networking
   URL: https://example.com/compose-networks
   Tags: docker, docker-compose, networking
```

#### Importing from Chrome

```
You: @MCP Show my Chrome bookmarks about React

Continue: I found 12 React bookmarks in Chrome:

1. React Documentation
   Path: Dev/Frontend/React
   URL: https://react.dev

2. React Hooks Guide
   Path: Dev/Frontend/React/Hooks
   URL: https://react.dev/reference/react

Would you like me to import any?

You: Import the first 5

Continue: Imported 5 React bookmarks into your "Frontend" category.
```

## IDE-Specific Features

### VS Code Integration

- **Quick Access**: Press Ctrl+L / Cmd+L to open Continue sidebar
- **Inline Chat**: Select code → Right-click → "Continue: Ask about this code"
- **Context Sharing**: Continue can see your current file and selection

### JetBrains Integration

- **Tool Window**: View → Tool Windows → Continue
- **Context Menu**: Right-click code → Continue
- **AI Actions**: Alt+J / Cmd+J for quick actions

## Keyboard Shortcuts

| Action | VS Code | JetBrains |
|--------|---------|-----------|
| Open Continue | Ctrl+L / Cmd+L | - |
| Quick Action | Ctrl+I / Cmd+I | Alt+J / Cmd+J |
| New Chat | Ctrl+Shift+L | - |

## Best Practices for IDE Usage

### 1. Context-Aware Bookmarking

Save links related to your current work:
```
# While editing api.py

You: @MCP I found this helpful FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
Can you save it with tags relevant to what I'm working on?

Continue: [Analyzes both the URL and your current code context]
Saved with tags: fastapi, python, api, rest, web-framework
```

### 2. Code Comments to Bookmarks

```
# You have a TODO comment with a useful link

You: @MCP Save the link in my TODO comment on line 45

Continue: [Reads line 45]
Found: # TODO: Implement retry logic - see https://example.com/retry-patterns
Saving this bookmark...
```

### 3. Project-Specific Collections

Organize bookmarks by project:
```
You: @MCP Save these 3 docs links in my "ProjectX" category:
- https://docs.example.com/auth
- https://docs.example.com/database
- https://docs.example.com/deployment

Continue: Analyzed and saved all 3 in "ProjectX" category with appropriate tags.
```

## Workflow Examples

### Research While Coding

1. You're implementing a feature
2. Find a helpful Stack Overflow answer
3. Use `@MCP` to save it with context
4. Continue extracts relevant tags from your code
5. Bookmark is categorized automatically

### Documentation Sprint

1. You're learning a new framework
2. Open Continue sidebar
3. As you find useful docs, save them with `@MCP`
4. Later: `@MCP list all my [framework] bookmarks`
5. Get organized overview of what you've saved

### Team Knowledge Sharing

1. Team member shares a link
2. Save it with `@MCP` and add team-relevant tags
3. Export/share bookmark database
4. Team has curated list of useful resources

## Troubleshooting

### MCP Tools Not Appearing

**Symptom**: `@MCP` doesn't show Retromark tools

**Solutions**:
1. Check config file location is correct
2. Verify JSON/YAML syntax (use a validator)
3. Restart IDE completely
4. Check Continue.dev logs: View → Output → Continue

### Server Connection Issues

**Symptom**: "MCP server not responding"

**Solutions**:
1. Verify absolute path to Retromark
2. Test manually: `uv --directory /path/to/retromark run src/server.py`
3. Check Python/uv is in PATH
4. Look for errors in Continue logs

### Performance Issues

**Symptom**: IDE feels slow when using MCP tools

**Solutions**:
1. Close unused MCP servers in config
2. Restart IDE to clear MCP cache
3. Check Retromark database size (large databases may be slow)

## Advanced Configuration

### Multiple Models with MCP

```json
{
  "models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022"
    },
    {
      "title": "GPT-4",
      "provider": "openai",
      "model": "gpt-4"
    }
  ],
  "mcpServers": {
    "retromark": { ... }
  }
}
```

All models can access Retromark tools.

### Environment Variables

Set custom environment for Retromark:

```json
{
  "mcpServers": {
    "retromark": {
      "command": "uv",
      "args": ["--directory", "/path/to/retromark", "run", "src/server.py"],
      "env": {
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

## Comparison with Other Clients

| Feature | Continue.dev | Claude Desktop | Amazon Q CLI |
|---------|-------------|----------------|--------------|
| **Context** | Current code | General chat | Terminal |
| **Access** | @ menu | Natural language | Command prompt |
| **Best For** | While coding | Research | Scripts |
| **MCP Support** | Full (R/P/T/S) | Full | Partial |

## Next Steps

- See [Client Comparison](client-comparison.md) for detailed feature comparison
- Check [Troubleshooting](troubleshooting.md) for common issues
- Return to [README](../README.md) for general documentation
