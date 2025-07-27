#!/usr/bin/env python3
"""
Content Generation Agent Test Suite
Tests for LinkedIn post generation, professional bio creation, and social media content
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestLinkedInGeneration(unittest.TestCase):
    """Test LinkedIn post generation functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_resume(self, filename, content):
        """Create a test resume file"""
        file_path = self.temp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_achievement_post_generation(self):
        """Test generation of LinkedIn posts from achievements"""
        resume_content = '''# John Smith
Software Engineer

john.smith@email.com | (555) 123-4567 | linkedin.com/in/johnsmith

## Professional Experience

### Senior Software Engineer
**Tech Company Inc.** | *January 2020 - Present*

- Led migration of monolithic application to microservices, reducing deployment time by 75%
- Implemented automated testing framework that increased code coverage from 45% to 92%
- Mentored 5 junior developers, with 3 receiving promotions within 18 months
- Optimized database queries resulting in 60% improvement in application response time

## Skills
Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL
'''
        
        file_path = self.create_test_resume("test_resume.md", resume_content)
        
        from content_generation_agent import LinkedInPostGenerator
        generator = LinkedInPostGenerator()
        posts = generator.generate_achievement_posts(str(file_path))
        
        # Should generate posts from quantified achievements
        self.assertGreater(len(posts), 0, "Should generate at least one post")
        
        # Check post quality
        for post in posts:
            self.assertIn('content', post, "Post should have content")
            self.assertIn('hashtags', post, "Post should have hashtags")
            self.assertLessEqual(len(post['content']), 3000, "Post should respect LinkedIn character limit")
    
    def test_skill_showcase_generation(self):
        """Test generation of skill showcase posts"""
        resume_content = '''# Jane Doe
Data Scientist

## Skills

**Programming Languages:** Python, R, SQL, Julia
**Machine Learning:** TensorFlow, PyTorch, scikit-learn, XGBoost
**Data Visualization:** Tableau, Power BI, Matplotlib, Plotly
**Cloud Platforms:** AWS, Google Cloud, Azure
**Big Data:** Spark, Hadoop, Kafka

## Professional Experience

### Senior Data Scientist
**Analytics Corp** | *2019 - Present*

- Built predictive models achieving 94% accuracy in customer churn prediction
- Developed real-time anomaly detection system processing 1M+ events per day
'''
        
        file_path = self.create_test_resume("data_scientist.md", resume_content)
        
        from content_generation_agent import LinkedInPostGenerator
        generator = LinkedInPostGenerator()
        skill_posts = generator.generate_skill_showcase(str(file_path))
        
        # Should generate skill-focused content
        self.assertGreater(len(skill_posts), 0, "Should generate skill showcase posts")
        
        # Verify skill categories are represented
        all_content = ' '.join(post['content'] for post in skill_posts)
        self.assertTrue(any(skill in all_content for skill in ['Python', 'Machine Learning', 'Cloud']),
                       "Should include actual skills from resume")
    
    def test_career_update_generation(self):
        """Test generation of career update posts"""
        resume_content = '''# Michael Johnson
Product Manager

## Professional Experience

### Senior Product Manager
**Innovation Labs** | *March 2023 - Present*

- Leading product strategy for AI-powered analytics platform
- Managing cross-functional team of 15 engineers and designers
- Launched 3 major features increasing user engagement by 45%

### Product Manager
**StartupXYZ** | *January 2020 - February 2023*

- Grew user base from 10K to 150K active users
- Increased revenue by 300% through strategic feature development
'''
        
        file_path = self.create_test_resume("product_manager.md", resume_content)
        
        from content_generation_agent import LinkedInPostGenerator
        generator = LinkedInPostGenerator()
        update_post = generator.generate_career_update(str(file_path))
        
        # Should generate career transition content
        self.assertIsNotNone(update_post, "Should generate career update post")
        self.assertIn('content', update_post, "Update should have content")
        self.assertIn('Senior Product Manager', update_post['content'], 
                     "Should mention current role")
    
    def test_hashtag_generation(self):
        """Test appropriate hashtag generation"""
        resume_content = '''# Sarah Chen
DevOps Engineer

## Skills
Kubernetes, Docker, Jenkins, Terraform, AWS, Python, Go

## Professional Experience
### DevOps Lead
**Cloud Solutions Inc** | *2021 - Present*

- Architected CI/CD pipeline reducing deployment time from 2 hours to 15 minutes
- Implemented Infrastructure as Code using Terraform across 50+ microservices
'''
        
        file_path = self.create_test_resume("devops.md", resume_content)
        
        from content_generation_agent import HashtagGenerator
        generator = HashtagGenerator()
        hashtags = generator.generate_hashtags(str(file_path))
        
        # Should generate relevant hashtags
        self.assertGreater(len(hashtags), 0, "Should generate hashtags")
        self.assertLessEqual(len(hashtags), 10, "Should not generate too many hashtags")
        
        # Check relevance
        hashtag_str = ' '.join(hashtags).lower()
        self.assertTrue(any(tech in hashtag_str for tech in ['devops', 'cloud', 'kubernetes']),
                       "Hashtags should be relevant to content")


