# Code Quality Check Workflow

> Workflow for systematic code quality analysis and improvement
> Version: 1.0.0
> Created: 2025-07-25

## Overview

This workflow guides the Code Quality Agent through a comprehensive analysis of project files, identifying issues, and providing actionable recommendations for improvement.

## Workflow Steps

### 1. Project Assessment
**Goal:** Understand the scope and context of the analysis

**Actions:**
- Identify all supported file types in the project
- Count files by type and estimate analysis time
- Check for any files that may need special handling
- Review project structure for context

**Output:** Project analysis summary with file counts and scope

### 2. File-by-File Analysis
**Goal:** Perform detailed quality analysis on each file

**Python Files:**
- Parse AST for structural analysis
- Check naming conventions (snake_case, PascalCase)
- Validate docstring presence and quality
- Assess function and class complexity
- Review import organization
- Check code style compliance (PEP 8)

**Batch Scripts:**
- Validate syntax and structure
- Check for proper variable quoting
- Identify dangerous commands
- Verify error handling practices
- Assess best practices compliance

**CSS Files:**
- Check formatting and indentation consistency
- Validate selector organization
- Identify duplicate rules
- Review vendor prefix usage
- Assess maintainability

**Markdown Files:**
- Validate heading structure and hierarchy
- Check link integrity
- Review formatting consistency
- Assess document organization
- Verify code block formatting

### 3. Issue Prioritization
**Goal:** Categorize and prioritize identified issues

**Critical Issues (Fix Immediately):**
- Syntax errors that prevent execution
- Security vulnerabilities
- Broken functionality

**Important Issues (Fix Soon):**
- Poor naming conventions
- Missing documentation
- Performance concerns
- Maintainability issues

**Minor Issues (Fix When Convenient):**
- Formatting inconsistencies
- Style guide violations
- Optimization opportunities

### 4. Recommendation Generation
**Goal:** Provide actionable suggestions for improvement

**For Each Issue:**
- Explain why it's a problem
- Provide specific fix instructions
- Show before/after examples when helpful
- Estimate effort required to fix

**Overall Recommendations:**
- Suggest systematic approaches to common issues
- Recommend tools or processes for prevention
- Prioritize improvements based on impact

### 5. Report Generation
**Goal:** Create comprehensive, actionable quality report

**Report Structure:**
- Executive summary with key metrics
- File-by-file detailed analysis
- Prioritized issue list
- Specific recommendations
- Next steps and action items

## Quality Standards

### Python Code Standards
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include docstrings for all public functions and classes
- Keep functions under 50 lines
- Limit line length to 88 characters
- Use type hints where appropriate

### Batch Script Standards
- Start scripts with `@echo off`
- Quote all variable assignments with spaces
- Include error checking after file operations
- Use proper exit codes
- Add comments for complex logic

### CSS Standards
- Use consistent 2-space indentation
- Organize properties logically
- Avoid duplicate selectors
- Use meaningful class names
- Include comments for complex sections

### Markdown Standards
- Start documents with H1 heading
- Use consistent heading hierarchy
- Ensure all links are valid
- Use proper list formatting
- Include descriptive link text

## Integration Points

### With Security Framework
- Respect file access permissions
- Log all analysis activities
- Request approval for any file modifications
- Operate within defined sandbox boundaries

### With Documentation Agent
- Coordinate updates to documentation
- Share findings about documentation issues
- Collaborate on README and guide improvements

### With User Approval
- Present findings clearly before any changes
- Request explicit approval for file modifications
- Provide rollback options for changes
- Maintain audit trail of all actions

## Error Handling

### Analysis Failures
- Log specific error details
- Continue with other files when possible
- Provide helpful error messages
- Suggest troubleshooting steps

### Permission Issues
- Respect security boundaries
- Request appropriate permissions
- Fail gracefully when access denied
- Provide clear explanation of limitations

### Resource Constraints
- Monitor memory and CPU usage
- Implement timeouts for large files
- Process files in manageable chunks
- Provide progress updates for long operations

## Quality Metrics

### Analysis Coverage
- Percentage of files analyzed successfully
- Types of issues identified
- Distribution of severity levels
- Time spent on analysis

### Issue Resolution
- Number of issues fixed
- Types of improvements made
- Impact on code quality scores
- User satisfaction with recommendations

### Process Efficiency
- Analysis time per file
- Resource usage during analysis
- Accuracy of issue detection
- Usefulness of recommendations

## Continuous Improvement

### Learning from Feedback
- Track which recommendations are implemented
- Monitor recurring issue patterns
- Adjust analysis algorithms based on results
- Update standards based on team preferences

### Tool Enhancement
- Add support for new file types
- Improve detection algorithms
- Enhance reporting capabilities
- Integrate with additional quality tools