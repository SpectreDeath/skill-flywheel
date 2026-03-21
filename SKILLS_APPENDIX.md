# Appendix: Epistemology Skills Rationale and Usage Examples

## Skill: Knowledge Verification and Justification (epist-001)

### Rationale
This skill addresses the foundational epistemological problem of distinguishing genuine knowledge from mere justified true belief (JTB). Drawing from the Stanford Encyclopedia of Philosophy (SEP) and Internet Encyclopedia of Philosophy (IEP), it implements responses to the Gettier problem, which demonstrated that JTB is insufficient for knowledge. For AI agents, this skill is essential because it provides a rigorous framework for evaluating whether the agent's beliefs constitute actual knowledge, enabling more reliable epistemic claims and preventing overconfident conclusions. The skill uses foundationalist structure combined with defeasibility conditions to block Gettier-style counterexamples.

### Usage Example
```json
{
  "input": {
    "proposition": "The temperature outside is 72°F",
    "belief_state": {
      "held": true,
      "confidence": 0.85
    },
    "truth_value": true,
    "justification_source": "perception",
    "defeaters_present": false,
    "process_reliability": 0.92
  },
  "expected_output": {
    "is_knowledge": true,
    "justification_status": "justified",
    "gettier_safe": true,
    "epistemic_luck_mitigated": true,
    "justification_type": "foundationalist"
  }
}
```

## Skill: Bayesian Evidence Updating (epist-002)

### Rationale
This skill implements the Bayesian approach to epistemology as detailed in the SEP's Bayesian Epistemology entry. It provides a mathematically rigorous framework for rationally updating degrees of belief (credences) in response to evidence using Bayes' theorem while maintaining probabilistic coherence. For AI agents, Bayesian reasoning is crucial because it provides a normative standard for how evidence should change beliefs, enabling calibrated uncertainty quantification and preventing dogmatic or arbitrary belief revision. The skill addresses the problem of old evidence and provides foundations based on accuracy-dominance and Dutch Book arguments.

### Usage Example
```json
{
  "input": {
    "prior_credences": {
      "H1_healthy_heart": 0.7,
      "H2_heart_condition_A": 0.2,
      "H3_heart_condition_B": 0.1
    },
    "new_evidence": "Patient shows elevated troponin levels",
    "likelihoods": {
      "H1_healthy_heart": 0.05,
      "H2_heart_condition_A": 0.85,
      "H3_heart_condition_B": 0.90
    }
  },
  "expected_output": {
    "posterior_credences": {
      "H1_healthy_heart": 0.157,
      "H2_heart_condition_A": 0.724,
      "H3_heart_condition_B": 0.119
    },
    "confirmation_strength": {
      "H1_healthy_heart": 0.224,
      "H2_heart_condition_A": 3.62,
      "H3_heart_condition_B": 1.19
    },
    "coherence_maintained": true
  }
}
```

## Skill: Social Testimony and Epistemic Trust (epist-003)

### Rationale
This skill implements the epistemology of testimony as presented in the SEP's Social Epistemology entry. It addresses how agents should evaluate beliefs derived from others' assertions, handling the reductionist vs anti-reductionist debate about testimony. For AI agents, this is critical in contexts involving human-provided information, misinformation detection, and collaborative knowledge formation. The skill models rational responses to peer disagreement and group belief aggregation, enabling agents to navigate social epistemic environments responsibly.

### Usage Example
```json
{
  "input": {
    "testimony_content": "The new drug has completed Phase III trials with 95% efficacy",
    "speaker_info": {
      "expertise": 0.9,
      "honesty": 0.85,
      "accuracy_history": 0.88
    },
    "listener_background": {
      "background_knowledge": ["basic pharmacology", "clinical trial phases"],
      "independent_evidence": false
    },
    "peer_disagreement": {
      "peer_credence": 0.3,
      "peer_evidence": "I read that sample size was only 200 participants",
      "is_peer": true
    }
  },
  "expected_output": {
    "testimonial_justification": "justified",
    "disagreement_response": "concede",
    "group_aggregated_belief": {
      "aggregated_credence": 0.625,
      "confidence": "moderate"
    },
    "trust_level": 0.72
  }
}
```

## Skill: Intentional Action Recognition (agency-001)

### Rationale
This skill implements the standard theory of agency from the SEP's Agency entry, based on the Anscombe-Davidson framework. It enables agents to distinguish genuine intentional actions from mere behaviors, analyze the mental states (desires, beliefs, intentions) that ground agency, and detect deviant causal chains. For AI agents, this skill is essential for understanding both human behavior (for interaction and assistance) and their own action attribution, ensuring that outputs are attributable to genuine agency rather than accidental outcomes.

