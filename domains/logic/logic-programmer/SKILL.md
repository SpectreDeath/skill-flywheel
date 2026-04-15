---
Domain: logic
Version: 1.0.0
Complexity: Intermediate
Type: Process
Category: Development
Estimated Execution Time: 50ms - 2 minutes
name: logic-programmer
---

## Description

General logic programming principles and relational design patterns. Covers fundamental concepts applicable across Prolog dialects (SWI-Prolog, GNU Prolog, etc.), emphasizing declarative problem-solving, unification, backtracking, and data-driven programming.

## Purpose

To provide foundational guidance for logic programming, enabling agents to approach problems from a relational rather than procedural perspective.

## When to Use

- Solving search-based problems
- Knowledge representation and reasoning
- Building rule-based systems
- Parsing and grammar development
- Constraint satisfaction problems

## When NOT to Use

- When procedural solution is simpler
- Performance-critical code requiring imperative optimization
- Tasks not involving logical inference

## Input Format

```yaml
logic_request:
  action: "solve|design|explain|optimize"
  problem: string        # Problem description
  constraints: array     # Domain constraints
  approach: string       # Preferred approach
```

## Output Format

```yaml
logic_result:
  status: "success" | "error"
  solution: string       # Prolog solution
  explanation: string    # Logical explanation
  alternatives: array    # Alternative solutions
```

## Capabilities

### 1. Unification Fundamentals

Understanding unification as pattern matching:

```prolog
% Unification examples
X = Y.                    % X and Y unify (succeeds)
X = f(Y).                 % X = f(Y), Y unified to variable
f(A, B) = f(1, 2).       % A=1, B=2
[A, B] = [1, 2].         % A=1, B=2
```

### 2. Backtracking and Search

Exploiting Prolog's search engine:

```prolog
% Generate all solutions via backtracking
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% Find all solutions with findall/3
findall(X, (member(X, [1,2,3]), X > 1), Results).
% Results = [2, 3]
```

### 3. Recursion Patterns

Core recursive problem solving:

```prolog
% List processing
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.

% Tree traversal
tree_sum(empty, 0).
tree_sum(node(L, V, R), Sum) :-
    tree_sum(L, SL),
    tree_sum(R, SR),
    Sum is V + SL + SR.
```

### 4. Meta-programming

Programs that manipulate programs:

```prolog
% Call with accumulated results
maplist(_, [], []).
maplist(Pred, [H|T], [R|Rest]) :-
    call(Pred, H, R),
    maplist(Pred, T, Rest).

% Rule inspection
clause(Head, Body).
```

### 5. Difference Lists

Efficient list processing:

```prolog
% Difference list append - O(1)
dlist_append(D1-D2, D2-D3, D1-D3).

% Conversion
list_to_dlist(List, D-D) :-
    append(List, [], D).
```

### 6. Cut and Control

Managing search strategy:

```prolog
% Green cut - pruning equivalent choices
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).

% Red cut - changing search behavior
first_solution(X) :- member(X, [1,2,3,4]), !.
```

## Implementation Notes

- Start with declarative specification before implementation
- Use failure-driven loops for side effects
- Prefer pure predicates when possible
- Avoid green cuts that affect semantics
- Use freeze/1 or when/2 for delayed evaluation

## Best Practices

1. **Think Relations**: Define what relates, not what to do
2. **Separate Logic**: Keep pure logic separate from I/O
3. **Mode Thinking**: Consider all instantiation patterns
4. **Failure Analysis**: Understand why predicates fail
5. **Generate and Test**: Separate generation from filtering
6. **Accumulator Pattern**: Use accumulators for efficiency

## Error Handling

```prolog
% Catch specific errors
catch(Goal, Exception, Handler).

% Common exceptions
throw(error(assertion_failed, _)).
throw(instantiation_error).
throw(type_error(atom, Term)).
```

## Version History

- **1.0.0**: Initial skill for general logic programming

## Constraints

- MUST document non-logical (side-effect) predicates
- ALWAYS consider instantiation modes
- STOP if search space becomes too large