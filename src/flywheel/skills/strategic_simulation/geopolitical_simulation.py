#!/usr/bin/env python3
"""
geopolitical-simulation

Geopolitical agent simulation framework with timeline branching,
diplomatic rules, and geographic map integration.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """Immutable agent state."""

    id: str
    strategy: str
    resources: float
    history: List[str] = field(default_factory=list)
    beliefs: List[str] = field(default_factory=list)
    tom_level: int = 0


@dataclass
class GameState:
    """Immutable game state."""

    version: int
    agents: Dict[str, Agent]
    board: Dict[str, str]
    history: List[Dict]
    metadata: Dict


def create_state(scenario: str = "default") -> GameState:
    """Create initial game state."""
    return GameState(
        version=1, agents={}, board={}, history=[], metadata={"scenario": scenario}
    )


def create_agent(agent_id: str, strategy: str, resources: float) -> Agent:
    """Create new agent with strategy."""
    return Agent(
        id=agent_id,
        strategy=strategy,
        resources=resources,
        history=[],
        beliefs=[],
        tom_level=0,
    )


def update_agent(agent: Agent, **updates) -> Agent:
    """Return updated agent (immutable)."""
    return Agent(
        id=updates.get("id", agent.id),
        strategy=updates.get("strategy", agent.strategy),
        resources=updates.get("resources", agent.resources),
        history=updates.get("history", agent.history),
        beliefs=updates.get("beliefs", agent.beliefs),
        tom_level=updates.get("tom_level", agent.tom_level),
    )


def add_belief(agent: Agent, belief: str) -> Agent:
    """Add belief to agent (immutable)."""
    return update_agent(agent, beliefs=agent.beliefs + [belief])


PAYOFF_MATRIX = {
    "hawk": {"hawk": -25, "dove": 50, "retreat": 0},
    "dove": {"hawk": 0, "dove": 25, "retreat": 10},
    "retreat": {"hawk": -10, "dove": 5, "retreat": 15},
}


def get_payoff(action: str, opponent_action: str) -> int:
    """Get payoff for action pair."""
    return PAYOFF_MATRIX.get(action, {}).get(opponent_action, 0)


def hawk_dominates(
    player_strategy: str, player_resources: float, opp_resources: float
) -> bool:
    """Rule: hawk with more resources dominates."""
    return player_strategy == "hawk" and player_resources > opp_resources


def alliance_formed(p1: Agent, p2: Agent, diplomatic_history: List[Dict]) -> bool:
    """Rule: alliance forms if sufficient diplomatic contact."""
    return any(d.get("type") == "alliance" for d in diplomatic_history)


class TimelineManager:
    """Timeline branching for counterfactual analysis."""

    def __init__(self):
        self.timelines: Dict[str, GameState] = {}

    def branch(self, state: GameState, move: Dict) -> str:
        """Create new timeline without modifying original."""
        timeline_id = str(uuid.uuid4())[:8]
        new_version = state.version + 1

        new_state = GameState(
            version=new_version,
            agents=state.agents.copy(),
            board=state.board.copy(),
            history=state.history + [move],
            metadata=state.metadata.copy(),
        )

        self.timelines[timeline_id] = new_state
        return timeline_id

    def branch_multiple(
        self, state: GameState, moves: List[Dict]
    ) -> Dict[str, GameState]:
        """Branch multiple possible futures."""
        results = {}
        for move in moves:
            tid = self.branch(state, move)
            results[tid] = self.timelines[tid]
        return results

    def compare_outcomes(self, timeline_ids: List[str], scorer_fn) -> List[Any]:
        """Compare outcomes across branches."""
        return [
            scorer_fn(self.timelines[tid])
            for tid in timeline_ids
            if tid in self.timelines
        ]


class GeoMap:
    """Geographic map with agent positions."""

    def __init__(self, geojson_data: Optional[Dict] = None):
        self.geojson = geojson_data or {}
        self.agents: Dict[str, str] = {}
        self.adjacencies: Dict[str, List[str]] = defaultdict(list)

    def place_agent(self, agent_id: str, region_id: str):
        """Place agent on map region."""
        self.agents[agent_id] = region_id

    def get_neighbors(self, region_id: str) -> List[str]:
        """Get neighboring regions."""
        return self.adjacencies.get(region_id, [])

    def bfs_influence(self, start_region: str, depth: int = 3) -> set:
        """BFS-based spatial reasoning."""
        visited = {start_region}
        queue = [(start_region, 0)]

        while queue:
            region, d = queue.pop(0)
            if d >= depth:
                continue
            for neighbor in self.get_neighbors(region):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, d + 1))

        return visited


SCENARIOS = {
    "ukraine": {
        "description": "Ukraine Crisis Simulation",
        "regions": ["ukraine", "russia", "belarus", "poland", "moldova"],
        "initial_agents": {
            "ukraine": {"strategy": "dove", "resources": 30},
            "russia": {"strategy": "hawk", "resources": 80},
            "belarus": {"strategy": "retreat", "resources": 15},
        },
    },
    "middle_east": {
        "description": "Middle East Regional",
        "regions": ["israel", "iran", "saudi_arabia", "syria", "iraq", "egypt"],
        "initial_agents": {
            "israel": {"strategy": "hawk", "resources": 50},
            "iran": {"strategy": "hawk", "resources": 55},
            "saudi_arabia": {"strategy": "dove", "resources": 45},
        },
    },
    "south_china": {
        "description": "South China Sea",
        "regions": ["china", "vietnam", "philippines", "taiwan", "malaysia"],
        "naval": True,
    },
}


def geopolitical_simulation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for geopolitical-simulation.

    Args:
        payload: Input with action, state, agents, scenario

    Returns:
        Updated state or timeline results
    """
    action = payload.get("action", "create_state")
    scenario = payload.get("scenario", "default")

    if action == "create_state":
        return _create_scenario(scenario)
    elif action == "create_agent":
        return _create_agent(payload)
    elif action == "branch_timeline":
        return _branch_timeline(payload)
    elif action == "decide":
        return _make_decision(payload)
    elif action == "analyze":
        return _analyze_state(payload)
    else:
        return {"error": f"Unknown action: {action}"}