### Usage Example
```json
{
  "input": {
    "event_description": "Agent scheduled a meeting for 3pm",
    "agent_mental_states": {
      "desires": ["coordinate team availability", "complete project on time"],
      "beliefs": ["meeting needed for project sync", "team members available at 3pm"],
      "intentions": ["schedule weekly sync meeting"]
    },
    "causal_history": [
      "identified project delay risk",
      "believed meeting would mitigate risk",
      "formed intention to schedule",
      "executed scheduling action"
    ],
    "context": "collaborative project management"
  },
  "expected_output": {
    "is_action": true,
    "is_intentional": true,
    "reason_explanation_available": true,
    "causal_deviance_risk": false,
    "agency_type": "intentional"
  }
}
```

## Skill: Practical Reasoning and Goal-Directed Planning (agency-002)

### Rationale
This skill implements practical reasoning following the SEP's treatment of Practical Reason and Agency. It enables agents to convert goals (ends) into action plans through instrumental rationality, managing means-end coherence and handling the relationship between desires, beliefs, and actions. For AI agents, this skill is foundational for autonomous behavior—enabling the agent to not only receive goals but intelligently determine how to achieve them while maintaining coherence and detecting akrasia (weakness of will).

### Usage Example
```json
{
  "input": {
    "agent_ends": [
      {"goal": "submit report by Friday", "priority": 1},
      {"goal": "maintain work-life balance", "priority": 2}
    ],
    "available_means": [
      "work_overtime_thursday",
      "delegate_partial_tasks",
      "request_extension",
      "prioritize_critical_sections"
    ],
    "beliefs_about_world": {
      "current_progress": "60%",
      "available_hours": 16,
      "colleague_availability": true
    },
    "preferences": {
      "work_overtime_thursday": -0.3,
      "delegate_partial_tasks": 0.7,
      "request_extension": -0.1,
      "prioritize_critical_sections": 0.8
    }
  },
  "expected_output": {
    "recommended_actions": [
      "prioritize_critical_sections",
      "delegate_partial_tasks"
    ],
    "plan_structure": {
      "phase_1": "identify critical sections (30 min)",
      "phase_2": "complete critical sections (8 hours)",
      "phase_3": "delegate non-critical to colleague (15 min)"
    },
    "instrumental_coherence": true,
    "akrasia_risk": false,
    "means_end_analysis": {
      "primary_goal_feasible": true,
      "secondary_goal_preserved": true
    }
  }
}
```

## Skill: Knowledge-How Recognition (agency-003)

### Rationale
This skill implements the epistemology of knowledge-how as presented in the SEP's Knowledge How entry, addressing the intellectualist vs anti-intellectualist debate about whether knowing how to do something reduces to knowing that something is the case. For AI agents, this skill is crucial for capability assessment—distinguishing between agents that merely have propositional knowledge versus those that can actually perform tasks, and recognizing when ability has been lost or degraded (e.g., in transfer learning scenarios).

### Usage Example
```json
{
  "input": {
    "subject": "ChessAI_Model_v2",
    "skill_claim": "knowing how to play chess at grandmaster level",
    "demonstrated_ability": true,
    "propositional_knowledge": {
      "knows_opening_theory": true,
      "knows_tactical_patterns": true,
      "knows_endgame_principles": true,
      "can_explain_reasoning": false
    },
    "circumstances": {
      "time_control": "classical",
      "opponent_rating": 2700,
      "hardware_available": "high_compute"
    },
    "performance_context": "competitive chess match"
  },
  "expected_output": {
    "has_knowledge_how": true,
    "knowledge_type": "propositional_based",
    "general_ability": true,
    "circumstantial_ability": true,
    "intellectualist_analysis": {
      "sufficient_propositional_knowledge": true,
      "ability_explained_by_knowledge_that": true
    },
    "anti_intellectualist_analysis": {
      "dispositional_element_present": true,
      "ability_extends_beyond_propositional": false
    }
  }
}
```

## Skill: Reliabilist Justification Assessment (logic-001)

### Rationale
This skill implements process reliabilism as discussed in the IEP's Reliabilism entry and SEP's Epistemology. It evaluates whether beliefs are justified based on whether they were formed by reliable (truth-conducive) processes. For AI agents, this provides an externalist justification framework that complements internalist approaches—enabling agents to assess whether their information sources and inference methods are reliably producing true beliefs, addressing challenges like the barn facade case and the generality problem.

