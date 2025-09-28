#!/usr/bin/env python
"""
Resume Slash Command - Quick access to resume management features
Usage: /resume [update|linkedin|team] [options]
"""

import sys
import os
from pathlib import Path

# Fix Windows Unicode issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Import the resume manager
sys.path.insert(0, str(Path(__file__).parent))
from resume_manager import ResumeManager

def main():
    """Main slash command handler"""
    manager = ResumeManager()
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command in ['update', 'u']:
        if len(sys.argv) < 3:
            print("❌ Please specify team member: va, gp, ss, or sp")
            return
        member = sys.argv[2].lower()
        section = sys.argv[3] if len(sys.argv) > 3 else None
        manager.update_resume(member, section)
    
    elif command in ['linkedin', 'l']:
        if len(sys.argv) < 3:
            print("❌ Please specify team member: va, gp, ss, or sp")
            return
        member = sys.argv[2].lower()
        sync_type = sys.argv[3] if len(sys.argv) > 3 else 'summary'
        manager.linkedin_sync(member, sync_type)
    
    elif command in ['team', 't']:
        format_type = sys.argv[2] if len(sys.argv) > 2 else 'pdf'
        manager.team_profile(format_type)
    
    elif command in ['list', 'ls']:
        print("\n👥 Team Members with Resumes:")
        for resume in manager.cv_dir.glob("*_resume.md"):
            member = resume.stem.replace('_resume', '')
            pdf_exists = resume.with_suffix('.pdf').exists()
            status = "✅" if pdf_exists else "⚠️"
            print(f"  {status} {member.upper()} - {'PDF ready' if pdf_exists else 'PDF needs update'}")
    
    elif command in ['help', 'h', '--help', '-h']:
        print_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

def print_help():
    """Print help information"""
    print("""
📝 Resume Manager - Claude Flow Integration
    
Usage: /resume [command] [options]

Commands:
  update <member> [section]  Update team member resume and generate PDF
  linkedin <member> [type]   Generate LinkedIn content (summary/skills/post)
  team [format]              Generate team capabilities overview
  list                       List all team members
  help                       Show this help message

Team Members:
  va - VA Resume
  gp - GP Resume
  ss - SS Resume  
  sp - SP Resume

Examples:
  /resume update va           # Update VA's resume and generate PDF
  /resume linkedin gp skills  # Generate LinkedIn skills for GP
  /resume team pdf            # Create team overview PDF
  /resume list                # List all team members

Shortcuts:
  u = update, l = linkedin, t = team, ls = list, h = help
""")

if __name__ == "__main__":
    main()