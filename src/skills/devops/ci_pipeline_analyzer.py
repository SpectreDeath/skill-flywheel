"""
CI Pipeline Analyzer

Analyzes CI/CD pipelines to identify stages, parallelization opportunities,
bottlenecks, and optimization suggestions.

Supports: GitHub Actions, GitLab CI, Jenkins
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class PipelineStage:
    name: str
    type: str
    jobs: List[str] = field(default_factory=list)
    estimated_time: int = 0
    dependencies: List[str] = field(default_factory=list)
    is_parallel: bool = False


@dataclass
class JobInfo:
    name: str
    stage: str
    needs: List[str] = field(default_factory=list)
    runs_on: str = ""
    script: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    cache: bool = False
    timeout: int = 360


CI_PROVIDERS = ["github", "gitlab", "jenkins"]


def detect_provider(config: str) -> Optional[str]:
    """Detect CI provider from config content."""
    config_lower = config.lower()

    if "github" in config_lower or ".github" in config_lower:
        return "github"
    elif "gitlab" in config_lower or "script:" in config_lower:
        return "gitlab"
    elif "jenkinsfile" in config_lower or "pipeline {" in config_lower:
        return "jenkins"

    if "on:" in config or "jobs:" in config:
        return "github"
    elif "stages:" in config:
        return "gitlab"
    elif "agent {" in config or "stages {" in config:
        return "jenkins"

    return None


def parse_github_actions(config: str) -> Dict[str, Any]:
    """Parse GitHub Actions workflow YAML."""
    try:
        workflow = yaml.safe_load(config)
    except yaml.YAMLError:
        return {"error": "Invalid YAML format"}

    jobs = {}
    stages = {}

    if not workflow or "jobs" not in workflow:
        return {"error": "No jobs found in GitHub Actions workflow"}

    for job_name, job_config in workflow.get("jobs", {}).items():
        runs_on = job_config.get("runs-on", "unknown")
        needs = job_config.get("needs", [])
        if isinstance(needs, str):
            needs = [needs]

        script = job_config.get("steps", [])
        script_lines = []
        for step in script:
            if isinstance(step, dict) and "run" in step:
                script_lines.append(step["run"])

        cache = any(
            "cache" in str(step).lower() for step in job_config.get("steps", [])
        )

        timeout = job_config.get("timeout-minutes", 60) * 60

        jobs[job_name] = JobInfo(
            name=job_name,
            stage="build"
            if "build" in job_name.lower()
            else "test"
            if "test" in job_name.lower()
            else "deploy"
            if "deploy" in job_name.lower()
            else "unknown",
            needs=needs,
            runs_on=str(runs_on),
            script=script_lines,
            cache=cache,
            timeout=timeout,
        )

    return {"jobs": jobs, "provider": "github"}


def parse_gitlab_ci(config: str) -> Dict[str, Any]:
    """Parse GitLab CI YAML."""
    try:
        pipeline = yaml.safe_load(config)
    except yaml.YAMLError:
        return {"error": "Invalid YAML format"}

    jobs = {}
    stages = []

    stages = pipeline.get("stages", ["build", "test", "deploy"])

    if not isinstance(pipeline, dict):
        return {"error": "Invalid GitLab CI format"}

    for job_name, job_config in pipeline.items():
        if job_name in [
            "stages",
            "variables",
            "image",
            "before_script",
            "after_script",
        ]:
            continue

        if not isinstance(job_config, dict):
            continue

        needs = job_config.get("needs", [])
        if isinstance(needs, str):
            needs = [needs]

        script = job_config.get("script", [])
        if isinstance(script, str):
            script = [script]

        cache = "cache" in job_config

        stage_idx = 0
        job_stage = job_config.get("stage", "test")
        if job_stage in stages:
            stage_idx = stages.index(job_stage)

        timeout = job_config.get("timeout", "1h")
        if isinstance(timeout, str):
            if "h" in timeout:
                timeout = int(timeout.replace("h", "")) * 3600
            elif "m" in timeout:
                timeout = int(timeout.replace("m", "")) * 60
            else:
                timeout = 3600

        jobs[job_name] = JobInfo(
            name=job_name,
            stage=job_stage,
            needs=needs,
            script=script,
            cache=cache,
            timeout=timeout,
        )

    return {"jobs": jobs, "stages": stages, "provider": "gitlab"}


def parse_jenkins(config: str) -> Dict[str, Any]:
    """Parse Jenkinsfile."""
    jobs = {}

    stage_pattern = r"stage\s*['\"](.+?)['\"]\s*\{"
    steps_pattern = r"steps\s*\{([^}]+)\}"

    stages = re.findall(stage_pattern, config)

    stage_blocks = re.split(r"stage\s+", config)

    for i, block in enumerate(stage_blocks[1:], 0):
        stage_name = stages[i] if i < len(stages) else f"stage_{i}"

        steps_match = re.search(steps_pattern, block)
        script_lines = []
        if steps_match:
            steps_content = steps_match.group(1)
            script_lines = [
                line.strip()
                for line in steps_content.split("\n")
                if line.strip() and not line.strip().startswith("//")
            ]

        timeout = 3600

        jobs[stage_name] = JobInfo(
            name=stage_name,
            stage="build"
            if "build" in stage_name.lower()
            else "test"
            if "test" in stage_name.lower()
            else "deploy"
            if "deploy" in stage_name.lower()
            else "unknown",
            script=script_lines,
            timeout=timeout,
        )

    return {"jobs": jobs, "provider": "jenkins"}


def identify_stages(jobs: Dict[str, JobInfo]) -> List[PipelineStage]:
    """Identify pipeline stages from jobs."""
    stage_map = {}

    for job_name, job in jobs.items():
        stage_type = job.stage
        if stage_type not in stage_map:
            stage_map[stage_type] = PipelineStage(
                name=stage_type, type=stage_type, jobs=[], estimated_time=job.timeout
            )
        stage_map[stage_type].jobs.append(job_name)
        stage_map[stage_type].estimated_time = max(
            stage_map[stage_type].estimated_time, job.timeout
        )

    return list(stage_map.values())


def find_parallel_jobs(jobs: Dict[str, JobInfo]) -> List[List[str]]:
    """Find jobs that can run in parallel."""
    parallel_groups = []

    no_deps = [name for name, job in jobs.items() if not job.needs]
    if no_deps:
        parallel_groups.append(no_deps)

    by_stage = {}
    for name, job in jobs.items():
        stage = job.stage
        if stage not in by_stage:
            by_stage[stage] = []
        by_stage[stage].append(name)

    for stage, job_names in by_stage.items():
        deps_in_stage = []
        for name in job_names:
            job = jobs[name]
            for need in job.needs:
                if need in job_names:
                    deps_in_stage.append(name)

        parallel = [n for n in job_names if n not in deps_in_stage]
        if len(parallel) > 1:
            parallel_groups.append(parallel)

    return parallel_groups


def detect_bottlenecks(
    jobs: Dict[str, JobInfo], stages: List[PipelineStage]
) -> List[Dict[str, Any]]:
    """Detect potential bottlenecks in the pipeline."""
    bottlenecks = []

    slow_jobs = sorted(
        [(name, job) for name, job in jobs.items()],
        key=lambda x: x[1].timeout,
        reverse=True,
    )[:3]

    for name, job in slow_jobs:
        if job.timeout > 600:
            bottlenecks.append(
                {
                    "type": "slow_job",
                    "name": name,
                    "estimated_time": job.timeout,
                    "reason": f"Job takes approximately {job.timeout // 60} minutes",
                }
            )

    for stage in stages:
        if len(stage.jobs) > 3:
            bottlenecks.append(
                {
                    "type": "large_stage",
                    "name": stage.name,
                    "job_count": len(stage.jobs),
                    "reason": f"Stage has {len(stage.jobs)} jobs that may benefit from splitting",
                }
            )

    sequential_deps = []
    for name, job in jobs.items():
        if job.needs and len(job.needs) > 2:
            sequential_deps.append(
                {
                    "name": name,
                    "dependencies": job.needs,
                    "reason": "Job has multiple sequential dependencies",
                }
            )

    bottlenecks.extend(sequential_deps)

    no_cache_jobs = [name for name, job in jobs.items() if not job.cache and job.script]
    if len(no_cache_jobs) > 2:
        bottlenecks.append(
            {
                "type": "no_caching",
                "count": len(no_cache_jobs),
                "jobs": no_cache_jobs[:5],
                "reason": f"{len(no_cache_jobs)} jobs don't use caching",
            }
        )

    return bottlenecks


def generate_optimizations(
    jobs: Dict[str, JobInfo],
    stages: List[PipelineStage],
    bottlenecks: List[Dict[str, Any]],
    target_time: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Generate optimization suggestions."""
    optimizations = []

    parallel_groups = find_parallel_jobs(jobs)
    if len(parallel_groups) > 1:
        optimizations.append(
            {
                "type": "parallelization",
                "description": "Run independent jobs in parallel",
                "impact": "high",
                "potential_savings": "30-50%",
                "details": parallel_groups,
            }
        )

    no_cache = [n for n, j in jobs.items() if not j.cache and j.script]
    if no_cache:
        optimizations.append(
            {
                "type": "caching",
                "description": "Enable caching for dependencies and build artifacts",
                "impact": "high",
                "potential_savings": "20-40%",
                "affected_jobs": no_cache[:5],
            }
        )

    if any("npm install" in " ".join(j.script) for j in jobs.values() if j.script):
        optimizations.append(
            {
                "type": "package_manager",
                "description": "Use npm ci instead of npm install for faster, deterministic installs",
                "impact": "medium",
                "potential_savings": "30-60 seconds",
            }
        )

    if any("pip install" in " ".join(j.script) for j in jobs.values() if j.script):
        optimizations.append(
            {
                "type": "python_packages",
                "description": "Use pip cache and --no-deps for faster installations",
                "impact": "medium",
                "potential_savings": "20-40 seconds",
            }
        )

    large_stages = [s for s in stages if len(s.jobs) > 2]
    for stage in large_stages:
        optimizations.append(
            {
                "type": "split_stage",
                "description": f"Split '{stage.name}' stage into smaller stages",
                "impact": "medium",
                "potential_savings": "Parallel execution within stage",
            }
        )

    for b in bottlenecks:
        if b["type"] == "slow_job":
            optimizations.append(
                {
                    "type": "optimize_slow_job",
                    "description": f"Optimize slow job '{b['name']}'",
                    "impact": "high",
                    "potential_savings": f"Reduce {b['estimated_time'] // 60} minutes",
                    "suggestions": [
                        "Add caching for dependencies",
                        "Use incremental builds",
                        "Parallelize test execution",
                        "Reduce unnecessary steps",
                    ],
                }
            )

    optimizations.append(
        {
            "type": "matrix_strategy",
            "description": "Use matrix strategy to run jobs in parallel for different configurations",
            "impact": "medium",
            "potential_savings": "Multiple configs in parallel",
        }
    )

    return optimizations


