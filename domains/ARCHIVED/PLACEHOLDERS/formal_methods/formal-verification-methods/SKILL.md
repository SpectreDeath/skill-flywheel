---
Domain: formal_methods
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: formal-verification-methods
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




## Description

Automatically designs and implements optimal formal verification methods for comprehensive system verification, including deductive verification, runtime verification, static analysis, and hybrid verification approaches. This skill provides comprehensive frameworks for combining multiple verification techniques, verification of complex systems, and integration with development workflows.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Deductive Verification**: Design and implement deductive verification frameworks using Hoare logic, separation logic, and program logics
- **Runtime Verification**: Create runtime verification systems for monitoring and checking system properties during execution
- **Static Analysis**: Implement static analysis techniques for detecting bugs, security vulnerabilities, and correctness issues
- **Hybrid Verification**: Develop hybrid verification approaches combining multiple techniques for comprehensive coverage
- **Verification Integration**: Integrate formal verification with software development workflows and CI/CD pipelines
- **Property-Based Testing**: Create property-based testing frameworks for systematic testing with formal properties
- **Verification Automation**: Automate verification processes with intelligent tool selection and configuration

## Usage Examples

### Deductive Verification Framework

```python
"""
Deductive Verification Framework using Hoare Logic
"""

from typing import List, Dict, Set, Tuple, Optional, Union, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import z3

@dataclass
class HoareTriple:
    """Hoare triple: {precondition} program {postcondition}"""
    precondition: str
    program: str
    postcondition: str
    
    def to_string(self) -> str:
        return f"{{ {self.precondition} }} {self.program} {{ {self.postcondition} }}"

@dataclass
class ProgramState:
    """Program state with variable assignments"""
    variables: Dict[str, int]
    
    def __hash__(self):
        return hash(tuple(self.variables.items()))
    
    def __eq__(self, other):
        return self.variables == other.variables

class Assertion:
    """Base class for assertions"""
    
    @abstractmethod
    def evaluate(self, state: ProgramState) -> bool:
        pass
    
    @abstractmethod
    def to_z3(self) -> z3.BoolRef:
        pass

class VariableAssertion(Assertion):
    """Assertion about a variable"""
    
    def __init__(self, var_name: str, operator: str, value: int):
        self.var_name = var_name
        self.operator = operator
        self.value = value
    
    def evaluate(self, state: ProgramState) -> bool:
        if self.var_name not in state.variables:
            return False
        
        var_value = state.variables[self.var_name]
        
        if self.operator == "==":
            return var_value == self.value
        elif self.operator == "!=":
            return var_value != self.value
        elif self.operator == "<":
            return var_value < self.value
        elif self.operator == ">":
            return var_value > self.value
        elif self.operator == "<=":
            return var_value <= self.value
        elif self.operator == ">=":
            return var_value >= self.value
        return False
    
    def to_z3(self) -> z3.BoolRef:
        var = z3.Int(self.var_name)
        
        if self.operator == "==":
            return var == self.value
        elif self.operator == "!=":
            return var != self.value
        elif self.operator == "<":
            return var < self.value
        elif self.operator == ">":
            return var > self.value
        elif self.operator == "<=":
            return var <= self.value
        elif self.operator == ">=":
            return var >= self.value
        return z3.BoolVal(False)

class CompoundAssertion(Assertion):
    """Compound assertion combining multiple assertions"""
    
    def __init__(self, left: Assertion, operator: str, right: Assertion):
        self.left = left
        self.operator = operator
        self.right = right
    
    def evaluate(self, state: ProgramState) -> bool:
        left_result = self.left.evaluate(state)
        right_result = self.right.evaluate(state)
        
        if self.operator == "&&":
            return left_result and right_result
        elif self.operator == "||":
            return left_result or right_result
        return False
    
    def to_z3(self) -> z3.BoolRef:
        left_z3 = self.left.to_z3()
        right_z3 = self.right.to_z3()
        
        if self.operator == "&&":
            return z3.And(left_z3, right_z3)
        elif self.operator == "||":
            return z3.Or(left_z3, right_z3)
        return z3.BoolVal(False)

class ProgramStatement(ABC):
    """Abstract base class for program statements"""
    
    @abstractmethod
    def execute(self, state: ProgramState) -> ProgramState:
        pass
    
    @abstractmethod
    def get_precondition(self) -> Assertion:
        pass
    
    @abstractmethod
    def get_postcondition(self) -> Assertion:
        pass
    
    @abstractmethod
    def verify(self) -> bool:
        pass

class AssignmentStatement(ProgramStatement):
    """Assignment statement: variable = expression"""
    
    def __init__(self, var_name: str, expression: Callable[[ProgramState], int]):
        self.var_name = var_name
        self.expression = expression
    
    def execute(self, state: ProgramState) -> ProgramState:
        new_state = ProgramState(state.variables.copy())
        new_state.variables[self.var_name] = self.expression(state)
        return new_state
    
    def get_precondition(self) -> Assertion:
        # For assignment, precondition is typically True
        return VariableAssertion("true", "==", 1)
    
    def get_postcondition(self) -> Assertion:
        # Postcondition relates old and new values
        return VariableAssertion(self.var_name, "!=", -1)  # Simplified
    
    def verify(self) -> bool:
        # Verify using Z3
        solver = z3.Solver()
        
        # Create Z3 variables
        for var in self.expression.__code__.co_varnames:
            solver.add(z3.Int(var) == 0)  # Simplified
        
        return solver.check() == z3.sat

class ConditionalStatement(ProgramStatement):
    """Conditional statement: if condition then else"""
    
    def __init__(self, condition: Assertion, 
                 then_branch: ProgramStatement, 
                 else_branch: ProgramStatement):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def execute(self, state: ProgramState) -> ProgramState:
        if self.condition.evaluate(state):
            return self.then_branch.execute(state)
        else:
            return self.else_branch.execute(state)
    
    def get_precondition(self) -> Assertion:
        # Precondition for conditional
        then_pre = self.then_branch.get_precondition()
        else_pre = self.else_branch.get_precondition()
        return CompoundAssertion(then_pre, "&&", else_pre)
    
    def get_postcondition(self) -> Assertion:
        # Postcondition for conditional
        then_post = self.then_branch.get_postcondition()
        else_post = self.else_branch.get_postcondition()
        return CompoundAssertion(then_post, "||", else_post)
    
    def verify(self) -> bool:
        # Verify both branches
        return (self.then_branch.verify() and 
                self.else_branch.verify() and
                self.condition_to_z3().check() == z3.sat)
    
    def condition_to_z3(self) -> z3.BoolRef:
        return self.condition.to_z3()

class LoopStatement(ProgramStatement):
    """Loop statement with invariant"""
    
    def __init__(self, condition: Assertion, 
                 body: ProgramStatement, 
                 invariant: Assertion):
        self.condition = condition
        self.body = body
        self.invariant = invariant
    
    def execute(self, state: ProgramState) -> ProgramState:
        current_state = state
        
        while self.condition.evaluate(current_state):
            current_state = self.body.execute(current_state)
            
        return current_state
    
    def get_precondition(self) -> Assertion:
        # Precondition: invariant holds initially
        return self.invariant
    
    def get_postcondition(self) -> Assertion:
        # Postcondition: invariant and not condition
        not_condition = CompoundAssertion(self.condition, "==", False)
        return CompoundAssertion(self.invariant, "&&", not_condition)
    
    def verify(self) -> bool:
        # Verify loop invariant
        solver = z3.Solver()
        
        # Invariant must hold initially
        solver.add(self.invariant.to_z3())
        
        # Invariant must be preserved by body
        # This is a simplified check
        return solver.check() == z3.sat

class DeductiveVerifier:
    """Main deductive verification framework"""
    
    def __init__(self):
        self.program_statements: List[ProgramStatement] = []
        self.hoare_triples: List[HoareTriple] = []
        
    def add_statement(self, statement: ProgramStatement):
        """Add a program statement to verify"""
        self.program_statements.append(statement)
        
    def add_hoare_triple(self, triple: HoareTriple):
        """Add a Hoare triple to verify"""
        self.hoare_triples.append(triple)
        
    def verify_program(self) -> Tuple[bool, List[str]]:
        """Verify the entire program"""
        errors = []
        
        for i, statement in enumerate(self.program_statements):
            if not statement.verify():
                errors.append(f"Statement {i} verification failed")
                
        for i, triple in enumerate(self.hoare_triples):
            if not self.verify_hoare_triple(triple):
                errors.append(f"Hoare triple {i} verification failed")
                
        return len(errors) == 0, errors
    
    def verify_hoare_triple(self, triple: HoareTriple) -> bool:
        """Verify a single Hoare triple"""
        # Parse and verify the triple
        # This is a simplified implementation
        return True
        
    def generate_verification_conditions(self) -> List[z3.BoolRef]:
        """Generate verification conditions for the program"""
        conditions = []
        
        for statement in self.program_statements:
            # Generate VC for each statement
            conditions.append(z3.BoolVal(True))  # Simplified
            
        return conditions

# Example usage: Verify a simple sorting algorithm
def example_deductive_verification():
    """Example: Deductive verification of bubble sort"""
    
    verifier = DeductiveVerifier()
    
    # Create program statements for bubble sort
    # This is a simplified example
    
    # Precondition: array is defined
    precondition = VariableAssertion("array_defined", "==", 1)
    
    # Postcondition: array is sorted
    postcondition = VariableAssertion("array_sorted", "==", 1)
    
    # Create Hoare triple
    triple = HoareTriple(
        precondition="array_defined == 1",
        program="bubble_sort(array)",
        postcondition="array_sorted == 1"
    )
    
    verifier.add_hoare_triple(triple)
    
    # Verify
    result, errors = verifier.verify_program()
    
    print(f"Verification result: {'Success' if result else 'Failed'}")
    if errors:
        for error in errors:
            print(f"  Error: {error}")
    
    return verifier

if __name__ == "__main__":
    example_deductive_verification()
```

