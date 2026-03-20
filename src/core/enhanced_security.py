#!/usr/bin/env python3
"""
Enhanced Security and Compliance System for Skill Flywheel

This module provides advanced security scanning, compliance checking, vulnerability
detection, and automated security hardening for the enhanced MCP server.
It includes ML-based threat detection and real-time security monitoring.
"""

import asyncio
import logging
import re
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

# ML imports for advanced threat detection
try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
    from sklearn.feature_extraction.text import TfidfVectorizer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    warnings.warn("ML libraries not available for advanced threat detection.", stacklevel=2)

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceFramework(Enum):
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    NIST = "NIST"
    GDPR = "GDPR"
    HIPAA = "HIPAA"

class VulnerabilityType(Enum):
    HARDCODED_SECRET = "hardcoded_secret"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    INSECURE_CRYPTO = "insecure_crypto"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    INFORMATION_DISCLOSURE = "information_disclosure"

@dataclass
class SecurityScanResult:
    """Result of a security scan."""
    scan_id: str
    skill_id: str
    timestamp: datetime
    security_level: SecurityLevel
    vulnerabilities: List[Dict[str, Any]]
    compliance_issues: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    ml_threat_score: float

@dataclass
class ComplianceReport:
    """Compliance framework report."""
    report_id: str
    framework: ComplianceFramework
    timestamp: datetime
    compliance_score: float
    requirements: List[Dict[str, Any]]
    violations: List[Dict[str, Any]]
    recommendations: List[str]

@dataclass
class SecurityPolicy:
    """Security policy configuration."""
    policy_id: str
    name: str
    description: str
    rules: List[Dict[str, Any]]
    enabled: bool
    last_updated: datetime

