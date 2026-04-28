% Logical Data Fusion in Prolog
% Constraint satisfaction, conflict resolution, and knowledge integration

% Entity and relationship facts (asserted dynamically)
% entity(Entity)
% entity_attribute(Entity, Attribute, Value)
% relationship(From, To, Type)

% Consistency checking
consistent_entity(Entity) :-
    entity(Entity),
    not(has_conflicting_attributes(Entity)).

consistent_relationship(From, To, Type) :-
    relationship(From, To, Type),
    entity(From), entity(To),
    not(contradictory_relationship(From, To, Type)).

has_conflicting_attributes(Entity) :-
    entity_attribute(Entity, Attr, Value1),
    entity_attribute(Entity, Attr, Value2),
    Value1 \= Value2.

contradictory_relationship(From, To, Type) :-
    relationship(From, To, OtherType),
    Type \= OtherType,
    mutually_exclusive_types(Type, OtherType).

mutually_exclusive_types('friend', 'enemy').
mutually_exclusive_types('parent', 'child').

% Constraint satisfaction
constraint_satisfied(Constraint) :-
    atom_string(ConstraintAtom, Constraint),
    call(ConstraintAtom).

% Conflict resolution
conflicting_entities(E1, E2, Attribute) :-
    entity_attribute(E1, Attribute, Value1),
    entity_attribute(E2, Attribute, Value2),
    Value1 \= Value2,
    similar_entities(E1, E2).

resolution_strategy(Conflict, 'merge_with_majority') :-
    conflict_votes(Conflict, Votes),
    majority_vote(Votes, Winner),
    Winner \= 'tie'.

resolution_strategy(Conflict, 'keep_both_entities') :-
    conflict_votes(Conflict, Votes),
    majority_vote(Votes, 'tie').

resolution_strategy(Conflict, 'manual_resolution_required') :-
    high_stakes_conflict(Conflict).

merged_entity(E1, E2, Merged) :-
    resolution_strategy(conflict(E1, E2, _), 'merge_with_majority'),
    merge_attributes(E1, E2, Merged).

% Knowledge integration
integrated_fact(Fact, Confidence) :-
    consistent_fact(Fact),
    supporting_evidence(Fact, EvidenceCount),
    Confidence is min(1.0, EvidenceCount / 3).

inferred_relationship(From, To, Type, 'transitive_closure') :-
    relationship(From, Intermediate, Type),
    relationship(Intermediate, To, Type),
    From \= To, Intermediate \= To.

inferred_relationship(From, To, 'inverse', InverseType) :-
    relationship(To, From, OriginalType),
    inverse_relationship(OriginalType, InverseType).

knowledge_consistent :-
    not(inconsistent_knowledge(_, _)).

inconsistent_knowledge(Fact1, Fact2) :-
    integrated_fact(Fact1, C1), integrated_fact(Fact2, C2),
    contradicts(Fact1, Fact2),
    C1 > 0.7, C2 > 0.7.

% Helper predicates
similar_entities(E1, E2) :- shared_attributes(E1, E2, Count), Count > 2.

shared_attributes(E1, E2, Count) :-
    findall(Attr, (entity_attribute(E1, Attr, V1), entity_attribute(E2, Attr, V2), V1 = V2), Shared),
    length(Shared, Count).

conflict_votes(conflict(E1, E2, Attr), [V1, V2]) :- entity_attribute(E1, Attr, V1), entity_attribute(E2, Attr, V2).

majority_vote([V, V], V).
majority_vote([V1, V2], 'tie') :- V1 \= V2.

high_stakes_conflict(conflict(E1, E2, safety)) :- entity_attribute(E1, 'type', 'safety_critical').

merge_attributes(E1, E2, Merged) :- Merged = merged(E1, E2).

consistent_fact(Fact) :- entity(Fact) ; relationship(_, _, Fact).

supporting_evidence(Fact, Count) :- evidence_count(Fact, Count).

evidence_count(Fact, 1) :- entity_attribute(Fact, _, _).
evidence_count(Fact, Count) :- relationship(Fact, _, _), Count = 2.

contradicts(Fact1, Fact2) :- mutually_exclusive(Fact1, Fact2).

mutually_exclusive(Fact1, Fact2) :- contradicts(Fact1, Fact2).

inverse_relationship('parent', 'child').
inverse_relationship('friend', 'friend').
inverse_relationship('manages', 'managed_by').

% Belief fusion
fused_belief(Belief, FusedConfidence) :-
    findall(C, belief_confidence(Belief, C), Confidences),
    average_confidence(Confidences, FusedConfidence).

belief_confidence(Belief, Confidence) :- entity_attribute(Belief, 'confidence', Confidence).

average_confidence(List, Average) :- sum_list(List, Sum), length(List, Len), Average is Sum / Len.

% Uncertainty handling
uncertain_fact(Fact, Uncertainty) :-
    integrated_fact(Fact, Confidence),
    Uncertainty is 1.0 - Confidence.

high_uncertainty_fact(Fact) :- uncertain_fact(Fact, U), U > 0.5.

requires_investigation(Fact) :- high_uncertainty_fact(Fact), critical_fact(Fact).

critical_fact(Fact) :- entity_attribute(Fact, 'importance', 'high').

% Decision support
decision_recommendation(Action, 'proceed') :-
    required_facts_satisfied(Action),
    no_high_uncertainty_facts(Action).

decision_recommendation(Action, 'investigate_further') :-
    has_uncertain_facts(Action).

decision_recommendation(Action, 'reconsider') :-
    has_contradictory_facts(Action).

required_facts_satisfied(Action) :- forall(required_fact(Action, Fact), integrated_fact(Fact, _)).

has_uncertain_facts(Action) :- required_fact(Action, Fact), uncertain_fact(Fact, _).

has_contradictory_facts(Action) :- inconsistent_knowledge(_, _).