### Runtime Verification Framework

```python
"""
Runtime Verification Framework
"""

from typing import List, Dict, Set, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import threading
import time
from enum import Enum

class PropertyType(Enum):
    """Types of runtime properties"""
    SAFETY = "safety"
    LIVENESS = "liveness"
    SECURITY = "security"

@dataclass
class RuntimeEvent:
    """Runtime event with timestamp"""
    event_type: str
    timestamp: float
    data: Dict[str, Any]
    
    def to_string(self) -> str:
        return f"{self.event_type} at {self.timestamp}: {self.data}"

class RuntimeProperty(ABC):
    """Abstract base class for runtime properties"""
    
    def __init__(self, property_id: str, property_type: PropertyType):
        self.property_id = property_id
        self.property_type = property_type
        self.violations: List[RuntimeEvent] = []
        
    @abstractmethod
    def check_event(self, event: RuntimeEvent) -> bool:
        """Check if event satisfies the property"""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get current status of the property"""
        pass

class SafetyProperty(RuntimeProperty):
    """Safety property: something bad never happens"""
    
    def __init__(self, property_id: str, bad_condition: Callable[[RuntimeEvent], bool]):
        super().__init__(property_id, PropertyType.SAFETY)
        self.bad_condition = bad_condition
        
    def check_event(self, event: RuntimeEvent) -> bool:
        """Check if event violates safety property"""
        if self.bad_condition(event):
            self.violations.append(event)
            return False
        return True
        
    def get_status(self) -> str:
        violation_count = len(self.violations)
        return f"Safety property {self.property_id}: {violation_count} violations"

class LivenessProperty(RuntimeProperty):
    """Liveness property: something good eventually happens"""
    
    def __init__(self, property_id: str, good_condition: Callable[[RuntimeEvent], bool]):
        super().__init__(property_id, PropertyType.LIVENESS)
        self.good_condition = good_condition
        self.eventually_happened = False
        
    def check_event(self, event: RuntimeEvent) -> bool:
        """Check if event satisfies liveness property"""
        if self.good_condition(event):
            self.eventually_happened = True
        return self.eventually_happened
        
    def get_status(self) -> str:
        status = "satisfied" if self.eventually_happened else "not yet satisfied"
        return f"Liveness property {self.property_id}: {status}"

class SecurityProperty(RuntimeProperty):
    """Security property: security constraints are maintained"""
    
    def __init__(self, property_id: str, security_check: Callable[[RuntimeEvent], bool]):
        super().__init__(property_id, PropertyType.SECURITY)
        self.security_check = security_check
        
    def check_event(self, event: RuntimeEvent) -> bool:
        """Check if event violates security property"""
        if not self.security_check(event):
            self.violations.append(event)
            return False
        return True
        
    def get_status(self) -> str:
        violation_count = len(self.violations)
        return f"Security property {self.property_id}: {violation_count} violations"

class RuntimeMonitor:
    """Main runtime monitoring framework"""
    
    def __init__(self):
        self.properties: List[RuntimeProperty] = []
        self.event_queue: List[RuntimeEvent] = []
        self.monitoring_active = False
        self.monitor_thread = None
        
    def add_property(self, property: RuntimeProperty):
        """Add a property to monitor"""
        self.properties.append(property)
        
    def start_monitoring(self):
        """Start runtime monitoring"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop runtime monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log a runtime event"""
        event = RuntimeEvent(
            event_type=event_type,
            timestamp=time.time(),
            data=data
        )
        self.event_queue.append(event)
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            if self.event_queue:
                event = self.event_queue.pop(0)
                self._check_properties(event)
            time.sleep(0.1)  # Check every 100ms
            
    def _check_properties(self, event: RuntimeEvent):
        """Check all properties against the event"""
        for property in self.properties:
            property.check_event(event)
            
    def get_status_report(self) -> Dict[str, str]:
        """Get status report for all properties"""
        report = {}
        for property in self.properties:
            report[property.property_id] = property.get_status()
        return report
        
    def get_violations(self) -> List[Tuple[str, RuntimeEvent]]:
        """Get all property violations"""
        violations = []
        for property in self.properties:
            for violation in property.violations:
                violations.append((property.property_id, violation))
        return violations

# Example usage: Monitor a web server
def example_runtime_monitoring():
    """Example: Runtime monitoring of a web server"""
    
    monitor = RuntimeMonitor()
    
    # Add safety property: no more than 100 concurrent connections
    def too_many_connections(event: RuntimeEvent) -> bool:
        return (event.event_type == "connection_count" and 
                event.data.get("count", 0) > 100)
    
    safety_prop = SafetyProperty("max_connections", too_many_connections)
    monitor.add_property(safety_prop)
    
    # Add liveness property: requests are eventually processed
    def request_processed(event: RuntimeEvent) -> bool:
        return event.event_type == "request_processed"
    
    liveness_prop = LivenessProperty("requests_processed", request_processed)
    monitor.add_property(liveness_prop)
    
    # Add security property: no unauthorized access
    def unauthorized_access(event: RuntimeEvent) -> bool:
        return (event.event_type == "access_attempt" and 
                event.data.get("authorized", False) == False)
    
    security_prop = SecurityProperty("no_unauthorized_access", unauthorized_access)
    monitor.add_property(security_prop)
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Simulate events
    monitor.log_event("connection_count", {"count": 50})
    monitor.log_event("request_processed", {"request_id": "req_001"})
    monitor.log_event("access_attempt", {"user": "admin", "authorized": True})
    monitor.log_event("connection_count", {"count": 150})  # Violation
    monitor.log_event("access_attempt", {"user": "hacker", "authorized": False})  # Violation
    
    # Get status
    time.sleep(1)  # Wait for monitoring
    status = monitor.get_status_report()
    
    print("Runtime monitoring status:")
    for prop_id, status_msg in status.items():
        print(f"  {status_msg}")
    
    # Get violations
    violations = monitor.get_violations()
    print(f"\nTotal violations: {len(violations)}")
    for prop_id, violation in violations:
        print(f"  {prop_id}: {violation.to_string()}")
    
    monitor.stop_monitoring()
    return monitor

if __name__ == "__main__":
    example_runtime_monitoring()
```

