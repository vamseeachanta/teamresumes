#!/usr/bin/env python3
"""
Integration Test Suite
Tests for integration with Claude Code and Agent OS framework
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import json
from unittest.mock import Mock, patch, MagicMock

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestClaudeCodeIntegration(unittest.TestCase):
    """Test integration with Claude Code interface"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_sub_agent_command_registration(self):
        """Test registration of sub-agent commands with Claude Code"""
        from integration_handler import ClaudeCodeIntegration
        
        integration = ClaudeCodeIntegration()
        commands = integration.get_registered_commands()
        
        # Should register sub-agent commands
        self.assertIsInstance(commands, dict)
        self.assertIn('run-agent', commands)
        self.assertIn('run-workflow', commands)
        self.assertIn('list-agents', commands)
        self.assertIn('agent-status', commands)
    
    def test_agent_command_execution(self):
        """Test execution of agent commands through Claude Code interface"""
        from integration_handler import ClaudeCodeIntegration
        
        integration = ClaudeCodeIntegration()
        
        # Test single agent execution
        result = integration.execute_command('run-agent', {
            'agent': 'code-quality-agent',
            'action': 'analyze',
            'target': '*.py'
        })
        
        # Should return structured result
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('agent', result)
        self.assertIn('results', result)
    
    def test_workflow_command_execution(self):
        """Test workflow execution through Claude Code interface"""
        from integration_handler import ClaudeCodeIntegration
        
        integration = ClaudeCodeIntegration()
        
        # Test workflow execution
        result = integration.execute_command('run-workflow', {
            'workflow': 'code-quality-check',
            'context': {'project_path': str(self.temp_path)}
        })
        
        # Should return workflow results
        self.assertIsInstance(result, dict)
        self.assertIn('workflow_id', result)
        self.assertIn('status', result)
        self.assertIn('agent_results', result)
    
    def test_agent_listing(self):
        """Test listing available agents"""
        from integration_handler import ClaudeCodeIntegration
        
        integration = ClaudeCodeIntegration()
        
        result = integration.execute_command('list-agents', {})
        
        # Should return list of available agents
        self.assertIsInstance(result, dict)
        self.assertIn('agents', result)
        self.assertIsInstance(result['agents'], list)
        
        # Check agent information structure
        if result['agents']:
            agent = result['agents'][0]
            self.assertIn('name', agent)
            self.assertIn('specialization', agent)
            self.assertIn('status', agent)
    
    def test_agent_status_monitoring(self):
        """Test agent status monitoring"""
        from integration_handler import ClaudeCodeIntegration
        
        integration = ClaudeCodeIntegration()
        
        result = integration.execute_command('agent-status', {
            'agent': 'code-quality-agent'
        })
        
        # Should return agent status information
        self.assertIsInstance(result, dict)
        self.assertIn('agent', result)
        self.assertIn('status', result)
        self.assertIn('last_execution', result)


