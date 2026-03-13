#!/usr/bin/env python3
"""
Skill: migration-manager
Domain: database_engineering
Description: Database schema migration and version control system
"""

import asyncio
import logging
import time
import uuid
import json
import os
import hashlib
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

class MigrationType(Enum):
    """Types of database migrations"""
    SCHEMA = "schema"
    DATA = "data"
    INDEX = "index"
    CONSTRAINT = "constraint"
    PROCEDURE = "procedure"

class MigrationStatus(Enum):
    """Migration execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class DatabaseType(Enum):
    """Supported database types"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MARIADB = "mariadb"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"

@dataclass
class Migration:
    """Represents a database migration"""
    migration_id: str
    version: str
    name: str
    description: str
    migration_type: MigrationType
    up_sql: str
    down_sql: str
    checksum: str
    dependencies: List[str]
    created_at: float
    executed_at: Optional[float]
    status: MigrationStatus
    error_message: Optional[str]

@dataclass
class MigrationPlan:
    """Represents a migration execution plan"""
    plan_id: str
    target_version: str
    migrations: List[Migration]
    estimated_duration: int
    rollback_possible: bool
    created_at: float

@dataclass
class DatabaseConnection:
    """Database connection configuration"""
    connection_id: str
    database_type: DatabaseType
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_enabled: bool
    connection_timeout: int
    created_at: float

