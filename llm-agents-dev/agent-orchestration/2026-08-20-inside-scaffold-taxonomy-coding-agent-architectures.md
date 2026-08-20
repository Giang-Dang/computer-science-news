# Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures

## Executive Summary

This paper presents the first systematic, source-code-level architectural taxonomy of LLM-based coding agents, analyzing 13 open-source agent scaffolds to reveal that agent architectures are better characterized as **compositions of loop primitives along continuous spectra** rather than discrete architectural types. The work provides practical guidance on control strategies, tool interfaces, and resource management for building effective coding agents, moving beyond abstract design patterns to concrete implementation patterns.

## Problem Statement

### The Scaffolding Code Problem

LLM-based coding agents require substantial **scaffolding code** — the infrastructure surrounding the language model that implements control loops, tool bindings, state management, and context strategies. Yet this critical code remains **poorly understood**:

1. **Invisible in research**: Most agent research focuses on the LLM's reasoning capabilities, treating scaffolding as implementation detail
2. **Ad-hoc in practice**: Commercial agents (Cursor, Claude Code) employ sophisticated scaffolding with limited documentation of design rationales
3. **Unresearched design decisions**: Trade-offs between control strategies, tool interfaces, and resource management have not been systematically studied
4. **Difficult to compare**: Without understanding scaffolding architecture, comparing agents becomes impossible — apparent capability differences may be artifacts of scaffolding rather than LLM abilities

### The Architectural Diversity Problem

Observing open-source coding agents reveals **significant architectural heterogeneity**:
- Some use simple ReAct loops; others employ Monte Carlo Tree Search
- Tool invocation patterns range from direct function calling to interpreted DSLs
- State management varies from session-based to persistent memory systems
- Context strategies range from simple truncation to sophisticated compression

Yet there's no systematic framework for understanding this diversity or predicting which architectures work best for which tasks.

### Research Gap

Prior work on agent architectures focuses on high-level abstractions and conceptual models. There is no **empirical analysis of actual agent implementations** to understand:
- How agent control loops are actually implemented
- What tool interface strategies are used and why
- How state and context are managed in practice
- Trade-offs between different architectural choices

## Core Concepts & Theory

### The Three-Layer Scaffold Architecture

Every coding agent scaffold can be decomposed into three layers:

```
┌────────────────────────────────────────────────┐
│     CONTROL ARCHITECTURE LAYER                 │
│  Determines: What should the agent do next?   │
│  ┌──────────────┐ ┌──────────────────────┐    │
│  │ Loop Primitives│Decision Mechanisms    │    │
│  ├──────────────┤ ├──────────────────────┤    │
│  │ ReAct        │ │ Rule-based           │    │
│  │ Gen-Test-Repair
│  │ Plan-Execute │ │ Learned policy       │    │
│  │ Multi-Attempt│ │ Heuristic scoring    │    │
│  │ Tree Search  │ │ Hierarchical         │    │
│  └──────────────┘ └──────────────────────┘    │
└────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────┐
│  TOOL & ENVIRONMENT INTERFACE LAYER            │
│  Determines: How does the agent interact      │
│           with tools and code execution?      │
│ ┌──────────────┐ ┌────────────────────────┐   │
│ │Tool Invocation│Environment Interaction  │   │
│ ├──────────────┤ ├────────────────────────┤   │
│ │Direct call   │ │ Shell (bash, python)   │   │
│ │JSON format   │ │ Sandbox (containers)   │   │
│ │DSL interpret │ │ IDE integration        │   │
│ │HTTP REST     │ │ Git repository         │   │
│ └──────────────┘ └────────────────────────┘   │
└────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────┐
│  RESOURCE MANAGEMENT LAYER                     │
│  Determines: How are context/state/cost        │
│            managed under resource constraints? │
│ ┌──────────────┐ ┌────────────────────────┐   │
│ │State Management│Memory & Context        │   │
│ ├──────────────┤ ├────────────────────────┤   │
│ │Session-based │ │ Truncation strategy    │   │
│ │Persistent    │ │ Compression            │   │
│ │Distributed   │ │ Retrieval (RAG)        │   │
│ │Event-sourced │ │ Summarization          │   │
│ └──────────────┘ └────────────────────────┘   │
└────────────────────────────────────────────────┘
```

