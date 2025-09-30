# Claude Flow Setup for TeamResumes

## Overview

The Claude Flow has been successfully configured for the TeamResumes project. This setup integrates with the Agent OS framework to provide automated resume management, PDF generation, and LinkedIn content creation.

## Setup Completed

### 1. UV Environment
- Created Python 3.11 virtual environment
- Installed all project dependencies from pyproject.toml
- Environment location: `.venv/`

### 2. Configuration Files
- **Claude Flow Config**: `.agent-os/claude-flow.yaml`
  - Defines workflows for resume updates, LinkedIn sync, and team profiles
  - Configures parallel processing and automation settings
  
- **Resume Manager**: `.agent-os/commands/resume_manager.py`
  - Core Python module for resume operations
  - Handles PDF generation, LinkedIn content, and team profiles

- **Resume Command**: `.agent-os/commands/resume.py`
  - Slash command wrapper for easy access
  - Provides simple CLI interface

## Available Commands

### Resume Management
```bash
# List all team members and their PDF status
python .agent-os/commands/resume.py list

# Update a team member's resume and generate PDF
python .agent-os/commands/resume.py update va

# Generate LinkedIn content
python .agent-os/commands/resume.py linkedin va summary
python .agent-os/commands/resume.py linkedin gp skills
python .agent-os/commands/resume.py linkedin ss post

# Create team capabilities overview
python .agent-os/commands/resume.py team pdf
```

### Slash Command Usage
You can also use the slash command wrapper:
```bash
./slash /resume list
./slash /resume update va
./slash /resume linkedin gp skills
./slash /resume team
```

## Features

### 1. Resume Updates
- Validates markdown format
- Generates PDF using pandoc/wkhtmltopdf
- Auto-commits changes to git (if enabled)
- Supports team members: VA, GP, SS, SP

### 2. LinkedIn Integration
- **Summary**: Professional summary for LinkedIn profile
- **Skills**: Formatted skills list with endorsement suggestions
- **Post**: Ready-to-post content with achievements

### 3. Team Profiles
- Aggregates all team member resumes
- Generates skills matrix
- Creates team overview document
- Supports PDF, Markdown, and HTML formats

### 4. Parallel Processing
- Enabled for file operations
- PDF generation runs concurrently
- Maximum 5 workers for optimal performance

## Workflows

### Resume Update Workflow
1. Validate markdown format
2. Generate PDF from markdown
3. Commit changes (if auto-commit enabled)

### LinkedIn Sync Workflow
1. Extract skills, experience, achievements
2. Generate formatted content
3. Save to `cv/linkedin/` directory

### Team Profile Workflow
1. Collect all resume files
2. Generate skills matrix
3. Create combined overview document

## Configuration

### Git Integration
- Auto-commit: Enabled
- Branch strategy: main
- Commit format: Conventional commits

### PDF Generation
- Engine: wkhtmltopdf
- Stylesheet: resume-stylesheet.css
- Format: PDF by default

### UV Environment
- Python version: 3.11
- Auto-activate: Yes
- Dependencies: pyproject.toml

## Directory Structure
```
teamresumes/
├── .agent-os/
│   ├── claude-flow.yaml       # Main configuration
│   └── commands/
│       ├── resume_manager.py  # Core functionality
│       └── resume.py          # Slash command
├── cv/                        # Resume files
│   ├── va_resume.md
│   ├── gp_resume.md
│   ├── ss_resume.md
│   ├── sp_resume.md
│   └── linkedin/              # LinkedIn content
├── docs/                      # Team documentation
└── .venv/                     # Python environment
```

## Next Steps

1. **Update All PDFs**: Run `python .agent-os/commands/resume.py update gp` for each team member
2. **Generate LinkedIn Content**: Create summaries for all team members
3. **Create Team Profile**: Generate team capabilities overview
4. **Set Up Automation**: Configure GitHub Actions for automatic PDF generation

## Troubleshooting

### PDF Generation Issues
- Ensure pandoc is installed: `pandoc --version`
- Check wkhtmltopdf: `wkhtmltopdf --version`
- Fallback to Python PDF generation if needed

### Unicode Errors on Windows
- Fixed with UTF-8 encoding wrapper
- Emojis now display correctly in console

### YAML Configuration Errors
- All list items properly quoted
- No mixed syntax issues
- Valid YAML structure

## Integration with Agent OS

This Claude Flow integrates seamlessly with:
- Agent OS slash commands
- UV environment management
- Git workflow automation
- Parallel processing capabilities
- Cross-repository synchronization

The system is ready for production use and can be extended with additional workflows as needed.