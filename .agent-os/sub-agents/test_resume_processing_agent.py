#!/usr/bin/env python3
"""
Resume Processing Agent Test Suite
Tests for the resume validation, PDF generation QA, and content quality functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestResumeValidation(unittest.TestCase):
    """Test resume format validation functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_valid_resume_structure(self):
        """Test validation of properly structured resume"""
        valid_resume = '''# John Smith
**Software Engineer**

📧 john.smith@email.com | 📱 (555) 123-4567 | 🌐 linkedin.com/in/johnsmith

## Professional Experience

### Senior Software Engineer
**Tech Company Inc.** | *January 2020 - Present*

- Developed and maintained web applications using Python and JavaScript
- Led team of 5 developers on major product initiatives
- Improved system performance by 40% through optimization

### Software Engineer
**Previous Company** | *June 2018 - December 2019*

- Built REST APIs and microservices
- Collaborated with cross-functional teams
- Implemented automated testing frameworks

## Skills

**Programming Languages:** Python, JavaScript, Java, SQL
**Frameworks:** React, Django, Node.js, Flask
**Tools:** Git, Docker, AWS, PostgreSQL

## Education

**Bachelor of Science in Computer Science**  
University of Technology | 2018
'''
        
        file_path = self.create_test_file("valid_resume.md", valid_resume)
        
        from resume_processing_agent import ResumeValidator
        validator = ResumeValidator()
        issues = validator.validate_file(str(file_path))
        
        # Should have minimal issues for a well-structured resume
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 0, "Valid resume should not have critical issues")
    
    def test_missing_required_sections(self):
        """Test detection of missing required resume sections"""
        incomplete_resume = '''# Jane Doe

Just a name and no other information.
'''
        
        file_path = self.create_test_file("incomplete_resume.md", incomplete_resume)
        
        from resume_processing_agent import ResumeValidator
        validator = ResumeValidator()
        issues = validator.validate_file(str(file_path))
        
        # Should detect missing required sections
        missing_sections = [issue for issue in issues if 'missing' in issue.get('type', '').lower()]
        self.assertGreater(len(missing_sections), 0, "Should detect missing required sections")
    
    def test_contact_information_validation(self):
        """Test validation of contact information formats"""
        invalid_contact_resume = '''# John Smith
**Software Engineer**

Email: invalid-email | Phone: not-a-phone | LinkedIn: broken-link

## Professional Experience
Some experience here.

## Skills
Some skills here.

## Education
Some education here.
'''
        
        file_path = self.create_test_file("invalid_contact.md", invalid_contact_resume)
        
        from resume_processing_agent import ResumeValidator
        validator = ResumeValidator()
        issues = validator.validate_file(str(file_path))
        
        # Should detect contact information issues
        contact_issues = [issue for issue in issues if 'contact' in issue.get('type', '').lower()]
        self.assertGreater(len(contact_issues), 0, "Should detect contact information issues")
    
    def test_experience_section_validation(self):
        """Test validation of professional experience sections"""
        poor_experience_resume = '''# John Smith
📧 john@email.com

## Professional Experience

### Job Title
Company Name

Did some work.

### Another Job
Another Company | sometime in the past

- Worked on stuff and helped with things
- Was awesome at coding and made things better
'''
        
        file_path = self.create_test_file("poor_experience.md", poor_experience_resume)
        
        from resume_processing_agent import ResumeValidator
        validator = ResumeValidator()
        issues = validator.validate_file(str(file_path))
        
        # Should detect experience formatting issues
        experience_issues = [issue for issue in issues if 'experience' in issue.get('type', '').lower()]
        self.assertGreater(len(experience_issues), 0, "Should detect experience formatting issues")


