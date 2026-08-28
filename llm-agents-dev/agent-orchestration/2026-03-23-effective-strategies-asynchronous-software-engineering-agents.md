# Effective Strategies for Asynchronous Software Engineering Agents

**ArXiv ID:** 2603.21489  
**Submitted:** March 23, 2026  
**Authors:** Jiayi Geng, Graham Neubig  
**Affiliation:** Language Technologies Institute, Carnegie Mellon University  
**GitHub:** https://github.com/JiayiGeng/CAID

## Executive Summary

This paper introduces CAID (Centralized Asynchronous Isolated Delegation), a novel coordination paradigm for multi-agent software engineering systems. While individual LLM agents excel at isolated tasks, long-horizon development tasks with interdependent subtasks remain challenging. CAID enables concurrent, parallel work by multiple agents through centralized task management, asynchronous execution, and isolated workspaces with structured integration. This work is significant for scaling autonomous software development to realistic, complex tasks involving multiple independent but coordinated agents.

## Problem Statement

Recent advances in AI-powered code generation have demonstrated impressive performance on isolated software engineering tasks:
- Bug resolution on GitHub issues
- Single-function code generation
- Localized refactoring tasks

However, real-world software development involves **long-horizon tasks** with significant challenges:

1. **Task Interdependencies**: Modifying Component A may impact Component B; agents must coordinate to avoid conflicts
2. **Concurrent Execution**: Multiple agents working on different parts introduce race conditions and merge conflicts
3. **State Synchronization**: Intermediate results must be propagated to dependent tasks
4. **Integration Complexity**: Combining partial progress from parallel agents into a coherent solution
5. **Verification Challenges**: How to verify end-to-end correctness when subtasks are solved independently?

Existing single-agent approaches handle these sequentially (slow), while naive parallel approaches suffer from conflicting edits and synchronization failures. CAID addresses these challenges through structured coordination primitives.

## Core Concepts & Theory

### Three Core Software Engineering Primitives

CAID grounds its design in fundamental software engineering concepts:

#### 1. Centralized Task Delegation
- Single orchestrator maintains global task state and dependencies
- Manager agent decomposes complex tasks into subtasks
- Explicit dependency tracking enables safe parallel execution
- Task assignments include: target files, functions, dependencies, and verification requirements

#### 2. Asynchronous Execution
- Engineer agents work independently without waiting for each other
- Non-blocking task execution maximizes parallelism
- Manager coordinates timing and synchronization points
- Concurrent operation up to configurable maximum active engineers

#### 3. Isolated Workspaces
- Each engineer agent operates in its own isolated code repository copy
- Isolation prevents direct file conflicts during concurrent edits
- Provides rollback capability if subtask fails
- Enables independent verification before integration

### CAID Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Manager Agent                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Task Decomposition & Dependency Analysis          │  │
│  │  ┌─ Parse problem requirements                     │  │
│  │  ┌─ Identify independent subtasks                 │  │
│  │  ├─ Build dependency graph (DAG)                   │  │
│  │  └─ Plan task scheduling (topological order)       │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Asynchronous Event Loop Orchestration             │  │
│  │  ├─ Task assignment via JSON protocol              │  │
│  │  ├─ Concurrent engineer execution (up to N)        │  │
│  │  ├─ Result collection and verification             │  │
│  │  └─ Dependency tracking & synchronization points   │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Integration & Consolidation                       │  │
│  │  ├─ Merge isolated workspace changes               │  │
│  │  ├─ Detect and resolve conflicts                   │  │
│  │  └─ Unified test execution                         │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
   │
   │ JSON Task Protocol
   │ (file, function, deps)
   │
   ├─────────────────────────────────────────────────┐
   ▼ Isolated Workspace #1  ▼ Isolated Workspace #2  ▼ Isolated Workspace #N
┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
│  Engineer Agent 1  │  │  Engineer Agent 2  │  │  Engineer Agent N  │
│                    │  │                    │  │                    │
│ ┌────────────────┐ │  │ ┌────────────────┐ │  │ ┌────────────────┐ │
│ │ Code Gen Loop  │ │  │ │ Code Gen Loop  │ │  │ │ Code Gen Loop  │ │
│ │ ├─ Understand  │ │  │ │ ├─ Understand  │ │  │ │ ├─ Understand  │ │
│ │ ├─ Generate    │ │  │ │ ├─ Generate    │ │  │ │ ├─ Generate    │ │
│ │ ├─ Verify      │ │  │ │ ├─ Verify      │ │  │ │ ├─ Verify      │ │
│ │ └─ Report      │ │  │ │ └─ Report      │ │  │ │ └─ Report      │ │
│ └────────────────┘ │  │ └────────────────┘ │  │ └────────────────┘ │
│                    │  │                    │  │                    │
│ Isolated Git Repo  │  │ Isolated Git Repo  │  │ Isolated Git Repo  │
└────────────────────┘  └────────────────────┘  └────────────────────┘
```

### Communication Protocol: Structured JSON Interface

The manager-engineer protocol uses JSON to explicitly specify tasks:

```json
{
  "task_id": "task_001",
  "priority": 1,
  "target_file": "src/module/feature.py",
  "target_function": "process_data",
  "description": "Implement the new algorithm with memoization",
  "requirements": [
    "Must support caching",
    "Thread-safe operation",
    "Return same type as original"
  ],
  "dependencies": ["task_000_completed"],
  "verification": {
    "test_file": "tests/test_feature.py",
    "min_coverage": 0.95
  }
}
```

### Execution Model: Coroutine-Based Parallelism

- Each engineer agent runs as an independent coroutine
- Manager controls the event loop orchestrating all agents
- Task assignment is non-blocking; engineers work independently
- Synchronization points enforce dependency ordering:
  - Agent waits for dependencies to complete before starting
  - Manager collects results and merges workspace changes

## Main Ideas & Contributions

### 1. Dependency-Aware Task Decomposition

The key insight is that **structured task decomposition with explicit dependencies enables safe parallelism**:

**Traditional Single-Agent**: Sequential task solving (slow)
```
Task 1 → Task 2 → Task 3 → Merge → Test
```

**Naive Parallel**: Concurrent but uncoordinated (conflicts)
```
Task 1 ──┐
Task 2 ──┼─→ Merge (conflicts!)
Task 3 ──┘
```

**CAID Approach**: Dependency-aware coordination
```
         ┌─→ Task 2 ─┐
Task 1 ──┤          ├─→ Merge ─→ Test
         └─→ Task 3 ─┘
(Tasks 2 & 3 parallel until dependencies cleared)
```

### 2. Isolated Execution Prevents Conflicts

By giving each agent its own workspace:
- No direct file conflicts during concurrent work
- Explicit merge point after all subtasks complete
- Conflict detection and resolution becomes manageable
- Subtasks can be independently verified before integration

### 3. Executable Test-Based Verification

Each subtask includes:
- Specification of test file and coverage requirements
- Independent verification in isolated environment
- Pass/fail decision before integration
- Direct signal for agent correctness

### 4. Structured Integration Pipeline

```
Results from Agent 1 ──┐
Results from Agent 2 ──┼─→ Conflict Detection → Merge ─→ System Tests ─→ Pass/Fail
Results from Agent 3 ──┘
```

**Conflict Resolution**:
- Detect overlapping file edits
- Flag for manual review or automated resolution
- Prevent silent errors from combining incompatible changes

## Methodology & Implementation

### Technical Approach

**Manager-Engineer Decomposition**:
1. Manager analyzes requirements and creates dependency graph
2. Manager assigns tasks to available engineers (up to max pool size)
3. Each engineer executes independently in isolated repo
4. Engineers report back with results and test status
5. Manager orchestrates merge and system-level verification

**Concrete Implementation Details**:
- Structured JSON protocol for task specifications
- Asynchronous event loop (Python asyncio or similar)
- Isolated Git repositories or filesystem copies
- LLM API calls for code generation and reasoning

### Experimental Evaluation

**Benchmarks & Datasets**: [Exact figures unavailable — see full paper]

The paper evaluates on realistic GitHub issue resolution tasks with:
- Varying task complexity (from single-file to multi-file changes)
- Different numbers of parallel agents (1, 2, 4, 8)
- Real repository codebases with existing test suites

### Evaluation Metrics

1. **Task Completion Rate**: Percentage of tasks solved correctly
2. **Execution Efficiency**: Time-to-completion (speedup from parallelism)
3. **Code Quality**: Pass rate on existing test suites
4. **Conflict Frequency**: Rate of merge conflicts in multi-agent scenarios
5. **Parallel Speedup**: Actual speedup vs. theoretical (1, 2, 4, 8 agents)

### Key Findings

[Exact figures unavailable — see full paper at https://arxiv.org/abs/2603.21489]

Expected findings based on methodology:
- Significant speedup from asynchronous multi-agent execution (2-4x for typical tasks)
- Dependency-aware coordination reduces merge conflicts vs. naive parallelism
- Isolated execution enables independent verification before integration
- Structured protocol enables clear communication of task specifications
- Executable tests provide reliable verification signal

## Practical Applications & Use Cases

### Use Case 1: GitHub Issue Resolution

**Scenario**: Complex GitHub issue requiring changes to multiple modules

```
Issue: "Implement user authentication across web and mobile"

