# Runtime-Structured Task Decomposition for Agentic Coding Systems

## Executive Summary

This paper presents an architectural approach for managing complex task decomposition and execution flow in LLM-based coding agents through executable control logic rather than monolithic prompts. By formalizing task partitioning as runtime-structured graphs, the approach achieves 51.7% lower retry costs for debugging and root cause analysis in software engineering tasks while maintaining rigorous schema validation across execution boundaries.

## Problem Statement

Traditional LLM-based coding agents suffer from several critical limitations in task decomposition:

1. **Monolithic Prompt Design**: Large, unstructured prompts conflate planning, code generation, and error recovery, making it difficult to diagnose failures and adjust execution strategy midstream.

2. **Implicit Task Boundaries**: Without explicit control flow specification, agents cannot dynamically adjust their reasoning or tool usage based on intermediate results, leading to cascading failures and expensive retry cycles.

3. **State Management Overhead**: Managing execution state through natural language conversations requires expensive context windows and frequent LLM calls to reconstruct agent knowledge.

4. **Verification Complexity**: Checking correctness at task boundaries requires expensive full-context validation rather than precise schema-driven assertion.

The research gap addressed is the lack of formal architectural patterns that balance flexibility (agents adapt to different scenarios) with structure (predictable, auditable execution flows).

## Core Concepts & Theory

### Execution-Grounded Task Architecture

The core innovation is replacing prompt-driven task orchestration with **runtime-structured control graphs** that formalize:

- **Task Nodes**: Discrete units of work (code analysis, implementation, testing, debugging) with defined input/output contracts
- **Control Edges**: Conditional transitions based on task outcome or state predicates
- **Schema Validation**: Executable assertions at task boundaries ensuring structural correctness
- **State Externalization**: Separation of execution state (metadata) from reasoning (LLM context)

### Multi-Agent Coordination Pattern

The framework enables a specialist-router topology:

```
┌─────────────────────────────────────────┐
│        Request Router Agent             │
│  (Task classification & sequencing)     │
└────────────────┬────────────────────────┘
                 │
         ┌───────┴───────┬───────────┬────────────┐
         │               │           │            │
    ┌────▼────┐   ┌─────▼────┐ ┌───▼────┐  ┌────▼─────┐
    │  Code   │   │ Debug    │ │ Test   │  │  Root    │
    │Analysis │   │ Agent    │ │ Agent  │  │ Cause    │
    │ Agent   │   │          │ │        │  │ Analyzer │
    └────┬────┘   └────┬─────┘ └───┬────┘  └────┬─────┘
         │              │           │            │
         └──────────────┴───────────┴────────────┘
                        │
              ┌─────────▼──────────┐
              │  Unified State     │
              │  & Artifact Store  │
              └────────────────────┘
```

### Task Decomposition Formalism

Each task is defined as a tuple: `Task = (ID, Input, Process, Output, Validation)`

Where:
- **Input**: Structured data schema (code files, error traces, test results)
- **Process**: LLM invocation with tool access (code parsing, test execution, error analysis)
- **Output**: Predicted structured result schema (e.g., bug location + fix suggestion)
- **Validation**: Runtime schema assertion ensuring output matches contract

### Execution Flow Control

Rather than embedding control logic in prompts, the system uses explicit state machines:

```
State: AnalyzeCode
  Input: {code: str, error: Optional[str]}
  Agent: CodeAnalysisAgent
  Tools: [code_parser, dependency_analyzer, type_checker]
  Output: {findings: List[Issue], severity: str}
  Transition:
    - if findings.empty → State: CodeComplete
    - if severity == CRITICAL → State: DebugCode
    - else → State: PlanFix
```

This enables:
1. **Precise Agent Context**: Each agent receives only relevant task context, reducing token overhead
2. **Failure Recovery**: The router can retry specific tasks, adjust tool selection, or escalate to different agents
3. **Transparent Auditability**: Every transition and decision is logged with explicit state snapshots

## Main Ideas & Contributions

### 1. Control Graph Architecture for Agentic Systems

The paper introduces a formal model for decomposing coding tasks into executable control graphs where each node represents a well-defined computation task. This replaces ad-hoc prompt chaining with:

- **Deterministic task sequences** for predictable workflows
- **Conditional branching** based on intermediate results
- **Explicit fallback policies** for failure recovery

### 2. Schema-Driven Output Validation

Rather than hoping LLM outputs match expectations, the system enforces structured contracts:

- Each task declares its output schema (JSON/Pydantic models)
- LLM generations are parsed and validated before state transition
- Failed validations trigger retry with refined prompts or agent switching

### 3. State Externalization & Caching

Instead of maintaining execution state in LLM context windows:

- Task outcomes are persisted in structured state stores
- Router agents access state via APIs rather than LLM reprocessing
- Reduces context overhead and enables long-horizon execution

### 4. Cost Optimization Through Selective Escalation

Rather than using large models uniformly:

- Lightweight models handle simple classification tasks
- Escalation to larger models occurs only for complex reasoning
- Results in 51.7% reduction in retry costs compared to monolithic agents

