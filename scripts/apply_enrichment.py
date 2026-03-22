import json
from pathlib import Path

ENRICHMENT_DATA = {
    "qrisp-quantum-algorithms-grover-qpe-qaoa": {
        "tags": ["quantum", "qrisp", "grover", "qpe", "qaoa", "algorithms"],
        "category": "Quantum Computing",
        "estimated_time": "30m"
    },
    "dynamic-model-router": {
        "tags": ["orchestration", "routing", "qos", "latency", "failover"],
        "category": "Model Orchestration",
        "estimated_time": "25ms"
    },
    "hardware-model-selector": {
        "tags": ["hardware", "vram", "cuda", "resource-matching", "optimization"],
        "category": "Model Orchestration",
        "estimated_time": "20ms"
    },
    "model-ensemble-orchestrator": {
        "tags": ["ensemble", "consensus", "multi-model", "voting", "accuracy"],
        "category": "Model Orchestration",
        "estimated_time": "1500ms"
    },
    "model-health-monitor": {
        "tags": ["monitoring", "diagnostics", "gpu", "stability", "health-check"],
        "category": "Model Orchestration",
        "estimated_time": "50ms"
    },
    "model-latency-predictor": {
        "tags": ["prediction", "latency", "ttft", "performance", "real-time"],
        "category": "Model Orchestration",
        "estimated_time": "15ms"
    },
    "multi-model-fusion-engine": {
        "tags": ["fusion", "token-merging", "synthesis", "speculative-decoding"],
        "category": "Model Orchestration",
        "estimated_time": "2500ms"
    },
    "ralph-chaos-model-selector": {
        "tags": ["entropy", "noise-reduction", "chaos-monkey", "edge-cases"],
        "category": "Model Orchestration",
        "estimated_time": "10ms"
    },
    "task-model-optimizer": {
        "tags": ["semantic-routing", "task-matching", "efficiency", "specialization"],
        "category": "Model Orchestration",
        "estimated_time": "35ms"
    },
    "a-coding-guide-to-acp-systems": {
        "tags": ["acp", "coding-guide", "ml-engineering", "patterns", "best-practices"],
        "category": "AI/ML Engineering",
        "estimated_time": "45m"
    }
}

def apply_enrichment():
    registry_path = Path("skill_registry.json")
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    updated_count = 0
    for skill in registry:
        name = skill["name"]
        if name in ENRICHMENT_DATA:
            skill.update(ENRICHMENT_DATA[name])
            updated_count += 1
            
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    print(f"Enriched {updated_count} skills in JSON registry.")

if __name__ == "__main__":
    apply_enrichment()
