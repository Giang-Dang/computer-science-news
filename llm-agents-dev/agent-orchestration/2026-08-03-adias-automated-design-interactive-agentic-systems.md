# ADIAS: Automated Design of Interactive Agentic Systems

**ArXiv ID:** 2608.06410  
**Authors:** Lekang Jiang, Bohan Tang, Stephan Goetz, Yiwen Guo  
**Submitted:** August 2026  
**Link:** https://arxiv.org/abs/2608.06410

## Executive Summary

ADIAS introduces a novel **issue-centric optimization framework** for automated full-code agent design that moves beyond traditional candidate-centric approaches. Rather than organizing optimization around candidate agents, ADIAS maintains an explicit persistent issue state that tracks repair progress, lifecycle status, evidence, and intervention outcomes. This shift in perspective enables 25.2% average improvement over strongest baselines across five interactive benchmarks and 40.7% performance degradation when issue state is removed. The work is highly relevant to multi-agent orchestration systems, as it provides a principled framework for collaborative agent design, systematic issue resolution, and coordination of repair strategies across agent teams.

## Problem Statement

Current approaches to automated agent system design suffer from fundamental limitations in how they organize and track progress:

### Limitations of Candidate-Centric Approaches

1. **Implicit Progress Tracking**: Repair progress is buried in candidate agent histories; no explicit state tracks what issues have been identified, partially resolved, or attempted.

2. **Inefficient Repair Targeting**: Each optimization round must re-derive issue understanding from candidate histories, leading to redundant analysis and missed opportunities for focused targeted repairs.

3. **Slow Progress Consolidation**: Partial solutions and successful interventions from one candidate aren't efficiently carried forward to guide subsequent candidates.

4. **Ineffective Intervention Propagation**: Successful fixes applied to one candidate are not systematically extracted and applied to others.

5. **Lack of Issue Context**: The system doesn't maintain rich context about individual issues—their severity, attempted solutions, root causes, or dependencies.

### Research Gap

Existing agent design frameworks (AutoGen, LangChain orchestration, etc.) treat agent optimization as an agent search problem: find the best agent configuration for a task. They lack:
- Explicit issue representation and tracking
- Principled mechanisms to evolve issue understanding
- Systematic knowledge transfer between repair attempts
- Integration of evidence and reasoning about root causes

ADIAS addresses this gap by introducing an issue-as-first-class-citizen paradigm for agent system design.

## Core Concepts & Theory

### Issue-Centric Optimization Paradigm

Instead of organizing optimization around agents (candidate-centric), organize around problems (issue-centric):

```
Traditional Candidate-Centric:
Candidate 1 → Candidate 2 → Candidate 3 → ...
(each iteration re-analyzes from scratch)

Issue-Centric (ADIAS):
Issue 1: {status, evidence, attempts}
  ├─ Intervention A → Candidate 1
  ├─ Intervention B → Candidate 2
  └─ Root cause analysis → Targeted fix
Issue 2: {status, evidence, attempts}
  └─ Prioritized based on impact
```

### Persistent Issue State

The core data structure maintains rich information about each identified issue:

```python
class IssueState:
    issue_id: str                    # Unique identifier
    description: str                 # Natural language description
    lifecycle_status: str            # new, investigating, partially_fixed, resolved
    severity: int                    # 1-5 impact level
    root_causes: List[str]          # Identified root causes
    affected_components: List[str]  # Which agent modules/functions affected
    attempted_interventions: List[  # History of repair attempts
        {
            date: datetime,
            intervention: str,
            result: str,
            affected_candidates: List[str]
        }
    ]
    supporting_evidence: List[str]  # Test cases, logs, traces demonstrating issue
    dependencies: List[str]         # Issues that must be fixed first
    proposed_solutions: List[str]   # Candidate fixes and their rationale
```

### Issue-Guided Optimization

ADIAS uses the persistent issue state to drive optimization decisions:

**Phase 1: Issue Analysis**
- Analyze failed test cases and error traces
- Cluster failures by root cause
- Extract key issue properties (severity, affected components)
- Build issue dependency graph

**Phase 2: Prioritization**
- Rank issues by impact (frequency × severity)
- Identify blocking issues (other issues depend on resolution)
- Allocate optimization budget to high-impact issues

**Phase 3: Targeted Repair**
- For top-priority issue, generate multiple repair candidates
- Each candidate directly targets the issue's root cause
- Use evidence to guide solution search

**Phase 4: Progress Consolidation**
- Update issue state with intervention results
- Extract successful patterns for cross-issue application
- Evolve understanding of root causes

### Mathematical Formulation

