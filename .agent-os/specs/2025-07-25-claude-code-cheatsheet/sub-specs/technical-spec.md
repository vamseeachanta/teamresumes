# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-07-25-claude-code-cheatsheet/spec.md

> Created: 2025-07-25
> Version: 1.0.0

## Technical Requirements

- Create a single markdown cheatsheet file for Claude Code reference
- File location: `.claude/claude-code-cheatsheet.md`
- Content must be optimized for quick reference during active development
- Include both general Claude Code features and TeamResumes-specific usage
- Use consistent formatting with code blocks and tables where appropriate
- Keep descriptions brief but complete enough to be actionable

## Approach Options

**Option A:** Separate files for commands, shortcuts, and workflows
- Pros: Focused content, easier to maintain sections
- Cons: Multiple files to reference, harder to search across topics

**Option B:** Single comprehensive cheatsheet (Selected)
- Pros: One-stop reference, easy to search, better for quick access
- Cons: Potentially long file, requires careful organization

**Rationale:** A single file better serves the cheatsheet purpose - developers want immediate access to all information without switching files. Proper sectioning and formatting will maintain readability.

## Content Structure Design

### 1. Quick Start
- Most common commands for TeamResumes tasks
- Essential keyboard shortcuts
- Basic workflow example

### 2. CLI Commands Reference
- Command syntax with examples
- Common flags and options
- TeamResumes-specific command patterns

### 3. Keyboard Shortcuts
- Complete shortcut list organized by function
- Platform-specific variations (Windows/Mac/Linux)
- Custom shortcut recommendations

### 4. Interactive Mode Features
- Search and navigation
- Multi-file operations
- Session management

### 5. TeamResumes Workflows
- Updating multiple resumes
- Generating PDFs with Claude Code
- Working with markdown templates
- Integrating with existing build scripts

### 6. Configuration & Settings
- Recommended settings for TeamResumes
- Environment variables
- Working with CLAUDE.md

### 7. Tips & Tricks
- Performance optimization
- Common patterns
- Troubleshooting guide

## External Dependencies

- No new dependencies required
- References existing Claude Code installation
- Integrates with current TeamResumes workflow