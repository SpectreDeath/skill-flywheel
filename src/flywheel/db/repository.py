"""Repository for skill database operations."""

from typing import List, Optional

from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from flywheel.server.config import ServerConfig
from .models import Base, EvolutionJob, Skill, SkillVersion

config = ServerConfig()


def get_database_url() -> str:
    """Get database URL from config."""
    db_config = config.config.get("database", {})
    db_type = db_config.get("type", "sqlite")

    if db_type == "postgresql":
        return db_config.get(
            "connection_string", "postgresql+asyncpg://localhost:5432/flywheel"
        )

    # Default SQLite
    db_path = db_config.get("path", "data/skill_registry.db")
    return f"sqlite:///{db_path}"


def is_async(db_url: str) -> bool:
    """Check if database is async."""
    return db_url.startswith("postgresql")


class SkillRepository:
    """Repository for skill operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self, domain: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[Skill]:
        """Get all skills."""
        query = select(Skill)
        if domain:
            query = query.where(Skill.domain == domain)
        query = query.limit(limit).offset(offset)
        return list(self.session.execute(query).scalars().all())

    def get_by_name(self, name: str) -> Optional[Skill]:
        """Get skill by name."""
        return self.session.execute(
            select(Skill).where(Skill.name == name)
        ).scalar_one_or_none()

    def create(self, skill: Skill) -> Skill:
        """Create a new skill."""
        self.session.add(skill)
        self.session.commit()
        self.session.refresh(skill)
        return skill

    def update(self, skill: Skill) -> Skill:
        """Update an existing skill."""
        self.session.commit()
        self.session.refresh(skill)
        return skill

    def delete(self, name: str) -> bool:
        """Delete a skill."""
        skill = self.get_by_name(name)
        if skill:
            self.session.delete(skill)
            self.session.commit()
            return True
        return False


def get_repository() -> SkillRepository:
    """Get a repository instance."""
    db_url = get_database_url()

    if is_async(db_url):
        engine = create_async_engine(db_url)
        async_session = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        return SkillRepository(async_session())
    else:
        engine = create_engine(db_url.replace("sqlite:///", "sqlite:///"))
        session = sessionmaker(bind=engine)()
        return SkillRepository(session)


def init_db():
    """Initialize database tables."""
    db_url = get_database_url()
    engine = create_engine(db_url.replace("sqlite:///", "sqlite:///"))
    Base.metadata.create_all(engine)
