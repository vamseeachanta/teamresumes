#!/usr/bin/env python3
"""
Content Generation Agent Implementation
Generates LinkedIn posts, professional bios, and social media content from resume data
"""

import re
import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerationIssue:
    """Represents a content generation issue or suggestion"""
    
    def __init__(self, content_type: str, severity: str, 
                 issue_type: str, message: str, suggestion: str = ""):
        self.content_type = content_type
        self.severity = severity  # info, warning, error
        self.issue_type = issue_type
        self.message = message
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'content_type': self.content_type,
            'severity': self.severity,
            'type': self.issue_type,
            'message': self.message,
            'suggestion': self.suggestion
        }


class ResumeDataExtractor:
    """Extracts structured data from resume markdown"""
    
    def __init__(self):
        self.data = {}
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extract structured data from resume file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Extract basic info
            self.data = {
                'name': self._extract_name(lines),
                'title': self._extract_title(lines),
                'contact': self._extract_contact(content),
                'skills': self._extract_skills(content),
                'experience': self._extract_experience(content),
                'education': self._extract_education(content),
                'achievements': self._extract_achievements(content)
            }
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error extracting data from {file_path}: {e}")
            return {}
    
    def _extract_name(self, lines: List[str]) -> str:
        """Extract name from resume"""
        for line in lines:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()
        return "Professional"
    
    def _extract_title(self, lines: List[str]) -> str:
        """Extract professional title"""
        # Look for bold title after name
        for i, line in enumerate(lines):
            if line.strip().startswith('# '):
                # Check next few lines for bold title
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip().startswith('**') and lines[j].strip().endswith('**'):
                        return lines[j].strip()[2:-2]
                break
        return "Professional"
    
    def _extract_contact(self, content: str) -> Dict[str, str]:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        if email_match:
            contact['email'] = email_match.group()
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', content.lower())
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        # Phone
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\+\d{1,3}\s*\d{3}\s*\d{3}\s*\d{4}'
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, content)
            if phone_match:
                contact['phone'] = phone_match.group()
                break
        
        return contact
    
    def _extract_skills(self, content: str) -> Dict[str, List[str]]:
        """Extract and categorize skills"""
        skills = {'technical': [], 'soft': [], 'other': []}
        
        # Find skills section
        skills_section = self._extract_section_content(content, 'skills')
        if not skills_section:
            return skills
        
        # Look for categorized skills (bold categories)
        category_matches = re.findall(r'\*\*([^*]+)\*\*:\s*([^*\n]+)', skills_section)
        
        if category_matches:
            for category, skill_list in category_matches:
                skill_items = [s.strip() for s in skill_list.split(',')]
                category_lower = category.lower()
                
                if any(tech in category_lower for tech in ['programming', 'technical', 'tools', 'technologies']):
                    skills['technical'].extend(skill_items)
                elif any(soft in category_lower for soft in ['soft', 'leadership', 'communication']):
                    skills['soft'].extend(skill_items)
                else:
                    skills['other'].extend(skill_items)
        else:
            # Extract from plain text
            all_skills = re.findall(r'\b[A-Z][A-Za-z+#.]*\b', skills_section)
            technical_keywords = ['Python', 'JavaScript', 'Java', 'React', 'Node', 'AWS', 'Docker', 'SQL']
            
            for skill in all_skills:
                if any(tech in skill for tech in technical_keywords):
                    skills['technical'].append(skill)
                else:
                    skills['other'].append(skill)
        
        return skills
    
    def _extract_experience(self, content: str) -> List[Dict[str, Any]]:
        """Extract professional experience"""
        experience = []
        
        exp_section = self._extract_section_content(content, 'professional experience')
        if not exp_section:
            exp_section = self._extract_section_content(content, 'experience')
        
        if not exp_section:
            return experience
        
        # Split by H3 headings (job titles)
        jobs = re.split(r'\n### ', exp_section)
        
        for job in jobs:
            if not job.strip():
                continue
            
            lines = job.strip().split('\n')
            if not lines:
                continue
            
            # Extract job info
            job_data = {
                'title': lines[0].strip(),
                'company': '',
                'duration': '',
                'achievements': []
            }
            
            # Look for company and duration
            for line in lines[1:5]:  # Check first few lines
                if '**' in line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        job_data['company'] = parts[0].replace('**', '').strip()
                        job_data['duration'] = parts[1].replace('*', '').strip()
                    break
            
            # Extract achievements (bullet points)
            for line in lines:
                if line.strip().startswith('- '):
                    achievement = line.strip()[2:].strip()
                    if achievement:
                        job_data['achievements'].append(achievement)
            
            if job_data['achievements'] or job_data['company']:
                experience.append(job_data)
        
        return experience
    
    def _extract_education(self, content: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        
        edu_section = self._extract_section_content(content, 'education')
        if not edu_section:
            return education
        
        # Look for degree patterns
        degree_patterns = [
            r'(PhD|Ph\.D\.|Doctor of Philosophy)\s+([^|]+)(?:\s*\|\s*([^|]+))?(?:\s*\|\s*(\d{4}))?',
            r'(MS|M\.S\.|Master of Science)\s+([^|]+)(?:\s*\|\s*([^|]+))?(?:\s*\|\s*(\d{4}))?',
            r'(BS|B\.S\.|Bachelor of Science)\s+([^|]+)(?:\s*\|\s*([^|]+))?(?:\s*\|\s*(\d{4}))?',
            r'(MBA|Master of Business Administration)\s*(?:\s*\|\s*([^|]+))?(?:\s*\|\s*(\d{4}))?'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, edu_section)
            for match in matches:
                edu_data = {
                    'degree': match[0],
                    'field': match[1] if len(match) > 1 and match[1] else '',
                    'institution': match[2] if len(match) > 2 and match[2] else '',
                    'year': match[3] if len(match) > 3 and match[3] else ''
                }
                education.append(edu_data)
        
        return education
    
    def _extract_achievements(self, content: str) -> List[Dict[str, Any]]:
        """Extract quantified achievements"""
        achievements = []
        
        # Find all bullet points with numbers/percentages
        bullet_pattern = r'- ([^-\n]+(?:\d+[%$]?|\d+[x\s]*(?:times|fold)|\d+[KMB]?|\d+\+)[^-\n]*)'
        matches = re.findall(bullet_pattern, content)
        
        for match in matches:
            achievement_text = match.strip()
            
            # Extract metrics
            metrics = re.findall(r'\b(\d+(?:\.\d+)?)\s*([%$]?|[KMB]|times?|fold|x)\b', achievement_text)
            
            achievement_data = {
                'text': achievement_text,
                'metrics': metrics,
                'quantified': len(metrics) > 0
            }
            
            achievements.append(achievement_data)
        
        return achievements
    
    def _extract_section_content(self, content: str, section_name: str) -> str:
        """Extract content from a specific section"""
        pattern = f'## {re.escape(section_name)}'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if not match:
            return ""
        
        # Get content from section start to next H2 section
        start_pos = match.end()
        next_section = re.search(r'\n## ', content[start_pos:])
        
        if next_section:
            end_pos = start_pos + next_section.start()
            return content[start_pos:end_pos].strip()
        else:
            return content[start_pos:].strip()


class LinkedInPostGenerator:
    """Generates LinkedIn posts from resume data"""
    
    def __init__(self):
        self.extractor = ResumeDataExtractor()
        self.character_limit = 3000
        
        # Achievement templates
        self.achievement_templates = [
            "🎯 Proud to share: {achievement}\n\nThis experience taught me {lesson}.\n\n{reflection}\n\n{hashtags}",
            "💡 Results matter: {achievement}\n\n{process}\n\nKey takeaway: {insight}\n\n{hashtags}",
            "🚀 Breaking barriers: {achievement}\n\n{challenge} But {solution}.\n\n{hashtags}",
            "📈 Data-driven impact: {achievement}\n\n{method}\n\nWhy this matters: {significance}\n\n{hashtags}"
        ]
    
    def generate_achievement_posts(self, file_path: str) -> List[Dict[str, Any]]:
        """Generate LinkedIn posts from resume achievements"""
        posts = []
        
        try:
            data = self.extractor.extract_from_file(file_path)
            achievements = data.get('achievements', [])
            
            # Filter quantified achievements
            quantified = [a for a in achievements if a.get('quantified', False)]
            
            # Generate posts for top achievements
            for achievement in quantified[:5]:  # Top 5 achievements
                post = self._create_achievement_post(achievement, data)
                if post:
                    posts.append(post)
            
        except Exception as e:
            logger.error(f"Error generating achievement posts: {e}")
        
        return posts
    
    def generate_skill_showcase(self, file_path: str) -> List[Dict[str, Any]]:
        """Generate posts showcasing skills and expertise"""
        posts = []
        
        try:
            data = self.extractor.extract_from_file(file_path)
            skills = data.get('skills', {})
            experience = data.get('experience', [])
            
            # Generate skill story posts
            for category, skill_list in skills.items():
                if skill_list and category in ['technical', 'other']:
                    post = self._create_skill_post(category, skill_list, experience, data)
                    if post:
                        posts.append(post)
            
        except Exception as e:
            logger.error(f"Error generating skill showcase posts: {e}")
        
        return posts
    
    def generate_career_update(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Generate career update/transition post"""
        
        try:
            data = self.extractor.extract_from_file(file_path)
            experience = data.get('experience', [])
            
            if not experience:
                return None
            
            current_role = experience[0]  # Most recent role
            
            content = f"Excited to share an update on my career journey! 🌟\n\n"
            content += f"Currently serving as {current_role.get('title', '')} at {current_role.get('company', '')}, "
            content += f"where I'm focused on driving impactful results.\n\n"
            
            # Add key achievements
            if current_role.get('achievements'):
                content += "Recent highlights include:\n"
                for achievement in current_role['achievements'][:3]:
                    content += f"• {achievement}\n"
                content += "\n"
            
            content += "Grateful for the opportunities to grow and contribute to meaningful work. "
            content += "Always interested in connecting with fellow professionals and exploring new challenges!\n\n"
            
            hashtags = self._generate_role_hashtags(current_role, data)
            content += ' '.join(hashtags)
            
            return {
                'content': content,
                'type': 'career_update',
                'hashtags': hashtags,
                'character_count': len(content)
            }
            
        except Exception as e:
            logger.error(f"Error generating career update: {e}")
            return None
    
    def _create_achievement_post(self, achievement: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a single achievement post"""
        
        achievement_text = achievement.get('text', '')
        if not achievement_text:
            return None
        
        # Extract action and impact
        action_verbs = ['increased', 'reduced', 'improved', 'led', 'developed', 'implemented', 'achieved']
        action = next((verb for verb in action_verbs if verb in achievement_text.lower()), 'delivered')
        
        # Create content
        content = f"💼 Professional milestone: {achievement_text}\n\n"
        content += f"This achievement reflects the power of {action.replace('ed', 'ing')} strategically and measuring impact.\n\n"
        content += "Key factors that made this possible:\n"
        content += "• Focus on data-driven decisions\n"
        content += "• Collaborative team approach\n"
        content += "• Continuous improvement mindset\n\n"
        content += "What strategies have driven your biggest professional wins?\n\n"
        
        hashtags = self._generate_achievement_hashtags(achievement_text, data)
        content += ' '.join(hashtags)
        
        if len(content) <= self.character_limit:
            return {
                'content': content,
                'type': 'achievement',
                'hashtags': hashtags,
                'character_count': len(content)
            }
        
        return None
    
    def _create_skill_post(self, category: str, skills: List[str], experience: List[Dict], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a skill showcase post"""
        
        if not skills:
            return None
        
        # Take top skills
        top_skills = skills[:5]
        skill_str = ', '.join(top_skills)
        
        content = f"🔧 Tech Stack Spotlight: {skill_str}\n\n"
        content += f"Over the years, I've had the opportunity to work extensively with these {category} tools. "
        content += "Each brings unique strengths to solving complex challenges.\n\n"
        
        # Add experience context if available
        if experience:
            recent_role = experience[0]
            content += f"In my current role as {recent_role.get('title', '')}, "
            content += f"I leverage these skills to drive results and innovation.\n\n"
        
        content += "What's your go-to tech stack? Always interested in learning about new tools and approaches!\n\n"
        
        hashtags = self._generate_skill_hashtags(top_skills, data)
        content += ' '.join(hashtags)
        
        if len(content) <= self.character_limit:
            return {
                'content': content,
                'type': 'skill_showcase',
                'hashtags': hashtags,
                'character_count': len(content)
            }
        
        return None
    
    def _generate_achievement_hashtags(self, achievement: str, data: Dict[str, Any]) -> List[str]:
        """Generate relevant hashtags for achievement post"""
        hashtags = ['#Achievement', '#ProfessionalGrowth']
        
        # Add role-based hashtags
        title = data.get('title', '').lower()
        if 'engineer' in title:
            hashtags.extend(['#SoftwareEngineering', '#TechLeadership'])
        elif 'manager' in title or 'director' in title:
            hashtags.extend(['#Leadership', '#TeamManagement'])
        elif 'data' in title:
            hashtags.extend(['#DataScience', '#Analytics'])
        
        # Add metric-based hashtags
        if any(word in achievement.lower() for word in ['revenue', 'sales', 'profit']):
            hashtags.append('#BusinessImpact')
        if any(word in achievement.lower() for word in ['efficiency', 'optimization', 'performance']):
            hashtags.append('#Optimization')
        if any(word in achievement.lower() for word in ['team', 'people', 'mentor']):
            hashtags.append('#PeopleManagement')
        
        return hashtags[:8]  # Limit to 8 hashtags
    
    def _generate_skill_hashtags(self, skills: List[str], data: Dict[str, Any]) -> List[str]:
        """Generate hashtags for skill posts"""
        hashtags = ['#TechStack', '#ProfessionalSkills']
        
        # Add skill-specific hashtags
        for skill in skills[:3]:
            clean_skill = re.sub(r'[^A-Za-z0-9]', '', skill)
            if clean_skill:
                hashtags.append(f'#{clean_skill}')
        
        # Add role hashtags
        title = data.get('title', '').lower()
        if 'developer' in title or 'engineer' in title:
            hashtags.append('#SoftwareDevelopment')
        elif 'data' in title:
            hashtags.append('#DataScience')
        elif 'devops' in title:
            hashtags.append('#DevOps')
        
        return hashtags[:8]
    
    def _generate_role_hashtags(self, role: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
        """Generate hashtags for role-based posts"""
        hashtags = ['#CareerUpdate', '#ProfessionalJourney']
        
        title = role.get('title', '').lower()
        if 'senior' in title:
            hashtags.append('#SeniorRole')
        if 'lead' in title or 'manager' in title:
            hashtags.append('#Leadership')
        if 'engineer' in title:
            hashtags.append('#Engineering')
        
        return hashtags[:6]


class HashtagGenerator:
    """Generates relevant hashtags for content"""
    
    def __init__(self):
        self.hashtag_map = {
            'technical': {
                'python': '#Python', 'javascript': '#JavaScript', 'java': '#Java',
                'react': '#React', 'node': '#NodeJS', 'aws': '#AWS', 'docker': '#Docker',
                'kubernetes': '#Kubernetes', 'sql': '#SQL', 'postgresql': '#PostgreSQL'
            },
            'roles': {
                'engineer': '#SoftwareEngineering', 'developer': '#SoftwareDevelopment',
                'manager': '#Management', 'director': '#Leadership', 'architect': '#SoftwareArchitecture',
                'scientist': '#DataScience', 'analyst': '#DataAnalytics', 'devops': '#DevOps'
            },
            'industries': {
                'fintech': '#FinTech', 'healthcare': '#HealthTech', 'ecommerce': '#ECommerce',
                'startup': '#StartupLife', 'enterprise': '#Enterprise', 'saas': '#SaaS'
            }
        }
    
    def generate_hashtags(self, file_path: str, max_hashtags: int = 10) -> List[str]:
        """Generate relevant hashtags from resume content"""
        hashtags = set()
        
        try:
            extractor = ResumeDataExtractor()
            data = extractor.extract_from_file(file_path)
            
            # Add role-based hashtags
            title = data.get('title', '').lower()
            for role, hashtag in self.hashtag_map['roles'].items():
                if role in title:
                    hashtags.add(hashtag)
            
            # Add technical hashtags
            skills = data.get('skills', {})
            for skill_list in skills.values():
                for skill in skill_list:
                    skill_lower = skill.lower()
                    for tech, hashtag in self.hashtag_map['technical'].items():
                        if tech in skill_lower:
                            hashtags.add(hashtag)
            
            # Add general professional hashtags
            hashtags.update(['#ProfessionalDevelopment', '#TechCommunity', '#Innovation'])
            
            return list(hashtags)[:max_hashtags]
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return ['#Professional', '#TechCommunity']


class BioGenerator:
    """Generates professional bios of various lengths"""
    
    def __init__(self):
        self.extractor = ResumeDataExtractor()
    
    def generate_short_bio(self, file_path: str, max_chars: int = 500) -> str:
        """Generate a short professional bio"""
        
        try:
            data = self.extractor.extract_from_file(file_path)
            
            name = data.get('name', 'Professional')
            title = data.get('title', 'Professional')
            experience = data.get('experience', [])
            skills = data.get('skills', {})
            
            # Build short bio
            bio = f"{name} is a {title}"
            
            if experience:
                current_role = experience[0]
                bio += f" currently working as {current_role.get('title', '')} at {current_role.get('company', '')}."
            else:
                bio += "."
            
            # Add key skills
            tech_skills = skills.get('technical', [])
            if tech_skills:
                bio += f" Expertise includes {', '.join(tech_skills[:3])}."
            
            # Add key achievement
            if experience and experience[0].get('achievements'):
                top_achievement = experience[0]['achievements'][0]
                if len(bio + " " + top_achievement) <= max_chars:
                    bio += f" {top_achievement}"
            
            return bio[:max_chars]
            
        except Exception as e:
            logger.error(f"Error generating short bio: {e}")
            return "Professional with expertise in technology and innovation."
    
    def generate_long_bio(self, file_path: str, max_chars: int = 2000) -> str:
        """Generate a detailed professional bio"""
        
        try:
            data = self.extractor.extract_from_file(file_path)
            
            name = data.get('name', 'Professional')
            title = data.get('title', 'Professional')
            experience = data.get('experience', [])
            education = data.get('education', [])
            skills = data.get('skills', {})
            
            # Build comprehensive bio
            bio_parts = []
            
            # Introduction
            bio_parts.append(f"{name} is a {title} with a proven track record of delivering impactful results.")
            
            # Current role
            if experience:
                current_role = experience[0]
                bio_parts.append(f"Currently serving as {current_role.get('title', '')} at {current_role.get('company', '')}, {name.split()[0]} focuses on driving innovation and excellence.")
                
                # Key achievements
                if current_role.get('achievements'):
                    bio_parts.append("Recent accomplishments include:")
                    for achievement in current_role['achievements'][:3]:
                        bio_parts.append(f"• {achievement}")
            
            # Background
            if len(experience) > 1:
                bio_parts.append(f"With experience spanning multiple roles, {name.split()[0]} has developed expertise across diverse challenges and industries.")
            
            # Education
            if education:
                edu_list = [f"{edu.get('degree', '')} in {edu.get('field', '')}" for edu in education if edu.get('degree')]
                if edu_list:
                    bio_parts.append(f"Educational background includes {', '.join(edu_list)}.")
            
            # Skills and expertise
            all_skills = []
            for skill_list in skills.values():
                all_skills.extend(skill_list)
            
            if all_skills:
                bio_parts.append(f"Core competencies span {', '.join(all_skills[:8])}.")
            
            # Closing
            bio_parts.append(f"{name.split()[0]} is passionate about leveraging technology to solve complex problems and drive meaningful impact.")
            
            bio = ' '.join(bio_parts)
            return bio[:max_chars]
            
        except Exception as e:
            logger.error(f"Error generating long bio: {e}")
            return "Professional with extensive experience in technology and leadership, focused on driving innovation and delivering results."
    
    def generate_bio_variations(self, file_path: str, count: int = 3) -> List[str]:
        """Generate multiple bio variations"""
        variations = []
        
        try:
            data = self.extractor.extract_from_file(file_path)
            
            # Variation 1: Achievement-focused
            variations.append(self._create_achievement_bio(data))
            
            # Variation 2: Skill-focused
            variations.append(self._create_skill_bio(data))
            
            # Variation 3: Experience-focused
            variations.append(self._create_experience_bio(data))
            
            return variations[:count]
            
        except Exception as e:
            logger.error(f"Error generating bio variations: {e}")
            return ["Professional with expertise in technology and innovation."] * count
    
    def _create_achievement_bio(self, data: Dict[str, Any]) -> str:
        """Create achievement-focused bio"""
        name = data.get('name', 'Professional')
        title = data.get('title', 'Professional')
        achievements = data.get('achievements', [])
        experience = data.get('experience', [])
        
        # Use title from experience if available and more specific
        if experience and experience[0].get('title'):
            current_title = experience[0]['title']
            if 'Marketing' in current_title or len(current_title) > len(title):
                title = current_title
        
        bio = f"{name} is a results-driven {title} with a track record of measurable impact. "
        
        if achievements:
            quantified = [a for a in achievements if a.get('quantified')]
            if quantified:
                bio += f"Notable achievements include {quantified[0].get('text', '')}."
        
        return bio
    
    def _create_skill_bio(self, data: Dict[str, Any]) -> str:
        """Create skill-focused bio"""
        name = data.get('name', 'Professional')
        title = data.get('title', 'Professional')
        skills = data.get('skills', {})
        experience = data.get('experience', [])
        
        # Use title from experience if available and more specific
        if experience and experience[0].get('title'):
            current_title = experience[0]['title']
            if 'Marketing' in current_title or len(current_title) > len(title):
                title = current_title
        
        bio = f"{name} is a skilled {title} with deep expertise in modern technologies. "
        
        tech_skills = skills.get('technical', [])
        if tech_skills:
            bio += f"Specializes in {', '.join(tech_skills[:5])} and related technologies."
        
        return bio
    
    def _create_experience_bio(self, data: Dict[str, Any]) -> str:
        """Create experience-focused bio"""
        name = data.get('name', 'Professional')
        title = data.get('title', 'Professional')
        experience = data.get('experience', [])
        
        # Use title from experience if available and more specific
        if experience and experience[0].get('title'):
            current_title = experience[0]['title']
            if 'Marketing' in current_title or len(current_title) > len(title):
                title = current_title
        
        bio = f"{name} is an experienced {title} with a diverse background across multiple organizations. "
        
        if len(experience) >= 2:
            companies = [exp.get('company', '') for exp in experience[:3] if exp.get('company')]
            if companies:
                bio += f"Has contributed to success at {', '.join(companies)}."
        
        return bio


class SocialMediaGenerator:
    """Generates content for various social media platforms"""
    
    def __init__(self):
        self.extractor = ResumeDataExtractor()
    
    def generate_twitter_thread(self, file_path: str) -> List[str]:
        """Generate a Twitter/X thread from achievements"""
        
        try:
            data = self.extractor.extract_from_file(file_path)
            achievements = data.get('achievements', [])
            
            thread = []
            
            # Opening tweet
            thread.append("🧵 Thread: Lessons learned from recent professional wins...")
            
            # Achievement tweets
            quantified = [a for a in achievements if a.get('quantified')][:3]
            
            for i, achievement in enumerate(quantified, 2):
                tweet = f"{i}/{len(quantified)+1} {achievement.get('text', '')[:240]}"
                thread.append(tweet)
            
            # Closing tweet
            thread.append(f"{len(quantified)+1}/{len(quantified)+1} Key takeaway: Consistent focus on measurable impact drives real results. What's been your biggest professional win lately?")
            
            return thread
            
        except Exception as e:
            logger.error(f"Error generating Twitter thread: {e}")
            return ["Professional achievements and lessons learned..."]


class ContentCalendarGenerator:
    """Generates content calendar suggestions"""
    
    def __init__(self):
        self.extractor = ResumeDataExtractor()
    
    def generate_monthly_calendar(self, file_path: str) -> Dict[str, Any]:
        """Generate a month's worth of content suggestions"""
        
        try:
            data = self.extractor.extract_from_file(file_path)
            
            calendar = {
                'month': datetime.now().strftime('%B %Y'),
                'posts': []
            }
            
            # Week 1: Achievement spotlight
            calendar['posts'].append({
                'date': 'Week 1',
                'type': 'achievement',
                'topic': 'Share a recent professional win with metrics',
                'hashtags': ['#Achievement', '#ProfessionalGrowth']
            })
            
            # Week 2: Skills showcase
            calendar['posts'].append({
                'date': 'Week 2', 
                'type': 'skills',
                'topic': 'Highlight technical skills and expertise',
                'hashtags': ['#TechStack', '#Skills']
            })
            
            # Week 3: Industry insights
            calendar['posts'].append({
                'date': 'Week 3',
                'type': 'thought_leadership',
                'topic': 'Share industry observations or trends',
                'hashtags': ['#Industry', '#Innovation']
            })
            
            # Week 4: Career journey
            calendar['posts'].append({
                'date': 'Week 4',
                'type': 'career_story',
                'topic': 'Reflect on career growth and lessons learned',
                'hashtags': ['#CareerJourney', '#ProfessionalDevelopment']
            })
            
            return calendar
            
        except Exception as e:
            logger.error(f"Error generating content calendar: {e}")
            return {'month': 'Current', 'posts': []}


class TemplateEngine:
    """Handles content templates and formatting"""
    
    def __init__(self):
        self.templates = {
            'achievement': {
                'metric_highlight': "🎯 {action} {metric} by {amount} through {method}",
                'impact_story': "The challenge: {challenge}\nThe approach: {approach}\nThe result: {result}",
                'lesson_learned': "Key insight: {insight}\n\nThis taught me {lesson}"
            },
            'skill': {
                'expertise': "After {years} years working with {skill}, I've learned {insight}",
                'evolution': "{skill} has evolved significantly - here's what's changed: {changes}",
                'application': "How I use {skill} to {application}"
            }
        }
    
    def apply_achievement_template(self, achievement_data: Dict[str, str]) -> str:
        """Apply template to achievement data"""
        
        template = self.templates['achievement']['metric_highlight']
        
        try:
            return template.format(**achievement_data)
        except KeyError as e:
            logger.warning(f"Missing template data: {e}")
            return f"Achievement: {achievement_data.get('action', 'Delivered')} significant results"
    
    def apply_skill_story_template(self, skill_data: Dict[str, Any]) -> str:
        """Apply template to skill story data"""
        
        template = self.templates['skill']['expertise']
        
        try:
            return template.format(**skill_data)
        except KeyError as e:
            logger.warning(f"Missing skill template data: {e}")
            return f"Expertise in {skill_data.get('skill', 'technology')} with proven results"


class ContentGenerationAgent:
    """Main content generation agent that coordinates all generators"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.linkedin_generator = LinkedInPostGenerator()
        self.bio_generator = BioGenerator()
        self.social_generator = SocialMediaGenerator()
        self.hashtag_generator = HashtagGenerator()
        self.calendar_generator = ContentCalendarGenerator()
        self.template_engine = TemplateEngine()
    
    def generate_content_package(self, file_path: str) -> Dict[str, Any]:
        """Generate comprehensive content package from resume"""
        
        package = {
            'source_file': file_path,
            'generation_date': datetime.now().isoformat(),
            'linkedin_posts': [],
            'bios': {},
            'social_media': {},
            'hashtags': [],
            'content_calendar': {},
            'issues': []
        }
        
        try:
            # Generate LinkedIn content
            package['linkedin_posts'] = self.linkedin_generator.generate_achievement_posts(file_path)
            skill_posts = self.linkedin_generator.generate_skill_showcase(file_path)
            package['linkedin_posts'].extend(skill_posts)
            
            career_update = self.linkedin_generator.generate_career_update(file_path)
            if career_update:
                package['linkedin_posts'].append(career_update)
            
            # Generate bios
            package['bios']['short'] = self.bio_generator.generate_short_bio(file_path)
            package['bios']['long'] = self.bio_generator.generate_long_bio(file_path)
            package['bios']['variations'] = self.bio_generator.generate_bio_variations(file_path)
            
            # Generate social media content
            package['social_media']['twitter_thread'] = self.social_generator.generate_twitter_thread(file_path)
            
            # Generate hashtags
            package['hashtags'] = self.hashtag_generator.generate_hashtags(file_path)
            
            # Generate content calendar
            package['content_calendar'] = self.calendar_generator.generate_monthly_calendar(file_path)
            
        except Exception as e:
            logger.error(f"Error generating content package: {e}")
            package['issues'].append({
                'type': 'generation_error',
                'message': f"Content generation failed: {e}",
                'severity': 'error'
            })
        
        return package
    
    def save_content_package(self, package: Dict[str, Any], output_dir: str = "generated-content") -> str:
        """Save generated content to files"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        source_name = Path(package['source_file']).stem
        
        # Save LinkedIn posts
        linkedin_file = output_path / f"{source_name}_linkedin_{timestamp}.md"
        with open(linkedin_file, 'w', encoding='utf-8') as f:
            f.write("# LinkedIn Content\n\n")
            for i, post in enumerate(package['linkedin_posts'], 1):
                f.write(f"## Post {i}: {post.get('type', 'content').title()}\n\n")
                f.write(f"{post.get('content', '')}\n\n")
                f.write(f"**Hashtags:** {' '.join(post.get('hashtags', []))}\n\n")
                f.write(f"**Character count:** {post.get('character_count', 0)}\n\n")
                f.write("---\n\n")
        
        # Save bios
        bio_file = output_path / f"{source_name}_bios_{timestamp}.md"
        with open(bio_file, 'w', encoding='utf-8') as f:
            f.write("# Professional Bios\n\n")
            f.write(f"## Short Bio\n\n{package['bios']['short']}\n\n")
            f.write(f"## Long Bio\n\n{package['bios']['long']}\n\n")
            f.write("## Bio Variations\n\n")
            for i, bio in enumerate(package['bios']['variations'], 1):
                f.write(f"### Variation {i}\n\n{bio}\n\n")
        
        # Save package as JSON
        json_file = output_path / f"{source_name}_content_package_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False)
        
        return str(json_file)


def main():
    """Command-line interface for the content generation agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate content from resume data")
    parser.add_argument("file", help="Resume markdown file to process")
    parser.add_argument("--output", default="generated-content", 
                       help="Output directory for generated content")
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both",
                       help="Output format")
    
    args = parser.parse_args()
    
    agent = ContentGenerationAgent()
    package = agent.generate_content_package(args.file)
    
    if args.format in ["json", "both"]:
        output_file = agent.save_content_package(package, args.output)
        print(f"Content package saved to: {output_file}")
    
    if args.format in ["markdown", "both"]:
        # Print LinkedIn posts to console
        print("\n# Generated LinkedIn Posts\n")
        for i, post in enumerate(package['linkedin_posts'], 1):
            print(f"## Post {i}: {post.get('type', 'content').title()}\n")
            print(post.get('content', ''))
            print(f"\n**Hashtags:** {' '.join(post.get('hashtags', []))}")
            print(f"**Characters:** {post.get('character_count', 0)}")
            print("\n---\n")


if __name__ == "__main__":
    main()