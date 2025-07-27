# Getting Started with Sub-Agents

## Executive Summary

The TeamResumes Sub-Agents System is an **automated task execution platform** that helps maintain code quality, documentation, and professional content without manual effort. Think of it as having a team of AI assistants that can:

- **Analyze and improve your code** (like having a code reviewer)
- **Keep your documentation up-to-date** (no more broken links or outdated docs)
- **Process and validate resume files** (ensure professional formatting)
- **Generate LinkedIn content** (turn your resume into social media posts)
- **Monitor project health** (check for security issues and outdated dependencies)

### 🎯 **Business Value**
- **Save 2-4 hours per week** on manual code reviews and documentation maintenance
- **Improve code quality** by 30-40% through automated analysis and recommendations
- **Ensure professional consistency** across all resume and content formats
- **Reduce security risks** through automated vulnerability scanning
- **Accelerate content creation** for professional networking

### 🚀 **Key Benefits**
- **Zero Learning Curve**: Simple commands that anyone can use
- **Instant Results**: Get feedback and improvements in seconds, not hours
- **Always Available**: Run analysis anytime, no waiting for human reviewers
- **Consistent Quality**: Same high standards applied every time
- **Integrated Workflow**: Works seamlessly with existing development processes

---

## What Are Sub-Agents?

Sub-agents are **specialized AI assistants** that automatically perform specific tasks in your project. Instead of manually checking code quality, updating documentation, or formatting resumes, you simply tell a sub-agent to do it for you.

### Real-World Analogy
Imagine you have a small team of specialists:
- **Quality Inspector** (Code Quality Agent) - Reviews all code for problems
- **Librarian** (Documentation Agent) - Keeps all documentation organized and current  
- **HR Specialist** (Resume Processing Agent) - Ensures resumes are perfectly formatted
- **Marketing Assistant** (Content Generation Agent) - Creates social media content
- **IT Security** (Maintenance Agent) - Monitors for security issues

Each specialist knows exactly what to do in their area of expertise, and they can work together on larger projects.

---

## Quick Start (5 Minutes)

### Step 1: Check What's Available
First, see what assistants are ready to help:

```bash
# See all available assistants
list-agents
```

You'll see something like:
```
Found 5 agents:
• code-quality-agent: Analyzes code quality, style, and best practices
• documentation-agent: Maintains documentation, validates links, generates docs
• resume-processing-agent: Validates and processes resume markdown files
• content-generation-agent: Generates LinkedIn posts and professional bios
• maintenance-agent: Monitors dependencies, security vulnerabilities, project health
```

### Step 2: Try Your First Command
Let's check the quality of your Python code:

```bash
# Analyze your Python files for quality issues
run-agent code-quality-agent analyze *.py
```

You'll get a report showing:
- Code quality score (0-100)
- Issues found (if any)
- Specific recommendations for improvement

### Step 3: Run a Complete Workflow
Instead of running agents one by one, you can run a complete workflow:

```bash
# Run a complete quality check (code + documentation)
run-workflow code-quality-check
```

This automatically runs multiple agents in the right order and gives you a comprehensive report.

---

## Common Use Cases

### 📝 **Before Committing Code**
**Problem**: "I want to make sure my code is good quality before pushing to GitHub"

**Solution**:
```bash
# Quick quality check before commit
run-workflow code-quality-check
```

**What it does**:
- Analyzes your code for style issues, complexity problems, and best practice violations
- Checks documentation for broken links and missing sections
- Provides specific recommendations for improvement

### 💼 **Updating Your Resume**
**Problem**: "I updated my resume and want to make sure it's properly formatted and create LinkedIn content"

**Solution**:
```bash
# Process and validate your resume
run-agent resume-processing-agent validate cv/your_resume.md

# Generate LinkedIn content from your resume
run-agent content-generation-agent linkedin cv/your_resume.md
```

**What it does**:
- Validates resume structure and formatting
- Checks for missing sections or inconsistencies
- Creates LinkedIn posts highlighting your skills and experience
- Generates professional bio variations

### 🔒 **Monthly Project Health Check**
**Problem**: "I want to make sure my project doesn't have security vulnerabilities or outdated dependencies"