class TestBioGeneration(unittest.TestCase):
    """Test professional bio generation functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_resume(self, filename, content):
        """Create a test resume file"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_short_bio_generation(self):
        """Test generation of short professional bio"""
        resume_content = '''# Emily Rodriguez
Full Stack Developer

emily@email.com | linkedin.com/in/emilyrodriguez

## Professional Experience

### Senior Full Stack Developer
**Tech Innovations** | *2020 - Present*

- Architected scalable web applications serving 500K+ daily users
- Led frontend modernization using React and TypeScript
- Mentored team of 8 developers on best practices

## Skills
JavaScript, TypeScript, Python, React, Node.js, PostgreSQL, AWS

## Education
BS Computer Science - Stanford University (2018)
'''
        
        file_path = self.create_test_resume("fullstack.md", resume_content)
        
        from content_generation_agent import BioGenerator
        generator = BioGenerator()
        short_bio = generator.generate_short_bio(str(file_path))
        
        # Should generate concise bio
        self.assertIsNotNone(short_bio, "Should generate short bio")
        self.assertLessEqual(len(short_bio), 500, "Short bio should be concise")
        self.assertIn('Full Stack Developer', short_bio, "Should include current role")
    
    def test_long_bio_generation(self):
        """Test generation of detailed professional bio"""
        resume_content = '''# Dr. Amanda Williams
Research Scientist

## Professional Experience

### Principal Research Scientist
**AI Research Lab** | *2019 - Present*

- Published 15 papers in top-tier conferences (NeurIPS, ICML, CVPR)
- Led team developing novel deep learning architectures for computer vision
- Secured $2M in research grants from NSF and DARPA

### Senior Research Scientist
**University Research Center** | *2015 - 2019*

- Developed breakthrough algorithm improving object detection accuracy by 23%
- Collaborated with industry partners including Google and Microsoft

## Education
PhD Computer Science - MIT (2015)
MS Computer Science - MIT (2012)
BS Mathematics - Harvard (2010)

## Skills
Python, TensorFlow, PyTorch, Computer Vision, Deep Learning, Research Leadership
'''
        
        file_path = self.create_test_resume("researcher.md", resume_content)
        
        from content_generation_agent import BioGenerator
        generator = BioGenerator()
        long_bio = generator.generate_long_bio(str(file_path))
        
        # Should generate comprehensive bio
        self.assertIsNotNone(long_bio, "Should generate long bio")
        self.assertGreater(len(long_bio), 500, "Long bio should be detailed")
        self.assertIn('Research Scientist', long_bio, "Should include role")
        self.assertIn('PhD', long_bio, "Should include education")
    
    def test_bio_variations(self):
        """Test generation of multiple bio variations"""
        resume_content = '''# David Park
Marketing Director

## Professional Experience

### Marketing Director
**Global Brands Inc** | *2021 - Present*

- Increased brand awareness by 150% through integrated marketing campaigns
- Managed $5M annual marketing budget with 20% YoY efficiency improvement
- Built and led team of 12 marketing professionals

## Skills
Digital Marketing, Brand Strategy, Team Leadership, Analytics, Content Marketing

## Education
MBA Marketing - Wharton (2015)
'''
        
        file_path = self.create_test_resume("marketing.md", resume_content)
        
        from content_generation_agent import BioGenerator
        generator = BioGenerator()
        bio_variations = generator.generate_bio_variations(str(file_path), count=3)
        
        # Should generate multiple unique variations
        self.assertEqual(len(bio_variations), 3, "Should generate requested number of variations")
        
        # Check uniqueness
        self.assertEqual(len(set(bio_variations)), 3, "All variations should be unique")
        
        # All should mention key elements
        for bio in bio_variations:
            self.assertIn('Marketing', bio, "All bios should mention marketing")


