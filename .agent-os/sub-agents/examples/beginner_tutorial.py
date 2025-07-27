#!/usr/bin/env python3
"""
Beginner Tutorial for Sub-Agents System
Step-by-step walkthrough with explanations for new users
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_section(title, description=""):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    if description:
        print(f"   {description}")
    print("="*60)

def print_step(step_num, title, description=""):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {title}")
    if description:
        print(f"    {description}")
    print("-" * 40)

def wait_for_user(message="Press Enter to continue..."):
    """Wait for user input before proceeding"""
    input(f"\n⏸️  {message}")

def tutorial_introduction():
    """Introduction to the tutorial"""
    print_section("Welcome to Sub-Agents Tutorial!", 
                 "Learn how to use AI assistants to improve your code and content")
    
    print("""
🤖 What are Sub-Agents?
   Sub-agents are AI assistants that automatically:
   • Check your code quality and suggest improvements
   • Keep your documentation up-to-date  
   • Validate and process resume files
   • Generate LinkedIn content from your resume
   • Monitor your project for security issues

🎯 What you'll learn:
   1. How to see what assistants are available
   2. How to run your first quality check
   3. How to understand the results
   4. How to process resume files
   5. How to run automated workflows

⏱️  Time needed: About 10 minutes

💡 Tip: Don't worry about memorizing commands - we'll show you everything!
""")
    
    wait_for_user("Ready to start? Press Enter...")

def step_1_discover_agents():
    """Step 1: Discover available agents"""
    print_step(1, "Discover Your AI Assistants", 
              "Let's see what helpers are available")
    
    print("""
🔍 First, let's see what AI assistants are ready to help you.
   Think of this like checking what tools are in your toolbox.
""")
    
    try:
        from integration_handler import ClaudeCodeIntegration
        
        print("🤖 Running: list-agents")
        print("   (This shows all available AI assistants)")
        
        integration = ClaudeCodeIntegration()
        result = integration.execute_command('list-agents', {})
        
        if result.get('status') == 'success':
            agents = result.get('agents', [])
            print(f"\n✅ Found {len(agents)} AI assistants ready to help:")
            
            for i, agent in enumerate(agents, 1):
                print(f"\n   {i}. {agent['name']}")
                print(f"      What it does: {agent['specialization']}")
                print(f"      Status: {agent['status']} ✅")
            
            print(f"\n💡 Explanation:")
            print(f"   • Each assistant specializes in different tasks")
            print(f"   • All {len(agents)} assistants are active and ready to use")
            print(f"   • You can use them individually or together in workflows")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            print("   This might mean the system isn't set up correctly.")
    
    except Exception as e:
        print(f"❌ Error running example: {e}")
        print("   (This is just a demonstration - the actual commands work in your terminal)")
    
    wait_for_user("Understood? Let's try running an assistant...")

def step_2_first_agent():
    """Step 2: Run your first agent"""
    print_step(2, "Run Your First AI Assistant", 
              "Let's check your code quality")
    
    print("""
🎯 Now let's run the Code Quality Assistant to check your Python files.
   This is like having a senior developer review your code instantly!
""")
    
    try:
        from integration_handler import ClaudeCodeIntegration, ResultFormatter
        
        print("🤖 Running: run-agent code-quality-agent analyze *.py")
        print("   (This analyzes all Python files for quality and style)")
        
        integration = ClaudeCodeIntegration()
        result = integration.execute_command('run-agent', {
            'agent': 'code-quality-agent',
            'action': 'analyze',
            'target': '*.py'
        })
        
        formatter = ResultFormatter()
        
        if result.get('status') == 'success':
            formatted = formatter.format_agent_result(result)
            print(f"\n✅ Analysis Complete!")
            print(formatted)
            
            # Explain what this means
            print(f"\n💡 What this means:")
            print(f"   • Quality Score: Higher is better (0-100 scale)")
            print(f"   • Issues Found: Specific problems to fix")
            print(f"   • Recommendations: Exact steps to improve your code")
            print(f"   • Execution Time: How long the analysis took")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error running example: {e}")
        print("   (This is a demonstration - try the real command in your terminal)")
    
    print("""
