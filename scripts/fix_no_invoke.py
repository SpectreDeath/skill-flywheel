"""
Batch fix: Add invoke() wrappers to pre-existing modules that lack them.
Target: cognitive skills, data pipelines, context_hub_provider.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PROJECT_ROOT, "src", "flywheel", "skills")

COGNITIVE_SKILLS = {
    "accuracy_and_speed": {
        "class": "AccuracySpeedOptimizer",
        "actions": {
            "solve_with_time_limit": "solve_with_time_limit",
            "estimate_difficulty": "estimate_difficulty",
            "allocate_time": "allocate_time",
            "eliminate_wrong_answers": "eliminate_wrong_answers",
            "verify_answer": "verify_answer",
            "get_info": None,
        },
        "default_action": "solve_with_time_limit",
    },
    "analytical_thinking": {
        "class": "AnalyticalThinker",
        "actions": {
            "analyze_problem": "analyze_problem",
            "decompose": "decompose",
            "identify_patterns": "identify_patterns",
            "synthesize_insights": "synthesize_insights",
            "root_cause_analysis": "root_cause_analysis",
            "get_info": None,
        },
        "default_action": "analyze_problem",
    },
    "conclusive_thinking": {
        "class": "ConclusiveThinker",
        "actions": {
            "evaluate_evidence": "evaluate_evidence",
            "determine_conclusion": "determine_conclusion",
            "state_conclusion": "state_conclusion",
            "add_evidence": "add_evidence",
            "assess_sufficiency": "assess_sufficiency",
            "get_info": None,
        },
        "default_action": "evaluate_evidence",
    },
    "convergent_thinking": {
        "class": "ConvergentThinker",
        "actions": {
            "solve": "solve",
            "analyze_problem": "analyze_problem",
            "make_decision": "make_decision",
            "evaluate_claim": "evaluate_claim",
            "synthesize_knowledge": "synthesize_knowledge",
            "find_answer": "find_answer",
            "assess_facts": "assess_facts",
            "conclude": "conclude",
            "get_info": None,
        },
        "default_action": "solve",
    },
    "critical_evaluation": {
        "class": "CriticalEvaluator",
        "actions": {
            "evaluate_claim": "evaluate_claim",
            "evaluate_source": "evaluate_source",
            "create_weighted_evaluation": "create_weighted_evaluation",
            "get_info": None,
        },
        "default_action": "evaluate_claim",
    },
    "decision_making": {
        "class": "DecisionMaker",
        "actions": {
            "create_decision": "create_decision",
            "add_criterion": "add_criterion",
            "add_option": "add_option",
            "score_option": "score_option",
            "evaluate": "evaluate",
            "decide": "decide",
            "create_decision_tree": "create_decision_tree",
            "get_info": None,
        },
        "default_action": "decide",
    },
    "depth_of_understanding": {
        "class": "DepthUnderstander",
        "actions": {
            "surface_level": "surface_level",
            "relationship_level": "relationship_level",
            "mechanism_level": "mechanism_level",
            "implication_level": "implication_level",
            "build_depth_understanding": "build_depth_understanding",
            "explain_algorithm": "explain_algorithm",
            "get_info": None,
        },
        "default_action": "build_depth_understanding",
    },
    "fact_based_assessment": {
        "class": "FactBasedAssessor",
        "actions": {
            "add_fact": "add_fact",
            "add_opinion": "add_opinion",
            "separate_facts_from_opinions": "separate_facts_from_opinions",
            "analyze_facts": "analyze_facts",
            "draw_conclusion": "draw_conclusion",
            "assess_facts": "assess_facts",
            "assess_data": "assess_data",
            "get_info": None,
        },
        "default_action": "assess_facts",
    },
    "focused_selection": {
        "class": "FocusedSelector",
        "actions": {
            "define_frame": "define_frame",
            "identify_noise": "identify_noise",
            "calculate_relevance": "calculate_relevance",
            "filter_items": "filter_items",
            "verify_focus": "verify_focus",
            "select_best": "select_best",
            "filter_information": "filter_information",
            "get_info": None,
        },
        "default_action": "filter_information",
    },
    "information_retrieval": {
        "class": "InformationRetriever",
        "actions": {
            "define_need": "define_need",
            "build_search_query": "build_search_query",
            "search": "search",
            "verify_source": "verify_source",
            "extract_relevant_info": "extract_relevant_info",
            "retrieve_and_verify": "retrieve_and_verify",
            "search_information": "search_information",
            "get_info": None,
        },
        "default_action": "search_information",
    },
    "knowledge_synthesis": {
        "class": "KnowledgeSynthesizer",
        "actions": {
            "add_source": "add_source",
            "identify_connections": "identify_connections",
            "resolve_conflicts": "resolve_conflicts",
            "synthesize": "synthesize",
            "build_knowledge_graph": "build_knowledge_graph",
            "synthesize_knowledge": "synthesize_knowledge",
            "get_info": None,
        },
        "default_action": "synthesize_knowledge",
    },
    "logical_reasoning": {
        "class": "LogicalReasoner",
        "actions": {
            "evaluate_syllogism": "evaluate_syllogism",
            "modus_ponens": "modus_ponens",
            "modus_tollens": "modus_tollens",
            "detect_fallacy": "detect_fallacy",
            "evaluate_argument": "evaluate_argument",
            "create_syllogism": "create_syllogism",
            "get_info": None,
        },
        "default_action": "evaluate_argument",
    },
    "sequential_problem_solving": {
        "class": "SequentialProblemSolver",
        "actions": {
            "create_problem": "create_problem",
            "add_step": "add_step",
            "execute_step": "execute_step",
            "verify_step": "verify_step",
            "get_solution": "get_solution",
            "solve_step_by_step": "solve_step_by_step",
            "get_info": None,
        },
        "default_action": "solve_step_by_step",
    },
    "technique_application": {
        "class": "TechniqueApplicator",
        "actions": {
            "identify_problem_type": "identify_problem_type",
            "select_technique": "select_technique",
            "apply_technique": "apply_technique",
            "verify_result": "verify_result",
            "execute_procedure": "execute_procedure",
            "get_info": None,
        },
        "default_action": "apply_technique",
    },
}


def generate_cognitive_invoke(skill_name, config):
    """Generate invoke() wrapper for a cognitive skill."""
    class_name = config["class"]
    actions = config["actions"]
    default_action = config["default_action"]

    action_cases = []
    for action_name, method_name in actions.items():
        if method_name is None:
            # get_info action
            action_cases.append(
                f'    if action == "{action_name}":\n'
                f'        return {{"result": {{"name": "{skill_name}", "actions": {sorted([a for a in actions if a != "get_info"])} }}, "metadata": {{"action": action, "timestamp": timestamp}}}}'
            )
        else:
            action_cases.append(
                f'    if action == "{action_name}":\n'
                f'        result = getattr(instance, "{method_name}")(**kwargs)\n'
                f'        return {{"result": result if not inspect.isawaitable(result) else asyncio.get_event_loop().run_until_complete(result), "metadata": {{"action": action, "timestamp": timestamp}}}}'
            )

    cases_code = "\n".join(action_cases)

    wrapper = f'''

# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "{default_action}")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {{k: v for k, v in payload.items() if k != "action"}}

    instance = {class_name}()

    if action == "get_info":
        return {{"result": {{"name": "{skill_name}", "actions": {sorted([a for a in actions if a != "get_info"])} }}, "metadata": {{"action": action, "timestamp": timestamp}}}}

    method = getattr(instance, action, None)
    if method is None:
        return {{"result": {{"error": f"Unknown action: {{action}}"}}, "metadata": {{"action": action, "timestamp": timestamp}}}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {{"result": result, "metadata": {{"action": action, "timestamp": timestamp}}}}
'''
    return wrapper


def generate_data_analyzer_invoke():
    """Generate invoke() for data_analyzer (standalone functions)."""
    return '''

# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "analyze")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = ["analyze", "clean", "insights", "get_info"]

    if action == "get_info":
        return {"result": {"name": "data-analyzer", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    if action == "analyze":
        dataset = payload.get("dataset", [])
        if not dataset:
            return {"result": {"error": "No dataset provided"}, "metadata": {"action": action, "timestamp": timestamp}}
        result = analyze_dataset(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    elif action == "clean":
        dataset = payload.get("dataset", [])
        result = clean_data(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    elif action == "insights":
        dataset = payload.get("dataset", [])
        result = generate_insights(dataset)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

    else:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}
'''


def generate_context_hub_invoke():
    """Generate invoke() for context_hub_provider (standalone async functions)."""
    return '''

# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "search")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = ["search", "get_doc", "annotate", "clear_annotation", "get_info"]

    if action == "get_info":
        return {"result": {"name": "context-hub-provider", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    try:
        if action == "search":
            result = await search(query=payload.get("query", ""), tags=payload.get("tags"), limit=payload.get("limit", 20))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "get_doc":
            result = await get_doc(doc_id=payload.get("doc_id", ""), language=payload.get("language"))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "annotate":
            result = await annotate(doc_id=payload.get("doc_id", ""), note=payload.get("note", ""))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "clear_annotation":
            result = await clear_annotation(doc_id=payload.get("doc_id", ""))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action, "timestamp": timestamp}}
'''


def generate_apache_beam_invoke():
    """Generate invoke() for apache_beam_streaming_batch_processing."""
    return '''

# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "create_pipeline")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = [
        "create_pipeline", "configure_options", "create_windowing_strategy",
        "create_aggregation_transform", "run_pipeline", "get_info"
    ]

    if action == "get_info":
        return {"result": {"name": "apache-beam-streaming-batch-processing", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    instance = BatchPipelineBuilder()

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    kwargs = {k: v for k, v in payload.items() if k != "action"}
    result = method(**kwargs)
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
'''


def generate_federated_learning_invoke():
    """Generate invoke() for federated_learning_differential_privacy."""
    return '''

# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "local_train")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = [
        "local_train", "clip_gradients", "add_gaussian_noise",
        "select_clients", "calculate_noise_multiplier", "get_info"
    ]

    if action == "get_info":
        return {"result": {"name": "federated-learning-differential-privacy", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    kwargs = {k: v for k, v in payload.items() if k != "action"}

    # SimpleMLP requires input_dim and hidden_dim
    try:
        instance = SimpleMLP(input_dim=kwargs.pop("input_dim", 10), hidden_dim=kwargs.pop("hidden_dim", 5))
    except Exception as e:
        return {"result": {"error": f"Failed to instantiate SimpleMLP: {e}"}, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    try:
        result = method(**kwargs)
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action, "timestamp": timestamp}}
'''


def find_module_file(name):
    """Find the .py file for a module name."""
    for root, dirs, files in os.walk(SKILLS_ROOT):
        for f in files:
            if f == name + ".py":
                return os.path.join(root, f)
    return None


def add_invoke_to_file(filepath, invoke_code):
    """Append invoke() code to a file if it doesn't already have one."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if "async def invoke(" in content or "def invoke(" in content:
        print(f"  SKIP (already has invoke): {os.path.basename(filepath)}")
        return False

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(invoke_code)

    print(f"  FIXED: {os.path.basename(filepath)}")
    return True