### Static Analysis Framework

```python
"""
Static Analysis Framework
"""

from typing import List, Dict, Set, Tuple, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import ast
import re

@dataclass
class AnalysisResult:
    """Result of static analysis"""
    issue_type: str
    severity: str  # "low", "medium", "high", "critical"
    file_path: str
    line_number: int
    column: int
    description: str
    suggestion: str
    
    def to_string(self) -> str:
        return (f"{self.severity.upper()}: {self.issue_type} at "
                f"{self.file_path}:{self.line_number}:{self.column}\n"
                f"  {self.description}\n"
                f"  Suggestion: {self.suggestion}")

class StaticAnalyzer(ABC):
    """Abstract base class for static analyzers"""
    
    @abstractmethod
    def analyze_file(self, file_path: str) -> List[AnalysisResult]:
        """Analyze a single file"""
        pass
    
    @abstractmethod
    def get_analyzer_name(self) -> str:
        """Get name of the analyzer"""
        pass

class SecurityAnalyzer(StaticAnalyzer):
    """Security vulnerability analyzer"""
    
    def __init__(self):
        self.dangerous_functions = {
            'eval': 'Use of eval() is dangerous',
            'exec': 'Use of exec() is dangerous',
            'input': 'Raw input() can be unsafe',
            'pickle.loads': 'Untrusted pickle data can be dangerous',
            'subprocess.call': 'Shell=True can be dangerous'
        }
        
        self.sql_injection_patterns = [
            r"execute\s*\(\s*['\"]\s*SELECT.*\+.*['\"]",
            r"cursor\.execute\s*\(\s*['\"].*%.*['\"]",
            r"query\s*=\s*['\"].*%.*['\"]"
        ]
    
    def analyze_file(self, file_path: str) -> List[AnalysisResult]:
        """Analyze file for security issues"""
        results = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Check for dangerous function calls
            for line_num, line in enumerate(lines, 1):
                for func, description in self.dangerous_functions.items():
                    if func in line:
                        results.append(AnalysisResult(
                            issue_type="Dangerous Function",
                            severity="high",
                            file_path=file_path,
                            line_number=line_num,
                            column=line.find(func),
                            description=f"Found dangerous function: {func}",
                            suggestion=description
                        ))
                
                # Check for SQL injection patterns
                for pattern in self.sql_injection_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        results.append(AnalysisResult(
                            issue_type="SQL Injection",
                            severity="critical",
                            file_path=file_path,
                            line_number=line_num,
                            column=0,
                            description="Potential SQL injection vulnerability",
                            suggestion="Use parameterized queries instead"
                        ))
                        
        except Exception as e:
            results.append(AnalysisResult(
                issue_type="Analysis Error",
                severity="medium",
                file_path=file_path,
                line_number=0,
                column=0,
                description=f"Could not analyze file: {str(e)}",
                suggestion="Check file permissions and encoding"
            ))
            
        return results
    
    def get_analyzer_name(self) -> str:
        return "Security Analyzer"

class CodeQualityAnalyzer(StaticAnalyzer):
    """Code quality analyzer"""
    
    def __init__(self):
        self.long_line_threshold = 100
        self.complexity_threshold = 10
        
    def analyze_file(self, file_path: str) -> List[AnalysisResult]:
        """Analyze file for code quality issues"""
        results = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Check for long lines
            for line_num, line in enumerate(lines, 1):
                if len(line) > self.long_line_threshold:
                    results.append(AnalysisResult(
                        issue_type="Long Line",
                        severity="low",
                        file_path=file_path,
                        line_number=line_num,
                        column=self.long_line_threshold,
                        description=f"Line too long ({len(line)} chars)",
                        suggestion=f"Consider breaking line at {self.long_line_threshold} characters"
                    ))
                
            # Check for complex functions using AST
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = self._calculate_complexity(node)
                        if complexity > self.complexity_threshold:
                            results.append(AnalysisResult(
                                issue_type="High Complexity",
                                severity="medium",
                                file_path=file_path,
                                line_number=node.lineno,
                                column=node.col_offset,
                                description=f"Function '{node.name}' has high cyclomatic complexity ({complexity})",
                                suggestion="Consider refactoring to reduce complexity"
                            ))
            except SyntaxError:
                results.append(AnalysisResult(
                    issue_type="Syntax Error",
                    severity="high",
                    file_path=file_path,
                    line_number=0,
                    column=0,
                    description="File contains syntax errors",
                    suggestion="Fix syntax errors before analysis"
                ))
                
        except Exception as e:
            results.append(AnalysisResult(
                issue_type="Analysis Error",
                severity="medium",
                file_path=file_path,
                line_number=0,
                column=0,
                description=f"Could not analyze file: {str(e)}",
                suggestion="Check file permissions and encoding"
            ))
            
        return results
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, 
                                ast.Try, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        return complexity
    
    def get_analyzer_name(self) -> str:
        return "Code Quality Analyzer"

class StaticAnalysisFramework:
    """Main static analysis framework"""
    
    def __init__(self):
        self.analyzers: List[StaticAnalyzer] = []
        
    def add_analyzer(self, analyzer: StaticAnalyzer):
        """Add an analyzer to the framework"""
        self.analyzers.append(analyzer)
        
    def analyze_files(self, file_paths: List[str]) -> Dict[str, List[AnalysisResult]]:
        """Analyze multiple files"""
        results = {}
        
        for file_path in file_paths:
            file_results = []
            
            for analyzer in self.analyzers:
                try:
                    analyzer_results = analyzer.analyze_file(file_path)
                    file_results.extend(analyzer_results)
                except Exception as e:
                    file_results.append(AnalysisResult(
                        issue_type="Analyzer Error",
                        severity="medium",
                        file_path=file_path,
                        line_number=0,
                        column=0,
                        description=f"Analyzer {analyzer.get_analyzer_name()} failed: {str(e)}",
                        suggestion="Check analyzer configuration"
                    ))
            
            results[file_path] = file_results
            
        return results
    
    def generate_report(self, results: Dict[str, List[AnalysisResult]]) -> str:
        """Generate analysis report"""
        report = ["Static Analysis Report", "=" * 40, ""]
        
        total_issues = 0
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for file_path, file_results in results.items():
            if file_results:
                report.append(f"File: {file_path}")
                report.append("-" * len(f"File: {file_path}"))
                
                for result in file_results:
                    report.append(result.to_string())
                    report.append("")
                    total_issues += 1
                    severity_counts[result.severity] += 1
            else:
                report.append(f"File: {file_path} - No issues found")
                report.append("")
        
        # Summary
        report.append("Summary")
        report.append("-------")
        report.append(f"Total issues: {total_issues}")
        for severity, count in severity_counts.items():
            report.append(f"{severity.upper()}: {count}")
        
        return "\n".join(report)

# Example usage
def example_static_analysis():
    """Example: Static analysis of Python files"""
    
    framework = StaticAnalysisFramework()
    
    # Add analyzers
    framework.add_analyzer(SecurityAnalyzer())
    framework.add_analyzer(CodeQualityAnalyzer())
    
    # Analyze files (assuming test files exist)
    test_files = ["test_security.py", "test_quality.py"]
    
    # Create test files for demonstration
    with open("test_security.py", "w") as f:
        f.write("""
# Security issues
def dangerous_function():
    user_input = input("Enter something: ")
    eval(user_input)
    
    import subprocess
    subprocess.call("ls", shell=True)
""")
    
    with open("test_quality.py", "w") as f:
        f.write("""
# Code quality issues
def very_long_function_name_that_exceeds_the_recommended_length_and_should_be_refactored():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    if True:
                                        if True:
                                            pass
""")
    
    # Analyze files
    results = framework.analyze_files(["test_security.py", "test_quality.py"])
    
    # Generate report
    report = framework.generate_report(results)
    print(report)
    
    # Clean up test files
    import os
    os.remove("test_security.py")
    os.remove("test_quality.py")
    
    return framework

if __name__ == "__main__":
    example_static_analysis()
```

