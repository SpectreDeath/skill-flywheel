"""Celery tasks for skill evolution."""

import logging
import uuid
from typing import Any, Dict, List, Optional

from celery import Celery
from flywheel.evolution.config import EvolutionConfig
from flywheel.evolution.evaluator import SkillFitnessEvaluator
from flywheel.evolution.evolver import SkillEvolver
from flywheel.evolution.genome import SkillGenome
from flywheel.evolution.mutator import LLMMutator
from flywheel.server.config import ServerConfig

logger = logging.getLogger(__name__)

config = ServerConfig()

celery_app = Celery(
    "flywheel_evolution",
    broker=config.config["celery"]["broker_url"],
    backend=config.config["celery"]["result_backend"],
)

celery_app.conf.update(
    task_serializer=config.config["celery"]["task_serializer"],
    result_serializer=config.config["celery"]["result_serializer"],
    accept_content=config.config["celery"]["accept_content"],
    timezone=config.config["celery"]["timezone"],
    enable_utc=config.config["celery"]["enable_utc"],
)


class EvolutionJobStatus:
    """Track evolution job status for WebSocket updates."""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = "pending"
        self.current_generation = 0
        self.total_generations = 0
        self.best_fitness = 0.0
        self.population_size = 0
        self.progress = 0.0
        self.errors: List[str] = []
        self.results: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "current_generation": self.current_generation,
            "total_generations": self.total_generations,
            "best_fitness": self.best_fitness,
            "population_size": self.population_size,
            "progress": self.progress,
            "errors": self.errors,
            "results": self.results,
        }


_active_jobs: Dict[str, EvolutionJobStatus] = {}


def get_job_status(job_id: str) -> Optional[EvolutionJobStatus]:
    """Get job status by ID."""
    return _active_jobs.get(job_id)


@celery_app.task(bind=True)
def run_evolution_generation(self, job_id: str, config_dict: Dict[str, Any]):
    """Run a single evolution generation."""
    status = get_job_status(job_id)
    if not status:
        return {"error": "Job not found"}

    try:
        status.status = "running"

        # This is a simplified version - actual implementation would
        # use the SkillEvolver to run generations
        status.current_generation += 1
        status.progress = status.current_generation / max(status.total_generations, 1)
        status.best_fitness = status.current_generation * 0.1  # Placeholder

        return status.to_dict()

    except Exception as e:
        logger.error(f"Evolution generation failed: {e}")
        status.errors.append(str(e))
        status.status = "failed"
        return status.to_dict()


@celery_app.task(bind=True)
def run_full_evolution(
    self,
    job_id: str,
    initial_genome_data: Dict[str, Any],
    config_dict: Dict[str, Any],
    max_generations: int = 10,
):
    """Run full evolution loop."""
    status = get_job_status(job_id)
    if not status:
        return {"error": "Job not found"}

    try:
        status.status = "running"
        status.total_generations = max_generations

        # Initialize genome using Pydantic model_validate
        initial_genome = SkillGenome.model_validate(initial_genome_data)

        # Placeholder for actual evolution
        # In production, this would use SkillEvolver
        for gen in range(max_generations):
            status.current_generation = gen + 1
            status.progress = status.current_generation / max_generations
            status.best_fitness = (gen + 1) * 0.1

            # Simulate work
            import time

            time.sleep(0.1)

        status.status = "completed"
        status.results = {
            "best_fitness": status.best_fitness,
            "generations": max_generations,
            "final_genome": initial_genome.model_dump(),
        }

        return status.to_dict()

    except Exception as e:
        logger.error(f"Evolution failed: {e}")
        status.errors.append(str(e))
        status.status = "failed"
        return status.to_dict()


def start_evolution_job(
    initial_genome_data: Dict[str, Any],
    config_dict: Optional[Dict[str, Any]] = None,
    max_generations: int = 10,
) -> str:
    """Start a new evolution job."""
    job_id = str(uuid.uuid4())
    status = EvolutionJobStatus(job_id)
    status.total_generations = max_generations
    status.population_size = (
        config_dict.get("population_size", 20) if config_dict else 20
    )
    _active_jobs[job_id] = status

    # Queue the task
    run_full_evolution.apply_async(
        args=[job_id, initial_genome_data, config_dict or {}, max_generations],
        task_id=job_id,
    )

    return job_id
