# A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function and Execution Topology

**Authors:** Jia Huang, Joey Tianyi Zhou  
**Affiliations:** Agency for Science, Technology and Research (A*STAR), Centre for Frontier AI Research (CFAR), Singapore  
**ArXiv ID:** 2605.13850  
**Submission Date:** May 2026  
**Focus Area:** Agent architecture design, design patterns, multi-agent topologies

## Executive Summary

This paper identifies and addresses a critical ambiguity in agent design: existing frameworks focus exclusively on either *what agents do* (cognitive function) or *how they're structured* (execution topology), but conflate these orthogonal dimensions. The paper introduces a **two-dimensional taxonomy** that disambiguates agent design patterns by their cognitive functions (seven categories) and execution topologies (six archetypes), revealing that the same topology can implement fundamentally different patterns with distinct failure modes, performance characteristics, and deployment constraints. This framework is essential for software development automation, where choosing the right agent topology-function combination determines whether multi-agent systems succeed or fail.

## Problem Statement

### The Topology-Function Ambiguity

Current agent design frameworks suffer from a critical gap in clarity:

**Industry Guides Focus on Topology:** AWS, Microsoft, and open-source frameworks (LangChain, AutoGen) emphasize execution topology—how data flows through the system (chain, parallel, hierarchical, etc.). However, they rarely discuss *what cognitive functions* are being implemented.

**Academic Surveys Focus on Cognition:** Cognitive science literature categorizes agents by their decision-making functions (reasoning, planning, memory, reflection) but is largely disconnected from practical system topology.

**The Result:** Teams often confuse fundamentally different systems. For example, three distinct agent patterns all use an "Orchestrator-Workers" topology but have entirely different:
- **Failure modes:** Plan-and-Execute fails when the plan is wrong; Hierarchical Delegation fails when coordinators bottleneck; Adversarial Verification requires strict communication protocols
- **Scaling properties:** Plan-and-Execute scales poorly to 100+ workers; Hierarchical Delegation with sub-coordinators scales better
- **Design requirements:** Verification patterns need reliable agents; Planning patterns need good planners

### Motivating Example: Code Review Agents

Three teams use the same "Orchestrator-Workers" topology for code review:

**Team A (Plan-and-Execute):**
```
Orchestrator: Generates a review plan (check coverage, security, performance, style)
Workers: Execute each check independently
Combine: Merge results into final review
```
Failure: If the generated plan omits a critical check (e.g., thread safety), all workers execute the incomplete plan.

**Team B (Hierarchical Delegation):**
```
Orchestrator: Routes code sections to specialized reviewers
Sub-coordinators: Architecture team, Security team, Performance team
Workers: Individual reviewers within each team
```
Failure: Bottleneck at the orchestrator or sub-coordinators if traffic is uneven.

**Team C (Adversarial Verification):**
```
Orchestrator: Proposes a code review
Workers: Review the review (critique, find holes)
Orchestrator: Refine review based on critiques
Workers: Re-verify
```
Failure: Requires trustworthy workers (they must be able to critique competently), and may not converge.

Without clear terminology, teams cannot discuss trade-offs or learn from each other's experiences.

## Core Concepts & Theory

### Dimension 1: Cognitive Functions (Seven Categories)

Agents implement one or more of these cognitive functions:

| Function | Definition | Example in Dev Automation |
|----------|-----------|---------------------------|
| **Perception** | Observing and interpreting environment/task state | Reading code files, understanding requirements, monitoring execution |
| **Memory** | Storing, retrieving, and updating context/knowledge | Maintaining conversation history, caching analysis results, version tracking |
| **Reasoning** | Inferring conclusions from observations and knowledge | Analyzing code patterns, diagnosing bugs, planning solutions |
| **Action** | Taking steps to modify the environment | Writing code, committing changes, invoking APIs |
| **Reflection** | Evaluating outcomes and learning from experience | Checking test results, analyzing code coverage, refining prompts |
| **Collaboration** | Coordinating with other agents | Delegating tasks, sharing findings, aggregating results |
| **Governance** | Enforcing constraints, monitoring compliance, managing risk | Approval workflows, access control, audit logging |

Each agent or team specializes in one or more of these functions.

### Dimension 2: Execution Topology (Six Archetypes)

