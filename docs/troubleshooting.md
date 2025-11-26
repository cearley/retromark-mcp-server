# Troubleshooting Guide

Common issues and solutions for Retromark MCP server.

## Common Issues

### Server Won't Start

**Symptoms**:
- Client says MCP tools aren't available
- "Server not responding" errors
- Tools don't appear in client

**Solutions**:

1. **Check Configuration Path**
   ```bash
   # Verify config file exists
   cat ~/.config/claude/config.json  # Claude Code
   cat "~/Library/Application Support/Claude/claude_desktop_config.json"  # Claude Desktop
   cat ~/.continue/config.json  # Continue.dev
   cat ~/.aws/amazonq/mcp.json  # Amazon Q
   ```

2. **Verify Absolute Path**
   - Use `pwd` in Retromark directory to get absolute path
   - Ensure path in config matches exactly
   - No relative paths (no `~` or `./`)

3. **Test Server Manually**
   ```bash
   cd /path/to/retromark-mcp-server
   uv run src/server.py
   # Should start without errors
   ```

4. **Check Python/uv in PATH**
   ```bash
   which uv
   which python3
   ```

### Permission Denied Errors

**Symptoms**:
- "Permission denied" when server tries to start
- Can't create database file
- Can't read bookmarks

**Solutions**:

1. **Make Scripts Executable**
   ```bash
   chmod +x /path/to/retromark-mcp-server/src/server.py
   chmod +x /path/to/retromark-mcp-server/main.py
   ```

2. **Check Directory Permissions**
   ```bash
   ls -la ~/Documents/github/retromark-mcp-server/data/
   # Should be writable by your user
   ```

3. **Create Data Directory**
   ```bash
   mkdir -p ~/Documents/github/retromark-mcp-server/data
   ```

### Database Issues

**Symptoms**:
- Bookmarks not saving
- "Database locked" errors
- Data not persisting

**Solutions**:

1. **Check Database Location**
   ```bash
   ls -la ~/Documents/github/retromark-mcp-server/data/bookmarks.db
   ```

2. **Fix Database Permissions**
   ```bash
   chmod 644 ~/Documents/github/retromark-mcp-server/data/bookmarks.db
   ```

3. **Reinitialize Database**
   ```bash
   cd /path/to/retromark-mcp-server
   rm data/bookmarks.db  # Backup first!
   uv run src/server.py  # Will recreate database
   ```

### Configuration Syntax Errors

**Symptoms**:
- Client won't load configuration
- Server appears disabled
- No MCP servers listed

**Solutions**:

1. **Validate JSON Syntax**
   ```bash
   # macOS/Linux with jq
   jq . ~/.config/claude/config.json

   # Online validator
   # Copy/paste config to https://jsonlint.com
   ```

2. **Common JSON Mistakes**
   ```json
   // ❌ Wrong - trailing comma
   {
     "mcpServers": {
       "retromark": {...},
     }
   }

   // ✅ Correct - no trailing comma
   {
     "mcpServers": {
       "retromark": {...}
     }
   }
   ```

3. **Check Quotes**
   - Use double quotes (`"`) not single quotes (`'`)
   - Escape backslashes in Windows paths: `C:\\Users\\...`

## Client-Specific Issues

### Claude Desktop

**Issue**: MCP server not showing up

**Solutions**:
1. Completely quit Claude Desktop (not just close window)
2. Check config file location (macOS vs Windows vs Linux)
3. Review Claude Desktop logs: Help → View Logs

**Issue**: Tools work but slow

**Solution**: Check internet connection for Claude API calls

### Continue.dev

**Issue**: @ menu doesn't show Retromark

**Solutions**:
1. Reload VS Code/IDE window
2. Check Continue.dev output: View → Output → Continue
3. Verify config in correct location (`~/.continue/`)

**Issue**: MCP options greyed out

**Solution**: Ensure Continue.dev version supports MCP (check for updates)

### Amazon Q CLI

**Issue**: "MCP server not available"

**Solutions**:
1. Restart Amazon Q CLI completely
2. Check `~/.aws/amazonq/mcp.json` exists
3. Verify `autoApprove` list syntax

**Issue**: Tools require manual approval

**Solution**: Add tool names to `autoApprove` array in config

## Installation Issues

### uv Not Found

**Symptom**: `command not found: uv`

**Solutions**:

1. **Install uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Or use Python directly**
   ```json
   {
     "command": "python3",
     "args": ["/path/to/retromark-mcp-server/src/server.py"]
   }
   ```

3. **Add uv to PATH**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

### Dependencies Missing

**Symptom**: Import errors when starting server

**Solutions**:

1. **Install with uv** (recommended)
   ```bash
   cd /path/to/retromark-mcp-server
   uv sync
   ```

