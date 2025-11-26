# Amazon Q CLI Setup

Complete guide for using Retromark with Amazon Q CLI.

## Overview

Amazon Q CLI is a terminal-based AI assistant from AWS. It integrates with Retromark for bookmark management in terminal workflows, especially useful for AWS-focused development.

**Use Case**: Terminal-based bookmark management, AWS documentation organization, CLI-driven workflows.

## Prerequisites

- Python 3.10+ installed
- Retromark installed (see main [README.md](../README.md#installation))
- Amazon Q CLI installed
- AWS account (for Amazon Q CLI)

## Installing Amazon Q CLI

Follow the [official Amazon Q CLI installation guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html).

Quick install:
```bash
# macOS/Linux
curl -sSL https://d2eo22ngex1n9g.cloudfront.net/releases/installer/install.sh | bash

# Verify installation
q --version
```

## Configuration

### 1. Locate Configuration File

Amazon Q MCP configuration: `~/.aws/amazonq/mcp.json`

If the file doesn't exist, create it:
```bash
mkdir -p ~/.aws/amazonq
touch ~/.aws/amazonq/mcp.json
```

### 2. Add Retromark Configuration

Edit `~/.aws/amazonq/mcp.json`:

```json
{
  "bookmark_manager": {
    "command": "uv",
    "args": [
      "--directory",
      "/absolute/path/to/retromark-mcp-server",
      "run",
      "src/server.py"
    ],
    "env": {},
    "disabled": false,
    "autoApprove": [
      "get_url_data",
      "store_url",
      "search_bookmarks",
      "list_categories",
      "list_bookmarks_by_category",
      "delete_bookmark",
      "list_chrome_bookmarks",
      "import_chrome_bookmark"
    ]
  }
}
```

**Important**: Replace `/absolute/path/to/retromark-mcp-server` with your actual path.

### 3. Alternative: Using Python Directly

```json
{
  "bookmark_manager": {
    "command": "python3",
    "args": [
      "/absolute/path/to/retromark-mcp-server/src/server.py"
    ],
    "env": {},
    "disabled": false,
    "autoApprove": [
      "get_url_data",
      "store_url",
      "search_bookmarks",
      "list_categories",
      "list_bookmarks_by_category",
      "delete_bookmark",
      "list_chrome_bookmarks",
      "import_chrome_bookmark"
    ]
  }
}
```

### 4. Restart Amazon Q CLI

If Amazon Q CLI is running, restart it:
```bash
# Exit any active Q sessions
# Restart
q chat
```

## Using Retromark with Amazon Q CLI

### Starting a Session

```bash
q chat
```

You'll see:
```
Welcome to Amazon Q CLI!
>
```

### Example Workflows

#### Saving AWS Documentation

```
> Save this Lambda documentation: https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html

Analyzing the page...

This appears to be AWS Lambda Function URLs documentation. Would you like me to save it?

Suggested details:
- Title: Lambda function URLs - AWS Lambda
- Category: AWS
- Tags: aws, lambda, function-urls, serverless
- Description: Documentation for creating HTTP(S) endpoints for Lambda functions
- Importance: 4

> Yes, save it

Bookmark saved successfully!
```

#### Searching AWS Bookmarks

```
> Show me my AWS serverless bookmarks

I found 8 serverless-related bookmarks:

1. Lambda function URLs
   URL: https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html
   Tags: aws, lambda, function-urls, serverless

2. API Gateway Integration
   URL: https://docs.aws.amazon.com/apigateway/
   Tags: aws, api-gateway, serverless, rest-api

...

Would you like details on any specific bookmark?
```

#### Organizing Cloud Resources

```
> List my bookmark categories

You have 5 categories:

1. AWS (23 bookmarks)
2. Azure (8 bookmarks)
3. Programming (45 bookmarks)
4. DevOps (19 bookmarks)
5. Documentation (31 bookmarks)

> Show me the AWS category

Displaying AWS bookmarks:

[Lists all 23 AWS bookmarks with titles, URLs, and tags]
```

### Auto-Approve Feature

The `autoApprove` list in configuration means Amazon Q won't ask for permission before using these tools. This makes interactions faster:

**Without autoApprove**:
```
> Save this URL

Amazon Q: I need permission to use the store_url tool. Allow? (y/n)
```

**With autoApprove**:
```
> Save this URL

Amazon Q: [Directly saves the URL]
Bookmark saved!
```

## Terminal-Specific Features

### Quick Commands

Amazon Q CLI supports concise commands:

```bash
# Quick save
> bookmark https://example.com

# Quick search
> find bookmarks about kubernetes

# List all
> show categories
```

### Piping Output

Use Amazon Q with standard Unix pipes:

```bash
# Save URLs from a file
cat urls.txt | while read url; do
  echo "Save $url" | q chat --once
done
```

### Scripting Integration

```bash
#!/bin/bash
# Save multiple AWS docs

urls=(
  "https://docs.aws.amazon.com/lambda/"
  "https://docs.aws.amazon.com/dynamodb/"
  "https://docs.aws.amazon.com/s3/"
)

for url in "${urls[@]}"; do
  echo "Save $url in AWS category" | q chat --once
done
```

## AWS-Specific Workflows

### Documentation Organization

```
> I'm starting a new AWS project. Save these service docs:
- Lambda: https://docs.aws.amazon.com/lambda/
- DynamoDB: https://docs.aws.amazon.com/dynamodb/
- S3: https://docs.aws.amazon.com/s3/

All in "Project-Alpha" category with tag "aws-foundation"
```

### Learning Path Tracking

```
> I'm learning AWS SAA certification. Tag my AWS bookmarks with "saa-study"

[Amazon Q updates relevant bookmarks with the saa-study tag]
```

### Team Knowledge Base

```
> Export all bookmarks in the "AWS-Best-Practices" category

[Provides list that can be shared with team]
```

## Configuration Options

### Environment Variables

Set custom environment for Retromark:

```json
{
  "bookmark_manager": {
    "command": "uv",
    "args": ["..."],
    "env": {
      "RETROMARK_DB": "/custom/path/bookmarks.db"
    },
    "disabled": false,
    "autoApprove": [...]
  }
}
```

### Disabling the Server

To temporarily disable Retromark:

```json
{
  "bookmark_manager": {
    "...": "...",
    "disabled": true
  }
}
```

### Selective Auto-Approve

Only auto-approve safe read operations:

```json
{
  "bookmark_manager": {
    "...": "...",
    "autoApprove": [
      "get_url_data",
      "search_bookmarks",
      "list_categories",
      "list_bookmarks_by_category",
      "list_chrome_bookmarks"
    ]
  }
}
```

This requires manual approval for write operations (`store_url`, `delete_bookmark`).

## Troubleshooting

### Server Not Starting

**Symptom**: "MCP server bookmark_manager not available"

**Solutions**:
1. Check configuration file location: `~/.aws/amazonq/mcp.json`
2. Verify JSON syntax (use `jq . ~/.aws/amazonq/mcp.json`)
3. Check absolute path to Retromark
4. Verify Amazon Q CLI version supports MCP

### Permission Errors

**Symptom**: "Permission denied" when accessing server

**Solutions**:
1. Make `src/server.py` executable: `chmod +x src/server.py`
2. Check directory permissions
3. Verify Python/uv in PATH: `which uv` or `which python3`

### Tools Not Auto-Approving

**Symptom**: Q asks permission despite autoApprove

**Solutions**:
1. Check tool names in `autoApprove` match exactly
2. Restart Amazon Q CLI after config changes
3. Verify JSON syntax in config file

## Advanced Usage

### Multiple MCP Servers

You can configure multiple MCP servers:

```json
{
  "bookmark_manager": {
    "command": "uv",
    "args": ["--directory", "/path/to/retromark", "run", "src/server.py"],
    "disabled": false,
    "autoApprove": [...]
  },
  "other_server": {
    "command": "...",
    "args": ["..."],
    "disabled": false,
    "autoApprove": [...]
  }
}
```

### Session Persistence

Amazon Q CLI sessions can be long-running. Retromark maintains state between tool calls within a session.

### Logging

Enable verbose logging for debugging:

```bash
q chat --debug
```

Check logs at: `~/.aws/amazonq/logs/`

## Comparison with Other Clients

| Feature | Amazon Q CLI | Claude Desktop | Continue.dev |
|---------|-------------|----------------|--------------|
| **Context** | Terminal | Desktop chat | IDE |
| **Best For** | AWS workflows | General use | Coding |
| **Auto-approve** | Yes | No | No |
| **Scripting** | Easy | Limited | No |

## Next Steps

- See [Client Comparison](client-comparison.md) for detailed comparison
- Check [Troubleshooting](troubleshooting.md) for common issues
- Return to [README](../README.md) for general documentation
