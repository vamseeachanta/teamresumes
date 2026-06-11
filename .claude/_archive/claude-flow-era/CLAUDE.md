# Local Claude Configuration - Team Resumes

> **Context Budget**: 2KB max | Inherits from workspace-hub CLAUDE.md

## Key Rules

1. **Orchestrate, don't execute** - Delegate via Task tool
2. **TDD mandatory** - Tests before implementation
3. **YAGNI** - Only what's needed
4. **No sycophancy** - Ask questions when unclear
5. **Batch operations** - 1 message = ALL related operations

## Plan Mode Convention

Save plans to: `specs/modules/<module>/`
- Templates: `specs/templates/plan-template.md`
- Cross-Review (MANDATORY): 3 iterations with OpenAI Codex + Google Gemini

## File Organization

- `/src` - Source code
- `/tests` - Test files
- `/docs` - Documentation
- `/specs` - Plans and specifications
- `/scripts` - Utilities

## Reference Docs (Load On-Demand)

| Doc | When |
|-----|------|
| `.claude/docs/engineering-principles.md` | Code quality, TDD, debugging |
| `.claude/docs/ai-orchestration.md` | SPARC, agents, coordination |
| `.claude/docs/agents.md` | Spawning agents |
| `.claude/docs/mcp-tools.md` | MCP coordination |
| `.claude/docs/execution-patterns.md` | Complex workflows |
| `.claude/docs/CONTEXT_LIMITS.md` | Context management |

## Environment

- Python: `>=3.10` with uv environment
- Run tests: `uv run pytest`

---

*Verbose docs extracted to `.claude/docs/`. See workspace-hub rules for full standards.*
