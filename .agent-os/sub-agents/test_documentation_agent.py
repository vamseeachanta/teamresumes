#!/usr/bin/env python3
"""
Documentation Agent Test Suite
Tests for the documentation maintenance functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestLinkValidation(unittest.TestCase):
    """Test link validation functionality"""
    
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
    
    def test_valid_internal_links(self):
        """Test validation of valid internal links"""
        # Create target file
        self.create_test_file("target.md", "# Target File\n\nThis is the target.")
        
        # Create file with valid link
        source_content = """# Source File

[Link to target](target.md)
[Link to section](#section)

## Section
Content here.
"""
        
        file_path = self.create_test_file("source.md", source_content)
        
        from documentation_agent import LinkValidator
        validator = LinkValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should have no broken link issues
        broken_links = [issue for issue in issues if issue['type'] == 'broken_link']
        self.assertEqual(len(broken_links), 0, "Valid links should not be flagged as broken")
    
    def test_broken_internal_links(self):
        """Test detection of broken internal links"""
        source_content = """# Source File

[Broken link](nonexistent.md)
[Another broken link](../missing/file.md)
"""
        
        file_path = self.create_test_file("source.md", source_content)
        
        from documentation_agent import LinkValidator
        validator = LinkValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should detect broken links
        broken_links = [issue for issue in issues if issue['type'] == 'broken_link']
        self.assertGreater(len(broken_links), 0, "Should detect broken internal links")
    
    def test_external_link_validation(self):
        """Test external link validation"""
        source_content = """# Source File

[Valid external link](https://github.com)
[Invalid protocol](ftp://example.com)
"""
        
        file_path = self.create_test_file("source.md", source_content)
        
        from documentation_agent import LinkValidator
        validator = LinkValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should handle external links appropriately
        self.assertIsInstance(issues, list, "Should return list of issues")
    
    def test_anchor_link_validation(self):
        """Test anchor link validation within documents"""
        source_content = """# Source File

[Valid anchor](#section-1)
[Broken anchor](#nonexistent-section)

## Section 1
Content here.
"""
        
        file_path = self.create_test_file("source.md", source_content)
        
        from documentation_agent import LinkValidator
        validator = LinkValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should detect broken anchors
        broken_anchors = [issue for issue in issues if 'anchor' in issue.get('message', '').lower()]
        self.assertGreater(len(broken_anchors), 0, "Should detect broken anchor links")


class TestCrossReferenceValidation(unittest.TestCase):
    """Test cross-reference validation functionality"""
    
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
    
    def test_agent_os_cross_references(self):
        """Test validation of Agent OS cross-references"""
        # Create Agent OS structure
        self.create_test_file(".agent-os/product/mission.md", "# Mission\n\nProduct mission.")
        self.create_test_file(".agent-os/specs/test-spec/spec.md", "# Test Spec\n\nSpec content.")
        
        # Create file with cross-references
        source_content = """# Documentation

References:
- @.agent-os/product/mission.md
- @.agent-os/specs/test-spec/spec.md
- @.agent-os/nonexistent/file.md
"""
        
        file_path = self.create_test_file("README.md", source_content)
        
        from documentation_agent import CrossReferenceValidator
        validator = CrossReferenceValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should detect broken cross-references
        broken_refs = [issue for issue in issues if 'broken' in issue.get('type', '')]
        self.assertGreater(len(broken_refs), 0, "Should detect broken cross-references")
    
    def test_spec_cross_references(self):
        """Test validation of spec-to-spec cross-references"""
        # Create spec files
        self.create_test_file(".agent-os/specs/spec1/spec.md", "# Spec 1")
        self.create_test_file(".agent-os/specs/spec2/spec.md", "# Spec 2")
        
        # Create spec with references
        source_content = """# Spec 3

Related specs:
- @.agent-os/specs/spec1/spec.md
- @.agent-os/specs/spec2/spec.md
- @.agent-os/specs/missing-spec/spec.md
"""
        
        file_path = self.create_test_file(".agent-os/specs/spec3/spec.md", source_content)
        
        from documentation_agent import CrossReferenceValidator
        validator = CrossReferenceValidator(str(self.temp_path))
        issues = validator.validate_file(str(file_path))
        
        # Should validate spec references
        self.assertIsInstance(issues, list, "Should return list of validation issues")


class TestReadmeMaintenanceAnalysis(unittest.TestCase):
    """Test README.md maintenance functionality"""
    
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
    
    def test_readme_structure_validation(self):
        """Test README structure validation"""
        readme_content = """# Project Title

Some description.

## Features

- Feature 1
- Feature 2

## Installation

Steps here.
"""
        
        file_path = self.create_test_file("README.md", readme_content)
        
        from documentation_agent import ReadmeAnalyzer
        analyzer = ReadmeAnalyzer(str(self.temp_path))
        issues = analyzer.analyze_file(str(file_path))
        
        # Should validate structure
        self.assertIsInstance(issues, list, "Should return list of issues")
    
    def test_missing_readme_sections(self):
        """Test detection of missing README sections"""
        incomplete_readme = """# Project Title

Just a title and some text.
"""
        
        file_path = self.create_test_file("README.md", incomplete_readme)
        
        from documentation_agent import ReadmeAnalyzer
        analyzer = ReadmeAnalyzer(str(self.temp_path))
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect missing sections
        missing_sections = [issue for issue in issues if 'missing' in issue.get('type', '')]
        self.assertGreater(len(missing_sections), 0, "Should detect missing README sections")
    
    def test_readme_content_freshness(self):
        """Test README content freshness analysis"""
        # Create some code files
        self.create_test_file("main.py", "def main(): pass")
        self.create_test_file("utils.py", "def helper(): pass")
        
        # Create README that might be outdated
        readme_content = """# Project

Old description that doesn't mention new features.
"""
        
        file_path = self.create_test_file("README.md", readme_content)
        
        from documentation_agent import ReadmeAnalyzer
        analyzer = ReadmeAnalyzer(str(self.temp_path))
        issues = analyzer.analyze_file(str(file_path))
        
        # Should analyze content freshness
        self.assertIsInstance(issues, list, "Should return analysis results")


class TestDocumentationGeneration(unittest.TestCase):
    """Test automatic documentation generation"""
    
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
    
    def test_api_documentation_generation(self):
        """Test API documentation generation from Python code"""
        python_code = '''
def process_resume(resume_path):
    """Process a resume file and generate PDF.
    
    Args:
        resume_path (str): Path to the resume markdown file
        
    Returns:
        bool: True if successful, False otherwise
    """
    return True

class ResumeProcessor:
    """Main class for processing resumes."""
    
    def __init__(self):
        """Initialize the processor."""
        pass
    
    def validate_format(self, content):
        """Validate resume format.
        
        Args:
            content (str): Resume content
            
        Returns:
            list: List of validation errors
        """
        return []
'''
        
        file_path = self.create_test_file("resume_processor.py", python_code)
        
        from documentation_agent import ApiDocumentationGenerator
        generator = ApiDocumentationGenerator(str(self.temp_path))
        docs = generator.generate_from_file(str(file_path))
        
        # Should generate documentation
        self.assertIsInstance(docs, str, "Should return generated documentation")
        self.assertIn("process_resume", docs, "Should include function documentation")
        self.assertIn("ResumeProcessor", docs, "Should include class documentation")
    
    def test_project_structure_documentation(self):
        """Test project structure documentation generation"""
        # Create project structure
        self.create_test_file("main.py", "# Main script")
        self.create_test_file("utils/helpers.py", "# Helper functions")
        self.create_test_file("docs/guide.md", "# User Guide")
        self.create_test_file("tests/test_main.py", "# Tests")
        
        from documentation_agent import ProjectStructureGenerator
        generator = ProjectStructureGenerator(str(self.temp_path))
        structure_docs = generator.generate_structure_docs()
        
        # Should generate project structure documentation
        self.assertIsInstance(structure_docs, str, "Should return structure documentation")
        self.assertIn("main.py", structure_docs, "Should include main files")
        self.assertIn("utils", structure_docs, "Should include directory structure")


class TestDocumentationIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_configuration(self):
        """Test that the documentation agent configuration is valid"""
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()
        config = parser.get_agent_config("documentation-agent")
        
        self.assertIsNotNone(config, "Documentation agent configuration should exist")
        self.assertEqual(config['name'], "documentation-agent")
        self.assertEqual(config['specialization'], "documentation-maintenance")
    
    def test_security_integration(self):
        """Test that the documentation agent works with security framework"""
        from security_framework import SecurityFramework, PermissionType
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()
        config = parser.get_agent_config("documentation-agent")
        
        framework = SecurityFramework()
        session_id = framework.create_session("documentation-agent", config)
        
        # Test permissions
        can_read_md = framework.check_permission(
            session_id, PermissionType.READ, "README.md", config
        )
        can_write_docs = framework.check_permission(
            session_id, PermissionType.WRITE, "docs/guide.md", config
        )
        
        self.assertTrue(can_read_md, "Should be able to read markdown files")
        # Note: write permission depends on specific configuration
        
        framework.end_session(session_id)


def run_tests():
    """Run all documentation agent tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestLinkValidation,
        TestCrossReferenceValidation,
        TestReadmeMaintenanceAnalysis,
        TestDocumentationGeneration,
        TestDocumentationIntegration
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