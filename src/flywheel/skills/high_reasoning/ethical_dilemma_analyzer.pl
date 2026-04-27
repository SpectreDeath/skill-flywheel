% Ethical Frameworks in Prolog
% Deontological, Utilitarian, Virtue Ethics, and Care Ethics frameworks

% Scenario and stakeholder facts (asserted dynamically)
% scenario(Description).
% stakeholder(Name).

% Ethical principles
principle('autonomy', 'respect for individual rights and self-determination').
principle('beneficence', 'maximize good outcomes').
principle('non-maleficence', 'avoid causing harm').
principle('justice', 'fair distribution of benefits and burdens').

% Deontological rules - duty-based ethics
deontological_permissible_actions(Action) :-
    respects_principles(Action),
    not violates_rights(Action).

respects_principles('tell_truth') :- scenario(_).
respects_principles('keep_promise') :- scenario(_).
respects_principles('respect_autonomy') :- stakeholder(_).

violates_rights('lie_to_save_life') :- scenario(_).
violates_rights('break_confidentiality') :- stakeholder(_).

% Utilitarian rules - maximize overall happiness
utilitarian_optimal_action(Action) :-
    maximizes_net_happiness(Action),
    minimizes_harm(Action).

maximizes_net_happiness('help_majority') :- stakeholder_count(N), N > 3.
maximizes_net_happiness('prevent_greater_harm') :- scenario(_).

minimizes_harm('minimize_casualties') :- stakeholder(_).
minimizes_harm('preserve_relationships') :- stakeholder(_).

% Virtue ethics - character-based reasoning
virtue_based_recommendations(Action) :-
    demonstrates_virtue(Action, Virtue),
    Virtue \= 'cowardice'.

demonstrates_virtue('act_bravely', 'courage').
demonstrates_virtue('show_compassion', 'empathy').
demonstrates_virtue('act_fairly', 'justice').
demonstrates_virtue('be_honest', 'integrity').

% Care ethics - relationship and context focused
care_ethics_relationships(Action) :-
    preserves_relationships(Action),
    considers_context(Action).

preserves_relationships('maintain_trust') :- stakeholder(_).
preserves_relationships('show_empathy') :- stakeholder(_).

considers_context('understand_perspectives') :- scenario(_).
considers_context('weigh_consequences') :- stakeholder(_).

% Stakeholder counting for utilitarian analysis
stakeholder_count(Count) :- aggregate(count, stakeholder(_), Count).

% Ethical dilemma patterns
dilemma_pattern('trolley_problem', 'sacrifice_one_to_save_many').
dilemma_pattern('organ_donation', 'allocation_of_scarce_resources').
dilemma_pattern('truth_telling', 'honesty_vs_harm_prevention').

% Framework compatibility analysis
compatible_frameworks(utilitarianism, care_ethics).
compatible_frameworks(deontology, virtue_ethics).
conflicting_frameworks(utilitarianism, deontology).