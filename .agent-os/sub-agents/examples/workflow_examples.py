#!/usr/bin/env python3
"""
Workflow Examples for Sub-Agents System
Demonstrates advanced workflow creation and execution patterns
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration_handler import ClaudeCodeIntegration, AgentOSIntegration
from agent_coordinator import AgentCoordinator, WorkflowParser


def example_sequential_workflow():
    """Example: Create and run a sequential workflow"""
    print("=== Sequential Workflow Example ===")
    
    # Define a sequential workflow
    workflow = {
        'name': 'code-review-workflow',
        'description': 'Complete code review process',
        'execution': {'type': 'sequential'},
        'agents': ['code-quality-agent', 'documentation-agent'],
        'steps': [
            {
                'agent': 'code-quality-agent',
                'action': 'analyze',
                'parameters': {'target': '*.py'},
                'output_key': 'quality_results'
            },
            {
                'agent': 'documentation-agent',
                'action': 'update',
                'input_from': 'quality_results',
                'condition': 'quality_results.issues_found > 0'
            }
        ]
    }
    
    # Execute workflow
    coordinator = AgentCoordinator()
    result = coordinator.execute_workflow(workflow)
    
    print(f"Workflow Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    print(f"Agents Executed: {len(result['agent_results'])}")
    
    # Show agent results
    for agent_result in result['agent_results']:
        agent = agent_result.get('agent', 'unknown')
        status = agent_result.get('status', 'unknown')
        print(f"  • {agent}: {status}")


def example_parallel_workflow():
    """Example: Create and run a parallel workflow"""
    print("=== Parallel Workflow Example ===")
    
    # Define a parallel workflow
    workflow = {
        'name': 'maintenance-scan',
        'description': 'Parallel maintenance tasks',
        'execution': {'type': 'parallel', 'max_concurrent': 3},
        'agents': ['maintenance-agent', 'code-quality-agent', 'documentation-agent'],
        'steps': [
            {
                'agent': 'maintenance-agent',
                'action': 'security_scan',
                'parameters': {'scope': 'dependencies'}
            },
            {
                'agent': 'code-quality-agent',
                'action': 'quick_scan',
                'parameters': {'target': '*.py'}
            },
            {
                'agent': 'documentation-agent',
                'action': 'link_check',
                'parameters': {'scope': 'all'}
            }
        ]
    }
    
    # Execute workflow
    coordinator = AgentCoordinator()
    result = coordinator.execute_workflow(workflow)
    
    print(f"Workflow Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    print(f"Agents Executed: {len(result['agent_results'])}")
    
    # Show parallel execution results
    for agent_result in result['agent_results']:
        agent = agent_result.get('agent', 'unknown')
        status = agent_result.get('status', 'unknown')
        duration = agent_result.get('duration', 0)
        print(f"  • {agent}: {status} ({duration:.2f}s)")


def example_conditional_workflow():
    """Example: Workflow with conditional execution"""
    print("=== Conditional Workflow Example ===")
    
    # Define workflow with conditions
    workflow = {
        'name': 'adaptive-quality-check',
        'description': 'Quality check that adapts based on findings',
        'execution': {'type': 'sequential'},
        'agents': ['code-quality-agent', 'documentation-agent', 'content-generation-agent'],
        'steps': [
            {
                'agent': 'code-quality-agent',
                'action': 'analyze',
                'parameters': {'target': '*.py'},
                'output_key': 'quality_results'
            },
            {
                'agent': 'documentation-agent',
                'action': 'update',
                'condition': 'quality_results.issues_found > 0',
                'input_from': 'quality_results'
            },
            {
                'agent': 'content-generation-agent',
                'action': 'generate_report',
                'condition': 'quality_results.score < 80',
                'input_from': 'quality_results'
            }
        ]
    }
    
    # Execute workflow
    coordinator = AgentCoordinator()
    result = coordinator.execute_workflow(workflow)
    
    print(f"Workflow Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    
    # Show which steps were executed
    executed_agents = [r.get('agent') for r in result['agent_results']]
    skipped_agents = set(workflow['agents']) - set(executed_agents)
    
    print(f"Executed: {', '.join(executed_agents)}")
    if skipped_agents:
        print(f"Skipped: {', '.join(skipped_agents)}")


def example_mixed_workflow():
    """Example: Mixed sequential and parallel execution"""
    print("=== Mixed Workflow Example ===")
    
    # Define mixed workflow
    workflow = {
        'name': 'comprehensive-analysis',
        'description': 'Mixed sequential and parallel analysis',
        'execution': {'type': 'mixed'},
        'agents': ['code-quality-agent', 'maintenance-agent', 'documentation-agent', 'resume-processing-agent'],
        'steps': [
            {
                'agent': 'code-quality-agent',
                'action': 'initial_scan',
                'parameters': {'target': '*.py'},
                'output_key': 'quality_scan'
            },
            {
                'agent': 'maintenance-agent',
                'action': 'dependency_check',
                'parallel': True,
                'output_key': 'maintenance_scan'
            },
            {
                'agent': 'documentation-agent',
                'action': 'structure_check',
                'parallel': True,
                'output_key': 'docs_scan'
            },
            {
                'agent': 'resume-processing-agent',
                'action': 'generate_summary',
                'depends_on': ['code-quality-agent', 'maintenance-agent'],
                'input_from': 'quality_scan'
            }
        ]
    }
    
    # Execute workflow
    coordinator = AgentCoordinator()
    result = coordinator.execute_workflow(workflow)
    
    print(f"Workflow Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    
    # Show execution order and timing
    for i, agent_result in enumerate(result['agent_results'], 1):
        agent = agent_result.get('agent', 'unknown')
        status = agent_result.get('status', 'unknown')
        duration = agent_result.get('duration', 0)
        print(f"  {i}. {agent}: {status} ({duration:.2f}s)")


def example_workflow_validation():
    """Example: Validate workflow definitions"""
    print("=== Workflow Validation Example ===")
    
    parser = WorkflowParser()
    
    # Valid workflow
    valid_workflow = {
        'name': 'test-workflow',
        'agents': ['code-quality-agent'],
        'steps': [
            {'agent': 'code-quality-agent', 'action': 'test'}
        ]
    }
    
    # Invalid workflow (missing required fields)
    invalid_workflow = {
        'name': 'incomplete-workflow',
        # Missing 'agents' and 'steps'
    }
    
    # Test valid workflow
    try:
        validated = parser.parse_workflow_dict(valid_workflow)
        print("✅ Valid workflow parsed successfully")
        print(f"   Name: {validated['name']}")
        print(f"   Parsed at: {validated['parsed_at']}")
    except ValueError as e:
        print(f"❌ Valid workflow failed: {e}")
    
    # Test invalid workflow
    try:
        parser.parse_workflow_dict(invalid_workflow)
        print("❌ Invalid workflow should have failed validation")
    except ValueError as e:
        print(f"✅ Invalid workflow correctly rejected: {e}")


def example_workflow_with_error_handling():
    """Example: Workflow with comprehensive error handling"""
    print("=== Error Handling Workflow Example ===")
    
    # Define workflow that might have errors
    workflow = {
        'name': 'robust-analysis',
        'description': 'Analysis with error handling',
        'execution': {'type': 'sequential'},
        'agents': ['code-quality-agent', 'nonexistent-agent', 'documentation-agent'],
        'steps': [
            {
                'agent': 'code-quality-agent',
                'action': 'analyze',
                'parameters': {'target': '*.py'}
            },
            {
                'agent': 'nonexistent-agent',  # This will fail
                'action': 'fake_action'
            },
            {
                'agent': 'documentation-agent',
                'action': 'update'
            }
        ]
    }
    
    # Execute workflow with error handling
    coordinator = AgentCoordinator()
    result = coordinator.execute_workflow(workflow)
    
    print(f"Workflow Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    print(f"Successful agents: {len([r for r in result['agent_results'] if r.get('status') == 'success'])}")
    print(f"Failed agents: {len([r for r in result['agent_results'] if r.get('status') == 'error'])}")
    
    # Show errors
    errors = result.get('errors', [])
    if errors:
        print(f"\nErrors encountered ({len(errors)}):")
        for error in errors:
            print(f"  • Step {error.get('step', '?')}: {error.get('message', 'Unknown error')}")


def example_custom_workflow_creation():
    """Example: Create and save custom workflows"""
    print("=== Custom Workflow Creation Example ===")
    
    from integration_handler import ConfigurationManager
    
    config_manager = ConfigurationManager()
    
    # Create custom workflows for different scenarios
    workflows_to_create = [
        {
            'name': 'quick-check',
            'agents': ['code-quality-agent'],
            'execution_type': 'sequential'
        },
        {
            'name': 'full-maintenance',
            'agents': ['maintenance-agent', 'documentation-agent', 'code-quality-agent'],
            'execution_type': 'parallel'
        },
        {
            'name': 'content-pipeline',
            'agents': ['resume-processing-agent', 'content-generation-agent'],
            'execution_type': 'sequential'
        }
    ]
    
    created_workflows = []
    for workflow_def in workflows_to_create:
        success = config_manager.create_custom_workflow(**workflow_def)
        if success:
            created_workflows.append(workflow_def['name'])
            print(f"✅ Created: {workflow_def['name']}")
        else:
            print(f"❌ Failed to create: {workflow_def['name']}")
    
    # List all available workflows
    print(f"\nAvailable workflows after creation:")
    workflows = config_manager.list_available_workflows()
    for workflow in workflows:
        status = "✅ New" if workflow['name'] in created_workflows else "📁 Existing"
        print(f"  {status} {workflow['name']} ({workflow['type']})")


def main():
    """Run all workflow examples"""
    print("Sub-Agents Workflow Examples")
    print("=" * 50)
    
    examples = [
        example_sequential_workflow,
        example_parallel_workflow,
        example_conditional_workflow,
        example_mixed_workflow,
        example_workflow_validation,
        example_workflow_with_error_handling,
        example_custom_workflow_creation
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n{i}. {example_func.__doc__.split(':')[1].strip()}")
            print("-" * 40)
            example_func()
        except Exception as e:
            print(f"Error running example: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    main()