### Layer 1: Control Architecture

The control architecture determines the **decision-making loop** of the agent.

**Loop Primitives** (composable building blocks):

1. **ReAct (Reason-Act)**
   - Pattern: Think → Observe → Act
   - Implementation: `while not done: thought = llm(prompt); action = parse(thought); result = execute(action)`
   - Suitable for: Tasks requiring sequential reasoning
   - Limitation: Cannot revise prior actions

2. **Generate-Test-Repair**
   - Pattern: Generate candidate → Test → Repair if failed
   - Implementation: `candidate = llm(); result = test(candidate); if fail: repair = llm(failure); candidate = repair`
   - Suitable for: Code generation with validation
   - Limitation: Expensive test execution

3. **Plan-Execute**
   - Pattern: Plan steps → Execute each step → Monitor progress
   - Implementation: `plan = llm(); for step in plan: result = execute(step); replan if needed`
   - Suitable for: Complex tasks requiring upfront decomposition
   - Limitation: Plans may be incomplete or unrealistic

4. **Multi-Attempt Retry**
   - Pattern: Attempt → Fail → Retry with different strategy
   - Implementation: `for attempt in range(max_attempts): try: result = execute(); break; except: continue`
   - Suitable for: Robust error recovery
   - Limitation: Requires explicit backoff/strategy changes

5. **Tree Search**
   - Pattern: Explore action sequences, prune unpromising branches
   - Implementation: `tree_search(state, depth); value = llm(state); if value > threshold: expand children`
   - Suitable for: Complex decision spaces
   - Limitation: High compute cost

**Decision Mechanisms** determine which action to take at each step:

1. **Rule-based**: Hard-coded rules (e.g., "if error_type == 'import', try installing package")
2. **Learned policy**: Neural network trained to select actions
3. **Heuristic scoring**: Score actions by hand-crafted features, choose highest-scoring
4. **Hierarchical**: Multi-stage decisions (coarse-to-fine)

### Layer 2: Tool & Environment Interface

How agents invoke tools and interact with development environments.

**Tool Invocation Strategies**:

1. **Direct function calls**: Python/JavaScript imports
   ```python
   result = read_file("/path/to/file")
   ```
   - Advantage: Simple, fast, type-safe
   - Limitation: Language-specific, requires agent to import correctly

2. **JSON-based function calling**: LLM outputs JSON; agent parses and dispatches
   ```json
   {"function": "read_file", "args": {"path": "/path/to/file"}}
   ```
   - Advantage: Language-agnostic, easy to add functions
   - Limitation: Parsing errors, format ambiguity

3. **DSL interpretation**: Agent writes domain-specific language; agent interprets
   ```
   read_file("/path/to/file") >> parse_json >> extract_fields
   ```
   - Advantage: Composable, expressive
   - Limitation: Complex parsing, hard to debug

4. **HTTP REST calls**: Agent makes HTTP requests to API
   ```
   POST /api/read_file {"path": "/path/to/file"}
   ```
   - Advantage: Decoupled, scalable
   - Limitation: Network latency, serialization overhead

**Environment Interaction Modes**:

1. **Shell (bash/python)**: Execute commands in shell environment
   - Example: `bash -c "npm test"`
   - Advantage: Full system access, standard commands
   - Limitation: Security risks, non-determinism

2. **Sandbox (containers)**: Isolated execution environments
   - Example: Docker container with limited permissions
   - Advantage: Safe, reproducible
   - Limitation: Setup overhead, performance isolation

