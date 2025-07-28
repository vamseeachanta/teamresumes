# Agent Coordination Prompt Templates

> Specialized prompts for multi-agent orchestration, workflow execution, and coordination
> Version: 1.0.0
> Created: 2025-07-27

## Workflow Execution

### Sequential Workflow Coordination

```
Execute sequential workflow "{workflow_name}" with the following agents:

**Execution Plan:**
1. **Agent Sequence:** {agent_list}
2. **Total Estimated Time:** {estimated_duration}
3. **Success Criteria:** {success_criteria}

**Coordination Requirements:**
- Wait for each agent to complete before starting the next
- Pass output data between agents as specified
- Monitor for failures and handle gracefully
- Maintain execution context throughout workflow

**Agent Handoff Protocol:**
- Agent A completes → validate output → prepare input for Agent B
- Include shared context: {shared_context}
- Error handling: {error_strategy}

**Progress Tracking:**
- Report status after each agent completion
- Log execution times and resource usage
- Maintain audit trail for coordination decisions

**Final Deliverables:**
- Consolidated results from all agents
- Execution summary with timing metrics
- Any errors or warnings encountered
```

### Parallel Workflow Coordination

```
Execute parallel workflow "{workflow_name}" with concurrent agent execution:

**Parallel Execution Setup:**
- **Agents to Run Simultaneously:** {parallel_agents}
- **Maximum Concurrency:** {max_concurrent}
- **Resource Allocation:** {resource_limits}

**Coordination Strategy:**
- Launch all agents simultaneously
- Monitor progress independently
- Aggregate results as agents complete
- Handle varying completion times

**Resource Management:**
- CPU allocation per agent: {cpu_allocation}
- Memory limits per agent: {memory_limits}
- File system coordination: {file_locking}
- Network bandwidth sharing: {network_policy}

**Synchronization Points:**
- Data dependencies: {data_dependencies}
- Completion barriers: {completion_barriers}
- Result aggregation: {aggregation_strategy}

**Performance Optimization:**
- Load balancing across agents
- Early termination on critical failures
- Resource scaling based on workload
- Deadlock prevention mechanisms
```

### Mixed Execution Workflow

```
Execute mixed workflow "{workflow_name}" combining sequential and parallel phases:

**Execution Phases:**
1. **Sequential Phase:** {sequential_agents}
   - Dependencies: {dependencies}
   - Data flow: {data_flow}

2. **Parallel Phase:** {parallel_agents}
   - Concurrent execution groups: {execution_groups}
   - Synchronization requirements: {sync_requirements}

3. **Final Sequential Phase:** {final_agents}
   - Result consolidation: {consolidation_strategy}
   - Cleanup operations: {cleanup_tasks}

**Phase Transitions:**
- Sequential → Parallel: {transition_criteria_1}
- Parallel → Sequential: {transition_criteria_2}
- Data passing between phases: {inter_phase_data}

**Coordination Challenges:**
- Managing state between phases
- Handling partial failures in parallel phase
- Maintaining data consistency
- Resource cleanup after each phase
```

## Conditional Agent Activation

### Condition-Based Execution

```
Evaluate conditions for agent activation in workflow "{workflow_name}":

**Conditional Logic:**
- **Primary Condition:** {primary_condition}
- **Secondary Conditions:** {secondary_conditions}
- **Fallback Behavior:** {fallback_behavior}

**Condition Evaluation:**
```javascript
if ({condition_expression}) {
    activate_agent("{agent_name}");
    parameters = {conditional_parameters};
} else {
    log_skip_reason("{skip_reason}");
    proceed_to_next_step();
}
```

**Dynamic Parameter Adjustment:**
- Adjust agent parameters based on condition results
- Modify execution priority based on context
- Set timeout values based on workload assessment

**Decision Documentation:**
- Log all condition evaluations
- Record parameter adjustments made
- Document skip reasons for audit trail
```

### Quality Gate Implementation

```
Implement quality gates for workflow progression:

**Quality Metrics Evaluation:**
- **Code Quality Score:** Must be >= {quality_threshold}
- **Security Vulnerability Count:** Must be <= {security_threshold}
- **Test Coverage:** Must be >= {coverage_threshold}

**Gate Decision Logic:**
```yaml
quality_gates:
  excellent:
    condition: "quality_score >= 90 AND vulnerabilities == 0"
    action: "proceed_fast_track"
    
  good:
    condition: "quality_score >= 70 AND vulnerabilities <= 2"
    action: "proceed_standard"
    
  needs_improvement:
    condition: "quality_score < 70 OR vulnerabilities > 2"
    action: "trigger_remediation_workflow"