class TestAgentOSIntegration(unittest.TestCase):
    """Test integration with Agent OS framework"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_agent_os_workflow_integration(self):
        """Test integration with Agent OS workflow system"""
        from integration_handler import AgentOSIntegration
        
        integration = AgentOSIntegration()
        
        # Test workflow discovery
        workflows = integration.discover_workflows()
        
        self.assertIsInstance(workflows, list)
        
        # Should include predefined workflows
        workflow_names = [w['name'] for w in workflows]
        self.assertIn('code-quality-check', workflow_names)
        self.assertIn('resume-processing', workflow_names)
    
    def test_agent_os_configuration_sync(self):
        """Test synchronization with Agent OS configuration"""
        from integration_handler import AgentOSIntegration
        
        integration = AgentOSIntegration()
        
        # Test configuration validation
        config_status = integration.validate_configuration()
        
        self.assertIsInstance(config_status, dict)
        self.assertIn('valid', config_status)
        self.assertIn('agents_configured', config_status)
        self.assertIn('workflows_available', config_status)
    
    def test_agent_os_spec_integration(self):
        """Test integration with Agent OS spec system"""
        from integration_handler import AgentOSIntegration
        
        integration = AgentOSIntegration()
        
        # Test spec execution with sub-agents
        spec_result = integration.execute_spec_with_agents(
            spec_path='.agent-os/specs/test-spec',
            agents=['code-quality-agent', 'documentation-agent']
        )
        
        self.assertIsInstance(spec_result, dict)
        self.assertIn('spec_status', spec_result)
        self.assertIn('agent_contributions', spec_result)
    
    def test_claude_md_integration(self):
        """Test integration with CLAUDE.md instructions"""
        from integration_handler import AgentOSIntegration
        
        integration = AgentOSIntegration()
        
        # Test CLAUDE.md parsing for sub-agent instructions
        claude_instructions = integration.parse_claude_md_instructions()
        
        self.assertIsInstance(claude_instructions, dict)
        self.assertIn('sub_agent_workflows', claude_instructions)
        self.assertIn('agent_coordination_rules', claude_instructions)


class TestResultDisplayAndFormatting(unittest.TestCase):
    """Test result display and formatting functionality"""
    
    def test_agent_result_formatting(self):
        """Test formatting of agent execution results"""
        from integration_handler import ResultFormatter
        
        formatter = ResultFormatter()
        
        # Mock agent result
        agent_result = {
            'agent': 'code-quality-agent',
            'status': 'success',
            'duration': 15.5,
            'results': {
                'quality_score': 85,
                'issues_found': 3,
                'recommendations': ['Add more comments', 'Reduce complexity']
            }
        }
        
        formatted = formatter.format_agent_result(agent_result)
        
        # Should return formatted string
        self.assertIsInstance(formatted, str)
        self.assertIn('code-quality-agent', formatted)
        self.assertIn('85', formatted)  # Quality score
        self.assertIn('15.5s', formatted)  # Duration
    
    def test_workflow_result_formatting(self):
        """Test formatting of workflow execution results"""
        from integration_handler import ResultFormatter
        
        formatter = ResultFormatter()
        
        # Mock workflow result
        workflow_result = {
            'workflow_name': 'code-quality-check',
            'status': 'completed',
            'duration_seconds': 45.2,
            'agent_results': [
                {
                    'agent': 'code-quality-agent',
                    'status': 'success',
                    'results': {'quality_score': 85}
                },
                {
                    'agent': 'documentation-agent',
                    'status': 'success',
                    'results': {'docs_updated': True}
                }
            ],
            'errors': []
        }
        
        formatted = formatter.format_workflow_result(workflow_result)
        
        # Should return formatted workflow summary
        self.assertIsInstance(formatted, str)
        self.assertIn('code-quality-check', formatted)
        self.assertIn('completed', formatted)
        self.assertIn('45.2s', formatted)
        self.assertIn('2 agents', formatted)
    
    def test_error_result_formatting(self):
        """Test formatting of error results"""
        from integration_handler import ResultFormatter
        
        formatter = ResultFormatter()
        
        # Mock error result
        error_result = {
            'agent': 'maintenance-agent',
            'status': 'error',
            'error': 'Failed to scan dependencies',
            'timestamp': '2025-07-27T10:30:00'
        }
        
        formatted = formatter.format_error_result(error_result)
        
        # Should return formatted error message
        self.assertIsInstance(formatted, str)
        self.assertIn('ERROR', formatted.upper())
        self.assertIn('maintenance-agent', formatted)
        self.assertIn('Failed to scan dependencies', formatted)
    
    def test_progress_display(self):
        """Test real-time progress display"""
        from integration_handler import ProgressDisplay
        
        display = ProgressDisplay()
        
        # Test progress updates
        display.start_workflow('test-workflow', 3)
        display.update_agent_progress('code-quality-agent', 'running', 50)
        display.update_agent_progress('documentation-agent', 'completed', 100)
        progress_text = display.get_current_display()
        
        # Should show current progress
        self.assertIsInstance(progress_text, str)
        self.assertIn('test-workflow', progress_text)
        self.assertIn('50%', progress_text)
        self.assertIn('completed', progress_text)


class TestUserCommands(unittest.TestCase):
    """Test user command interface"""
    
    def test_command_parsing(self):
        """Test parsing of user commands"""
        from integration_handler import CommandParser
        
        parser = CommandParser()
        
        # Test various command formats
        test_commands = [
            "run agent code-quality-agent on *.py",
            "execute workflow code-quality-check",
            "list agents",
            "show agent status for maintenance-agent",
            "run workflow resume-processing with context project_path=."
        ]
        
        for command in test_commands:
            parsed = parser.parse_command(command)
            self.assertIsInstance(parsed, dict)
            self.assertIn('action', parsed)
            self.assertIn('parameters', parsed)
    
    def test_command_validation(self):
        """Test validation of user commands"""
        from integration_handler import CommandValidator
        
        validator = CommandValidator()
        
        # Test valid commands
        valid_command = {
            'action': 'run_agent',
            'parameters': {
                'agent': 'code-quality-agent',
                'target': '*.py'
            }
        }
        
        is_valid, errors = validator.validate_command(valid_command)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test invalid commands
        invalid_command = {
            'action': 'run_agent',
            'parameters': {
                # Missing required 'agent' parameter
                'target': '*.py'
            }
        }
        
        is_valid, errors = validator.validate_command(invalid_command)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_help_generation(self):
        """Test automatic help generation"""
        from integration_handler import HelpGenerator
        
        help_gen = HelpGenerator()
        
        # Test general help
        general_help = help_gen.generate_general_help()
        self.assertIsInstance(general_help, str)
        self.assertIn('sub-agent', general_help.lower())
        self.assertIn('workflow', general_help.lower())
        
        # Test agent-specific help
        agent_help = help_gen.generate_agent_help('code-quality-agent')
        self.assertIsInstance(agent_help, str)
        self.assertIn('code-quality-agent', agent_help)
        
        # Test workflow help
        workflow_help = help_gen.generate_workflow_help('code-quality-check')
        self.assertIsInstance(workflow_help, str)
        self.assertIn('code-quality-check', workflow_help)


class TestLoggingAndMonitoring(unittest.TestCase):
    """Test logging and monitoring integration"""
    
    def test_execution_logging(self):
        """Test logging of agent and workflow executions"""
        from integration_handler import ExecutionLogger
        
        logger = ExecutionLogger()
        
        # Test agent execution logging
        logger.log_agent_execution(
            agent='code-quality-agent',
            action='analyze',
            status='success',
            duration=15.5,
            results={'quality_score': 85}
        )
        
        # Test workflow execution logging
        logger.log_workflow_execution(
            workflow='code-quality-check',
            status='completed',
            duration=45.2,
            agents_executed=['code-quality-agent', 'documentation-agent']
        )
        
        # Verify logs are recorded
        execution_history = logger.get_execution_history()
        self.assertIsInstance(execution_history, list)
        self.assertGreater(len(execution_history), 0)
    
    def test_performance_monitoring(self):
        """Test performance monitoring integration"""
        from integration_handler import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # Start monitoring
        session_id = monitor.start_monitoring_session('test-workflow')
        
        # Record metrics
        monitor.record_agent_metrics(session_id, 'code-quality-agent', {
            'cpu_usage': 45.2,
            'memory_usage': 128.5,
            'execution_time': 15.3
        })
        
        # Get performance summary
        summary = monitor.get_performance_summary(session_id)
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_cpu_usage', summary)
        self.assertIn('peak_memory_usage', summary)
        self.assertIn('total_execution_time', summary)
    
    def test_error_tracking(self):
        """Test error tracking and reporting"""
        from integration_handler import ErrorTracker
        
        tracker = ErrorTracker()
        
        # Record errors
        tracker.record_error(
            component='agent_coordinator',
            error_type='agent_failure',
            message='Code quality agent failed to analyze file',
            context={'agent': 'code-quality-agent', 'file': 'test.py'}
        )
        
        # Get error statistics
        error_stats = tracker.get_error_statistics()
        
        self.assertIsInstance(error_stats, dict)
        self.assertIn('total_errors', error_stats)
        self.assertIn('errors_by_type', error_stats)
        self.assertIn('recent_errors', error_stats)


class TestConfigurationManagement(unittest.TestCase):
    """Test configuration management integration"""
    
    def test_agent_configuration_updates(self):
        """Test updating agent configurations"""
        from integration_handler import ConfigurationManager
        
        config_manager = ConfigurationManager()
        
        # Test configuration update
        updated = config_manager.update_agent_config(
            agent='code-quality-agent',
            updates={
                'behavior': {
                    'analysis_depth': 'comprehensive',
                    'report_format': 'detailed'
                }
            }
        )
        
        self.assertTrue(updated)
        
        # Verify configuration was updated
        current_config = config_manager.get_agent_config('code-quality-agent')
        self.assertEqual(
            current_config['behavior']['analysis_depth'],
            'comprehensive'
        )
    
    def test_workflow_configuration_management(self):
        """Test workflow configuration management"""
        from integration_handler import ConfigurationManager
        
        config_manager = ConfigurationManager()
        
        # Test creating custom workflow
        workflow_created = config_manager.create_custom_workflow(
            name='custom-quality-check',
            agents=['code-quality-agent', 'maintenance-agent'],
            execution_type='sequential'
        )
        
        self.assertTrue(workflow_created)
        
        # Verify workflow exists
        available_workflows = config_manager.list_available_workflows()
        workflow_names = [w['name'] for w in available_workflows]
        self.assertIn('custom-quality-check', workflow_names)
    
    def test_global_settings_management(self):
        """Test global settings management"""
        from integration_handler import ConfigurationManager
        
        config_manager = ConfigurationManager()
        
        # Test updating global settings
        settings_updated = config_manager.update_global_settings({
            'max_concurrent_agents': 5,
            'default_timeout': 600,
            'enable_audit_logging': True
        })
        
        self.assertTrue(settings_updated)
        
        # Verify settings were applied
        current_settings = config_manager.get_global_settings()
        self.assertEqual(current_settings['max_concurrent_agents'], 5)
        self.assertEqual(current_settings['default_timeout'], 600)
        self.assertTrue(current_settings['enable_audit_logging'])


def run_tests():
    """Run all integration tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestClaudeCodeIntegration,
        TestAgentOSIntegration,
        TestResultDisplayAndFormatting,
        TestUserCommands,
        TestLoggingAndMonitoring,
        TestConfigurationManagement
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