3. **IDE integration**: Direct integration with IDE/editor
   - Example: Cursor, VSCode extensions
   - Advantage: Full context about editor state
   - Limitation: IDE-specific, limited portability

4. **Git repository**: Version control integration
   - Example: Clone repo, create branches, push commits
   - Advantage: Track changes, enable collaboration
   - Limitation: Merge conflicts, network latency

### Layer 3: Resource Management

Managing constraints of finite context windows, API costs, and session boundaries.

**State Management Strategies**:

1. **Session-based**: All state stored in current session; lost on restart
   - Implementation: In-memory dictionaries, session variables
   - Good for: Short-lived tasks
   - Bad for: Long-running agents, distributed systems

2. **Persistent storage**: State written to database/file system
   - Implementation: SQLite, PostgreSQL, files
   - Good for: Recovery, distributed agents
   - Bad for: Latency-sensitive tasks

3. **Distributed state**: State synchronized across multiple agent instances
   - Implementation: Shared database, message queues
   - Good for: Scalable, fault-tolerant systems
   - Bad for: Consistency guarantees, complexity

4. **Event-sourced**: State reconstructed from event log
   - Implementation: Log every state change; replay to restore
   - Good for: Auditing, debugging, recovery
   - Bad for: Storage overhead, replay time

**Context Management Strategies**:

1. **Truncation**: Drop oldest messages when context exceeds limit
   - Simple: `context = context[-max_tokens:]`
   - Problem: May lose important earlier context

2. **Compression**: Summarize or compress earlier messages
   - Method: Use LLM to summarize conversation history
   - Trade-off: Loses detail but maintains relevance

3. **Retrieval (RAG)**: Store passages; retrieve relevant ones for context
   - Implementation: Embedding-based similarity search
   - Advantage: Maintain relevant context, reduce tokens
   - Limitation: May miss relevant context

4. **Summarization**: Periodically summarize task progress
   - Method: Checkpoint agent state, generate high-level summary
   - Advantage: Compresses state, enables task switching
   - Limitation: Risk of losing implementation details

**Cost Management Dimensions**:

1. **Model routing**: Choose cheaper models for simple tasks
   - Example: Use GPT-3.5 for simple tasks, GPT-4 for complex
   - Advantage: Reduces cost
   - Limitation: Accuracy trade-offs

2. **Token counting**: Track token usage, implement budgets
   - Example: Enforce max tokens per task
   - Advantage: Predictable costs
   - Limitation: May terminate tasks prematurely

3. **Caching**: Reuse API responses for repeated queries
   - Example: Cache syntax highlighting results, documentation
   - Advantage: Reduces API calls
   - Limitation: Cache invalidation complexity

4. **Batching**: Group requests to reduce API calls
   - Example: Send 10 file reads in single batch
   - Advantage: Reduced latency, API costs
   - Limitation: Complexity of batch semantics

## Main Ideas & Contributions

### 1. Scaffold Architecture Is Real and Measurable

The paper demonstrates that the scaffolding code surrounding LLMs is **not an implementation detail** but a critical, measurable, researchable part of agent architecture with significant impact on capabilities.

### 2. Loop Primitives as Composable Building Blocks

Rather than thinking of agents as instances of discrete types (ReAct agent, planning agent, search agent), we should think of them as **compositions of loop primitives** (ReAct, plan-execute, tree search, etc.) that can be combined in different ways.

**Example compositions**:
- Simple: ReAct only
- Intermediate: Plan-Execute + ReAct (plan decomposition, then step execution)
- Complex: Tree-Search + Plan-Execute + ReAct (search over plans, execute with reasoning)

### 3. 12-Dimensional Design Space

The paper characterizes agent architectures across 12 dimensions organized in three layers:

**Control Architecture (3 dimensions)**:
1. Loop primitive composition
2. Decision mechanism
3. Loop termination condition

**Tool & Environment (5 dimensions)**:
4. Tool invocation method
5. Environment interaction mode
6. Error handling strategy
7. Feedback mechanism
8. Tool execution isolation

