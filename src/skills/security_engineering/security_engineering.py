#!/usr/bin/env python3
"""
Security Engineering Skill Module
Provides comprehensive security engineering capabilities including threat modeling,
vulnerability assessment, secure coding practices, cryptography, and security analysis.

This skill handles security architecture, risk assessment, penetration testing,
security compliance, and defensive security measures for software systems.
"""

import os
import re
import json
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging
import hashlib
import secrets
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityEngineeringSkill:
    """Security Engineering skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Security Engineering skill.
        
        Args:
            config: Configuration dictionary with security settings
        """
        self.config = config or {}
        self.threat_models = ['stride', 'dread', 'pasta', 'octave']
        self.vulnerability_types = [
            'sql_injection', 'xss', 'csrf', 'injection', 'broken_auth',
            'sensitive_data_exposure', 'xml_external_entities',
            'broken_access_control', 'security_misconfiguration',
            'insufficient_logging_monitoring'
        ]
        self.cryptography_algorithms = [
            'aes', 'rsa', 'ecdsa', 'sha256', 'bcrypt', 'argon2'
        ]
        self.compliance_frameworks = [
            'owasp', 'nist', 'iso27001', 'soc2', 'pci_dss', 'gdpr'
        ]
        
    def perform_threat_modeling(self, system_description: str, 
                              modeling_approach: str = "stride") -> Dict[str, Any]:
        """
        Perform threat modeling for a system.
        
        Args:
            system_description: Description of the system to model
            modeling_approach: Threat modeling methodology (stride, dread, pasta, etc.)
        
        Returns:
            Dictionary containing threat model analysis
        """
        try:
            # Analyze system components
            system_analysis = self._analyze_system_components(system_description)
            
            # Generate threat model based on approach
            if modeling_approach.lower() == "stride":
                threat_model = self._generate_stride_model(system_analysis)
            elif modeling_approach.lower() == "dread":
                threat_model = self._generate_dread_model(system_analysis)
            elif modeling_approach.lower() == "pasta":
                threat_model = self._generate_pasta_model(system_analysis)
            else:
                return {"error": f"Unsupported threat modeling approach: {modeling_approach}"}
            
            # Generate mitigation strategies
            mitigations = self._generate_mitigation_strategies(threat_model)
            
            return {
                "status": "success",
                "system_description": system_description,
                "modeling_approach": modeling_approach,
                "system_analysis": system_analysis,
                "threat_model": threat_model,
                "mitigations": mitigations,
                "risk_assessment": self._assess_risk(threat_model)
            }
            
        except Exception as e:
            return {"error": f"Failed to perform threat modeling: {str(e)}"}
    
    def conduct_vulnerability_assessment(self, codebase_path: str,
                                       assessment_type: str = "static") -> Dict[str, Any]:
        """
        Conduct vulnerability assessment of a codebase.
        
        Args:
            codebase_path: Path to the codebase to assess
            assessment_type: Type of assessment (static, dynamic, manual)
        
        Returns:
            Dictionary containing vulnerability assessment results
        """
        try:
            codebase_dir = Path(codebase_path)
            if not codebase_dir.exists():
                return {"error": f"Codebase path does not exist: {codebase_path}"}
            
            # Analyze codebase structure
            codebase_analysis = self._analyze_codebase_structure(codebase_dir)
            
            # Perform vulnerability scanning
            if assessment_type == "static":
                vulnerabilities = self._perform_static_analysis(codebase_dir)
            elif assessment_type == "dynamic":
                vulnerabilities = self._perform_dynamic_analysis(codebase_dir)
            else:
                vulnerabilities = self._perform_manual_analysis(codebase_dir)
            
            # Generate security recommendations
            recommendations = self._generate_security_recommendations(vulnerabilities)
            
            return {
                "status": "success",
                "codebase_path": str(codebase_dir),
                "assessment_type": assessment_type,
                "codebase_analysis": codebase_analysis,
                "vulnerabilities": vulnerabilities,
                "recommendations": recommendations,
                "severity_summary": self._summarize_vulnerability_severity(vulnerabilities)
            }
            
        except Exception as e:
            return {"error": f"Failed to conduct vulnerability assessment: {str(e)}"}
    
    def implement_secure_coding_practices(self, language: str = "python",
                                        framework: str = "django") -> Dict[str, Any]:
        """
        Implement secure coding practices for a specific language/framework.
        
        Args:
            language: Programming language (python, java, javascript, etc.)
            framework: Framework (django, spring, react, etc.)
        
        Returns:
            Dictionary containing secure coding implementation
        """
        try:
            # Generate secure coding guidelines
            guidelines = self._generate_secure_coding_guidelines(language, framework)
            
            # Generate secure code templates
            templates = self._generate_secure_code_templates(language, framework)
            
            # Generate security checks
            security_checks = self._generate_security_checks(language, framework)
            
            return {
                "status": "success",
                "language": language,
                "framework": framework,
                "guidelines": guidelines,
                "templates": templates,
                "security_checks": security_checks,
                "best_practices": self._get_security_best_practices(language, framework)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement secure coding practices: {str(e)}"}
    
    def implement_cryptography_solution(self, algorithm: str = "aes",
                                      key_size: int = 256,
                                      use_case: str = "data_encryption") -> Dict[str, Any]:
        """
        Implement cryptographic solution for specific use case.
        
        Args:
            algorithm: Cryptographic algorithm (aes, rsa, ecdsa, etc.)
            key_size: Key size in bits
            use_case: Use case (data_encryption, digital_signatures, hashing, etc.)
        
        Returns:
            Dictionary containing cryptographic implementation
        """
        try:
            # Generate cryptographic implementation
            if algorithm.lower() == "aes" and use_case == "data_encryption":
                crypto_files = self._implement_aes_encryption(key_size)
            elif algorithm.lower() == "rsa" and use_case == "digital_signatures":
                crypto_files = self._implement_rsa_signatures(key_size)
            elif algorithm.lower() == "bcrypt" and use_case == "password_hashing":
                crypto_files = self._implement_password_hashing()
            else:
                return {"error": f"Unsupported algorithm/use case combination: {algorithm}/{use_case}"}
            
            return {
                "status": "success",
                "algorithm": algorithm,
                "key_size": key_size,
                "use_case": use_case,
                "files": crypto_files,
                "security_analysis": self._analyze_crypto_security(algorithm, key_size, use_case)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement cryptography solution: {str(e)}"}
    
    def perform_security_audit(self, system_path: str,
                             audit_scope: List[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive security audit of a system.
        
        Args:
            system_path: Path to the system to audit
            audit_scope: Scope of audit (authentication, authorization, data_protection, etc.)
        
        Returns:
            Dictionary containing security audit results
        """
        try:
            system_dir = Path(system_path)
            if not system_dir.exists():
                return {"error": f"System path does not exist: {system_path}"}
            
            if audit_scope is None:
                audit_scope = ["authentication", "authorization", "data_protection", 
                             "input_validation", "logging_monitoring"]
            
            # Perform security checks based on scope
            audit_results = {}
            for scope in audit_scope:
                if scope == "authentication":
                    audit_results[scope] = self._audit_authentication(system_dir)
                elif scope == "authorization":
                    audit_results[scope] = self._audit_authorization(system_dir)
                elif scope == "data_protection":
                    audit_results[scope] = self._audit_data_protection(system_dir)
                elif scope == "input_validation":
                    audit_results[scope] = self._audit_input_validation(system_dir)
                elif scope == "logging_monitoring":
                    audit_results[scope] = self._audit_logging_monitoring(system_dir)
            
            # Generate compliance report
            compliance_report = self._generate_compliance_report(audit_results, audit_scope)
            
            return {
                "status": "success",
                "system_path": str(system_dir),
                "audit_scope": audit_scope,
                "audit_results": audit_results,
                "compliance_report": compliance_report,
                "security_score": self._calculate_security_score(audit_results)
            }
            
        except Exception as e:
            return {"error": f"Failed to perform security audit: {str(e)}"}
    
    def _analyze_system_components(self, system_description: str) -> Dict[str, Any]:
        """Analyze system components for threat modeling."""
        components = {
            "data_flows": [],
            "trust_boundaries": [],
            "assets": [],
            "entry_points": [],
            "external_dependencies": []
        }
        
        # Parse system description for components
        description_lower = system_description.lower()
        
        if "database" in description_lower:
            components["data_flows"].append("Database access")
            components["assets"].append("Database")
        
        if "api" in description_lower or "web service" in description_lower:
            components["entry_points"].append("API endpoints")
            components["external_dependencies"].append("API clients")
        
        if "authentication" in description_lower:
            components["trust_boundaries"].append("Authentication boundary")
        
        if "user input" in description_lower:
            components["entry_points"].append("User input")
        
        return components
    
    def _generate_stride_model(self, system_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate STRIDE threat model."""
        stride_threats = {
            "spoofing": [],
            "tampering": [],
            "repudiation": [],
            "information_disclosure": [],
            "denial_of_service": [],
            "elevation_of_privilege": []
        }
        
        # Generate threats based on system components
        if "API endpoints" in system_analysis["entry_points"]:
            stride_threats["spoofing"].append("API endpoint spoofing")
            stride_threats["tampering"].append("API request tampering")
            stride_threats["information_disclosure"].append("API data exposure")
        
        if "Database access" in system_analysis["data_flows"]:
            stride_threats["tampering"].append("Database tampering")
            stride_threats["information_disclosure"].append("Database data exposure")
            stride_threats["elevation_of_privilege"].append("Database privilege escalation")
        
        if "User input" in system_analysis["entry_points"]:
            stride_threats["tampering"].append("Input data tampering")
            stride_threats["denial_of_service"].append("Input-based DoS")
        
        return stride_threats
    
    def _generate_dread_model(self, system_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate DREAD threat model."""
        dread_threats = []
        
        # Generate threats with DREAD scoring
        base_threats = [
            {
                "threat": "SQL Injection",
                "damage": 8, "reproducibility": 9, "exploitability": 7,
                "affected_users": 9, "discoverability": 6
            },
            {
                "threat": "Cross-Site Scripting",
                "damage": 6, "reproducibility": 8, "exploitability": 8,
                "affected_users": 7, "discoverability": 7
            },
            {
                "threat": "Authentication Bypass",
                "damage": 9, "reproducibility": 6, "exploitability": 5,
                "affected_users": 10, "discoverability": 4
            }
        ]
        
        for threat in base_threats:
            threat["risk_score"] = self._calculate_dread_score(threat)
            dread_threats.append(threat)
        
        return {"threats": dread_threats}
    
    def _generate_pasta_model(self, system_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PASTA threat model."""
        pasta_model = {
            "stage_1": {"business_objectives": [], "technical_objectives": []},
            "stage_2": {"data_flows": system_analysis["data_flows"]},
            "stage_3": {"security_requirements": []},
            "stage_4": {"threat_scenarios": []},
            "stage_5": {"vulnerability_analysis": []},
            "stage_6": {"attack_scenarios": []},
            "stage_7": {"risk_assessment": []}
        }
        
        # Populate PASTA stages
        pasta_model["stage_1"]["business_objectives"] = ["Data protection", "System availability"]
        pasta_model["stage_3"]["security_requirements"] = ["Authentication", "Authorization", "Encryption"]
        pasta_model["stage_4"]["threat_scenarios"] = ["Unauthorized access", "Data theft", "Service disruption"]
        
        return pasta_model
    
    def _calculate_dread_score(self, threat: Dict[str, int]) -> int:
        """Calculate DREAD risk score."""
        return (threat["damage"] + threat["reproducibility"] + threat["exploitability"] + 
                threat["affected_users"] + threat["discoverability"]) // 5
    
    def _generate_mitigation_strategies(self, threat_model: Dict[str, Any]) -> List[str]:
        """Generate mitigation strategies for identified threats."""
        mitigations = []
        
        if isinstance(threat_model, dict):
            for category, threats in threat_model.items():
                if category == "spoofing":
                    mitigations.extend([
                        "Implement strong authentication",
                        "Use multi-factor authentication",
                        "Validate digital certificates"
                    ])
                elif category == "tampering":
                    mitigations.extend([
                        "Use data integrity checks",
                        "Implement digital signatures",
                        "Use secure communication protocols"
                    ])
                elif category == "information_disclosure":
                    mitigations.extend([
                        "Implement encryption",
                        "Use access controls",
                        "Mask sensitive data"
                    ])
        
        return list(set(mitigations))  # Remove duplicates
    
    def _assess_risk(self, threat_model: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk from threat model."""
        risk_levels = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }
        
        # Count threats by severity
        if isinstance(threat_model, dict):
            for category, threats in threat_model.items():
                if isinstance(threats, list):
                    for threat in threats:
                        if isinstance(threat, dict) and "risk_score" in threat:
                            score = threat["risk_score"]
                            if score >= 8:
                                risk_levels["critical"] += 1
                            elif score >= 6:
                                risk_levels["high"] += 1
                            elif score >= 4:
                                risk_levels["medium"] += 1
                            else:
                                risk_levels["low"] += 1
        
        return {
            "risk_levels": risk_levels,
            "overall_risk": self._determine_overall_risk(risk_levels),
            "risk_treatment": self._recommend_risk_treatment(risk_levels)
        }
    
    def _determine_overall_risk(self, risk_levels: Dict[str, int]) -> str:
        """Determine overall risk level."""
        if risk_levels["critical"] > 0:
            return "critical"
        elif risk_levels["high"] > 2:
            return "high"
        elif risk_levels["medium"] > 5:
            return "medium"
        else:
            return "low"
    
    def _recommend_risk_treatment(self, risk_levels: Dict[str, int]) -> List[str]:
        """Recommend risk treatment strategies."""
        treatments = []
        
        if risk_levels["critical"] > 0:
            treatments.append("Immediate risk mitigation required")
        if risk_levels["high"] > 0:
            treatments.append("Implement compensating controls")
        if risk_levels["medium"] > 0:
            treatments.append("Schedule risk reduction activities")
        if risk_levels["low"] > 0:
            treatments.append("Monitor and review periodically")
        
        return treatments
    
    def _analyze_codebase_structure(self, codebase_dir: Path) -> Dict[str, Any]:
        """Analyze codebase structure for vulnerability assessment."""
        structure = {
            "file_types": [],
            "directories": [],
            "sensitive_files": [],
            "configuration_files": []
        }
        
        for item in codebase_dir.rglob("*"):
            if item.is_file():
                file_ext = item.suffix.lower()
                if file_ext not in structure["file_types"]:
                    structure["file_types"].append(file_ext)
                
                if any(keyword in item.name.lower() for keyword in 
                      ["config", "secret", "key", "password", "credential"]):
                    structure["sensitive_files"].append(str(item))
                
                if any(keyword in item.name.lower() for keyword in 
                      ["config", "settings", "env", "properties"]):
                    structure["configuration_files"].append(str(item))
        
        for item in codebase_dir.iterdir():
            if item.is_dir():
                structure["directories"].append(str(item))
        
        return structure
    
    def _perform_static_analysis(self, codebase_dir: Path) -> List[Dict[str, Any]]:
        """Perform static code analysis for vulnerabilities."""
        vulnerabilities = []
        
        # Check for common vulnerability patterns
        vulnerability_patterns = {
            "sql_injection": [
                r"execute\s*\(\s*['\"]\s*SELECT.*\+.*['\"]",
                r"cursor\.execute\s*\(\s*.*\+.*\)",
                r"query\s*=\s*.*\+.*"
            ],
            "xss": [
                r"innerHTML\s*=\s*.*",
                r"document\.write\s*\(\s*.*\)",
                r"eval\s*\(\s*.*\)"
            ],
            "hardcoded_secrets": [
                r"password\s*=\s*['\"][^'\"]{8,}['\"]",
                r"api[_-]?key\s*=\s*['\"][^'\"]{10,}['\"]",
                r"secret\s*=\s*['\"][^'\"]{10,}['\"]"
            ]
        }
        
        for file_path in codebase_dir.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    line_number = 1
                    
                    for line in content.split('\n'):
                        for vuln_type, patterns in vulnerability_patterns.items():
                            for pattern in patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    vulnerabilities.append({
                                        "file": str(file_path),
                                        "line": line_number,
                                        "type": vuln_type,
                                        "severity": self._get_vulnerability_severity(vuln_type),
                                        "description": f"Potential {vuln_type} vulnerability",
                                        "code": line.strip()
                                    })
                        line_number += 1
            except Exception as e:
                logger.warning(f"Could not analyze file {file_path}: {e}")
        
        return vulnerabilities
    
    def _perform_dynamic_analysis(self, codebase_dir: Path) -> List[Dict[str, Any]]:
        """Perform dynamic analysis (placeholder for runtime analysis)."""
        # This would typically involve running the application and testing
        return [
            {
                "type": "placeholder",
                "description": "Dynamic analysis requires running application",
                "severity": "info",
                "recommendation": "Implement runtime security testing"
            }
        ]
    
    def _perform_manual_analysis(self, codebase_dir: Path) -> List[Dict[str, Any]]:
        """Perform manual security analysis."""
        return [
            {
                "type": "architecture_review",
                "description": "Review system architecture for security flaws",
                "severity": "medium",
                "recommendation": "Implement defense in depth"
            }
        ]
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type."""
        severity_map = {
            "sql_injection": "critical",
            "xss": "high",
            "csrf": "medium",
            "hardcoded_secrets": "high",
            "injection": "critical"
        }
        return severity_map.get(vuln_type, "medium")
    
    def _generate_security_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on vulnerabilities."""
        recommendations = []
        
        critical_vulns = [v for v in vulnerabilities if v.get("severity") == "critical"]
        high_vulns = [v for v in vulnerabilities if v.get("severity") == "high"]
        
        if critical_vulns:
            recommendations.append("Address critical vulnerabilities immediately")
        if high_vulns:
            recommendations.append("Implement security controls for high-risk issues")
        
        vuln_types = set(v.get("type") for v in vulnerabilities)
        if "sql_injection" in vuln_types:
            recommendations.append("Implement parameterized queries and input validation")
        if "xss" in vuln_types:
            recommendations.append("Implement output encoding and content security policy")
        if "hardcoded_secrets" in vuln_types:
            recommendations.append("Use secure secret management solutions")
        
        return recommendations
    
    def _summarize_vulnerability_severity(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Summarize vulnerability severity distribution."""
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "medium")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        return severity_counts
    
    def _generate_secure_coding_guidelines(self, language: str, framework: str) -> Dict[str, List[str]]:
        """Generate secure coding guidelines for language/framework."""
        guidelines = {
            "input_validation": [],
            "authentication": [],
            "authorization": [],
            "data_protection": [],
            "error_handling": []
        }
        
        if language == "python":
            guidelines["input_validation"].extend([
                "Use type hints and validate all inputs",
                "Implement proper input sanitization",
                "Use libraries like pydantic for validation"
            ])
            guidelines["authentication"].extend([
                "Use bcrypt or Argon2 for password hashing",
                "Implement proper session management",
                "Use secure random number generation"
            ])
        
        if framework == "django":
            guidelines["data_protection"].extend([
                "Use Django's built-in CSRF protection",
                "Implement proper database security",
                "Use Django's ORM to prevent SQL injection"
            ])
        
        return guidelines
    
    def _generate_secure_code_templates(self, language: str, framework: str) -> Dict[str, str]:
        """Generate secure code templates."""
        templates = {}
        
        if language == "python":
            templates["secure_input_validation"] = """
def validate_user_input(user_input: str) -> str:
    \"\"\"Secure input validation function.\"\"\"
    import re
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>&"\'\\]', '', user_input)
    
    # Limit input length
    if len(sanitized) > 100:
        raise ValueError("Input too long")
    
    return sanitized.strip()

def secure_password_hash(password: str) -> str:
    \"\"\"Secure password hashing using bcrypt.\"\"\"
    import bcrypt
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')
"""
        
        if framework == "django":
            templates["secure_view"] = """
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@login_required
@csrf_protect
@require_http_methods(["POST"])
def secure_api_view(request):
    \"\"\"Secure API view with proper authentication and CSRF protection.\"\"\"
    try:
        # Validate input
        data = request.POST
        user_input = data.get('input', '')
        
        if not user_input:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        
        # Process request securely
        result = process_user_data(user_input)
        
        return JsonResponse({'result': result})
        
    except Exception as e:
        logger.error(f"Error in secure_api_view: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
"""
        
        return templates
    
    def _generate_security_checks(self, language: str, framework: str) -> List[str]:
        """Generate security checklist for language/framework."""
        checks = [
            "Input validation implemented",
            "Output encoding applied",
            "Authentication mechanisms in place",
            "Authorization controls implemented",
            "Error handling does not leak information",
            "Logging and monitoring implemented",
            "Dependencies are up to date",
            "Configuration is secure"
        ]
        
        if language == "python":
            checks.extend([
                "Use secure random number generation",
                "Implement proper exception handling",
                "Avoid using eval() and exec()",
                "Use secure libraries and frameworks"
            ])
        
        if framework == "django":
            checks.extend([
                "CSRF protection enabled",
                "Security middleware configured",
                "Debug mode disabled in production",
                "Database security implemented"
            ])
        
        return checks
    
    def _get_security_best_practices(self, language: str, framework: str) -> List[str]:
        """Get security best practices for language/framework."""
        practices = [
            "Follow the principle of least privilege",
            "Implement defense in depth",
            "Use secure coding standards",
            "Regular security testing and auditing",
            "Keep dependencies updated",
            "Implement proper logging and monitoring",
            "Use secure configuration management",
            "Train developers on security practices"
        ]
        
        return practices
    
    def _implement_aes_encryption(self, key_size: int) -> Dict[str, str]:
        """Implement AES encryption solution."""
        aes_content = f"""import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AESEncryption:
    \"\"\"AES encryption implementation with secure key management.\"\"\"
    
    def __init__(self, key_size: int = {key_size}):
        self.key_size = key_size
        self.backend = default_backend()
    
    def generate_key(self) -> bytes:
        \"\"\"Generate a secure random key.\"\"\"
        return os.urandom(self.key_size // 8)
    
    def encrypt(self, plaintext: str, key: bytes) -> str:
        \"\"\"Encrypt plaintext using AES.\"\"\"
        # Generate random IV
        iv = os.urandom(16)
        
        # Pad plaintext to 16-byte boundary
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8'))
        padded_data += padder.finalize()
        
        # Create cipher and encrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return base64 encoded IV + ciphertext
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    
    def decrypt(self, encrypted_data: str, key: bytes) -> str:
        \"\"\"Decrypt AES encrypted data.\"\"\"
        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Extract IV and ciphertext
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]
        
        # Create cipher and decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext)
        plaintext += unpadder.finalize()
        
        return plaintext.decode('utf-8')

# Example usage
if __name__ == "__main__":
    aes = AESEncryption({key_size})
    key = aes.generate_key()
    
    # Encrypt data
    plaintext = "Sensitive data to encrypt"
    encrypted = aes.encrypt(plaintext, key)
    print(f"Encrypted: {{encrypted}}")
    
    # Decrypt data
    decrypted = aes.decrypt(encrypted, key)
    print(f"Decrypted: {{decrypted}}")
"""
        
        return {"aes_encryption.py": aes_content}
    
    def _implement_rsa_signatures(self, key_size: int) -> Dict[str, str]:
        """Implement RSA digital signatures."""
        rsa_content = f"""from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import base64

class RSASignature:
    \"\"\"RSA digital signature implementation.\"\"\"
    
    def __init__(self, key_size: int = {key_size}):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        \"\"\"Generate RSA key pair.\"\"\"
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )
        self.public_key = self.private_key.public_key()
    
    def sign_message(self, message: str) -> str:
        \"\"\"Sign a message using private key.\"\"\"
        if not self.private_key:
            raise ValueError("Private key not generated")
        
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, message: str, signature: str) -> bool:
        \"\"\"Verify signature using public key.\"\"\"
        if not self.public_key:
            raise ValueError("Public key not available")
        
        try:
            self.public_key.verify(
                base64.b64decode(signature.encode('utf-8')),
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
    
    def export_public_key(self) -> str:
        \"\"\"Export public key in PEM format.\"\"\"
        if not self.public_key:
            raise ValueError("Public key not generated")
        
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def import_public_key(self, pem_key: str):
        \"\"\"Import public key from PEM format.\"\"\"
        self.public_key = serialization.load_pem_public_key(
            pem_key.encode('utf-8')
        )

# Example usage
if __name__ == "__main__":
    rsa_sig = RSASignature({key_size})
    rsa_sig.generate_keys()
    
    # Sign message
    message = "This is a test message"
    signature = rsa_sig.sign_message(message)
    print(f"Signature: {{signature}}")
    
    # Verify signature
    is_valid = rsa_sig.verify_signature(message, signature)
    print(f"Signature valid: {{is_valid}}")
"""
        
        return {"rsa_signatures.py": rsa_content}
    
    def _implement_password_hashing(self) -> Dict[str, str]:
        """Implement secure password hashing."""
        bcrypt_content = """import bcrypt
import secrets
import string
from typing import Optional

class PasswordManager:
    \"\"\"Secure password hashing and verification.\"\"\"
    
    def __init__(self, rounds: int = 12):
        self.rounds = rounds
    
    def hash_password(self, password: str) -> str:
        \"\"\"Hash password using bcrypt.\"\"\"
        # Convert to bytes and hash
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        \"\"\"Verify password against hash.\"\"\"
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    def generate_secure_password(self, length: int = 16) -> str:
        \"\"\"Generate a secure random password.\"\"\"
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        # Ensure password meets complexity requirements
        while not self._meets_complexity(password):
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        return password
    
    def _meets_complexity(self, password: str) -> bool:
        \"\"\"Check if password meets complexity requirements.\"\"\"
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)
        
        return all([has_upper, has_lower, has_digit, has_special])

# Example usage
if __name__ == "__main__":
    pm = PasswordManager()
    
    # Hash password
    password = "MySecurePassword123!"
    hashed = pm.hash_password(password)
    print(f"Hashed: {{hashed}}")
    
    # Verify password
    is_valid = pm.verify_password(password, hashed)
    print(f"Password valid: {{is_valid}}")
    
    # Generate secure password
    new_password = pm.generate_secure_password()
    print(f"Generated password: {{new_password}}")
"""
        
        return {"password_hashing.py": bcrypt_content}
    
    def _analyze_crypto_security(self, algorithm: str, key_size: int, use_case: str) -> Dict[str, Any]:
        """Analyze cryptographic security."""
        security_analysis = {
            "algorithm_security": "unknown",
            "key_security": "unknown",
            "implementation_security": "unknown",
            "recommendations": []
        }
        
        if algorithm.lower() == "aes":
            security_analysis.update({
                "algorithm_security": "high",
                "key_security": "high" if key_size >= 256 else "medium",
                "implementation_security": "high",
                "recommendations": [
                    "Use AES-256 for maximum security",
                    "Implement proper key management",
                    "Use secure random IVs",
                    "Consider authenticated encryption modes"
                ]
            })
        
        elif algorithm.lower() == "rsa":
            security_analysis.update({
                "algorithm_security": "high",
                "key_security": "high" if key_size >= 2048 else "medium",
                "implementation_security": "medium",
                "recommendations": [
                    "Use RSA-2048 or higher",
                    "Implement proper padding schemes",
                    "Use secure random number generation",
                    "Consider elliptic curve alternatives"
                ]
            })
        
        return security_analysis
    
    def _audit_authentication(self, system_dir: Path) -> Dict[str, Any]:
        """Audit authentication mechanisms."""
        audit_results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check for authentication-related files
        auth_files = list(system_dir.rglob("*auth*")) + list(system_dir.rglob("*login*"))
        
        if not auth_files:
            audit_results["issues"].append("No authentication mechanisms found")
            audit_results["status"] = "fail"
        else:
            audit_results["status"] = "pass"
            audit_results["recommendations"].append("Review authentication implementation")
        
        return audit_results
    
    def _audit_authorization(self, system_dir: Path) -> Dict[str, Any]:
        """Audit authorization mechanisms."""
        audit_results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check for authorization-related files
        authz_files = list(system_dir.rglob("*permission*")) + list(system_dir.rglob("*role*"))
        
        if not authz_files:
            audit_results["issues"].append("No authorization mechanisms found")
            audit_results["status"] = "fail"
        else:
            audit_results["status"] = "pass"
            audit_results["recommendations"].append("Review authorization implementation")
        
        return audit_results
    
    def _audit_data_protection(self, system_dir: Path) -> Dict[str, Any]:
        """Audit data protection mechanisms."""
        audit_results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check for encryption and data protection
        encryption_files = list(system_dir.rglob("*encrypt*")) + list(system_dir.rglob("*crypto*"))
        
        if not encryption_files:
            audit_results["issues"].append("No encryption mechanisms found")
            audit_results["status"] = "fail"
        else:
            audit_results["status"] = "pass"
            audit_results["recommendations"].append("Review encryption implementation")
        
        return audit_results
    
    def _audit_input_validation(self, system_dir: Path) -> Dict[str, Any]:
        """Audit input validation mechanisms."""
        audit_results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check for input validation patterns
        validation_issues = []
        
        for py_file in system_dir.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                    # Check for unsafe input handling
                    if "eval(" in content or "exec(" in content:
                        validation_issues.append(f"Unsafe code execution in {py_file}")
                    
                    if "input(" in content and "validate" not in content:
                        validation_issues.append(f"Unvalidated input in {py_file}")
                        
            except:
                pass
        
        if validation_issues:
            audit_results["issues"] = validation_issues
            audit_results["status"] = "fail"
        else:
            audit_results["status"] = "pass"
            audit_results["recommendations"].append("Continue implementing input validation")
        
        return audit_results
    
    def _audit_logging_monitoring(self, system_dir: Path) -> Dict[str, Any]:
        """Audit logging and monitoring mechanisms."""
        audit_results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check for logging implementation
        logging_files = list(system_dir.rglob("*log*")) + list(system_dir.rglob("*monitor*"))
        
        if not logging_files:
            audit_results["issues"].append("No logging mechanisms found")
            audit_results["status"] = "fail"
        else:
            audit_results["status"] = "pass"
            audit_results["recommendations"].append("Review logging implementation")
        
        return audit_results
    
    def _generate_compliance_report(self, audit_results: Dict[str, Any], 
                                  audit_scope: List[str]) -> Dict[str, Any]:
        """Generate compliance report."""
        compliance_report = {
            "frameworks": {},
            "overall_compliance": "unknown",
            "compliance_score": 0
        }
        
        # Calculate compliance score
        total_checks = len(audit_scope)
        passed_checks = sum(1 for result in audit_results.values() 
                          if result.get("status") == "pass")
        
        compliance_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # Generate framework-specific compliance
        for framework in self.compliance_frameworks:
            compliance_report["frameworks"][framework] = {
                "compliance_score": compliance_score,
                "requirements_met": passed_checks,
                "total_requirements": total_checks,
                "status": "compliant" if compliance_score >= 80 else "non-compliant"
            }
        
        compliance_report["overall_compliance"] = "compliant" if compliance_score >= 80 else "non-compliant"
        compliance_report["compliance_score"] = compliance_score
        
        return compliance_report
    
    def _calculate_security_score(self, audit_results: Dict[str, Any]) -> int:
        """Calculate overall security score."""
        total_score = 0
        max_score = len(audit_results) * 100
        
        for result in audit_results.values():
            if result.get("status") == "pass":
                total_score += 100
            elif result.get("status") == "fail":
                total_score += 0
            else:
                total_score += 50  # Partial score for unknown
        
        return int((total_score / max_score) * 100) if max_score > 0 else 0


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "security_engineering",
        "description": "Provides comprehensive security engineering capabilities",
        "version": "1.0.0",
        "domain": "security_engineering",
        "functions": [
            {
                "name": "perform_threat_modeling",
                "description": "Perform threat modeling for systems using various methodologies"
            },
            {
                "name": "conduct_vulnerability_assessment",
                "description": "Conduct vulnerability assessment of codebases and systems"
            },
            {
                "name": "implement_secure_coding_practices",
                "description": "Implement secure coding practices for specific languages/frameworks"
            },
            {
                "name": "implement_cryptography_solution",
                "description": "Implement cryptographic solutions for various use cases"
            },
            {
                "name": "perform_security_audit",
                "description": "Perform comprehensive security audits of systems"
            }
        ]
    }

def execute_function(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a function from this skill.
    
    Args:
        function_name: Name of the function to execute
        arguments: Arguments for the function
    
    Returns:
        Function execution result
    """
    skill = SecurityEngineeringSkill()
    
    if function_name == "perform_threat_modeling":
        system_description = arguments.get("system_description")
        modeling_approach = arguments.get("modeling_approach", "stride")
        return skill.perform_threat_modeling(system_description, modeling_approach)
    elif function_name == "conduct_vulnerability_assessment":
        codebase_path = arguments.get("codebase_path")
        assessment_type = arguments.get("assessment_type", "static")
        return skill.conduct_vulnerability_assessment(codebase_path, assessment_type)
    elif function_name == "implement_secure_coding_practices":
        language = arguments.get("language", "python")
        framework = arguments.get("framework", "django")
        return skill.implement_secure_coding_practices(language, framework)
    elif function_name == "implement_cryptography_solution":
        algorithm = arguments.get("algorithm", "aes")
        key_size = arguments.get("key_size", 256)
        use_case = arguments.get("use_case", "data_encryption")
        return skill.implement_cryptography_solution(algorithm, key_size, use_case)
    elif function_name == "perform_security_audit":
        system_path = arguments.get("system_path")
        audit_scope = arguments.get("audit_scope", [])
        return skill.perform_security_audit(system_path, audit_scope)
    else:
        return {"error": f"Unknown function: {function_name}"}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP-compatible invoke function for the Security Engineering skill.
    
    Args:
        payload: Dictionary containing function name and arguments
    
    Returns:
        Function execution result
    """
    function_name = payload.get("function_name")
    arguments = payload.get("arguments", {})
    
    return execute_function(function_name, arguments)

if __name__ == "__main__":
    # Test the skill
    skill = SecurityEngineeringSkill()
    
    print("Testing Security Engineering Skill...")
    
    # Test threat modeling
    system_desc = "Web application with user authentication, database access, and API endpoints"
    result = skill.perform_threat_modeling(system_desc, "stride")
    print(f"Threat modeling result: {result}")
    
    # Test cryptography implementation
    result = skill.implement_cryptography_solution("aes", 256, "data_encryption")
    print(f"Cryptography implementation result: {result}")