```

**Remediation Workflows:**
- Low quality → Enhanced code analysis + documentation update
- Security issues → Security scan + vulnerability remediation
- Coverage gaps → Test generation + validation

**Stakeholder Notification:**
- Quality gate failures → Immediate notification
- Threshold warnings → Daily summary
- Success metrics → Weekly reporting
```

## Agent Communication

### Data Passing Between Agents

```
Coordinate data passing between agents "{source_agent}" → "{target_agent}":

**Data Transfer Protocol:**
1. **Source Agent Output Validation:**
   - Verify output format: {expected_format}
   - Validate required fields: {required_fields}
   - Check data quality: {quality_checks}

2. **Data Transformation:**
   - Input format for target agent: {target_format}
   - Required transformations: {transformations}
   - Data filtering rules: {filter_rules}

3. **Transfer Execution:**
   - Secure data handoff
   - Verify target agent receives complete data
   - Log transfer success/failure

**Data Schema Validation:**
```json
{
  "source_schema": {expected_source_schema},
  "target_schema": {expected_target_schema},
  "transformation_rules": {transformation_mapping}
}
```

**Error Handling:**
- Data validation failures → Retry with source agent
- Format mismatches → Apply automatic transformation
- Missing data → Request specific fields from source
```

### Shared Context Management

```
Manage shared context across agents in workflow "{workflow_name}":

**Context Structure:**
```json
{
  "workflow_context": {
    "workflow_id": "{workflow_id}",
    "execution_start": "{timestamp}",
    "project_path": "{project_path}",
    "user_preferences": {user_preferences}
  },
  "agent_results": {
    "{agent_name}": {agent_output},
    "shared_metrics": {shared_metrics}
  },
  "execution_state": {
    "current_phase": "{phase}",
    "completed_agents": ["{completed_agents}"],
    "pending_agents": ["{pending_agents}"]
  }
}
```

**Context Access Patterns:**
- **Read-Only Access:** All agents can read shared context
- **Write Access:** Only designated agents can update specific sections
- **Versioned Updates:** Maintain history of context changes

**Context Synchronization:**
- Real-time updates during execution
- Conflict resolution for concurrent updates
- Rollback capability for failed operations
```

## Error Handling and Recovery

### Failure Recovery Strategies

```
Implement failure recovery for agent coordination in "{workflow_name}":

**Failure Classification:**
1. **Agent Failure:** Individual agent crashes or errors
2. **Communication Failure:** Data passing between agents fails
3. **Resource Failure:** System resources exhausted
4. **Workflow Failure:** Overall workflow logic error

**Recovery Strategies by Type:**

**Agent Failure Recovery:**
- **Retry Policy:** Maximum {max_retries} attempts with {retry_delay} delay
- **Fallback Agents:** Use alternative agent for same functionality
- **Partial Success:** Continue workflow with degraded functionality
- **Complete Abort:** Terminate workflow and notify user

**Communication Failure Recovery:**
- **Data Retry:** Re-attempt data transfer with exponential backoff
- **Alternative Channels:** Use backup communication mechanisms
- **Data Recreation:** Re-execute source agent if data is corrupted
- **Manual Intervention:** Request user assistance for critical data

**Resource Failure Recovery:**
- **Resource Scaling:** Request additional system resources
- **Load Balancing:** Redistribute work across available resources
- **Graceful Degradation:** Reduce agent concurrency to conserve resources
- **Queue Management:** Defer non-critical agents until resources available
```

### Rollback and Cleanup

```
Execute rollback and cleanup procedures for failed workflow "{workflow_name}":

**Rollback Strategy:**
1. **Identify Rollback Point:** Last successful checkpoint
2. **Assess Impact:** Determine which operations need reversal
3. **Execute Rollback:** Systematically undo changes
4. **Verify State:** Confirm system returned to stable state

**Cleanup Operations:**
- **File System Cleanup:**
  - Remove temporary files created during workflow
  - Restore backed-up files if modifications were made
  - Clean up working directories

- **Memory Cleanup:**
  - Release allocated resources
  - Clear shared context data
  - Terminate hanging agent processes

- **Security Cleanup:**
  - Revoke temporary permissions granted
  - Close security sessions
  - Clear sensitive data from memory

**Post-Failure Analysis:**
- Document failure root cause
- Update failure recovery procedures
- Recommend workflow improvements
- Generate incident report
```