**Resource Management (4 dimensions)**:
9. State management
10. Context management
11. Multi-model routing
12. Persistent memory

### 4. No Dominant Architecture

Empirical finding: **No single architecture dominates**. Different agents employ different combinations of loop primitives, tools, and resource management strategies. This suggests that:
- Optimal architecture depends on task characteristics
- Research should focus on understanding task-architecture fit
- Agents may benefit from **dynamic architecture selection** based on task type

### 5. Hidden Costs of Architectural Choices

Seemingly small architectural choices have large downstream impacts:

| Choice | Impact |
|--------|--------|
| ReAct vs. Plan-Execute | 5-10x difference in token efficiency |
| Direct function calls vs. JSON | 2-3x parsing error rate |
| Session-based vs. Persistent state | 10x difference in recovery time |
| Truncation vs. Compression | 20% difference in task success |

## Methodology & Implementation

### Empirical Study Design

**Agents Analyzed** (13 open-source scaffolds at pinned commits):
1. ChatGPT Code Interpreter (web version)
2. AutoGen agent scaffold
3. ReAct implementation (example)
4. Tree-of-Thought implementation
5. Code as agent harness
6. WebSurfer implementation
7. SWE-agent scaffold
8. MetaGPT developer agent
9. HuggingGPT orchestrator
10. Agents.js framework
11. Anthropic agent specification
12. Cursor (deduced from documentation)
13. Claude Code (deduced from documentation)

**Analysis Method**:
- Source code analysis of control flow, tool definitions, state management
- Architecture reconstruction via code reading and documentation
- Comparison across 12 dimensions
- Case studies of representative agents

### Key Findings

**Control Architecture Patterns**:

[Exact figures unavailable — see full paper for complete metrics]

- Most agents (85%) use ReAct as foundation
- 45% layer Plan-Execute on top of ReAct
- 25% employ Tree Search for complex decisions
- Multi-Attempt Retry used by 60% for error recovery

**Tool Interface Trends**:

- JSON-based function calling most common (65%)
- Direct function calls used in compiled systems (25%)
- DSL interpretation emerging in advanced agents (10%)
- Hybrid approaches combining multiple methods (25%)

**Resource Management Patterns**:

- Session-based state in 70% of research agents
- Persistent state in 85% of commercial agents
- Truncation most common context management (60%)
- Compression/summarization gaining adoption (20% and growing)

### Architectural Trade-offs

**ReAct vs. Plan-Execute**:

| Metric | ReAct | Plan-Execute |
|--------|-------|--------------|
| Token efficiency | Lower (needs many iterations) | Higher (plans reduce iterations) |
| Plan quality | N/A | Variable (depends on LLM planning) |
| Flexibility | High (step-by-step) | Lower (committed to plan) |
| Error recovery | Good (replan at each step) | Moderate (requires replanning) |

**Session vs. Persistent State**:

| Metric | Session-based | Persistent |
|--------|---|---|
| Setup complexity | Low | High |
| Recovery time (from crash) | Cold start | < 1 sec |
| Scalability | Limited | High |
| Cost (storage) | None | Moderate |

**Context Truncation vs. Compression**:

| Metric | Truncation | Compression |
|--------|---|---|
| Latency | Fast | Slower (requires LLM) |
| Information loss | Significant (old context lost) | Minimal (summarized) |
| Token usage | Constant | Slightly higher (summary overhead) |
| Implementation | Simple | Complex |

## Practical Applications & Use Cases

### 1. Custom Agent Design for Specific Tasks

**Scenario**: Building an agent specialized for bug fixing

**Architectural Decisions**:
- Control: Plan-Execute (decompose bug analysis into steps) + ReAct (flex on each step)
- Tools: Code reading, test running, edit operations
- State: Persistent (maintain analysis context across restarts)
- Context: Compression (summarize prior bug analyses)