def calculate_time_savings(
    jobs: Dict[str, JobInfo], optimizations: List[Dict[str, Any]]
) -> Dict[str, int]:
    """Calculate estimated time savings."""
    total_time = sum(job.timeout for job in jobs.values())

    savings = 0

    for opt in optimizations:
        if opt["type"] == "parallelization":
            savings += int(total_time * 0.4)
        elif opt["type"] == "caching":
            savings += int(total_time * 0.25)
        elif opt["type"] == "optimize_slow_job":
            if "potential_savings" in opt:
                match = re.search(r"(\d+)", opt["potential_savings"])
                if match:
                    savings += int(match.group(1)) * 60

    return {
        "current_estimated_time": total_time,
        "potential_savings": savings,
        "optimized_estimated_time": max(0, total_time - savings),
    }


def ci_pipeline_analyzer(config: str, options: dict = None) -> dict:
    """
    Analyze CI/CD pipeline configuration.

    Args:
        config: CI pipeline configuration (YAML format)
        options: Analysis options including:
            - provider: Force specific CI provider (github, gitlab, jenkins)
            - target_time: Target pipeline execution time in seconds

    Returns:
        Analysis results containing stages, parallelization, bottlenecks,
        optimizations, and time savings
    """
    if options is None:
        options = {}

    provider = options.get("provider")
    target_time = options.get("target_time")

    if not config or not config.strip():
        return {"status": "error", "error": "No pipeline configuration provided"}

    if provider is None:
        provider = detect_provider(config)

    if provider is None:
        return {
            "status": "error",
            "error": "Could not detect CI provider. Please specify provider in options.",
        }

    if provider == "github":
        parsed = parse_github_actions(config)
    elif provider == "gitlab":
        parsed = parse_gitlab_ci(config)
    elif provider == "jenkins":
        parsed = parse_jenkins(config)
    else:
        return {"status": "error", "error": f"Unsupported provider: {provider}"}

    if "error" in parsed:
        return {"status": "error", "error": parsed["error"]}

    jobs = parsed.get("jobs", {})

    if not jobs:
        return {"status": "error", "error": "No jobs found in pipeline configuration"}

    stages = identify_stages(jobs)
    parallel_jobs = find_parallel_jobs(jobs)
    bottlenecks = detect_bottlenecks(jobs, stages)
    optimizations = generate_optimizations(jobs, stages, bottlenecks, target_time)
    time_savings = calculate_time_savings(jobs, optimizations)

    return {
        "status": "success",
        "provider": provider,
        "stages": [
            {
                "name": s.name,
                "type": s.type,
                "jobs": s.jobs,
                "estimated_time": s.estimated_time,
            }
            for s in stages
        ],
        "parallel_jobs": parallel_jobs,
        "bottlenecks": bottlenecks,
        "optimizations": optimizations,
        "estimated_time": time_savings,
        "summary": {
            "total_jobs": len(jobs),
            "total_stages": len(stages),
            "parallel_groups": len(parallel_jobs),
            "bottleneck_count": len(bottlenecks),
            "optimization_count": len(optimizations),
        },
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    config = payload.get("config", "")
    options = payload.get("options", {})

    result = ci_pipeline_analyzer(config, options)

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "ci-pipeline-analyzer",
        "description": "Analyze CI/CD pipelines to identify stages, parallelization, bottlenecks, and optimization suggestions",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
