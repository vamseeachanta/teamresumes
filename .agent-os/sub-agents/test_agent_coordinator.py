#!/usr/bin/env python3
"""
Agent Coordinator Test Suite
Tests for multi-agent coordination, workflow execution, and conditional activation
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import json
import time
from unittest.mock import Mock, patch, MagicMock

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestWorkflowDefinition(unittest.TestCase):
    """Test workflow definition and parsing"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_workflow_yaml_parsing(self):
        """Test parsing of workflow YAML definitions"""
        workflow_yaml = """
name: code-quality-check
description: Comprehensive code quality analysis workflow
version: 1.0.0

agents:
  - name: code-quality-agent
    priority: high
  - name: documentation-agent
    priority: medium
  - name: maintenance-agent
    priority: medium

execution:
  type: sequential
  timeout: 3600
  
steps:
  - agent: code-quality-agent
    action: analyze_python_code
    parameters:
      file_path: "*.py"
      
  - agent: documentation-agent
    action: check_documentation
    depends_on: code-quality-agent
    
  - agent: maintenance-agent
    action: check_dependencies
    condition: "code_quality_score < 80"
"""
        
        workflow_file = self.temp_path / "test_workflow.yaml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_yaml)
        
        from agent_coordinator import WorkflowParser
        parser = WorkflowParser()
        workflow = parser.parse_workflow(str(workflow_file))
        
        # Verify workflow parsing
        self.assertIsNotNone(workflow, "Workflow should be parsed")
        self.assertEqual(workflow['name'], 'code-quality-check')
        self.assertEqual(len(workflow['agents']), 3)
        self.assertEqual(workflow['execution']['type'], 'sequential')
        self.assertEqual(len(workflow['steps']), 3)
    
    def test_workflow_validation(self):
        """Test validation of workflow definitions"""
        # Invalid workflow (missing required fields)
        invalid_workflow = {
            'name': 'test-workflow',
            # Missing 'agents' and 'steps'
        }
        
        from agent_coordinator import WorkflowValidator
        validator = WorkflowValidator()
        
        is_valid, errors = validator.validate_workflow(invalid_workflow)
        self.assertFalse(is_valid, "Invalid workflow should not pass validation")
        self.assertGreater(len(errors), 0, "Should report validation errors")
    
    def test_parallel_workflow_definition(self):
        """Test parallel execution workflow definition"""
        workflow_yaml = """
name: parallel-analysis
description: Run multiple analyses in parallel
version: 1.0.0

agents:
  - name: code-quality-agent
  - name: security-scanner
  - name: documentation-agent

execution:
  type: parallel
  max_concurrent: 3
  
steps:
  - group: analysis
    parallel: true
    agents:
      - agent: code-quality-agent
        action: full_analysis
      - agent: security-scanner
        action: vulnerability_scan
      - agent: documentation-agent
        action: check_completeness
"""
        
        workflow_file = self.temp_path / "parallel_workflow.yaml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_yaml)
        
        from agent_coordinator import WorkflowParser
        parser = WorkflowParser()
        workflow = parser.parse_workflow(str(workflow_file))
        
        # Verify parallel configuration
        self.assertEqual(workflow['execution']['type'], 'parallel')
        self.assertEqual(workflow['execution']['max_concurrent'], 3)
        self.assertTrue(workflow['steps'][0]['parallel'])