def verify_invoke(filepath):
    """Verify the file can be compiled."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    try:
        compile(content, filepath, "exec")
        return True
    except SyntaxError as e:
        print(f"  SYNTAX ERROR in {os.path.basename(filepath)}: {e}")
        return False


def main():
    fixed = 0
    skipped = 0

    # 1. Fix cognitive skills
    print("Fixing cognitive skills...")
    for skill_name, config in COGNITIVE_SKILLS.items():
        filepath = find_module_file(skill_name)
        if not filepath:
            print(f"  NOT FOUND: {skill_name}")
            skipped += 1
            continue

        invoke_code = generate_cognitive_invoke(skill_name, config)
        if add_invoke_to_file(filepath, invoke_code):
            if verify_invoke(filepath):
                fixed += 1
            else:
                print(f"  VERIFY FAILED: {skill_name}")
                skipped += 1
        else:
            skipped += 1

    # 2. Fix data_analyzer
    print("\nFixing data_analyzer...")
    filepath = find_module_file("data_analyzer")
    if filepath:
        if add_invoke_to_file(filepath, generate_data_analyzer_invoke()):
            if verify_invoke(filepath):
                fixed += 1
    else:
        print("  NOT FOUND: data_analyzer")
        skipped += 1

    # 3. Fix context_hub_provider
    print("\nFixing context_hub_provider...")
    filepath = find_module_file("context_hub_provider")
    if filepath:
        if add_invoke_to_file(filepath, generate_context_hub_invoke()):
            if verify_invoke(filepath):
                fixed += 1
    else:
        print("  NOT FOUND: context_hub_provider")
        skipped += 1

    # 4. Fix apache_beam
    print("\nFixing apache_beam_streaming_batch_processing...")
    filepath = find_module_file("apache_beam_streaming_batch_processing")
    if filepath:
        if add_invoke_to_file(filepath, generate_apache_beam_invoke()):
            if verify_invoke(filepath):
                fixed += 1
    else:
        print("  NOT FOUND: apache_beam_streaming_batch_processing")
        skipped += 1

    # 5. Fix federated_learning
    print("\nFixing federated_learning_differential_privacy...")
    filepath = find_module_file("federated_learning_differential_privacy")
    if filepath:
        if add_invoke_to_file(filepath, generate_federated_learning_invoke()):
            if verify_invoke(filepath):
                fixed += 1
    else:
        print("  NOT FOUND: federated_learning_differential_privacy")
        skipped += 1

    print(f"\n{'=' * 50}")
    print(f"Fixed: {fixed}, Skipped: {skipped}")
    return fixed


if __name__ == "__main__":
    main()
