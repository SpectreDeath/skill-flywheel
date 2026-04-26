#!/usr/bin/env python3
"""
Behavioral Orchestrator

Wraps skill invocations with Karpathy-inspired behavioral guidelines:
- Think Before Coding (explicit assumptions)
- Simplicity First (minimal complexity)
- Surgical Changes (focused modifications)
- Goal-Driven Execution (verifiable criteria)
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime

from flywheel.behavioral.constraints import (
    SimplicityConstraint,
    AssumptionsConstraint,
    SurgicalConstraint,
    GoalsConstraint
)
from flywheel.quality.auditor import QualityAuditor

logger = logging.getLogger(__name__)


class BehavioralOrchestrator:
    """
    Orchestrates skill execution with behavioral quality checks.
    
    Applies cross-cutting behavioral constraints across all surfaces
    (Prolog, Hy, Python) without modifying the core skill logic.
    """
    
    def __init__(self, skill_manager=None):
        self.skill_manager = skill_manager
        self.auditor = QualityAuditor()
        
        # Initialize constraint checkers
        self.constraints = {
            "simplicity": SimplicityConstraint(),
            "assumptions": AssumptionsConstraint(),
            "surgical": SurgicalConstraint(),
            "goals": GoalsConstraint(),
        }
    
    def invoke(
        self,
        skill_name: str,
        payload: Dict[str, Any],
        surfaces: Optional[Dict[str, Any]] = None,
        profile: str = "karpathy_balanced",
        original_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a skill with behavioral guidelines enforced.
        
        Args:
            skill_name: Name of the skill to invoke
            payload: Input parameters for the skill
            surfaces: Optional pre-loaded surfaces (prolog, hy, python)
            profile: Behavioral profile (karpathy_strict, balanced, minimal, etc.)
            original_context: Original code/file context for surgical checks
            
        Returns:
            Dict containing:
                - result: The skill's output
                - quality_report: Behavioral compliance assessment
                - metadata: Execution details
        """
        from flywheel.behavioral.profiles import get_profile
        
        profile_obj = get_profile(profile)
        profile_config = profile_obj.to_dict()
        logger.info(f"Executing '{skill_name}' with behavioral profile: {profile}")
        
        # Load skill and surfaces
        if self.skill_manager:
            skill_module = self._load_skill(skill_name)
            if surfaces is None:
                surfaces = self._load_surfaces(skill_module)
        else:
            # Direct invocation (surfaces passed in)
            skill_module = None
        
        # === PRE-EXECUTION: Behavioral Pre-Checks ===
        pre_results = self._run_pre_checks(payload, profile_config, surfaces)
        
        if not pre_results["passed"]:
            return self._build_failed_result(
                skill_name, "pre-execution", pre_results
            )
        
        # === EXECUTION: Run Skill ===
        result = self._execute_skill(skill_name, skill_module, payload, surfaces)
        
        # === POST-EXECUTION: Behavioral Validation ===
        post_results = self._run_post_checks(
            result, payload, original_context, profile_config
        )
        
        # === COMPILE QUALITY REPORT ===
        quality_report = self._compile_quality_report(
            pre_results, post_results, profile_config
        )
        
        return {
            "result": result,
            "quality_report": quality_report,
            "metadata": {
                "skill": skill_name,
                "profile": profile,
                "timestamp": datetime.now().isoformat(),
                "behavioral_gates_passed": quality_report["checks_passed"],
                "behavioral_gates_total": quality_report["checks_total"],
            },
        }
    
    def _load_skill(self, skill_name: str):
        """Load skill from manager"""
        if skill_name not in self.skill_manager.skills:
            raise ValueError(f"Skill not found: {skill_name}")
        return self.skill_manager.skills[skill_name]
    
    def _load_surfaces(self, skill_module):
        """Detect and load surface files from skill module"""
        import inspect
        from pathlib import Path
        
        surfaces = {}
        
        if hasattr(skill_module, "PROLOG_SURFACE"):
            surfaces["prolog"] = skill_module.PROLOG_SURFACE
        
        if hasattr(skill_module, "HY_SURFACE"):
            surfaces["hy"] = skill_module.HY_SURFACE
        
        return surfaces
    
    def _run_pre_checks(self, payload, profile, surfaces):
        """Run behavioral pre-execution checks"""
        results = {"passed": True, "checks": {}}
        
        if "simplicity" in profile["constraints"]:
            check = self.constraints["simplicity"].pre_check(payload, profile)
            results["checks"]["simplicity"] = check
            results["passed"] = results["passed"] and check.passed
        
        if "assumptions" in profile["constraints"]:
            check = self.constraints["assumptions"].pre_check(payload)
            results["checks"]["assumptions"] = check
            results["passed"] = results["passed"] and check.passed
        
        return results
    
    def _execute_skill(self, skill_name, skill_module, payload, surfaces):
        """Execute the actual skill"""
        logger.debug(f"Executing skill: {skill_name}")
        
        if self.skill_manager:
            if hasattr(skill_module, "invoke"):
                import asyncio
                result = asyncio.run(skill_module.invoke(payload))
            else:
                func_name = skill_name.replace("-", "_")
                if hasattr(skill_module, func_name):
                    func = getattr(skill_module, func_name)
                    import inspect
                    sig = inspect.signature(func)
                    if "surfaces" in sig.parameters:
                        result = func(payload, surfaces)
                    else:
                        result = func(payload)
                else:
                    result = {"error": f"No invocable function found in {skill_name}"}
        else:
            result = {"error": "No skill manager provided"}
        
        return result
    
    def _run_post_checks(self, result, payload, original_context, profile):
        """Run behavioral post-execution checks"""
        results = {"passed": True, "checks": {}}
        
        if "simplicity" in profile["constraints"]:
            check = self.constraints["simplicity"].post_check(result, payload)
            results["checks"]["simplicity"] = check
            results["passed"] = results["passed"] and check.passed
        
        if "surgical" in profile["constraints"] and original_context:
            check = self.constraints["surgical"].validate(
                original_context, result, payload
            )
            results["checks"]["surgical"] = check
            results["passed"] = results["passed"] and check.passed
        
        if "goals" in profile["constraints"]:
            criteria = payload.get("success_criteria", [])
            check = self.constraints["goals"].verify(result, criteria)
            results["checks"]["goals"] = check
            results["passed"] = results["passed"] and check.passed
        
        return results
    
    def _compile_quality_report(self, pre_results, post_results, profile):
        """Compile overall quality report."""
        all_checks = {**pre_results["checks"], **post_results["checks"]}
        
        # Convert dataclass objects to dicts for compatibility
        dict_checks = {}
        for name, check in all_checks.items():
            if hasattr(check, '__dict__'):
                dict_checks[name] = vars(check)
            elif isinstance(check, dict):
                dict_checks[name] = check
            else:
                dict_checks[name] = {
                    "passed": getattr(check, "passed", False),
                    "violation": getattr(check, "violation", ""),
                    "severity": getattr(check, "severity", "warning"),
                    "suggestion": getattr(check, "suggestion", ""),
                }
        
        checks_passed = sum(
            1 for check in dict_checks.values() if check.get("passed", False)
        )
        checks_total = len(dict_checks)
        
        from flywheel.quality.reporter import QualityReporter
        reporter = QualityReporter()
        
        overall_score = reporter.calculate_overall_score(dict_checks)
        
        return {
            "overall_score": overall_score,
            "grade": reporter.get_grade(overall_score),
            "passed": all(
                check.get("passed", False) for check in dict_checks.values()
            ),
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "profile": profile["name"],
            "checks": dict_checks,
            "recommendations": reporter.generate_recommendations(dict_checks, overall_score),
        }
    
    def _build_failed_result(self, skill_name, stage, pre_results):
        """Build result for failed pre-execution checks"""
        return {
            "result": {
                "error": "Behavioral pre-checks failed",
                "stage": stage,
                "skill": skill_name,
                "details": pre_results,
            },
            "quality_report": {
                "overall_score": 0,
                "grade": "F",
                "passed": False,
                "checks_passed": 0,
                "checks_total": len(pre_results.get("checks", {})),
                "checks": pre_results.get("checks", {}),
            },
            "metadata": {
                "skill": skill_name,
                "timestamp": datetime.now().isoformat(),
            },
        }