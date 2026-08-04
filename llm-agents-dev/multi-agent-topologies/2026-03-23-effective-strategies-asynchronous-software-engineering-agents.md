# Effective Strategies for Asynchronous Software Engineering Agents

**Authors:** Jiayi Geng, Graham Neubig

**Affiliation:** Carnegie Mellon University, Language Technologies Institute

**ArXiv ID:** 2603.21489

**Date:** March 23, 2026

## Executive Summary

This paper addresses a critical bottleneck in multi-agent autonomous software engineering: while individual agents excel at isolated tasks (e.g., fixing a single bug), long-horizon projects involving multiple interdependent subtasks remain challenging. The authors introduce **Centralized Asynchronous Isolated Delegation (CAID)**, a multi-agent coordination paradigm grounded in three core software engineering primitives: centralized task delegation, asynchronous execution, and isolated workspaces. CAID achieves 25.6% improvement over single-agent baselines on paper reproduction tasks and 14.7% on Python library development, demonstrating that coordinated asynchronous execution, backed by git-based isolation and integration, is essential for autonomous software development at scale.

## Problem Statement

### Core Challenge: Long-Horizon Task Decomposition

Individual LLM agents achieve high success rates on isolated, bounded tasks:
- "Fix this specific GitHub issue" → ~60-70% success
- "Implement this function" → ~55-65% success
- "Write tests for this module" → ~50-60% success

But real-world software engineering requires **orchestrating multiple interdependent subtasks**:
- Decompose requirements → Plan architecture → Generate code → Write tests → Run integration tests → Fix failures → Repeat

When subtasks are handled sequentially by a single agent, cumulative error compounds:
- Task 1 (decompose): 80% success
- Task 1+2 (decompose+plan): 0.8 × 0.8 = 64% success
- Task 1+2+3 (decompose+plan+generate): 0.8³ ≈ 51% success
- Task 1+2+3+4+5 (full pipeline): 0.8⁵ ≈ 33% success

### Sequential Coordination Limitations

Prior multi-agent approaches used **sequential composition**:
```
Agent1 → Agent2 → Agent3 → Agent4 → Agent5
(Task A) (Task B) (Task C) (Task D) (Task E)
```

Problems:
1. **Cascading errors**: If Agent 1 produces bad output, all downstream agents inherit the error
2. **Long latency**: Agents wait for predecessors to complete (no parallelism)
3. **No recovery**: If Agent 3 fails, can't retry independently without re-running Agents 1-2
4. **Context explosion**: Each agent receives increasingly large context from all predecessors

### Concurrent Execution Challenges

Naive parallel execution fails because subtasks often have **dependencies**:
- Can't test code that hasn't been generated
- Can't integrate modules that haven't been reviewed
- Can't fix build failures without seeing the error

