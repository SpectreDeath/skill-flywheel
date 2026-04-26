% Bayesian Network Reasoning - Prolog Surface for Probabilistic Logic
% Domain: PROBABILISTIC_MODELS

% Check if two variables are d-separated given evidence
% d_separated(X, Y, EvidenceSet, Independent) - true if X and Y are independent given EvidenceSet
d_separated(X, Y, Evidence, Independent) :-
    % For simplicity in this implementation, we'll check if there's no active path
    % between X and Y given Evidence
    \+ active_path(X, Y, Evidence, _),
    Independent = true.

% Active path exists if there's a path where all colliders are "activated"
% and all non-colliders are not in evidence
active_path(X, Y, Evidence, Path) :-
    findall(Path, path_between(X, Y, Path), AllPaths),
    member(ActivePath, AllPaths),
    path_is_active(ActivePath, Evidence, true),
    Path = ActivePath.

% Find any undirected path between two nodes (ignoring edge direction initially)
path_between(X, Y, Path) :-
    path_between_helper(X, Y, [X], Path).

path_between_helper(X, Y, Visited, [X|Path]) :-
    X \= Y,
    (edge(X, Z); edge(Z, X)),  % Edge can go either direction
    \+ member(Z, Visited),
    path_between_helper(Z, Y, [Z|Visited], Path).
path_between_helper(X, Y, _, [Y]) :- X = Y.

% Check if a path is active given evidence
% A path is active if:
% 1. No non-collider node is in evidence
% 2. Every collider node either is in evidence or has a descendant in evidence
path_is_active([], _, true).
path_is_active([_], _, true).
path_is_active([X,Y,Z|Rest], Evidence, Active) :-
    % Check if Y is a collider on this path: X -> Y <- Z
    (   (edge(X,Y), edge(Z,Y))  % X -> Y <- Z
    ;   (edge(Y,X), edge(Y,Z))  % X <- Y -> Z  (not a collider)
    ;   (edge(X,Y), edge(Y,Z))  % X -> Y -> Z  (not a collider)
    ;   (edge(Y,X), edge(Z,Y))  % X <- Y <- Z  (not a collider)
    ),
    % Y is a collider if both edges point TO Y
    (   (edge(X,Y), edge(Z,Y))  % X -> Y <- Z (collider)
    ->  % If collider, it's active if Y or its descendant is in evidence
        (   member(Y, Evidence)
        ;   has_descendant_in_evidence(Y, Evidence)
        )
    ;   % If not collider, it's active only if Y is NOT in evidence
        \+ member(Y, Evidence)
    ),
    path_is_active([Y,Z|Rest], Evidence, Active).

% Has a descendant in evidence (simplified - would need full traversal in practice)
has_descendant_in_evidence(Node, Evidence) :-
    (edge(Node, Desc); edge(Desc, Node)),
    member(Desc, Evidence).
has_descendant_in_evidence(Node, Evidence) :-
    (edge(Node, Desc); edge(Desc, Node)),
    has_descendant_in_evidence(Desc, Evidence).

% Find Markov blanket of a variable: parents, children, and children's other parents
markov_blanket(Variable, MB) :-
    findall(Member, (markov_blanket_member(Variable, Member); member(Member, EvidenceFacts)), MBList),
    sort(MBList, MB).

markov_blanket_member(Variable, Member) :-
    (   parent_of(Member, Variable)   % Parents
    ;   child_of(Member, Variable)    % Children
    ;   (child_of(Variable, Child), child_of(Member, Child), Member \= Variable)  % Other parents of children
    ).

parent_of(Parent, Child) :- edge(Parent, Child).
child_of(Parent, Child) :- edge(Parent, Child).

% Evidence would come from payload - simplified here
EvidenceFacts = [].


% Variable elimination ordering heuristics based on graph structure
% Variables with fewer connections are better to eliminate early
elimination_score(Variable, Score) :-
    count_neighbors(Variable, NeighborCount),
    Score is NeighborCount.

count_neighbors(Variable, Count) :-
    findall(N, (edge(Variable, N); edge(N, Variable)), Neighbors),
    length(Neighbors, Count).


% Simple conditional independence checker for demonstration
% In reality, this would use d-separation or other causal inference methods
conditionally_independent(Var1, Var2, EvidenceVars) :-
    % For this simplified model, we'll say variables are independent if:
    % 1. They're not directly connected
    % 2. They don't share common children (simplified)
    \+ directly_connected(Var1, Var2),
    \+ shares_common_child(Var1, Var2).

directly_connected(X, Y) :- edge(X, Y).
directly_connected(X, Y) :- edge(Y, X).

shares_common_child(X, Y) :-
    edge(X, Z),
    edge(Y, Z).
shares_common_child(X, Y) :-
    edge(Z, X),
    edge(Z, Y).