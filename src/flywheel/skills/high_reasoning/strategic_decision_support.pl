% Strategic Decision Logic in Prolog
% Decision frameworks and strategic reasoning

% Decision context (asserted dynamically)
% decision_context(Type)

% Decision options and criteria (asserted dynamically)
% decision_option(OptionId)
% decision_criterion(Criterion)

% Decision frameworks
decision_framework('rational_choice', 'optimal_for_simple_decisions') :-
    decision_context('operational'),
    decision_options_count(C), C =< 3.

decision_framework('bounded_rationality', 'practical_for_complex_decisions') :-
    decision_context('strategic'),
    decision_options_count(C), C > 3.

decision_framework('intuitive_judgment', 'useful_for_time_pressure') :-
    decision_context('tactical').

% Strategic considerations
strategic_consideration('long_term_impact', 'high') :-
    decision_context('strategic').

strategic_consideration('stakeholder_alignment', 'critical') :-
    decision_context('organizational').

strategic_consideration('resource_constraints', 'important') :-
    decision_context('operational').

% Constraint satisfaction
constraint_satisfied('budget_limit') :- decision_context('operational').
constraint_satisfied('timeline_requirements') :- decision_context('tactical').
constraint_satisfied('quality_standards') :- decision_context('strategic').

% Decision quality assessment
high_quality_decision(Decision) :-
    decision_framework(Decision, _),
    constraint_satisfied(_),
    strategic_consideration(_, 'high').

medium_quality_decision(Decision) :-
    decision_framework(Decision, _),
    constraint_satisfied(_).

% Risk assessment integration
acceptable_risk(Decision) :- high_quality_decision(Decision).
acceptable_risk(Decision) :- medium_quality_decision(Decision), not(high_risk_context(_)).

high_risk_context('strategic') :- decision_context('strategic').
high_risk_context('organizational') :- decision_context('organizational').

% Helper predicates
decision_options_count(Count) :- findall(O, decision_option(O), Options), length(Options, Count).