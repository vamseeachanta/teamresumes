#!/usr/bin/env python
"""
Resume Manager - Claude Flow Integration for TeamResumes
Manages team resumes with automated PDF generation and LinkedIn content creation
"""

import os
import sys
import subprocess
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class ResumeManager:
    """Manages resume operations with Claude Flow integration"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.cv_dir = self.root_dir / "cv"
        self.docs_dir = self.root_dir / "docs"
        self.config_file = self.root_dir / ".agent-os/claude-flow.yaml"
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load Claude Flow configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def update_resume(self, team_member: str, section: Optional[str] = None) -> bool:
        """Update a team member's resume"""
        print(f"\n📝 Updating resume for {team_member.upper()}...")
        
        resume_file = self.cv_dir / f"{team_member}_resume.md"
        if not resume_file.exists():
            print(f"❌ Resume file not found: {resume_file}")
            return False
        
        # Generate PDF
        if self.generate_pdf(resume_file):
            print(f"✅ PDF generated successfully")
        
        # Commit changes if enabled
        if self.config.get('integrations', {}).get('git', {}).get('auto_commit'):
            self.commit_changes(team_member)
        
        return True
    
    def generate_pdf(self, resume_file: Path) -> bool:
        """Generate PDF from markdown resume"""
        print(f"  📄 Generating PDF from {resume_file.name}...")
        
        output_file = resume_file.with_suffix('.pdf')
        stylesheet = self.root_dir / "resume-stylesheet.css"
        
        # Use pandoc for conversion
        cmd = [
            "pandoc",
            str(resume_file),
            "-o", str(output_file),
            "--css", str(stylesheet),
            "--pdf-engine=wkhtmltopdf"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ PDF saved to: {output_file.name}")
                return True
            else:
                print(f"  ❌ PDF generation failed: {result.stderr}")
                return False
        except FileNotFoundError:
            print("  ⚠️ pandoc not found. Using Python fallback...")
            return self.generate_pdf_python(resume_file)
    
    def generate_pdf_python(self, resume_file: Path) -> bool:
        """Generate PDF using Python libraries as fallback"""
        try:
            # Import the existing workflow script
            workflow_script = self.root_dir / "dev_tools/run_workflow_pdfkit.py"
            if workflow_script.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("workflow", workflow_script)
                workflow = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(workflow)
                
                # Run the workflow
                workflow.main()
                return True
            else:
                print(f"  ❌ Workflow script not found")
                return False
        except Exception as e:
            print(f"  ❌ Python PDF generation failed: {e}")
            return False
    
    def linkedin_sync(self, team_member: str, sync_type: str = "summary") -> bool:
        """Generate LinkedIn content from resume"""
        print(f"\n🔗 Generating LinkedIn {sync_type} for {team_member.upper()}...")
        
        resume_file = self.cv_dir / f"{team_member}_resume.md"
        if not resume_file.exists():
            print(f"❌ Resume file not found: {resume_file}")
            return False
        
        # Create LinkedIn directory if needed
        linkedin_dir = self.cv_dir / "linkedin"
        linkedin_dir.mkdir(exist_ok=True)
        
        # Read resume content
        with open(resume_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate content based on type
        if sync_type == "summary":
            output = self.generate_summary(content, team_member)
        elif sync_type == "skills":
            output = self.extract_skills(content, team_member)
        elif sync_type == "post":
            output = self.generate_post(content, team_member)
        else:
            print(f"❌ Unknown sync type: {sync_type}")
            return False
        
        # Save output
        output_file = linkedin_dir / f"{team_member}_{sync_type}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"✅ LinkedIn {sync_type} saved to: {output_file}")
        return True
    
    def generate_summary(self, content: str, team_member: str) -> str:
        """Generate LinkedIn summary from resume"""
        lines = content.split('\n')
        summary_lines = []
        
        # Extract key sections
        in_summary = False
        for line in lines:
            if '## Summary' in line or '## Professional Summary' in line:
                in_summary = True
                continue
            elif in_summary and line.startswith('##'):
                break
            elif in_summary and line.strip():
                summary_lines.append(line)
        
        # Create LinkedIn-formatted summary
        summary = f"# LinkedIn Summary for {team_member.upper()}\n\n"
        summary += "## Professional Summary\n\n"
        summary += '\n'.join(summary_lines[:5])  # Limit to 5 lines
        summary += "\n\n## Key Skills\n\n"
        summary += self.extract_skills_list(content)
        summary += f"\n\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d')}*"
        
        return summary
    
    def extract_skills(self, content: str, team_member: str) -> str:
        """Extract skills section for LinkedIn"""
        skills = self.extract_skills_list(content)
        
        output = f"# LinkedIn Skills for {team_member.upper()}\n\n"
        output += "## Technical Skills\n\n"
        output += skills
        output += "\n\n## Endorsements\n\n"
        output += "Request endorsements for these top skills:\n"
        
        # Get top 5 skills
        skill_items = skills.split('\n')[:5]
        for skill in skill_items:
            if skill.strip():
                output += f"- {skill.strip().lstrip('- ')}\n"
        
        return output
    
    def extract_skills_list(self, content: str) -> str:
        """Extract skills list from resume content"""
        lines = content.split('\n')
        skills = []
        
        in_skills = False
        for line in lines:
            if '## Skills' in line or '## Technical Skills' in line:
                in_skills = True
                continue
            elif in_skills and line.startswith('##'):
                break
            elif in_skills and line.strip():
                skills.append(line)
        
        return '\n'.join(skills[:10])  # Limit to 10 skills
    
    def generate_post(self, content: str, team_member: str) -> str:
        """Generate LinkedIn post from recent achievements"""
        template = self.config.get('templates', {}).get('linkedin_post', '')
        
        # Extract achievements
        achievements = self.extract_achievements(content)
        skills = self.extract_skills_list(content).split('\n')[:3]
        
        # Format post
        post = f"# LinkedIn Post for {team_member.upper()}\n\n"
        post += "## Suggested Post\n\n"
        post += "🚀 Professional Update\n\n"
        post += f"Excited to share my expertise in: {', '.join(s.strip('- ') for s in skills if s)}\n\n"
        
        if achievements:
            post += "Recent Achievements:\n"
            for achievement in achievements[:3]:
                post += f"• {achievement}\n"
        
        post += "\n#Engineering #Technology #Innovation #ProfessionalGrowth"
        
        return post
    
    def extract_achievements(self, content: str) -> List[str]:
        """Extract achievements from resume"""
        achievements = []
        lines = content.split('\n')
        
        for line in lines:
            # Look for achievement indicators
            if any(keyword in line.lower() for keyword in ['achieved', 'delivered', 'led', 'improved', 'reduced']):
                achievement = line.strip().lstrip('- •')
                if achievement:
                    achievements.append(achievement)
        
        return achievements[:5]  # Top 5 achievements
    
    def team_profile(self, format: str = "pdf") -> bool:
        """Generate team capabilities overview"""
        print(f"\n👥 Generating team profile in {format} format...")
        
        # Collect all resumes
        resumes = list(self.cv_dir.glob("*_resume.md"))
        if not resumes:
            print("❌ No resume files found")
            return False
        
        print(f"  Found {len(resumes)} team members")
        
        # Generate skills matrix
        skills_matrix = self.generate_skills_matrix(resumes)
        
        # Create overview document
        overview = "# Team Capabilities Overview\n\n"
        overview += f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        overview += "## Team Members\n\n"
        
        for resume in resumes:
            member = resume.stem.replace('_resume', '').upper()
            overview += f"- **{member}**: {self.get_member_title(resume)}\n"
        
        overview += "\n## Combined Skills Matrix\n\n"
        overview += skills_matrix
        
        # Save overview
        output_file = self.docs_dir / f"team_overview.{format if format != 'pdf' else 'md'}"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(overview)
        
        print(f"✅ Team overview saved to: {output_file}")
        
        # Convert to PDF if requested
        if format == "pdf":
            self.generate_pdf(output_file)
        
        return True
    
    def get_member_title(self, resume_file: Path) -> str:
        """Extract member title from resume"""
        with open(resume_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:10]:  # Check first 10 lines
                if 'Engineer' in line or 'Scientist' in line or 'Manager' in line:
                    return line.strip().lstrip('#').strip()
        return "Team Member"
    
    def generate_skills_matrix(self, resumes: List[Path]) -> str:
        """Generate skills matrix from all resumes"""
        all_skills = {}
        
        for resume in resumes:
            member = resume.stem.replace('_resume', '').upper()
            with open(resume, 'r', encoding='utf-8') as f:
                content = f.read()
                skills = self.extract_skills_list(content).split('\n')
                for skill in skills:
                    skill = skill.strip().lstrip('- ')
                    if skill:
                        if skill not in all_skills:
                            all_skills[skill] = []
                        all_skills[skill].append(member)
        
        # Format matrix
        matrix = "| Skill | Team Members |\n"
        matrix += "|-------|-------------|\n"
        
        for skill, members in sorted(all_skills.items()):
            matrix += f"| {skill} | {', '.join(members)} |\n"
        
        return matrix
    
    def commit_changes(self, team_member: str) -> bool:
        """Commit resume changes to git"""
        print(f"  📤 Committing changes for {team_member}...")
        
        try:
            # Add files
            subprocess.run(["git", "add", f"cv/{team_member}_resume.*"], cwd=self.root_dir)
            
            # Commit
            message = f"docs: Update {team_member.upper()} resume"
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  ✅ Changes committed")
                return True
            else:
                print(f"  ℹ️ No changes to commit")
                return False
        except Exception as e:
            print(f"  ❌ Git commit failed: {e}")
            return False

def main():
    """Main entry point for resume manager"""
    parser = argparse.ArgumentParser(description="Resume Manager - Claude Flow Integration")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Update resume command
    update_parser = subparsers.add_parser('update', help='Update a team member resume')
    update_parser.add_argument('member', choices=['va', 'gp', 'ss', 'sp'], 
                              help='Team member code')
    update_parser.add_argument('--section', choices=['experience', 'skills', 'education'],
                              help='Specific section to update')
    
    # LinkedIn sync command
    linkedin_parser = subparsers.add_parser('linkedin', help='Generate LinkedIn content')
    linkedin_parser.add_argument('member', choices=['va', 'gp', 'ss', 'sp'],
                                help='Team member code')
    linkedin_parser.add_argument('--type', choices=['summary', 'skills', 'post'],
                                default='summary', help='Content type to generate')
    
    # Team profile command
    team_parser = subparsers.add_parser('team', help='Generate team profile')
    team_parser.add_argument('--format', choices=['pdf', 'markdown', 'html'],
                            default='pdf', help='Output format')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List team members')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = ResumeManager()
    
    # Execute command
    if args.command == 'update':
        manager.update_resume(args.member, args.section)
    elif args.command == 'linkedin':
        manager.linkedin_sync(args.member, args.type)
    elif args.command == 'team':
        manager.team_profile(args.format)
    elif args.command == 'list':
        print("\n👥 Team Members:")
        for resume in manager.cv_dir.glob("*_resume.md"):
            member = resume.stem.replace('_resume', '')
            print(f"  - {member.upper()}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()