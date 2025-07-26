# Spec Requirements Document

> Spec: Agent OS Cheatsheet
> Created: 2025-07-25
> Status: Planning

## Overview

Create a comprehensive cheatsheet for Agent OS that provides quick reference for team members using the Agent OS framework within the TeamResumes project. This will improve onboarding and daily workflow efficiency.

### Future Update Prompt

For future modifications to this spec, use the following prompt:
```
Update the Agent OS cheatsheet spec to include:
- New Agent OS commands or workflows
- Additional troubleshooting tips
- Updated project-specific instructions
- Team feedback on missing information
Maintain compatibility with existing Agent OS structure and ensure the cheatsheet remains concise and actionable.
```

## User Stories

### Quick Reference for Team Members

As a team member, I want to quickly reference Agent OS commands and workflows, so that I can efficiently use the framework without constantly referring to full documentation.

Team members need a concise reference guide that shows common commands, file locations, and workflow patterns. They should be able to find information about creating specs, executing tasks, and understanding the Agent OS structure within seconds.

### Onboarding New Team Members

As a team lead, I want new team members to have a clear starting point for Agent OS, so that they can become productive quickly without extensive training.

New team members should be able to understand the basic Agent OS concepts, locate key files, and start contributing to the project with minimal guidance.

## Spec Scope

1. **Command Reference** - Quick reference for all Agent OS slash commands and their usage
2. **File Structure Guide** - Visual representation of Agent OS directory structure with explanations
3. **Workflow Patterns** - Common workflows like creating specs and executing tasks
4. **Project-Specific Tips** - TeamResumes-specific Agent OS usage patterns and conventions
5. **Troubleshooting Guide** - Common issues and their solutions

## Out of Scope

- Detailed Agent OS implementation documentation
- Full tutorial content (keep it as a quick reference)
- Installation instructions (assumed to be already set up)
- Modifications to existing Agent OS functionality

## Expected Deliverable

1. A single markdown file (agent-os-cheatsheet.md) in the .agent-os folder
2. Content organized in scannable sections with clear headers
3. Examples specific to the TeamResumes project where applicable

## Spec Documentation

- Tasks: @.agent-os/specs/2025-07-25-agent-os-cheatsheet/tasks.md
- Technical Specification: @.agent-os/specs/2025-07-25-agent-os-cheatsheet/sub-specs/technical-spec.md
- Tests Specification: @.agent-os/specs/2025-07-25-agent-os-cheatsheet/sub-specs/tests.md