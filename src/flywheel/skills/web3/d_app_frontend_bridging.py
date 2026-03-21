import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def generate_contract_calls(contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
    calls = {"web3_library": "ethers.js v6", "calls": []}

    for contract in contracts:
        call = {
            "address": contract.get("address", "0x0"),
            "abi": contract.get("abi", []),
            "methods": {},
        }

        for func in contract.get("functions", []):
            call["methods"][func] = {
                "signature": f"{func}",
                "call_data_example": "0x00000000",
            }

        calls["calls"].append(call)

    return calls


def create_event_listeners(
    contract_address: str, events: List[str]
) -> List[Dict[str, Any]]:
    listeners = []

    for event in events:
        listener = {
            "event": event,
            "filter": {
                "address": contract_address,
                "topics": [
                    "0x00000000000000000000000000000000000000000000000000000000"
                    + str(hash(event))[:8]
                ],
            },
            "handler": f"handle{event}Event",
        }
        listeners.append(listener)

    return listeners


def generate_frontend_bridge(config: Dict[str, Any]) -> Dict[str, Any]:
    bridge = {
        "bridge_id": f"dapp-bridge-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "web3_provider": config.get("web3_provider", "window.ethereum"),
        "chain_id": config.get("chain_id", 1),
        "contracts": [],
    }

    for contract in config.get("contracts", []):
        bridge["contracts"].append(
            {
                "name": contract.get("name", "Contract"),
                "address": contract.get("address", "0x0"),
                "abi_source": contract.get("abi_source", "local"),
                "events": contract.get("events", []),
            }
        )

    return bridge


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "bridge")

    try:
        if action == "bridge":
            config = payload.get("config", {})
            bridge = generate_frontend_bridge(config)

            return {
                "result": bridge,
                "metadata": {
                    "action": "bridge",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "contracts":
            contracts = payload.get("contracts", [])
            calls = generate_contract_calls(contracts)
            return {
                "result": calls,
                "metadata": {
                    "action": "contracts",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "events":
            contract_address = payload.get("contract_address", "0x0")
            events = payload.get("events", [])
            listeners = create_event_listeners(contract_address, events)
            return {
                "result": {"listeners": listeners},
                "metadata": {
                    "action": "events",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in d_app_frontend_bridging: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