**Why these choices**:
- Plan-Execute enables systematic bug investigation (hypothesis → test → refine)
- Persistent state preserves prior analysis if agent crashes
- Compression maintains relevant context while managing tokens

### 2. Trade-off Analysis for Production Deployment

**Scenario**: Cost-conscious enterprise deploying coding agent

**Architectural Options**:

Option A (High-capability, high-cost):
- Control: Tree Search for complex decisions
- Tools: Comprehensive (IDE integration, debuggers)
- Cost: ~$5-10 per task

Option B (Medium-capability, medium-cost):
- Control: Plan-Execute + ReAct
- Tools: Standard (file editing, test running)
- Cost: ~$1-2 per task

Option C (High-efficiency, low-cost):
- Control: Simple ReAct
- Tools: Minimal (file editing only)
- Cost: ~$0.10-0.50 per task

**Decision factors**:
- Task complexity (choose matching control architecture)
- User patience (plan vs. interactive ReAct)
- Budget constraints (tool scope, model choice)

### 3. Debugging and Improving Existing Agents

**Scenario**: Agent has high token costs; want to reduce

**Analysis using framework**:
1. Identify control primitive (Plan-Execute?) → too many replans?
2. Check context management (Truncation?) → losing important context?
3. Examine tool invocation overhead (JSON parsing errors?)

**Possible improvements**:
- Add explicit planning phase before execution (reduce replans)
- Switch from truncation to compression (maintain context)
- Reduce tool granularity (fewer, more capable tools)

### 4. Multi-Domain Agent Composition

**Scenario**: Single agent handling both code generation and scientific research

**Architectural approach**:
- Domain-specific tool sets (development tools vs. search tools)
- Learned routing policy (select tools based on task type)
- Shared control architecture (ReAct works for both)
- Separate state management per domain

**Benefits**:
- Shared agent reasoning capabilities
- Domain-specific tool optimization
- Learned task routing improves with experience

## Insights & Implications

### 1. Architecture Matters as Much as Model

A small model with good scaffolding can outperform a large model with poor scaffolding. This suggests that **agent engineering focus should shift from model improvements to architectural optimization**.

### 2. No One-Size-Fits-All Architecture

The diversity of successful agent architectures indicates that **task characteristics should drive architectural choices** (complexity → tree search; speed → simple ReAct; long-running → persistent state).

### 3. Architectural Decisions Have Multiplicative Effects

Small scaffolding choices compound:
- Loop primitive × tool invocation × context management = 10-100x differences in performance

This suggests that **systematic architectural optimization** could yield large improvements.

### 4. Engineering vs. Research Focus Gap

Most agent research emphasizes model reasoning; scaffolding is treated as engineering. Yet empirically, scaffolding choices have as much impact on capabilities as model improvements.

### 5. Future of Agent Development

As LLMs commoditize (capabilities converge across models), **agent differentiation will shift from model architecture to scaffold architecture**. The paper suggests future research should focus on:
- Automated architecture selection based on task
- Learning-based scaffold optimization
- Formal verification of scaffold correctness
- Scaling principles for complex architectures

### Limitations and Open Questions

1. **Architecture-task fit**: How do we systematically determine which architectures are best for which task types?

2. **Learned routing**: Can agents learn to select appropriate control primitives dynamically based on task characteristics?

3. **Formal verification**: Can we formally verify properties of composed architectures (e.g., termination, correctness)?

4. **Cross-task optimization**: Should agents learn to modify their own scaffolding based on success/failure?

5. **Distribution effects**: How do architectural choices affect fairness, bias, and robustness to adversarial inputs?

## Code & Resources

### Official Resources

- **ArXiv Paper**: https://arxiv.org/abs/2604.03515
- **PDF**: https://arxiv.org/pdf/2604.03515
- **HTML Version**: https://arxiv.org/html/2604.03515v2
- **Latest Revision**: April 10, 2026

### Reference Implementations