🎓 What just happened:
   1. The AI assistant scanned all your Python files
   2. It checked for style issues, complexity problems, and best practices
   3. It gave you a quality score and specific recommendations
   4. All of this happened in just a few seconds!
""")
    
    wait_for_user("Makes sense? Let's try a complete workflow...")

def step_3_workflow():
    """Step 3: Run a complete workflow"""
    print_step(3, "Run a Complete Workflow", 
              "Multiple AI assistants working together")
    
    print("""
🚀 Workflows are like having multiple specialists work together.
   Instead of running one assistant at a time, a workflow runs several
   in the right order to complete a bigger task.
""")
    
    try:
        from integration_handler import ClaudeCodeIntegration, ResultFormatter
        
        print("🤖 Running: run-workflow code-quality-check")
        print("   (This runs multiple assistants: code quality + documentation)")
        
        integration = ClaudeCodeIntegration()
        result = integration.execute_command('run-workflow', {
            'workflow': 'code-quality-check',
            'context': {'project_path': '.'}
        })
        
        formatter = ResultFormatter()
        
        if result.get('status') in ['completed', 'partial_failure']:
            formatted = formatter.format_workflow_result(result)
            print(f"\n✅ Workflow Complete!")
            print(formatted)
            
            print(f"\n💡 What this workflow did:")
            print(f"   1. Code Quality Assistant: Analyzed all your code")
            print(f"   2. Documentation Assistant: Checked your documentation")
            print(f"   3. Coordination: Made sure they worked together properly")
            print(f"   4. Reporting: Gave you a summary of everything found")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error running example: {e}")
        print("   (This is a demonstration - try the real command in your terminal)")
    
    print("""
🎓 Why workflows are powerful:
   • Save time: One command does multiple tasks
   • Coordination: Assistants share information with each other  
   • Comprehensive: Get a complete picture of your project health
   • Consistent: Same thorough process every time
""")
    
    wait_for_user("Ready to learn about resume processing?")

def step_4_resume_processing():
    """Step 4: Resume processing example"""
    print_step(4, "Process Resume Files", 
              "Validate resumes and generate LinkedIn content")
    
    print("""
💼 The Resume Processing Assistant helps with professional documents.
   It can validate your resume format and even generate LinkedIn content!
""")
    
    try:
        from integration_handler import ClaudeCodeIntegration
        
        print("🤖 Example commands for resume processing:")
        print()
        print("   1. Validate resume format:")
        print("      run-agent resume-processing-agent validate cv/your_resume.md")
        print()
        print("   2. Generate LinkedIn content:")  
        print("      run-agent content-generation-agent linkedin cv/your_resume.md")
        print()
        print("   3. Create professional bio:")
        print("      run-agent content-generation-agent bio cv/your_resume.md")
        
        print(f"\n💡 What these commands do:")
        print(f"   • Validate: Checks resume structure, formatting, required sections")
        print(f"   • LinkedIn: Creates posts highlighting your skills and experience")
        print(f"   • Bio: Generates professional bio variations for different uses")
        
        # Show example output
        print(f"\n📄 Example output for resume validation:")
        print(f"   ✅ Resume structure: Valid")
        print(f"   ✅ Required sections: All present")  
        print(f"   ⚠️  Skills section: Could be more detailed")
        print(f"   📝 Recommendation: Add 2-3 more technical skills")
        
    except Exception as e:
        print(f"❌ Error in example: {e}")
    
    print("""
🎓 Resume processing benefits:
   • Professional quality: Ensures your resume meets standards
   • Content creation: Automatically generates social media content
   • Time savings: No manual formatting or content writing
   • Consistency: Same high standards applied every time
