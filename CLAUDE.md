# CLAUDE.md

## Agent OS Documentation

### Product Context
- **Mission & Vision:** @.agent-os/product/mission.md
- **Technical Architecture:** @.agent-os/product/tech-stack.md
- **Development Roadmap:** @.agent-os/product/roadmap.md
- **Decision History:** @.agent-os/product/decisions.md

### Development Standards
- **Code Style:** @~/.agent-os/standards/code-style.md
- **Best Practices:** @~/.agent-os/standards/best-practices.md

### Project Management
- **Active Specs:** @.agent-os/specs/
- **Spec Planning:** Use `@~/.agent-os/instructions/create-spec.md`
- **Tasks Execution:** Use `@~/.agent-os/instructions/execute-tasks.md`

### Sub-Agent System
- **Available Agents:** @.agent-os/sub-agents/configurations/
- **Agent Coordination:** @.agent-os/sub-agents/coordination/
- **Integration Commands:** See sub-agent commands below

## Workflow Instructions

When asked to work on this codebase:

1. **First**, check @.agent-os/product/roadmap.md for current priorities
2. **Then**, follow the appropriate instruction file:
   - For new features: @.agent-os/instructions/create-spec.md
   - For tasks execution: @.agent-os/instructions/execute-tasks.md
3. **Always**, adhere to the standards in the files listed above

## Sub-Agent Commands

The project includes a comprehensive sub-agent system for automated tasks:

### Available Agents
- **code-quality-agent**: Analyzes code quality, style, and best practices
- **documentation-agent**: Maintains documentation, validates links, generates docs
- **resume-processing-agent**: Validates and processes resume markdown files
- **content-generation-agent**: Generates LinkedIn posts and professional bios
- **maintenance-agent**: Monitors dependencies, security vulnerabilities, project health

### Basic Commands
```bash
# Execute single agent
run-agent <agent-name> [action] [target]

# Execute predefined workflow
run-workflow <workflow-name> [context]

# List available agents and workflows
list-agents
list-workflows

# Check agent status
agent-status <agent-name>
```

### Example Usage
```bash
# Analyze code quality
run-agent code-quality-agent analyze *.py

# Update documentation
run-agent documentation-agent update

# Process resume
run-agent resume-processing-agent validate cv/va_resume.md

# Generate LinkedIn content
run-agent content-generation-agent linkedin cv/va_resume.md

# Run full quality check workflow
run-workflow code-quality-check
```

### Predefined Workflows
- **code-quality-check**: Sequential quality analysis and documentation updates
- **resume-processing**: Complete resume validation and processing pipeline
- **maintenance-check**: Dependency and security scanning

## Important Notes

- Product-specific files in `.agent-os/product/` override any global standards
- User's specific instructions override (or amend) instructions found in `.agent-os/specs/...`
- Sub-agents follow all project standards and security requirements
- Always adhere to established patterns, code style, and best practices documented above.