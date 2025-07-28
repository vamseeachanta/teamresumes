#!/usr/bin/env python3
"""
Resume Processing Agent Implementation
Validates resume markdown format, ensures PDF generation quality, and maintains professional content standards
"""

import re
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeIssue:
    """Represents a resume validation issue"""
    
    def __init__(self, file_path: str, line_number: int, severity: str, 
                 issue_type: str, message: str, suggestion: str = ""):
        self.file_path = file_path
        self.line_number = line_number
        self.severity = severity  # critical, important, minor
        self.issue_type = issue_type
        self.message = message
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'severity': self.severity,
            'type': self.issue_type,
            'message': self.message,
            'suggestion': self.suggestion
        }


class ResumeValidator:
    """Validates resume markdown format and structure"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.issues = []
    
    def validate_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Validate a resume markdown file"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            self._validate_structure(lines, file_path)
            self._validate_contact_information(lines, file_path)
            self._validate_required_sections(lines, file_path)
            self._validate_formatting_consistency(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error validating resume {file_path}: {e}")
            self.issues.append(ResumeIssue(
                file_path, 1, "critical", "validation_error",
                f"Could not validate resume: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _validate_structure(self, lines: List[str], file_path: str):
        """Validate basic resume structure"""
        
        # Check for name header (H1)
        has_name_header = False
        first_line_content = None
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('# '):
                has_name_header = True
                first_line_content = line.strip()[2:].strip()
                break
            elif line.strip() and not first_line_content:
                first_line_content = line.strip()
        
        if not has_name_header:
            self.issues.append(ResumeIssue(
                file_path, 1, "important", "missing_name_header",
                "Resume should start with name as H1 heading (# Name)",
                "Add your full name as the first H1 heading"
            ))
        
        # Check for professional title/subtitle
        has_subtitle = False
        content = '\n'.join(lines)
        
        # Look for bold subtitle after name
        if re.search(r'#\s+[^#\n]+\n\s*\*\*[^*]+\*\*', content):
            has_subtitle = True
        
        if not has_subtitle and has_name_header:
            self.issues.append(ResumeIssue(
                file_path, 2, "minor", "missing_professional_title",
                "Consider adding a professional title below your name",
                "Add your job title in bold: **Software Engineer**"
            ))
    
    def _validate_contact_information(self, lines: List[str], file_path: str):
        """Validate contact information format and completeness"""
        
        content = '\n'.join(lines)
        
        # Check for email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        
        if not emails:
            self.issues.append(ResumeIssue(
                file_path, 1, "important", "missing_contact_email",
                "Resume should include a professional email address",
                "Add your email in contact section: 📧 your.email@domain.com"
            ))
        else:
            # Validate email quality
            for email in emails:
                if any(unprofessional in email.lower() for unprofessional in 
                      ['123', 'abc', 'test', 'temp', 'sexy', 'cool', 'hot']):
                    self.issues.append(ResumeIssue(
                        file_path, 1, "minor", "unprofessional_email",
                        f"Email '{email}' may appear unprofessional",
                        "Consider using firstname.lastname@domain.com format"
                    ))
        
        # Check for phone number
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}-\d{4}',  # (555) 123-4567
            r'\d{3}-\d{3}-\d{4}',        # 555-123-4567
            r'\+\d{1,3}\s*\d{3}\s*\d{3}\s*\d{4}',  # +1 555 123 4567
            r'\d{3}\.\d{3}\.\d{4}'       # 555.123.4567
        ]
        
        has_phone = any(re.search(pattern, content) for pattern in phone_patterns)
        
        if not has_phone:
            self.issues.append(ResumeIssue(
                file_path, 1, "minor", "missing_contact_phone",
                "Consider including a phone number",
                "Add phone number: 📱 (555) 123-4567"
            ))
        
        # Check for LinkedIn profile
        linkedin_patterns = [
            r'linkedin\.com/in/[\w-]+',
            r'linkedin\.com/profile/[\w-]+',
            r'linkedin\.com[\w/.-]*'
        ]
        
        has_linkedin = any(re.search(pattern, content.lower()) for pattern in linkedin_patterns)
        
        if not has_linkedin:
            self.issues.append(ResumeIssue(
                file_path, 1, "minor", "missing_linkedin",
                "Consider including LinkedIn profile",
                "Add LinkedIn: 🌐 linkedin.com/in/yourprofile"
            ))
    
    def _validate_required_sections(self, lines: List[str], file_path: str):
        """Validate presence of required resume sections"""
        
        content = '\n'.join(lines).lower()
        
        required_sections = {
            'professional_experience': ['professional experience', 'work experience', 'experience'],
            'skills': ['skills', 'technical skills', 'core competencies'],
            'education': ['education', 'academic background', 'qualifications']
        }
        
        for section_name, keywords in required_sections.items():
            found = any(keyword in content for keyword in keywords)
            
            if not found:
                self.issues.append(ResumeIssue(
                    file_path, 1, "important", f"missing_section_{section_name}",
                    f"Resume is missing {section_name.replace('_', ' ').title()} section",
                    f"Add ## {section_name.replace('_', ' ').title()} section with relevant content"
                ))
        
        # Check for empty sections and poor experience formatting
        for i, line in enumerate(lines):
            if line.strip().startswith('## '):
                section_name = line.strip()[3:].strip()
                
                # Look for content until next H2 section
                content_found = False
                section_content = []
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith('## '):  # Only H2 sections, not H3 or deeper
                        break
                    if lines[j].strip():  # Non-empty line
                        content_found = True
                        section_content.append(lines[j].strip())
                
                if not content_found:
                    self.issues.append(ResumeIssue(
                        file_path, i + 1, "important", "empty_section",
                        f"Section '{section_name}' appears to be empty",
                        "Add relevant content to this section"
                    ))
                
                # Check for poor experience formatting
                if 'experience' in section_name.lower():
                    self._validate_experience_section_content(section_content, file_path, i + 1)
    
    def _validate_experience_section_content(self, content_lines: List[str], file_path: str, start_line: int):
        """Validate experience section content for proper formatting"""
        
        # Check for vague job descriptions
        vague_phrases = ['did some work', 'worked on', 'helped with', 'was awesome', 'made things']
        
        for i, line in enumerate(content_lines):
            for phrase in vague_phrases:
                if phrase in line.lower():
                    self.issues.append(ResumeIssue(
                        file_path, start_line + i, "minor", "vague_experience_description",
                        f"Experience description contains vague phrase: '{phrase}'",
                        "Use specific, quantified achievements instead of vague descriptions"
                    ))
        
        # Check for missing date formats
        date_pattern = r'\b(19|20)\d{2}\b|\b\d{1,2}/\d{4}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(19|20)\d{2}\b'
        has_dates = any(re.search(date_pattern, line, re.IGNORECASE) for line in content_lines)
        
        if not has_dates and len(content_lines) > 2:
            self.issues.append(ResumeIssue(
                file_path, start_line, "minor", "missing_experience_dates",
                "Experience section appears to be missing employment dates",
                "Add date ranges for employment periods (e.g., 'January 2020 - Present')"
            ))
    
    def _validate_formatting_consistency(self, lines: List[str], file_path: str):
        """Validate formatting consistency throughout resume"""
        
        # Check heading hierarchy
        heading_levels = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                level = len(line.strip()) - len(line.strip().lstrip('#'))
                heading_levels.append((i, level))
        
        # Validate heading progression
        for i in range(1, len(heading_levels)):
            prev_line, prev_level = heading_levels[i-1]
            curr_line, curr_level = heading_levels[i]
            
            if curr_level > prev_level + 1:
                self.issues.append(ResumeIssue(
                    file_path, curr_line, "minor", "heading_hierarchy_skip",
                    f"Heading skips from H{prev_level} to H{curr_level}",
                    "Use consecutive heading levels (H1, H2, H3, etc.)"
                ))
        
        # Check for consistent bullet point formatting
        bullet_patterns = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('+ '):
                bullet_patterns.append((i, stripped[0]))
        
        if bullet_patterns:
            primary_bullet = max(set(pattern[1] for pattern in bullet_patterns), 
                               key=lambda x: sum(1 for p in bullet_patterns if p[1] == x))
            
            inconsistent_bullets = [p for p in bullet_patterns if p[1] != primary_bullet]
            
            if inconsistent_bullets:
                for line_num, bullet_char in inconsistent_bullets[:3]:  # Report first 3
                    self.issues.append(ResumeIssue(
                        file_path, line_num, "minor", "inconsistent_bullet_formatting",
                        f"Inconsistent bullet point character '{bullet_char}'",
                        f"Use consistent bullet points: '{primary_bullet}'"
                    ))


class SkillsValidator:
    """Validates skills section formatting and organization"""
    
    def __init__(self):
        self.technical_skills = {
            'programming_languages', 'frameworks', 'databases', 'tools', 
            'technologies', 'platforms', 'operating_systems', 'cloud_services'
        }
        
        self.soft_skills = {
            'communication', 'leadership', 'teamwork', 'problem_solving',
            'analytical', 'creative', 'organizational', 'management'
        }
    
    def validate_skills_section(self, file_path: str) -> List[Dict[str, Any]]:
        """Validate skills section formatting"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            skills_section = self._extract_skills_section(lines)
            
            if skills_section:
                # Check for categorized vs uncategorized skills
                if self._is_uncategorized_list(skills_section):
                    issues.append({
                        'file_path': file_path,
                        'line_number': 1,
                        'severity': 'minor',
                        'type': 'skills_organization',
                        'message': 'Skills appear to be in a single list rather than categorized',
                        'suggestion': 'Consider organizing skills by category (e.g., Programming Languages, Frameworks, Tools)'
                    })
                
                # Check for proper formatting
                formatting_issues = self._check_skills_formatting(skills_section, file_path)
                issues.extend(formatting_issues)
                
        except Exception as e:
            logger.error(f"Error validating skills in {file_path}: {e}")
        
        return issues
    
    def analyze_skills_categories(self, file_path: str) -> Dict[str, List[str]]:
        """Analyze and categorize skills found in resume"""
        categories = {'technical': [], 'soft': [], 'other': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Extract potential skills
            skills_text = self._extract_skills_section(content.split('\n'))
            if skills_text:
                potential_skills = re.findall(r'\b[A-Za-z][A-Za-z\s.+#-]{2,20}\b', skills_text)
                
                for skill in potential_skills:
                    skill = skill.strip()
                    if any(tech in skill.lower() for tech in 
                          ['python', 'javascript', 'java', 'react', 'django', 'sql', 'aws', 'git']):
                        categories['technical'].append(skill)
                    elif any(soft in skill.lower() for soft in 
                           ['communication', 'leadership', 'teamwork', 'problem']):
                        categories['soft'].append(skill)
                    else:
                        categories['other'].append(skill)
                        
        except Exception as e:
            logger.error(f"Error analyzing skills categories in {file_path}: {e}")
        
        return categories
    
    def _extract_skills_section(self, lines: List[str]) -> str:
        """Extract the skills section content"""
        in_skills_section = False
        skills_content = []
        
        for line in lines:
            if re.match(r'^##\s+skills', line.strip(), re.IGNORECASE):
                in_skills_section = True
                continue
            elif in_skills_section and line.strip().startswith('##'):
                break
            elif in_skills_section:
                skills_content.append(line)
        
        return '\n'.join(skills_content)
    
    def _is_uncategorized_list(self, skills_text: str) -> bool:
        """Check if skills are in a single uncategorized list"""
        # Look for comma-separated list or simple bullet points
        comma_separated = ',' in skills_text and not re.search(r'\*\*[^*]+\*\*:', skills_text)
        simple_bullets = re.search(r'^[-*+]\s+[^*\n]+(,|\n[-*+])', skills_text, re.MULTILINE)
        
        return comma_separated or bool(simple_bullets)
    
    def _check_skills_formatting(self, skills_text: str, file_path: str) -> List[Dict[str, Any]]:
        """Check skills formatting issues"""
        issues = []
        
        # Check for proper categorization format
        if '**' not in skills_text and ':' not in skills_text:
            issues.append({
                'file_path': file_path,
                'line_number': 1,
                'severity': 'minor',
                'type': 'skills_formatting',
                'message': 'Skills section lacks clear categorization formatting',
                'suggestion': 'Use bold categories: **Programming Languages:** Python, JavaScript'
            })
        
        # Check for "etc." or similar lazy endings
        if re.search(r'\betc\.?\b|\band more\b|\band others\b', skills_text.lower()):
            issues.append({
                'file_path': file_path,
                'line_number': 1,
                'severity': 'minor',
                'type': 'vague_skills_ending',
                'message': 'Skills section contains vague endings like "etc." or "and more"',
                'suggestion': 'List specific skills instead of using vague terms'
            })
        
        return issues


class PDFGenerationQA:
    """Quality assurance for PDF generation process"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
    
    def check_generation_requirements(self, file_path: str) -> Dict[str, bool]:
        """Check if all requirements for PDF generation are met"""
        requirements = {}
        
        # Check for pandoc
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            requirements['pandoc_available'] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            requirements['pandoc_available'] = False
        
        # Check for wkhtmltopdf
        try:
            result = subprocess.run(['wkhtmltopdf', '--version'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            requirements['wkhtmltopdf_available'] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            requirements['wkhtmltopdf_available'] = False
        
        # Check for CSS stylesheet
        css_files = list(self.project_root.rglob('*.css'))
        requirements['css_stylesheet'] = len(css_files) > 0
        
        # Check file readability
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            requirements['file_readable'] = len(content.strip()) > 0
        except Exception:
            requirements['file_readable'] = False
        
        return requirements
    
    def get_validation_criteria(self) -> List[str]:
        """Get list of PDF validation criteria"""
        return [
            'page_formatting',
            'font_consistency', 
            'content_completeness',
            'layout_quality',
            'proper_margins',
            'readable_font_size',
            'professional_appearance'
        ]
    
    def validate_pdf_output(self, pdf_path: str) -> Dict[str, Any]:
        """Validate PDF output quality (placeholder for actual PDF analysis)"""
        # This would be expanded with actual PDF analysis using libraries like PyPDF2
        validation_results = {
            'file_exists': Path(pdf_path).exists(),
            'file_size_reasonable': False,
            'pages_count': 0,
            'text_extractable': False,
            'formatting_preserved': False
        }
        
        if validation_results['file_exists']:
            try:
                file_size = Path(pdf_path).stat().st_size
                validation_results['file_size_reasonable'] = 1000 < file_size < 10000000  # 1KB to 10MB
            except Exception:
                pass
        
        return validation_results


class ContentQualityAnalyzer:
    """Analyzes resume content quality and professionalism"""
    
    def __init__(self):
        self.unprofessional_words = {
            'awesome', 'cool', 'stuff', 'things', 'whatever', 'kinda', 'sorta',
            'pretty good', 'really good', 'super', 'very', 'extremely'
        }
        
        self.vague_terms = {
            'various', 'multiple', 'many', 'several', 'some', 'different',
            'numerous', 'a lot of', 'plenty of'
        }
        
        self.action_verbs = {
            'developed', 'implemented', 'designed', 'created', 'built', 'managed',
            'led', 'optimized', 'improved', 'increased', 'reduced', 'achieved',
            'delivered', 'executed', 'coordinated', 'established', 'maintained'
        }
    
    def analyze_language_quality(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze professional language and tone"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                lines = content.split('\n')
            
            # Check for unprofessional language
            for i, line in enumerate(lines, 1):
                for word in self.unprofessional_words:
                    if word in line.lower():
                        issues.append({
                            'file_path': file_path,
                            'line_number': i,
                            'severity': 'minor',
                            'type': 'unprofessional_language',
                            'message': f"Line contains unprofessional word: '{word}'",
                            'suggestion': f"Replace '{word}' with more professional language"
                        })
            
            # Check for first person pronouns
            first_person_pattern = r'\b(i|me|my|myself)\b'
            for i, line in enumerate(lines, 1):
                if re.search(first_person_pattern, line.lower()):
                    issues.append({
                        'file_path': file_path,
                        'line_number': i,
                        'severity': 'minor',
                        'type': 'first_person_usage',
                        'message': 'Resume contains first-person pronouns',
                        'suggestion': 'Use third-person or omit pronouns for professional tone'
                    })
                    break  # Only report once
                        
        except Exception as e:
            logger.error(f"Error analyzing language quality in {file_path}: {e}")
        
        return issues
    
    def analyze_achievement_quantification(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze if achievements are properly quantified"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Look for bullet points that might be achievements
            achievement_lines = []
            for i, line in enumerate(lines, 1):
                if re.match(r'^\s*[-*+]\s+', line):
                    achievement_lines.append((i, line.strip()))
            
            # Check for quantification
            quantified_count = 0
            for line_num, line in achievement_lines:
                # Look for numbers, percentages, timeframes
                has_metrics = bool(re.search(r'\b\d+[%$]?|\b\d+\s*(million|thousand|billion|k)\b|\b\d+x\b', line.lower()))
                
                if has_metrics:
                    quantified_count += 1
                else:
                    # Check if it's a vague achievement
                    if any(vague in line.lower() for vague in self.vague_terms):
                        issues.append({
                            'file_path': file_path,
                            'line_number': line_num,
                            'severity': 'minor',
                            'type': 'vague_achievement',
                            'message': 'Achievement lacks specific details or metrics',
                            'suggestion': 'Add specific numbers, percentages, or timeframes to quantify impact'
                        })
            
            # Overall quantification assessment
            if achievement_lines and quantified_count / len(achievement_lines) < 0.3:
                issues.append({
                    'file_path': file_path,
                    'line_number': 1,
                    'severity': 'minor',
                    'type': 'low_quantification_rate',
                    'message': f'Only {quantified_count}/{len(achievement_lines)} achievements are quantified',
                    'suggestion': 'Add metrics to more achievements (aim for 50%+ quantified)'
                })
                
        except Exception as e:
            logger.error(f"Error analyzing achievement quantification in {file_path}: {e}")
        
        return issues
    
    def analyze_content_completeness(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze content completeness and depth"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for very short sections
            current_section = None
            section_content = []
            
            for line in lines:
                if line.strip().startswith('## '):
                    # Process previous section
                    if current_section and len(section_content) < 2:
                        issues.append({
                            'file_path': file_path,
                            'line_number': 1,
                            'severity': 'minor',
                            'type': 'brief_section_content',
                            'message': f"Section '{current_section}' appears very brief",
                            'suggestion': f"Consider adding more detail to the {current_section} section"
                        })
                    
                    current_section = line.strip()[3:].strip()
                    section_content = []
                elif line.strip():
                    section_content.append(line)
            
            # Check final section
            if current_section and len(section_content) < 2:
                issues.append({
                    'file_path': file_path,
                    'line_number': 1,
                    'severity': 'minor',
                    'type': 'brief_section_content',
                    'message': f"Section '{current_section}' appears very brief",
                    'suggestion': f"Consider adding more detail to the {current_section} section"
                })
            
            # Check overall resume length
            non_empty_lines = [line for line in lines if line.strip()]
            if len(non_empty_lines) < 20:
                issues.append({
                    'file_path': file_path,
                    'line_number': 1,
                    'severity': 'minor',
                    'type': 'brief_resume_content',
                    'message': 'Resume appears quite brief overall',
                    'suggestion': 'Consider adding more detailed descriptions and achievements'
                })
                
        except Exception as e:
            logger.error(f"Error analyzing content completeness in {file_path}: {e}")
        
        return issues


class ResumeProcessingAgent:
    """Main resume processing agent that coordinates all analyzers"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.resume_validator = ResumeValidator(str(self.project_root))
        self.skills_validator = SkillsValidator()
        self.pdf_qa = PDFGenerationQA(str(self.project_root))
        self.content_analyzer = ContentQualityAnalyzer()
    
    def analyze_resume(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive resume analysis"""
        
        path = Path(file_path)
        results = {
            'file_path': file_path,
            'structure_issues': [],
            'skills_issues': [],
            'content_quality_issues': [],
            'pdf_generation_readiness': {},
            'overall_score': 0
        }
        
        # Only analyze markdown files
        if path.suffix.lower() != '.md':
            results['error'] = f"File type '{path.suffix}' is not supported. Only .md files are analyzed."
            return results
        
        try:
            # Structure validation
            results['structure_issues'] = self.resume_validator.validate_file(file_path)
            
            # Skills validation
            results['skills_issues'] = self.skills_validator.validate_skills_section(file_path)
            
            # Content quality analysis
            language_issues = self.content_analyzer.analyze_language_quality(file_path)
            quantification_issues = self.content_analyzer.analyze_achievement_quantification(file_path)
            completeness_issues = self.content_analyzer.analyze_content_completeness(file_path)
            
            results['content_quality_issues'] = language_issues + quantification_issues + completeness_issues
            
            # PDF generation readiness
            results['pdf_generation_readiness'] = self.pdf_qa.check_generation_requirements(file_path)
            
            # Calculate overall score
            results['overall_score'] = self._calculate_overall_score(results)
            
        except Exception as e:
            logger.error(f"Error analyzing resume {file_path}: {e}")
            results['error'] = f"Analysis failed: {e}"
        
        return results
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a formatted resume analysis report"""
        
        file_path = analysis_results.get('file_path', 'Unknown')
        report_lines = [f"# Resume Analysis Report: {Path(file_path).name}\\n"]
        
        if 'error' in analysis_results:
            report_lines.append(f"**Error:** {analysis_results['error']}\\n")
            return "\\n".join(report_lines)
        
        # Overall score
        score = analysis_results.get('overall_score', 0)
        report_lines.append(f"**Overall Quality Score:** {score}/100\\n")
        
        # Issue summary
        total_issues = (
            len(analysis_results.get('structure_issues', [])) +
            len(analysis_results.get('skills_issues', [])) +
            len(analysis_results.get('content_quality_issues', []))
        )
        
        report_lines.append(f"**Total Issues Found:** {total_issues}\\n")
        
        # Structure issues
        structure_issues = analysis_results.get('structure_issues', [])
        if structure_issues:
            report_lines.append("## Structure and Format Issues\\n")
            for issue in structure_issues:
                severity = issue.get('severity', 'unknown').title()
                message = issue.get('message', '')
                suggestion = issue.get('suggestion', '')
                
                report_lines.append(f"**{severity}:** {message}")
                if suggestion:
                    report_lines.append(f"  - *Suggestion:* {suggestion}")
                report_lines.append("")
        
        # Skills issues
        skills_issues = analysis_results.get('skills_issues', [])
        if skills_issues:
            report_lines.append("## Skills Section Issues\\n")
            for issue in skills_issues:
                severity = issue.get('severity', 'unknown').title()
                message = issue.get('message', '')
                suggestion = issue.get('suggestion', '')
                
                report_lines.append(f"**{severity}:** {message}")
                if suggestion:
                    report_lines.append(f"  - *Suggestion:* {suggestion}")
                report_lines.append("")
        
        # Content quality issues
        content_issues = analysis_results.get('content_quality_issues', [])
        if content_issues:
            report_lines.append("## Content Quality Issues\\n")
            for issue in content_issues:
                severity = issue.get('severity', 'unknown').title()
                message = issue.get('message', '')
                suggestion = issue.get('suggestion', '')
                
                report_lines.append(f"**{severity}:** {message}")
                if suggestion:
                    report_lines.append(f"  - *Suggestion:* {suggestion}")
                report_lines.append("")
        
        # PDF generation readiness
        pdf_readiness = analysis_results.get('pdf_generation_readiness', {})
        if pdf_readiness:
            report_lines.append("## PDF Generation Readiness\\n")
            for requirement, status in pdf_readiness.items():
                status_text = "PASS" if status else "FAIL"
                report_lines.append(f"- **{requirement.replace('_', ' ').title()}:** {status_text}")
            report_lines.append("")
        
        # Recommendations
        if total_issues > 0:
            report_lines.append("## Recommendations\\n")
            if score < 70:
                report_lines.append("- Focus on addressing critical and important issues first")
                report_lines.append("- Consider professional resume review or templates")
            elif score < 85:
                report_lines.append("- Address remaining formatting and content issues")
                report_lines.append("- Quantify more achievements with specific metrics")
            else:
                report_lines.append("- Minor polish and formatting improvements")
                report_lines.append("- Resume is in good shape overall")
            report_lines.append("")
        
        return "\\n".join(report_lines)
    
    def _calculate_overall_score(self, results: Dict[str, Any]) -> int:
        """Calculate overall quality score (0-100)"""
        
        base_score = 100
        
        # Deduct points for issues
        structure_issues = results.get('structure_issues', [])
        skills_issues = results.get('skills_issues', [])
        content_issues = results.get('content_quality_issues', [])
        
        # Severity-based deductions
        for issue in structure_issues + skills_issues + content_issues:
            severity = issue.get('severity', 'minor')
            if severity == 'critical':
                base_score -= 15
            elif severity == 'important':
                base_score -= 8
            elif severity == 'minor':
                base_score -= 3
        
        # PDF readiness bonus/penalty
        pdf_readiness = results.get('pdf_generation_readiness', {})
        ready_count = sum(1 for status in pdf_readiness.values() if status)
        total_requirements = len(pdf_readiness)
        
        if total_requirements > 0:
            readiness_ratio = ready_count / total_requirements
            if readiness_ratio < 0.5:
                base_score -= 10
            elif readiness_ratio == 1.0:
                base_score += 5
        
        return max(0, min(100, base_score))


def main():
    """Command-line interface for the resume processing agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze resume quality and format")
    parser.add_argument("file", help="Resume markdown file to analyze")
    parser.add_argument("--format", choices=["json", "report"], default="report",
                       help="Output format")
    
    args = parser.parse_args()
    
    agent = ResumeProcessingAgent()
    results = agent.analyze_resume(args.file)
    
    if args.format == "json":
        import json
        print(json.dumps(results, indent=2))
    else:
        report = agent.generate_report(results)
        print(report)


if __name__ == "__main__":
    main()