Agent systems are structured according to one or more of these topologies:

#### 1. **Chain**
```
A₁ → A₂ → A₃ → ... → Aₙ
```
**Characteristics:** Linear, sequential execution. Each agent's output feeds into the next.
**When Used:** Single-threaded, deterministic workflows (compile → test → deploy)
**Software Dev Examples:** Build pipeline, code transformation chain, documentation generation
**Time Constraint:** Seconds only; adds latency proportional to number of agents

#### 2. **Route**
```
     ┌─→ A₂ ──┐
A₁ ──┤        ├─→ Result
     └─→ A₃ ──┘
```
**Characteristics:** Conditional branching; one of several agents processes the task.
**When Used:** Classification-based delegation (route to the right specialized agent based on task type)
**Software Dev Examples:** Route code changes to appropriate reviewer specialty, route tickets to experts
**Time Constraint:** Minutes to hours; depends on router accuracy

#### 3. **Parallel**
```
     ┌─→ A₁ ──┐
Task ┤─→ A₂ ──┼─→ Aggregate
     └─→ A₃ ──┘
```
**Characteristics:** All agents process the same task independently; results are aggregated.
**When Used:** Ensemble approaches, redundancy, diverse perspectives
**Software Dev Examples:** Multiple code reviewers in parallel, multiple test generators voting on coverage
**Time Constraint:** Hours to days; enables longer, more thorough analysis

#### 4. **Orchestrate**
```
         Coordinator
            │
    ┌───┬───┴────┬───┐
    ↓   ↓        ↓   ↓
    A₁  A₂       A₃  A₄
```
**Characteristics:** Central orchestrator manages task decomposition and delegation.
**When Used:** Complex workflows with inter-agent dependencies
**Software Dev Examples:** Test generation orchestrator that coordinates unit test generator, integration test generator, performance test generator
**Time Constraint:** Days to weeks; complex tasks benefit from adaptive orchestration

#### 5. **Loop**
```
    Task
      ↓
    Agent
      ↓
    Check
      ↓
    [Good?] ──No──┐
      │            │
      │            ↓
      │          Update
      │            │
      └────────────┘
      Yes
      ↓
    Result
```
**Characteristics:** Iterative execution with feedback-driven refinement.
**When Used:** Convergence problems, multi-stage refinement
**Software Dev Examples:** Iterative test generation (generate tests → run → fail → refine → repeat)
**Time Constraint:** Hours to days; useful when single-pass solutions are insufficient

#### 6. **Hierarchy**
```
         Master
          / \
        M₁   M₂
        / \   / \
       A₁ A₂ A₃ A₄
```
**Characteristics:** Multi-level agent structure with recursion; coordinators manage sub-teams.
**When Used:** Large-scale problems requiring recursive decomposition
**Software Dev Examples:** Large codebase refactoring: master decomposes into modules, each module has a coordinator and workers
**Time Constraint:** Days to weeks; scales to large problems but adds coordination complexity

### Design Pattern Classification

The framework enables precise classification of 28+ design patterns (7 cognitive functions × 4 primary topology combinations):

**Example: Five Distinct Code Review Patterns**

| Pattern | Cognitive | Topology | Failure Mode | Best Use Case |
|---------|-----------|----------|-------------|------------------|
| Plan-and-Execute | Reasoning + Action | Chain + Parallel | Wrong plan | Standardized reviews (style, coverage) |
| Hierarchical Delegation | Collaboration + Governance | Hierarchy | Coordinator bottleneck | Large teams, specialized reviewers |
| Adversarial Verification | Reflection + Reasoning | Loop | Non-convergence | High-stakes reviews requiring robustness |
| Multi-Reviewer Ensemble | Reasoning + Collaboration | Parallel | Conflicting reviews | Complex code requiring diverse expertise |
| Streaming Router | Perception + Collaboration | Route + Loop | Misclassification | High-volume, heterogeneous tasks |

### Time-Complexity Trade-offs

The framework reveals relationships between **time constraints** and **viable topologies**:

