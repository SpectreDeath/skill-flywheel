import time
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def get_protocol_abi(protocol: str) -> Dict[str, Any]:
    abis = {
        "uniswap": {
            "name": "Uniswap V3",
            "factory": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "functions": [
                "swapExactInputSingle",
                "swapExactOutputSingle",
                "addLiquidity",
            ],
        },
        "aave": {
            "name": "Aave V3",
            "pool": "0x87870Bca3F3f6335e32cdC7d553e1dEA5AF2E75b",
            "functions": ["supply", "borrow", "repay", "withdraw", "flashLoan"],
        },
        "compound": {
            "name": "Compound",
            "comptroller": "0x3d9819210A31b4961b30EF540b3a58825733a1C5",
            "functions": ["enterMarkets", "exitMarket", "borrow", "repayBorrow"],
        },
        "curve": {
            "name": "Curve",
            "address": "0x99a58482BD75cbab83b277EC9282256796785F55",
            "functions": ["add_liquidity", "remove_liquidity", "exchange"],
        },
    }

    return abis.get(protocol.lower(), {"error": "Protocol not supported"})


def generate_swap_transaction(protocol: str, params: Dict[str, Any]) -> Dict[str, Any]:
    token_in = params.get("token_in", "0x0000000000000000000000000000000000000000")
    token_out = params.get("token_out", "0x0000000000000000000000000000000000000000")
    amount_in = params.get("amount_in", "0")
    fee = params.get("fee", 3000)

    tx = {
        "to": get_protocol_abi(protocol).get("router", "0x0"),
        "data": "0x".join(
            [
                "04e45aaf".ljust(32 * 2, "0"),
                amount_in.lstrip("0x").zfill(64),
                (int(amount_in, 0) * 995 // 1000).hex().lstrip("0x").zfill(64)
                if amount_in.startswith("0x")
                else "0",
                token_in.lstrip("0x").zfill(64),
                token_out.lstrip("0x").zfill(64),
                "0" * 64,
                "0" * 64,
                "0" * 64,
                hex(fee).lstrip("0x").zfill(64),
            ]
        ),
    }

    return tx


def calculate_routes(
    token_in: str, token_out: str, amount: str
) -> List[Dict[str, Any]]:
    routes = []

    direct = {
        "path": [token_in, token_out],
        "protocols": ["Uniswap V3"],
        "estimated_output": str(
            int(amount, 0) * 997 // 1000
            if amount.startswith("0x")
            else int(amount) * 997 // 1000
        ),
    }
    routes.append(direct)

    hop = {
        "path": [token_in, "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", token_out],
        "protocols": ["Uniswap V3", "Uniswap V3"],
        "estimated_output": str(
            int(amount, 0) * 994 // 1000000
            if amount.startswith("0x")
            else int(amount) * 994 // 1000000
        ),
    }
    routes.append(hop)

    return routes


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "integrate")

    try:
        if action == "integrate":
            protocol = payload.get("protocol", "uniswap")
            abi = get_protocol_abi(protocol)

            return {
                "result": {"protocol_abi": abi},
                "metadata": {
                    "action": "integrate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "swap":
            protocol = payload.get("protocol", "uniswap")
            params = payload.get("params", {})
            tx = generate_swap_transaction(protocol, params)
            return {
                "result": {"transaction": tx},
                "metadata": {"action": "swap", "timestamp": datetime.now().isoformat()},
            }

        elif action == "routes":
            token_in = payload.get("token_in", "0x0")
            token_out = payload.get("token_out", "0x0")
            amount = payload.get("amount", "0")
            routes = calculate_routes(token_in, token_out, amount)
            return {
                "result": {"routes": routes},
                "metadata": {
                    "action": "routes",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in defi_protocol_integration: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