""")
    
    wait_for_user("Last step - let's learn about maintenance...")

def step_5_maintenance():
    """Step 5: Project maintenance"""
    print_step(5, "Project Maintenance & Security", 
              "Keep your project healthy and secure")
    
    print("""
🔒 The Maintenance Assistant monitors your project health.
   It's like having an IT security specialist checking your project regularly.
""")
    
    try:
        print("🤖 Example maintenance commands:")
        print()
        print("   1. Complete maintenance check:")
        print("      run-workflow maintenance-check")
        print()
        print("   2. Security scan only:")
        print("      run-agent maintenance-agent security-scan")
        print()
        print("   3. Check for updates:")
        print("      run-agent maintenance-agent update-check")
        
        print(f"\n💡 What maintenance checking finds:")
        print(f"   • Security vulnerabilities in dependencies")
        print(f"   • Outdated packages that need updates")
        print(f"   • Project health metrics and recommendations")
        print(f"   • Performance optimization opportunities")
        
        # Show example output
        print(f"\n🔍 Example maintenance report:")
        print(f"   🛡️  Security: 2 vulnerabilities found")
        print(f"   📦 Dependencies: 5 packages need updates")
        print(f"   📊 Health Score: 78/100")
        print(f"   ⚡ Recommendation: Update numpy to fix security issue")
        
    except Exception as e:
        print(f"❌ Error in example: {e}")
    
    print("""
🎓 Why maintenance matters:
   • Security: Protect against known vulnerabilities
   • Performance: Keep dependencies optimized  
   • Reliability: Prevent issues before they happen
   • Compliance: Meet security standards automatically
""")
    
    wait_for_user("Ready for the summary?")

def tutorial_summary():
    """Tutorial summary and next steps"""
    print_section("🎉 Congratulations!", 
                 "You've learned the essentials of sub-agents!")
    
    print("""
🎯 What you've learned:
   1. ✅ How to discover available AI assistants (list-agents)
   2. ✅ How to run individual assistants (run-agent)
   3. ✅ How to use workflows for complex tasks (run-workflow)
   4. ✅ How to process resumes and generate content
   5. ✅ How to maintain project health and security

🚀 Your essential commands:
   • list-agents                          (see what's available)
   • run-workflow code-quality-check      (check code + docs)
   • run-workflow maintenance-check       (security + health)
   • run-agent resume-processing-agent validate cv/resume.md
   • run-agent content-generation-agent linkedin cv/resume.md

💡 Pro tips for success:
   • Start with workflows - they do more with less effort
   • Read the output carefully - it tells you exactly what to fix
   • Run quality checks before committing code to GitHub
   • Use maintenance checks monthly to stay secure
   • Don't be afraid to experiment - the assistants won't break anything

📚 Next steps:
   1. Try these commands in your terminal (not just this tutorial)
   2. Read GETTING_STARTED.md for more detailed examples
   3. Check QUICK_REFERENCE.md for a handy command list
   4. Explore the examples/ folder for advanced usage

🎓 Remember:
   • These AI assistants are here to help, not replace your judgment
   • They provide recommendations - you decide what to implement
   • The more you use them, the more time they'll save you
   • Quality and security checks become automatic habits

🔗 Helpful resources:
   • Quick Reference: .agent-os/sub-agents/QUICK_REFERENCE.md
   • Complete Guide: .agent-os/sub-agents/GETTING_STARTED.md  
   • Technical Docs: .agent-os/sub-agents/README.md
   • More Examples: .agent-os/sub-agents/examples/
""")
    
    print("\n🎉 You're ready to use sub-agents like a pro!")
    print("   Go try some commands in your terminal!")

def main():
    """Run the complete beginner tutorial"""
    print("🎓 Sub-Agents Beginner Tutorial")
    print("   Learn to use AI assistants for code quality and content creation")
    
    # Run tutorial steps
    tutorial_introduction()
    step_1_discover_agents()
    step_2_first_agent()
    step_3_workflow()
    step_4_resume_processing()
    step_5_maintenance()
    tutorial_summary()

if __name__ == "__main__":
    main()