### Usage Example
```json
{
  "input": {
    "belief": "The object in front of me is a barn",
    "formation_process": {
      "process_type": "perception",
      "process_description": "visual perception in normal lighting conditions",
      "reliability_estimate": 0.95,
      "input_beliefs": []
    },
    "truth_value": false,
    "alternative_processes_available": [
      "tactile_examination",
      "measurement_instrument"
    ],
    "normal_worlds_consistency": false
  },
  "expected_output": {
    "is_justified": false,
    "process_reliability": 0.95,
    "justification_type": "basic",
    "generality_problem_applies": true,
    "alternative_assessment": {
      "has_alternative_reliable": true,
      "should_have_inquired": true,
      "reliability_normal_worlds": 0.95,
      "reliability_actual": 0.001
    }
  }
}
```

## Skill: Formal Logic Systems (logic-002)

### Rationale
This skill implements formal logical systems from the Open Logic Project, covering propositional logic, first-order predicate logic, and meta-logic principles. It provides both syntactic (proof-theoretic) and semantic approaches to argument evaluation. For AI agents, formal logic is the foundation of rigorous reasoning—enabling sound inference, proof construction, validity checking, and counterexample identification. This skill is essential for any task requiring deductive reasoning, argument analysis, or systematic error detection.

### Usage Example
```json
{
  "input": {
    "argument": {
      "premises": [
        "All humans are mortal",
        "Socrates is human",
        "If all humans are mortal then Socrates is mortal"
      ],
      "conclusion": "Socrates is mortal"
    },
    "logical_system": "propositional",
    "proof_method": "natural_deduction"
  },
  "expected_output": {
    "valid": true,
    "proof": {
      "steps": [
        {"line": 1, "formula": "∀x(Human(x) → Mortal(x))", "justification": "Premise"},
        {"line": 2, "formula": "Human(Socrates)", "justification": "Premise"},
        {"line": 3, "formula": "Human(Socrates) → Mortal(Socrates)", "justification": "Universal Instantiation from 1"},
        {"line": 4, "formula": "Mortal(Socrates)", "justification": "Modus Ponens from 2, 3"}
      ],
      "conclusion_supported": true
    },
    "counterexample": null,
    "logical_analysis": {
      "form": "universal_instantiation_modus_ponens",
      "validity_justification": "truth-functionally valid"
    }
  }
}
```

## Skill: Epistemic Evaluation Synthesis (epist-004)

### Rationale
This meta-skill integrates multiple epistemological frameworks (internalist, externalist, social, and Bayesian) to evaluate complex epistemic situations that require simultaneous assessment using different approaches. Drawing from multiple SEP and IEP sources, it provides a unified evaluation framework that can weight different considerations appropriately. For AI agents, this skill is essential for handling real-world epistemic complexity—where a single framework is insufficient, such as evaluating testimony-based beliefs that also require reliability assessment and Bayesian updating when new evidence arrives.

### Usage Example
```json
{
  "input": {
    "epistemic_situation": {
      "belief": "Climate change is primarily human-caused",
      "formation_method": "scientific_testimony",
      "speaker_source": "IPCC_report",
      "current_credence": 0.85,
      "new_evidence": "Recent study shows 99.9% correlation between CO2 and temperature over 800k years",
      "peer_context": {
        "disagreement_present": true,
        "peer_position": "natural_cycle_variation",
        "peer_expertise": "climate_skeptic_scientist"
      }
    },
    "applicable_frameworks": [
      "internalist_justification",
      "reliabilist_justification",
      "bayesian_updating",
      "social_testimony"
    ],
    "context": {
      "decision_relevance": "policy_formation",
      "stakes": "high",
      "time_horizon": "long_term"
    }
  },
  "expected_output": {
    "synthesis_assessment": {
      "internalist_justification": "strong",
      "reliability_score": 0.94,
      "bayesian_confirmation": 1.45,
      "testimonial_justification": "justified",
      "overall_epistemic_status": "well_justified_belief"
    },
    "framework_weightings": {
      "internalist": 0.25,
      "reliabilist": 0.30,
      "bayesian": 0.25,
      "social_testimony": 0.20
    },
    "overall_justification": "The belief is strongly supported across all frameworks. Scientific testimony from authoritative sources combined with independent evidence and high process reliability converge on high confidence.",
    "recommendations": [
      "Update credence to 0.95 given new Bayesian evidence",
      "Consider addressing peer disagreement with additional evidence",
      "Document justification for transparency"
    ]
  }
}
```
