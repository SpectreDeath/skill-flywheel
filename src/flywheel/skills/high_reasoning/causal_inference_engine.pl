% Causal Inference Logic in Prolog
% Intervention analysis, counterfactual reasoning, and causal strength

% Causal relationships (loaded dynamically)
% causes(X, Y) - X causes Y
% confounder(X, Y, Z) - Z confounds relationship between X and Y

% Intervention analysis - what happens if we force a variable
intervention_effect(Var, Effect) :-
    causes(Var, Effect),
    not(backdoor_path(Var, Effect, _)).

intervention_effect(Var, 'no_direct_effect') :-
    variable(Var),
    not(causes(Var, _)).

% Counterfactual reasoning - what would have happened
counterfactual(antecedent, consequent) :-
    observed(Variable, Value),
    causes(Variable, consequent),
    format(atom(antecedent), 'if ~w had been different', [Variable]).

% Causal strength assessment
causal_strength(Cause, Effect, 'strong') :-
    causes(Cause, Effect),
    not(confounder(Cause, Effect, _)),
    mediator(Cause, Effect, _).

causal_strength(Cause, Effect, 'weak') :-
    causes(Cause, Effect),
    confounder(Cause, Effect, _).

causal_strength(Cause, Effect, 'spurious') :-
    confounder(Cause, Effect, Confounder),
    causes(Confounder, Effect).

% Backdoor path detection (simplified)
backdoor_path(X, Y, [X, Z, Y]) :-
    causes(X, Z),
    causes(Z, Y),
    not(collider(Z, X, Y)).

backdoor_path(X, Y, [X, Z, W, Y]) :-
    causes(X, Z),
    causes(Z, W),
    causes(W, Y),
    not(collider(Z, X, W)),
    not(collider(W, Z, Y)).

% Collider detection
collider(Var, Parent1, Parent2) :-
    causes(Parent1, Var),
    causes(Parent2, Var).

% Mediation analysis
mediated_effect(Cause, Effect, Mediator) :-
    causes(Cause, Mediator),
    causes(Mediator, Effect).

direct_effect(Cause, Effect) :-
    causes(Cause, Effect),
    not(mediated_effect(Cause, Effect, _)).

% Simpson's paradox detection
simpsons_paradox(X, Y) :-
    causes(X, Y),
    aggregate_group(Group, (observed_group(Group), correlation(Group, X, Y, negative)), NegativeGroups),
    correlation(overall, X, Y, positive),
    length(NegativeGroups, N), N > 0.

% Causal discovery heuristics
likely_causal(X, Y) :-
    correlation(X, Y, strong),
    temporal_order(X, Y),
    not(common_cause(X, Y, _)).

confounded_relationship(X, Y) :-
    correlation(X, Y, _),
    common_cause(X, Y, Z),
    not(causes(X, Y)).

% Experimental design recommendations
needs_randomization(X, Y) :-
    confounder(X, Y, _).

needs_blocking(X, Y, Confounder) :-
    confounder(X, Y, Confounder),
    not(randomizable(Confounder)).

% Causal inference validity checks
valid_estimation(X, Y, Method) :-
    causes(X, Y),
    method_applicable(Method, X, Y),
    not(violates_assumptions(Method, X, Y)).

method_applicable('regression', X, Y) :- causes(X, Y).
method_applicable('instrumental_variables', X, Y) :- has_instrument(X, Y).
method_applicable('difference_in_differences', X, Y) :- panel_data(X, Y).