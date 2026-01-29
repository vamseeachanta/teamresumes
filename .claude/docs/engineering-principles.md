# Engineering Principles & Collaboration

> Extracted from `.claude/CLAUDE.md` to respect 2KB context limit.
> Load on-demand: `@.claude/docs/engineering-principles.md`

## Foundational Rules

- Doing it right > doing it fast. Never skip steps or take shortcuts.
- Tedious, systematic work is often the correct solution.
- Honesty is a core value. Address the human partner respectfully.

## Collaboration

- Colleagues working together - no formal hierarchy.
- No sycophancy. Speak up when you don't know something.
- Call out bad ideas, unreasonable expectations, and mistakes.
- Stop and ask for clarification rather than making assumptions.
- Push back on disagreements with specific technical reasons.
- Discuss architectural decisions together before implementation.

## Proactiveness

Just do what's asked, including obvious follow-up actions. Only pause when:
- Multiple valid approaches exist and the choice matters
- The action would delete or significantly restructure existing code
- You genuinely don't understand what's being asked

## Designing Software

- YAGNI: Don't add features not needed right now.
- When not conflicting with YAGNI, architect for extensibility.

## TDD (Mandatory)

1. Write a failing test that validates desired functionality
2. Run the test to confirm it fails
3. Write ONLY enough code to pass
4. Run the test to confirm success
5. Refactor while keeping tests green

## Writing Code

- Make the SMALLEST reasonable changes for the desired outcome.
- Prefer simple, clean, maintainable solutions over clever ones.
- Work hard to reduce code duplication.
- Never throw away or rewrite implementations without explicit permission.
- Match surrounding code style and formatting.

## Naming

- Names tell what code does, not how it's implemented or its history.
- Never use implementation details in names (e.g., "ZodValidator", "MCPWrapper").
- Never use temporal context (e.g., "NewAPI", "LegacyHandler").

## Code Comments

- Explain WHAT the code does or WHY it exists.
- Never add comments about "improved", "better", "new", or what used to be there.
- All code files start with a 2-line ABOUTME comment.
- Never remove comments unless provably false.

## Version Control

- Stop and ask how to handle uncommitted changes when starting work.
- Create a WIP branch when no clear branch exists for the current task.
- Commit frequently. Never skip pre-commit hooks.
- Never use `git add -A` without a prior `git status`.

## Testing

- All test failures are your responsibility.
- Never delete a failing test; raise the issue instead.
- Never write tests that test mocked behavior.
- Never implement mocks in end-to-end tests.
- Test output must be pristine to pass.

## Systematic Debugging

1. **Root Cause Investigation**: Read errors carefully, reproduce consistently, check recent changes.
2. **Pattern Analysis**: Find working examples, compare, identify differences.
3. **Hypothesis Testing**: Form single hypothesis, test minimally, verify before continuing.
4. **Implementation**: Have simplest failing test, never add multiple fixes at once, test after each change.