class TestSocialMediaContent(unittest.TestCase):
    """Test social media content generation"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_resume(self, filename, content):
        """Create a test resume file"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_twitter_thread_generation(self):
        """Test generation of Twitter/X thread from achievements"""
        resume_content = '''# Lisa Thompson
Cybersecurity Specialist

## Professional Experience

### Senior Security Engineer
**SecureNet Corp** | *2020 - Present*

- Prevented 50+ security breaches saving company $10M in potential losses
- Implemented zero-trust architecture reducing security incidents by 85%
- Developed security training program for 500+ employees
- Led incident response team handling critical vulnerabilities

## Skills
Penetration Testing, Security Architecture, Python, SIEM, Cloud Security
'''
        
        file_path = self.create_test_resume("security.md", resume_content)
        
        from content_generation_agent import SocialMediaGenerator
        generator = SocialMediaGenerator()
        thread = generator.generate_twitter_thread(str(file_path))
        
        # Should generate multi-tweet thread
        self.assertIsInstance(thread, list, "Thread should be a list of tweets")
        self.assertGreater(len(thread), 1, "Thread should have multiple tweets")
        
        # Check character limits
        for tweet in thread:
            self.assertLessEqual(len(tweet), 280, "Each tweet should respect character limit")
    
    def test_content_calendar_generation(self):
        """Test generation of content calendar suggestions"""
        resume_content = '''# Robert Kim
Software Architect

## Professional Experience

### Principal Software Architect
**Enterprise Solutions** | *2018 - Present*

- Designed microservices architecture serving 10M+ users
- Reduced system latency by 70% through optimization
- Established coding standards adopted by 200+ developers
- Speaking at 5+ tech conferences annually

## Skills
System Design, Java, Kubernetes, Architecture Patterns, Team Leadership
'''
        
        file_path = self.create_test_resume("architect.md", resume_content)
        
        from content_generation_agent import ContentCalendarGenerator
        generator = ContentCalendarGenerator()
        calendar = generator.generate_monthly_calendar(str(file_path))
        
        # Should generate content calendar
        self.assertIsInstance(calendar, dict, "Calendar should be a dictionary")
        self.assertIn('posts', calendar, "Calendar should have posts")
        self.assertGreater(len(calendar['posts']), 0, "Should suggest multiple posts")
        
        # Check post structure
        for post in calendar['posts']:
            self.assertIn('date', post, "Each post should have a date")
            self.assertIn('type', post, "Each post should have a type")
            self.assertIn('topic', post, "Each post should have a topic")


class TestContentTemplates(unittest.TestCase):
    """Test content template functionality"""
    
    def test_achievement_template_application(self):
        """Test application of achievement templates"""
        from content_generation_agent import TemplateEngine
        engine = TemplateEngine()
        
        achievement_data = {
            'action': 'Increased',
            'metric': 'customer satisfaction',
            'amount': '35%',
            'timeframe': '6 months',
            'method': 'implementing AI-powered support system'
        }
        
        result = engine.apply_achievement_template(achievement_data)
        
        # Should generate formatted achievement
        self.assertIsNotNone(result, "Should generate achievement text")
        self.assertIn('35%', result, "Should include metric")
        self.assertIn('customer satisfaction', result, "Should include what was improved")
    
    def test_skill_story_template(self):
        """Test skill story template generation"""
        from content_generation_agent import TemplateEngine
        engine = TemplateEngine()
        
        skill_data = {
            'skill': 'Python',
            'years': 8,
            'context': 'data science and automation',
            'achievement': 'automated 50+ manual processes',
            'insight': 'the importance of choosing the right tools for each task'
        }
        
        result = engine.apply_skill_story_template(skill_data)
        
        # Should generate skill narrative
        self.assertIsNotNone(result, "Should generate skill story")
        self.assertIn('Python', result, "Should mention the skill")
        self.assertIn('8', result, "Should include years of experience")


class TestContentGenerationIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_configuration(self):
        """Test that the content generation agent configuration is valid"""
        from agent_config_parser import AgentConfigParser
        
        # Use absolute path to configurations directory
        config_dir = Path(__file__).parent / "configurations"
        parser = AgentConfigParser(str(config_dir))
        agents = parser.load_all_agents()
        config = parser.get_agent_config("content-generation-agent")
        
        self.assertIsNotNone(config, "Content generation agent configuration should exist")
        self.assertEqual(config['name'], "content-generation-agent")
        self.assertEqual(config['specialization'], "content-creation-and-marketing")
    
    def test_security_integration(self):
        """Test that the content generation agent works with security framework"""
        from security_framework import SecurityFramework, PermissionType
        from agent_config_parser import AgentConfigParser
        
        # Use absolute path to configurations directory
        config_dir = Path(__file__).parent / "configurations"
        parser = AgentConfigParser(str(config_dir))
        agents = parser.load_all_agents()
        config = parser.get_agent_config("content-generation-agent")
        
        framework = SecurityFramework()
        session_id = framework.create_session("content-generation-agent", config)
        
        # Test permissions
        can_read_resume = framework.check_permission(
            session_id, PermissionType.READ, "test_resume.md", config
        )
        can_write_temp = framework.check_permission(
            session_id, PermissionType.WRITE, "temp/test.md", config
        )
        
        self.assertTrue(can_read_resume, "Should be able to read resume files")
        self.assertTrue(can_write_temp, "Should be able to write temp files")
        
        framework.end_session(session_id)


def run_tests():
    """Run all content generation agent tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestLinkedInGeneration,
        TestBioGeneration,
        TestSocialMediaContent,
        TestContentTemplates,
        TestContentGenerationIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)