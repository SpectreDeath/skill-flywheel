---
Domain: logic
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Development
Estimated Execution Time: 100ms - 5 minutes
name: swi-prolog-programmer
---

## Description

Expert SWI-Prolog programming practices for declarative logic programming. Emphasizes relational thinking, DCGs (Definite Clause Grammars), constraint libraries (CLP(FD), CLP(B)), module system, and SWI-specific tooling including tracing, profiling, and editor integrations.

## Purpose

To provide comprehensive guidance for writing robust, multi-directional Prolog predicates using SWI-Prolog's full ecosystem, with emphasis on test-driven development using PlUnit and proper module organization.

## When to Use

- Writing SWI-Prolog code for knowledge representation
- Building parsers with DCGs
- Implementing constraint solving (CLP)
- Creating knowledge-base systems
- Testing Prolog code with PlUnit

## When NOT to Use

- When imperative/OO solution is more appropriate
- When Prolog is not available in the environment
- Simple tasks that don't require logic programming

## Input Format

```yaml
prolog_request:
  action: "write|debug|test|refactor|optimize"
  task: string           # Task description
  file_path: string     # Prolog file to work with
  constraints: array     # Optional: CLP constraints
  test_mode: boolean    # Whether to generate PlUnit tests
```

## Output Format

```yaml
prolog_result:
  status: "success" | "error"
  code: string           # Generated Prolog code
  tests: string         # PlUnit tests (if requested)
  explanation: string   # Logic explanation
```

## Capabilities

### 1. Relational Thinking

Write predicates that work in multiple directions:

```prolog
% Multi-directional append
my_append([], L, L).
my_append([H|T], L, [H|R]) :- my_append(T, L, R).

% Works as: append([1,2], [3,4], X)     -> X = [1,2,3,4]
% Works as: append(X, Y, [1,2,3,4])     -> X=[], Y=[1,2,3,4]; X=[1], Y=[2,3,4]; ...
```

### 2. Definite Clause Grammars (DCGs)

Build parsers and text processing:

```prolog
% Simple DCG for sentence parsing
sentence --> noun_phrase, verb_phrase.
noun_phrase --> determiner, noun.
verb_phrase --> verb, noun_phrase.

determiner --> [the].
noun --> [cat] | [dog].
verb --> [chases] | [sees].

% Usage: phrase(sentence, [the, cat, chases, the, dog])
```

### 3. Constraint Libraries

CLP(FD) for finite domain constraints:

```prolog
% Send More Money puzzle
send_more_money :-
    Vars = [S,E,N,D,M,O,R,Y],
    Vars in 0..9,
    S #> 0,
    M #> 0,
    all_different(Vars),
    1000*S + 100*E + 10*N + D + 
    1000*M + 100*O + 10*R + Y #= 
    10000*M + 1000*O + 100*N + 10*E + Y,
    labeling([], Vars).
```

CLP(B) for boolean constraints:

```prolog
% Boolean circuit satisfaction
sat_formula(Formula) :-
    Formula = (A #\/ B #/\ C),
    sat(Formula).
```

### 4. Module System

Proper module organization:

```prolog
% my_module.pl
:- module(my_module, [pred1/2, pred2/3]).
:- use_module(library(lists)).

pred1(X, Y) :- ...
pred2(A, B, C) :- ...
```

### 5. SWI-Prolog Tools

- **Prolog tracer**: `?- trace.`
- **Profiler**: `?- profile/1.`
- **_thread_local**: Threaded fact storage
- **plunit**: Unit testing framework

### 6. PlUnit Testing

```prolog
:- use_module(library(plunit)).

:- begin_tests(my_module).

test(append_empty) :-
    my_append([], L, L).

test(append_basic) :-
    my_append([1,2], [3], [1,2,3]).

:- end_tests(my_module).

% Run: ?- run_tests.
```

## Implementation Notes

- Always use `format/2` for output, not `write/1`
- Prefer `format/3` with ~w for debugging
- Use `debug/3` for conditional debugging
- Use `assertz/1` for dynamic facts, but prefer static rules
- Avoid cut (!) except in specific patterns
- Use `call_with_time_limit/2` for long-running queries

## Best Practices

1. **Relational Design**: Write predicates that work forwards and backwards
2. **Steadfastness**: Ensure predicates don't depend on instantiation order
3. **Mode Declarations**: Add mode declarations for documentation
4. **Test First**: Write PlUnit tests before implementation
5. **DCGs for Text**: Use DCGs instead of string manipulation
6. **Constraints First**: Use CLP before explicit enumeration
7. **Module Organization**: Group related predicates in modules
8. **Version Targeting**: Use SWI-Prolog 9.2.x stable or 9.3.x dev

## Error Handling

- Use `catch/3` for exception handling
- Handle instantiation errors with `must_be/2`
- Use `reset` for backtracking control
- Check mode with `ground/1`, `var/1`

## Configuration Options

```yaml
swi_prolog_config:
  version: "9.2.x" | "9.3.x"
  pack_management: boolean
  thread_local: boolean
  profiling: boolean
```

## Version History

- **1.0.0**: Initial skill for SWI-Prolog best practices

## Constraints

- MUST use PlUnit for testing in production code
- ALWAYS declare modes for exported predicates
- STOP if predicate has side effects without documentation