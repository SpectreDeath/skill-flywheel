#!/usr/bin/env python3
"""
Skill: data-quality-checker
Domain: data_engineering
Description: Data quality validation and monitoring system for data pipelines
"""

import asyncio
import logging
import re
import statistics
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class QualityRuleType(Enum):
    """Types of quality rules"""
    NOT_NULL = "not_null"           # Field cannot be null
    UNIQUE = "unique"              # Field values must be unique
    RANGE = "range"                # Value must be within range
    REGEX = "regex"                # Value must match regex pattern
    CUSTOM = "custom"              # Custom validation function
    REFERENTIAL_INTEGRITY = "referential_integrity"  # Foreign key validation
    STATISTICAL = "statistical"    # Statistical validation

class QualitySeverity(Enum):
    """Quality rule severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class QualityStatus(Enum):
    """Quality check statuses"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"

@dataclass
class QualityRule:
    """Represents a data quality rule"""
    rule_id: str
    name: str
    description: str
    rule_type: QualityRuleType
    field_name: str
    parameters: Dict[str, Any]
    severity: QualitySeverity
    enabled: bool
    created_at: float
    last_modified: float

@dataclass
class QualityCheck:
    """Represents a quality check execution"""
    check_id: str
    rule_id: str
    dataset_name: str
    total_records: int
    passed_records: int
    failed_records: int
    status: QualityStatus
    error_details: List[Dict[str, Any]]
    execution_time: float
    executed_at: float

@dataclass
class QualityProfile:
    """Represents data quality profile for a dataset"""
    dataset_name: str
    total_records: int
    null_count: int
    unique_count: int
    duplicate_count: int
    min_value: Optional[float]
    max_value: Optional[float]
    mean_value: Optional[float]
    std_dev: Optional[float]
    null_percentage: float
    duplicate_percentage: float
    profiled_at: float