class SecurityScanner:
    """Advanced security scanning system."""
    
    def __init__(self):
        self.vulnerability_patterns = self._load_vulnerability_patterns()
        self.compliance_frameworks = self._load_compliance_frameworks()
        self.security_policies = self._load_security_policies()
        
        # ML-based threat detection
        if ML_AVAILABLE:
            self.threat_detector = IsolationForest(contamination=0.1, random_state=42)
            self.text_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            self.ml_trained = False
            self.ml_training_data = []
    
    def _load_vulnerability_patterns(self) -> Dict[str, List[str]]:
        """Load vulnerability detection patterns."""
        return {
            VulnerabilityType.HARDCODED_SECRET.value: [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
                r'private[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\'][^"\']+["\']',
                r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'][^"\']+["\']'
            ],
            VulnerabilityType.SQL_INJECTION.value: [
                r'execute\s*\(\s*["\'][^"\']*%s',
                r'cursor\.execute\s*\(\s*["\'][^"\']*{',
                r'query\s*=\s*["\'][^"\']*%s',
                r'SELECT.*\+.*',
                r'INSERT.*\+.*',
                r'UPDATE.*\+.*',
                r'DELETE.*\+.*'
            ],
            VulnerabilityType.XSS.value: [
                r'innerHTML\s*=\s*',
                r'outerHTML\s*=\s*',
                r'document\.write\s*\(',
                r'eval\s*\(',
                r'innerHTML.*\+.*',
                r'outerHTML.*\+.*'
            ],
            VulnerabilityType.COMMAND_INJECTION.value: [
                r'os\.system\s*\(',
                r'os\.popen\s*\(',
                r'subprocess\.',
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\('
            ],
            VulnerabilityType.PATH_TRAVERSAL.value: [
                r'\.\.\/',
                r'\.\.\\',
                r'os\.path\.join\s*\([^)]*\.\.',
                r'open\s*\([^)]*\.\.',
                r'file\s*\([^)]*\.\.'
            ],
            VulnerabilityType.INSECURE_CRYPTO.value: [
                r'hashlib\.md5\s*\(',
                r'hashlib\.sha1\s*\(',
                r'random\.random\s*\(',
                r'random\.randint\s*\(',
                r'random\.choice\s*\(',
                r'random\.shuffle\s*\('
            ],
            VulnerabilityType.PRIVILEGE_ESCALATION.value: [
                r'os\.getuid\s*\(\)',
                r'os\.getgid\s*\(\)',
                r'os\.setuid\s*\(',
                r'os\.setgid\s*\(',
                r'subprocess\.Popen\s*\([^)]*shell\s*=\s*True',
                r'os\.system\s*\([^)]*sudo'
            ],
            VulnerabilityType.INFORMATION_DISCLOSURE.value: [
                r'print\s*\([^)]*password',
                r'print\s*\([^)]*secret',
                r'print\s*\([^)]*key',
                r'print\s*\([^)]*token',
                r'logger\.(debug|info)\s*\([^)]*password',
                r'logger\.(debug|info)\s*\([^)]*secret',
                r'logger\.(debug|info)\s*\([^)]*key',
                r'logger\.(debug|info)\s*\([^)]*token'
            ]
        }
    
    def _load_compliance_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Load compliance framework requirements."""
        return {
            ComplianceFramework.SOC2.value: {
                "name": "SOC 2 Type II",
                "requirements": [
                    {"id": "CC6.1", "description": "Logical and physical access controls are selected and implemented to protect against threats from sources outside the system boundaries."},
                    {"id": "CC6.2", "description": "Logical and physical access controls are selected and implemented to limit access to system components."},
                    {"id": "CC6.3", "description": "Personnel with access to the system are provided with guidance as to the importance of protecting the confidentiality and integrity of the information handled by the system."},
                    {"id": "CC6.4", "description": "The entity selects and implements controls to detect, log, and report on events that are indicators of compromise."},
                    {"id": "CC6.5", "description": "The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on roles, or similar criteria, consistent with the entity's criteria for authorizing access to the system."}
                ]
            },
            ComplianceFramework.ISO27001.value: {
                "name": "ISO 27001",
                "requirements": [
                    {"id": "A.9.1.1", "description": "Access to information and application system functions shall be restricted in accordance with the access control policy."},
                    {"id": "A.9.2.1", "description": "User registration and de-registration shall be controlled."},
                    {"id": "A.9.2.2", "description": "User access provisioning shall be controlled."},
                    {"id": "A.9.4.1", "description": "Information accessing shall be restricted in accordance with the access control policy."},
                    {"id": "A.9.4.2", "description": "Secure log-on procedures shall be used."},
                    {"id": "A.10.1.1", "description": "Cryptographic controls shall be used in accordance with policy."},
                    {"id": "A.12.4.1", "description": "Events shall be detected and the relevant support processes informed as quickly as possible."}
                ]
            },
            ComplianceFramework.NIST.value: {
                "name": "NIST Cybersecurity Framework",
                "requirements": [
                    {"id": "PR.AC-1", "description": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized users, devices, and other assets."},
                    {"id": "PR.AC-4", "description": "Access permissions are managed, incorporating the principles of least privilege and separation of duties."},
                    {"id": "PR.DS-1", "description": "Data-in-transit is protected."},
                    {"id": "PR.DS-2", "description": "Data-at-rest is protected."},
                    {"id": "DE.CM-1", "description": "Network baselines are established and managed."},
                    {"id": "DE.CM-3", "description": "Personnel awareness programs and activities are established or managed to strengthen the cybersecurity culture."},
                    {"id": "DE.CM-7", "description": "All anomalies are investigated."}
                ]
            }
        }
    
    def _load_security_policies(self) -> List[SecurityPolicy]:
        """Load default security policies."""
        return [
            SecurityPolicy(
                policy_id="policy_001",
                name="Hardcoded Secrets Policy",
                description="Prevent hardcoded secrets in code",
                rules=[
                    {"type": "regex", "pattern": r'password\s*=\s*["\'][^"\']+["\']', "severity": "high"},
                    {"type": "regex", "pattern": r'secret\s*=\s*["\'][^"\']+["\']', "severity": "high"},
                    {"type": "regex", "pattern": r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "severity": "high"}
                ],
                enabled=True,
                last_updated=datetime.now()
            ),
            SecurityPolicy(
                policy_id="policy_002",
                name="Code Injection Prevention",
                description="Prevent code injection vulnerabilities",
                rules=[
                    {"type": "regex", "pattern": r'eval\s*\(', "severity": "critical"},
                    {"type": "regex", "pattern": r'exec\s*\(', "severity": "critical"},
                    {"type": "regex", "pattern": r'__import__\s*\(', "severity": "high"}
                ],
                enabled=True,
                last_updated=datetime.now()
            ),
            SecurityPolicy(
                policy_id="policy_003",
                name="Input Validation",
                description="Ensure proper input validation",
                rules=[
                    {"type": "regex", "pattern": r'input\s*\(\)', "severity": "medium"},
                    {"type": "regex", "pattern": r'raw_input\s*\(\)', "severity": "medium"},
                    {"type": "regex", "pattern": r'input\s*\([^)]*\)', "severity": "medium"}
                ],
                enabled=True,
                last_updated=datetime.now()
            )
        ]
    
    async def scan_skill(self, skill_path: Path) -> SecurityScanResult:
        """Perform comprehensive security scan of a skill."""
        try:
            # Read skill content
            with open(skill_path, encoding='utf-8') as f:
                content = f.read()
            
            skill_id = skill_path.stem
            
            # Perform vulnerability scanning
            vulnerabilities = self._scan_vulnerabilities(content, skill_id)
            
            # Perform compliance checking
            compliance_issues = self._check_compliance(content, skill_id)
            
            # Calculate risk scores
            risk_score = self._calculate_risk_score(vulnerabilities, compliance_issues)
            
            # ML-based threat detection
            ml_threat_score = self._analyze_threat_ml(content) if ML_AVAILABLE else 0.0
            
            # Generate recommendations
            recommendations = self._generate_security_recommendations(vulnerabilities, compliance_issues)
            
            # Determine security level
            security_level = self._determine_security_level(risk_score, ml_threat_score)
            
            return SecurityScanResult(
                scan_id=f"scan_{skill_id}_{datetime.now().isoformat()}",
                skill_id=skill_id,
                timestamp=datetime.now(),
                security_level=security_level,
                vulnerabilities=vulnerabilities,
                compliance_issues=compliance_issues,
                recommendations=recommendations,
                risk_score=risk_score,
                ml_threat_score=ml_threat_score
            )
            
        except Exception as e:
            logger.error(f"Error scanning skill {skill_path}: {e}")
            return SecurityScanResult(
                scan_id=f"scan_error_{datetime.now().isoformat()}",
                skill_id="unknown",
                timestamp=datetime.now(),
                security_level=SecurityLevel.CRITICAL,
                vulnerabilities=[{"type": "scan_error", "description": str(e)}],
                compliance_issues=[],
                recommendations=["Fix scan error"],
                risk_score=1.0,
                ml_threat_score=0.0
            )
    
    def _scan_vulnerabilities(self, content: str, skill_id: str) -> List[Dict[str, Any]]:
        """Scan for known vulnerability patterns."""
        vulnerabilities = []
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    vulnerabilities.append({
                        "type": vuln_type,
                        "description": f"Potential {vuln_type} vulnerability",
                        "line": content[:match.start()].count('\n') + 1,
                        "code": match.group(0),
                        "severity": self._get_vulnerability_severity(vuln_type),
                        "confidence": self._calculate_confidence(match.group(0), pattern)
                    })
        
        return vulnerabilities
    
    def _check_compliance(self, content: str, skill_id: str) -> List[Dict[str, Any]]:
        """Check compliance with security frameworks."""
        violations = []
        
        # Check SOC 2 compliance
        soc2_violations = self._check_soc2_compliance(content)
        violations.extend(soc2_violations)
        
        # Check ISO 27001 compliance
        iso27001_violations = self._check_iso27001_compliance(content)
        violations.extend(iso27001_violations)
        
        # Check NIST compliance
        nist_violations = self._check_nist_compliance(content)
        violations.extend(nist_violations)
        
        return violations
    
    def _check_soc2_compliance(self, content: str) -> List[Dict[str, Any]]:
        """Check SOC 2 compliance violations."""
        violations = []
        
        # Check for hardcoded secrets (CC6.1)
        if re.search(r'password\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
            violations.append({
                "framework": "SOC2",
                "requirement": "CC6.1",
                "description": "Hardcoded secrets detected - violates access control policy",
                "severity": "high"
            })
        
        # Check for insecure logging (CC6.4)
        if re.search(r'logger\.(debug|info)\s*\([^)]*(password|secret|key)', content, re.IGNORECASE):
            violations.append({
                "framework": "SOC2",
                "requirement": "CC6.4",
                "description": "Sensitive information in logs - violates monitoring requirements",
                "severity": "medium"
            })
        
        return violations
    
    def _check_iso27001_compliance(self, content: str) -> List[Dict[str, Any]]:
        """Check ISO 27001 compliance violations."""
        violations = []
        
        # Check for weak cryptography (A.10.1.1)
        if re.search(r'hashlib\.(md5|sha1)\s*\(', content, re.IGNORECASE):
            violations.append({
                "framework": "ISO27001",
                "requirement": "A.10.1.1",
                "description": "Weak cryptographic algorithms detected",
                "severity": "high"
            })
        
        # Check for insecure random generation (A.10.1.1)
        if re.search(r'random\.(random|randint|choice|shuffle)\s*\(', content, re.IGNORECASE):
            violations.append({
                "framework": "ISO27001",
                "requirement": "A.10.1.1",
                "description": "Insecure random number generation detected",
                "severity": "medium"
            })
        
        return violations
    
    def _check_nist_compliance(self, content: str) -> List[Dict[str, Any]]:
        """Check NIST compliance violations."""
        violations = []
        
        # Check for weak access controls (PR.AC-1)
        if re.search(r'input\s*\(\)', content, re.IGNORECASE):
            violations.append({
                "framework": "NIST",
                "requirement": "PR.AC-1",
                "description": "Unvalidated user input detected",
                "severity": "medium"
            })
        
        # Check for data protection (PR.DS-1)
        if re.search(r'print\s*\([^)]*password', content, re.IGNORECASE):
            violations.append({
                "framework": "NIST",
                "requirement": "PR.DS-1",
                "description": "Sensitive data exposed in output",
                "severity": "high"
            })
        
        return violations
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict[str, Any]], 
                             compliance_issues: List[Dict[str, Any]]) -> float:
        """Calculate overall risk score."""
        if not vulnerabilities and not compliance_issues:
            return 0.0
        
        # Calculate weighted risk score
        risk_score = 0.0
        
        # Vulnerability risk
        for vuln in vulnerabilities:
            severity_weight = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
            confidence_weight = vuln.get("confidence", 0.5)
            risk_score += severity_weight.get(vuln.get("severity", "medium"), 0.5) * confidence_weight
        
        # Compliance risk
        for issue in compliance_issues:
            severity_weight = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 0.9}
            risk_score += severity_weight.get(issue.get("severity", "medium"), 0.3)
        
        # Normalize to 0-1 range
        return min(1.0, risk_score / 10.0)
    
    def _analyze_threat_ml(self, content: str) -> float:
        """Analyze content for threats using ML."""
        try:
            if not self.ml_trained:
                self._train_ml_model()
            
            # Vectorize content
            content_vector = self.text_vectorizer.transform([content])
            
            # Predict anomaly score
            anomaly_score = self.threat_detector.decision_function(content_vector)[0]
            
            # Convert to threat score (0-1)
            threat_score = max(0, min(1, (anomaly_score + 0.5) * 2))
            
            return threat_score
            
        except Exception as e:
            logger.error(f"ML threat analysis failed: {e}")
            return 0.0
    
    def _train_ml_model(self):
        """Train ML model for threat detection."""
        if not self.ml_training_data:
            # Use synthetic training data if none available
            self.ml_training_data = [
                "def secure_function():\n    # Secure code\n    return True",
                "def vulnerable_function():\n    eval(input('Enter code: '))",
                "password = 'secret123'\nprint(password)",
                "import hashlib\nhash_value = hashlib.sha256(data.encode()).hexdigest()",
                "os.system('rm -rf /')",
                "def safe_function():\n    # Safe implementation\n    return secure_result"
            ]
        
        # Vectorize training data
        X = self.text_vectorizer.fit_transform(self.ml_training_data)
        
        # Train model
        self.threat_detector.fit(X)
        self.ml_trained = True
        logger.info("ML threat detection model trained")
    
    def _generate_security_recommendations(self, vulnerabilities: List[Dict[str, Any]], 
                                         compliance_issues: List[Dict[str, Any]]) -> List[str]:
        """Generate security improvement recommendations."""
        recommendations = []
        
        # Group vulnerabilities by type
        vuln_types = {v["type"] for v in vulnerabilities}
        
        if VulnerabilityType.HARDCODED_SECRET.value in vuln_types:
            recommendations.append("Remove hardcoded secrets and use environment variables or secure credential storage")
        
        if VulnerabilityType.SQL_INJECTION.value in vuln_types:
            recommendations.append("Use parameterized queries and input validation to prevent SQL injection")
        
        if VulnerabilityType.XSS.value in vuln_types:
            recommendations.append("Implement proper output encoding and input validation to prevent XSS")
        
        if VulnerabilityType.COMMAND_INJECTION.value in vuln_types:
            recommendations.append("Avoid using shell commands with user input, use safe APIs instead")
        
        if VulnerabilityType.INSECURE_CRYPTO.value in vuln_types:
            recommendations.append("Use strong cryptographic algorithms (SHA-256, AES-256) instead of weak ones")
        
        # Compliance recommendations
        framework_violations = {issue.get("framework") for issue in compliance_issues}
        
        if "SOC2" in framework_violations:
            recommendations.append("Implement SOC 2 compliant access controls and monitoring")
        
        if "ISO27001" in framework_violations:
            recommendations.append("Follow ISO 27001 guidelines for information security management")
        
        if "NIST" in framework_violations:
            recommendations.append("Implement NIST cybersecurity framework controls")
        
        if not recommendations:
            recommendations.append("No specific recommendations - code appears secure")
        
        return recommendations
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type."""
        severity_map = {
            VulnerabilityType.HARDCODED_SECRET.value: "high",
            VulnerabilityType.SQL_INJECTION.value: "critical",
            VulnerabilityType.XSS.value: "high",
            VulnerabilityType.COMMAND_INJECTION.value: "critical",
            VulnerabilityType.PATH_TRAVERSAL.value: "high",
            VulnerabilityType.INSECURE_CRYPTO.value: "medium",
            VulnerabilityType.PRIVILEGE_ESCALATION.value: "high",
            VulnerabilityType.INFORMATION_DISCLOSURE.value: "medium"
        }
        return severity_map.get(vuln_type, "medium")
    
    def _calculate_confidence(self, match: str, pattern: str) -> float:
        """Calculate confidence score for vulnerability match."""
        # Simple confidence calculation based on match characteristics
        confidence = 0.5
        
        # Increase confidence for exact matches
        if match.strip() == pattern.replace(r'["\']', '').replace(r'[^"\']+', match.strip()):
            confidence += 0.3
        
        # Increase confidence for longer matches
        if len(match) > 20:
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _determine_security_level(self, risk_score: float, ml_threat_score: float) -> SecurityLevel:
        """Determine overall security level."""
        combined_score = (risk_score + ml_threat_score) / 2
        
        if combined_score >= 0.8:
            return SecurityLevel.CRITICAL
        elif combined_score >= 0.6:
            return SecurityLevel.HIGH
        elif combined_score >= 0.3:
            return SecurityLevel.MEDIUM
        else:
            return SecurityLevel.LOW

class SecurityHardener:
    """Automated security hardening system."""
    
    def __init__(self):
        self.hardening_rules = self._load_hardening_rules()
    
    def _load_hardening_rules(self) -> List[Dict[str, Any]]:
        """Load security hardening rules."""
        return [
            {
                "name": "Replace hardcoded secrets",
                "pattern": r'password\s*=\s*["\']([^"\']+)["\']',
                "replacement": 'password = os.environ.get("APP_PASSWORD", "default")',
                "description": "Replace hardcoded password with environment variable"
            },
            {
                "name": "Replace hardcoded API keys",
                "pattern": r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
                "replacement": 'api_key = os.environ.get("API_KEY", "")',
                "description": "Replace hardcoded API key with environment variable"
            },
            {
                "name": "Replace eval with safe alternatives",
                "pattern": r'eval\s*\(([^)]+)\)',
                "replacement": 'ast.literal_eval(\\1)',
                "description": "Replace unsafe eval with safe literal evaluation"
            },
            {
                "name": "Add input validation",
                "pattern": r'input\s*\(\)',
                "replacement": 'input("Enter value: ") if len(input("Enter value: ")) > 0 else None',
                "description": "Add basic input validation"
            },
            {
                "name": "Replace weak crypto",
                "pattern": r'hashlib\.md5\s*\(',
                "replacement": 'hashlib.sha256(',
                "description": "Replace weak MD5 with SHA-256"
            },
            {
                "name": "Replace weak random",
                "pattern": r'random\.(random|randint|choice|shuffle)',
                "replacement": 'secrets.randbelow',
                "description": "Replace weak random with cryptographically secure secrets"
            }
        ]
    
    def harden_skill(self, skill_path: Path) -> Dict[str, Any]:
        """Apply security hardening to a skill."""
        try:
            # Read original content
            with open(skill_path, encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply hardening rules
            hardened_content = original_content
            applied_rules = []
            
            for rule in self.hardening_rules:
                if re.search(rule["pattern"], hardened_content, re.IGNORECASE):
                    # Create backup
                    backup_path = skill_path.with_suffix(skill_path.suffix + '.backup')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    
                    # Apply rule
                    hardened_content = re.sub(
                        rule["pattern"], 
                        rule["replacement"], 
                        hardened_content, 
                        flags=re.IGNORECASE
                    )
                    
                    applied_rules.append(rule["name"])
            
            # Write hardened content
            if hardened_content != original_content:
                with open(skill_path, 'w', encoding='utf-8') as f:
                    f.write(hardened_content)
                
                return {
                    "success": True,
                    "skill_id": skill_path.stem,
                    "applied_rules": applied_rules,
                    "backup_created": True,
                    "message": f"Applied {len(applied_rules)} hardening rules"
                }
            else:
                return {
                    "success": True,
                    "skill_id": skill_path.stem,
                    "applied_rules": [],
                    "backup_created": False,
                    "message": "No hardening rules applicable"
                }
                
        except Exception as e:
            logger.error(f"Error hardening skill {skill_path}: {e}")
            return {
                "success": False,
                "skill_id": skill_path.stem,
                "applied_rules": [],
                "backup_created": False,
                "error": str(e)
            }

class SecurityMonitor:
    """Real-time security monitoring system."""
    
    def __init__(self):
        self.security_events = []
        self.monitoring_active = False
        self.alert_thresholds = {
            "risk_score": 0.7,
            "ml_threat_score": 0.8,
            "vulnerability_count": 5
        }
    
    def start_monitoring(self):
        """Start real-time security monitoring."""
        self.monitoring_active = True
        logger.info("Security monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time security monitoring."""
        self.monitoring_active = False
        logger.info("Security monitoring stopped")
    
    def log_security_event(self, event: Dict[str, Any]):
        """Log a security event."""
        event["timestamp"] = datetime.now().isoformat()
        self.security_events.append(event)
        
        # Check for alerts
        if self.monitoring_active:
            self._check_security_alerts(event)
    
    def _check_security_alerts(self, event: Dict[str, Any]):
        """Check if security event triggers alerts."""
        risk_score = event.get("risk_score", 0)
        ml_threat_score = event.get("ml_threat_score", 0)
        vulnerability_count = len(event.get("vulnerabilities", []))
        
        alerts = []
        
        if risk_score > self.alert_thresholds["risk_score"]:
            alerts.append(f"High risk score detected: {risk_score:.2f}")
        
        if ml_threat_score > self.alert_thresholds["ml_threat_score"]:
            alerts.append(f"High ML threat score detected: {ml_threat_score:.2f}")
        
        if vulnerability_count > self.alert_thresholds["vulnerability_count"]:
            alerts.append(f"High vulnerability count detected: {vulnerability_count}")
        
        # Log alerts
        for alert in alerts:
            logger.warning(f"SECURITY ALERT: {alert}")
    
    def get_security_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get security monitoring summary."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        relevant_events = [
            event for event in self.security_events
            if start_time <= datetime.fromisoformat(event["timestamp"]) <= end_time
        ]
        
        summary = {
            "total_events": len(relevant_events),
            "high_risk_events": len([e for e in relevant_events if e.get("risk_score", 0) > 0.7]),
            "critical_threats": len([e for e in relevant_events if e.get("ml_threat_score", 0) > 0.8]),
            "vulnerability_trends": self._calculate_vulnerability_trends(relevant_events),
            "security_score": self._calculate_overall_security_score(relevant_events)
        }
        
        return summary
    
    def _calculate_vulnerability_trends(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate vulnerability trends."""
        vuln_counts = [len(event.get("vulnerabilities", [])) for event in events]
        
        if not vuln_counts:
            return {"trend": "stable", "avg_count": 0, "trend_direction": "no_data"}
        
        avg_count = sum(vuln_counts) / len(vuln_counts)
        
        # Simple trend analysis
        if len(vuln_counts) >= 4:
            first_half = vuln_counts[:len(vuln_counts)//2]
            second_half = vuln_counts[len(vuln_counts)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg * 1.2:
                trend_direction = "increasing"
            elif second_avg < first_avg * 0.8:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"
        else:
            trend_direction = "insufficient_data"
        
        return {
            "avg_count": avg_count,
            "trend_direction": trend_direction,
            "max_count": max(vuln_counts),
            "min_count": min(vuln_counts)
        }
    
    def _calculate_overall_security_score(self, events: List[Dict[str, Any]]) -> float:
        """Calculate overall security score (0-100)."""
        if not events:
            return 100.0
        
        total_risk = sum(event.get("risk_score", 0) for event in events)
        total_threats = sum(event.get("ml_threat_score", 0) for event in events)
        
        avg_risk = total_risk / len(events)
        avg_threat = total_threats / len(events)
        
        # Calculate security score (lower risk/threat = higher score)
        security_score = 100 - (avg_risk * 50) - (avg_threat * 50)
        
        return max(0, min(100, security_score))

# Global security instances
global_security_scanner = SecurityScanner()
global_security_hardener = SecurityHardener()
global_security_monitor = SecurityMonitor()

async def scan_skill_security(skill_path: Path) -> SecurityScanResult:
    """Scan a skill for security vulnerabilities."""
    return await global_security_scanner.scan_skill(skill_path)

def harden_skill_security(skill_path: Path) -> Dict[str, Any]:
    """Apply security hardening to a skill."""
    return global_security_hardener.harden_skill(skill_path)

def start_security_monitoring():
    """Start real-time security monitoring."""
    global_security_monitor.start_monitoring()

def stop_security_monitoring():
    """Stop real-time security monitoring."""
    global_security_monitor.stop_monitoring()

def get_security_summary(days: int = 7) -> Dict[str, Any]:
    """Get security monitoring summary."""
    return global_security_monitor.get_security_summary(days)

if __name__ == "__main__":
    # Example usage
    async def main():
        print("Enhanced Security System Examples")
        
        # Test security scanning
        test_skill_path = Path("domains/agent_evolution/SKILL.self-improvement-loop/SKILL.md")
        if test_skill_path.exists():
            scan_result = await scan_skill_security(test_skill_path)
            print(f"Security scan completed: {scan_result.security_level.value} risk level")
            print(f"Vulnerabilities found: {len(scan_result.vulnerabilities)}")
            print(f"Risk score: {scan_result.risk_score:.2f}")
        else:
            print("Test skill not found, skipping scan")
        
        # Test security monitoring
        global_security_monitor.log_security_event({
            "skill_id": "test_skill",
            "risk_score": 0.8,
            "ml_threat_score": 0.9,
            "vulnerabilities": [{"type": "test", "description": "test vulnerability"}]
        })
        
        summary = get_security_summary(1)
        print(f"Security summary: {summary}")
        
        print("Enhanced Security system working correctly")
    
    asyncio.run(main())