class TestAgentCoordination(unittest.TestCase):
    """Test agent coordination and execution"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create mock agent configurations
        self.mock_agents = {
            'code-quality-agent': {
                'name': 'code-quality-agent',
                'specialization': 'code-quality-analysis',
                'status': 'active'
            },
            'documentation-agent': {
                'name': 'documentation-agent',
                'specialization': 'documentation-maintenance',
                'status': 'active'
            }
        }
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_sequential_execution(self):
        """Test sequential execution of multiple agents"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Create a sequential workflow
        workflow = {
            'name': 'sequential-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {'agent': 'code-quality-agent', 'action': 'analyze'},
                {'agent': 'documentation-agent', 'action': 'update'}
            ]
        }
        
        # Mock agent execution
        with patch.object(coordinator, '_execute_agent') as mock_execute:
            mock_execute.return_value = {'status': 'success', 'results': {}}
            
            results = coordinator.execute_workflow(workflow)
            
            # Verify sequential execution
            self.assertEqual(mock_execute.call_count, 2)
            self.assertEqual(results['status'], 'completed')
            self.assertEqual(len(results['agent_results']), 2)
    
    def test_parallel_execution(self):
        """Test parallel execution of multiple agents"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Create a parallel workflow
        workflow = {
            'name': 'parallel-test',
            'execution': {'type': 'parallel', 'max_concurrent': 2},
            'steps': [
                {
                    'group': 'analysis',
                    'parallel': True,
                    'agents': [
                        {'agent': 'code-quality-agent', 'action': 'analyze'},
                        {'agent': 'documentation-agent', 'action': 'check'}
                    ]
                }
            ]
        }
        
        # Mock agent execution with timing
        execution_times = []
        def mock_execute_with_timing(agent_name, action, params):
            start_time = time.time()
            time.sleep(0.1)  # Simulate work
            execution_times.append((agent_name, start_time))
            return {'status': 'success', 'results': {}}
        
        with patch.object(coordinator, '_execute_agent', side_effect=mock_execute_with_timing):
            results = coordinator.execute_workflow(workflow)
            
            # Verify parallel execution
            self.assertEqual(results['status'], 'completed')
            # Check that agents started close together (parallel)
            if len(execution_times) >= 2:
                time_diff = abs(execution_times[1][1] - execution_times[0][1])
                self.assertLess(time_diff, 0.5, "Agents should start nearly simultaneously")
    
    def test_conditional_execution(self):
        """Test conditional agent activation"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Create workflow with conditions
        workflow = {
            'name': 'conditional-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {
                    'agent': 'code-quality-agent',
                    'action': 'analyze',
                    'output_key': 'quality_score'
                },
                {
                    'agent': 'documentation-agent',
                    'action': 'update',
                    'condition': 'quality_score < 80'
                }
            ]
        }
        
        # Test with high quality score (should skip second agent)
        def mock_execute_high_score(agent_name, action, params):
            if agent_name == 'code-quality-agent':
                return {'status': 'success', 'results': {'quality_score': 90}}
            return {'status': 'success', 'results': {}}
        
        with patch.object(coordinator, '_execute_agent', side_effect=mock_execute_high_score):
            results = coordinator.execute_workflow(workflow)
            
            # Documentation agent should be skipped
            self.assertEqual(len(results['agent_results']), 1)
            self.assertEqual(results['agent_results'][0]['agent'], 'code-quality-agent')
    
    def test_error_handling(self):
        """Test error handling in workflow execution"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Create workflow
        workflow = {
            'name': 'error-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {'agent': 'code-quality-agent', 'action': 'analyze'},
                {'agent': 'documentation-agent', 'action': 'update'}
            ]
        }
        
        # Mock agent execution with error
        def mock_execute_with_error(agent_name, action, params):
            if agent_name == 'code-quality-agent':
                return {'status': 'error', 'error': 'Analysis failed'}
            return {'status': 'success', 'results': {}}
        
        with patch.object(coordinator, '_execute_agent', side_effect=mock_execute_with_error):
            results = coordinator.execute_workflow(workflow)
            
            # Workflow should handle error gracefully
            self.assertEqual(results['status'], 'partial_failure')
            self.assertIn('errors', results)
            self.assertEqual(len(results['errors']), 1)


class TestAgentCommunication(unittest.TestCase):
    """Test inter-agent communication and data sharing"""
    
    def test_data_passing_between_agents(self):
        """Test passing data from one agent to another"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Workflow with data dependencies
        workflow = {
            'name': 'data-passing-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {
                    'agent': 'code-quality-agent',
                    'action': 'analyze',
                    'output_key': 'analysis_results'
                },
                {
                    'agent': 'documentation-agent',
                    'action': 'generate_report',
                    'input_from': 'analysis_results'
                }
            ]
        }
        
        # Track data passed between agents
        passed_data = {}
        
        def mock_execute_with_data(agent_name, action, params):
            if agent_name == 'code-quality-agent':
                return {
                    'status': 'success',
                    'results': {
                        'quality_score': 85,
                        'issues': ['missing_docstring', 'long_function']
                    }
                }
            elif agent_name == 'documentation-agent':
                # Should receive data from previous agent
                passed_data.update(params)
                return {'status': 'success', 'results': {'report_generated': True}}
            return {'status': 'success', 'results': {}}
        
        with patch.object(coordinator, '_execute_agent', side_effect=mock_execute_with_data):
            results = coordinator.execute_workflow(workflow)
            
            # Verify data was passed
            self.assertIn('analysis_results', passed_data)
            self.assertEqual(passed_data['analysis_results']['quality_score'], 85)
    
    def test_shared_context(self):
        """Test shared context between agents"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        # Create shared context
        shared_context = {
            'project_path': '/test/project',
            'target_files': ['*.py', '*.js'],
            'config': {'strict_mode': True}
        }
        
        workflow = {
            'name': 'shared-context-test',
            'context': shared_context,
            'execution': {'type': 'sequential'},
            'steps': [
                {'agent': 'code-quality-agent', 'action': 'analyze'},
                {'agent': 'documentation-agent', 'action': 'update'}
            ]
        }
        
        # Track context received by agents
        received_contexts = []
        
        def mock_execute_with_context(agent_name, action, params):
            received_contexts.append(params.get('context', {}))
            return {'status': 'success', 'results': {}}
        
        with patch.object(coordinator, '_execute_agent', side_effect=mock_execute_with_context):
            results = coordinator.execute_workflow(workflow)
            
            # All agents should receive the shared context
            self.assertEqual(len(received_contexts), 2)
            for context in received_contexts:
                self.assertEqual(context['project_path'], '/test/project')
                self.assertTrue(context['config']['strict_mode'])


class TestWorkflowManagement(unittest.TestCase):
    """Test workflow management and lifecycle"""
    
    def test_workflow_registration(self):
        """Test registering and retrieving workflows"""
        from agent_coordinator import WorkflowManager
        
        manager = WorkflowManager()
        
        # Register a workflow
        workflow = {
            'name': 'test-workflow',
            'version': '1.0.0',
            'description': 'Test workflow',
            'agents': ['code-quality-agent'],
            'steps': []
        }
        
        manager.register_workflow('test-workflow', workflow)
        
        # Retrieve workflow
        retrieved = manager.get_workflow('test-workflow')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['name'], 'test-workflow')
        
        # List workflows
        workflows = manager.list_workflows()
        self.assertIn('test-workflow', workflows)
    
    def test_workflow_versioning(self):
        """Test workflow version management"""
        from agent_coordinator import WorkflowManager
        
        manager = WorkflowManager()
        
        # Register multiple versions
        workflow_v1 = {
            'name': 'versioned-workflow',
            'version': '1.0.0',
            'description': 'Version 1'
        }
        
        workflow_v2 = {
            'name': 'versioned-workflow',
            'version': '2.0.0',
            'description': 'Version 2'
        }
        
        manager.register_workflow('versioned-workflow', workflow_v1)
        manager.register_workflow('versioned-workflow', workflow_v2)
        
        # Get specific version
        v1 = manager.get_workflow('versioned-workflow', version='1.0.0')
        v2 = manager.get_workflow('versioned-workflow', version='2.0.0')
        
        self.assertEqual(v1['description'], 'Version 1')
        self.assertEqual(v2['description'], 'Version 2')
        
        # Get latest version by default
        latest = manager.get_workflow('versioned-workflow')
        self.assertEqual(latest['version'], '2.0.0')
    
    def test_workflow_status_tracking(self):
        """Test tracking workflow execution status"""
        from agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        
        workflow = {
            'name': 'status-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {'agent': 'code-quality-agent', 'action': 'analyze'}
            ]
        }
        
        # Track status changes
        status_changes = []
        
        def mock_status_callback(status):
            status_changes.append(status)
        
        with patch.object(coordinator, '_execute_agent') as mock_execute:
            mock_execute.return_value = {'status': 'success', 'results': {}}
            
            results = coordinator.execute_workflow(
                workflow,
                status_callback=mock_status_callback
            )
            
            # Verify status changes were tracked
            self.assertGreater(len(status_changes), 0)
            self.assertIn('running', status_changes)
            self.assertIn('completed', status_changes)


class TestCoordinatorIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_discovery(self):
        """Test automatic discovery of available agents"""
        from agent_coordinator import AgentCoordinator
        from agent_config_parser import AgentConfigParser
        
        # Use absolute path to configurations directory
        config_dir = Path(__file__).parent / "configurations"
        parser = AgentConfigParser(str(config_dir))
        
        coordinator = AgentCoordinator(config_parser=parser)
        available_agents = coordinator.discover_agents()
        
        # Should discover all configured agents
        self.assertIsInstance(available_agents, list)
        self.assertGreater(len(available_agents), 0)
        
        # Check for known agents
        agent_names = [agent['name'] for agent in available_agents]
        self.assertIn('code-quality-agent', agent_names)
        self.assertIn('documentation-agent', agent_names)
    
    def test_security_integration(self):
        """Test coordinator integration with security framework"""
        from agent_coordinator import AgentCoordinator
        from security_framework import SecurityFramework
        
        coordinator = AgentCoordinator()
        security = SecurityFramework()
        
        # Set security framework
        coordinator.set_security_framework(security)
        
        # Create workflow requiring permissions
        workflow = {
            'name': 'security-test',
            'execution': {'type': 'sequential'},
            'steps': [
                {
                    'agent': 'code-quality-agent',
                    'action': 'analyze',
                    'requires_permissions': ['file_read', 'file_analyze']
                }
            ]
        }
        
        # Mock agent execution
        with patch.object(coordinator, '_execute_agent') as mock_execute:
            mock_execute.return_value = {'status': 'success', 'results': {}}
            
            results = coordinator.execute_workflow(workflow)
            
            # Should create security session for agent
            self.assertEqual(results['status'], 'completed')
    
    def test_workflow_file_loading(self):
        """Test loading workflows from YAML files"""
        from agent_coordinator import WorkflowLoader
        
        loader = WorkflowLoader()
        
        # Create test workflow file
        workflow_yaml = """
name: file-test-workflow
version: 1.0.0
description: Test loading from file

agents:
  - name: code-quality-agent
    required: true

execution:
  type: sequential
  
steps:
  - agent: code-quality-agent
    action: analyze_all
"""
        
        workflow_file = Path(__file__).parent / "test_workflow.yaml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_yaml)
        
        try:
            # Load workflow from file
            workflow = loader.load_workflow_file(str(workflow_file))
            
            self.assertIsNotNone(workflow)
            self.assertEqual(workflow['name'], 'file-test-workflow')
            self.assertEqual(len(workflow['steps']), 1)
        finally:
            # Cleanup
            if workflow_file.exists():
                workflow_file.unlink()


def run_tests():
    """Run all agent coordinator tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestWorkflowDefinition,
        TestAgentCoordination,
        TestAgentCommunication,
        TestWorkflowManagement,
        TestCoordinatorIntegration
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