## Input Format

### Formal Verification Specification

```yaml
formal_verification_specification:
  system_name: string             # Name of the system to verify
  verification_type: "deductive|runtime|static|hybrid"
  
  if verification_type == "deductive":
    deductive_specification:
      preconditions: array        # List of preconditions
      postconditions: array       # List of postconditions
      invariants: array           # Loop invariants
      program_logic: "hoare|separation|program_logic"
      
  if verification_type == "runtime":
    runtime_specification:
      properties: array           # Runtime properties to monitor
      monitoring_strategy: "event_based|trace_based|hybrid"
      violation_handling: "log|alert|terminate"
      
  if verification_type == "static":
    static_specification:
      analysis_targets: array     # Files/directories to analyze
      analysis_types: array       # Security, quality, correctness
      severity_thresholds: object # Severity level thresholds
      
  if verification_type == "hybrid":
    hybrid_specification:
      verification_methods: array # Combination of methods
      integration_strategy: string
      coverage_requirements: object

verification_config:
  tools: array                    # Verification tools to use
  automation_level: string        # Manual, semi-automatic, automatic
  integration_points: array       # CI/CD integration points
  reporting_format: string        # Report format
```

### Property Specification

```yaml
property_specification:
  property_id: string
  property_type: "safety|liveness|security|correctness"
  temporal_logic: "LTL|CTL|CTL*|PCTL"
  formula: string                 # Formal property specification
  
  if property_type == "safety":
    safety_property:
      bad_states: array           # States that should never be reached
      constraints: array          # System constraints
      
  if property_type == "liveness":
    liveness_property:
      good_states: array          # States that should eventually be reached
      fairness_conditions: array  # Fairness requirements
      
  if property_type == "security":
    security_property:
      attack_vectors: array       # Potential attack vectors
      security_invariants: array  # Security invariants
      
  verification_strategy:
    verification_method: string   # Deductive, model checking, etc.
    tool_selection: string        # Tool selection strategy
    resource_allocation: object   # Resource allocation for verification
```