## Workflow Monitoring

### Real-Time Workflow Monitoring

```
Monitor real-time execution of workflow "{workflow_name}":

**Monitoring Metrics:**
- **Execution Progress:** {current_step}/{total_steps}
- **Agent Status:** {agent_status_list}
- **Resource Usage:** {resource_metrics}
- **Performance Metrics:** {performance_data}

**Alert Conditions:**
- **Critical:** Agent failure, security breach, resource exhaustion
- **Warning:** Performance degradation, quality threshold violations
- **Info:** Normal progress updates, completion notifications

**Monitoring Dashboard:**
```
Workflow: {workflow_name}
Status: {execution_status}
Progress: ████████▓▓ {progress_percentage}%
Elapsed Time: {elapsed_time}
Estimated Remaining: {estimated_remaining}

Active Agents:
├── {agent_1}: {status_1} ({progress_1}%)
├── {agent_2}: {status_2} ({progress_2}%)
└── {agent_3}: {status_3} ({progress_3}%)

Resource Usage:
├── CPU: {cpu_usage}%
├── Memory: {memory_usage}MB
└── Disk I/O: {disk_io}MB/s
```

**Performance Tracking:**
- Execution time per agent
- Resource consumption patterns
- Bottleneck identification
- Optimization opportunities
```

### Workflow Analytics and Reporting

```
Generate analytics report for completed workflow "{workflow_name}":

**Execution Summary:**
- **Total Duration:** {total_duration}
- **Agents Executed:** {agent_count}
- **Success Rate:** {success_percentage}%
- **Resource Efficiency:** {efficiency_score}

**Performance Analysis:**
- **Fastest Agent:** {fastest_agent} ({execution_time})
- **Slowest Agent:** {slowest_agent} ({execution_time})
- **Resource Peak:** {peak_resource_usage}
- **Bottlenecks Identified:** {bottleneck_list}

**Quality Metrics:**
- **Code Quality Improvement:** {quality_delta}
- **Documentation Coverage:** {doc_coverage}%
- **Security Issues Resolved:** {security_fixes}
- **Maintenance Items Addressed:** {maintenance_items}

**Recommendations:**
1. **Performance Optimization:**
   - {performance_recommendation_1}
   - {performance_recommendation_2}

2. **Resource Allocation:**
   - {resource_recommendation_1}
   - {resource_recommendation_2}

3. **Workflow Improvements:**
   - {workflow_recommendation_1}
   - {workflow_recommendation_2}

**Trend Analysis:**
- Compare with previous executions
- Identify improvement/degradation patterns
- Predict future resource requirements
- Suggest optimization strategies
```

## Workflow Definition

### Custom Workflow Creation

```
Create custom workflow definition for "{workflow_purpose}":

**Workflow Specification:**
```yaml
name: "{workflow_name}"
version: "1.0.0"
description: "{workflow_description}"

agents:
  - name: "{agent_1}"
    required: {required_flag}
    priority: {priority_level}
  - name: "{agent_2}"
    required: {required_flag}
    priority: {priority_level}

execution:
  type: "{execution_type}"  # sequential, parallel, mixed
  timeout: {timeout_seconds}
  max_concurrent: {max_concurrent}

context:
  {context_variables}

steps:
  - agent: "{agent_name}"
    action: "{action_name}"
    parameters:
      {action_parameters}
    depends_on: ["{dependency_list}"]
    condition: "{execution_condition}"
    output_key: "{output_identifier}"
```

**Validation Requirements:**
- All specified agents must exist and be active
- Dependencies must form a valid DAG (no cycles)
- Conditions must use valid syntax and available variables
- Resource requirements must be within system limits

**Testing Strategy:**
- Dry-run execution to validate workflow structure
- Mock agent execution for logic validation
- Performance testing with realistic data
- Error injection testing for failure scenarios
```

### Workflow Templates

