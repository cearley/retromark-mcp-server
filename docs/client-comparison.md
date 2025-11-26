# MCP Client Comparison

Guide to choosing the right MCP client for your Retromark workflow.

## Quick Decision Guide

**Choose Claude Desktop if you want:**
- General-purpose AI chat with bookmark management
- Desktop application with GUI
- Natural language interactions
- Research and content curation

**Choose Continue.dev if you want:**
- Bookmark management while coding
- IDE-integrated workflow
- Save documentation links without context switching
- Full MCP feature support

**Choose Amazon Q CLI if you want:**
- Terminal-based workflows
- AWS-focused documentation management
- Scriptable bookmark operations
- Auto-approved tool usage

## Detailed Comparison

### Feature Matrix

| Feature | Claude Desktop | Claude Code | Continue.dev | Amazon Q CLI |
|---------|----------------|-------------|--------------|--------------|
| **Platform** | Desktop app | CLI | IDE extension | CLI |
| **Interface** | GUI chat | Terminal | IDE sidebar | Terminal |
| **MCP Support** | Full | Full | Full (R/P/T/S) | Partial |
| **Auto-Approve** | No | No | No | Yes |
| **Scripting** | No | Limited | No | Yes |
| **Code Context** | No | No | Yes | No |
| **Best Platform** | macOS/Win/Linux | macOS/Linux | VS Code/JetBrains | macOS/Linux |

**MCP Features**:
- R = Resources
- P = Prompts
- T = Tools
- S = Sampling

### Use Case Comparison

#### Research & Learning

| Client | Rating | Notes |
|--------|--------|-------|
| Claude Desktop | ⭐⭐⭐⭐⭐ | Best for general research, natural conversations |
| Continue.dev | ⭐⭐⭐ | Good if research is code-related |
| Amazon Q CLI | ⭐⭐⭐ | Good for AWS/cloud research |

**Recommended**: Claude Desktop

#### Coding Workflows

| Client | Rating | Notes |
|--------|--------|-------|
| Claude Desktop | ⭐⭐⭐ | Can save links but requires context switching |
| Continue.dev | ⭐⭐⭐⭐⭐ | Best - integrated into IDE, sees code context |
| Amazon Q CLI | ⭐⭐ | Terminal-only, no IDE integration |

**Recommended**: Continue.dev

#### Terminal/Scripting

| Client | Rating | Notes |
|--------|--------|-------|
| Claude Desktop | ⭐ | GUI only, no CLI |
| Continue.dev | ⭐ | IDE-focused, not for scripting |
| Amazon Q CLI | ⭐⭐⭐⭐⭐ | Best - designed for terminal, scriptable |

**Recommended**: Amazon Q CLI

#### AWS Development

| Client | Rating | Notes |
|--------|--------|-------|
| Claude Desktop | ⭐⭐⭐ | General purpose, works well |
| Continue.dev | ⭐⭐⭐⭐ | Great for AWS SDK/CDK development |
| Amazon Q CLI | ⭐⭐⭐⭐⭐ | Best - AWS-native, optimized for AWS docs |

**Recommended**: Amazon Q CLI or Continue.dev

### Workflow Scenarios

#### Scenario 1: Daily Programming

**Context**: You're a developer working on various projects throughout the day.

**Best Choice**: **Continue.dev**

**Why**:
- Access bookmarks without leaving IDE
- Save documentation as you encounter it
- Code-aware bookmark suggestions
- Quick @ menu access

**Example Day**:
```
9:00 AM  - Working on React component
         - Find useful React Hooks guide
         - @MCP save with React tags

11:00 AM - Debugging API issue
         - @MCP search my API bookmarks
         - Find relevant Stack Overflow answer

2:00 PM  - Code review
         - Team member shares useful link
         - @MCP save for team knowledge base
```

#### Scenario 2: Learning New Technology

**Context**: You're learning AWS serverless architecture over several weeks.

**Best Choice**: **Claude Desktop**

**Why**:
- Natural conversational learning
- Can discuss and analyze articles
- Organized categorization
- Visual desktop interface

**Example Session**:
```
You: I'm learning AWS Lambda. Save this tutorial: https://...

Claude: I've analyzed it. This is a beginner Lambda tutorial covering:
- Function basics
- Event sources
- Best practices

Should I categorize as "AWS-Learning" with tags: lambda, serverless, tutorial?

You: Yes, and add importance 5

Claude: Saved! I notice you have 12 other AWS learning bookmarks.
Would you like me to show related resources?
```

#### Scenario 3: DevOps Automation

**Context**: You need to script bookmark management for team documentation.

