# Sub-Agents Quick Reference

## 🚀 **What This Does**
Automatically improve your code, documentation, and professional content with simple commands.

## ⚡ **Most Important Commands**

### 📋 **Check Code Quality**
```bash
run-workflow code-quality-check
```
*Analyzes your code and documentation for issues and improvements*

### 💼 **Process Resume** 
```bash
run-agent resume-processing-agent validate cv/your_resume.md
```
*Validates your resume format and structure*

### 📱 **Create LinkedIn Content**
```bash
run-agent content-generation-agent linkedin cv/your_resume.md
```
*Generates LinkedIn posts from your resume*

### 🔒 **Security Check**
```bash
run-workflow maintenance-check
```
*Scans for security issues and outdated dependencies*

### 📚 **Fix Documentation**
```bash
run-agent documentation-agent update
```
*Updates and validates all documentation*

## 🎯 **Quick Start (30 seconds)**

1. **See what's available:**
   ```bash
   list-agents
   ```

2. **Run your first check:**
   ```bash
   run-workflow code-quality-check
   ```

3. **Done!** Read the output for specific recommendations.

## ✅ **What Success Looks Like**
```
✅ Workflow: code-quality-check
Status: ✅ completed
Duration: 15.3s
Quality Score: 85/100
```

## ⚠️ **What Issues Look Like**
```
Issues Found: 3
• Add comments to utils.py line 45
• Fix indentation in data.py line 12
• Reduce complexity in calc.py line 78
```

## 🆘 **If Something Goes Wrong**
1. Check you're in the project root directory
2. Try: `list-agents` to verify everything is working
3. Run individual agents instead of workflows
4. Check file paths are correct (use relative paths)

## 📋 **Available Agents**
- **code-quality-agent**: Reviews code for quality and style
- **documentation-agent**: Maintains and updates documentation  
- **resume-processing-agent**: Validates resume format and content
- **content-generation-agent**: Creates LinkedIn posts and bios
- **maintenance-agent**: Monitors security and project health

## 🔧 **Workflow Templates**

### **Before Every Commit**
```bash
run-workflow code-quality-check
# Fix any issues reported
# Commit your code
```

### **Monthly Maintenance**
```bash
run-workflow maintenance-check
# Review and update dependencies
```

### **Resume Updates**
```bash
# 1. Edit your resume file
# 2. Validate it:
run-agent resume-processing-agent validate cv/your_resume.md
# 3. Generate content:
run-agent content-generation-agent linkedin cv/your_resume.md
```

## 💡 **Pro Tips**
- Start with `list-agents` to see what's available
- Use workflows (run multiple agents) instead of single agents when possible
- Read the output carefully - it tells you exactly what to fix
- Run quality checks before committing code
- The agents never modify your source code without permission

## 📞 **Need More Help?**
- **Detailed Guide**: See `GETTING_STARTED.md`
- **Full Documentation**: See `README.md`
- **Examples**: Check `examples/` folder
- **Troubleshooting**: All common issues covered in main docs

---
*This is your AI-powered assistant team - use them to save time and improve quality!*