class MigrationManager:
    """Database schema migration and version control system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the migration manager
        
        Args:
            config: Configuration dictionary with:
                - migrations_path: Path to migration files
                - backup_enabled: Whether to create backups before migrations
                - dry_run_mode: Whether to run migrations in dry-run mode
        """
        self.migrations_path = config.get("migrations_path", "./migrations")
        self.backup_enabled = config.get("backup_enabled", True)
        self.dry_run_mode = config.get("dry_run_mode", False)
        
        self.migrations: Dict[str, Migration] = {}
        self.migration_plans: Dict[str, MigrationPlan] = {}
        self.connections: Dict[str, DatabaseConnection] = {}
        
        self.migration_stats = {
            "total_migrations": 0,
            "executed_migrations": 0,
            "failed_migrations": 0,
            "rolled_back_migrations": 0,
            "total_backups": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Ensure migrations directory exists
        os.makedirs(self.migrations_path, exist_ok=True)
        
        # Load existing migrations
        self._load_migrations()
    
    def create_migration(self,
                        version: str,
                        name: str,
                        description: str,
                        migration_type: MigrationType,
                        up_sql: str,
                        down_sql: str,
                        dependencies: Optional[List[str]] = None) -> str:
        """
        Create a new migration
        
        Args:
            version: Migration version (e.g., "20231201_001")
            name: Migration name
            description: Migration description
            migration_type: Type of migration
            up_sql: SQL for forward migration
            down_sql: SQL for rollback migration
            dependencies: List of dependent migration IDs
            
        Returns:
            Migration ID
        """
        migration_id = str(uuid.uuid4())
        
        # Calculate checksum
        content = f"{up_sql}{down_sql}{version}{name}"
        checksum = hashlib.sha256(content.encode()).hexdigest()
        
        migration = Migration(
            migration_id=migration_id,
            version=version,
            name=name,
            description=description,
            migration_type=migration_type,
            up_sql=up_sql,
            down_sql=down_sql,
            checksum=checksum,
            dependencies=dependencies or [],
            created_at=time.time(),
            executed_at=None,
            status=MigrationStatus.PENDING,
            error_message=None
        )
        
        self.migrations[migration_id] = migration
        self.migration_stats["total_migrations"] += 1
        
        # Save migration file
        self._save_migration_file(migration)
        
        self.logger.info(f"Created migration: {migration_id} (version {version})")
        return migration_id
    
    def create_connection(self,
                         database_type: DatabaseType,
                         host: str,
                         port: int,
                         database: str,
                         username: str,
                         password: str,
                         ssl_enabled: bool = False,
                         connection_timeout: int = 30) -> str:
        """
        Create a database connection
        
        Args:
            database_type: Type of database
            host: Database host
            port: Database port
            database: Database name
            username: Database username
            password: Database password
            ssl_enabled: Whether SSL is enabled
            connection_timeout: Connection timeout in seconds
            
        Returns:
            Connection ID
        """
        connection_id = str(uuid.uuid4())
        
        connection = DatabaseConnection(
            connection_id=connection_id,
            database_type=database_type,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            ssl_enabled=ssl_enabled,
            connection_timeout=connection_timeout,
            created_at=time.time()
        )
        
        self.connections[connection_id] = connection
        self.logger.info(f"Created database connection: {connection_id}")
        return connection_id
    
    def plan_migration(self, target_version: str, connection_id: str) -> str:
        """
        Create a migration execution plan
        
        Args:
            target_version: Target version to migrate to
            connection_id: Database connection ID
            
        Returns:
            Plan ID
        """
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        # Get current version
        current_version = self._get_current_version(connection_id)
        
        # Find migrations to execute
        migrations_to_run = self._get_migrations_for_version(target_version, current_version)
        
        # Validate dependencies
        self._validate_migration_dependencies(migrations_to_run)
        
        # Calculate estimated duration
        estimated_duration = self._calculate_estimated_duration(migrations_to_run)
        
        plan_id = str(uuid.uuid4())
        
        plan = MigrationPlan(
            plan_id=plan_id,
            target_version=target_version,
            migrations=migrations_to_run,
            estimated_duration=estimated_duration,
            rollback_possible=True,
            created_at=time.time()
        )
        
        self.migration_plans[plan_id] = plan
        
        self.logger.info(f"Created migration plan: {plan_id} (target: {target_version})")
        return plan_id
    
    async def execute_migration(self, plan_id: str, connection_id: str) -> Dict[str, Any]:
        """
        Execute a migration plan
        
        Args:
            plan_id: Migration plan ID
            connection_id: Database connection ID
            
        Returns:
            Execution results
        """
        if plan_id not in self.migration_plans:
            raise ValueError(f"Plan {plan_id} not found")
        
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        plan = self.migration_plans[plan_id]
        connection = self.connections[connection_id]
        
        execution_results = {
            "plan_id": plan_id,
            "connection_id": connection_id,
            "target_version": plan.target_version,
            "start_time": time.time(),
            "migrations_executed": [],
            "success": True,
            "error_details": []
        }
        
        # Create backup if enabled
        backup_id = None
        if self.backup_enabled and not self.dry_run_mode:
            backup_id = await self._create_backup(connection)
            execution_results["backup_id"] = backup_id
        
        try:
            # Execute migrations
            for migration in plan.migrations:
                if self.dry_run_mode:
                    self.logger.info(f"DRY RUN: Would execute migration {migration.version}")
                    migration.status = MigrationStatus.COMPLETED
                    migration.executed_at = time.time()
                else:
                    await self._execute_single_migration(migration, connection)
                
                execution_results["migrations_executed"].append({
                    "migration_id": migration.migration_id,
                    "version": migration.version,
                    "status": migration.status.value,
                    "executed_at": migration.executed_at
                })
                
                if migration.status == MigrationStatus.FAILED:
                    execution_results["success"] = False
                    execution_results["error_details"].append({
                        "migration_id": migration.migration_id,
                        "error": migration.error_message
                    })
                    break
            
            execution_results["end_time"] = time.time()
            execution_results["duration"] = execution_results["end_time"] - execution_results["start_time"]
            
            if execution_results["success"]:
                self.migration_stats["executed_migrations"] += len(plan.migrations)
                self.logger.info(f"Migration plan {plan_id} completed successfully")
            else:
                self.migration_stats["failed_migrations"] += 1
                self.logger.error(f"Migration plan {plan_id} failed")
        
        except Exception as e:
            execution_results["success"] = False
            execution_results["error_details"].append({
                "error": str(e)
            })
            self.logger.error(f"Migration plan {plan_id} failed with exception: {e}")
        
        return execution_results
    
    async def rollback_migration(self, migration_id: str, connection_id: str) -> Dict[str, Any]:
        """
        Rollback a specific migration
        
        Args:
            migration_id: Migration ID to rollback
            connection_id: Database connection ID
            
        Returns:
            Rollback results
        """
        if migration_id not in self.migrations:
            raise ValueError(f"Migration {migration_id} not found")
        
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        migration = self.migrations[migration_id]
        connection = self.connections[connection_id]
        
        rollback_results = {
            "migration_id": migration_id,
            "version": migration.version,
            "start_time": time.time(),
            "success": True,
            "error_details": []
        }
        
        try:
            if self.dry_run_mode:
                self.logger.info(f"DRY RUN: Would rollback migration {migration.version}")
                migration.status = MigrationStatus.ROLLED_BACK
            else:
                await self._execute_rollback(migration, connection)
            
            rollback_results["end_time"] = time.time()
            rollback_results["duration"] = rollback_results["end_time"] - rollback_results["start_time"]
            
            if migration.status == MigrationStatus.ROLLED_BACK:
                self.migration_stats["rolled_back_migrations"] += 1
                self.logger.info(f"Rollback of migration {migration_id} completed successfully")
            else:
                rollback_results["success"] = False
                rollback_results["error_details"].append({
                    "error": migration.error_message
                })
                self.logger.error(f"Rollback of migration {migration_id} failed")
        
        except Exception as e:
            rollback_results["success"] = False
            rollback_results["error_details"].append({
                "error": str(e)
            })
            self.logger.error(f"Rollback of migration {migration_id} failed with exception: {e}")
        
        return rollback_results
    
    def get_migration_status(self, connection_id: str) -> Dict[str, Any]:
        """
        Get migration status for a database connection
        
        Args:
            connection_id: Database connection ID
            
        Returns:
            Migration status information
        """
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        current_version = self._get_current_version(connection_id)
        pending_migrations = self._get_pending_migrations(current_version)
        
        return {
            "connection_id": connection_id,
            "current_version": current_version,
            "total_migrations": self.migration_stats["total_migrations"],
            "executed_migrations": self.migration_stats["executed_migrations"],
            "pending_migrations": len(pending_migrations),
            "failed_migrations": self.migration_stats["failed_migrations"],
            "latest_migrations": self._get_latest_migrations(10),
            "status_timestamp": time.time()
        }
    
    def get_migration_stats(self) -> Dict[str, Any]:
        """Get migration statistics"""
        return {
            "total_migrations": self.migration_stats["total_migrations"],
            "executed_migrations": self.migration_stats["executed_migrations"],
            "failed_migrations": self.migration_stats["failed_migrations"],
            "rolled_back_migrations": self.migration_stats["rolled_back_migrations"],
            "total_backups": self.migration_stats["total_backups"],
            "success_rate": self.migration_stats["executed_migrations"] / max(1, self.migration_stats["total_migrations"]),
            "active_connections": len(self.connections),
            "active_plans": len(self.migration_plans)
        }
    
    def _load_migrations(self):
        """Load existing migrations from files"""
        migration_files = [f for f in os.listdir(self.migrations_path) if f.endswith('.json')]
        
        for filename in migration_files:
            filepath = os.path.join(self.migrations_path, filename)
            try:
                with open(filepath, 'r') as f:
                    migration_data = json.load(f)
                    migration = Migration(**migration_data)
                    self.migrations[migration.migration_id] = migration
            except Exception as e:
                self.logger.error(f"Failed to load migration file {filename}: {e}")
    
    def _save_migration_file(self, migration: Migration):
        """Save migration to file"""
        filename = f"{migration.version}_{migration.name.replace(' ', '_').lower()}.json"
        filepath = os.path.join(self.migrations_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(asdict(migration), f, indent=2)
    
    def _get_current_version(self, connection_id: str) -> str:
        """Get current database version"""
        # In a real implementation, this would query the database
        # For now, return a mock version
        return "20230101_000"
    
    def _get_migrations_for_version(self, target_version: str, current_version: str) -> List[Migration]:
        """Get migrations to execute for target version"""
        # Filter migrations between current and target version
        migrations = [
            m for m in self.migrations.values()
            if current_version < m.version <= target_version
        ]
        
        # Sort by version
        migrations.sort(key=lambda m: m.version)
        
        return migrations
    
    def _validate_migration_dependencies(self, migrations: List[Migration]):
        """Validate migration dependencies"""
        migration_map = {m.migration_id: m for m in migrations}
        
        for migration in migrations:
            for dep_id in migration.dependencies:
                if dep_id not in migration_map:
                    raise ValueError(f"Dependency {dep_id} not found for migration {migration.version}")
    
    def _calculate_estimated_duration(self, migrations: List[Migration]) -> int:
        """Calculate estimated migration duration"""
        base_duration = len(migrations) * 30  # 30 seconds per migration
        complexity_factor = sum(1 for m in migrations if m.migration_type in [MigrationType.SCHEMA, MigrationType.DATA])
        
        return base_duration + (complexity_factor * 60)
    
    async def _create_backup(self, connection: DatabaseConnection) -> str:
        """Create database backup"""
        backup_id = str(uuid.uuid4())
        
        # In a real implementation, this would create an actual database backup
        # For now, simulate backup creation
        await asyncio.sleep(1)
        
        self.migration_stats["total_backups"] += 1
        self.logger.info(f"Created backup: {backup_id}")
        
        return backup_id
    
    async def _execute_single_migration(self, migration: Migration, connection: DatabaseConnection):
        """Execute a single migration"""
        try:
            migration.status = MigrationStatus.RUNNING
            
            # In a real implementation, this would execute the SQL against the database
            # For now, simulate execution
            await asyncio.sleep(2)
            
            migration.status = MigrationStatus.COMPLETED
            migration.executed_at = time.time()
            
            self.logger.info(f"Executed migration {migration.version} successfully")
            
        except Exception as e:
            migration.status = MigrationStatus.FAILED
            migration.error_message = str(e)
            self.logger.error(f"Failed to execute migration {migration.version}: {e}")
    
    async def _execute_rollback(self, migration: Migration, connection: DatabaseConnection):
        """Execute migration rollback"""
        try:
            migration.status = MigrationStatus.RUNNING
            
            # In a real implementation, this would execute the down SQL against the database
            # For now, simulate rollback
            await asyncio.sleep(1)
            
            migration.status = MigrationStatus.ROLLED_BACK
            
            self.logger.info(f"Rolled back migration {migration.version} successfully")
            
        except Exception as e:
            migration.status = MigrationStatus.FAILED
            migration.error_message = str(e)
            self.logger.error(f"Failed to rollback migration {migration.version}: {e}")
    
    def _get_pending_migrations(self, current_version: str) -> List[Migration]:
        """Get pending migrations"""
        return [
            m for m in self.migrations.values()
            if m.version > current_version and m.status == MigrationStatus.PENDING
        ]
    
    def _get_latest_migrations(self, limit: int) -> List[Dict[str, Any]]:
        """Get latest migrations"""
        sorted_migrations = sorted(
            self.migrations.values(),
            key=lambda m: m.created_at,
            reverse=True
        )
        
        return [
            {
                "migration_id": m.migration_id,
                "version": m.version,
                "name": m.name,
                "status": m.status.value,
                "created_at": m.created_at
            }
            for m in sorted_migrations[:limit]
        ]

# Global migration manager instance
_migration_manager = MigrationManager({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_migration", "create_connection", "plan_migration", 
                     "execute_migration", "rollback_migration", "get_status", "get_stats"
            - migration_data: Migration configuration
            - connection_data: Database connection configuration
            - execution_data: Execution parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_migration":
            migration_data = payload.get("migration_data", {})
            
            migration_id = _migration_manager.create_migration(
                version=migration_data.get("version", "20230101_001"),
                name=migration_data.get("name", "New Migration"),
                description=migration_data.get("description", ""),
                migration_type=MigrationType(migration_data.get("migration_type", "schema")),
                up_sql=migration_data.get("up_sql", ""),
                down_sql=migration_data.get("down_sql", ""),
                dependencies=migration_data.get("dependencies", [])
            )
            
            return {
                "result": {
                    "migration_id": migration_id,
                    "message": f"Created migration: {migration_id}"
                },
                "metadata": {
                    "action": "create_migration",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_connection":
            connection_data = payload.get("connection_data", {})
            
            connection_id = _migration_manager.create_connection(
                database_type=DatabaseType(connection_data.get("database_type", "postgresql")),
                host=connection_data.get("host", "localhost"),
                port=connection_data.get("port", 5432),
                database=connection_data.get("database", "test"),
                username=connection_data.get("username", "user"),
                password=connection_data.get("password", "password"),
                ssl_enabled=connection_data.get("ssl_enabled", False),
                connection_timeout=connection_data.get("connection_timeout", 30)
            )
            
            return {
                "result": {
                    "connection_id": connection_id,
                    "message": f"Created database connection: {connection_id}"
                },
                "metadata": {
                    "action": "create_connection",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "plan_migration":
            execution_data = payload.get("execution_data", {})
            
            plan_id = _migration_manager.plan_migration(
                target_version=execution_data.get("target_version", "20231201_001"),
                connection_id=execution_data.get("connection_id", "")
            )
            
            return {
                "result": {
                    "plan_id": plan_id,
                    "message": f"Created migration plan: {plan_id}"
                },
                "metadata": {
                    "action": "plan_migration",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "execute_migration":
            execution_data = payload.get("execution_data", {})
            
            results = await _migration_manager.execute_migration(
                plan_id=execution_data.get("plan_id", ""),
                connection_id=execution_data.get("connection_id", "")
            )
            
            return {
                "result": results,
                "metadata": {
                    "action": "execute_migration",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "rollback_migration":
            execution_data = payload.get("execution_data", {})
            
            results = await _migration_manager.rollback_migration(
                migration_id=execution_data.get("migration_id", ""),
                connection_id=execution_data.get("connection_id", "")
            )
            
            return {
                "result": results,
                "metadata": {
                    "action": "rollback_migration",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            connection_id = payload.get("connection_id", "")
            status = _migration_manager.get_migration_status(connection_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "connection_id": connection_id
                }
            }
        
        elif action == "get_stats":
            stats = _migration_manager.get_migration_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
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
        logger.error(f"Error in migration_manager: {e}")
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
    """Example of how to use the migration manager skill"""
    
    # Create a database connection
    connection_id = await invoke({
        "action": "create_connection",
        "connection_data": {
            "database_type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "username": "admin",
            "password": "secret"
        }
    })
    
    print(f"Created connection: {connection_id['result']['connection_id']}")
    
    # Create a migration
    migration_id = await invoke({
        "action": "create_migration",
        "migration_data": {
            "version": "20231201_001",
            "name": "Add user profiles table",
            "description": "Create user_profiles table for storing user profile information",
            "migration_type": "schema",
            "up_sql": """
            CREATE TABLE user_profiles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                bio TEXT,
                avatar_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            "down_sql": "DROP TABLE user_profiles;",
            "dependencies": []
        }
    })
    
    print(f"Created migration: {migration_id['result']['migration_id']}")
    
    # Create another migration
    migration_id2 = await invoke({
        "action": "create_migration",
        "migration_data": {
            "version": "20231201_002",
            "name": "Add indexes for performance",
            "description": "Add indexes on frequently queried columns",
            "migration_type": "index",
            "up_sql": """
            CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
            CREATE INDEX idx_users_email ON users(email);
            """,
            "down_sql": """
            DROP INDEX IF EXISTS idx_user_profiles_user_id;
            DROP INDEX IF EXISTS idx_users_email;
            """,
            "dependencies": [migration_id['result']['migration_id']]
        }
    })
    
    print(f"Created migration: {migration_id2['result']['migration_id']}")
    
    # Plan migration
    plan_id = await invoke({
        "action": "plan_migration",
        "execution_data": {
            "target_version": "20231201_002",
            "connection_id": connection_id['result']['connection_id']
        }
    })
    
    print(f"Created migration plan: {plan_id['result']['plan_id']}")
    
    # Execute migration
    results = await invoke({
        "action": "execute_migration",
        "execution_data": {
            "plan_id": plan_id['result']['plan_id'],
            "connection_id": connection_id['result']['connection_id']
        }
    })
    
    print(f"Migration results: {results['result']}")
    
    # Get migration status
    status = await invoke({
        "action": "get_status",
        "connection_id": connection_id['result']['connection_id']
    })
    
    print(f"Migration status: {status['result']}")
    
    # Get migration statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Migration stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())