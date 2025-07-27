#!/usr/bin/env python3
"""
Sub-Agent Security Framework
Enforces permissions and security boundaries for sub-agents
"""

import os
import fnmatch
import time
import hashlib
import json
import logging
from typing import Dict, List, Set, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PermissionType(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

class SecurityLevel(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityViolation:
    """Represents a security violation event"""
    agent_name: str
    violation_type: str
    attempted_action: str
    file_path: str
    timestamp: float
    details: str

@dataclass
class AgentSession:
    """Tracks an active agent session"""
    agent_name: str
    start_time: float
    operations_count: int
    files_accessed: Set[str]
    last_activity: float
    max_operations: int
    timeout: int

class SecurityFramework:
    """Enforces security policies for sub-agents"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.violations: List[SecurityViolation] = []
        self.active_sessions: Dict[str, AgentSession] = {}
        self.file_locks: Dict[str, str] = {}  # file_path -> agent_name
        self.audit_log: List[Dict[str, Any]] = []
        
    def create_session(self, agent_name: str, config: Dict[str, Any]) -> str:
        """Create a new agent session with security constraints"""
        session_id = self._generate_session_id(agent_name)
        
        # Extract security settings from config
        security = config.get('security', {})
        behavior = config.get('behavior', {})
        
        session = AgentSession(
            agent_name=agent_name,
            start_time=time.time(),
            operations_count=0,
            files_accessed=set(),
            last_activity=time.time(),
            max_operations=behavior.get('max_operations', 50),
            timeout=security.get('timeout', 300)
        )
        
        self.active_sessions[session_id] = session
        self._log_audit_event("session_created", agent_name, {"session_id": session_id})
        
        logger.info(f"Created security session for agent {agent_name}: {session_id}")
        return session_id
    
    def check_permission(self, session_id: str, operation: PermissionType, 
                        file_path: str, config: Dict[str, Any]) -> bool:
        """Check if an agent has permission to perform an operation"""
        
        if not self._validate_session(session_id):
            return False
        
        session = self.active_sessions[session_id]
        agent_name = session.agent_name
        
        # Update session activity
        session.last_activity = time.time()
        session.operations_count += 1
        
        # Check operation limits
        if session.operations_count > session.max_operations:
            self._record_violation(
                agent_name, "operation_limit_exceeded", 
                f"{operation.value} {file_path}", file_path,
                f"Exceeded max operations limit: {session.max_operations}"
            )
            return False
        
        # Normalize file path
        try:
            full_path = (self.project_root / file_path).resolve()
            relative_path = full_path.relative_to(self.project_root)
        except (ValueError, OSError):
            self._record_violation(
                agent_name, "path_traversal_attempt",
                f"{operation.value} {file_path}", file_path,
                "Attempted to access file outside project root"
            )
            return False
        
        # Check sandbox mode
        security = config.get('security', {})
        if security.get('sandbox_mode', True):
            if not self._is_path_in_sandbox(relative_path):
                self._record_violation(
                    agent_name, "sandbox_violation",
                    f"{operation.value} {file_path}", file_path,
                    "Attempted to access file outside sandbox"
                )
                return False
        
        # Check specific permissions
        permissions = config.get('permissions', {})
        allowed_patterns = permissions.get(operation.value, [])
        
        if not self._matches_patterns(str(relative_path), allowed_patterns):
            self._record_violation(
                agent_name, "permission_denied",
                f"{operation.value} {file_path}", file_path,
                f"No {operation.value} permission for this file pattern"
            )
            return False
        
        # Check file locks for write operations
        if operation == PermissionType.WRITE:
            if not self._acquire_file_lock(str(relative_path), agent_name):
                self._record_violation(
                    agent_name, "file_lock_conflict",
                    f"{operation.value} {file_path}", file_path,
                    "File is locked by another agent"
                )
                return False
        
        # Log successful permission check
        session.files_accessed.add(str(relative_path))
        self._log_audit_event("permission_granted", agent_name, {
            "operation": operation.value,
            "file_path": str(relative_path),
            "session_id": session_id
        })
        
        return True
    
    def require_user_approval(self, session_id: str, operation: str, 
                            file_path: str, details: str) -> bool:
        """Check if user approval is required for an operation"""
        
        if not self._validate_session(session_id):
            return False
        
        session = self.active_sessions[session_id]
        agent_name = session.agent_name
        
        # For now, all write operations require approval
        # In a real implementation, this would integrate with the user interface
        self._log_audit_event("approval_required", agent_name, {
            "operation": operation,
            "file_path": file_path,
            "details": details,
            "session_id": session_id
        })
        
        # Mock approval for testing - in reality this would prompt the user
        logger.info(f"User approval required for {agent_name}: {operation} on {file_path}")
        return True  # Mock approval
    
    def release_file_lock(self, file_path: str, agent_name: str) -> bool:
        """Release a file lock held by an agent"""
        normalized_path = str(Path(file_path).as_posix())
        
        if normalized_path in self.file_locks:
            if self.file_locks[normalized_path] == agent_name:
                del self.file_locks[normalized_path]
                self._log_audit_event("file_lock_released", agent_name, {
                    "file_path": normalized_path
                })
                return True
            else:
                logger.warning(f"Agent {agent_name} tried to release lock held by {self.file_locks[normalized_path]}")
                return False
        
        return True  # No lock to release
    
    def end_session(self, session_id: str) -> None:
        """End an agent session and clean up resources"""
        if session_id not in self.active_sessions:
            return
        
        session = self.active_sessions[session_id]
        agent_name = session.agent_name
        
        # Release all file locks held by this agent
        locks_to_release = [path for path, agent in self.file_locks.items() 
                           if agent == agent_name]
        
        for file_path in locks_to_release:
            self.release_file_lock(file_path, agent_name)
        
        # Log session statistics
        duration = time.time() - session.start_time
        self._log_audit_event("session_ended", agent_name, {
            "session_id": session_id,
            "duration_seconds": duration,
            "operations_count": session.operations_count,
            "files_accessed": len(session.files_accessed)
        })
        
        del self.active_sessions[session_id]
        logger.info(f"Ended session for agent {agent_name}: {session_id}")
    
    def get_security_report(self) -> Dict[str, Any]:
        """Generate a security report for audit purposes"""
        return {
            "violations": [
                {
                    "agent": v.agent_name,
                    "type": v.violation_type,
                    "action": v.attempted_action,
                    "file": v.file_path,
                    "timestamp": v.timestamp,
                    "details": v.details
                }
                for v in self.violations
            ],
            "active_sessions": len(self.active_sessions),
            "file_locks": len(self.file_locks),
            "audit_events": len(self.audit_log)
        }
    
    def _generate_session_id(self, agent_name: str) -> str:
        """Generate a unique session ID"""
        timestamp = str(time.time())
        content = f"{agent_name}:{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _validate_session(self, session_id: str) -> bool:
        """Validate that a session is active and not expired"""
        if session_id not in self.active_sessions:
            logger.warning(f"Invalid session ID: {session_id}")
            return False
        
        session = self.active_sessions[session_id]
        
        # Check session timeout
        if time.time() - session.last_activity > session.timeout:
            logger.warning(f"Session expired: {session_id}")
            self.end_session(session_id)
            return False
        
        return True
    
    def _is_path_in_sandbox(self, path: Path) -> bool:
        """Check if a path is within the allowed sandbox"""
        # For TeamResumes, allow access to most project files but restrict sensitive areas
        path_str = str(path).replace("\\", "/")
        
        # Allowed areas
        allowed_prefixes = [
            "cv/",
            "docs/",
            "dev_tools/",
            ".agent-os/",
            ".claude/",
            "temp/",  # Allow temporary files for agents
            "generated-content/",  # Allow generated content output
            "README.md",
            "CLAUDE.md"
        ]
        
        # Restricted areas
        restricted_prefixes = [
            ".git/",
            "node_modules/",
            "__pycache__/",
            ".env"
        ]
        
        # Check restricted areas first
        for prefix in restricted_prefixes:
            if path_str.startswith(prefix):
                return False
        
        # Check allowed areas
        for prefix in allowed_prefixes:
            if path_str.startswith(prefix):
                return True
        
        # Allow root-level files with specific extensions
        if "/" not in path_str and path_str.endswith(('.md', '.py', '.bat', '.css', '.yaml')):
            return True
        
        return False
    
    def _matches_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """Check if a file path matches any of the given patterns"""
        for pattern in patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    def _acquire_file_lock(self, file_path: str, agent_name: str) -> bool:
        """Attempt to acquire a lock on a file"""
        normalized_path = str(Path(file_path).as_posix())
        
        if normalized_path in self.file_locks:
            current_holder = self.file_locks[normalized_path]
            if current_holder != agent_name:
                logger.warning(f"File {file_path} is locked by {current_holder}")
                return False
        
        self.file_locks[normalized_path] = agent_name
        self._log_audit_event("file_lock_acquired", agent_name, {
            "file_path": normalized_path
        })
        return True
    
    def _record_violation(self, agent_name: str, violation_type: str, 
                         attempted_action: str, file_path: str, details: str) -> None:
        """Record a security violation"""
        violation = SecurityViolation(
            agent_name=agent_name,
            violation_type=violation_type,
            attempted_action=attempted_action,
            file_path=file_path,
            timestamp=time.time(),
            details=details
        )
        
        self.violations.append(violation)
        
        # Log as audit event as well
        self._log_audit_event("security_violation", agent_name, {
            "violation_type": violation_type,
            "attempted_action": attempted_action,
            "file_path": file_path,
            "details": details
        })
        
        logger.warning(f"Security violation by {agent_name}: {violation_type} - {details}")
    
    def _log_audit_event(self, event_type: str, agent_name: str, details: Dict[str, Any]) -> None:
        """Log an audit event"""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "agent_name": agent_name,
            "details": details
        }
        
        self.audit_log.append(event)
        
        # In a real implementation, this would write to a persistent audit log
        logger.debug(f"Audit event: {event_type} by {agent_name}")


def main():
    """Test the security framework"""
    # Create framework
    framework = SecurityFramework()
    
    # Mock agent configuration
    agent_config = {
        "name": "test-agent",
        "permissions": {
            "read": ["*.py", "*.md"],
            "write": ["*.py"],
            "execute": ["code_analysis"]
        },
        "security": {
            "max_file_size": 10,
            "timeout": 300,
            "sandbox_mode": True,
            "audit_logging": True
        },
        "behavior": {
            "max_operations": 50
        }
    }
    
    # Test session creation and permissions
    session_id = framework.create_session("test-agent", agent_config)
    
    # Test permission checks
    tests = [
        (PermissionType.READ, "cv/va_resume.md", True),
        (PermissionType.WRITE, "cv/va_resume.md", False),  # Not in write permissions
        (PermissionType.READ, ".git/config", False),  # Restricted area
        (PermissionType.WRITE, "main.py", True),  # Should work
    ]
    
    for operation, file_path, expected in tests:
        result = framework.check_permission(session_id, operation, file_path, agent_config)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status} {operation.value} {file_path}: {result}")
    
    # End session
    framework.end_session(session_id)
    
    # Print security report
    report = framework.get_security_report()
    print(f"\nSecurity Report:")
    print(f"Violations: {len(report['violations'])}")
    print(f"Active Sessions: {report['active_sessions']}")
    print(f"Audit Events: {report['audit_events']}")


if __name__ == "__main__":
    main()