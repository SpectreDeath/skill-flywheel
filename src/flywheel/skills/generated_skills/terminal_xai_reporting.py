"""
Terminal XAI Reporting

Skill: terminal-xai-reporting
Domain: generated_skills
Description: ASCII visualization and terminal reporting for explainable AI outputs.

Actions:
- ascii_bar: Generate ASCII horizontal bar chart from a dict of {name: value}
- local_report: Format a full local explanation report (main effects + interactions)
- global_report: Format a global summary report
- section_header: Generate formatted section divider
"""

from datetime import datetime
from typing import Any, Dict, List


def section_header(title: str, width: int = 60) -> str:
    """Generate a formatted section divider with title."""
    border = "=" * width
    if not title:
        return f"+{border}+"
    pad = width - len(title) - 2
    left = pad // 2
    right = pad - left
    return f"+{'=' * left} {title} {'=' * right}+"


def ascii_bar(items: Dict[str, float], width: int = 40, max_label: int = 12) -> str:
    """Generate ASCII horizontal bar chart from {name: value} dict."""
    if not items:
        return "(empty chart)"
    sorted_items = sorted(items.items(), key=lambda x: abs(x[1]), reverse=True)
    max_abs = max(abs(v) for _, v in sorted_items) or 1.0
    lines = []
    for name, value in sorted_items:
        label = name[:max_label].ljust(max_label)
        bar_len = int(abs(value) / max_abs * width)
        bar = "#" * bar_len
        sign = "+" if value >= 0 else "-"
        lines.append(f"  {label} |{bar} {sign}{abs(value):.4f}")
    return "\n".join(lines)


def local_report(
    sample_id: str,
    main_effects: Dict[str, float],
    top_interactions: List[Dict[str, Any]],
) -> str:
    """Format a full local explanation report."""
    lines = [
        section_header(f"LOCAL XAI REPORT — {sample_id}"),
        "",
        "Main Effects (feature contributions):",
        ascii_bar(main_effects),
        "",
        "Top Interactions:",
    ]
    if top_interactions:
        for item in top_interactions[:5]:
            pair = item.get("pair", item.get("key", "?"))
            val = item.get("value", 0)
            lines.append(f"  {pair}: {val:+.4f}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append(section_header(""))
    return "\n".join(lines)


def global_report(
    n_samples: int,
    top_features: List[Dict[str, Any]],
    interaction_count: int,
) -> str:
    """Format a global summary report."""
    lines = [
        section_header("GLOBAL XAI SUMMARY"),
        "",
        f"Samples aggregated: {n_samples}",
        f"Total tracked interactions: {interaction_count}",
        "",
        "Top Global Features:",
    ]
    for i, feat in enumerate(top_features[:10]):
        idx = feat.get("index", "?")
        effect = feat.get("mean_effect", 0)
        lines.append(f"  {i + 1}. Feature {idx}: {effect:+.4f}")
    lines.append("")
    lines.append(section_header(""))
    return "\n".join(lines)


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for terminal-xai-reporting skill."""
    action = payload.get("action", "ascii_bar")

    if action == "ascii_bar":
        result = {
            "chart": ascii_bar(payload.get("items", {}), payload.get("width", 40))
        }
    elif action == "local_report":
        report = local_report(
            payload.get("sample_id", "unknown"),
            payload.get("main_effects", {}),
            payload.get("top_interactions", []),
        )
        result = {"report": report}
    elif action == "global_report":
        report = global_report(
            payload.get("n_samples", 0),
            payload.get("top_features", []),
            payload.get("interaction_count", 0),
        )
        result = {"report": report}
    elif action == "section_header":
        result = {
            "header": section_header(payload.get("title", ""), payload.get("width", 60))
        }
    else:
        result = {"error": f"Unknown action: {action}"}

    return {
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }


singleton = "terminal-xai-reporting"

if __name__ == "__main__":
    import asyncio

    effects = {"age": 0.35, "income": -0.22, "credit_score": 0.18, "debt": -0.12}
    print(
        asyncio.run(invoke({"action": "section_header", "title": "TEST"}))["result"][
            "header"
        ]
    )
    print(
        asyncio.run(invoke({"action": "ascii_bar", "items": effects}))["result"][
            "chart"
        ]
    )
    interactions = [
        {"pair": "[age, income]", "value": 0.08},
        {"pair": "[credit, debt]", "value": -0.05},
    ]
    print(
        asyncio.run(
            invoke(
                {
                    "action": "local_report",
                    "sample_id": "sample-001",
                    "main_effects": effects,
                    "top_interactions": interactions,
                }
            )
        )["result"]["report"]
    )
