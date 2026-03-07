#!/usr/bin/env python3
"""
Phase 3 Advanced Features Test Suite

This script tests all the advanced features implemented in Phase 3,
including ML-based analytics, enhanced security scanning, and advanced
performance monitoring capabilities.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import os

# Set environment variables for local testing
os.environ["REGISTRY_FILE"] = str(Path(__file__).parent.parent / "skill_registry.json")

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.advanced_analytics import (
    analyze_skill_performance, generate_skill_recommendations,
    get_anomaly_summary, get_performance_insights,
    PerformancePredictor, AnomalyDetector, SkillRecommender
)
from src.core.enhanced_security import (
    scan_skill_security, harden_skill_security,
    start_security_monitoring, stop_security_monitoring,
    get_security_summary, SecurityScanner, SecurityHardener
)
from src.core.performance_monitoring import (
    record_performance_metric, get_skill_performance_stats,
    generate_performance_report, MetricType
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase3AdvancedTester:
    """Comprehensive tester for Phase 3 advanced features."""
    
    def __init__(self):
        self.test_results = []
        self.test_skill_path = Path("domains/agent_evolution/SKILL.self-improvement-loop/SKILL.md")
        
    async def run_all_tests(self):
        """Run all Phase 3 advanced feature tests."""
        logger.info("Starting Phase 3 Advanced Features Test Suite")
        
        # Test 1: Advanced Analytics - ML Performance Prediction
        await self.test_ml_performance_prediction()
        
        # Test 2: Advanced Analytics - Anomaly Detection
        await self.test_anomaly_detection()
        
        # Test 3: Advanced Analytics - Skill Recommendations
        await self.test_intelligent_recommendations()
        
        # Test 4: Enhanced Security - Vulnerability Scanning
        await self.test_vulnerability_scanning()
        
        # Test 5: Enhanced Security - Compliance Checking
        await self.test_compliance_checking()
        
        # Test 6: Enhanced Security - Automated Hardening
        await self.test_security_hardening()
        
        # Test 7: Enhanced Security - Real-time Monitoring
        await self.test_security_monitoring()
        
        # Test 8: Integration - ML + Security + Performance
        await self.test_advanced_integration()
        
        # Test 9: Performance - Large-scale Analytics
        await self.test_large_scale_analytics()
        
        # Generate test report
        self.generate_test_report()
        
        logger.info("Phase 3 Advanced Features Test Suite Completed")
    
    async def test_ml_performance_prediction(self):
        """Test ML-based performance prediction."""
        logger.info("Testing ML Performance Prediction...")
        
        try:
            # Test with sample metrics
            metrics = {
                "execution_time": 2.5,
                "success_rate": 0.95,
                "quality_score": 0.85,
                "resource_usage": 0.6
            }
            
            # Analyze performance
            analysis = await analyze_skill_performance("test_skill_ml", metrics)
            
            self._record_test_result("ML Performance Prediction - Basic", 
                                   analysis.get("predictions") is not None)
            
            # Test prediction generation
            if analysis.get("predictions"):
                prediction = analysis["predictions"][0]
                self._record_test_result("ML Performance Prediction - Prediction Generated", 
                                       hasattr(prediction, 'predicted_value'))
                self._record_test_result("ML Performance Prediction - Confidence Interval", 
                                       hasattr(prediction, 'confidence_interval'))
            
            # Test with multiple data points for training
            for i in range(60):  # Generate enough data for ML training
                test_metrics = {
                    "execution_time": 2.0 + (i * 0.1),
                    "success_rate": 0.9 + (i * 0.001),
                    "quality_score": 0.8 + (i * 0.005),
                    "resource_usage": 0.5 + (i * 0.01)
                }
                await analyze_skill_performance("test_skill_ml", test_metrics)
            
            # Test prediction after training
            final_analysis = await analyze_skill_performance("test_skill_ml", metrics)
            self._record_test_result("ML Performance Prediction - After Training", 
                                   len(final_analysis.get("predictions", [])) > 0)
            
        except Exception as e:
            logger.error(f"ML Performance Prediction test failed: {e}")
            self._record_test_result("ML Performance Prediction - Error", False, str(e))
    
    async def test_anomaly_detection(self):
        """Test advanced anomaly detection."""
        logger.info("Testing Anomaly Detection...")
        
        try:
            # Create anomaly detector
            detector = AnomalyDetector()
            
            # Generate baseline data
            for i in range(50):
                baseline_metrics = {
                    "execution_time": 2.0 + (i * 0.01),
                    "success_rate": 0.95,
                    "quality_score": 0.85,
                    "resource_usage": 0.6
                }
                detector.update_baseline("test_skill_anomaly", baseline_metrics)
            
            # Test normal metrics (should not trigger anomalies)
            normal_metrics = {
                "execution_time": 2.5,
                "success_rate": 0.95,
                "quality_score": 0.85,
                "resource_usage": 0.6
            }
            
            anomalies = detector.detect_anomalies("test_skill_anomaly", normal_metrics)
            self._record_test_result("Anomaly Detection - Normal Metrics", len(anomalies) == 0)
            
            # Test anomalous metrics (should trigger anomalies)
            anomalous_metrics = {
                "execution_time": 10.0,  # Much higher than baseline
                "success_rate": 0.5,     # Much lower than baseline
                "quality_score": 0.3,    # Much lower than baseline
                "resource_usage": 0.9    # Much higher than baseline
            }
            
            anomalies = detector.detect_anomalies("test_skill_anomaly", anomalous_metrics)
            self._record_test_result("Anomaly Detection - Anomalous Metrics", len(anomalies) > 0)
            
            # Test anomaly details
            if anomalies:
                anomaly = anomalies[0]
                self._record_test_result("Anomaly Detection - Anomaly Type", 
                                       hasattr(anomaly, 'anomaly_type'))
                self._record_test_result("Anomaly Detection - Severity", 
                                       hasattr(anomaly, 'severity'))
                self._record_test_result("Anomaly Detection - Suggested Actions", 
                                       hasattr(anomaly, 'suggested_actions'))
            
        except Exception as e:
            logger.error(f"Anomaly Detection test failed: {e}")
            self._record_test_result("Anomaly Detection - Error", False, str(e))
    
    async def test_intelligent_recommendations(self):
        """Test intelligent skill recommendations."""
        logger.info("Testing Intelligent Recommendations...")
        
        try:
            # Create skill recommender
            recommender = SkillRecommender()
            
            # Update skill profiles with test data
            for skill_id in ["skill_ai", "skill_security", "skill_performance"]:
                for i in range(20):
                    metrics = {
                        "execution_time": 2.0 + (i * 0.1),
                        "quality_score": 0.8 + (i * 0.01)
                    }
                    context = {
                        "time_of_day": i % 24,
                        "day_of_week": i % 7,
                        "user_type": "developer" if i % 2 == 0 else "analyst"
                    }
                    recommender.update_skill_profile(skill_id, metrics, context)
            
            # Test skill recommendations
            recommendations = await generate_skill_recommendations(
                "Research AI security best practices",
                {"user_type": "developer", "time_of_day": 14},
                ["skill_ai", "skill_security", "skill_performance"]
            )
            
            self._record_test_result("Intelligent Recommendations - Basic", 
                                   len(recommendations) > 0)
            
            # Test recommendation details
            if recommendations:
                rec = recommendations[0]
                self._record_test_result("Intelligent Recommendations - Confidence Score", 
                                       hasattr(rec, 'confidence_score'))
                self._record_test_result("Intelligent Recommendations - Actions", 
                                       hasattr(rec, 'actions'))
                self._record_test_result("Intelligent Recommendations - Expected Impact", 
                                       hasattr(rec, 'expected_impact'))
            
            # Test context matching
            context_specific_recommendations = await generate_skill_recommendations(
                "Performance optimization for web applications",
                {"user_type": "developer", "application_type": "web"},
                ["skill_performance", "skill_security", "skill_ai"]
            )
            
            self._record_test_result("Intelligent Recommendations - Context Matching", 
                                   len(context_specific_recommendations) > 0)
            
        except Exception as e:
            logger.error(f"Intelligent Recommendations test failed: {e}")
            self._record_test_result("Intelligent Recommendations - Error", False, str(e))
    
    async def test_vulnerability_scanning(self):
        """Test enhanced vulnerability scanning."""
        logger.info("Testing Vulnerability Scanning...")
        
        try:
            # Test with existing skill file
            if self.test_skill_path.exists():
                scan_result = await scan_skill_security(self.test_skill_path)
                
                self._record_test_result("Vulnerability Scanning - Basic Scan", 
                                       scan_result is not None)
                self._record_test_result("Vulnerability Scanning - Security Level", 
                                       hasattr(scan_result, 'security_level'))
                self._record_test_result("Vulnerability Scanning - Risk Score", 
                                       hasattr(scan_result, 'risk_score'))
                
                # Test vulnerability detection
                if scan_result.vulnerabilities:
                    vuln = scan_result.vulnerabilities[0]
                    self._record_test_result("Vulnerability Scanning - Vulnerability Details", 
                                           all(key in vuln for key in ['type', 'description', 'severity']))
                
                # Test compliance checking
                if scan_result.compliance_issues:
                    issue = scan_result.compliance_issues[0]
                    self._record_test_result("Vulnerability Scanning - Compliance Issues", 
                                           all(key in issue for key in ['framework', 'requirement', 'description']))
                
            else:
                logger.warning("Test skill file not found, creating test content")
                
                # Create test skill with vulnerabilities
                test_skill_content = '''
# Test Skill with Security Issues

## Purpose
Test skill for security scanning

## Description
This skill contains various security vulnerabilities for testing purposes.

## Workflow
1. Read user input: input("Enter password: ")
2. Execute command: os.system("echo " + user_input)
3. Store secrets: password = "secret123"
4. Use weak crypto: import hashlib; hash_value = hashlib.md5(data.encode()).hexdigest()
5. SQL injection: cursor.execute("SELECT * FROM users WHERE id = " + user_id)

## Constraints
None
'''
                
                test_skill_path = Path("test_vulnerable_skill.md")
                with open(test_skill_path, 'w') as f:
                    f.write(test_skill_content)
                
                # Scan the test skill
                scan_result = await scan_skill_security(test_skill_path)
                
                self._record_test_result("Vulnerability Scanning - Test File Scan", 
                                       scan_result is not None)
                
                # Should detect vulnerabilities
                self._record_test_result("Vulnerability Scanning - Vulnerabilities Detected", 
                                       len(scan_result.vulnerabilities) > 0)
                
                # Clean up
                test_skill_path.unlink()
            
        except Exception as e:
            logger.error(f"Vulnerability Scanning test failed: {e}")
            self._record_test_result("Vulnerability Scanning - Error", False, str(e))
    
    async def test_compliance_checking(self):
        """Test compliance framework checking."""
        logger.info("Testing Compliance Checking...")
        
        try:
            # Create test content with compliance violations
            test_content = '''
# Test Skill with Compliance Issues

## Purpose
Test compliance checking

## Description
This skill contains compliance violations for testing.

## Workflow
1. Log sensitive data: logger.info("Password: " + password)
2. Use weak cryptography: hashlib.md5(data.encode())
3. Unvalidated input: input("Enter data: ")
4. Hardcoded secrets: api_key = "secret123"

## Constraints
None
'''
            
            test_skill_path = Path("test_compliance_skill.md")
            with open(test_skill_path, 'w') as f:
                f.write(test_content)
            
            # Scan for compliance issues
            scan_result = await scan_skill_security(test_skill_path)
            
            self._record_test_result("Compliance Checking - SOC2 Violations", 
                                   any(issue.get("framework") == "SOC2" for issue in scan_result.compliance_issues))
            
            self._record_test_result("Compliance Checking - ISO27001 Violations", 
                                   any(issue.get("framework") == "ISO27001" for issue in scan_result.compliance_issues))
            
            self._record_test_result("Compliance Checking - NIST Violations", 
                                   any(issue.get("framework") == "NIST" for issue in scan_result.compliance_issues))
            
            # Clean up
            test_skill_path.unlink()
            
        except Exception as e:
            logger.error(f"Compliance Checking test failed: {e}")
            self._record_test_result("Compliance Checking - Error", False, str(e))
    
    async def test_security_hardening(self):
        """Test automated security hardening."""
        logger.info("Testing Security Hardening...")
        
        try:
            # Create test content with security issues
            vulnerable_content = '''
# Test Skill with Security Issues

## Purpose
Test security hardening

## Description
This skill contains security issues that should be hardened.

## Workflow
1. Hardcoded password: password = "secret123"
2. Hardcoded API key: api_key = "apikey123"
3. Unsafe eval: eval(user_input)
4. Weak crypto: hashlib.md5(data.encode())
5. Weak random: random.randint(1, 100)

## Constraints
None
'''
            
            test_skill_path = Path("test_hardening_skill.md")
            with open(test_skill_path, 'w') as f:
                f.write(vulnerable_content)
            
            # Apply security hardening
            hardening_result = harden_skill_security(test_skill_path)
            
            self._record_test_result("Security Hardening - Basic", 
                                   hardening_result.get("success", False))
            
            self._record_test_result("Security Hardening - Rules Applied", 
                                   len(hardening_result.get("applied_rules", [])) > 0)
            
            # Read hardened content
            with open(test_skill_path, 'r') as f:
                hardened_content = f.read()
            
            # Check if hardening was applied
            self._record_test_result("Security Hardening - Password Replaced", 
                                   "os.environ.get" in hardened_content)
            
            self._record_test_result("Security Hardening - API Key Replaced", 
                                   "os.environ.get" in hardened_content)
            
            self._record_test_result("Security Hardening - Eval Replaced", 
                                   "ast.literal_eval" in hardened_content)
            
            # Clean up
            test_skill_path.unlink()
            backup_path = Path("test_hardening_skill.md.backup")
            if backup_path.exists():
                backup_path.unlink()
            
        except Exception as e:
            logger.error(f"Security Hardening test failed: {e}")
            self._record_test_result("Security Hardening - Error", False, str(e))
    
    async def test_security_monitoring(self):
        """Test real-time security monitoring."""
        logger.info("Testing Security Monitoring...")
        
        try:
            # Start monitoring
            start_security_monitoring()
            
            # Log security events
            from src.core.enhanced_security import global_security_monitor
            
            # Log normal event
            global_security_monitor.log_security_event({
                "skill_id": "normal_skill",
                "risk_score": 0.2,
                "ml_threat_score": 0.1,
                "vulnerabilities": []
            })
            
            # Log high-risk event
            global_security_monitor.log_security_event({
                "skill_id": "risky_skill",
                "risk_score": 0.9,
                "ml_threat_score": 0.8,
                "vulnerabilities": [
                    {"type": "sql_injection", "description": "SQL injection vulnerability"},
                    {"type": "hardcoded_secret", "description": "Hardcoded secret detected"}
                ]
            })
            
            # Get security summary
            summary = get_security_summary(1)
            
            self._record_test_result("Security Monitoring - Event Logging", 
                                   summary.get("total_events", 0) >= 2)
            
            self._record_test_result("Security Monitoring - High Risk Detection", 
                                   summary.get("high_risk_events", 0) > 0)
            
            self._record_test_result("Security Monitoring - Critical Threats", 
                                   summary.get("critical_threats", 0) > 0)
            
            # Test vulnerability trends
            if "vulnerability_trends" in summary:
                trends = summary["vulnerability_trends"]
                self._record_test_result("Security Monitoring - Vulnerability Trends", 
                                       "avg_count" in trends)
                self._record_test_result("Security Monitoring - Trend Direction", 
                                       "trend_direction" in trends)
            
            # Stop monitoring
            stop_security_monitoring()
            
        except Exception as e:
            logger.error(f"Security Monitoring test failed: {e}")
            self._record_test_result("Security Monitoring - Error", False, str(e))
    
    async def test_advanced_integration(self):
        """Test integration of ML, security, and performance features."""
        logger.info("Testing Advanced Integration...")
        
        try:
            # Create a comprehensive test scenario
            skill_id = "integrated_test_skill"
            
            # Generate performance data
            for i in range(100):
                metrics = {
                    "execution_time": 2.0 + (i * 0.05),
                    "success_rate": 0.9 + (i * 0.001),
                    "quality_score": 0.8 + (i * 0.005),
                    "resource_usage": 0.5 + (i * 0.01)
                }
                
                # Record performance metric
                record_performance_metric(
                    skill_id,
                    MetricType.EXECUTION_TIME,
                    metrics["execution_time"],
                    {"iteration": i},
                    "autogen"
                )
                
                # Analyze with ML
                await analyze_skill_performance(skill_id, metrics)
            
            # Get performance insights
            insights = await get_performance_insights(skill_id, 1)
            
            self._record_test_result("Advanced Integration - Performance Insights", 
                                   insights.get("basic_stats") is not None)
            
            self._record_test_result("Advanced Integration - Trend Analysis", 
                                   insights.get("trends") is not None)
            
            self._record_test_result("Advanced Integration - Performance Ranking", 
                                   insights.get("performance_ranking") is not None)
            
            # Generate skill recommendations
            recommendations = await generate_skill_recommendations(
                "Optimize performance and security for AI applications",
                {"user_type": "developer", "domain": "ai"},
                [skill_id, "skill_security", "skill_performance"]
            )
            
            self._record_test_result("Advanced Integration - Cross-Feature Recommendations", 
                                   len(recommendations) > 0)
            
            # Get performance report
            report = generate_performance_report(1)
            
            self._record_test_result("Advanced Integration - Comprehensive Reporting", 
                                   report is not None)
            
        except Exception as e:
            logger.error(f"Advanced Integration test failed: {e}")
            self._record_test_result("Advanced Integration - Error", False, str(e))
    
    async def test_large_scale_analytics(self):
        """Test analytics performance with large-scale data."""
        logger.info("Testing Large-Scale Analytics...")
        
        try:
            # Test with multiple skills
            skills = [f"skill_{i}" for i in range(50)]
            
            # Generate large dataset
            start_time = time.time()
            
            for skill_id in skills:
                for i in range(100):  # 100 data points per skill
                    metrics = {
                        "execution_time": 2.0 + (i * 0.01),
                        "success_rate": 0.9 + (i * 0.001),
                        "quality_score": 0.8 + (i * 0.005),
                        "resource_usage": 0.5 + (i * 0.01)
                    }
                    
                    # Record metrics
                    record_performance_metric(
                        skill_id,
                        MetricType.EXECUTION_TIME,
                        metrics["execution_time"],
                        {"batch": i // 10},
                        "autogen"
                    )
                    
                    # ML analysis
                    await analyze_skill_performance(skill_id, metrics)
            
            generation_time = time.time() - start_time
            
            # Test analytics performance
            start_time = time.time()
            
            # Get insights for all skills
            for skill_id in skills:
                insights = await get_performance_insights(skill_id, 1)
            
            analytics_time = time.time() - start_time
            
            # Test anomaly detection on large dataset
            detector = AnomalyDetector()
            
            start_time = time.time()
            for skill_id in skills:
                for i in range(10):
                    metrics = {
                        "execution_time": 2.0 + (i * 0.1),
                        "success_rate": 0.9,
                        "quality_score": 0.8,
                        "resource_usage": 0.6
                    }
                    detector.update_baseline(skill_id, metrics)
            
            anomaly_time = time.time() - start_time
            
            # Record performance results
            self._record_test_result("Large-Scale Analytics - Data Generation", 
                                   generation_time < 30.0,  # Should complete in under 30 seconds
                                   f"Generation took {generation_time:.2f}s")
            
            self._record_test_result("Large-Scale Analytics - Analytics Processing", 
                                   analytics_time < 10.0,  # Should process quickly
                                   f"Analytics took {analytics_time:.2f}s")
            
            self._record_test_result("Large-Scale Analytics - Anomaly Detection", 
                                   anomaly_time < 5.0,  # Should be fast
                                   f"Anomaly detection took {anomaly_time:.2f}s")
            
            logger.info(f"Large-scale test completed: Generation={generation_time:.2f}s, "
                       f"Analytics={analytics_time:.2f}s, Anomaly={anomaly_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Large-Scale Analytics test failed: {e}")
            self._record_test_result("Large-Scale Analytics - Error", False, str(e))
    
    def _record_test_result(self, test_name: str, success: bool, error_message: str = None):
        """Record a test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "error_message": error_message,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        status = "PASS" if success else "FAIL"
        logger.info(f"Test '{test_name}': {status}")
        if error_message:
            logger.error(f"  Error: {error_message}")
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        logger.info("\n" + "="*60)
        logger.info("PHASE 3 ADVANCED FEATURES TEST REPORT")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        # Group tests by category
        categories = {
            "ML Performance Prediction": [],
            "Anomaly Detection": [],
            "Intelligent Recommendations": [],
            "Vulnerability Scanning": [],
            "Compliance Checking": [],
            "Security Hardening": [],
            "Security Monitoring": [],
            "Advanced Integration": [],
            "Large-Scale Analytics": []
        }
        
        for result in self.test_results:
            for category in categories:
                if category.lower().replace(" ", "_") in result["test_name"].lower():
                    categories[category].append(result)
                    break
        
        logger.info("\nCategory-wise Results:")
        logger.info("-" * 40)
        
        for category, tests in categories.items():
            if tests:
                category_passed = sum(1 for t in tests if t["success"])
                category_total = len(tests)
                logger.info(f"{category}: {category_passed}/{category_total} ({(category_passed/category_total)*100:.1f}%)")
        
        logger.info("\nDetailed Results:")
        logger.info("-" * 40)
        
        for result in self.test_results:
            status = "✓ PASS" if result["success"] else "✗ FAIL"
            logger.info(f"{status} {result['test_name']}")
            if result["error_message"]:
                logger.info(f"     Error: {result['error_message']}")
        
        # Save report to file
        report_data = {
            "timestamp": time.time(),
            "phase": "Phase 3 - Advanced Features",
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            "categories": {k: {"passed": sum(1 for t in v if t["success"]), "total": len(v)} 
                          for k, v in categories.items() if v},
            "test_results": self.test_results
        }
        
        report_file = Path("phase3_test_report.json")
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"\nDetailed report saved to: {report_file}")
        
        # Return success status
        return failed_tests == 0

async def main():
    """Main test execution."""
    logger.info("Phase 3 Advanced Features Test Suite Starting...")
    
    tester = Phase3AdvancedTester()
    success = await tester.run_all_tests()
    
    if success:
        logger.info("🎉 All Phase 3 tests passed! Advanced features are working correctly.")
        logger.info("Phase 3 implementation is complete and validated.")
        sys.exit(0)
    else:
        logger.error("❌ Some Phase 3 tests failed. Please check the implementation.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())