**Best Choice**: **Amazon Q CLI**

**Why**:
- Terminal-native
- Scriptable with bash/Python
- Auto-approve for automation
- Pipe-friendly output

**Example Script**:
```bash
#!/bin/bash
# Import team wiki links

while IFS= read -r url; do
  echo "Save $url in team-docs category" | q chat --once
done < wiki-links.txt
```

#### Scenario 4: Content Curation

**Context**: You curate technology articles for a newsletter.

**Best Choice**: **Claude Desktop**

**Why**:
- Conversational workflow
- Can discuss article quality
- Natural categorization
- Desktop GUI for review

**Example Workflow**:
```
You: I found these 5 articles about AI. Can you analyze them and
save the best ones with appropriate tags?

[Provides URLs]

Claude: I've analyzed all 5. Here's my assessment:
1. Excellent technical depth - SAVE
2. Too basic for your audience - SKIP
3. Great practical examples - SAVE
...

Saved 3 articles in "AI-Content" with quality ratings.
```

### Configuration Complexity

| Client | Setup Difficulty | Configuration File | Format |
|--------|-----------------|-------------------|--------|
| Claude Desktop | Easy | claude_desktop_config.json | JSON |
| Continue.dev | Easy | config.json or mcpServers/ | JSON/YAML |
| Amazon Q CLI | Medium | mcp.json | JSON |

### Platform Support

| Client | macOS | Windows | Linux |
|--------|-------|---------|-------|
| Claude Desktop | ✅ | ✅ | ✅ |
| Claude Code | ✅ | ❌ | ✅ |
| Continue.dev | ✅ | ✅ | ✅ |
| Amazon Q CLI | ✅ | ⚠️ | ✅ |

✅ = Fully supported
⚠️ = Limited/experimental support
❌ = Not supported

### Performance Considerations

| Client | Startup Time | Response Time | Resource Usage |
|--------|-------------|---------------|----------------|
| Claude Desktop | Fast | Fast | Medium |
| Continue.dev | Fast | Fast | Low (IDE plugin) |
| Amazon Q CLI | Medium | Fast | Low |

## Multi-Client Strategy

### Using Multiple Clients Together

You can (and should) use multiple clients for different contexts:

**Example Multi-Client Setup**:
1. **Continue.dev**: Primary for coding (VS Code)
2. **Claude Desktop**: Research and article curation
3. **Amazon Q CLI**: Automation scripts

**Benefit**: Same bookmark database, accessed through the best interface for each task.

**Configuration**:
- All three clients point to the same Retromark instance
- All share the same SQLite database
- Bookmarks saved in one client appear in all others

### Recommended Combinations

#### For Developers
```
Primary: Continue.dev (IDE)
Secondary: Claude Desktop (research)
Scripts: Amazon Q CLI (automation)
```

#### For Researchers/Writers
```
Primary: Claude Desktop (main work)
Secondary: Continue.dev (technical docs)
```

#### For DevOps Engineers
```
Primary: Amazon Q CLI (terminal workflows)
Secondary: Continue.dev (code/config editing)
```

## Migration Between Clients

### Switching from Amazon Q to Claude Desktop

**Why**: You want a GUI and better conversational AI

**Steps**:
1. Install Claude Desktop
2. Add Retromark to Claude config
3. Both clients use same database
4. No migration needed!

### Adding Continue.dev to Existing Setup

**Why**: You want IDE integration

**Steps**:
1. Install Continue.dev extension
2. Add Retromark to Continue config
3. Access existing bookmarks via @ menu
4. Save new bookmarks from IDE

### Database is Shared

**Important**: The SQLite database is shared across all clients. Changes made in one client immediately appear in others (after refresh).

## Decision Flow Chart

```
Do you primarily work in an IDE?
├─ Yes → Continue.dev
└─ No
   │
   Do you need terminal/scripting?
   ├─ Yes → Amazon Q CLI
   └─ No → Claude Desktop
```

## Summary

| Your Primary Activity | Recommended Client | Why |
|----------------------|-------------------|-----|
| Software Development | Continue.dev | IDE integration |
| Research & Learning | Claude Desktop | Natural conversations |
| DevOps & Automation | Amazon Q CLI | Terminal & scripts |
| AWS Development | Amazon Q CLI | AWS-optimized |
| Content Curation | Claude Desktop | Analysis & discussion |
| Team Documentation | Amazon Q CLI | Scriptable imports |

## Next Steps

- Read detailed setup for your chosen client
- Consider multi-client setup for different contexts
- See [Troubleshooting](troubleshooting.md) if issues arise
- Return to [README](../README.md) for general documentation