class TestSkillsValidation(unittest.TestCase):
    """Test skills section validation functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_well_formatted_skills(self):
        """Test validation of well-formatted skills section"""
        good_skills_resume = '''# Developer Name
📧 email@example.com

## Skills

**Programming Languages:** Python, JavaScript, Java, C++
**Web Frameworks:** Django, React, Angular, Vue.js
**Databases:** PostgreSQL, MongoDB, Redis
**Tools & Technologies:** Git, Docker, AWS, Kubernetes
**Operating Systems:** Linux, macOS, Windows

## Professional Experience
Some experience here.

## Education
Some education here.
'''
        
        file_path = self.create_test_file("good_skills.md", good_skills_resume)
        
        from resume_processing_agent import SkillsValidator
        validator = SkillsValidator()
        issues = validator.validate_skills_section(str(file_path))
        
        # Should have minimal issues for well-formatted skills
        formatting_issues = [issue for issue in issues if 'formatting' in issue.get('type', '').lower()]
        self.assertEqual(len(formatting_issues), 0, "Well-formatted skills should not have formatting issues")
    
    def test_poorly_formatted_skills(self):
        """Test detection of poorly formatted skills section"""
        poor_skills_resume = '''# Developer Name
📧 email@example.com

## Skills

Python, JavaScript, React, Django, Git, AWS, Linux, PostgreSQL, etc.

## Professional Experience
Some experience here.

## Education  
Some education here.
'''
        
        file_path = self.create_test_file("poor_skills.md", poor_skills_resume)
        
        from resume_processing_agent import SkillsValidator
        validator = SkillsValidator()
        issues = validator.validate_skills_section(str(file_path))
        
        # Should detect formatting issues
        formatting_issues = [issue for issue in issues if 'formatting' in issue.get('type', '').lower() or 'organization' in issue.get('type', '').lower()]
        self.assertGreater(len(formatting_issues), 0, "Should detect skills formatting issues")
    
    def test_skills_categorization(self):
        """Test skills categorization analysis"""
        mixed_skills_resume = '''# Developer Name
📧 email@example.com

## Skills

Python, communication skills, JavaScript, teamwork, React, problem solving, AWS, leadership

## Professional Experience
Some experience here.

## Education
Some education here.
'''
        
        file_path = self.create_test_file("mixed_skills.md", mixed_skills_resume)
        
        from resume_processing_agent import SkillsValidator
        validator = SkillsValidator()
        analysis = validator.analyze_skills_categories(str(file_path))
        
        # Should identify different categories of skills
        self.assertIn('technical', analysis, "Should identify technical skills")
        self.assertIn('soft', analysis, "Should identify soft skills")


class TestPDFGenerationQA(unittest.TestCase):
    """Test PDF generation quality assurance functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_pdf_generation_requirements(self):
        """Test PDF generation requirements checking"""
        resume_content = '''# John Smith
📧 john@email.com

## Professional Experience
Software Engineer at Tech Company

## Skills
Python, JavaScript

## Education
BS Computer Science
'''
        
        file_path = self.create_test_file("test_resume.md", resume_content)
        
        from resume_processing_agent import PDFGenerationQA
        qa_checker = PDFGenerationQA()
        requirements_check = qa_checker.check_generation_requirements(str(file_path))
        
        # Should check for required tools and dependencies
        self.assertIn('pandoc_available', requirements_check, "Should check for pandoc availability")
        self.assertIn('css_stylesheet', requirements_check, "Should check for CSS stylesheet")
    
    def test_pdf_output_validation(self):
        """Test PDF output quality validation"""
        # This test would validate generated PDF output
        # For now, we'll test the validation logic without actual PDF generation
        
        from resume_processing_agent import PDFGenerationQA
        qa_checker = PDFGenerationQA()
        
        # Test validation criteria
        validation_criteria = qa_checker.get_validation_criteria()
        
        expected_criteria = [
            'page_formatting',
            'font_consistency',
            'content_completeness',
            'layout_quality'
        ]
        
        for criterion in expected_criteria:
            self.assertIn(criterion, validation_criteria, f"Should include {criterion} in validation criteria")


