# High Reasoning Skills - Modular Mind Architecture
# Skills in this directory use multi-surface reasoning:
# - Prolog for symbolic/logical reasoning
# - Hy (Lisp) for heuristic/adaptive strategies
# - Datalog for relational knowledge modeling
# - Python for orchestration and integration

from .sat_solver_optimization import register_skill as register_sat_solver
from .belief_revision import register_skill as register_belief_revision
from .bayesian_networks import register_skill as register_bayesian_networks
from .knowledge_graph import register_skill as register_knowledge_graph
from .ethical_dilemma_analyzer import register_skill as register_ethical_dilemma_analyzer
from .strategic_game_analyzer import register_skill as register_strategic_game_analyzer
from .resource_optimizer import register_skill as register_resource_optimizer
from .causal_inference_engine import register_skill as register_causal_inference_engine
from .adaptive_planner import register_skill as register_adaptive_planner
from .uncertainty_analyzer import register_skill as register_uncertainty_analyzer