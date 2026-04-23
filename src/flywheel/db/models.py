"""SQLAlchemy models for Skill Flywheel."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Skill(Base):
    """Skill model."""

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    domain: Mapped[str] = mapped_column(String(100), nullable=False, default="general")
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    purpose: Mapped[Optional[str]] = mapped_column(Text)
    instructions: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SkillVersion(Base):
    """Skill version history."""

    __tablename__ = "skill_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    instructions: Mapped[Optional[str]] = mapped_column(Text)
    fitness_score: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EvolutionJob(Base):
    """Evolution job tracking."""

if __name__ == "__main__":
    __tablename__ = "evolution_jobs"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        job_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
        status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
        current_generation: Mapped[int] = mapped_column(Integer, default=0)
        total_generations: Mapped[int] = mapped_column(Integer, default=0)
        best_fitness: Mapped[float] = mapped_column(Float, default=0.0)
        error_message: Mapped[Optional[str]] = mapped_column(Text)
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
        completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)