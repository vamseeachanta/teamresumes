# Sub-Agents System Documentation

## Overview

The TeamResumes sub-agents system provides automated task execution for code quality, documentation maintenance, resume processing, content generation, and project maintenance. Each sub-agent specializes in specific tasks while working together through coordinated workflows.

## Quick Start

### Prerequisites

- Python 3.6+
- All project dependencies installed
- `.agent-os/sub-agents/` directory structure in place

### Basic Usage

```bash
# List available agents
python -c "from integration_handler import ClaudeCodeIntegration; print(ClaudeCodeIntegration().execute_command('list-agents', {}))"

# Run a single agent
python -c "from integration_handler import ClaudeCodeIntegration; print(ClaudeCodeIntegration().execute_command('run-agent', {'agent': 'code-quality-agent', 'target': '*.py'}))"

# Execute a workflow
python -c "from integration_handler import ClaudeCodeIntegration; print(ClaudeCodeIntegration().execute_command('run-workflow', {'workflow': 'code-quality-check'}))"
```

## Available Agents

### 1. Code Quality Agent
**Purpose**: Analyzes code quality, style consistency, and best practices adherence

**Capabilities**:
- Python code analysis (PEP 8, complexity, maintainability)
- Batch script validation for Windows
- CSS and markdown consistency checking
- Code metrics and quality scoring

**Usage**:
```bash
run-agent code-quality-agent analyze *.py
run-agent code-quality-agent validate dev_tools/*.bat
```

**Configuration**: `.agent-os/sub-agents/configurations/code-quality-agent.yaml`

### 2. Documentation Agent
**Purpose**: Maintains and updates project documentation

**Capabilities**:
- Cross-reference link validation
- Automatic documentation generation
- README.md maintenance and updates
- Documentation structure analysis

**Usage**:
```bash
run-agent documentation-agent update
run-agent documentation-agent validate-links
```

**Configuration**: `.agent-os/sub-agents/configurations/documentation-agent.yaml`

### 3. Resume Processing Agent
**Purpose**: Validates and processes resume markdown files

**Capabilities**:
- Resume markdown validation
- PDF generation quality assurance
- Skills and experience formatting validation
- Resume data extraction and analysis

**Usage**:
```bash
run-agent resume-processing-agent validate cv/va_resume.md
run-agent resume-processing-agent analyze cv/
```

**Configuration**: `.agent-os/sub-agents/configurations/resume-processing-agent.yaml`

### 4. Content Generation Agent
**Purpose**: Generates professional content from resume data

**Capabilities**:
- LinkedIn post generation (respects 3000 character limit)
- Professional bio generation with variations
- Social media content templates
- Skills and experience highlighting

**Usage**:
```bash
run-agent content-generation-agent linkedin cv/va_resume.md
run-agent content-generation-agent bio cv/va_resume.md --style=professional
```

**Configuration**: `.agent-os/sub-agents/configurations/content-generation-agent.yaml`

### 5. Maintenance Agent
**Purpose**: Monitors project health and maintenance needs

**Capabilities**:
- Dependency monitoring and analysis
- Security vulnerability scanning
- Project health metrics tracking
- Update recommendations

**Usage**:
```bash
run-agent maintenance-agent scan
run-agent maintenance-agent health-check
```

**Configuration**: `.agent-os/sub-agents/configurations/maintenance-agent.yaml`

## Predefined Workflows

### Code Quality Check
**Description**: Comprehensive code quality analysis and documentation updates

**Execution Type**: Sequential
**Agents**: code-quality-agent → documentation-agent
**Usage**: `run-workflow code-quality-check`

**Steps**:
1. Analyze code quality across Python, batch, and CSS files
2. Update documentation based on findings
3. Generate quality report

### Resume Processing
**Description**: Complete resume validation and processing pipeline

**Execution Type**: Sequential
**Agents**: resume-processing-agent → content-generation-agent
**Usage**: `run-workflow resume-processing`

**Steps**:
1. Validate resume markdown structure and content
2. Generate LinkedIn content and professional bios
3. Create content packages for social media

### Maintenance Check
**Description**: Project health and security monitoring

**Execution Type**: Parallel
**Agents**: maintenance-agent (multiple actions)
**Usage**: `run-workflow maintenance-check`

**Steps**:
1. Scan dependencies for vulnerabilities
2. Check project health metrics
3. Generate maintenance recommendations

## Advanced Usage

### Custom Workflows

Create custom workflows by combining agents:

```python
from integration_handler import ConfigurationManager

config_manager = ConfigurationManager()
config_manager.create_custom_workflow(
    name='custom-quality-check',
    agents=['code-quality-agent', 'maintenance-agent'],
    execution_type='sequential'
)
```

### Agent Status Monitoring

```python
from integration_handler import ClaudeCodeIntegration

integration = ClaudeCodeIntegration()
status = integration.execute_command('agent-status', {'agent': 'code-quality-agent'})
print(f"Agent Status: {status}")
```