def _create_scenario(scenario: str) -> Dict[str, Any]:
    """Create scenario with initial state."""
    if scenario not in SCENARIOS:
        scenario = "default"

    config = SCENARIOS[scenario]
    state = create_state(scenario)

    agents = {}
    for agent_id, config_data in config.get("initial_agents", {}).items():
        agent = create_agent(
            agent_id, config_data["strategy"], config_data["resources"]
        )
        agents[agent_id] = agent

    state = GameState(
        version=1,
        agents=agents,
        board={},
        history=[],
        metadata={"scenario": scenario, "regions": config.get("regions", [])},
    )

    return {
        "state": {
            "version": state.version,
            "scenario": scenario,
            "agents": {
                k: {"id": v.id, "strategy": v.strategy, "resources": v.resources}
                for k, v in state.agents.items()
            },
            "regions": config.get("regions", []),
        },
        "timeline_id": str(uuid.uuid4())[:8],
    }


def _create_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create agent in state."""
    agent_id = payload.get("agent_id", "agent_" + str(uuid.uuid4())[:4])
    strategy = payload.get("strategy", "neutral")
    resources = payload.get("resources", 50.0)

    agent = create_agent(agent_id, strategy, resources)

    return {
        "agent": {
            "id": agent.id,
            "strategy": agent.strategy,
            "resources": agent.resources,
        },
    }


def _branch_timeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Branch timeline for counterfactual."""
    moves = payload.get("moves", [{"action": "test_move"}])
    timeline_mgr = TimelineManager()

    state = create_state()
    branches = timeline_mgr.branch_multiple(state, moves)

    return {
        "timelines": list(branches.keys()),
        "count": len(branches),
    }


def _make_decision(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make strategic decision for agent."""
    strategy = payload.get("strategy", "tit_for_tat")
    history = payload.get("history", [])
    opp_history = payload.get("opp_history", [])
    resources = payload.get("resources", 50.0)
    opp_resources = payload.get("opp_resources", 50.0)

    if strategy == "hawk":
        action = "hawk"
        reasoning = "Hawk strategy: aggressive posture"
    elif strategy == "dove":
        action = "dove"
        reasoning = "Dove strategy: peaceful approach"
    elif strategy == "tit_for_tat":
        action = opp_history[-1] if opp_history else "dove"
        reasoning = f"Tit-for-tat: mirrors last move ({action})"
    elif strategy == "grudger":
        action = "defect" if "defect" in opp_history else "cooperate"
        reasoning = f"Grudger: {'defects' if action == 'defect' else 'cooperates'}"
    elif strategy == "retreat":
        action = "retreat"
        reasoning = "Retreat strategy: conservative positioning"
    else:
        action = "dove"
        reasoning = "Default: cooperate"

    payoff = get_payoff(action, "dove")  # vs default opponent

    return {
        "action": action,
        "payoff": payoff,
        "reasoning": reasoning,
    }


def _analyze_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze current state."""
    agents = payload.get("agents", {})

    hawks = sum(1 for a in agents.values() if a.get("strategy") == "hawk")
    doves = sum(1 for a in agents.values() if a.get("strategy") == "dove")

    return {
        "total_agents": len(agents),
        "hawks": hawks,
        "doves": doves,
        "balance": "hawk_heavy"
        if hawks > doves
        else "dove_heavy"
        if doves > hawks
        else "balanced",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "create_state")
    try:
        result = geopolitical_simulation(payload)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in geopolitical-simulation: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "geopolitical-simulation",
            "description": "Geopolitical agent simulation with timeline branching, diplomatic rules, and geographic maps.",
            "version": "1.0.0",
            "domain": "strategic_simulation",
        }