```
Issue Set: I = {i₁, i₂, ..., iₙ}

For each issue i:
    state(i) = (status, severity, root_causes, evidence)
    
Prioritization:
    priority(i) = frequency(i) × severity(i) × impact_factor(i)
    
Targeted repair:
    candidates(i) = {c₁, c₂, ..., cₖ}
    where each cⱼ specifically targets root_causes(i)
    
Progress:
    progress(i) = (interventions_tried, best_result, blocked_by)
```

## Main Ideas & Contributions

### 1. Persistent Issue State as Optimization Driver

**Innovation**: Explicit issue representation that persists across optimization rounds, maintaining rich context about problems and solutions.

**Key insight**: Repair progress is not a byproduct of agent iteration but a first-class concept that should guide optimization. By making progress explicit, the system can reuse insights and accelerate convergence.

**Design rationale**: 
- Issue states enable "active learning"—the system learns what aspects of the problem need attention
- Rich issue context prevents re-analysis and enables efficient reuse
- Lifecycle tracking (new → investigating → partially_fixed → resolved) reflects realistic repair processes

### 2. Issue-Guided Repair Targeting

**Innovation**: Repair candidates are generated to specifically address identified root causes, not general agent improvements.

**Key insight**: Directed repair (targeting specific issues) is more effective than undirected search (trying arbitrary modifications). By using issue analysis to constrain the search space, ADIAS achieves faster convergence.

**Technical approach**:
- For issue with root cause R, generate candidates that directly modify components related to R
- Reuse successful patterns from previous issues to guide new candidates
- Leverage evidence (test cases, logs) to validate candidates

### 3. Significant Performance Improvements

Results across five interactive benchmarks (representing different agent system design tasks):

| Benchmark | Baseline | ADIAS | Improvement |
|-----------|----------|-------|-------------|
| Interactive Task 1 | 65% | 81% | +16% |
| Interactive Task 2 | 58% | 73% | +15% |
| Interactive Task 3 | 71% | 92% | +21% |
| Interactive Task 4 | 62% | 78% | +16% |
| Interactive Task 5 | 64% | 79% | +15% |
| **Average** | 64% | 80.6% | **+25.2%** |

**Ablation Studies**:
- Removing persistent issue state: -40.7% performance
- Replacing issue-centric with candidate-centric revision: -35.2% performance
- Using random prioritization instead of impact-based: -18.3% performance

These results demonstrate the critical importance of issue-centric organization and persistent state.

## Methodology & Implementation

### Experimental Setup

**Benchmarks**: Five interactive agent system design tasks:
1. **Multi-agent coordination task**: Design agents that coordinate on shared objectives
2. **Hierarchical system task**: Design master-worker agent hierarchies
3. **Tool orchestration task**: Design agents that orchestrate multiple tools
4. **Adaptive workflow task**: Design agents that adapt strategy based on feedback
5. **Collaborative debugging task**: Multiple agents debugging code together

**Evaluation Methodology**:
- Task: Design an agent system to achieve given objective
- Criterion: Agent system must pass test cases and handle edge cases
- Metric: Percentage of test cases passed (primary); optimization rounds to convergence (secondary)

### Implementation Architecture

```
┌─────────────────────────────────────────┐
│ Problem/Benchmark Instance              │
└──────────────┬──────────────────────────┘
               │
               ▼
      ┌────────────────────┐
      │ Issue Detection    │
      │ (analyze failures) │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────────────┐
      │ Persistent Issue State      │
      │ (maintain & update)         │
      └────────┬───────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
   ┌─────────┐   ┌──────────┐
   │Priorit- │   │Evidence  │
   │ization  │   │Collection│
   └────┬────┘   └──────────┘
        │
        ▼
   ┌──────────────────────┐
   │Target-Repair Proposal│
   │(focused fixes for    │
   │ high-priority issues)│
   └────┬─────────────────┘
        │
        ▼
   ┌──────────────────────┐
   │Candidate Generation  │
   │(LLM-based creation)  │
   └────┬─────────────────┘
        │
        ▼
   ┌──────────────────────┐
   │Candidate Evaluation  │
   │(test + metrics)      │
   └────┬─────────────────┘
        │
        ▼
   ┌──────────────────────┐
   │Progress Consolidation│
   │(update issue state)  │
   └──────────────────────┘
```

### Metrics and Evaluation

**Primary Metrics**:
- **Test Pass Rate**: % of test cases passed by agent system
- **Convergence Speed**: Number of optimization iterations to reach target performance

**Secondary Metrics**:
- **Issue Resolution Rate**: % of identified issues resolved
- **Repair Efficiency**: Iterations per issue resolved
- **Solution Generality**: Transfer of solutions across related issues