## Output Format

### Verification Results

```yaml
verification_results:
  system_name: string
  verification_timestamp: timestamp
  verification_type: string
  
  verification_summary:
    total_properties: number
    verified_properties: number
    failed_properties: number
    unknown_properties: number
    verification_coverage: number
    
  property_results:
    - property_id: string
      result: "verified|failed|unknown"
      verification_time: number
      resources_used: object
      evidence: string            # Evidence of verification
      
      if result == "failed":
        failure_details:
          failure_type: string    # Type of failure
          root_cause: string      # Root cause analysis
          counterexample: object  # Counterexample if available
          suggested_fixes: array  # Suggested fixes
          
      if result == "unknown":
        uncertainty_details:
          reason: string          # Reason for unknown result
          additional_analysis_needed: array
          confidence_level: number

performance_metrics:
  total_verification_time: number
  average_property_time: number
  peak_memory_usage: string
  cpu_usage: string
  parallelization_factor: number

quality_metrics:
  verification_reliability: number
  false_positive_rate: number
  false_negative_rate: number
  verification_completeness: number
```

### Verification Report

```yaml
verification_report:
  report_id: string
  report_type: "summary|detailed|compliance"
  generation_timestamp: timestamp
  
  executive_summary:
    verification_status: string   # Overall verification status
    risk_assessment: string       # Risk assessment
    recommendations: array        # High-level recommendations
    
  detailed_analysis:
    method_specific_results: array
    integration_analysis: object
    performance_analysis: object
    
  compliance_assessment:
    standards_complied: array     # Standards verified against
    compliance_level: string      # Level of compliance
    gaps_identified: array        # Compliance gaps
    
  appendices:
    technical_details: object
    tool_configurations: array
    verification_artifacts: array
```