class TestContentQuality(unittest.TestCase):
    """Test resume content quality analysis"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_professional_language_check(self):
        """Test professional language and tone analysis"""
        unprofessional_resume = '''# John Smith
📧 john@email.com

## Professional Experience

### Developer
**Cool Company** | *2020 - Now*

- I did some stuff with computers
- Made things work better
- Was awesome at coding
- Helped people with stuff

## Skills

I'm good at Python and other things. I know how to use computers really well.
'''
        
        file_path = self.create_test_file("unprofessional.md", unprofessional_resume)
        
        from resume_processing_agent import ContentQualityAnalyzer
        analyzer = ContentQualityAnalyzer()
        issues = analyzer.analyze_language_quality(str(file_path))
        
        # Should detect unprofessional language
        language_issues = [issue for issue in issues if 'language' in issue.get('type', '').lower() or 'tone' in issue.get('type', '').lower()]
        self.assertGreater(len(language_issues), 0, "Should detect unprofessional language")
    
    def test_achievement_quantification(self):
        """Test analysis of quantified achievements"""
        vague_achievements_resume = '''# John Smith
📧 john@email.com

## Professional Experience

### Software Engineer
**Tech Company** | *2020 - 2023*

- Improved system performance
- Led a team
- Increased efficiency
- Reduced costs
- Enhanced user experience

## Skills
Python, JavaScript

## Education
BS Computer Science
'''
        
        file_path = self.create_test_file("vague_achievements.md", vague_achievements_resume)
        
        from resume_processing_agent import ContentQualityAnalyzer
        analyzer = ContentQualityAnalyzer()
        issues = analyzer.analyze_achievement_quantification(str(file_path))
        
        # Should detect lack of quantification
        quantification_issues = [issue for issue in issues if 'quantification' in issue.get('type', '').lower() or 'metrics' in issue.get('type', '').lower()]
        self.assertGreater(len(quantification_issues), 0, "Should detect lack of quantified achievements")
    
    def test_content_completeness(self):
        """Test content completeness analysis"""
        sparse_resume = '''# John Smith
📧 john@email.com

## Professional Experience
Developer

## Skills  
Programming

## Education
College

## Summary
Brief summary.
'''
        
        file_path = self.create_test_file("sparse_resume.md", sparse_resume)
        
        from resume_processing_agent import ContentQualityAnalyzer
        analyzer = ContentQualityAnalyzer()
        issues = analyzer.analyze_content_completeness(str(file_path))
        
        # Should detect incomplete content
        completeness_issues = [issue for issue in issues if 'brief' in issue.get('type', '').lower() or 'incomplete' in issue.get('type', '').lower() or 'missing' in issue.get('type', '').lower()]
        self.assertGreater(len(completeness_issues), 0, "Should detect incomplete content")


class TestResumeProcessingIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_configuration(self):
        """Test that the resume processing agent configuration is valid"""
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()
        config = parser.get_agent_config("resume-processing-agent")
        
        self.assertIsNotNone(config, "Resume processing agent configuration should exist")
        self.assertEqual(config['name'], "resume-processing-agent")
        self.assertEqual(config['specialization'], "resume-validation-and-processing")
    
    def test_security_integration(self):
        """Test that the resume processing agent works with security framework"""
        from security_framework import SecurityFramework, PermissionType
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()
        config = parser.get_agent_config("resume-processing-agent")
        
        framework = SecurityFramework()
        session_id = framework.create_session("resume-processing-agent", config)
        
        # Test permissions
        can_read_resume = framework.check_permission(
            session_id, PermissionType.READ, "cv/resume.md", config
        )
        can_write_pdf = framework.check_permission(
            session_id, PermissionType.WRITE, "cv/resume.pdf", config
        )
        
        self.assertTrue(can_read_resume, "Should be able to read resume files")
        self.assertTrue(can_write_pdf, "Should be able to write PDF files")
        
        framework.end_session(session_id)


def run_tests():
    """Run all resume processing agent tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestResumeValidation,
        TestSkillsValidation,
        TestPDFGenerationQA,
        TestContentQuality,
        TestResumeProcessingIntegration
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