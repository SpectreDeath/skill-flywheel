% Uncertainty Analysis Logic in Prolog
% Belief revision, uncertainty propagation, and decision-making under uncertainty

% Belief revision frameworks (Doyle, AGM theory)
belief_revision(Belief, NewStrength, 'evidence_conflict') :-
    belief(Belief, OldStrength),
    evidence_conflicts(Belief, Evidence),
    revise_belief_agm(Belief, Evidence, NewStrength),
    abs(OldStrength - NewStrength) > 0.3.

belief_revision(Belief, NewStrength, 'new_evidence') :-
    belief(Belief, OldStrength),
    new_evidence(Belief, EvidenceStrength),
    bayesian_update(OldStrength, EvidenceStrength, NewStrength).

belief_revision(Belief, NewStrength, 'consistency_restoration') :-
    belief(Belief, OldStrength),
    inconsistent_beliefs(Belief, OtherBeliefs),
    restore_consistency(Belief, OtherBeliefs, NewStrength).

% Bayesian belief updating
bayesian_update(Prior, Likelihood, Posterior) :-
    Posterior is (Prior * Likelihood) / ((Prior * Likelihood) + ((1 - Prior) * (1 - Likelihood))).

% Uncertainty propagation
uncertainty_propagation(Source, Target, 'high') :-
    uncertainty_source(Source),
    directly_affects(Source, Target),
    uncertainty_level(Source, high).

uncertainty_propagation(Source, Target, 'medium') :-
    uncertainty_source(Source),
    indirectly_affects(Source, Target),
    uncertainty_level(Source, medium).

uncertainty_propagation(Source, Target, 'low') :-
    uncertainty_source(Source),
    weakly_affects(Source, Target),
    uncertainty_level(Source, low).

% Decision thresholds under uncertainty
decision_threshold('accept_risk', 0.8, 'high_confidence_required') :-
    scenario(_),
    high_stakes_decision.

decision_threshold('gather_more_info', 0.6, 'uncertainty_too_high') :-
    scenario(_),
    uncertainty_level(_, high).

decision_threshold('implement_hedge', 0.4, 'balance_risk_return') :-
    scenario(_),
    risk_return_tradeoff.

% Risk assessment categories
risk_category(Scenario, 'high_risk', Probability) :-
    scenario(Scenario),
    count_uncertainty_sources(Count),
    Count > 5,
    Probability is 0.8.

risk_category(Scenario, 'medium_risk', Probability) :-
    scenario(Scenario),
    count_uncertainty_sources(Count),
    Count >= 3, Count =< 5,
    Probability is 0.5.

risk_category(Scenario, 'low_risk', Probability) :-
    scenario(Scenario),
    count_uncertainty_sources(Count),
    Count < 3,
    Probability is 0.2.

% Evidence evaluation
evidence_strength(Evidence, 'strong') :- reliable_source(Evidence), consistent_history(Evidence).
evidence_strength(Evidence, 'moderate') :- reliable_source(Evidence), not(consistent_history(Evidence)).
evidence_strength(Evidence, 'weak') :- not(reliable_source(Evidence)).

% Belief consistency checking
consistent_beliefs :- not(contradictory_beliefs(_, _)).
contradictory_beliefs(Belief1, Belief2) :-
    belief(Belief1, S1), belief(Belief2, S2),
    mutually_exclusive(Belief1, Belief2),
    S1 > 0.5, S2 > 0.5.

% Uncertainty quantification
uncertainty_measure('epistemic', Value) :- belief_uncertainty(Value).
uncertainty_measure('aleatoric', Value) :- inherent_randomness(Value).

% Decision robustness
robust_decision(Decision) :-
    belief(Decision, Strength),
    Strength > 0.7,
    not(high_uncertainty_sources).

robust_decision(Decision) :-
    belief(Decision, Strength),
    Strength > 0.5,
    has_hedging_strategies(Decision).

% Counterfactual reasoning
counterfactual_impact(Action, Outcome, Probability) :-
    action(Action),
    possible_outcome(Action, Outcome),
    outcome_probability(Outcome, Probability).

% Value of information analysis
voi_decision('gather_info', Value) :- expected_value_with_info(Value1), expected_value_without_info(Value2), Value is Value1 - Value2.

% Helper predicates
count_uncertainty_sources(Count) :- aggregate(count, uncertainty_source(_), Count).

directly_affects(X, Y) :- causes(X, Y).
indirectly_affects(X, Z) :- causes(X, Y), causes(Y, Z), X \= Z.
weakly_affects(X, Y) :- correlated(X, Y), not(causes(X, Y)), not(causes(Y, X)).

uncertainty_level(Source, high) :- critical_uncertainty(Source).
uncertainty_level(Source, medium) :- important_uncertainty(Source).
uncertainty_level(Source, low) :- minor_uncertainty(Source).

high_stakes_decision :- involves_safety, or involves_large_investment.
risk_return_tradeoff :- uncertain_outcomes, potential_high_returns.

reliable_source(Evidence) :- peer_reviewed(Evidence), recent(Evidence).
consistent_history(Evidence) :- multiple_confirmations(Evidence).

mutually_exclusive(B1, B2) :- contradicts(B1, B2).

belief_uncertainty(Value) :- Value is 0.3.  % Placeholder
inherent_randomness(Value) :- Value is 0.2.  % Placeholder

high_uncertainty_sources :- count_uncertainty_sources(C), C > 3.
has_hedging_strategies(Action) :- exists_backup_plan(Action).

action(Action) :- belief(Action, _).
possible_outcome(Action, Outcome) :- belief(Outcome, _).
outcome_probability(Outcome, Prob) :- belief(Outcome, Prob).

expected_value_with_info(Value) :- Value is 100.  % Placeholder
expected_value_without_info(Value) :- Value is 80.  % Placeholder