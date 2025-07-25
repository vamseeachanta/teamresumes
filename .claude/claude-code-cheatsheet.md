# Claude Code Cheatsheet

> Quick reference for Claude Code CLI in the TeamResumes project
> Last Updated: 2025-07-25

## 🚀 Quick Start

### Most Common Commands

```bash
# Start Claude Code in current directory
claude

# Open specific file or directory
claude path/to/file.md
claude .agent-os/specs/

# Chat mode (ask questions about code)
claude --chat "explain this build script"

# Continue previous conversation
claude --continue

# Show help
claude --help
```

### Essential Keyboard Shortcuts (Interactive Mode)

- `Ctrl+O` - Open file/directory
- `Ctrl+K` - Clear conversation
- `Ctrl+R` - Search command history
- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Claude Code
- `Tab` - Autocomplete file paths

### Quick TeamResumes Example

```bash
# Update all team member resumes
claude "Update all resume markdown files to include the new project"

# Generate PDFs for all resumes
claude "Run the build scripts to generate PDFs for all team members"

# Review resume formatting
claude va_resume.md "Check if this resume follows our standard format"
```

## 📖 CLI Commands Reference

### Basic Commands

```bash
claude [options] [path] [prompt]

# Options:
--chat, -c          # Start in chat mode
--continue          # Continue last conversation
--model MODEL       # Specify model (opus, sonnet, haiku)
--no-cache         # Disable context caching
--json             # Output in JSON format
--version          # Show version info
--help             # Show help
```

### File Operations

```bash
# Open and edit specific file
claude resume/va_resume.md

# Work with multiple files
claude "Update skills section" resume/*.md

# Review changes
claude --diff "Show me what changed in the last commit"
```

### Project Context

```bash
# Add context from CLAUDE.md
claude --context .

# Use specific context file
claude --context .agent-os/product/mission.md

# Ignore context
claude --no-context
```

## ⌨️ Keyboard Shortcuts

### Navigation
| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+O` | Open file/directory | Browse project files |
| `Ctrl+P` | Command palette | Quick access to commands |
| `Ctrl+F` | Find in conversation | Search current chat |
| `Ctrl+G` | Go to line | Jump to specific line |
| `↑/↓` | Navigate history | Browse previous commands |
| `PgUp/PgDn` | Scroll conversation | Move through long responses |

### Editing
| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+K` | Clear conversation | Start fresh |
| `Ctrl+Z` | Undo last action | Revert changes |
| `Ctrl+E` | Edit mode | Modify current file |
| `Ctrl+S` | Save changes | Write to disk |
| `Tab` | Autocomplete | Complete file paths |

### Session Management
| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+C` | Cancel operation | Stop current task |
| `Ctrl+D` | Exit Claude Code | Close session |
| `Ctrl+L` | Clear screen | Clean display |
| `Ctrl+R` | Search history | Find previous commands |

## 🔄 TeamResumes Workflows

### 1. Update Multiple Resumes

```bash
# Add new skill to all resumes
claude "Add 'Agent OS' to skills section in all resume files"

# Update project descriptions
claude "Update the OrcaFlex project description in all resumes to mention the new digital twin feature"
```

### 2. Generate PDFs

```bash
# Single resume
claude "Run generate_va_resume.bat to create PDF"

# All resumes
claude "Execute all generate_*.bat scripts to build PDFs"

# Check output
claude "List all files in output/ directory"
```

### 3. Format Consistency

```bash
# Check formatting
claude "Review all resumes and ensure consistent section headings"

# Fix formatting issues
claude "Standardize the date format in all experience sections to 'MMM YYYY'"
```

### 4. LinkedIn Content Generation

```bash
# Extract skills for LinkedIn
claude va_resume.md "Generate a LinkedIn skills section from this resume"

# Create post content
claude "Create a LinkedIn post about my latest project from va_resume.md"
```

### 5. Team Overview

```bash
# Generate team summary
claude "Create a summary of all team members' skills from the resume files"

# Skills matrix
claude "Build a skills matrix showing which team members have which technologies"
```

## ⚙️ Configuration & Settings

### Environment Variables

```bash
# Set default model
export CLAUDE_MODEL=opus

# Set context timeout
export CLAUDE_CONTEXT_TIMEOUT=3600

# Custom config location
export CLAUDE_CONFIG_DIR=~/.claude
```

### CLAUDE.md Integration

Your project's CLAUDE.md is automatically loaded. Key sections:
- Agent OS documentation references
- Development standards
- Project-specific workflows

### Recommended Settings

```json
// .claude/config.json
{
  "model": "opus",
  "contextWindow": 200000,
  "temperature": 0.7,
  "cacheContext": true,
  "autoSave": true
}
```

## 💡 Tips & Tricks

### Performance Optimization

1. **Use context caching**: Enabled by default, saves time on repeated operations
2. **Batch operations**: Process multiple files in one command
3. **Specific prompts**: Be precise to get better results faster

### Common Patterns

```bash
# Before making changes, review current state
claude "Show me the current structure of va_resume.md"

# Make targeted updates
claude va_resume.md "Add the new certification to the certifications section"

# Verify changes
claude --diff "Show what changed in va_resume.md"
```

### TeamResumes Specific

1. **Resume Updates**: Always update markdown first, then generate PDFs
2. **Consistency**: Use Claude to ensure all resumes follow the same format
3. **Validation**: Check that all required sections are present

### Troubleshooting

**Issue**: Changes not saving
```bash
# Check file permissions
claude "Check if I have write permissions for resume files"
```

**Issue**: PDF generation fails
```bash
# Debug build script
claude "Review generate_va_resume.bat and check for errors"
```

**Issue**: Context not loading
```bash
# Verify CLAUDE.md exists
claude "Check if CLAUDE.md exists in the project root"
```

## 🔗 Integration with TeamResumes

### Working with Build Scripts

```bash
# Review build process
claude "Explain how the generate_*.bat scripts work"

# Modify build scripts
claude "Update generate_all_resumes.bat to include error handling"
```

### Git Integration

```bash
# Commit changes
claude "Create a git commit for the resume updates"

# Review changes before committing
claude "Show me all modified files in the working directory"
```

### CI/CD Pipeline

```bash
# Check GitHub Actions
claude "Review .github/workflows and explain the PDF generation process"

# Update workflow
claude "Add all team members to the GitHub Actions PDF generation"
```

---

**Pro Tip**: Save frequently used commands as aliases in your shell configuration:
```bash
alias resume-update="claude 'Update all resume files with latest changes'"
alias resume-build="claude 'Run all generate_*.bat scripts'"
```