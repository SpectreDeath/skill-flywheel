import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def create_synthetic_data(
    schema: Dict[str, Any], num_rows: int
) -> List[Dict[str, Any]]:
    import random

    data = []
    for _ in range(num_rows):
        row = {}
        for field, ftype in schema.items():
            if ftype == "int":
                row[field] = random.randint(0, 100)
            elif ftype == "float":
                row[field] = random.random() * 100
            elif ftype == "str":
                row[field] = "sample_" + str(random.randint(1, 1000))
            elif ftype == "bool":
                row[field] = random.choice([True, False])
        data.append(row)
    return data


def detect_imbalance(dataset: List[Dict[str, Any]], label_col: str) -> Dict[str, Any]:
    labels = [row.get(label_col) for row in dataset]
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    len(labels)
    imbalance_ratio = max(counts.values()) / max(1, min(counts.values()))
    return {
        "counts": counts,
        "imbalance_ratio": imbalance_ratio,
        "is_imbalanced": imbalance_ratio > 3,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "create")
        if action == "create":
            schema = payload.get("schema", {"id": "int", "value": "float"})
            num_rows = payload.get("num_rows", 100)
            result = create_synthetic_data(schema, num_rows)
        elif action == "imbalance":
            dataset = payload.get("dataset", [])
            label = payload.get("label_column", "label")
            result = detect_imbalance(dataset, label)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
