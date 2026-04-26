% Belief Revision System - Prolog Surface for Logical Consistency
% Domain: EPISTEMOLOGY

% Check consistency of belief and evidence set
% Input: List of belief/evidence facts, Output: List of conflicts
check_consistency(Facts, Conflicts) :-
    findall((B1,B2), 
            (member(B1, Facts), member(B2, Facts), B1 \= B2, 
             conflicts_with(B1, B2)), 
            RawConflicts),
    % Remove duplicate conflicts (A,B and B,A are the same)
    sort(RawConflicts, Sorted),
    % Remove duplicates where order doesn't matter
    include(\+is_duplicate_conflict, Sorted, Conflicts).

% Two beliefs conflict if they cannot both be true with high confidence
conflicts_with(belief(B1, C1), belief(B2, C2)) :-
    % Extract belief names and confidence values
    belief_name(B1, Name1),
    belief_name(B2, Name2),
    confidence_value(C1, Conf1),
    confidence_value(C2, Conf2),
    % They conflict if they refer to the same proposition but with incompatible confidence
    (   Name1 == Name2
    ->  % Same proposition: check if confidences are incompatible
        (   Conf1 > 0.8, Conf2 < 0.2
        ;   Conf1 < 0.2, Conf2 > 0.8
        ;   % One is very confident true, other very confident false
        false
        )
    ;   % Different propositions: check for logical contradiction
        contradicts(Name1, Name2)
    ).

% Extract belief name from fact
belief_name(belief(Name, _), Name).
belief_name(evidence(Name, _), Name).

% Extract confidence value from fact
confidence_value(confidence(_, Conf), Conf).
confidence_value(belief(_, Conf), Conf).
confidence_value(evidence(_, Conf), Conf).

% Define contradictions between propositions
contradicts('P', 'not_P').
contradicts('not_P', 'P').
contradicts('X_is_true', 'X_is_false').
contradicts('X_is_false', 'X_is_true').
contradicts('A_causes_B', 'A_prevents_B').
contradicts('A_prevents_B', 'A_causes_B').

% Helper to check if two conflicts are duplicates (order-independent)
is_duplicate_conflict(Conf1-Conf2) :-
    member(Conf2-Conf1, [Conf1-Conf2]), !, fail.
is_duplicate_conflict(_).

% Suggest belief revision strategy based on confidence distribution
suggest_revision_strategy(Facts, Strategy) :-
    % Extract all confidence values
    findall(Conf, (member(Fact, Facts), confidence_value(Fact, Conf)), Confidences),
    % Calculate statistics
    mean(Confidences, MeanConf),
    std_dev(Confidences, StdDev),
    % Determine strategy based on distribution
    (   MeanConf > 0.7, StdDev < 0.2
    ->  Strategy = 'confirmatory'  % High confidence, low variance
    ;   MeanConf < 0.3, StdDev < 0.2
    ->  Strategy = 'skeptical'     % Low confidence, low variance
    ;   StdDev > 0.4
    ->  Strategy = 'exploratory'   % High variance
    ;   MeanConf > 0.6
    ->  Strategy = 'conservative'  % Moderately high confidence
    ;   MeanConf < 0.4
    ->  Strategy = 'aggressive'    % Low confidence
    ;   true
    ->  Strategy = 'balanced'      % Default case
    ).

% Statistical helpers
mean(List, Mean) :-
    sum(List, Sum),
    length(List, Length),
    Mean is Sum / Length.

sum([], 0).
sum([H|T], Sum) :-
    sum(T, Rest),
    Sum is H + Rest.

std_dev(List, StdDev) :-
    mean(List, Mean),
    sum_of_squares_diff(List, Mean, SumDiff),
    length(List, Length),
    Length > 0,
    Variance is SumDiff / Length,
    StdDev is sqrt(Variance).

sum_of_squares_diff([], _, 0).
sum_of_squares_diff([H|T], Mean, SumDiff) :-
    sum_of_squares_diff(T, Mean, Rest),
    Diff is H - Mean,
    SumDiff is Diff*Diff + Rest.

% Extract beliefs that need revision based on evidence conflicts
beliefs_to_revise(Facts, NewEvidence, ToRevise) :-
    % For each belief, check if new evidence contradicts it significantly
    findall(Belief, 
            (   member(belief(BeliefName, Conf), Facts),
                member(evidence(EvidName, EvidConf), NewEvidence),
                % Check if they're related and conflicting
                related_propositions(BeliefName, EvidName),
                confidence_conflicts(Conf, EvidConf)
            ),
            Belief).

% Check if two propositions are related (simplified)
related_propositions(Prop1, Prop2) :-
    % Same base name ignoring negation
    strip_negation(Prop1, Base1),
    strip_negation(Prop2, Base2),
    Base1 == Base2.

strip_negation(not_P, P) :- !.
strip_negation(Prop, Prop).

% Check if confidence values significantly conflict
confidence_conflicts(C1, C2) :-
    % One is high (>0.8), other is low (<0.2)
    (   C1 > 0.8, C2 < 0.2
    ;   C1 < 0.2, C2 > 0.8
    ).