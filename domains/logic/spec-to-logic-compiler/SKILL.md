---
Domain: logic
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Development
Estimated Execution Time: 100ms - 5 minutes
name: spec-to-logic-compiler
---

## Description

Compiles task descriptions and specifications into executable logic programs (DML/Prolog) for guaranteed execution semantics. This skill provides frameworks for converting markdown specifications into deterministic, verifiable logic-based workflows that ensure all steps are executed in order.

## Purpose

To create reliable, deterministic agent workflows by compiling specifications to logic programs instead of relying on prompt-based execution where steps may be skipped or reordered.

## When to Use

- When deterministic execution is required
- Building complex multi-step agent workflows
- Implementing retry/fallback logic
- Creating verifiable tool definitions
- Ensuring all steps in a specification are executed

## When NOT to Use

- Simple, linear tasks
- When human oversight can catch missed steps
- Situations where flexibility is preferred over determinism

## Input Format

```yaml
compile_request:
  source_type: "markdown|yaml|json"
  spec_content: string   # Specification to compile
  output_format: "dml|prolog"
  tools: array          # Available tools
```

## Output Format

```yaml
compile_result:
  status: "success" | "error"
  compiled_code: string  # Generated DML/Prolog
  execution_order: array # Ordered steps
  guarantees: array      # Execution guarantees
```

## Capabilities

### 1. Markdown to DML Compilation

Convert markdown specs to executable logic:

```markdown
<!-- Original markdown -->
# API Documentation Lookup

## Arguments
- Query: API name to look up

## Tools needed
- web_search
```

```prolog
% Compiled DML
tool(search(Query, Results), "Search the web") :-
    exec(web_search(query: Query), Results).

agent_main(Query) :-
    system("You are an API documentation assistant..."),
    task("Look up documentation for: {Query}"),
    search(Query, Results),
    answer("Found documentation: {Results}").
```

### 2. Fallback Logic Compilation

Automatic retry on failure via backtracking:

```prolog
% Try fast approach first, fall back to thorough approach
agent_main(Question) :-
    system("Answer concisely."),
    task("Answer: {Question}"),
    validate_answer,                % Fails if inadequate
    answer("Done").

agent_main(Question) :-
    system("Answer thoroughly."),
    task("Research {Question} in depth"),
    validate_answer,
    answer("Done").
```

### 3. Tool Orchestration

Define deterministic tool sequences:

```prolog
tool(fetch_spec(Url, Spec), "Fetch OpenAPI spec") :-
    exec(web_fetch(url: Url), Spec).

tool(generate_client(Lang, Spec, Code), "Generate client") :-
    exec(cli(command: ["openapi-generator", "-g", Lang, "-i", Spec]), Code).

agent_main(Lang, Url) :-
    fetch_spec(Url, Spec),
    generate_client(Lang, Spec, Code),
    save_file("./output." + Lang, Code),
    answer("Client generated").
```

### 4. Loop and Iteration

Compile iteration patterns:

```prolog
% Process multiple files
agent_main(Files) :-
    maplist(process_file, Files),
    answer("All files processed").

process_file(File) :-
    read_file(File, Content),
    analyze(Content, Result),
    store_result(File, Result).
```

### 5. Validation Gates

Compile verification steps:

```prolog
validate_answer :-
    get_answer(A),
    length(A, Len),
    Len > 10,                           % Must be substantial
    \+ contains(A, "I don't know"),    % Must not contain uncertainty
    !.
```

### 6. State Management

Track execution state:

```prolog
:- use_module(library(journal)).
:- journal_mode(append).

agent_main(Task) :-
    journal(started(Task)),
    execute(Task, Result),
    journal(completed(Task, Result)),
    answer(Result).

execute(Task, Result) :-
    ...
```

## Implementation Notes

- Use `journal/1` for execution tracing
- Compile with `--watch` for development
- Use `deepclause run` for testing
- Export DML files for agent integration

## Configuration Options

```yaml
dml_config:
  target_runtime: "wasm|swi-prolog|native"
  tracing: boolean
  max_iterations: number
  timeout_seconds: number
```

## Best Practices

1. **Explicit Steps**: Every step in markdown becomes a predicate
2. **Backtrack Fallbacks**: Define alternative approaches for failure
3. **Validate Early**: Add validation predicates after key steps
4. **Trace Execution**: Use journal for debugging
5. **Separate Concerns**: Tools = predicates, workflow = clauses

## Error Handling

```prolog
% Graceful failure handling
agent_main(Task) :-
    catch(do_task(Task), Error, handle(Error)).

handle(error(timeout, _)) :-
    answer("Task timed out, try simpler approach").
handle(error(资源不足, _)) :-
    answer("Insufficient resources").
```

## Version History

- **1.0.0**: Initial skill for spec-to-logic compilation

## Constraints

- MUST validate compiled code before production use
- ALWAYS set timeout for long-running tasks
- STOP if compiled logic becomes unreadable