**Solution**:
```bash
# Comprehensive health and security scan
run-workflow maintenance-check
```

**What it does**:
- Scans for security vulnerabilities in dependencies
- Checks for outdated packages that need updates
- Analyzes project health metrics
- Provides prioritized recommendations

### 📚 **Documentation Maintenance**
**Problem**: "My documentation probably has broken links and outdated information"

**Solution**:
```bash
# Update and validate all documentation
run-agent documentation-agent update
```

**What it does**:
- Validates all links in documentation files
- Updates cross-references and table of contents
- Checks for missing documentation sections
- Ensures documentation structure is consistent

---

## Understanding the Output

### ✅ **Success Output Example**
```
🔄 Workflow: code-quality-check
Status: ✅ completed
Duration: 15.3s
2 agents executed

Agent Results:
  ✅ code-quality-agent: success (12.1s)
  ✅ documentation-agent: success (3.2s)
```

**What this means**:
- The workflow completed successfully
- It took about 15 seconds total
- Both agents (code quality and documentation) finished without errors

### ⚠️ **Issues Found Example**
```
🔄 Agent: code-quality-agent
Status: ✅ success
Quality Score: 75/100
Issues Found: 3

Recommendations:
• Add more comments to explain complex logic in utils.py
• Reduce complexity in calculate_metrics function
• Fix inconsistent indentation in data_processor.py
```

**What this means**:
- Your code quality is good (75/100) but could be better
- There are 3 specific issues to address
- Each recommendation tells you exactly what to fix and where

### ❌ **Error Example**
```
❌ Agent: maintenance-agent
Error: Failed to scan dependencies
Available commands: run-agent, run-workflow, list-agents
```

**What this means**:
- Something went wrong with the maintenance scan
- The error message tells you what failed
- You can try running it again or check the specific issue

---

## Step-by-Step Workflows

### 🎯 **Weekly Code Quality Routine**

**Goal**: Maintain high code quality and up-to-date documentation

**Steps**:
1. **Check current status**:
   ```bash
   list-agents
   ```

2. **Run comprehensive quality check**:
   ```bash
   run-workflow code-quality-check
   ```

3. **Address any issues found** (the output will tell you exactly what to fix)

4. **Verify improvements**:
   ```bash
   run-agent code-quality-agent analyze *.py
   ```

**Time Investment**: 5-10 minutes  
**Frequency**: Weekly or before major commits

### 💼 **Resume and Content Creation**

**Goal**: Update resume and create professional content for LinkedIn

**Steps**:
1. **Update your resume** (edit the markdown file manually)

2. **Validate the resume format**:
   ```bash
   run-agent resume-processing-agent validate cv/your_resume.md
   ```