## Configuration Options

### Verification Methods

```yaml
verification_methods:
  deductive_verification:
    description: "Mathematical proof-based verification"
    best_for: ["critical_systems", "safety_critical", "mathematical_algorithms"]
    complexity: "high"
    automation_level: "semi_automatic"
    
  runtime_verification:
    description: "Monitoring-based verification during execution"
    best_for: ["complex_systems", "real_time_systems", "security_monitoring"]
    complexity: "medium"
    automation_level: "automatic"
    
  static_analysis:
    description: "Analysis without program execution"
    best_for: ["code_quality", "security_vulnerabilities", "performance_issues"]
    complexity: "low_to_medium"
    automation_level: "automatic"
    
  hybrid_verification:
    description: "Combination of multiple verification methods"
    best_for: ["complex_systems", "high_assurance", "comprehensive_verification"]
    complexity: "high"
    automation_level: "semi_automatic"
```

### Integration Strategies

```yaml
integration_strategies:
  ci_cd_integration:
    description: "Integration with CI/CD pipelines"
    best_for: ["continuous_verification", "automated_testing", "devops_workflows"]
    complexity: "medium"
    implementation_effort: "medium"
    
  development_workflow:
    description: "Integration with development workflows"
    best_for: ["developer_productivity", "early_detection", "code_quality"]
    complexity: "low"
    implementation_effort: "low"
    
  compliance_framework:
    description: "Integration with compliance frameworks"
    best_for: ["regulatory_compliance", "standards_compliance", "audit_trails"]
    complexity: "high"
    implementation_effort: "high"
```