```
┌──────────────────────────────────────────────────────────────┐
│ Time Pressure vs. Viable Topologies                          │
├──────────────────────────────────────────────────────────────┤
│ Seconds (real-time):     Chain only                          │
│ Minutes:                 Chain, Route                        │
│ Hours:                   Chain, Route, Parallel, Loop        │
│ Days:                    Route, Parallel, Loop, Orchestrate  │
│ Weeks+:                  Any topology (Hierarchy, Recursion) │
└──────────────────────────────────────────────────────────────┘
```

This explains why real-time systems (seconds) must use Chain topology (sequential, minimal coordination), while research tasks (weeks) can afford Hierarchy (complex multi-level decomposition).

## Main Ideas & Contributions

### 1. Disambiguation Through Orthogonal Dimensions

**Core Insight:** Cognitive function (what) and execution topology (how) are independent. Conflating them obscures design choices.

**Example:** "Hierarchical Agent" is ambiguous:
- Could mean hierarchical reasoning (cognitive)
- Could mean hierarchical topology (structural)
- Could mean both

**Clarification:** Using the framework:
- "Hierarchy + Reasoning" = hierarchical task decomposition with planning at each level
- "Hierarchy + Reflection" = hierarchical verification (peer review at each level)
- "Hierarchy + Collaboration" = hierarchical delegation (coordinators manage workers)

### 2. Design Trade-offs Become Explicit

The framework reveals why certain patterns fail in certain contexts:

**Plan-and-Execute (Reasoning + Orchestrate):**
- ✓ Efficient: All workers execute in parallel once plan is made
- ✗ Brittle: Any error in planning propagates to all workers
- ✗ Poor for ambiguous tasks: Plan may miss critical checks

**Hierarchical Delegation (Collaboration + Hierarchy):**
- ✓ Flexible: Coordinators adapt assignments based on feedback
- ✓ Scalable: Distributed coordination avoids bottlenecks
- ✗ Overhead: Each coordinator adds latency and coordination cost
- ✗ Complex: Requires careful role definition

**Adversarial Verification (Reflection + Loop):**
- ✓ Robust: Iterative refinement catches errors
- ✓ Learns from failure: Loop improves as agents get feedback
- ✗ Convergence risk: May iterate indefinitely on hard problems
- ✗ Worker quality dependent: Requires capable critique agents

### 3. Scalability Laws Emerge

Different topologies scale differently with team size:

```
Architecture       N=5    N=10   N=50   N=100  N=500
─────────────────────────────────────────────────────
Chain              OK     OK     OK     OK     OK (slow)
Route              OK     OK     OK     OK     Risk (load)
Parallel           OK     OK     Risk   Risk   Risk (merge)
Orchestrate        OK     OK     Risk   Risk   Hard
Loop               OK     OK     Risk   Hard   Hard
Hierarchy          OK     OK     OK     OK     OK
```

Hierarchy with recursion is the only pattern that scales to very large teams (100+).

## Methodology & Implementation

### Empirical Validation

The paper validates the framework through:

1. **Comparative Case Studies:** Six agent systems from industry/academia, classified using the framework
2. **Design Exploration:** How the framework helps teams avoid design errors
3. **Scaling Studies:** Measuring performance of different topologies as team size increases

### Case Studies in Software Engineering

**Case A: Automated Code Review System (Company X)**
- Initial Design: Plan-and-Execute (Reasoning + Chain)
- Problem: Generated review plan missed security checks
- Redesign: Hierarchical Delegation (Collaboration + Hierarchy)
- Outcome: Specialized security team added, better coverage

**Case B: Multi-Agent Test Generation (Company Y)**
- Initial Design: Parallel Ensemble (Reasoning + Parallel)
- Problem: Test deduplication was expensive; many redundant tests
- Redesign: Orchestrated generation (Reasoning + Orchestrate)
- Outcome: Orchestrator learned to partition test space, reducing redundancy

**Case C: Long-Horizon Task Planning (Company Z)**
- Initial Design: Hierarchy (Reasoning + Hierarchy)
- Problem: Hierarchical plans became outdated as task unfolded
- Redesign: Hierarchy + Loop (Reasoning + Reflection + Hierarchy + Loop)
- Outcome: Periodic re-planning at each level improved success rate

### Implementation Guide

**Step 1: Define Cognitive Functions**
List which functions your system needs: Perception, Memory, Reasoning, Action, Reflection, Collaboration, Governance