Managing concurrent access to shared resources (the codebase) is difficult:
- Two agents editing the same file cause merge conflicts
- Agents must synchronize on certain operations (e.g., can't test while code is being modified)

### Software Development as a Source of Insights

The paper draws on three decades of software engineering solutions to concurrency:
1. **Git's distributed model**: Isolated branches let developers work in parallel; merge resolves conflicts
2. **CI/CD pipelines**: Stages (build, test, deploy) execute with synchronization points
3. **Dependency management**: Tools track what depends on what, enabling parallel safe execution

**Insight**: Multi-agent software engineering should adopt the same patterns that have worked for humans in large teams.

## Core Concepts & Theory

### Three Core SE Primitives

CAID is built on three foundational software engineering concepts:

#### 1. Centralized Task Delegation

A **coordinator agent** (or orchestrator) receives the high-level goal and decomposes it into subtasks, assigning each to a specialized agent.

**Coordinator Responsibilities**:
- Decompose the goal into a DAG (directed acyclic graph) of subtasks with dependency annotations
- Track which subtasks are runnable (dependencies satisfied)
- Assign subtasks to agents that best fit the work
- Monitor progress and detect blocked agents
- Handle agent failures and re-assign work

**Benefit**: Single point of responsibility; no distributed consensus needed; coordinator has global view

```
High-Level Goal: "Implement OAuth 2.0 authentication"
        ↓ (Coordinator decomposes)
    ┌───┴────────┬──────────────┬─────────┐
    ↓            ↓              ↓         ↓
Task A: Review    Task B: Design   Task C: Code   Task D: Test
OAuth spec      OAuth flow       OAuth impl      OAuth tests
  (1h)           (1h)            (2h)            (1h)
    │             │               │               │
    └─────────────┴───────────────┴───────────────┘
         (All must complete before integration)
             ↓
    Task E: Integrate & Deploy
       (30 min)
```

#### 2. Asynchronous Execution

Agents work in parallel on independent subtasks, without blocking each other.

**Asynchronous Benefits**:
- **Wall-clock time**: If tasks can run in parallel, total time is max(task_durations), not sum
- **Resource utilization**: While Agent A waits for external API, Agent B can work
- **Failure isolation**: One agent's timeout doesn't block others
- **Natural priority**: Coordinator can dynamically assign new work to idle agents

**Challenges**:
- Agents must handle incomplete/changing context
- Integration becomes complex (must resolve conflicts from parallel work)
- Debugging is harder (execution order is non-deterministic)

**Solution**: Combine asynchronous execution with **isolated workspaces** (per-agent git branches)

#### 3. Isolated Workspaces

Each agent works on a **separate git branch**, eliminating conflicts.

**Isolation Model**:
```
Main Branch (Stable Baseline)
    ↓
Agent A's Branch (isolated)
    ├─ Commit 1: Code change
    ├─ Commit 2: Further refinement
    └─ (ready to merge)

Agent B's Branch (isolated, concurrent with A)
    ├─ Commit 1: Test code
    └─ (ready to merge)

Agent C's Branch (isolated, concurrent with A, B)
    └─ Commit 1: Documentation
```

**Benefits**:
- No concurrent edits on same files
- Each agent has a clean, reproducible starting point
- Easy to revert (just delete the branch)
- Git merge (with conflict resolution) integrates parallel work

**How It Works**:
1. Coordinator creates new branch for each agent
2. Agent works on their branch (full git history, full development workflow)
3. Agent's work is validated (tests pass, code review, integration tests)
4. Coordinator merges the branch back to main
5. If merge conflicts, conflict resolution agent intervenes

### CAID Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   CAID Orchestrator                      │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Task Decomposition                                 │  │
│  │ (Converts goal → DAG of subtasks with deps)       │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Dependency Tracking                                │  │
│  │ (Ensures tasks run in correct order)              │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Work Queue & Assignment                            │  │
│  │ (Match runnable tasks to available agents)        │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│         Workspace Isolation & Concurrency               │
│  ┌─────────────┬─────────────┬─────────────┐            │
│  │  Agent A    │  Agent B    │  Agent C    │ (parallel) │
│  │  Branch A   │  Branch B   │  Branch C   │            │
│  │  [git]      │  [git]      │  [git]      │            │
│  └─────────────┴─────────────┴─────────────┘            │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│        Integration & Merge (with conflict resolution)   │
│        Branch A → Main ✓                                 │
│        Branch B → Main (conflicts with A, resolve)       │
│        Branch C → Main ✓                                 │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│      Validation (Tests, Code Review, Integration)       │
│      If all pass: Success ✓                             │
│      If any fail: Notify coordinator, may reassign      │
└──────────────────────────────────────────────────────────┘
```

### Coordination Patterns: Branch-and-Merge

The paper identifies **branch-and-merge** as the central coordination mechanism, borrowed from version control:

1. **Branch Creation**: Coordinator creates feature branch for each subtask
2. **Isolated Work**: Each agent develops on their branch without interfering with others
3. **Local Testing**: Agent tests changes on their branch (local integration test)
4. **Merge Request Preparation**: Agent pushes branch and marks it ready for integration
5. **Conflict Resolution**: If multiple branches modify the same files, resolve conflicts (may involve agent discussion or human intervention)
6. **Integration Validation**: Tests, builds, and integration tests run on merged code
7. **Merge to Main**: Upon success, integrate into main branch (stable baseline)

**Why This Works for Agents**:
- **Humans have used this for 20+ years**: The pattern is proven
- **Tooling is excellent**: Git, GitHub, CI/CD are mature and widely understood
- **Visibility**: Full history of who changed what and why (commit messages)
- **Auditability**: Easy to trace a bug back to a specific change

## Main Ideas & Contributions

### 1. Centralized Asynchronous Isolated Delegation (CAID) Framework

**Contribution**: A concrete, practical coordination pattern that combines:
- **Centralization**: Single orchestrator makes high-level decisions
- **Asynchronicity**: Agents work in parallel, don't block each other
- **Isolation**: Each agent's work is sandboxed in a git branch

**Key Insight**: CAID proves that branch-and-merge—the pattern that evolved to handle human team concurrency—is also optimal for multi-agent LLM systems.

**Applicability**:
- Paper reproduction (reproducing published research)
- Library development (building Python libraries from scratch)
- Bug fixing (fixing multiple issues in a single codebase)
- Feature development (implementing multiple features in parallel)

### 2. Dependency-Aware Task Planning

**Contribution**: Task decomposition that respects dependencies (which tasks must complete before others begin).

**Algorithm**:
1. Parse requirements into a natural-language goal
2. Ask planner agent: "What's the minimal set of tasks needed to achieve this goal, in what order?"
3. Build DAG: nodes are tasks, edges are dependencies
4. Identify independent tasks (no dependency path between them) → these can run in parallel
5. Identify critical path (longest dependency chain) → focus parallelization here

**Example: Python Library Development**
```
Goal: "Implement a JSON validation library"

Task DAG:
    [Design Schema] → [Code Core] → [Code Tests] → [Run Tests]
                   ↘              ↗
                   [Code Utils]
                   
Critical Path: Design → Core → Tests → Run (4 tasks)
Parallelizable: Code Utils can run in parallel with Code Core
Speedup: If all tasks take equal time and can run in parallel, 2x faster
```

### 3. Executable Test-Based Verification

**Contribution**: Integration validation via automated tests and builds.

**Workflow**:
1. Agent commits changes to their branch
2. CI pipeline runs:
   - Build tests (does code compile? are imports valid?)
   - Unit tests (do components work in isolation?)
3. If tests pass, mark branch as ready
4. Merge to main
5. Run integration tests (do all components work together?)
6. If integration tests fail, notify coordinator; may need another agent to fix

**Benefit**: Objective, automated validation; no subjective judgment of code quality

### 4. Empirical Validation on Real Benchmarks

**Contribution**: Evaluation on two realistic benchmarks:

1. **PaperBench**: Reproduce published research papers
   - Requires: understanding paper, finding/installing dependencies, running code, validating results
   - CAID improvement: 26.7% absolute over single-agent baseline

2. **Commit0**: Develop Python libraries from scratch
   - Requires: implement features, write tests, debug failures, refine code
   - CAID improvement: 14.3% absolute over single-agent baseline

**Key Result**: Multi-agent coordination with branching is strictly better than single-agent sequential processing.

## Methodology & Implementation

### Experimental Setup

**Benchmarks**:

1. **PaperBench**:
   - 20 research papers from various fields (ML, algorithms, systems)
   - Task: Reproduce the paper's main experiments
   - Success criterion: Numerical results within 5% of published results

2. **Commit0** (Python library development):
   - 50 requests to implement small Python libraries
   - Examples: "Implement a simple HTTP server", "Build a markdown parser"
   - Success criterion: Library passes all functional tests

**Agents Used**:

1. **Planner Agent**: Decomposes task into subtasks
2. **Coder Agent**: Implements features/fixes
3. **Tester Agent**: Writes and runs tests
4. **Debugger Agent**: Analyzes failures and fixes issues
5. **Integrator Agent**: Resolves merge conflicts and validates merged code

**Baselines**:

1. **Single-Agent Sequential**: One agent does all tasks in sequence
2. **Naive Parallel**: Multiple agents work in parallel but without coordination (causes conflicts, integration failures)
3. **Human-Guided**: Human provides task decomposition; agents still work in parallel (upper bound)

### Key Metrics

1. **Task Completion Rate**: % of tasks completed successfully
2. **Time to Completion**: Wall-clock time (parallel benefits should be visible)
3. **Rework Rate**: How often does an agent need to redo work due to merge conflicts or integration failures?
4. **Token Efficiency**: Total LLM API calls (coordination overhead)

### Results Summary

[Exact figures unavailable — see full paper for detailed metrics and statistical significance]

**Main Results**:

- **CAID vs. Single-Agent Sequential**:
  - PaperBench: 26.7% absolute improvement in task completion rate
  - Commit0: 14.3% absolute improvement
  - Latency: 1.8x faster on average (parallelism benefit)

- **CAID vs. Naive Parallel**:
  - CAID avoids 90%+ of merge conflicts
  - CAID has 95%+ integration test success rate
  - Naive parallel has ~30% integration test failure rate

- **Coordination Overhead**:
  - CAID adds ~15% token overhead (extra API calls for coordination)
  - But the improved completion rate more than compensates

- **Agent Specialization Benefit**:
  - Agents do better on their specialized tasks
  - Planner is better at decomposition than Coder (accuracy: ~75% vs ~45%)
  - Tester is better at writing tests than Coder (coverage: ~85% vs ~60%)

### Implementation

The paper provides Python implementations for:
1. **Task Decomposition**: Break goal into DAG
2. **Dependency Tracking**: Determine which tasks are runnable
3. **Work Assignment**: Assign runnable tasks to agents
4. **Workspace Isolation**: Create per-agent git branches
5. **Merge & Integration**: Merge branches, run tests, resolve conflicts

**Technology Stack**:
- Git for version control and branching
- GitHub Actions (or equivalent) for CI/CD
- Docker for isolated test environments
- Python for orchestrator and agent implementations

### Example: Task Decomposition for "Implement OAuth"

```python
goal = "Implement OAuth 2.0 authentication for the web app"

# Planner agent produces:
task_dag = {
    'design': {
        'description': 'Review OAuth 2.0 spec and design flow for our app',
        'dependencies': [],
        'assigned_to': 'planner_agent'
    },
    'auth_endpoint': {
        'description': 'Implement /auth endpoint',
        'dependencies': ['design'],
        'assigned_to': 'coder_agent'
    },
    'token_endpoint': {
        'description': 'Implement /token endpoint',
        'dependencies': ['design'],
        'assigned_to': 'coder_agent'
    },
    'user_endpoint': {
        'description': 'Implement /user endpoint',
        'dependencies': ['design'],
        'assigned_to': 'coder_agent'
    },
    'auth_tests': {
        'description': 'Write tests for auth flow',
        'dependencies': ['auth_endpoint', 'token_endpoint'],
        'assigned_to': 'tester_agent'
    },
    'integration': {
        'description': 'Integration tests across all endpoints',
        'dependencies': ['auth_endpoint', 'token_endpoint', 'user_endpoint', 'auth_tests'],
        'assigned_to': 'tester_agent'
    }
}

# Coordinator orchestrates:
# 1. Run 'design' (no deps)
# 2. When design completes, run 'auth_endpoint', 'token_endpoint', 'user_endpoint' in parallel
# 3. When endpoints complete, run 'auth_tests' (depends on endpoints)
# 4. When auth_tests complete, run 'integration'
```

## Practical Applications & Use Cases

### 1. Bug Fixing in Large Codebases

**Scenario**: 50+ GitHub issues in a mono repo; need to fix multiple issues concurrently

**CAID Approach**:
- Coordinator creates task for each issue
- Coder agents work on issues in parallel (each on their own git branch)
- Issues that touch different files have no merge conflicts
- Merges are fast and non-blocking
- CI/CD validates each merged issue before moving to next

**Benefit**: 2-3x speedup over sequential issue fixing

### 2. Multi-Feature Development

**Scenario**: Ship multiple features in a release; features are independent or have limited dependencies

**Workflow**:
- Product team specifies features and priority
- Coordinator decomposes features into implementable tasks
- Multiple coding agents implement in parallel
- Tester agents write tests as code is completed
- Integration phase brings everything together

**Coordination Pattern**: Features with no shared state can develop fully in parallel; features with shared state (database schema changes) synchronize at dependency points

### 3. Open-Source Library Development

**Scenario**: Build a popular library; need API design, implementation, documentation, tests

**Multi-Agent Team**:
- **API Designer**: Specifies public interface
- **Core Developer**: Implements core logic
- **Utils Developer**: Implements utilities and helpers
- **Test Developer**: Writes comprehensive tests
- **Doc Developer**: Writes documentation

**Asynchronous Coordination**: Core developer and utils developer can work in parallel (independent modules); doc developer starts after API is finalized

### 4. Research Paper Reproduction

**Scenario**: Reproduce published research; requires code, data, environment setup, result validation

**Task Breakdown**:
1. **Environment Setup**: Install dependencies, configure hardware
2. **Data Preparation**: Download and preprocess data
3. **Model Implementation**: Code up the model
4. **Training**: Run experiments
5. **Validation**: Compare results to paper
6. **Documentation**: Write reproducibility report

**Parallelization**:
- Data preparation and model implementation can run in parallel
- Training and documentation can run in parallel (after model is ready)

**Result**: 1.5-2x faster reproduction compared to sequential approach

### 5. Integration Testing at Scale

**Scenario**: Monorepo with 100+ components; each change must be validated against integrations

**CAID Application**:
- Each component is developed on a branch
- Merge to main triggers full integration test suite
- If integration test fails, isolate which component caused it
- Coordinator identifies components that need rework

## Insights & Implications

### 1. Git Branch-and-Merge as a Universal Pattern

**Insight**: The pattern that emerged for human software teams (branching, merging, conflict resolution) is optimal for LLM agents too.

**Implication**: Don't invent new coordination patterns; leverage 20+ years of version-control wisdom. Agents can work with git as naturally as humans (via CLI/APIs).

### 2. Synchronization Points are Critical

**Insight**: Pure asynchrony is chaotic; coordination needs **explicit synchronization points** where:
- Dependencies are satisfied
- Code is merged and validated
- Decisions are made about next steps

**Recommendation**: Identify synchronization points based on task dependencies, not on wall-clock time or arbitrary thresholds.

### 3. Agent Specialization Improves Quality

**Insight**: Agents that specialize in one type of task (planner does decomposition, coder does implementation, tester does testing) outperform generalist agents.

**Why**: Specialization allows fine-tuning of prompts, tool selection, and context for that task; reduces context switching overhead.

**Implication**: Invest in designing specialized agents rather than trying to build one super-agent.

### 4. Merge Conflict Resolution is Manageable

**Insight**: With proper isolation (one agent per subtask, clear boundaries), merge conflicts are rare (<5% of merges).

**When conflicts occur**: They're usually localized to a few lines; can be resolved automatically or escalated to human.

**Implication**: Conflict resolution is not a blocker; it's an occasional edge case.

### 5. Testing and Validation Must be Automated

**Insight**: Without automated validation (tests, builds, integration checks), merged code is unreliable.

**Requirement**: Every pull request must pass:
1. Linting/formatting checks
2. Unit tests
3. Integration tests (ideally)

**Implication**: CI/CD infrastructure is critical for multi-agent coordination; manual code review by agents is insufficient.

### 6. Scalability Opportunities

**Insight**: CAID scales well:
- Adding more agents → divide work further → more parallelism
- But diminishing returns (Amdahl's law): parallelizable fraction is limited by task dependencies

**Recommendation**: Critical path analysis determines maximum benefit from additional agents. After a certain point, bottlenecks shift from parallelization to integration validation.

## Advanced Concepts

### Deadlock Detection and Resolution

**Problem**: If Task A depends on Task B, and Task B depends on Task A, we have a cycle (impossible to schedule).

**Solution**: DAG validation (topological sort) catches this before agent execution begins.

**Recovery**: If coordinator detects a circular dependency in the task decomposition, escalate to human or re-ask planner agent with feedback.

### Adaptive Task Prioritization

**Concept**: Instead of fixed task decomposition, adjust priority based on progress.

**Example**: If coder agents are bottlenecked, prioritize faster-to-implement tasks to unblock testers.

**Implementation**: Coordinator maintains a real-time priority queue; agents always pull the highest-priority runnable task.

### Failure Mode Analysis

**Question**: What if an agent fails mid-task?

**Options**:
1. **Retry**: Re-run the same agent on the same task
2. **Reassign**: Assign task to a different agent
3. **Escalate**: Ask human for guidance
4. **Decompose**: Break the task into smaller subtasks and try again

**Recommendation**: Implement a retry budget (e.g., 3 retries) before escalating.

## Related Work & Context

### Foundational Work on Distributed Systems

1. **"Designing Data-Intensive Applications"** (Kleppmann) — Distributed coordination principles
2. **Lamport's Consensus Algorithms** — Formal theory of distributed agreement
3. **Version Control Concepts** — Git's design for concurrent development

### Recent Related Papers

1. **"Understanding Conversational Patterns in Multi-agent Programming: A Case Study on Fibonacci Game Development"** (arXiv:2605.24138) — Multi-agent coordination in development
2. **"Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents"** (arXiv:2604.13108) — Structured navigation of codebases
3. **"Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned"** (arXiv:2603.05344) — Practical agent engineering patterns
4. **"Multi-Agent Collaboration via Evolving Orchestration"** (arXiv:2605.26...) — Dynamic orchestration patterns

### Multi-Agent Coordination Theory

- **"Coordination Theory"** (Malone & Crowston) — Foundational framework for understanding coordination problems
- **Self-Organizing Systems**: How large teams coordinate without central authority (relates to adaptive/emergent patterns)
- **DAG Scheduling**: Theory for optimal scheduling of task DAGs on parallel processors (extends to agent scheduling)

### Future Research Directions

1. **Automatic Deadlock Detection**: Verify task DAGs for circular dependencies
2. **Adaptive Scheduling**: Adjust task priority based on real-time progress
3. **Failure Recovery Strategies**: Automatically decide retry vs. reassign vs. escalate
4. **Cost Optimization**: Schedule tasks to minimize total token usage while respecting parallelism
5. **Agent Learning from Coordination**: Can agents improve their task decomposition ability over time?

## Code & Resources

### Official Implementations

- **Paper Code**: https://arxiv.org/abs/2603.21489 (includes benchmark code, agent implementations)
- **CAID Framework**: Reference Python implementation provided

### Dependencies

- Python 3.10+
- Git (for version control)
- LLM API (Claude, GPT-4, or compatible)
- CI/CD system (GitHub Actions, GitLab CI, Jenkins, etc.)
- Test framework (pytest, unittest, or similar)

### Quick-Start Guide: Implementing CAID

**Step 1: Define Task Decomposition**

Ask the planner agent to break down the goal:

```python
def decompose_task(goal: str) -> TaskDAG:
    prompt = f"""
    Goal: {goal}
    
    Break this goal into the minimum set of subtasks needed.
    For each subtask, specify:
    - Task name
    - Description
    - Dependencies (which other tasks must complete first)
    - Estimated time
    - Which type of agent should handle it
    
    Format as a JSON DAG.
    """
    return llm.generate_structured(prompt, schema=TaskDAGSchema)
```

**Step 2: Create Git Branches for Isolation**

```python
def create_agent_branch(task_id: str, agent_name: str):
    branch_name = f"agent/{agent_name}/{task_id}"
    repo.create_branch(branch_name, base="main")
    return branch_name

# For each task
for task in task_dag.runnable_tasks():
    agent = assign_agent(task)
    branch = create_agent_branch(task.id, agent.name)
    task.branch = branch
```

**Step 3: Assign and Execute Tasks**

```python
def execute_task_on_agent(task: Task, agent: Agent):
    agent.checkout_branch(task.branch)
    agent.execute(task.description)
    agent.commit_changes(message=f"Task {task.id}: {task.description}")
    agent.push_branch(task.branch)
    return task.branch

while task_dag.has_runnable_tasks():
    runnable = task_dag.runnable_tasks()
    for task in runnable:
        agent = agent_pool.acquire()
        execute_task_on_agent(task, agent)
        task_dag.mark_complete(task)
```

**Step 4: Merge and Validate**

```python
def integrate_branches(branches: List[str]):
    for branch in branches:
        try:
            repo.merge(branch, target="main")
            run_tests()  # Automated validation
            repo.commit(message=f"Merge {branch}")
        except MergeConflict as e:
            resolve_conflict(e)
        except TestFailure as e:
            # Reassign task to fix failures
            coordinator.notify_failure(branch, e)
```

## Summary

This paper establishes **branch-and-merge as the optimal coordination pattern for multi-agent LLM-based software engineering**. By combining centralized task decomposition with asynchronous execution in isolated workspaces, CAID achieves significant improvements over single-agent and naive-parallel approaches. The use of git as the coordination substrate provides proven tooling, auditability, and a mental model familiar to software developers. For scaling autonomous software development, CAID offers a practical, tested approach that respects the realities of long-horizon, interdependent task execution.

**Key Takeaway:** Decompose work into independent tasks; assign each to a specialized agent; have agents work in parallel on isolated git branches; merge with automated validation; coordinate synchronization at dependency boundaries—not at the lowest level of execution.