## Error Handling

### Verification Failures

```yaml
verification_failures:
  timeout_exceeded:
    retry_strategy: "simplify_verification"
    max_retries: 3
    fallback_action: "partial_verification"
  
  resource_exhaustion:
    retry_strategy: "resource_optimization"
    max_retries: 2
    fallback_action: "distributed_verification"
  
  tool_failure:
    retry_strategy: "alternative_tool"
    max_retries: 2
    fallback_action: "manual_verification"
  
  specification_error:
    retry_strategy: "specification_correction"
    max_retries: 1
    fallback_action: "expert_review"
```

### Integration Failures

```yaml
integration_failures:
  ci_cd_failure:
    detection_strategy: "pipeline_monitoring"
    recovery_strategy: "rollback_verification"
    escalation: "manual_intervention"
  
  tool_incompatibility:
    detection_strategy: "compatibility_checking"
    recovery_strategy: "tool_configuration"
    escalation: "tool_replacement"
  
  performance_degradation:
    detection_strategy: "performance_monitoring"
    recovery_strategy: "optimization"
    escalation: "architecture_review"
```

## Performance Optimization

### Verification Optimization

```python
# Optimization: Incremental verification
class IncrementalVerifier:
    """Incremental verification for improved performance"""
    
    def __init__(self):
        self.verification_cache = {}
        self.dependency_graph = {}
        
    def verify_incrementally(self, changed_files: List[str], 
                           all_files: List[str]) -> Dict[str, List[AnalysisResult]]:
        """Verify only changed files and their dependencies"""
        affected_files = self._compute_affected_files(changed_files)
        
        results = {}
        for file_path in affected_files:
            if file_path in self.verification_cache:
                # Use cached result if dependencies haven't changed
                if self._dependencies_unchanged(file_path):
                    results[file_path] = self.verification_cache[file_path]
                    continue
            
            # Re-verify file
            file_results = self._verify_file(file_path)
            self.verification_cache[file_path] = file_results
            results[file_path] = file_results
            
        return results
        
    def _compute_affected_files(self, changed_files: List[str]) -> List[str]:
        """Compute files affected by changes"""
        affected = set(changed_files)
        
        for file_path in changed_files:
            if file_path in self.dependency_graph:
                affected.update(self.dependency_graph[file_path])
                
        return list(affected)
        
    def _dependencies_unchanged(self, file_path: str) -> bool:
        """Check if dependencies have changed"""
        # Implementation details
        return True

# Optimization: Parallel verification
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class ParallelVerifier:
    """Parallel verification for improved performance"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers
        
    def verify_parallel(self, files: List[str], 
                       verifier_func: Callable) -> Dict[str, Any]:
        """Verify files in parallel"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(verifier_func, file): file 
                for file in files
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results[file_path] = result
                except Exception as e:
                    results[file_path] = f"Verification failed: {str(e)}"
                    
        return results
```

### Resource Management

```yaml
resource_management:
  memory_optimization:
    technique: "lazy_evaluation"
    memory_strategy: "garbage_collection"
    memory_reduction: "significant"
    
  cpu_optimization:
    technique: "parallel_processing"
    cpu_strategy: "multithreading"
    cpu_efficiency: "improved"
    
  storage_optimization:
    technique: "incremental_storage"
    storage_strategy: "compression"
    storage_reduction: "moderate"
    
  network_optimization:
    technique: "distributed_processing"
    network_strategy: "caching"
    network_efficiency: "improved"
```

## Integration Examples

### With CI/CD Pipelines

```yaml
# GitHub Actions integration
name: Formal Verification
on: [push, pull_request]

jobs:
  verification:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup verification tools
        run: |
          # Install verification tools
          pip install formal-verification-framework
          
      - name: Run static analysis
        run: |
          python -m static_analysis.analyze --target src/
          
      - name: Run deductive verification
        run: |
          python -m deductive_verification.verify --target src/
          
      - name: Run runtime verification
        run: |
          python -m runtime_verification.monitor --target tests/
          
      - name: Generate report
        run: |
          python -m verification.report --format html --output report.html
          
      - name: Upload verification report
        uses: actions/upload-artifact@v2
        with:
          name: verification-report
          path: report.html
```

### With Development Workflows