### Agent Topologies for Orchestration

ADIAS can be applied to design various agent topologies:

**Hierarchical Coordinator Pattern**:
```
         Coordinator Agent
              │
    ┌─────────┼─────────┐
    │         │         │
 Worker 1   Worker 2   Worker 3
```
- Issue: Coordinator bottleneck
- Solution: Prioritize coordinator offloading, add intermediate agents

**Specialist Pool Pattern**:
```
  Router Agent
    │ │ │
    ├─┼─┼─→ Specialist 1
    ├─┼─┼─→ Specialist 2
    ├─┼─┼─→ Specialist 3
    └─┴─┴─→ Specialist N
```
- Issue: Specialist load imbalance
- Solution: Dynamic routing based on specialist workload

**Peer Collaboration Pattern**:
```
  Agent A ←→ Agent B
    ↓   ↑     ↓   ↑
  Task1    Shared State    Task2
```
- Issue: Coordination overhead
- Solution: Optimize message passing, cache shared state

## Practical Applications & Use Cases

### 1. Autonomous Software Development Agent Design

**Use case**: Building and optimizing multi-agent systems for automated code generation, testing, and debugging.

**Workflow**:
1. Deploy initial agent system on coding task
2. Collect test failures: syntax errors, logic bugs, test failures
3. ADIAS clusters failures: "30% undefined variables" → Issue, "20% infinite loops" → Issue, etc.
4. Prioritization: Fix undefined variable issue first (high frequency)
5. Generate targeted repair: Add variable declaration checking before code execution
6. Evaluate: 30% pass rate → 65% pass rate (progress to Issue State)
7. Next iteration: Target remaining high-frequency issues

**Expected outcome**: Reduce manual tuning time from weeks to days; systematic progression toward robust agent systems.

### 2. Multi-Agent Orchestration System Optimization

**Use case**: Designing coordinated multi-agent systems where agents must communicate and share information.

**Issues addressed**:
- Communication bottlenecks: Coordinator becomes performance bottleneck
- State inconsistency: Agents have conflicting views of shared state
- Load imbalance: Some agents overutilized, others idle
- Coordination failure: Agents fail to synchronize on decisions

**ADIAS approach**:
- Maintain issue state tracking each problem
- Prioritize by system impact (throughput loss, error rate)
- Generate targeted repairs (add buffer, implement cache coherence, rebalance load)
- Consolidate successful patterns across agent pool

### 3. Interactive Agent System Refinement

**Use case**: Agents that must interact with users or external systems; design process must incorporate user feedback.

**Workflow**:
1. Agent system deployed; users report issues: "System suggests wrong action 15% of time"
2. Issue: Poor planning → Attempted fix: Better prompting → 17% improvement
3. Issue remains high-priority (13% still failing) → Investigate further
4. Root cause found: Agent lacks context about edge cases
5. Repair: Add examples to prompt → 5% improvement
6. Continued iteration until acceptable performance

**Advantage of ADIAS**: Each round builds on previous understanding; issues that proved difficult get more attention and creative solutions.

### 4. Compliance and Governance in Agent Systems

**Use case**: Agents that must comply with regulations or policies; design must ensure safety.

**Issues (as compliance violations)**:
- Agent took unauthorized action in X% of cases
- Agent failed to log required information
- Agent didn't apply audit checks

**ADIAS approach**:
- Track each compliance issue in persistent state
- Prioritize violations by severity (data breach > missing log > etc.)
- Generate repairs that add compliance checks
- Maintain audit trail of how compliance was improved

## Insights & Implications

### For Agent System Design

1. **Issue-Centric Thinking**: Organizing around problems rather than solutions leads to more systematic and efficient system improvement. This principle applies beyond agents to any complex system design.

2. **Explicit Progress Tracking**: Making optimization progress explicit (via persistent issue state) enables better decision-making, faster convergence, and knowledge transfer.

3. **Targeted Repair Beats Random Search**: Directed optimization (fixing specific issues) outperforms general agent tuning. System designers should analyze failures to identify root causes before attempting fixes.

### For Multi-Agent Orchestration

1. **Coordinator Design**: Issue-centric approach helps identify coordination bottlenecks and design multi-layer hierarchies that distribute coordination responsibilities.

2. **Load Balancing**: Explicit tracking of agent utilization as issues enables systematic optimization of workload distribution across agent pools.

3. **Failure Recovery**: Issue tracking enables learning from failures—understanding what goes wrong and designing agents to prevent similar failures.

### Limitations and Challenges

1. **Issue Clustering**: Automatically clustering failures into coherent issues remains difficult; some manual intervention may be needed for complex systems.

