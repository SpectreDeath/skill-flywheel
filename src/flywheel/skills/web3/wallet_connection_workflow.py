import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def generate_connection_flow() -> Dict[str, Any]:
    flow = {
        "flow_id": f"wallet-connection-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "steps": [],
    }

    flow["steps"].append(
        {
            "step": 1,
            "action": "detect_wallet",
            "description": "Check for injected wallet (MetaMask, WalletConnect)",
            "code_example": "if (window.ethereum) { /* wallet detected */ }",
        }
    )

    flow["steps"].append(
        {
            "step": 2,
            "action": "request_accounts",
            "description": "Request wallet connection",
            "code_example": "const accounts = await ethereum.request({ method: 'eth_requestAccounts' })",
        }
    )

    flow["steps"].append(
        {
            "step": 3,
            "action": "verify_connection",
            "description": "Verify account access and chain",
            "code_example": "const chainId = await ethereum.request({ method: 'eth_chainId' })",
        }
    )

    flow["steps"].append(
        {
            "step": 4,
            "action": "handle_events",
            "description": "Listen for account/chain changes",
            "code_example": "ethereum.on('accountsChanged', handleAccountsChanged)",
        }
    )

    return flow


def handle_wallet_errors(error: Dict[str, Any]) -> Dict[str, Any]:
    error_code = error.get("code", 0)

    solutions = {
        4001: {
            "message": "User rejected request",
            "action": "Show friendly message and retry button",
        },
        4900: {
            "message": "Disconnected from chain",
            "action": "Prompt user to switch to correct network",
        },
        4901: {
            "message": "Chain not found",
            "action": "Prompt user to add/switch network",
        },
        "-32002": {
            "message": "Request already pending",
            "action": "Wait for existing request to complete",
        },
    }

    solution = solutions.get(
        error_code, {"message": "Unknown error", "action": "Contact support"}
    )

    return {
        "error_code": error_code,
        "error_message": error.get("message", ""),
        "solution": solution,
    }


def validate_wallet_state(wallet_state: Dict[str, Any]) -> Dict[str, Any]:
    validation = {"valid": True, "errors": [], "warnings": []}

    if not wallet_state.get("isConnected"):
        validation["errors"].append("Wallet not connected")
        validation["valid"] = False

    accounts = wallet_state.get("accounts", [])
    if not accounts or len(accounts) == 0:
        validation["errors"].append("No accounts available")
        validation["valid"] = False

    chain_id = wallet_state.get("chainId")
    if not chain_id:
        validation["warnings"].append("Chain ID not available")

    if wallet_state.get("isMetaMask") and not wallet_state.get("isConnected"):
        validation["warnings"].append("MetaMask detected but not connected")

    return validation


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "connect")

    try:
        if action == "connect":
            flow = generate_connection_flow()

            return {
                "result": flow,
                "metadata": {
                    "action": "connect",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "error":
            error = payload.get("error", {})
            result = handle_wallet_errors(error)
            return {
                "result": result,
                "metadata": {
                    "action": "error",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            wallet_state = payload.get("wallet_state", {})
            result = validate_wallet_state(wallet_state)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in wallet_connection_workflow: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