**Step 2: Choose Primary Topology**
Based on time constraints and task structure, select primary topology (Chain, Route, Parallel, Orchestrate, Loop, Hierarchy)

**Step 3: Identify Hybrid Patterns**
Many real systems combine 2-3 topologies. Document the combination explicitly.

**Step 4: Analyze Failure Modes**
For each component, identify how failures could propagate. Use the framework's known failure modes as a starting point.

**Step 5: Validate Against Time Constraints**
Ensure chosen topology aligns with your time budget (seconds, minutes, hours, days, weeks).

## Practical Applications & Use Cases

### Software Development Scenarios

#### 1. **Code Review Orchestration**

**System Design:**
```
Cognitive: Perception (read code) + Reasoning (analyze) + Collaboration (coordinate)
Topology: Hierarchy
  - Master Coordinator: Decides reviewer routing
  - Sub-coordinators: Architecture, Security, Performance teams
  - Workers: Individual reviewers
```

**Trade-offs:**
- Time: Hours (can afford deep review)
- Scalability: 50+ reviewers manageable
- Failure modes: Avoid if coordinator becomes bottleneck

#### 2. **Test Generation for Large Codebases**

**System Design:**
```
Cognitive: Reasoning (generate) + Reflection (verify) + Collaboration (coordinate)
Topology: Orchestrate + Loop
  - Orchestrator: Partitions code into test-generation chunks
  - Generators: Create unit/integration/property tests in parallel
  - Loop: Verify coverage, regenerate if gaps found
```

**Trade-offs:**
- Time: Days (complex task)
- Scalability: 10+ test generators
- Failure modes: Loop may not converge on very complex code

#### 3. **Specification-Driven Development**

**System Design:**
```
Cognitive: Perception + Reasoning + Action + Reflection
Topology: Chain → Orchestrate + Loop
  1. Chain: Parse spec → translate to requirements → decompose into tasks
  2. Orchestrate: Delegate tasks to dev agents
  3. Loop: Test → refine spec → regenerate code
```

**Trade-offs:**
- Time: Weeks
- Flexibility: Spec changes trigger re-planning
- Robustness: Loop provides validation

### Cross-Domain Applications

The framework applies beyond software development:

- **Document Analysis:** Hierarchical coordination of perception (reading), reasoning (analysis), collaboration (expert synthesis)
- **Research:** Chain (literature search → analysis → synthesis) + Loop (critique → refine)
- **Customer Support:** Route (classify issue) → Orchestrate (solve in parallel: technical + billing + escalation) + Loop (satisfaction check)

## Insights & Implications

### For Agent System Architects

1. **Topology-Cognitive Orthogonality Matters:** Treating topology and cognition as independent allows modular design. A change in topology doesn't require re-implementing reasoning; reasoning changes don't require topology restructuring.

2. **Fail-Fast Design Patterns:** The framework enables "fail-fast" identification of unsuitable patterns:
   - Does your time budget allow Hierarchy? If seconds, no.
   - Does your domain require Reflection? If yes, Loop is likely necessary.
   - Can your coordinator scale to N workers? If not, avoid flat Orchestrate; use Hierarchy instead.

3. **Hybrid Patterns Are Necessary:** No single topology is universally superior. Successful systems combine 2-3 topologies (e.g., Route + Orchestrate, Chain + Loop).

### For Software Development Automation

1. **Team Size Dictates Topology:**
   - 2-3 agents: Route or Parallel possible
   - 5-10 agents: Orchestrate or Hierarchy required
   - 50+ agents: Recursively nested Hierarchy necessary

2. **Task Ambiguity Requires Reflection (Loop):**
   - Well-defined tasks (e.g., "sort list of numbers"): Chain sufficient
   - Ambiguous tasks (e.g., "improve code quality"): Loop (iterative refinement) essential

3. **Specialized Agents Require Governance:**
   - If agents have different capabilities, Governance function and explicit role assignment (via Hierarchy or Delegation) is critical
   - Homogeneous agents can use simpler topologies (Chain, Parallel)

### For ML Ops and Monitoring

1. **Topology-Aware Metrics:**
   - Chain topology: Monitor latency at each agent (bottleneck identification)
   - Parallel: Monitor merge quality (how well are results combined?)
   - Loop: Monitor convergence time (is loop terminating?)
   - Hierarchy: Monitor coordinator utilization (is it a bottleneck?)