```python
# Integration with development workflow
class DevelopmentWorkflowIntegration:
    """Integration with development workflows"""
    
    def __init__(self):
        self.verification_hooks = {}
        self.code_review_integration = None
        self.ide_integration = None
        
    def setup_pre_commit_hook(self):
        """Setup pre-commit hook for verification"""
        hook_script = """
        #!/bin/bash
        echo "Running formal verification..."
        python -m verification.framework verify --target .
        
        if [ $? -ne 0 ]; then
            echo "Verification failed. Commit rejected."
            exit 1
        fi
        """
        
        with open(".git/hooks/pre-commit", "w") as f:
            f.write(hook_script)
            
        import os
        os.chmod(".git/hooks/pre-commit", 0o755)
        
    def integrate_with_code_review(self, review_system: str):
        """Integrate with code review system"""
        if review_system == "github":
            self._setup_github_integration()
        elif review_system == "gitlab":
            self._setup_gitlab_integration()
        elif review_system == "bitbucket":
            self._setup_bitbucket_integration()
            
    def setup_ide_integration(self, ide: str):
        """Setup IDE integration"""
        if ide == "vscode":
            self._setup_vscode_integration()
        elif ide == "intellij":
            self._setup_intellij_integration()
        elif ide == "vim":
            self._setup_vim_integration()
```

## Best Practices

1. **Verification Strategy**:
   - Choose appropriate verification methods for the system
   - Combine multiple verification techniques for comprehensive coverage
   - Use incremental verification for large codebases
   - Integrate verification early in the development process

2. **Property Specification**:
   - Write clear and precise formal properties
   - Use appropriate temporal logic for different property types
   - Validate properties with examples and counterexamples
   - Document property intent and scope

3. **Tool Integration**:
   - Integrate verification tools with CI/CD pipelines
   - Use automated verification where possible
   - Maintain tool configurations and dependencies
   - Monitor verification performance and adjust strategies

4. **Performance Optimization**:
   - Use incremental verification for efficiency
   - Apply parallel processing for large systems
   - Optimize resource usage and memory management
   - Monitor and tune verification performance

## Troubleshooting

### Common Issues

1. **Verification Failures**: Analyze failure reasons and apply appropriate recovery strategies
2. **Performance Problems**: Use profiling and optimization techniques
3. **Integration Failures**: Review integration configurations and dependencies
4. **Tool Incompatibilities**: Check tool versions and compatibility requirements
5. **Resource Issues**: Implement resource management and optimization

### Debug Mode

```python
# Debug mode: Enhanced debugging
class DebugVerifier:
    """Verifier with enhanced debugging capabilities"""
    
    def __init__(self):
        self.debug_log = []
        self.verification_trace = []
        
    def log_verification_step(self, step: str, details: Dict[str, Any]):
        """Log verification step for debugging"""
        self.debug_log.append({
            'step': step,
            'details': details,
            'timestamp': time.time()
        })
        
    def log_property_check(self, property_id: str, result: bool, 
                          counterexample: Optional[Any]):
        """Log property check for debugging"""
        self.verification_trace.append({
            'property_id': property_id,
            'result': result,
            'counterexample': counterexample,
            'timestamp': time.time()
        })
        
    def generate_debug_report(self) -> Dict[str, Any]:
        """Generate debug report"""
        return {
            'total_verification_steps': len(self.debug_log),
            'property_checks': len(self.verification_trace),
            'verification_trace': self.verification_trace,
            'debug_log': self.debug_log
        }
```

## Monitoring and Metrics

### Verification Metrics

```yaml
verification_metrics:
  correctness_metrics:
    properties_verified: number
    verification_coverage: number
    false_positives: number
    false_negatives: number
    
  performance_metrics:
    average_verification_time: number
    maximum_verification_time: number
    memory_usage_peak: string
    cpu_usage_peak: string
    
  integration_metrics:
    ci_cd_success_rate: number
    integration_latency: number
    tool_availability: number
    automation_effectiveness: number
    
  quality_metrics:
    verification_reliability: number
    property_completeness: number
    tool_accuracy: number
    process_maturity: number
```

## Dependencies

- **Verification Tools**: Deductive verifiers, model checkers, static analyzers
- **Runtime Monitoring**: Event logging systems, monitoring frameworks
- **CI/CD Integration**: Jenkins, GitHub Actions, GitLab CI, Azure DevOps
- **Development Tools**: IDE integrations, code review systems
- **Performance Tools**: Profiling and monitoring tools for verification performance

## Version History

- **1.0.0**: Initial release with comprehensive formal verification methods
- **1.1.0**: Added advanced hybrid verification techniques and CI/CD integration
- **1.2.0**: Enhanced runtime verification and property-based testing frameworks
- **1.3.0**: Improved performance optimization and parallel verification
- **1.4.0**: Advanced integration with development workflows and compliance frameworks

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.

## Constraints

To be provided dynamically during execution.