class DataQualityChecker:
    """Data quality validation and monitoring system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data quality checker
        
        Args:
            config: Configuration dictionary with:
                - default_severity: Default severity for new rules
                - tolerance_threshold: Tolerance for statistical checks
                - batch_size: Batch size for processing large datasets
        """
        self.default_severity = config.get("default_severity", "error")
        self.tolerance_threshold = config.get("tolerance_threshold", 0.05)
        self.batch_size = config.get("batch_size", 1000)
        
        self.quality_rules: Dict[str, QualityRule] = {}
        self.quality_checks: Dict[str, QualityCheck] = {}
        self.quality_profiles: Dict[str, QualityProfile] = {}
        
        self.quality_stats = {
            "total_rules": 0,
            "active_rules": 0,
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "quality_score": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background monitoring
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    def create_quality_rule(self,
                           name: str,
                           description: str,
                           rule_type: QualityRuleType,
                           field_name: str,
                           parameters: Dict[str, Any],
                           severity: QualitySeverity = QualitySeverity.ERROR,
                           enabled: bool = True) -> str:
        """
        Create a data quality rule
        
        Args:
            name: Rule name
            description: Rule description
            rule_type: Type of quality rule
            field_name: Field to validate
            parameters: Rule parameters
            severity: Rule severity
            enabled: Whether rule is enabled
            
        Returns:
            Rule ID
        """
        rule_id = str(uuid.uuid4())
        
        rule = QualityRule(
            rule_id=rule_id,
            name=name,
            description=description,
            rule_type=rule_type,
            field_name=field_name,
            parameters=parameters,
            severity=severity,
            enabled=enabled,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.quality_rules[rule_id] = rule
        self.quality_stats["total_rules"] += 1
        if enabled:
            self.quality_stats["active_rules"] += 1
        
        self.logger.info(f"Created quality rule: {rule_id}")
        return rule_id
    
    def profile_dataset(self, dataset_name: str, data: List[Dict[str, Any]]) -> str:
        """
        Profile a dataset to understand its quality characteristics
        
        Args:
            dataset_name: Name of the dataset
            data: Dataset records
            
        Returns:
            Profile ID
        """
        profile_id = str(uuid.uuid4())
        
        total_records = len(data)
        if total_records == 0:
            return profile_id
        
        # Analyze each field
        field_stats = {}
        for record in data:
            for field, value in record.items():
                if field not in field_stats:
                    field_stats[field] = {
                        "null_count": 0,
                        "unique_values": set(),
                        "values": []
                    }
                
                if value is None or value == "":
                    field_stats[field]["null_count"] += 1
                else:
                    field_stats[field]["unique_values"].add(value)
                    if isinstance(value, (int, float)):
                        field_stats[field]["values"].append(value)
        
        # Calculate overall statistics
        total_nulls = sum(stats["null_count"] for stats in field_stats.values())
        total_uniques = sum(len(stats["unique_values"]) for stats in field_stats.values())
        total_duplicates = total_records * len(field_stats) - total_uniques
        
        # Calculate statistical measures for numeric fields
        numeric_fields = [field for field, stats in field_stats.items() if stats["values"]]
        
        min_val = None
        max_val = None
        mean_val = None
        std_val = None
        
        if numeric_fields:
            all_values = []
            for field in numeric_fields:
                all_values.extend(field_stats[field]["values"])
            
            if all_values:
                min_val = min(all_values)
                max_val = max(all_values)
                mean_val = statistics.mean(all_values)
                std_val = statistics.stdev(all_values) if len(all_values) > 1 else 0.0
        
        profile = QualityProfile(
            dataset_name=dataset_name,
            total_records=total_records,
            null_count=total_nulls,
            unique_count=total_uniques,
            duplicate_count=total_duplicates,
            min_value=min_val,
            max_value=max_val,
            mean_value=mean_val,
            std_dev=std_val,
            null_percentage=(total_nulls / (total_records * len(field_stats))) * 100 if field_stats else 0.0,
            duplicate_percentage=(total_duplicates / (total_records * len(field_stats))) * 100 if field_stats else 0.0,
            profiled_at=time.time()
        )
        
        self.quality_profiles[dataset_name] = profile
        self.logger.info(f"Profiled dataset: {dataset_name}")
        
        return profile_id
    
    async def validate_dataset(self, dataset_name: str, data: List[Dict[str, Any]]) -> str:
        """
        Validate a dataset against quality rules
        
        Args:
            dataset_name: Name of the dataset
            data: Dataset records
            
        Returns:
            Check ID
        """
        check_id = str(uuid.uuid4())
        
        total_records = len(data)
        passed_records = 0
        failed_records = 0
        error_details = []
        
        # Get active rules for this dataset
        active_rules = [rule for rule in self.quality_rules.values() if rule.enabled]
        
        if not active_rules:
            status = QualityStatus.SKIPPED
            self.logger.warning(f"No active quality rules for dataset: {dataset_name}")
        else:
            # Validate each record against all rules
            for i, record in enumerate(data):
                record_passed = True
                
                for rule in active_rules:
                    if not self._validate_record_against_rule(record, rule):
                        record_passed = False
                        error_details.append({
                            "record_index": i,
                            "rule_id": rule.rule_id,
                            "rule_name": rule.name,
                            "field_name": rule.field_name,
                            "error_message": self._get_error_message(rule, record.get(rule.field_name))
                        })
                
                if record_passed:
                    passed_records += 1
                else:
                    failed_records += 1
            
            # Determine overall status
            failure_rate = failed_records / total_records if total_records > 0 else 0.0
            
            if failure_rate == 0:
                status = QualityStatus.PASSED
            elif failure_rate < 0.1:  # Less than 10% failure
                status = QualityStatus.WARNING
            else:
                status = QualityStatus.FAILED
        
        check = QualityCheck(
            check_id=check_id,
            rule_id="dataset_check",  # Aggregate check
            dataset_name=dataset_name,
            total_records=total_records,
            passed_records=passed_records,
            failed_records=failed_records,
            status=status,
            error_details=error_details,
            execution_time=0.0,  # Will be calculated
            executed_at=time.time()
        )
        
        start_time = time.time()
        
        # Execute individual rule validations
        for rule in active_rules:
            await self._validate_rule_async(check_id, rule, data)
        
        check.execution_time = time.time() - start_time
        self.quality_checks[check_id] = check
        
        # Update statistics
        self.quality_stats["total_checks"] += 1
        if status == QualityStatus.PASSED:
            self.quality_stats["passed_checks"] += 1
        else:
            self.quality_stats["failed_checks"] += 1
        
        self._update_quality_score()
        
        self.logger.info(f"Quality check completed: {check_id} ({status.value})")
        return check_id
    
    def get_quality_report(self, check_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed quality report for a check"""
        if check_id not in self.quality_checks:
            return None
        
        check = self.quality_checks[check_id]
        
        return {
            "check_id": check.check_id,
            "dataset_name": check.dataset_name,
            "status": check.status.value,
            "total_records": check.total_records,
            "passed_records": check.passed_records,
            "failed_records": check.failed_records,
            "failure_rate": check.failed_records / check.total_records if check.total_records > 0 else 0.0,
            "execution_time": check.execution_time,
            "executed_at": datetime.fromtimestamp(check.executed_at).isoformat(),
            "error_details": check.error_details[:100],  # Limit error details
            "error_summary": self._summarize_errors(check.error_details)
        }
    
    def get_quality_stats(self) -> Dict[str, Any]:
        """Get quality statistics"""
        return {
            "total_rules": self.quality_stats["total_rules"],
            "active_rules": self.quality_stats["active_rules"],
            "total_checks": self.quality_stats["total_checks"],
            "passed_checks": self.quality_stats["passed_checks"],
            "failed_checks": self.quality_stats["failed_checks"],
            "quality_score": self.quality_stats["quality_score"],
            "success_rate": self.quality_stats["passed_checks"] / self.quality_stats["total_checks"] if self.quality_stats["total_checks"] > 0 else 0.0,
            "tolerance_threshold": self.tolerance_threshold,
            "batch_size": self.batch_size
        }
    
    def _validate_record_against_rule(self, record: Dict[str, Any], rule: QualityRule) -> bool:
        """Validate a single record against a quality rule"""
        field_value = record.get(rule.field_name)
        
        try:
            if rule.rule_type == QualityRuleType.NOT_NULL:
                return field_value is not None and field_value != ""
            
            elif rule.rule_type == QualityRuleType.UNIQUE:
                # This would need to check against all records - simplified for single record
                return True  # Would need full dataset for proper unique validation
            
            elif rule.rule_type == QualityRuleType.RANGE:
                min_val = rule.parameters.get("min")
                max_val = rule.parameters.get("max")
                
                if not isinstance(field_value, (int, float)):
                    return False
                
                if min_val is not None and field_value < min_val:
                    return False
                if max_val is not None and field_value > max_val:
                    return False
                return True
            
            elif rule.rule_type == QualityRuleType.REGEX:
                pattern = rule.parameters.get("pattern", "")
                if not pattern:
                    return True
                return bool(re.match(pattern, str(field_value)))
            
            elif rule.rule_type == QualityRuleType.CUSTOM:
                # Execute custom validation function
                custom_func = rule.parameters.get("function")
                if custom_func:
                    return custom_func(field_value)
                return True
            
            elif rule.rule_type == QualityRuleType.REFERENTIAL_INTEGRITY:
                # Check if foreign key exists in referenced dataset
                ref_dataset = rule.parameters.get("reference_dataset")
                ref_field = rule.parameters.get("reference_field")
                # Simplified - would need actual dataset lookup
                return True
            
            elif rule.rule_type == QualityRuleType.STATISTICAL:
                # Statistical validation based on historical data
                profile = self.quality_profiles.get(rule.parameters.get("dataset_name"))
                if not profile:
                    return True
                
                if isinstance(field_value, (int, float)):
                    mean = profile.mean_value
                    std = profile.std_dev
                    threshold = rule.parameters.get("threshold", 3)
                    
                    if mean is not None and std is not None:
                        z_score = abs(field_value - mean) / std if std > 0 else 0
                        return z_score <= threshold
                
                return True
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error validating rule {rule.rule_id}: {e}")
            return False
    
    def _get_error_message(self, rule: QualityRule, field_value: Any) -> str:
        """Get error message for a failed rule"""
        if rule.rule_type == QualityRuleType.NOT_NULL:
            return f"Field '{rule.field_name}' cannot be null or empty"
        elif rule.rule_type == QualityRuleType.RANGE:
            return f"Field '{rule.field_name}' value {field_value} is outside allowed range"
        elif rule.rule_type == QualityRuleType.REGEX:
            return f"Field '{rule.field_name}' value '{field_value}' does not match required pattern"
        elif rule.rule_type == QualityRuleType.STATISTICAL:
            return f"Field '{rule.field_name}' value {field_value} is statistically anomalous"
        else:
            return f"Field '{rule.field_name}' failed validation: {rule.description}"
    
    async def _validate_rule_async(self, check_id: str, rule: QualityRule, data: List[Dict[str, Any]]):
        """Validate a rule against dataset asynchronously"""
        # This would implement the actual rule validation logic
        # For now, it's a placeholder for future implementation
        await asyncio.sleep(0.1)
    
    def _summarize_errors(self, error_details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize error details"""
        if not error_details:
            return {"total_errors": 0, "error_types": {}}
        
        error_types = {}
        for error in error_details:
            rule_name = error.get("rule_name", "Unknown")
            if rule_name not in error_types:
                error_types[rule_name] = 0
            error_types[rule_name] += 1
        
        return {
            "total_errors": len(error_details),
            "error_types": error_types,
            "top_errors": sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def _update_quality_score(self):
        """Update overall quality score"""
        if self.quality_stats["total_checks"] == 0:
            self.quality_stats["quality_score"] = 100.0
        else:
            success_rate = self.quality_stats["passed_checks"] / self.quality_stats["total_checks"]
            self.quality_stats["quality_score"] = success_rate * 100.0
    
    async def _monitoring_loop(self):
        """Background monitoring for quality issues"""
        while True:
            try:
                self._check_quality_trends()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(300)
    
    def _check_quality_trends(self):
        """Check for quality trends and anomalies"""
        # Analyze recent quality checks for trends
        recent_checks = [
            check for check in self.quality_checks.values()
            if time.time() - check.executed_at < 3600  # Last hour
        ]
        
        if len(recent_checks) < 10:
            return
        
        # Calculate trend in failure rate
        failure_rates = [check.failed_records / check.total_records for check in recent_checks if check.total_records > 0]
        
        if len(failure_rates) > 5:
            recent_avg = statistics.mean(failure_rates[-5:])
            earlier_avg = statistics.mean(failure_rates[:-5])
            
            if recent_avg > earlier_avg * (1 + self.tolerance_threshold):
                self.logger.warning(f"Quality degradation detected: failure rate increased from {earlier_avg:.2%} to {recent_avg:.2%}")

# Global quality checker instance
_quality_checker = DataQualityChecker({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_rule", "profile_dataset", "validate_dataset", 
                     "get_report", "get_stats", "get_profile"
            - rule_data: Quality rule configuration
            - dataset_data: Dataset information
            - validation_data: Validation parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_rule":
            rule_data = payload.get("rule_data", {})
            
            rule_id = _quality_checker.create_quality_rule(
                name=rule_data.get("name", "Quality Rule"),
                description=rule_data.get("description", ""),
                rule_type=QualityRuleType(rule_data.get("rule_type", "not_null")),
                field_name=rule_data.get("field_name", ""),
                parameters=rule_data.get("parameters", {}),
                severity=QualitySeverity(rule_data.get("severity", "error")),
                enabled=rule_data.get("enabled", True)
            )
            
            return {
                "result": {
                    "rule_id": rule_id,
                    "message": f"Created quality rule: {rule_id}"
                },
                "metadata": {
                    "action": "create_rule",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "profile_dataset":
            dataset_data = payload.get("dataset_data", {})
            
            profile_id = _quality_checker.profile_dataset(
                dataset_name=dataset_data.get("name", "Dataset"),
                data=dataset_data.get("data", [])
            )
            
            return {
                "result": {
                    "profile_id": profile_id,
                    "message": f"Profiled dataset: {dataset_data.get('name', 'Dataset')}"
                },
                "metadata": {
                    "action": "profile_dataset",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "validate_dataset":
            validation_data = payload.get("validation_data", {})
            
            check_id = await _quality_checker.validate_dataset(
                dataset_name=validation_data.get("dataset_name", "Dataset"),
                data=validation_data.get("data", [])
            )
            
            return {
                "result": {
                    "check_id": check_id,
                    "message": f"Validated dataset: {validation_data.get('dataset_name', 'Dataset')}"
                },
                "metadata": {
                    "action": "validate_dataset",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_report":
            check_id = payload.get("check_id", "")
            report = _quality_checker.get_quality_report(check_id)
            
            return {
                "result": report,
                "metadata": {
                    "action": "get_report",
                    "timestamp": datetime.now().isoformat(),
                    "check_id": check_id
                }
            }
        
        elif action == "get_stats":
            stats = _quality_checker.get_quality_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_profile":
            dataset_name = payload.get("dataset_name", "")
            if dataset_name in _quality_checker.quality_profiles:
                profile = _quality_checker.quality_profiles[dataset_name]
                return {
                    "result": {
                        "dataset_name": profile.dataset_name,
                        "total_records": profile.total_records,
                        "null_count": profile.null_count,
                        "unique_count": profile.unique_count,
                        "duplicate_count": profile.duplicate_count,
                        "null_percentage": profile.null_percentage,
                        "duplicate_percentage": profile.duplicate_percentage,
                        "min_value": profile.min_value,
                        "max_value": profile.max_value,
                        "mean_value": profile.mean_value,
                        "std_dev": profile.std_dev,
                        "profiled_at": datetime.fromtimestamp(profile.profiled_at).isoformat()
                    },
                    "metadata": {
                        "action": "get_profile",
                        "timestamp": datetime.now().isoformat(),
                        "dataset_name": dataset_name
                    }
                }
            else:
                return {
                    "result": None,
                    "metadata": {
                        "action": "get_profile",
                        "timestamp": datetime.now().isoformat(),
                        "dataset_name": dataset_name
                    }
                }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in data_quality_checker: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the data quality checker skill"""
    
    # Create quality rules
    rule1_id = await invoke({
        "action": "create_rule",
        "rule_data": {
            "name": "Email Format Validation",
            "description": "Validate email format",
            "rule_type": "regex",
            "field_name": "email",
            "parameters": {
                "pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            },
            "severity": "error"
        }
    })
    
    rule2_id = await invoke({
        "action": "create_rule",
        "rule_data": {
            "name": "Age Range Validation",
            "description": "Validate age is between 0 and 120",
            "rule_type": "range",
            "field_name": "age",
            "parameters": {
                "min": 0,
                "max": 120
            },
            "severity": "warning"
        }
    })
    
    print(f"Created rules: {rule1_id['result']['rule_id']}, {rule2_id['result']['rule_id']}")
    
    # Sample dataset
    sample_data = [
        {"name": "John Doe", "email": "john@example.com", "age": 30},
        {"name": "Jane Smith", "email": "jane@invalid", "age": 150},  # Invalid email and age
        {"name": "Bob Johnson", "email": "bob@example.com", "age": 25},
        {"name": "Alice Brown", "email": "", "age": 35},  # Missing email
    ]
    
    # Profile dataset
    profile_id = await invoke({
        "action": "profile_dataset",
        "dataset_data": {
            "name": "user_data",
            "data": sample_data
        }
    })
    
    print(f"Profiled dataset: {profile_id['result']['profile_id']}")
    
    # Validate dataset
    check_id = await invoke({
        "action": "validate_dataset",
        "validation_data": {
            "dataset_name": "user_data",
            "data": sample_data
        }
    })
    
    print(f"Validation check: {check_id['result']['check_id']}")
    
    # Get quality report
    report = await invoke({
        "action": "get_report",
        "check_id": check_id['result']['check_id']
    })
    
    print(f"Quality report: {report['result']}")
    
    # Get quality statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Quality stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
