# Bookmark Management

## Purpose
Core bookmark storage, retrieval, categorization, and search functionality for the MCP server mode.

## Requirements

### Requirement: Store Bookmark with Metadata
The system SHALL store bookmarks with comprehensive metadata in the SQLite database.

#### Scenario: Store new bookmark
- **WHEN** `store_url()` is called with url, title, category, tags, description, importance, and optional notes
- **THEN** the bookmark is inserted into the bookmarks table
- **AND** the URL is normalized by adding `https://` if no protocol is specified
- **AND** the category count is incremented in the categories table
- **AND** tag counts are incremented in the tags table for each tag
- **AND** timestamps are set using `datetime.now().isoformat()`

#### Scenario: Store duplicate URL
- **WHEN** `store_url()` is called with a URL that already exists
- **THEN** the existing bookmark is updated with new metadata
- **AND** category and tag counts are adjusted accordingly

### Requirement: Search Bookmarks
The system SHALL provide full-text search across all bookmark fields.

#### Scenario: Search by query term
- **WHEN** `search_bookmarks()` is called with a query string
- **THEN** results include bookmarks where the query matches url, title, description, category, tags, or notes
- **AND** search is case-insensitive using LIKE with wildcards
- **AND** results include all bookmark fields (id, url, title, category, tags, description, importance, notes, timestamps)

#### Scenario: Empty search results
- **WHEN** `search_bookmarks()` is called with a query that matches no bookmarks
- **THEN** an empty list is returned
- **AND** the response indicates success with `{"success": True, "bookmarks": []}`

### Requirement: List Categories
The system SHALL maintain and list all bookmark categories with counts.

#### Scenario: Retrieve all categories
- **WHEN** `list_categories()` is called
- **THEN** all categories are returned with their bookmark counts
- **AND** results are sorted alphabetically by category name
- **AND** the categories table is kept in sync with the bookmarks table

### Requirement: List Bookmarks by Category
The system SHALL retrieve all bookmarks in a specific category.

#### Scenario: Get bookmarks in category
- **WHEN** `list_bookmarks_by_category()` is called with a category name
- **THEN** all bookmarks with that category are returned
- **AND** results include all bookmark fields
- **AND** results are ordered by creation date (newest first)

#### Scenario: Non-existent category
- **WHEN** `list_bookmarks_by_category()` is called with a category that doesn't exist
- **THEN** an empty list is returned
- **AND** the response indicates success

### Requirement: Delete Bookmark
The system SHALL remove bookmarks and update related counts.

#### Scenario: Delete by URL
- **WHEN** `delete_bookmark()` is called with a URL
- **THEN** the bookmark is removed from the database
- **AND** the category count is decremented
- **AND** tag counts are decremented for all associated tags
- **AND** empty categories and tags are removed from their respective tables

#### Scenario: Delete non-existent bookmark
- **WHEN** `delete_bookmark()` is called with a URL that doesn't exist
- **THEN** the operation returns success without error
- **AND** no counts are modified

### Requirement: Tag Management
The system SHALL store tags as JSON arrays and maintain tag counts.

#### Scenario: Store tags with bookmark
- **WHEN** a bookmark is stored with a list of tags
- **THEN** tags are serialized to JSON string format
- **AND** each tag's count is tracked in the tags table
- **AND** tags are unique per bookmark

#### Scenario: Parse tags on retrieval
- **WHEN** bookmarks are retrieved from the database
- **THEN** tag JSON strings are parsed back to lists using `json.loads()`
- **AND** empty or null tag fields are handled gracefully

### Requirement: Importance Rating
The system SHALL support importance ratings from 1 to 5.

#### Scenario: Store importance
- **WHEN** a bookmark is stored with an importance value
- **THEN** the importance is stored as an integer (1-5)
- **AND** importance can be used for filtering or sorting

### Requirement: Notes Field
The system SHALL support optional notes on bookmarks.

#### Scenario: Add notes to bookmark
- **WHEN** `store_url()` is called with the notes parameter
- **THEN** the notes are stored in the notes column
- **AND** the notes column is created dynamically if it doesn't exist (migration pattern)

#### Scenario: Search includes notes
- **WHEN** `search_bookmarks()` is called
- **THEN** the query also searches within bookmark notes
- **AND** notes content is included in search results