3. **Fix any formatting issues** (the output will tell you what's wrong)

4. **Generate LinkedIn content**:
   ```bash
   run-agent content-generation-agent linkedin cv/your_resume.md
   ```

5. **Create professional bio variations**:
   ```bash
   run-agent content-generation-agent bio cv/your_resume.md
   ```

**Time Investment**: 10-15 minutes  
**Frequency**: Monthly or when updating resume

### 🔒 **Monthly Security and Maintenance**

**Goal**: Keep project secure and dependencies up-to-date

**Steps**:
1. **Run comprehensive maintenance check**:
   ```bash
   run-workflow maintenance-check
   ```

2. **Review security findings** and update dependencies as recommended

3. **Verify documentation is current**:
   ```bash
   run-agent documentation-agent update
   ```

**Time Investment**: 15-20 minutes  
**Frequency**: Monthly

---

## Tips for Success

### 🎯 **Start Small**
- Begin with single agent commands before trying workflows
- Focus on one area at a time (code quality, then documentation, etc.)
- Don't try to fix everything at once

### 📅 **Make it Routine**
- Run `run-workflow code-quality-check` before every major commit
- Schedule monthly maintenance checks
- Update resume and generate content quarterly

### 🔍 **Read the Output**
- The agents provide specific, actionable recommendations
- Each issue includes the file name and line number where relevant
- "Success" doesn't always mean "perfect" - check the scores and recommendations

### ⚡ **Batch Similar Tasks**
- Use workflows instead of individual agents when possible
- Process multiple files at once (e.g., `*.py` for all Python files)
- Group related activities (code quality + documentation updates)

### 🆘 **When Things Go Wrong**
- Check that file paths are correct (use relative paths from project root)
- Ensure you're in the right directory when running commands
- If an agent fails, try running it individually to see specific error messages

---

## Command Reference Card

### 📋 **Essential Commands**
```bash
# See what's available
list-agents
list-workflows

# Check agent status
agent-status code-quality-agent

# Run single agent
run-agent <agent-name> <action> <target>

# Run complete workflow
run-workflow <workflow-name>
```

### 🎯 **Most Useful Commands**
```bash
# Complete quality check
run-workflow code-quality-check

# Analyze Python code
run-agent code-quality-agent analyze *.py

# Validate resume
run-agent resume-processing-agent validate cv/resume.md

# Generate LinkedIn content
run-agent content-generation-agent linkedin cv/resume.md

# Security and maintenance check
run-workflow maintenance-check

# Update documentation
run-agent documentation-agent update
```

### 🔧 **Troubleshooting Commands**
```bash
# Check if agents are working
list-agents

# Check specific agent status
agent-status maintenance-agent

# Test with simple command
run-agent code-quality-agent --help
```

---

## Frequently Asked Questions

### ❓ **"How do I know if it's working?"**
Run `list-agents` - you should see 5 agents listed. If you see an error, check the installation instructions.

### ❓ **"What files can the agents analyze?"**
- **Code Quality Agent**: Python (*.py), Batch scripts (*.bat), CSS (*.css), Markdown (*.md)
- **Documentation Agent**: All markdown files (*.md), README files
- **Resume Processing Agent**: Resume markdown files (typically in cv/ folder)
- **Content Generation Agent**: Resume markdown files
- **Maintenance Agent**: Package files (requirements.txt, package.json, etc.)

### ❓ **"How long does it take?"**
- Single agent: 5-30 seconds depending on project size
- Complete workflow: 30 seconds to 2 minutes
- Most operations complete in under 1 minute

### ❓ **"Will it change my files?"**
- **Read-only agents** (code-quality, maintenance): Only analyze, never modify
- **Update agents** (documentation): May update documentation files with fixes
- **Generation agents** (content-generation): Create new files in `generated-content/` folder
- Your source code is never automatically modified

### ❓ **"What if I don't like the recommendations?"**
All recommendations are suggestions. You decide what to implement. The agents provide guidance, not requirements.

### ❓ **"Can I customize what the agents check?"**
Yes! Each agent has a configuration file in `.agent-os/sub-agents/configurations/` that you can modify. See the main README.md for details.

### ❓ **"Is it secure?"**
Yes. All agents run in a secure sandbox that:
- Only accesses your project files
- Cannot modify system files
- Logs all activities for audit
- Cannot access external networks without permission

---

## Next Steps

### 🚀 **Once You're Comfortable**
1. **Explore Advanced Workflows**: Look at `examples/workflow_examples.py` for complex scenarios
2. **Customize Agent Behavior**: Edit configuration files to match your preferences  
3. **Create Custom Workflows**: Combine agents in new ways for your specific needs
4. **Integrate with CI/CD**: Run quality checks automatically on every commit

### 📚 **Additional Resources**
- **Complete Documentation**: See `README.md` for technical details
- **Example Scripts**: Check `examples/` folder for practical usage patterns
- **Configuration Guide**: Learn to customize agent behavior
- **Troubleshooting**: Detailed problem-solving guide in README.md

### 🤝 **Getting Help**
- **Command Help**: Use `--help` flag with any command
- **Agent Status**: Check `agent-status <agent-name>` for diagnostic info
- **Documentation**: All documentation is in `.agent-os/sub-agents/` folder
- **Examples**: Run the example scripts to see how everything works

---

**Remember**: The sub-agents are here to help you maintain better code quality and create professional content more efficiently. Start with simple commands, build confidence, and gradually incorporate them into your regular workflow. You'll be surprised how much time and effort they save!