## Methodology & Implementation

### Experimental Setup

**Benchmarks Used**:
- HumanEval++ (synthetic code generation)
- GitHub Issues (real-world debugging scenarios)
- LeetCode Hard (complex algorithm implementation)
- Real production codebases (100K-1M LOC systems)

**Agent Configuration**:
- Base models: Claude 3.5 Sonnet, GPT-4, Mistral Large
- Tools: Code execution, type checking, test runners, documentation retrievers
- Router: Specialized task classifier with domain-specific prompts

**Baseline Comparisons**:
- Monolithic Agent: Single LLM with full context
- ReAct Agent: Step-by-step reasoning with reflection
- AutoGPT-style: Sequential tool calling without explicit control

### Metrics & Results

**Primary Metric: Retry Cost Reduction**
```
Monolithic Agent:    100% (baseline)
ReAct Pattern:       78% (22% reduction)
Runtime-Structured:  48% (51.7% reduction)
```

**Success Rate on Real Debugging Tasks**
- Identification accuracy: 89% (vs 71% monolithic)
- Root cause analysis: 84% (vs 62% monolithic)
- Complete fix generation: 67% (vs 41% monolithic)

**Latency Analysis**
- Monolithic: 45-120s per task (high variance, context recomputation)
- Runtime-Structured: 12-35s per task (predictable, caching benefits)

**Cost per Task (GPT-4 equivalent)**
- Monolithic: $0.45 average
- Runtime-Structured: $0.22 average (51% cost reduction)

### Agent Topologies Illustrated

**Example: Debugging Workflow**

```
┌──────────────────────────────────────────────────────────────┐
│                    Test Failure Received                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                    ┌────▼─────┐
                    │ Classify  │
                    │ Error     │
                    │ Type      │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         │               │               │              │
    ┌────▼────┐   ┌──────▼────┐   ┌────▼────┐    ┌────▼─────┐
    │ Syntax  │   │ Runtime   │   │ Logic   │    │Integration│
    │ Error   │   │ Error     │   │ Error   │    │Error      │
    └────┬────┘   └──────┬────┘   └────┬────┘    └────┬─────┘
         │               │             │              │
    ┌────▼────┐   ┌──────▼────┐   ┌────▼────┐    ┌────▼─────┐
    │ Parse   │   │Trace      │   │ Analyze │    │Validate  │
    │Code     │   │Execution  │   │Logic    │    │Contract  │
    └────┬────┘   └──────┬────┘   └────┬────┘    └────┬─────┘
         │               │             │              │
         └───────────────┼─────────────┴──────────────┘
                         │
                    ┌────▼─────────┐
                    │Generate Fix  │
                    │Candidates    │
                    └────┬─────────┘
                         │
                    ┌────▼──────┐
                    │Validate   │
                    │Against    │
                    │Tests      │
                    └────┬──────┘
                         │
                  ┌──────▼──────┐
                  │Return Fixed │
                  │Code + Report│
                  └─────────────┘
```

## Practical Applications & Use Cases

### 1. Continuous Integration Debugging

**Scenario**: A CI pipeline fails with a cryptic error from a dependency upgrade.

**Traditional Approach**: Single agent attempts to analyze logs, check code, identify root cause—expensive retries when context is lost.

**Runtime-Structured**: 
- Classification task: Error categorization (dependency version conflict, API breaking change, etc.)
- Analysis task: Specialized analyzer queries dependency manifests and changelog
- Root cause task: Traces dependency graph to identify conflict
- Result: 73% faster diagnosis, explicit audit trail

### 2. Refactoring Large Codebases

**Scenario**: Modernize legacy codebase (100K+ LOC) to new architecture.

**Challenge**: Monolithic approaches lose context across file boundaries; state explosion with full codebase.

**Solution**: 
- Task decomposition by module/layer
- State stores track refactoring progress across session boundaries
- Different agents specialize in API migration, test rewriting, dependency updates
- Result: Enables multi-day refactoring campaigns without context reset

### 3. Test Suite Expansion

**Scenario**: Increase test coverage for critical module from 45% to 80%.

**Workflow**:
- Classification: Identify untested code paths (control flow analysis)
- Generation: Create test cases for each path (test template + example data)
- Validation: Execute tests, ensure coverage metrics improve
- Schema validation: Ensure test output matches test framework contracts

**Result**: 89% of generated tests pass without manual intervention (vs 64% for monolithic)

### 4. Production Bug Fixing

**Scenario**: Fix critical bug in production code with minimal downtime.

**Runtime-Structured Advantages**:
- Parallel analysis: Multiple agents analyze logs, code paths, failing tests simultaneously
- Rapid feedback: Intermediate results inform agent selection (escalate to larger model if needed)
- Auditability: Complete execution trace for incident post-mortem

## Insights & Implications

### 1. Structured Execution > Prompting for Autonomy

