"""
OpenClaw Database Management Skill

Provides capabilities for managing OpenClaw's SQLite database,
including backup, restore, query, and maintenance operations.
"""

import gzip
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class OpenClawDatabaseManager:
    """Manage OpenClaw SQLite database."""

    def __init__(self, db_path: str | None = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = Path.home() / ".openclaw" / "openclaw.db"

    def get_database_info(self) -> Dict[str, Any]:
        """Get database information."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        stats = self.db_path.stat()

        return {
            "path": str(self.db_path),
            "size_bytes": stats.st_size,
            "size_mb": round(stats.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        }

    def list_tables(self) -> List[Dict[str, Any]]:
        """List all tables in the database."""
        if not self.db_path.exists():
            return [{"error": "Database not found"}]

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, type 
                FROM sqlite_master 
                WHERE type IN ('table', 'view')
                ORDER BY type, name
            """)

            tables = []
            for row in cursor.fetchall():
                table_name = row[0]

                cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                count = cursor.fetchone()[0]

                tables.append({"name": table_name, "type": row[1], "row_count": count})

            conn.close()
            return tables
        except sqlite3.Error as e:
            return [{"error": str(e)}]

    def query_table(
        self, table_name: str, limit: int = 100, offset: int = 0
    ) -> Dict[str, Any]:
        """Query data from a table."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                f'SELECT * FROM "{table_name}" LIMIT ? OFFSET ?', (limit, offset)
            )
            rows = cursor.fetchall()

            if not rows:
                return {"data": [], "columns": []}

            columns = rows[0].keys()
            data = [dict(row) for row in rows]

            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            total = cursor.fetchone()[0]

            conn.close()

            return {
                "data": data,
                "columns": list(columns),
                "total_rows": total,
                "limit": limit,
                "offset": offset,
            }
        except sqlite3.Error as e:
            return {"error": str(e)}

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a raw SQL query."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        query_upper = query.upper()

        if any(keyword in query_upper for keyword in dangerous_keywords):
            return {"error": "Destructive queries are not allowed"}

        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(query)

            if query_upper.strip().startswith("SELECT"):
                rows = cursor.fetchall()
                data = [dict(row) for row in rows] if rows else []
                columns = rows[0].keys() if rows else []

                conn.close()
                return {"data": data, "columns": list(columns), "row_count": len(data)}
            else:
                conn.commit()
                affected = cursor.rowcount
                conn.close()
                return {"success": True, "affected_rows": affected}
        except sqlite3.Error as e:
            return {"error": str(e)}

    def backup(self, backup_path: str | None = None) -> Dict[str, Any]:
        """Create a database backup."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        if backup_path:
            dest = Path(backup_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = self.db_path.parent / f"openclaw_backup_{timestamp}.db"

        try:
            shutil.copy2(self.db_path, dest)

            return {
                "status": "success",
                "backup_path": str(dest),
                "size_bytes": dest.stat().st_size,
            }
        except Exception as e:
            return {"error": str(e)}

    def compressed_backup(self, backup_path: str | None = None) -> Dict[str, Any]:
        """Create a compressed database backup."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        if backup_path:
            dest = Path(backup_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = self.db_path.parent / f"openclaw_backup_{timestamp}.db.gz"

        try:
            with open(self.db_path, "rb") as f_in:
                with gzip.open(dest, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            return {
                "status": "success",
                "backup_path": str(dest),
                "size_bytes": dest.stat().st_size,
            }
        except Exception as e:
            return {"error": str(e)}

    def restore(self, backup_path: str) -> Dict[str, Any]:
        """Restore database from backup."""
        source = Path(backup_path)

        if not source.exists():
            return {"error": f"Backup file not found: {backup_path}"}

        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(source, self.db_path)

            return {"status": "success", "restored_from": str(source)}
        except Exception as e:
            return {"error": str(e)}

    def vacuum(self) -> Dict[str, Any]:
        """Run VACUUM to optimize database."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        initial_size = self.db_path.stat().st_size

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("VACUUM")
            conn.close()

            final_size = self.db_path.stat().st_size
            freed = initial_size - final_size

            return {
                "status": "success",
                "initial_size_bytes": initial_size,
                "final_size_bytes": final_size,
                "freed_bytes": freed,
            }
        except sqlite3.Error as e:
            return {"error": str(e)}

    def get_conversation_history(
        self, agent_id: str | None = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.query_table("conversations", limit=limit)

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get agent usage statistics."""
        if not self.db_path.exists():
            return {"error": "Database not found"}

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            stats = {}

            cursor.execute("SELECT COUNT(*) FROM agents")
            stats["total_agents"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations")
            stats["total_conversations"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM messages")
            stats["total_messages"] = cursor.fetchone()[0]

            conn.close()

            return stats
        except sqlite3.Error as e:
            return {"error": str(e)}


MANIFEST = {
    "name": "openclaw_database_manager",
    "description": "Manage OpenClaw SQLite database - backup, restore, query, and optimize",
    "version": "1.0.0",
    "author": "Skill Flywheel",
    "capabilities": [
        "get_database_info",
        "list_tables",
        "query_table",
        "execute_query",
        "backup",
        "compressed_backup",
        "restore",
        "vacuum",
        "get_conversation_history",
        "get_agent_stats",
    ],
    "requirements": {"sqlite3": "Python standard library"},
}


def handle_request(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming requests."""

if __name__ == "__main__":
    manager = OpenClawDatabaseManager(params.get("db_path"))

        handlers = {
            "get_database_info": manager.get_database_info,
            "list_tables": manager.list_tables,
            "query_table": lambda: manager.query_table(
                params.get("table_name"), params.get("limit", 100), params.get("offset", 0)
            ),
            "execute_query": lambda: manager.execute_query(params.get("query")),
            "backup": lambda: manager.backup(params.get("backup_path")),
            "compressed_backup": lambda: manager.compressed_backup(
                params.get("backup_path")
            ),
            "restore": lambda: manager.restore(params.get("backup_path")),
            "vacuum": manager.vacuum,
            "get_conversation_history": lambda: manager.get_conversation_history(
                params.get("agent_id"), params.get("limit", 50)
            ),
            "get_agent_stats": manager.get_agent_stats,
        }

        handler = handlers.get(action)
        if handler:
            return handler()

        return {"error": f"Unknown action: {action}"}