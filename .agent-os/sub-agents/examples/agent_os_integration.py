#!/usr/bin/env python3
"""
Agent OS Integration Examples
Demonstrates integration between sub-agents and Agent OS framework
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration_handler import AgentOSIntegration, ClaudeCodeIntegration


def example_discover_workflows():
    """Example: Discover Agent OS workflows with sub-agents"""
    print("=== Discovering Agent OS Workflows ===")
    
    integration = AgentOSIntegration()
    workflows = integration.discover_workflows()
    
    print(f"Found {len(workflows)} workflows:")
    for workflow in workflows:
        print(f"  • {workflow['name']}: {workflow.get('description', 'No description')}")
        agents = workflow.get('agents', [])
        if agents:
            print(f"    Agents: {', '.join(agents)}")
        print()


def example_validate_configuration():
    """Example: Validate Agent OS configuration"""
    print("=== Validating Agent OS Configuration ===")
    
    integration = AgentOSIntegration()
    config_status = integration.validate_configuration()
    
    print(f"Configuration Status:")
    print(f"  Valid: {'✅' if config_status['valid'] else '❌'}")
    print(f"  Agents Configured: {config_status['agents_configured']}")
    print(f"  Workflows Available: {config_status['workflows_available']}")
    
    if not config_status['valid']:
        issues = config_status.get('issues', [])
        if issues:
            print(f"\n⚠️ Configuration Issues:")
            for issue in issues:
                print(f"    • {issue}")


def example_spec_integration():
    """Example: Execute Agent OS spec with sub-agents"""
    print("=== Agent OS Spec Integration ===")
    
    integration = AgentOSIntegration()
    
    # Mock spec execution with sub-agents
    spec_result = integration.execute_spec_with_agents(
        spec_path='.agent-os/specs/test-spec',
        agents=['code-quality-agent', 'documentation-agent']
    )
    
    print(f"Spec Execution:")
    print(f"  Status: {spec_result['spec_status']}")
    print(f"  Agent Contributions: {len(spec_result['agent_contributions'])}")
    
    for contribution in spec_result['agent_contributions']:
        agent = contribution.get('agent', 'unknown')
        status = contribution.get('status', 'unknown')
        print(f"    • {agent}: {status}")


def example_claude_md_parsing():
    """Example: Parse CLAUDE.md for sub-agent instructions"""
    print("=== CLAUDE.md Integration ===")
    
    integration = AgentOSIntegration()
    claude_instructions = integration.parse_claude_md_instructions()
    
    print(f"CLAUDE.md Instructions:")
    print(f"  Sub-agent workflows: {len(claude_instructions.get('sub_agent_workflows', []))}")
    print(f"  Coordination rules: {len(claude_instructions.get('agent_coordination_rules', []))}")
    
    # Show workflow instructions
    workflows = claude_instructions.get('sub_agent_workflows', [])
    if workflows:
        print(f"\n  Available workflow instructions:")
        for workflow in workflows[:3]:  # Show first 3
            print(f"    • {workflow}")


def example_integrated_workflow():
    """Example: Run integrated Agent OS + sub-agents workflow"""
    print("=== Integrated Workflow Example ===")
    
    # Use Claude Code integration with Agent OS context
    claude_integration = ClaudeCodeIntegration()
    
    # Run workflow with Agent OS context
    result = claude_integration.execute_command('run-workflow', {
        'workflow': 'code-quality-check',
        'context': {
            'agent_os_spec': '.agent-os/specs/2025-07-25-sub-agents-enhancement',
            'spec_task': '8.2',  # Update CLAUDE.md with sub-agent documentation
            'integration_mode': True
        }
    })
    
    print(f"Integrated Workflow:")
    print(f"  Status: {result.get('status', 'unknown')}")
    print(f"  Workflow ID: {result.get('workflow_id', 'N/A')}")
    
    if result.get('status') == 'completed':
        agent_results = result.get('agent_results', [])
        print(f"  Agents executed: {len(agent_results)}")
        
        for agent_result in agent_results:
            agent = agent_result.get('agent', 'unknown')
            status = agent_result.get('status', 'unknown')
            print(f"    • {agent}: {status}")


def example_spec_workflow_coordination():
    """Example: Coordinate sub-agents with spec requirements"""
    print("=== Spec-Driven Workflow Coordination ===")
    
    integration = AgentOSIntegration()
    
    # Example spec requirements
    spec_requirements = {
        'spec_name': 'sub-agents-enhancement',
        'current_task': '8.2',
        'task_description': 'Update CLAUDE.md with sub-agent documentation',
        'required_agents': ['documentation-agent'],
        'success_criteria': ['CLAUDE.md updated', 'sub-agent commands documented']
    }
    
    # Execute spec-driven workflow
    result = integration.execute_spec_workflow(spec_requirements)
    
    print(f"Spec-Driven Execution:")
    print(f"  Spec: {spec_requirements['spec_name']}")
    print(f"  Task: {spec_requirements['current_task']}")
    print(f"  Status: {result.get('status', 'unknown')}")
    
    if result.get('status') == 'completed':
        print(f"  Success criteria met: {result.get('criteria_met', 0)}/{len(spec_requirements['success_criteria'])}")


def example_roadmap_integration():
    """Example: Integrate sub-agents with roadmap tracking"""
    print("=== Roadmap Integration Example ===")
    
    integration = AgentOSIntegration()
    
    # Check roadmap status with sub-agents
    roadmap_status = integration.check_roadmap_progress()
    
    print(f"Roadmap Integration:")
    print(f"  Current phase: {roadmap_status.get('current_phase', 'unknown')}")
    print(f"  Phase progress: {roadmap_status.get('phase_progress', 0)}%")
    print(f"  Sub-agents contribution: {roadmap_status.get('sub_agents_contribution', 'none')}")
    
    # Show relevant agents for current phase
    relevant_agents = roadmap_status.get('relevant_agents', [])
    if relevant_agents:
        print(f"  Relevant agents for current phase:")
        for agent in relevant_agents:
            print(f"    • {agent}")


def example_mission_alignment():
    """Example: Ensure sub-agents align with product mission"""
    print("=== Mission Alignment Check ===")
    
    integration = AgentOSIntegration()
    
    # Check mission alignment
    alignment_check = integration.validate_mission_alignment()
    
    print(f"Mission Alignment:")
    print(f"  Aligned: {'✅' if alignment_check['aligned'] else '❌'}")
    print(f"  Mission focus: {alignment_check.get('mission_focus', 'unknown')}")
    print(f"  Sub-agents contribution: {alignment_check.get('contribution_score', 0)}/100")
    
    # Show alignment details
    alignment_details = alignment_check.get('details', {})
    for agent, details in alignment_details.items():
        alignment_score = details.get('alignment_score', 0)
        contribution = details.get('contribution', 'none')
        print(f"  • {agent}: {alignment_score}% aligned ({contribution})")


def example_decision_tracking():
    """Example: Track decisions made by sub-agents"""
    print("=== Decision Tracking Example ===")
    
    integration = AgentOSIntegration()
    
    # Track decisions from sub-agent execution
    decisions = integration.track_agent_decisions()
    
    print(f"Agent Decisions Tracking:")
    print(f"  Decisions recorded: {len(decisions)}")
    
    for decision in decisions:
        print(f"  • {decision.get('date', 'unknown')}: {decision.get('decision', 'no description')}")
        print(f"    Agent: {decision.get('agent', 'unknown')}")
        print(f"    Impact: {decision.get('impact', 'unknown')}")
        print()


def main():
    """Run all Agent OS integration examples"""
    print("Agent OS Integration Examples")
    print("=" * 50)
    
    examples = [
        example_discover_workflows,
        example_validate_configuration,
        example_spec_integration,
        example_claude_md_parsing,
        example_integrated_workflow,
        example_spec_workflow_coordination,
        example_roadmap_integration,
        example_mission_alignment,
        example_decision_tracking
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n{i}. {example_func.__doc__.split(':')[1].strip()}")
            print("-" * 40)
            example_func()
        except Exception as e:
            print(f"Error running example: {e}")
            # Note: Some examples use mock methods that may not be fully implemented
            print("(Note: Some Agent OS integration features are demonstration examples)")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    main()