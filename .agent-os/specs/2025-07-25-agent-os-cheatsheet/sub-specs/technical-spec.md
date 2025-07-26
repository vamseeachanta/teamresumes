# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-07-25-agent-os-cheatsheet/spec.md

> Created: 2025-07-25
> Version: 1.0.0

## Technical Requirements

- Create a single markdown file that serves as a quick reference guide
- File should be located at `.agent-os/agent-os-cheatsheet.md` for easy access
- Content must be scannable with clear section headers and formatting
- Include both general Agent OS commands and TeamResumes-specific usage
- Use code blocks for commands and file paths for clarity
- Keep descriptions concise - this is a cheatsheet, not full documentation

## Approach Options

**Option A:** Create multiple small reference files by topic
- Pros: Modular, easier to maintain individual sections
- Cons: Harder to scan quickly, requires multiple file lookups

**Option B:** Single comprehensive cheatsheet file (Selected)
- Pros: All information in one place, quick to scan, easy to search
- Cons: May become long, requires good organization

**Rationale:** A single file aligns with the cheatsheet concept - users want one place to look for quick answers. Good organization and formatting will address the length concern.

## Content Structure Design

### 1. Quick Start Section
- Essential commands to get started
- Where to find key files
- Basic workflow overview

### 2. Command Reference
- All slash commands with brief descriptions
- Common command patterns
- Examples with actual file paths

### 3. File Structure Map
- Visual ASCII diagram of Agent OS directories
- Brief explanation of each directory's purpose
- Links to key files

### 4. Workflow Patterns
- Step-by-step for common tasks
- Creating a new spec
- Executing tasks
- Reviewing and updating specs

### 5. TeamResumes Specific
- Project-specific conventions
- Common resume-related tasks
- Integration with existing scripts

### 6. Troubleshooting
- Common errors and solutions
- Where to check for issues
- Debug tips

## External Dependencies

- No new dependencies required
- Uses existing markdown rendering in the project