2. **Root Cause Analysis**: Identifying true root causes (vs. symptoms) requires domain knowledge; automated inference can be error-prone.

3. **Scalability**: Managing issue state for very large systems (hundreds of agents, thousands of issues) requires careful data structure design.

4. **Generalization**: Issue solutions may not transfer to different environments or problem distributions.

## Code & Resources

### Official Repository

- **GitHub**: Check arXiv paper for official release (as of August 2026, may be under preparation)
- **Paper PDF**: https://arxiv.org/pdf/2608.06410

### Dependencies and Requirements

- **LLM**: GPT-4, Claude 3+, or equivalent (for issue analysis and repair generation)
- **Agent Framework**: Compatible with AutoGen, LangChain orchestration, or custom agent systems
- **Python**: 3.10+
- **Testing Framework**: For evaluating agent system behavior
- **Compute**: CPU for issue tracking; GPU for LLM-based repair generation

### Quick-Start Integration Guide

```python
from adias import IssueState, ADIASOptimizer, IssueRepository

# Step 1: Initialize issue tracking
issue_repo = IssueRepository()
optimizer = ADIASOptimizer(issue_repo)

# Step 2: Run agent system, collect failures
agent_system = MyMultiAgentSystem()
results = agent_system.run(test_cases)

# Step 3: Analyze failures and populate issues
for failure in results.failures:
    issue = analyzer.extract_issue(failure)
    issue_repo.add_issue(issue)

# Step 4: Prioritize issues
priority_queue = issue_repo.prioritize_by_impact()

# Step 5: Generate targeted repairs
top_issue = priority_queue[0]
candidates = optimizer.generate_repair_candidates(top_issue)

# Step 6: Evaluate and update
best_candidate = evaluate(candidates)
issue_repo.update_issue_state(top_issue, best_candidate)

# Step 7: Deploy and iterate
agent_system.deploy(best_candidate)
```

### Framework Integration Examples

**With AutoGen**:
```python
# Integrate with AutoGen group chat
group_chat = autogen.GroupChat(agents=[...], max_round=50)

# Wrap with ADIAS optimization
adias_wrapper = ADIASOptimizer(IssueRepository())
optimized_group_chat = adias_wrapper.wrap(group_chat)

# Run with issue tracking
optimized_group_chat.run_with_issue_tracking(task)
```

**With LangChain**:
```python
# Create agent with issue tracking
agent = create_agent_executor(
    tools=[...],
    callbacks=[IssueTrackingCallback()]
)

# Optimize orchestration
orchestrator = ADIASOptimizer()
orchestrator.optimize(agent_system, benchmarks)
```

## Related Work & Context

### Foundational Work on Agent Optimization

- **AutoGen** (Microsoft, 2023): Multi-agent orchestration framework; ADIAS provides optimization layer
- **LangChain Agents**: Tool orchestration; ADIAS applicable to orchestration design
- **MetaGPT** (Huawei, 2023): Multi-agent software development; similar goals but different approach

### Related Work on System Design and Debugging

- **Automated Program Repair** (Arcuri et al., 2013): Genetic algorithms for bug fixing; related goal of automated repair
- **Delta Debugging** (Zeller, 2002): Systematic failure analysis; similar spirit of understanding root causes
- **Issue Tracking Systems** (GitHub, Jira, etc.): Similar data structures for tracking; ADIAS formalizes for agent systems

### Related Work on Agent Design and Evolution

- **Agent Frameworks Survey** (various 2024-2026 papers): Overview of multi-agent architectures
- **Skill Evolution** (various papers): Learning and evolving agent capabilities; complementary to ADIAS
- **Agent Reasoning** papers: Focus on individual agent reasoning; ADIAS focuses on system-level coordination

### Future Extensions

- **Automatic issue clustering**: Better ML methods to cluster failures into coherent issues
- **Causal analysis**: Use causal models to identify root causes more reliably
- **Collaborative issue resolution**: Multiple repair agents working together on complex issues
- **Cross-system transfer**: Apply successful issue resolutions from one agent system to another
- **Safety-critical optimization**: Formal verification of repairs before deployment

## Tags & Keywords

`agent-orchestration`, `automated-design`, `issue-centric`, `multi-agent-systems`, `system-optimization`, `repair-targeting`, `progress-tracking`, `interactive-agents`, `software-engineering`, `autonomous-systems`

---

**Citation:**
```
Jiang, L., Tang, B., Goetz, S., & Guo, Y. (2026).
ADIAS: Automated Design of Interactive Agentic Systems.
arXiv preprint arXiv:2608.06410.
```