The findings demonstrate that well-designed control structures outperform prompt engineering alone. Rather than crafting increasingly complex prompts, defining explicit task contracts and control flows yields:
- More predictable agent behavior
- Faster failure recovery
- Better cost efficiency
- Complete auditability

### 2. State Management is Critical Infrastructure

Externalizing execution state from LLM context windows enables:
- Long-horizon tasks (hours, days of execution)
- Cross-session persistence and resumption
- Cost-effective caching of intermediate results
- Enables agents to work across massive codebases without context overflow

### 3. Specialization Through Role Definition

Assigning agents to specific task types (debugging vs. implementation vs. testing) rather than universal "CodeAgent" instances improves:
- Token efficiency (agents see only relevant context)
- Success rates (domain-specific prompts are more effective)
- Debuggability (narrower scope = easier to diagnose failures)

### 4. Cost-Performance Trade-off Space

The paper reveals a latent variable: **model size vs. task complexity**. By explicitly routing tasks, the system can:
- Use small models (Llama 2 7B) for classification and boilerplate generation
- Reserve large models (GPT-4, Claude Opus) for complex reasoning
- Result: 51.7% cost reduction without sacrificing success rate

### Open Research Questions

1. **Generalization**: How do task graphs transfer between codebases? Can a refactoring graph learned on one system apply to another?

2. **Emergent Task Structures**: Can agents learn to propose new task decompositions when standard graphs fail?

3. **Multi-Agent Optimization**: How should the router balance parallel execution (speed) vs. sequential execution (context sharing)?

## Code & Resources

### Implementation Framework

The paper describes implementation patterns compatible with existing frameworks:

**Pseudo-code for Router Agent**:
```python
class TaskRouter:
    def route(self, failure_event, state):
        error_type = self.classify_error(failure_event)
        task_graph = self.load_graph(error_type)
        
        for task in task_graph.nodes:
            agent = self.select_agent(task)
            output = agent.execute(
                input=state.get_task_input(task),
                tools=task.tools,
                schema=task.output_schema
            )
            
            if not self.validate(output, task.output_schema):
                # Retry with different agent/model
                output = self.escalate(agent, task, output)
            
            state.persist(task.id, output)
        
        return state.get_final_output()
```

### Required Infrastructure

- **State Store**: Redis, PostgreSQL, or DynamoDB for execution state
- **Schema Validation**: Pydantic, JSON Schema validators
- **Tool Executor**: Code execution sandbox (Docker, nix-shell)
- **LLM API**: Compatible with function calling (OpenAI, Anthropic, open models)

### Dependency Stack

- `pydantic>=2.0` (schema validation)
- `tenacity` (retry logic)
- `python-dotenv` (environment management)
- Framework: LangChain, LlamaIndex, or custom orchestration

### Integration Guide

1. **Define Task Graphs**: Specify task nodes, edges, schemas as YAML/JSON config
2. **Implement Agent Classes**: Subclass base `TaskAgent` with domain prompts
3. **Configure Tools**: Register available tools (code parsers, executors, retrievers)
4. **Deploy Router**: Start router service, feed failure events as stream
5. **Monitor Execution**: Log all task transitions, states, and outcomes

## Related Work & Context

### Foundational Architectures

- **ReAct (Yao et al., 2023)**: Introduced reasoning-action loop; this work adds explicit control structure
- **AutoGPT / Agent Loops**: Iterative tool calling; this work adds task decomposition
- **SWE-Agent (Yang et al., 2024)**: Repository-aware agent; complementary to structured task execution

### Prior Work on Task Decomposition

- **Hierarchical Task Network Planning**: Classical AI planning (not neural)
- **Chain-of-Thought**: Implicit decomposition through reasoning; this work makes it explicit
- **Constitutional AI / Critique**: Feedback loops; this work adds control-theoretic formalism

### Related Multi-Agent Topologies

- **Hierarchical Agents** (Lillian Weng, 2023): Manager coordinates workers; similar concept with runtime structure
- **Specialist Ensemble** (GPT-4 technical report): Route different tasks to different models; this work adds formal schemas
- **MACOG** (Infrastructure-as-Code multi-agent): Task graphs for IaC generation

### Complementary Research Directions

1. **Learning Task Graphs**: Can agents propose optimal decompositions via meta-learning?
2. **Compositional Skill Learning**: How to reuse task structures across different domains?
3. **Formal Verification**: Can we prove correctness properties of task graphs?

## Future Research Implications

The runtime-structured approach opens pathways for:

- **Adaptive Task Graphs**: Systems that learn and evolve decomposition strategies based on success/failure patterns
- **Formal Specification**: Integration with formal methods to guarantee properties of agentic execution
- **Multi-Agent Consensus**: Using task graphs as communication protocol between heterogeneous agents
- **Cross-Codebase Transfer**: Transferring learned task graphs to new systems with minimal adaptation

---

**Paper Details**:
- **ArXiv ID**: 2605.15425
- **Published**: May 2026
- **Venue**: (Major conference/preprint)
- **Citations**: Part of emerging work on structured agent orchestration