2. **Failure Mode Prediction:**
   - Plan-and-Execute: Pre-flight check the generated plan for completeness
   - Hierarchical Delegation: Monitor coordinator queue depth (early warning of bottleneck)
   - Adversarial Verification: Set iteration limits (avoid infinite loops)

### Open Questions

1. Can we automatically recommend topologies given task descriptions and constraints?
2. How do agents learn to transition between topologies as problems evolve?
3. What are the sample complexity and convergence properties of different topologies under RL?
4. Can we formally verify properties (e.g., "plan-and-execute is guaranteed to find solution if plan is correct")?

## Code & Resources

### Official Repositories

- **ArXiv Paper:** [2605.13850](https://arxiv.org/abs/2605.13850)
- **Paper PDF:** [Direct Link](https://arxiv.org/pdf/2605.13850)
- **HTML Version:** [Readable Format](https://arxiv.org/html/2605.13850)

### Related Frameworks

- **AutoGen (Microsoft):** Supports Chain, Parallel (via GroupChat), and limited Orchestrate
- **LangChain:** Chain topology natively; Parallel via map-reduce patterns
- **Crew.ai:** Orchestrate + Hierarchy with role-based agent assignment
- **Multi-Agent Orchestration:** AWS Step Functions, Temporal, Apache Airflow

### Design Pattern Library

The paper includes a design pattern reference guide (28+ patterns) organized by:
- Cognitive function requirements
- Time constraints
- Scalability target
- Failure modes and mitigations

### Quick-Start: Applying the Framework

**1. Classify Your Current System:**
   - What cognitive functions do your agents implement?
   - What topology are they arranged in?
   - Use the 2D grid to find your current position

**2. Identify Gaps:**
   - Are missing cognitive functions? (e.g., you have Reasoning but no Reflection?)
   - Is topology suitable for time constraints?
   - Could hybrid patterns improve robustness?

**3. Plan Improvements:**
   - Add missing cognitive function → add new agent roles
   - Change topology → restructure communication
   - Add reflection → add Loop for iterative refinement

## Related Work & Context

### Prior Agent Classification Systems

- **Breadth-First Surveys:** Catalogs of agent types and applications, but limited organizing principles
- **Cognitive Science Frameworks:** Models of cognition (ACT-R, SOAR) that inform cognitive functions but don't address system topology
- **Topology-Focused Frameworks:** Industry guides on microservices/distributed systems architecture, but disconnected from agent cognition

### Foundational Design Patterns Work

- **Gang of Four (GoF) Design Patterns:** Structural patterns (Decorator, Proxy, Facade) provide precedent for formal pattern languages in software engineering
- **Enterprise Integration Patterns:** Topology and message routing patterns from messaging systems (pipes, filters, routers)
- **Microservices Patterns:** Service orchestration and choreography patterns

### Related Papers in This Repository

- [ABSTRAL: Automated Multi-Agent System Design via Skill-Referenced Adaptive Search](llm-agents-dev/agent-orchestration/2026-03-24-abstral-automated-multi-agent-system-design.md)
- [EvoAgent: Evolvable Agent Framework with Skill Learning](llm-agents-dev/agent-orchestration/2026-04-22-evoagent-evolvable-agent-framework-skill-learning.md)
- [GoAgent: Group-of-Agents Communication Topology Generation](llm-agents-dev/multi-agent-topologies/2026-03-17-goagent-group-of-agents-communication-topology.md)

### Future Directions

1. **Automatic Topology Recommendation:** Can ML models recommend optimal topology given task description, constraints, and agent capabilities?
2. **Dynamic Topology Switching:** Should agents switch topologies during execution based on observed performance?
3. **Formal Verification of Patterns:** Can we prove correctness properties for each pattern (e.g., "Plan-and-Execute terminates if plan is complete")?
4. **Emergent Topology Learning:** Can RL discover novel topologies not in the current framework?

---

**Citation:**
```
@misc{huang2026framework,
  title={A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function and Execution Topology},
  author={Huang, Jia and Zhou, Joey Tianyi},
  journal={arXiv preprint arXiv:2605.13850},
  year={2026}
}
```