### Result Formatting

```python
from integration_handler import ResultFormatter

formatter = ResultFormatter()
formatted_result = formatter.format_agent_result(agent_result)
print(formatted_result)
```

## Configuration Management

### Agent Configuration Structure

Each agent has a YAML configuration file in `.agent-os/sub-agents/configurations/`:

```yaml
name: "example-agent"
version: "1.0.0"
specialization: "Example tasks"

metadata:
  status: "active"
  author: "TeamResumes"
  capabilities:
    - "example_capability_1"
    - "example_capability_2"

behavior:
  analysis_depth: "comprehensive"
  report_format: "detailed"
  max_file_size: 10485760

security:
  sandbox_enabled: true
  allowed_file_extensions:
    - ".py"
    - ".md"
  restricted_paths:
    - "/etc"
    - "/usr/bin"

tools:
  allowed:
    - "file_read"
    - "file_write"
    - "file_analyze"
  
  restricted:
    - "external_api_calls"
    - "system_modifications"
```

### Updating Configurations

```python
from integration_handler import ConfigurationManager

config_manager = ConfigurationManager()
config_manager.update_agent_config('code-quality-agent', {
    'behavior': {
        'analysis_depth': 'comprehensive',
        'report_format': 'detailed'
    }
})
```

## Security Framework

### Sandboxing

All agents run within a security sandbox that:
- Restricts file system access to project directories
- Limits allowed file extensions
- Prevents access to system directories
- Logs all file operations for audit

### Permissions

Agents have granular permissions:
- **file_read**: Read files within sandbox
- **file_write**: Write files within sandbox  
- **file_analyze**: Analyze file contents
- **process_execute**: Execute safe subprocesses
- **system_info**: Access basic system information

### Audit Logging

All agent activities are logged for security audit:
- File access attempts
- Permission violations
- Command executions
- Error conditions

## Troubleshooting

### Common Issues

**Issue**: Agent not found error
**Solution**: Ensure agent configuration exists and name matches exactly
```bash
# Check available agents
run-agent list-agents
```

**Issue**: Permission denied
**Solution**: Verify file permissions and sandbox configuration
```bash
# Check agent status
agent-status <agent-name>
```

**Issue**: Configuration loading failed
**Solution**: Validate YAML syntax in agent configuration
```bash
# Test configuration parsing
python -c "import yaml; yaml.safe_load(open('.agent-os/sub-agents/configurations/agent-name.yaml'))"
```

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Monitoring

Monitor agent performance:

```python
from integration_handler import PerformanceMonitor

monitor = PerformanceMonitor()
session_id = monitor.start_monitoring_session('debug-session')
# ... run agents ...
summary = monitor.get_performance_summary(session_id)
```

## Integration with Claude Code

The sub-agents system integrates seamlessly with Claude Code through the integration handler:

### Command Registration

All sub-agent commands are automatically registered with Claude Code:
- `run-agent`
- `run-workflow` 
- `list-agents`
- `agent-status`
- `list-workflows`

### Result Formatting

Agent results are automatically formatted for Claude Code display with:
- Structured output formatting
- Progress indicators
- Error handling
- Performance metrics

### Real-time Monitoring

Progress updates are displayed in real-time during workflow execution:
- Workflow progress tracking
- Individual agent status
- Performance metrics
- Error reporting

## Development Guidelines

### Adding New Agents

1. Create agent configuration YAML file
2. Implement agent class with required methods
3. Add agent to coordination workflows if needed
4. Update documentation and examples
5. Add comprehensive tests

### Testing

Run the comprehensive test suite:

```bash
python test_integration.py
python test_security_framework.py
python test_agent_coordinator.py
```

### Contributing

1. Follow project code style standards
2. Add tests for new functionality
3. Update documentation
4. Ensure security compliance
5. Test integration with existing agents

## API Reference

### ClaudeCodeIntegration Class

Main integration point with Claude Code.

#### Methods

- `execute_command(command: str, parameters: Dict) -> Dict`
- `get_registered_commands() -> Dict`

### AgentCoordinator Class

Manages multi-agent workflow execution.

#### Methods

- `execute_workflow(workflow: Dict, status_callback: Optional[Callable]) -> Dict`
- `discover_agents() -> List[Dict]`

### ResultFormatter Class

Formats agent execution results for display.

#### Methods

- `format_agent_result(result: Dict) -> str`
- `format_workflow_result(result: Dict) -> str`
- `format_error_result(result: Dict) -> str`

### ConfigurationManager Class

Manages agent and workflow configurations.

#### Methods

- `update_agent_config(agent: str, updates: Dict) -> bool`
- `create_custom_workflow(name: str, agents: List[str], execution_type: str) -> bool`
- `list_available_workflows() -> List[Dict]`

---

For more information, see:
- Agent configurations: `.agent-os/sub-agents/configurations/`
- Workflow definitions: `.agent-os/sub-agents/coordination/`
- Integration tests: `.agent-os/sub-agents/test_*.py`