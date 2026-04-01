#!/usr/bin/env python3
"""
Session Manager for Agent Runtimes

Manages conversational sessions including:
- Session creation and persistence
- Message history tracking
- Token usage counting
- Session restoration

Pattern extracted from Claw Code's session_store.py and runtime.py.
"""

import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SessionMessage:
    """Single message in a session."""
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content, "timestamp": self.timestamp}


@dataclass
class Session:
    """A conversational session with history."""
    session_id: str
    messages: List[SessionMessage] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        self.messages.append(SessionMessage(role=role, content=content))
        self.updated_at = datetime.now().isoformat()

        # Rough token estimate
        if role in ("user", "system"):
            self.input_tokens += len(content.split())
        else:
            self.output_tokens += len(content.split())

    def get_turn_count(self) -> int:
        """Get number of conversation turns."""
        return len(self.messages) // 2

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "message_count": len(self.messages),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }


_session_store: Dict[str, Session] = {}


def create_session(session_id: Optional[str] = None, metadata: Optional[Dict] = None) -> Session:
    """Create a new session."""
    if not session_id:
        session_id = hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:12]

    session = Session(
        session_id=session_id,
        metadata=metadata or {}
    )
    _session_store[session_id] = session
    return session


def get_session(session_id: str) -> Optional[Session]:
    """Retrieve a session by ID."""
    return _session_store.get(session_id)


def submit_message(session_id: str, content: str) -> Optional[Session]:
    """Submit a user message to a session."""
    session = get_session(session_id)
    if not session:
        return None

    session.add_message("user", content)
    return session


def persist_session(session: Session, directory: str = ".sessions") -> str:
    """Persist a session to disk."""
    dir_path = Path(directory)
    dir_path.mkdir(exist_ok=True)

    file_path = dir_path / f"{session.session_id}.json"
    data = {
        "session_id": session.session_id,
        "messages": [m.to_dict() for m in session.messages],
        "input_tokens": session.input_tokens,
        "output_tokens": session.output_tokens,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "metadata": session.metadata
    }
    file_path.write_text(json.dumps(data, indent=2))

    logger.info(f"Persisted session {session.session_id} to {file_path}")
    return str(file_path)


def load_session(session_id: str, directory: str = ".sessions") -> Optional[Session]:
    """Load a session from disk."""
    file_path = Path(directory) / f"{session_id}.json"

    if not file_path.exists():
        return None

    data = json.loads(file_path.read_text())
    session = Session(
        session_id=data["session_id"],
        input_tokens=data.get("input_tokens", 0),
        output_tokens=data.get("output_tokens", 0),
        created_at=data.get("created_at", ""),
        updated_at=data.get("updated_at", ""),
        metadata=data.get("metadata", {})
    )
    session.messages = [
        SessionMessage(role=m["role"], content=m["content"], timestamp=m.get("timestamp", ""))
        for m in data.get("messages", [])
    ]

    _session_store[session_id] = session
    return session


def list_sessions(directory: str = ".sessions") -> List[Dict[str, Any]]:
    """List all persisted sessions."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    sessions = []
    for f in dir_path.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            sessions.append({
                "session_id": data.get("session_id", f.stem),
                "message_count": len(data.get("messages", [])),
                "input_tokens": data.get("input_tokens", 0),
                "output_tokens": data.get("output_tokens", 0)
            })
        except (json.JSONDecodeError, KeyError):
            continue

    return sessions


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "create")
    session_id = payload.get("session_id")
    content = payload.get("content", "")
    directory = payload.get("directory", ".sessions")

    if action == "create":
        metadata = payload.get("metadata", {})
        session = create_session(session_id, metadata)

        return {
            "result": session.to_dict(),
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "submit":
        if not session_id:
            return {
                "result": {"error": "session_id required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        session = get_session(session_id) or create_session(session_id)
        submit_message(session_id, content)

        return {
            "result": {
                "session_id": session_id,
                "message_count": len(session.messages),
                "last_message": content[:100] + "..." if len(content) > 100 else content
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "load":
        if not session_id:
            return {
                "result": {"error": "session_id required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        session = load_session(session_id, directory)
        if not session:
            return {
                "result": {"error": f"Session not found: {session_id}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        return {
            "result": session.to_dict(),
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "persist":
        if not session_id:
            return {
                "result": {"error": "session_id required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        session = get_session(session_id)
        if not session:
            return {
                "result": {"error": f"Session not found: {session_id}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        path = persist_session(session, directory)

        return {
            "result": {"path": path, "session_id": session_id},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "list":
        sessions = list_sessions(directory)

        return {
            "result": {"sessions": sessions, "count": len(sessions)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill():
    """Return skill metadata."""
    return {
        "name": "session-manager",
        "description": "Conversational session management with history tracking, token counting, and persistence for agent runtimes",
        "version": "1.0.0",
        "domain": "MODERN_BACKEND",
    }