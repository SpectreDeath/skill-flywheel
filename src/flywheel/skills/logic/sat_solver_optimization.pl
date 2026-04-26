% SAT Solver Optimization - Prolog Surface for Logical Constraints
% Domain: LOGIC

% Validate if a clause set is well-formed and logically processable
valid_clause_set(Clauses, Result) :-
    % Check that we have a list of clauses
    is_list(Clauses),
    % Process each clause to ensure it's valid
    maplist(valid_clause, Clauses, ValidClauses),
    % If all valid, we can proceed
    (   ValidClauses == Clauses
    ->  Result = valid
    ;   Result = needs_simplification
    ).

% Individual clause validation: must be a list of literals
valid_clause([]) :- !, fail.  % Empty clause is unsatisfiable (but valid)
valid_clause([Lit|Lits]) :-
    literal(Lit),
    valid_clause(Lits).

% Literal validation: atom or negated atom
literal(Atom) :-
    atom(Atom).
literal(\+Atom) :-
    atom(Atom).

% Simplify clause set by removing duplicates and tautologies
simplify_clause_set(Original, Simplified) :-
    % Remove duplicate literals within clauses
    maplist(sort, Original, Sorted),
    % Remove duplicate clauses
    sort(Sorted, Unique),
    % Remove tautological clauses (containing both P and ¬P)
    include(\+is_tautology, Unique, Simplified).

% Check if a clause is a tautology (contains complementary literals)
is_tautopia(Clause) :-
    member(Lit, Clause),
    complement(Lit, Lit2),
    member(Lit2, Clause).

complement(A, \+A).
complement(\+A, A).

% Extract variables from clause set for heuristic guidance
extract_variables(Clauses, Variables) :-
    findall(Lit, (member(C, Clauses), member(Lit, C)), AllLiterals),
    maplist(literal_to_variable, AllLiterals, Vars),
    sort(Vars, Variables).

literal_to_variable(V, V) :- atom(V).
literal_to_variable(\+V, V) :- atom(V).

% Suggest branching heuristic: variable with most occurrences
branching_heuristic(Clauses, Variables, SelectedVar) :-
    extract_variables(Clauses, Variables),
    maplist(count_occurrences(Clauses), Variables, Counts),
    pairs_keys_values(VariableCounts, Variables, Counts),
    % Sort by count descending, take first
    sort(2, @=<, VariableCounts, Sorted),
    Sorted = [SelectedVar-_, _|_].

count_occurrences(Clauses, Var, Count) :-
    extract_variables(Clauses, AllVars),
    member(Var, AllVars),
    findall(C, (member(C, Clauses), member(Lit, C), (Lit = Var ; Lit = \+Var)), Matches),
    length(Matches, Count).