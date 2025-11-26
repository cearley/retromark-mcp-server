# Claude Desktop & Claude Code Setup

Complete guide for using Retromark with Claude Desktop and Claude Code.

## Overview

Claude provides two MCP-compatible interfaces:
- **Claude Desktop**: Desktop application with built-in MCP server management
- **Claude Code**: Command-line interface for terminal-based AI assistance

Both can use Retromark for intelligent bookmark management.

## Prerequisites

- Python 3.10+ installed
- Retromark installed (see main [README.md](../README.md#installation))
- Claude Desktop or Claude Code installed

## Claude Desktop Setup

### 1. Locate Configuration File

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Edit Configuration

Open the configuration file and add the Retromark server:

```json
{
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

**Important**: Replace `/absolute/path/to/retromark-mcp-server` with the actual absolute path to your Retromark installation.

### 3. Alternative: Using Python Directly

If you don't have `uv` installed, you can use Python directly:

```json
{
  "mcpServers": {
    "retromark": {
      "command": "python3",
      "args": [
        "/absolute/path/to/retromark-mcp-server/src/server.py"
      ]
    }
  }
}
```

### 4. Restart Claude Desktop

After saving the configuration:
1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The Retromark server will start automatically

### 5. Verify Installation

In Claude Desktop, try asking:
- "What bookmark management tools do you have?"
- "Can you save this URL: https://example.com"

Claude should recognize the Retromark tools and be able to use them.

## Claude Code Setup

### 1. Locate Configuration File

Claude Code configuration: `~/.config/claude/config.json`

### 2. Edit Configuration

Add Retromark to your Claude Code configuration:

```json
{
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

### 3. Test with Claude Code

```bash
claude chat
```

Then ask Claude to use bookmark management features:
```
> Save this article: https://docs.anthropic.com/en/docs/intro-to-claude
```

## Example Workflows

### Saving a Bookmark

```
You: Save this article about Python asyncio: https://docs.python.org/3/library/asyncio.html

Claude: I'll analyze that article and save it for you.

[Claude calls get_url_data to fetch content]
[Claude analyzes the content]

Claude: I've analyzed the article. It's about Python's asyncio library for concurrent programming.
Would you like me to save it with these details?
- Title: asyncio — Asynchronous I/O
- Category: Programming
- Tags: python, asyncio, concurrent-programming, async-await
- Importance: 4 (High)
- Description: Official Python documentation for the asyncio library, covering async/await syntax and concurrent task execution.

You: Yes, save it

Claude: Bookmark saved successfully!
```

### Searching Bookmarks

```
You: Show me all my Python-related bookmarks

Claude: [Searches bookmarks for "python"]

I found 12 Python-related bookmarks:

1. asyncio — Asynchronous I/O
   URL: https://docs.python.org/3/library/asyncio.html
   Category: Programming
   Tags: python, asyncio, concurrent-programming

2. Python Type Hints - mypy
   URL: https://mypy.readthedocs.io/
   Category: Programming
   Tags: python, typing, mypy

[... more results ...]
```

### Importing from Chrome

```
You: List my Chrome bookmarks about AWS

Claude: [Lists Chrome bookmarks]

I found 8 AWS-related bookmarks in your Chrome:

1. AWS Management Console
   Path: Work/AWS/Console
   URL: https://console.aws.amazon.com/

2. Amazon EC2 Documentation
   Path: Work/AWS/Documentation
   URL: https://docs.aws.amazon.com/ec2/

Would you like me to import any of these into Retromark?

You: Import the first two into my "AWS" category

Claude: I've imported both bookmarks into your AWS category with appropriate tags.
```

## Tips for Using Retromark with Claude

### Natural Language

Claude understands natural requests. You can say:
- "Save this URL"
- "Bookmark this article about X"
- "Find my bookmarks related to Y"
- "Show my programming bookmarks"
- "Import Chrome bookmarks from my work profile"

### Conversational Refinement

Claude can help refine bookmark metadata:
```
You: Save https://example.com

Claude: I've analyzed it. It's about web development.
Should I categorize it as "Web Development" or "Programming"?

You: Web Development, and add tags for HTML and CSS

Claude: Saved with category "Web Development" and tags: html, css, web-development
```

### Batch Operations

```
You: I have these three URLs I want to save:
- https://example1.com
- https://example2.com
- https://example3.com
Can you analyze and categorize them all?

Claude: I'll analyze each one and suggest appropriate categories and tags.
[Proceeds to analyze and suggest metadata for each]
```

## Troubleshooting

### Server Not Starting

**Symptom**: Claude says bookmark tools aren't available

**Solutions**:
1. Check configuration file path is correct
2. Verify absolute path to Retromark directory
3. Check Claude Desktop logs (Help → View Logs)
4. Ensure Python/uv is in system PATH

### Permission Errors

**Symptom**: "Permission denied" errors

**Solutions**:
1. Make sure `src/server.py` is executable: `chmod +x src/server.py`
2. Check file permissions in Retromark directory
3. On macOS: Grant Claude Desktop necessary permissions in System Settings

### Database Location Issues

**Symptom**: Bookmarks not persisting between sessions

**Solution**: Check that `~/Documents/github/retromark-mcp-server/data/` directory exists and is writable.

## Advanced Configuration

### Custom Database Location

Set a custom database path by modifying `src/server.py`:

```python
DB_PATH = os.path.expanduser("~/custom/path/bookmarks.db")
```

### Using with Multiple Claude Profiles

Each Claude profile has its own MCP configuration. You can:
- Use the same Retromark instance across profiles (shared bookmarks)
- Set up separate Retromark instances with different database paths

## Next Steps

- See [Client Comparison](client-comparison.md) to understand when to use Claude vs other clients
- Check [Troubleshooting](troubleshooting.md) for common issues
- Return to [README](../README.md) for general Retromark documentation