```
Use workflow template "{template_name}" for common coordination patterns:

**Available Templates:**

**1. Quality Assurance Pipeline:**
```yaml
quality_pipeline:
  agents: [code-quality-agent, documentation-agent, maintenance-agent]
  execution: sequential
  gates: [quality_check, security_check]
```

**2. Content Generation Workflow:**
```yaml
content_workflow:
  agents: [resume-processing-agent, content-generation-agent]
  execution: sequential
  outputs: [linkedin_posts, professional_bios]
```

**3. Parallel Analysis:**
```yaml
parallel_analysis:
  agents: [multiple_analysis_agents]
  execution: parallel
  aggregation: results_consolidation
```

**Template Customization:**
- Override default parameters: {custom_parameters}
- Add conditional logic: {custom_conditions}
- Extend with additional agents: {additional_agents}
- Modify execution strategy: {execution_modifications}

**Template Validation:**
- Ensure all template variables are provided
- Validate custom parameters against agent requirements
- Check resource availability for template execution
- Verify security permissions for all template operations
```

## Integration Prompts

### Security Framework Integration

```
Integrate workflow coordination with security framework:

**Security Session Management:**
- Create security sessions for each agent
- Validate permissions before agent execution
- Monitor security violations during execution
- Clean up security sessions after completion

**Permission Validation:**
```python
for agent_name in workflow_agents:
    session_id = security.create_session(agent_name, agent_config)
    
    for permission in required_permissions:
        if not security.check_permission(session_id, permission):
            raise SecurityViolation(f"Agent {agent_name} lacks {permission}")
    
    execute_agent_with_session(agent_name, session_id)
    security.end_session(session_id)
```

**Audit Trail Integration:**
- Log all coordination decisions
- Record agent activation/deactivation
- Track data transfers between agents
- Monitor resource usage patterns
```

### Agent OS Framework Integration

```
Integrate coordination system with Agent OS framework:

**Framework Coordination:**
- Use Agent OS configuration system for workflow definitions
- Integrate with Claude Code for user interaction
- Leverage existing agent infrastructure
- Maintain compatibility with Agent OS standards

**Workflow Registration:**
- Register workflows in Agent OS workflow registry
- Enable workflow discovery through Agent OS CLI
- Support workflow versioning and updates
- Provide workflow documentation integration

**User Interface Integration:**
- Expose coordination commands through Agent OS CLI
- Provide real-time status updates to users
- Enable workflow interruption and resumption
- Support workflow debugging and inspection
```

## Variables for Dynamic Prompts

```yaml
# Available variables for prompt customization
variables:
  workflow_name: "Name of the workflow being executed"
  workflow_id: "Unique identifier for workflow execution"
  agent_list: "List of agents participating in workflow"
  execution_type: "sequential | parallel | mixed"
  shared_context: "Context data shared between agents"
  success_criteria: "Criteria for workflow success"
  error_strategy: "Strategy for handling errors"
  
# Timing variables
timing:
  estimated_duration: "Estimated total execution time"
  elapsed_time: "Time elapsed since workflow start"
  estimated_remaining: "Estimated time to completion"
  
# Resource variables
resources:
  max_concurrent: "Maximum concurrent agent executions"
  cpu_allocation: "CPU resources allocated per agent"
  memory_limits: "Memory limits per agent"
  
# Usage examples:
# {workflow_name} -> "code-quality-check"
# {execution_type} -> "sequential"
# {agent_list} -> ["code-quality-agent", "documentation-agent"]
```

## Quality Assurance Prompts

### Coordination Validation

```
Validate coordination logic for workflow "{workflow_name}":

**Validation Checklist:**
- [ ] All agent dependencies are resolvable
- [ ] No circular dependencies exist
- [ ] Resource requirements are within limits
- [ ] All required agents are available and active
- [ ] Conditional logic is syntactically correct
- [ ] Data schemas are compatible between agents

**Logic Verification:**
- Trace execution paths for all possible conditions
- Verify data flow integrity throughout workflow
- Check error handling coverage for all failure modes
- Validate timeout and retry configurations

**Performance Validation:**
- Estimate resource usage for concurrent execution
- Identify potential bottlenecks in agent coordination
- Verify scalability for larger workflows
- Test coordination overhead impact

**Security Validation:**
- Ensure proper permission isolation between agents
- Validate secure data transfer mechanisms
- Check audit logging completeness
- Verify compliance with security policies
```