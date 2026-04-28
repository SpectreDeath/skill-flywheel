% Quantum Logic and Cognitive Constraints in Prolog
% Models quantum-like cognitive processes with logical constraints

% Quantum superposition states
quantum_state(superposition, [state1, state2], amplitude(0.707, 0.707)).
quantum_state(entangled, [cognitive_state, emotional_state], amplitude(0.6, 0.8)).

% Cognitive constraints
cognitive_constraint(complexity_limit, high) :- context('complexity', Value), Value > 0.8.
cognitive_constraint(time_pressure, medium) :- context('time_pressure', Value), Value > 0.6.
cognitive_constraint(uncertainty_threshold, low) :- context('uncertainty', Value), Value < 0.3.

% Quantum inference rules
quantum_inference(collapse_to_decision, 0.85) :- quantum_state(superposition, _, _), evidence_strong.
quantum_inference(maintain_superposition, 0.65) :- quantum_state(superposition, _, _), evidence_weak.
quantum_inference(entangled_reasoning, 0.78) :- quantum_state(entangled, _, _).

% Decision logic under uncertainty
decision_logic(accept_uncertainty, 'optimal_for_exploration') :- uncertainty_high, exploration_valued.
decision_logic(reduce_uncertainty, 'optimal_for_exploitation') :- uncertainty_high, exploitation_needed.
decision_logic(confident_decision, 'direct_action') :- uncertainty_low, evidence_strong.

% Cognitive coherence constraints
coherent_reasoning :- not(contradictory_beliefs), logical_consistency > 0.7.
contradictory_beliefs :- belief(X, P1), belief(X, P2), P1 + P2 > 1.1.

% Quantum measurement analogies
cognitive_measurement(observe_belief, collapse_uncertainty) :- belief_uncertain.
cognitive_measurement(decision_commitment, state_collapse) :- confidence_high.

% Parallel processing constraints
parallel_reasoning_allowed :- cognitive_load < 0.7, time_available.
parallel_reasoning_allowed :- quantum_coherence > 0.8.

% Interference patterns
constructive_interference :- belief_alignment > 0.7, evidence_consistent.
destructive_interference :- belief_conflict > 0.6, evidence_contradictory.

% Quantum-like decision making
quantum_decision(superposition_evaluation) :- multiple_options, uncertainty_present.
quantum_decision(classical_optimization) :- single_optimal_choice, certainty_high.
quantum_decision(entangled_commitment) :- interdependent_choices, complex_constraints.

% Cognitive wave function collapse
collapse_trigger(evidence_threshold, 0.8) :- new_evidence > 0.8.
collapse_trigger(time_constraint, 0.9) :- deadline_approaching.
collapse_trigger(confidence_threshold, 0.75) :- decision_confidence > 0.9.

% Entanglement preservation
preserve_entanglement :- cognitive_coherence_maintained, interference_minimal.
break_entanglement :- measurement_occurred, state_collapsed.

% Helper predicates
evidence_strong :- evidence_strength > 0.8.
evidence_weak :- evidence_strength < 0.4.
uncertainty_high :- uncertainty_level > 0.7.
uncertainty_low :- uncertainty_level < 0.3.
exploration_valued :- context('strategy', 'exploratory').
exploitation_needed :- context('strategy', 'exploitative').
cognitive_load(Value) :- context('load', Value).
time_available :- context('time', 'sufficient').
belief_uncertain :- belief(_, P), P < 0.6.
confidence_high :- decision_confidence > 0.8.
belief_alignment(Value) :- context('alignment', Value).
belief_conflict(Value) :- context('conflict', Value).
new_evidence(Value) :- context('evidence', Value).
deadline_approaching :- context('deadline', 'near').
decision_confidence(Value) :- context('confidence', Value).
cognitive_coherence(Value) :- context('coherence', Value).
measurement_occurred :- context('measurement', 'occurred').
state_collapsed :- context('state', 'collapsed').