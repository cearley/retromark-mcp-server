# Chrome Integration

## Purpose
Cross-platform Chrome bookmark reading and import functionality from all Chrome profiles.

## Requirements

### Requirement: Cross-Platform Bookmark Path Detection
The system SHALL detect Chrome bookmark file locations across macOS, Windows, and Linux.

#### Scenario: macOS bookmark detection
- **WHEN** `get_chrome_bookmarks_paths()` is called on macOS
- **THEN** bookmark files are located at `~/Library/Application Support/Google/Chrome/*/Bookmarks`
- **AND** all Chrome profiles are scanned using glob patterns

#### Scenario: Windows bookmark detection
- **WHEN** `get_chrome_bookmarks_paths()` is called on Windows
- **THEN** bookmark files are located at `%LOCALAPPDATA%/Google/Chrome/User Data/*/Bookmarks`
- **AND** all Chrome profiles are scanned

#### Scenario: Linux bookmark detection
- **WHEN** `get_chrome_bookmarks_paths()` is called on Linux
- **THEN** bookmark files are located at `~/.config/google-chrome/*/Bookmarks`
- **AND** all Chrome profiles are scanned

### Requirement: Multi-Profile Support
The system SHALL read bookmarks from all Chrome profiles simultaneously.

#### Scenario: Multiple profiles detected
- **WHEN** Chrome has multiple profiles (Default, Profile 1, Profile 2, etc.)
- **THEN** all profile bookmark files are discovered
- **AND** each profile's bookmarks are included in results
- **AND** profile names are preserved in bookmark paths

### Requirement: Chrome Bookmark Parsing
The system SHALL parse Chrome's JSON bookmark format.

#### Scenario: Parse bookmark file
- **WHEN** `parse_chrome_bookmarks()` is called with a Chrome Bookmarks file
- **THEN** the JSON file is read and parsed
- **AND** bookmark nodes are extracted from the nested structure
- **AND** both "bookmark_bar" and "other" root nodes are processed

#### Scenario: Invalid bookmark file
- **WHEN** a bookmark file is corrupted or invalid JSON
- **THEN** an error is returned with `{"success": False, "error": "..."}`
- **AND** the error message indicates the parsing failure

### Requirement: Recursive Folder Extraction
The system SHALL recursively extract bookmarks from nested Chrome folders.

#### Scenario: Extract nested bookmarks
- **WHEN** Chrome bookmarks are organized in nested folders
- **THEN** `extract_bookmarks_from_node()` recursively traverses all folder levels
- **AND** bookmarks at any depth are extracted
- **AND** folder hierarchy is preserved in the path field

#### Scenario: Folder path construction
- **WHEN** a bookmark is nested in folders like "Bookmarks Bar" > "Work" > "Documentation"
- **THEN** the path is constructed as "Default/Bookmarks Bar/Work/Documentation"
- **AND** the profile name is included as the first path component

### Requirement: List Chrome Bookmarks Tool
The system SHALL expose Chrome bookmarks through an MCP tool.

#### Scenario: List all Chrome bookmarks
- **WHEN** `list_chrome_bookmarks()` MCP tool is called
- **THEN** bookmarks from all Chrome profiles are returned
- **AND** each bookmark includes url, name, and path fields
- **AND** results are formatted for display to the user

#### Scenario: Flat vs hierarchical listing
- **WHEN** `get_chrome_bookmarks()` is called with `flat=True`
- **THEN** bookmarks are returned as a flat list
- **WHEN** called with `flat=False`
- **THEN** bookmarks maintain their hierarchical folder structure

### Requirement: Import Chrome Bookmark to Retromark
The system SHALL import individual Chrome bookmarks into Retromark's SQLite database.

#### Scenario: Import bookmark with metadata
- **WHEN** `import_chrome_bookmark()` is called with a Chrome bookmark URL
- **THEN** the bookmark is located in Chrome's bookmarks
- **AND** webpage content is fetched using `get_url_data()`
- **AND** the bookmark is stored in Retromark with extracted metadata
- **AND** the Chrome folder path is used as the category

#### Scenario: Import non-existent Chrome bookmark
- **WHEN** `import_chrome_bookmark()` is called with a URL not in Chrome bookmarks
- **THEN** an error is returned indicating the bookmark was not found
- **AND** no data is stored in Retromark

### Requirement: Optional Import Fallback
The system SHALL handle browser integration module unavailability gracefully.

#### Scenario: Browser integration unavailable
- **WHEN** the `utils.browser_integration` module cannot be imported
- **THEN** fallback functions are defined
- **AND** calls to Chrome integration functions return `{"success": False, "error": "Browser integration module not available"}`
- **AND** the rest of the application continues to function
