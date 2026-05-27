# Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems

**ArXiv ID:** 2605.18747  
**Submitted:** May 18, 2026  
**Authors:** [See full paper on arXiv](https://arxiv.org/abs/2605.18747)

## Executive Summary

This comprehensive survey reimagines code as the operational substrate for intelligent agent systems, moving beyond code as a mere output target. By treating code as an executable harness that connects reasoning, action, and environment modeling, the paper establishes a unified framework for building reliable, scalable multi-agent systems. This paradigm shift directly addresses the challenge of coordinating multiple agents while maintaining consistency, testability, and long-horizon task completion in software development automation.

## Problem Statement

Traditional agent architectures struggle with:
- **Coordination overhead in multi-agent systems**: How do multiple agents maintain consistency when modifying shared code artifacts?
- **Verification and feedback loops**: Without executable verification, agents lack ground truth for whether their actions succeeded
- **Scaling from single to multi-agent systems**: Existing harness mechanisms (planning, memory, tool use) don't naturally extend to collaborative settings
- **Long-horizon execution**: Agents need reliable memory and planning mechanisms to execute complex, multi-step tasks
- **Shared state management**: Maintaining consistency across multiple agents operating on the same codebase

Prior agent systems treated code as the end product rather than the infrastructure. This survey identifies the gap between isolated agent capabilities and production-grade systems operating at repository, feature, or algorithm granularity.

## Core Concepts & Theory

### The Three-Layer Harness Architecture

The paper organizes code-as-harness around three connected layers:

#### Layer 1: Harness Interface
Code serves as the bridge between agents and their environment through:
- **Reasoning substrate**: Code captures agent reasoning in executable form
- **Action interface**: Typed tool interfaces separate agent cognition from execution
- **Environment modeling**: Code represents the agent's understanding of the system state

This enables agents to work with verifiable, executable specifications rather than unstructured text.

#### Layer 2: Harness Mechanisms
Four key mechanisms make harnesses reliable and adaptive:

**Planning**
- Code-based task decomposition: agents break down complex problems into executable subtasks
- Long-horizon orchestration: planning is encoded in executable control flow
- Goal hierarchies: nested task structures enable abstraction

**Memory**
- Persistent code artifacts: working code becomes the agent's memory
- Context management: relevant code sections are retrieved and maintained
- Temporal reasoning: agents track which code components have been modified and when

**Tool Use**
- Typed tool interfaces: functions/APIs with clear signatures prevent hallucinated functionality
- Error feedback: tool execution failures provide ground-truth information
- Iterative refinement: agents use execution outcomes to improve code

**Feedback-Driven Control & Optimization**
- Test-based verification: automated tests ground agent reasoning
- Execution traces: agents observe actual behavior to verify correctness
- Adaptive planning: agents adjust strategies based on test results

### Diagram: Single-Agent Harness Architecture

```
┌─────────────────────────────────────────────────────┐
│           Agent Reasoning Process                    │
│  (Planning, Memory Retrieval, Goal Decomposition)   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Code Harness Interface      │
        │  (Typed Tool Definitions)    │
        └──────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         ▼                            ▼
    ┌─────────────┐          ┌────────────────┐
    │   Execute   │          │  Environment   │
    │   Tools     │          │   Modeling     │
    └─────────────┘          └────────────────┘
         │                            │
         └──────────────┬─────────────┘
                        ▼
            ┌──────────────────────────┐
            │ Execution Results &      │
            │ Test Feedback            │
            └──────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         │ Update Memory & Adjust Plan │
         └─────────────────────────────┘
```

### Diagram: Multi-Agent Harness Coordination

```
┌─────────────────────────────────────────────────────────┐
│              Shared Code Repository                      │
│  (CRDT-based, Conflict-Free, Observable Updates)        │
└────────┬─────────────────────────────────┬──────────────┘
         │                                 │
    ┌────┴─────────┐            ┌─────────┴────┐
    │              │            │              │
    ▼              ▼            ▼              ▼
┌────────┐  ┌────────┐    ┌────────┐   ┌────────┐
│Agent 1 │  │Agent 2 │    │Agent 3 │   │Agent N │
│        │  │        │    │        │   │        │
│Observ. │  │Observ.│    │Observ. │   │Observ.│
│Updates │  │Updates│    │Updates │   │Updates│
└────────┘  └────────┘    └────────┘   └────────┘
    │              │            │              │
    └──────────────┼────────────┼──────────────┘
                   │            │
                   ▼            ▼
            ┌────────────────────────┐
            │  TODO-Claim Protocol   │
            │  (Conflict Resolution) │
            └────────────────────────┘
```

### Comparison with Existing Frameworks

**Traditional Code Completion** (Copilot, early LLM tools):
- Operates at line/function granularity
- Stateless suggestions
- No verification loop
- No multi-agent support

**Code as Agent Harness**:
- Operates at repository/feature/algorithm granularity
- Stateful, persistent code artifacts
- Execution-based verification
- Natural multi-agent coordination via shared code
- Feedback-driven continuous improvement

## Main Ideas & Contributions

### Novel Approach to Multi-Agent Coordination

Rather than explicit message passing between agents, the paper proposes **observation-driven coordination**:
- Agents work on shared code artifacts
- Changes are observable (through version control, CRDTs, or similar mechanisms)
- Agents coordinate by monitoring updates and claiming work items
- Deterministic convergence guaranteed through careful protocol design

### Skill-Based Architecture Extensions

Agents can be organized around specialized skills:
- **Coder Agent**: generates new code
- **Debugger Agent**: identifies and fixes bugs via test feedback
- **Reviewer Agent**: validates code quality and adherence to standards
- **Planner Agent**: decomposes high-level requests into tasks
- **Tester Agent**: creates comprehensive test suites

### Tool Use with Verification

The paper emphasizes **typed tool interfaces** as crucial for reliability:
```
Tool Definition (Type Signature):
  generate_test(code: str, requirements: str) -> str
  
Agent invokes: generate_test(my_code, spec)
Execution provides ground truth: test results
Feedback loop: agent observes pass/fail outcomes
```

This contrasts with hallucination-prone tool use in simpler systems.

## Methodology & Implementation

### Application Domains Studied

The paper covers representative methods across:

1. **Coding Assistants**
   - GitHub Copilot, Claude Code, OpenAI Codex CLI
   - Repository-scale task completion
   - Interactive refinement with users

2. **GUI/OS Automation**
   - Desktop automation agents
   - Cross-application workflows
   - Observable state through UI screenshots/DOM

3. **Embodied Agents**
   - Robotic task execution
   - Physical world feedback
   - Sensor-based state estimation

4. **Scientific Discovery**
   - Experiment design agents
   - Data analysis workflows
   - Literature integration agents

5. **DevOps & Enterprise Workflows**
   - Infrastructure automation
   - Deployment pipeline management
   - Multi-system coordination

### Evaluation Framework

The paper doesn't report a single benchmark but synthesizes insights across:
- **Code quality metrics**: test coverage, bug density, maintainability indices
- **Task completion rates**: percentage of tasks successfully completed end-to-end
- **Human oversight metrics**: number of human corrections required
- **Scalability**: maximum codebase size and agent count
- **Latency**: wall-clock time to completion

[Exact figures unavailable — see full paper for comprehensive evaluation data]

### Multi-Agent Topologies & Workflows

#### Hierarchical Workflow

```
┌──────────────────────────────────┐
│      User Request                 │
└────────────────┬─────────────────┘
                 ▼
         ┌───────────────┐
         │ Planner Agent │
         │ Decomposes    │
         │ into subtasks │
         └───────┬───────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
    ┌────────┐      ┌────────┐
    │Coder A │      │Coder B │
    │Impl. 1 │      │Impl. 2 │
    └───┬────┘      └───┬────┘
        │                │
        └────────┬───────┘
                 ▼
         ┌───────────────┐
         │ Reviewer Agent│
         │ Validates &   │
         │ Integrates    │
         └───────┬───────┘
                 ▼
         ┌───────────────┐
         │ Tester Agent  │
         │ Test suite    │
         │ coverage chk  │
         └───────┬───────┘
                 ▼
        ┌────────────────┐
        │ Final Output   │
        │ & Deployment   │
        └────────────────┘
```

#### Peer Collaboration Workflow

```
Agent 1         Shared Code         Agent 2
  │             Repository           │
  │  ◄──────── Observable ────────►  │
  │             Updates              │
  │                                  │
  ├─ Claim TODO item 1              │
  │  (Write lock on task)            │
  │                                  │
  │  ├─ Generate code               │
  │  ├─ Run tests                   │
  │  ├─ Commit to repo              │
  │  └─ Release lock                │
  │                                  │
  │                      ◄───────────┤
  │                     Observe      │
  │                     new code     │
  │                                  │
  ├─ Integrate changes              │
  │  (Merge/rebase)                 │
  │                                  │
  │                       ├─ Claim TODO item 2
  │                       │
  │                       ├─ Generate code
  │                       ├─ Run tests
  │                       └─ Commit
```

## Practical Applications & Use Cases

### Use Case 1: Feature Development Workflow

**Scenario**: Implement a new payment processing feature

**Multi-Agent Workflow**:
1. **Planner**: Decomposes feature into tasks (schema design, processor implementation, test suite, documentation)
2. **Coder-1**: Implements database schema and migrations
3. **Coder-2**: Implements payment processor API integration
4. **Tester**: Generates comprehensive test suite (unit, integration, end-to-end)
5. **Reviewer**: Validates code quality, security, and style
6. **Integration Agent**: Merges all components and resolves conflicts

**Code as Harness**: All work is coordinated through shared git repository with observable commits. Tests run automatically at each step. No explicit message passing required.

### Use Case 2: Debugging Complex Bug

**Scenario**: Production bug affecting 5% of transactions

**Multi-Agent Workflow**:
1. **Debugger-1**: Analyzes error logs and identifies suspicious code regions
2. **Debugger-2**: Searches codebase for similar patterns (using code search)
3. **Analyst**: Reproduces bug using generated test case
4. **Fixer**: Implements targeted fix
5. **Tester**: Validates fix with regression tests
6. **Reviewer**: Ensures minimal change scope and impact analysis

**Code as Harness**: Shared error logs, generated test cases, and code diffs form the coordination medium.

### Integration Challenges

1. **Dependency Management**: Multiple agents modifying same modules requires careful version pinning and dependency conflict resolution
2. **Test Flakiness**: Concurrent test execution can introduce flakiness; agents must manage test isolation
3. **Merge Conflicts**: Careful task decomposition needed to minimize file overlaps
4. **Consistency Guarantees**: CRDT or git-based protocols must ensure consistency under concurrent writes
5. **Cost Scaling**: Token consumption grows with codebase size; context management critical

### Scalability Considerations

- **Codebase Size**: Agents can handle 100K+ lines of code with proper context management
- **Agent Count**: 5-10 agents effective for large features; beyond requires hierarchical organization
- **Latency**: Each agent cycle incurs LLM inference latency; pipelining critical for performance
- **Cost**: Each agent cycle costs API calls; parallel execution reduces total latency but increases token cost

## Insights & Implications

### Advancement in Autonomous Coding

The code-as-harness paradigm represents a **qualitative shift** from stateless code suggestion to **autonomous system engineering**:
- Agents can now work on decade-old codebases with complex interdependencies
- Long-horizon task completion (days-long projects) becomes feasible
- Multi-agent coordination enables specialization (debugger, tester, reviewer roles)

### Impact on Developer Workflows

- **Shift from implementation to specification**: Developers write high-level requirements; agents implement
- **Continuous verification**: Automated testing and deployment become default
- **Decoupling from human pacing**: Agents operate independently, humans intervene for decisions

### Limitations and Open Questions

1. **Incomplete Feedback**: How to verify correctness when tests don't cover all edge cases?
2. **Hallucinated Dependencies**: Agents may invoke non-existent functions; typed tools mitigate but don't eliminate
3. **Regression Prevention**: How to ensure agent changes don't break unrelated functionality?
4. **Human Oversight**: Where and how should humans review agent decisions in safety-critical systems?
5. **Multimodal Extensions**: How to extend to non-code artifacts (UI, documentation, configs)?

### Relevance to Agent Frameworks

The paper's insights directly inform design of production agent systems:
- **Skill frameworks**: Agents organized by specialized skills (coder, debugger, reviewer)
- **Tool use standards**: Typed interfaces reduce hallucination and enable verification
- **Coordination protocols**: CRDT-based observation of shared artifacts beats explicit messaging
- **Feedback mechanisms**: Test results and execution traces provide ground truth for adaptation

## Code & Resources

### Official References and GitHub Repositories

- **ArXiv Paper**: https://arxiv.org/abs/2605.18747
- **Related Projects**:
  - Claude Code: https://github.com/anthropics/claude-code
  - OpenAI Codex: https://openai.com/blog/openai-codex/
  - OpenHands: https://github.com/All-Hands-AI/OpenHands
  - SWE-agent: https://github.com/princeton-nlp/SWE-agent

### Dependencies and Requirements

- **LLM Provider**: Claude 3.x, GPT-4, or similar capable LLM
- **Execution Environment**: Docker, Kubernetes, or local development environment
- **Version Control**: Git with support for conflict-free merges (or CRDT backend)
- **Testing Framework**: pytest, unittest, or equivalent
- **Compute**: GPU optional; CPU sufficient for most tasks

### Quick-Start Integration Guide

```python
# Pseudo-code example of code-as-harness architecture
from agent_framework import Agent, SharedCodeRepository, Tool

# Initialize shared repository
repo = SharedCodeRepository(git_url="https://github.com/project")

# Define typed tools
def generate_code(spec: str, language: str) -> str:
    """Generate code matching specification"""
    pass

def run_tests(codebase: str) -> dict:
    """Execute test suite, return results"""
    pass

# Create specialized agents
planner = Agent("planner", skills=["planning", "decomposition"])
coder = Agent("coder", skills=["code_generation", "refactoring"])
tester = Agent("tester", skills=["test_generation", "test_execution"])

# Coordinate through shared code
planner.observe(repo.get_latest_commit())
tasks = planner.decompose(user_request)
repo.create_todos(tasks)

for agent in [coder, tester]:
    agent.observe_updates(repo)
    agent.claim_todo(repo)
    agent.execute_task(repo)
    repo.commit_changes(agent.name)
```

## Related Work & Context

### Foundational Work on Agent Systems

- **Belief-Desire-Intention (BDI) Models**: Rao & Georgeff foundational work on agent architectures
- **Reactive vs. Deliberative Agents**: Brooks' subsumption architecture vs. classical planning
- **Multi-Agent Coordination**: Nash equilibrium, protocol-based coordination, consensus algorithms

### Related Papers

1. **CodeCRDT** (2510.18893): Observation-driven coordination using CRDTs for concurrent code generation
2. **Agentic AI in SDLC** (2604.26275): Six-layer reference architecture for production agentic systems
3. **Self-Organized Agents** (2404.02183): Independent agents collaborating on large-scale code generation
4. **AgentMesh** (2507.19902): Cooperative multi-agent framework with specialized roles

### Possible Extensions & Future Research

1. **Formal Verification**: Extend typed tools to support formal proof of correctness
2. **Hierarchical Decomposition**: Recursive agent teams for massive codebases
3. **Transfer Learning**: Agents learning from past projects to bootstrap on new domains
4. **Continuous Integration**: Tight feedback loops between agents and CI/CD pipelines
5. **Human-in-the-Loop**: Formal frameworks for human oversight and intervention

---

**Document Created**: 2026-05-27  
**Last Updated**: 2026-05-27
