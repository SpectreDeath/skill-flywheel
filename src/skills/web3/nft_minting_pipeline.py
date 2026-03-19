import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def generate_minting_config(config: Dict[str, Any]) -> Dict[str, Any]:
    minting_config = {
        "config_id": f"mint-config-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "token_standard": config.get("token_standard", "ERC-721"),
        "max_supply": config.get("max_supply", 10000),
        "mint_price_wei": config.get("mint_price_wei", 0),
        "max_per_wallet": config.get("max_per_wallet", 10),
    }

    if config.get("presale_enabled"):
        minting_config["presale"] = {
            "whitelist": config.get("whitelist", []),
            "presale_price_wei": config.get("presale_price_wei", 0),
            "presale_start": config.get("presale_start", "TBD"),
            "public_start": config.get("public_start", "TBD"),
        }

    minting_config["reveal"] = {
        "reveal_after_mint": config.get("reveal_after_mint", True),
        "base_uri": config.get("base_uri", "ipfs://placeholder"),
        "reveal_delay_seconds": config.get("reveal_delay_seconds", 0),
    }

    minting_config["royalties"] = {
        "recipient": config.get("royalty_recipient", ""),
        "percentage": config.get("royalty_percentage", 5),
    }

    return minting_config


def estimate_minting_gas(
    num_tokens: int, token_standard: str = "ERC-721"
) -> Dict[str, Any]:
    if token_standard == "ERC-721":
        base_gas = 90000
        per_token_gas = 65000
    else:
        base_gas = 55000
        per_token_gas = 35000

    estimated = base_gas + (num_tokens * per_token_gas)

    return {
        "token_standard": token_standard,
        "num_tokens": num_tokens,
        "estimated_gas": estimated,
        "estimated_gas_wei": estimated * 30000000000,
        "gas_price_gwei": 30,
    }


def generate_minting_transactions(
    config: Dict[str, Any], recipients: List[str]
) -> List[Dict[str, Any]]:
    transactions = []

    for i, recipient in enumerate(recipients):
        tx = {
            "to": config.get("contract_address", "0x0"),
            "from": config.get("minter_address", "0x0"),
            "data": "0x".join(
                [
                    "mint".ljust(10, "0"),
                    recipient.lstrip("0x").zfill(64),
                    hex(i + 1).lstrip("0x").zfill(64),
                ]
            ),
            "value": str(config.get("mint_price_wei", 0)),
        }
        transactions.append(tx)

    return transactions


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "config")

    try:
        if action == "config":
            config = payload.get("config", {})
            minting_config = generate_minting_config(config)

            return {
                "result": minting_config,
                "metadata": {
                    "action": "config",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "estimate":
            num_tokens = payload.get("num_tokens", 1)
            token_standard = payload.get("token_standard", "ERC-721")
            result = estimate_minting_gas(num_tokens, token_standard)
            return {
                "result": result,
                "metadata": {
                    "action": "estimate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "transactions":
            config = payload.get("config", {})
            recipients = payload.get("recipients", [])
            txs = generate_minting_transactions(config, recipients)
            return {
                "result": {"transactions": txs},
                "metadata": {
                    "action": "transactions",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in nft_minting_pipeline: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
