# AI Orchestration & SPARC Methodology

> Extracted from `.claude/CLAUDE.md` to respect 2KB context limit.
> Load on-demand: `@.claude/docs/ai-orchestration.md`

## Concurrent Execution Rules

- ALL operations MUST be concurrent/parallel in a single message.
- Never save working files to the root folder.
- Use Task tool for spawning agents concurrently.

### Golden Rule: 1 Message = ALL Related Operations

Batch all: TodoWrite, Task tool, file operations, bash commands, memory operations.

## File Organization

- `/src` - Source code
- `/tests` - Test files
- `/docs` - Documentation
- `/config` - Configuration
- `/scripts` - Utility scripts
- `/data` - CSV data (raw/, processed/, results/)
- `/reports` - Generated HTML reports

## HTML Reporting

- All visualizations MUST be interactive (Plotly, Bokeh, Altair, D3.js).
- Every module generates HTML reports.
- CSV data imported with relative paths.

## SPARC Workflow Phases

1. **Specification** - Requirements analysis
2. **Pseudocode** - Algorithm design
3. **Architecture** - System design
4. **Refinement** - TDD implementation
5. **Completion** - Integration

## Claude Code vs MCP Tools

**Claude Code handles ALL execution** (Task tool, file ops, code gen, bash, git, testing).
**MCP tools ONLY coordinate** (swarm init, agent types, task orchestration, memory).

## Agent Coordination Protocol

Every agent spawned via Task tool must run hooks:
- **Before**: `npx claude-flow@alpha hooks pre-task`
- **During**: `npx claude-flow@alpha hooks post-edit`
- **After**: `npx claude-flow@alpha hooks post-task`

## Available Agents (54 Total)

Core: coder, reviewer, tester, planner, researcher
Swarm: hierarchical/mesh/adaptive/collective-intelligence coordinators
GitHub: pr-manager, code-review-swarm, release-manager, repo-architect
SPARC: specification, pseudocode, architecture, refinement
Specialized: backend-dev, mobile-dev, ml-developer, cicd-engineer, system-architect