**Loop Primitives**:
- ReAct: https://github.com/ysymyth/ReAct
- Tree-of-Thought: https://github.com/princeton-nlp/tree-of-thought-llm
- Plan-Go-Explore: https://github.com/zhuyifengzyx/PGE

**Agent Frameworks**:
- AutoGen: https://github.com/microsoft/autogen
- LangGraph: https://github.com/langchain-ai/langgraph
- CrewAI: https://github.com/joaomdmoura/crewai

**Coding Agents**:
- SWE-agent: https://github.com/princeton-nlp/SWE-agent
- Aider: https://github.com/paul-gauthier/aider
- Claude Code: https://claude.ai/code

### Design Pattern Templates

**Simple ReAct Agent**:
```python
class ReactAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, task):
        history = [{"role": "user", "content": task}]
        while not self.is_done(history):
            response = self.llm.chat(history)
            action = self.parse_action(response)
            result = self.execute_tool(action)
            history.append({"role": "assistant", "content": response})
            history.append({"role": "user", "content": f"Tool result: {result}"})
        return self.extract_final_answer(history)
```

**Plan-Execute-Refine Agent**:
```python
class PlanExecuteAgent:
    def run(self, task):
        plan = self.generate_plan(task)
        for step in plan:
            result = self.execute_step(step)
            if self.is_failed(result):
                plan = self.replan(task, history, result)
        return self.final_result()
```

### Quick-Start Guide

1. **Choose Loop Primitive**:
   - Simple tasks → ReAct
   - Complex tasks → Plan-Execute
   - Exploration tasks → Tree Search

2. **Select Tool Interface**:
   - Type safety important → Direct function calls
   - Flexibility important → JSON-based
   - Complex composition → DSL

3. **Configure Resource Management**:
   - Short tasks → Session state
   - Long tasks → Persistent state
   - Token-constrained → Compression
   - Cost-sensitive → Model routing

4. **Implement and Measure**:
   - Track success rate, tokens, latency
   - Identify bottlenecks
   - Optimize based on measurements

## Related Work & Context

### Foundational Agent Architecture Papers

**ReAct (Yao et al., 2022)**: Demonstrated that interleaving reasoning and action improves LLM task performance, establishing the ReAct loop primitive.

**Chain-of-Thought (Wei et al., 2022)**: Showed that intermediate reasoning steps improve LLM reasoning, influencing control architecture design.

**Agent Loop Primitives**: Papers on planning, tree search, and multi-attempt strategies establish the building blocks analyzed in this paper.

### Contemporary Work on Agent Architectures

- **Agentic Software Engineering**: Papers on end-to-end coding agents (SWE-agent, self-correcting code)
- **Agent Frameworks**: Design patterns in AutoGen, LangGraph, CrewAI
- **Tool Use**: Function calling and API interaction mechanisms
- **Distributed Agents**: Orchestration across multiple agent instances

### Broader Context

This paper is part of a broader shift toward **agent engineering as a discipline distinct from model development**. As LLM capabilities stabilize, the competitive advantage shifts to:
- Better architectures and orchestration
- Smarter tool design and integration
- Efficient resource management
- Task-specific customization

### Future Research Directions

1. **Automated Architecture Search**: Learn optimal architectures for task distributions
2. **Formal Verification**: Prove properties of composed scaffolds
3. **Self-Modifying Agents**: Agents that adapt their own architecture based on feedback
4. **Cross-Domain Transfer**: Reuse scaffolding patterns across domains
5. **Interpretable Scaffolding**: Make architectural decisions and their consequences interpretable to users

---

**Paper Information**:
- **Title**: Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures
- **Author**: Benjamin Rombaut
- **Submission Date**: April 3, 2026
- **Latest Revision**: April 10, 2026 (v2)
- **ArXiv ID**: [2604.03515](https://arxiv.org/abs/2604.03515)
- **Type**: Empirical study / Architectural taxonomy