2. **Install with pip**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python version**
   ```bash
   python3 --version
   # Should be 3.10 or higher
   ```

## Performance Issues

### Slow Response Times

**Possible Causes & Solutions**:

1. **Large Database**
   - Check database size: `ls -lh ~/Documents/github/retromark-mcp-server/data/bookmarks.db`
   - Consider archiving old bookmarks

2. **Network Issues**
   - `get_url_data` fetches web content
   - Slow websites = slow responses
   - Check internet connection

3. **Multiple MCP Servers**
   - Disable unused MCP servers in client config
   - Each server uses resources

### High Memory Usage

**Solutions**:

1. Restart the MCP server (restart client)
2. Close unused client applications
3. Check for multiple Retromark instances running:
   ```bash
   ps aux | grep server.py
   ```

## Data Issues

### Bookmarks Not Syncing Between Clients

**Note**: This is expected behavior!

**Explanation**: All MCP clients share the same SQLite database. Changes should appear across clients.

**If not syncing**:
1. Verify all clients use same database path
2. Restart clients to refresh
3. Check file permissions on database

### Lost Bookmarks

**Recovery Steps**:

1. **Check Database File**
   ```bash
   sqlite3 ~/Documents/github/retromark-mcp-server/data/bookmarks.db "SELECT COUNT(*) FROM bookmarks;"
   ```

2. **Restore from Backup**
   - Check if you have database backups
   - Copy backup to `data/bookmarks.db`

3. **Check CLI Database** (separate!)
   ```bash
   cat ~/Documents/github/retromark-mcp-server/data/url_database.json
   ```

## Browser Integration Issues

### Chrome Bookmarks Not Found

**Symptoms**:
- `list_chrome_bookmarks` returns empty
- "No Chrome bookmarks found" error

**Solutions**:

1. **Verify Chrome is Installed**
   ```bash
   # macOS
   ls ~/Library/Application\ Support/Google/Chrome/

   # Linux
   ls ~/.config/google-chrome/
   ```

2. **Check Profile Paths**
   - Chrome stores bookmarks per profile
   - Check "Default" profile exists

3. **Permissions**
   - Ensure Retromark can read Chrome directories
   - On macOS: System Settings → Privacy & Security

## Getting Help

### Collecting Debug Information

Before asking for help, collect:

1. **Version Information**
   ```bash
   python3 --version
   uv --version
   cat /path/to/retromark-mcp-server/pyproject.toml | grep version
   ```

2. **Configuration** (redact sensitive info)
   ```bash
   cat ~/.config/claude/config.json  # Your client config
   ```

3. **Error Messages**
   - Full error text
   - Client logs
   - Terminal output

4. **Platform**
   - OS and version
   - Client and version

### Where to Get Help

1. **GitHub Issues**: [retromark-mcp-server/issues](https://github.com/cearley/retromark-mcp-server/issues)
2. **Docs**: Check all docs in `/docs` folder
3. **MCP Community**: General MCP questions

## Still Having Issues?

If these solutions don't help:

1. Create a GitHub issue with:
   - Problem description
   - Steps to reproduce
   - Error messages
   - Debug information (above)
   - What you've tried

2. Check for updates:
   ```bash
   cd /path/to/retromark-mcp-server
   git pull
   uv sync
   ```

3. Try fresh installation:
   ```bash
   # Backup your database first!
   cp data/bookmarks.db data/bookmarks.db.backup

   # Fresh install
   git clone https://github.com/cearley/retromark-mcp-server.git retromark-new
   cd retromark-new
   uv sync

   # Copy database back
   cp ../retromark-mcp-server/data/bookmarks.db data/
   ```

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Server won't start | Check absolute path in config |
| Permission denied | `chmod +x src/server.py` |
| Database locked | Restart client |
| JSON syntax error | Validate with `jq .` |
| Tools not appearing | Restart client completely |
| Slow performance | Check internet, database size |
| Chrome bookmarks empty | Check Chrome profile exists |

## Prevention

### Best Practices

1. **Use absolute paths** in all configs
2. **Backup database** regularly
3. **Keep uv/Python updated**
4. **Validate JSON** after editing configs
5. **Test manually** before client integration

### Regular Maintenance

```bash
# Monthly maintenance script
cd /path/to/retromark-mcp-server

# Update Retromark
git pull
uv sync

# Backup database
cp data/bookmarks.db data/bookmarks-$(date +%Y%m%d).db

# Clean old backups (keep last 5)
ls -t data/bookmarks-*.db | tail -n +6 | xargs rm

# Check database integrity
sqlite3 data/bookmarks.db "PRAGMA integrity_check;"
```

---

**Back to**: [README](../README.md) | [Client Comparison](client-comparison.md)
