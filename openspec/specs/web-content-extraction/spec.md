# Web Content Extraction

## Purpose
Sophisticated webpage content fetching and metadata extraction with multiple fallback strategies.

## Requirements

### Requirement: Fetch Webpage Content
The system SHALL fetch webpage content via HTTP requests with custom headers.

#### Scenario: Successful content fetch
- **WHEN** `get_url_data()` is called with a valid URL
- **THEN** an HTTP GET request is made with custom User-Agent headers
- **AND** the response HTML is retrieved
- **AND** the content is parsed with BeautifulSoup using the html.parser

#### Scenario: URL normalization before fetch
- **WHEN** a URL without a protocol is provided
- **THEN** `https://` is prepended to the URL
- **AND** the normalized URL is used for the request

#### Scenario: Request failure
- **WHEN** the HTTP request fails (network error, timeout, etc.)
- **THEN** an error is returned with `{"success": False, "error": "..."}`
- **AND** the error message describes the failure

### Requirement: Multi-Strategy Title Extraction
The system SHALL extract webpage titles using multiple fallback strategies.

#### Scenario: Extract from title tag
- **WHEN** the webpage has a `<title>` tag
- **THEN** the title is extracted from the tag's text content
- **AND** the title is stripped of whitespace

#### Scenario: Fallback to og:title meta tag
- **WHEN** no title tag exists or it's empty
- **THEN** the Open Graph `og:title` meta tag is checked
- **AND** its content attribute is used as the title

#### Scenario: Fallback to h1 tag
- **WHEN** no title or og:title exists
- **THEN** the first `<h1>` tag's text content is used
- **AND** whitespace is stripped

#### Scenario: No title found
- **WHEN** none of the title extraction strategies succeed
- **THEN** an empty string is returned for the title

### Requirement: Meta Description Extraction
The system SHALL extract meta descriptions with fallback attempts.

#### Scenario: Extract from description meta tag
- **WHEN** the webpage has a meta tag with name="description"
- **THEN** the content attribute is extracted
- **AND** the description is stripped of whitespace

#### Scenario: Fallback to og:description
- **WHEN** no description meta tag exists
- **THEN** the Open Graph `og:description` meta tag is checked
- **AND** its content attribute is used

#### Scenario: No description found
- **WHEN** no description meta tags exist
- **THEN** an empty string is returned for description

### Requirement: Main Content Extraction
The system SHALL extract main content using common HTML patterns.

#### Scenario: Extract from article tag
- **WHEN** the webpage has an `<article>` tag
- **THEN** the article's text content is extracted
- **AND** the content is truncated at 12,000 characters

#### Scenario: Fallback to main tag
- **WHEN** no article tag exists
- **THEN** the `<main>` tag is checked
- **AND** its text content is extracted

#### Scenario: Fallback to common content selectors
- **WHEN** no article or main tag exists
- **THEN** common content class names are tried: .content, .post-content, .entry-content, #content
- **AND** the first matching element's text is extracted

#### Scenario: No main content found
- **WHEN** no content extraction patterns match
- **THEN** an empty string is returned for main_content

### Requirement: AWS Workshop Studio Special Handling
The system SHALL detect and handle AWS Workshop Studio pages specially.

#### Scenario: AWS Workshop detection
- **WHEN** the URL contains "workshops.aws"
- **THEN** the system recognizes it as an AWS Workshop Studio page
- **AND** applies AWS-specific content extraction logic
- **AND** extracts workshop-specific metadata if available

### Requirement: URL Keyword Generation
The system SHALL generate keywords from URL path components.

#### Scenario: Extract path keywords
- **WHEN** a URL like "https://example.com/docs/python/getting-started" is processed
- **THEN** path components are extracted: ["docs", "python", "getting-started"]
- **AND** common path separators and extensions are removed
- **AND** keywords are included in the extracted data

### Requirement: Content Size Limits
The system SHALL enforce content size limits for extracted data.

#### Scenario: Truncate long content
- **WHEN** extracted main content exceeds 12,000 characters
- **THEN** the content is truncated at exactly 12,000 characters
- **AND** no error or warning is generated

#### Scenario: All fields within limits
- **WHEN** title, description, and content are all within limits
- **THEN** no truncation occurs
- **AND** full content is returned

### Requirement: BeautifulSoup Parser Configuration
The system SHALL use the built-in HTML parser for maximum compatibility.

#### Scenario: Parse with html.parser
- **WHEN** HTML content is parsed with BeautifulSoup
- **THEN** the `html.parser` backend is used (not lxml)
- **AND** no external parser dependencies are required

### Requirement: Custom HTTP Headers
The system SHALL send custom User-Agent headers to avoid blocking.

#### Scenario: Request headers
- **WHEN** making HTTP requests to fetch webpage content
- **THEN** a custom User-Agent string is included
- **AND** other headers are set to mimic a browser request
- **AND** this reduces the likelihood of being blocked by web servers