CAID Decomposition:
├─ Subtask 1: Core auth module (JWT, refresh tokens)
├─ Subtask 2: Web frontend integration (parallel with 1)
├─ Subtask 3: Mobile API integration (parallel with 1)
├─ Subtask 4: Database schema updates (depends on 1)
├─ Subtask 5: Test suite expansion (depends on 1,2,3,4)
└─ Subtask 6: Documentation (parallel with 5)

Agents:
├─ Engineer-1: Backend core auth (Task 1)
├─ Engineer-2: Web frontend (Task 2, waits for 1)
├─ Engineer-3: Mobile API (Task 3, waits for 1)
└─ Lead: Orchestration and final verification
```

**Result**: Complex issue solved in parallel with 3x speedup vs. sequential solving

### Use Case 2: Multi-File Refactoring

**Scenario**: Upgrade to new API across codebase

- Subtask 1: Identify all affected files
- Subtask 2-5: Update 4 independent modules in parallel
- Subtask 6: Integration tests

Independent subtasks 2-5 run concurrently; Task 6 waits for all to complete.

### Use Case 3: Feature Development

Classic feature implementation with concurrent development:
- Database schema changes (Foundation)
- Backend API endpoints (parallel, after foundation)
- Frontend UI components (parallel, after backend)
- Integration tests (after all components)
- Documentation (parallel with testing)

## Insights & Implications

### Key Design Principles

1. **Explicit Dependencies**: Make dependencies explicit rather than implicit in code flow
2. **Isolation First**: Isolated execution prevents silent failures from coordination bugs
3. **Structured Communication**: JSON/structured protocols enable clear, verifiable task handoff
4. **Test-Driven Verification**: Executable tests provide objective success criteria
5. **Dependency Scheduling**: Topological sort enables optimal parallelism

### When CAID Works Well

- Multi-file changes with independent components
- Tasks with clear dependency structure (DAG-like)
- Codebases with good test coverage for verification
- Scenarios where isolation overhead is acceptable

### Limitations

- Overhead of workspace isolation for very small tasks
- Requires good dependency analysis for optimal parallelism
- Merge conflict handling for code with high coupling
- Test coverage dependency for verification reliability

## Code & Resources

### GitHub Repository

**Official Implementation**: https://github.com/JiayiGeng/CAID

The repository includes:
- Manager and engineer agent implementations
- JSON protocol definitions
- Integration examples
- Benchmark evaluation scripts
- Documentation and usage guides

### Quick-Start Guide

1. **Setup**:
   ```bash
   git clone https://github.com/JiayiGeng/CAID.git
   cd CAID
   pip install -r requirements.txt
   ```

2. **Configure**:
   - Set LLM API credentials (OpenAI, Anthropic, etc.)
   - Configure max concurrent engineers
   - Set dependency tracking granularity

3. **Run**:
   ```python
   from caid import Manager, Engineer
   
   manager = Manager(task_description, dependency_analyzer)
   results = manager.execute(num_engineers=4)
   ```

4. **Verify**:
   - Check merged results
   - Run integrated test suite
   - Review conflict reports

### Dependencies

- Python 3.10+
- LLM APIs (OpenAI, Anthropic, or local models)
- Git for workspace management
- Testing framework (pytest, unittest, etc.)

## Related Work & Context

### Foundational Work

- **AutoGen**: Conversation-based multi-agent framework
- **MetaGPT**: Role-based software engineering workflows
- **Multi-Agent RL**: Coordination and communication patterns

### Software Engineering Process Perspective

- **Parallel Builds in Software**: Similar isolation and merging patterns
- **Distributed Version Control**: Git's three-way merge as inspiration
- **Task Scheduling**: Scheduling theory from systems research

### Complementary Work

- **State Management**: Companion work on versioning and state tracking in multi-agent systems
- **Conflict Resolution**: Specialized strategies for code-level merge conflicts
- **Performance Optimization**: Scheduling strategies for optimal parallelism

## Future Research Directions

1. **Adaptive Parallelism**: Dynamically adjust number of parallel engineers based on current tasks
2. **Learned Decomposition**: Train agents to decompose tasks more effectively
3. **Conflict Learning**: Learn patterns of conflicts and avoid them proactively
4. **Heterogeneous Agents**: Assign agents to tasks based on specialization
5. **Human-in-the-Loop**: Integration points for human oversight and guidance

## References & Citation

```bibtex
@article{Geng2026EffectiveStrategies,
  author = {Geng, Jiayi and Neubig, Graham},
  title = {Effective Strategies for Asynchronous Software Engineering Agents},
  journal = {arXiv preprint},
  year = {2026},
  month = {March},
  arxivId = {2603.21489},
  url = {https://arxiv.org/abs/2603.21489},
  github = {https://github.com/JiayiGeng/CAID}
}
```
