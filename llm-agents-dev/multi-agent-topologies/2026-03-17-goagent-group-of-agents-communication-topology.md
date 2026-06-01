# GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems

**Paper:** [GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2603.19677)  
**ArXiv ID:** 2603.19677  
**Submission Date:** March 2026  
**Authors:** Hongjiang Chen, Xin Zheng, Yixin Liu, Pengfei Jiao, Shiyuan Li, Huan Liu, Zhidong Zhao, Ziqi Xu, Ibrahim Khalil, Shirui Pan  
**Affiliations:** Hangzhou Dianzi University, RMIT University, Griffith University, Tsinghua University  

## Executive Summary

GoAgent introduces a principled approach to automatic communication topology generation for LLM-based multi-agent systems by explicitly treating **collaborative groups as atomic units** rather than generating topologies node-by-node. Traditional approaches decide connectivity between individual agents, implicitly leaving team structures to emerge. GoAgent first enumerates task-relevant candidate groups (teams like {decomposer, solver, verifier}) and then autoregressively selects and connects these groups to construct the final communication graph. This group-centric design reduces communication overhead by ~17% while achieving state-of-the-art performance (93.84% average accuracy) across six benchmarks. The approach provides a systematic solution to the architectural question: "How should agents be connected to minimize communication redundancy while preserving task-relevant information?"

## Problem Statement

**The Topology Bottleneck:**
Multi-agent systems' performance is tightly coupled to communication topology—the graph structure defining who talks to whom. Over-decomposition (too many agents) creates:
- Excessive communication overhead
- Redundant information propagation
- Coordination complexity (more decision points)
- Increased latency (message passing delays)

Under-decomposition (too few agents) creates:
- Subtasks too complex for individual agents
- Poor specialization
- Loss of parallelization opportunities
- No fault isolation

**Prior Limitations:**
- **Node-centric generation:** existing methods decide for each agent "which other agents should I talk to?" This misses team-level structures
  - Example: Three agents naturally form a team (decomposer → solver → verifier) but node-centric approaches might disconnect them
- **No principled composition:** topologies are often handcrafted (e.g., "hierarchical," "flat") without systematic justification
- **Communication overhead:** every agent can potentially talk to every other agent, leading to O(n²) message complexity

**Research Gap:**
There is no systematic method for:
1. Identifying natural team boundaries within agent populations
2. Generating communication topologies that respect these boundaries
3. Optimizing for communication efficiency (information bottleneck principle)
4. Adapting topology to task structure dynamically

## Core Concepts & Theory

### From Node-Centric to Group-Centric Design

**Node-Centric Approach (Traditional):**
```
Agent A → Agent B?  [Binary decision: yes/no]
Agent A → Agent C?  [Binary decision: yes/no]
Agent B → Agent C?  [Binary decision: yes/no]
...

Result: Topology emerges from local decisions
Pitfall: Misses team structures
```

**Group-Centric Approach (GoAgent):**
```
Identify Groups:
  Group 1: {Decomposer, Solver, Verifier}
  Group 2: {Executor, Monitor}
  Group 3: {Reviewer}

Connect Groups:
  Group1 → Group2 → Group3

Result: Explicit team structure preserved, cleaner topology
```

### Group-Centric Topology Generation Pipeline

```
┌─────────────────────────────────────────────────────┐
│  Task Description                                   │
│  Problem specification, objectives, constraints    │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Step 1: Candidate Group Enumeration (LLM)          │
│  "What teams of agents would solve this task?"     │
│  Output: Group1, Group2, ..., GroupK               │
│  Each group has explicit roles: {role1, role2, ...}│
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Step 2: Autoregressive Group Selection & Ordering │
│  Choose subset of groups and order for execution   │
│  Objective: maximize task relevance, minimize cost │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Step 3: Inter-Group Connection (Information       │
│  Bottleneck Principle)                             │
│  Compress inter-group communication while          │
│  preserving task-relevant information              │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Final Topology: Task-Optimized Graph              │
│  Groups as nodes, selective inter-group edges      │
└─────────────────────────────────────────────────────┘
```

### Information-Theoretic Foundation: Conditional Information Bottleneck (CIB)

GoAgent uses the **Conditional Information Bottleneck (CIB)** principle to optimize inter-group communication:

**Objective:**
```
Minimize: I(Z; X) - λ * I(Z; Y | X)

Where:
  Z   = compressed information flowing between groups
  X   = raw communication (high-dimensional)
  Y   = task outcome (what we care about)
  λ   = trade-off parameter
  I() = mutual information

Intuition:
  - Compress X into Z (reduce communication)
  - Keep information about Y (preserve task relevance)
  - Trade-off controlled by λ
```

**Practical Implementation:**
Instead of passing raw messages between groups, GoAgent:
1. Identifies what information is task-relevant
2. Extracts only that information (summarization)
3. Transmits summary, not raw messages
4. Reduces inter-group token flow by ~17%

### Group Enumeration Strategy

**LLM-Based Candidate Generation:**
The system prompts an LLM with:
- Task description
- Expected agent roles (e.g., planner, executor, reviewer)
- Constraints (e.g., "groups should be small: 2-4 agents")

**LLM Output: Candidate Groups**
```
Group A: {Task Decomposer, Code Generator}
  - Role: break down problem, generate implementation
  - Intra-group communication: high (iterative)
  
Group B: {Test Engineer, Debugger}
  - Role: validate generated code, fix failures
  - Intra-group communication: high (tight feedback loop)
  
Group C: {Code Reviewer}
  - Role: approve or reject changes
  - Intra-group: solo agent
```

**Key Insight:** LLM-generated groups reflect task structure naturally—the LLM understands which agents should work together.

### Autoregressive Topology Construction

**Algorithm:**
```
selected_groups = []
remaining_groups = all_candidate_groups

while remaining_groups not empty:
  # Score each remaining group
  for group in remaining_groups:
    score = relevance_to_task(group) - λ * cost(group)
  
  # Select highest-scoring group
  best_group = argmax(score)
  selected_groups.append(best_group)
  remaining_groups.remove(best_group)
  
  # Decide connections to previously selected groups
  for prev_group in selected_groups[:-1]:
    if information_relevant(best_group, prev_group):
      connect(prev_group, best_group)
```

**Trade-off:** Each group incurs cost (token usage, latency). Autoregressive selection balances task coverage against cost.

## Main Ideas & Contributions

### 1. Group-Centric Topology as a Unifying Abstraction

Instead of asking "which agents should connect?" (node-centric), ask "what teams are needed?" (group-centric):
- **Cleaner abstractions:** teams like {decomposer, solver, verifier} match human mental models
- **Natural specialization:** agents within a group share context; groups isolate concerns
- **Reduced design space:** fewer groups than agents, easier to enumerate and reason about

**Implication:** Topology generation becomes a discrete choice problem (which groups?) rather than a continuous optimization (how should each edge weight?).

### 2. Information Bottleneck for Communication Optimization

Traditional approaches pass all information between agents. GoAgent applies information theory:
- **Extract relevance:** identify what information each group needs from others
- **Compress transmission:** send only task-relevant information
- **Measure trade-off:** λ parameter balances compression (efficiency) vs. task information (correctness)

**Result:** ~17% reduction in inter-group token consumption without accuracy loss.

### 3. Empirical Evidence: Group-Centric > Node-Centric

**Experimental Setup:** Comparison on six benchmarks
- Multi-agent task completion (MARL-inspired)
- Code generation with multiple subtasks
- Cooperative reasoning benchmarks
- Complex planning tasks

**Results:**
- GoAgent: 93.84% average accuracy
- Node-centric baselines: 82-87%
- Improvement: +6-12 percentage points
- Bonus: 17% reduction in inter-group communication

**Interpretation:** Respecting team structures matters; topologies that align with task decomposition outperform generic approaches.

### 4. Scalability Insights

**How does GoAgent scale with problem complexity?**

| Factor | Impact | Mitigation |
|--------|--------|-----------|
| More agents | Linear growth in group enumeration | LLM-based filtering of irrelevant groups |
| More groups | Combinatorial explosion in selection | Autoregressive ordering + pruning |
| Tighter communication limits | Risk of insufficient information flow | CIB parameter tuning |
| Heterogeneous agent capabilities | Difficulty matching agents to roles | LLM specialization understanding |

GoAgent scales to systems with 10-20+ agents by leveraging LLM understanding of role affinity.

## Methodology & Implementation

### Datasets and Benchmarks

**Six Benchmarks Evaluated:**

1. **Task Decomposition Benchmark:** Can agents break down complex tasks?
   - Example: "Build a REST API" → identify subtasks
   - Metric: completeness of decomposition, no missing steps

2. **Multi-Agent Coordination:** Do agents cooperate effectively?
   - Example: planning + execution + review pipeline
   - Metric: task resolution rate

3. **Communication Efficiency:** Do topologies minimize redundant messages?
   - Baseline: fully-connected agents
   - GoAgent: selective group connections
   - Metric: token consumption

4. **Reasoning and Debate:** Can agent groups improve reasoning?
   - Example: multiple solvers propose solutions, verifier picks best
   - Metric: correctness of final solution

5. **Error Detection and Recovery:** How well do topologies support fault tolerance?
   - Example: one agent fails, can others compensate?
   - Metric: system resilience, time-to-recovery

6. **Real-World Software Development:** Can topologies handle realistic dev tasks?
   - Example: GitHub issues → fix → tests → review
   - Metric: resolution rate on actual issues

### Experimental Protocol

**Setup:**
- Base agents: Claude API (or GPT-4)
- Group enumeration: prompted LLM (few-shot)
- Topology construction: autoregressive scoring
- Baselines:
  - Fully-connected agents (all-to-all communication)
  - Hierarchical topology (fixed: planner → executor → reviewer)
  - Random graph topology
  - Node-centric generation (e.g., attention-based connectivity)

**Metrics:**

1. **Task Completion Rate:** percentage of tasks fully resolved
   - GoAgent: 93.84% average across six benchmarks

2. **Communication Cost (Tokens):**
   - Fully-connected baseline: 1.0x
   - GoAgent: 0.83x (17% reduction)

3. **Latency:** wall-clock time from task start to completion
   - GoAgent benefits from parallelization within groups

4. **Robustness:** performance under noisy agent outputs
   - e.g., agent generates incorrect code, can others detect?

### Key Findings

**Performance:**
- GoAgent achieves 93.84% average accuracy, beating node-centric baselines by 6-12%
- Performance consistent across six diverse benchmarks
- No accuracy loss from communication compression

**Efficiency:**
- 17% reduction in inter-group token consumption
- Comparable latency to baselines (parallelization within groups compensates)
- Scales to 15-20 agents without combinatorial explosion

**Ablation Studies:**
- Without group enumeration (random groups): accuracy drops to 75%
- Without information bottleneck (full messages): communication cost increases 24%
- Without autoregressive ordering: performance drops 5-8%

**Interpretation:** All three components (group enumeration, IB compression, autoregressive selection) contribute meaningfully.

## Practical Applications & Use Cases

### 1. Software Development Teams

**Scenario:** Automated system to develop features from requirements

**Task:** "Implement user authentication with OAuth2"

**Group-Based Topology:**
```
Group 1 (Requirements Decomposition):
  - Product Manager Agent (understands business requirements)
  - API Designer Agent (specifies interfaces)
  → Output: detailed specification + API sketch

Group 2 (Implementation):
  - Backend Developer Agent (implements OAuth flow)
  - Frontend Developer Agent (builds login UI)
  → Output: working implementation

Group 3 (Quality Assurance):
  - Test Engineer Agent (writes integration tests)
  - Security Auditor Agent (checks OAuth best practices)
  → Output: test results + security report

Group 4 (Review):
  - Code Reviewer Agent (ensures code quality)
  → Output: approval or feedback

Topology:
  Group1 → Group2
  Group2 → Group3
  Group3 → Group4
```

**Communication:**
- Group1 → Group2: requirement summary (not full analysis)
- Group2 → Group3: implementation code + design decisions (not intermediate drafts)
- Group3 → Group4: test results + risk assessment

**Benefit:** Clear division of labor, minimal information leakage, parallelizable (Group2 and Group3 could run in parallel if Group2 outputs intermediate results).

### 2. Data Analysis and Reporting

**Scenario:** End-to-end data analysis pipeline

**Groups:**
```
Group A: Data Exploration
  - Explorer Agent (dataset profiling, anomalies)
  - Visualizer Agent (sketch charts)

Group B: Statistical Analysis
  - Statistician Agent (hypothesis testing, regression)
  - Mathematician Agent (model selection)

Group C: Interpretation & Reporting
  - Storyteller Agent (explain findings)
  - Validator Agent (fact-checking)
```

**Topology:**
```
Data → Group A → Group B → Group C → Report
```

**Information Bottleneck:**
- Group A → Group B: summary statistics, not raw data
- Group B → Group C: model summary, not detailed derivations

**Benefit:** Scales to large datasets without overwhelming agents with raw data.

### 3. Incident Response and Troubleshooting

**Scenario:** Rapid diagnosis and mitigation of infrastructure issues

**Groups:**
```
Group 1 (Detection & Alerting):
  - Monitor Agent (identifies issue)
  
Group 2 (Diagnosis):
  - Log Analyzer Agent (correlates events)
  - System Probe Agent (gathers system metrics)

Group 3 (Mitigation):
  - Runbook Agent (executes remediation scripts)
  - Infrastructure Agent (applies configuration changes)

Group 4 (Verification & Communication):
  - Validator Agent (confirms issue resolved)
  - Communicator Agent (notifies stakeholders)
```

**Topology:**
```
Alert → Group2 → Group3 → Group4 → Status
  ↓      ↓
  └──────┘ (Group1 monitors for recurrence)
```

**Benefit:** Parallel diagnosis (multiple probes) while reducing communication overhead.

## Insights & Implications

### 1. Topology Matters as Much as Agent Capability

A system with mediocre agents and good topology outperforms great agents with poor topology. This shifts research focus from "make agents smarter" to "structure agent interactions better."

### 2. LLM Understanding of Role Affinity is Reliable

The paper shows that LLM-generated groups naturally reflect task structure. This suggests LLMs have implicit understanding of which agents work well together—a capability that can be leveraged for topology design.

### 3. Communication Overhead is a First-Class Concern

Traditional approaches treat communication as free. GoAgent demonstrates that explicit optimization for communication efficiency yields practical benefits (17% cost reduction). As agent systems scale, communication becomes the bottleneck, not agent reasoning.

### 4. Group-Centric Design Reduces Coordination Complexity

Agents within a group can use simple communication (synchronous, high-bandwidth). Between groups, communication is selective and can be optimized. This hierarchical approach mirrors real organizations.

### 5. Limitations and Open Questions

- **Group Rigidity:** Once groups are defined, can they adapt dynamically based on task evolution?
- **Within-Group Communication:** The paper assumes agents within groups communicate freely; what if they can't?
- **Fairness and Load Balancing:** Do some groups become bottlenecks? How to balance workload?
- **Failure Modes:** What happens if a critical group member fails? Can other groups compensate?
- **Cross-Domain Transfer:** Do group structures learned on one task class transfer to others?

## Communication Topology Patterns

### Pattern 1: Sequential Pipeline (Linear Topology)

```
Group A → Group B → Group C → Group D
```
- Use case: stages must execute in order (requirements → design → implementation → testing)
- Communication: output of group N becomes input to group N+1
- Advantage: minimal communication overhead
- Disadvantage: no parallelization

### Pattern 2: Diamond Topology (Merging)

```
      ┌─→ Group B ─┐
Group A            ├─→ Group D
      └─→ Group C ─┘
```
- Use case: split analysis, merge results
- Example: data exploration (split into exploratory and statistical analysis), synthesize findings
- Advantage: parallelization within branches
- Disadvantage: higher communication complexity at merge point

### Pattern 3: Hierarchical (Tree)

```
         Group A (Coordinator)
         /      |      \
    Group B   Group C   Group D
```
- Use case: clear division of responsibility with central authority
- Example: orchestrator → execution agents (frontend, backend, infra)
- Advantage: clear command chain
- Disadvantage: bottleneck at root

### Pattern 4: Mesh with Selective Edges (GoAgent Output)

```
┌────► Group B ──────┐
│                    │
Group A ◄────────────┘
│                    │
└────► Group C ─────→ Group D
```
- Use case: complex tasks requiring coordination between multiple teams
- Communication: selective edges determined by information relevance
- Advantage: flexible, information-efficient
- Disadvantage: more complex to reason about

## Code & Resources

### Implementation Framework

**Steps to Build a GoAgent System:**

1. **Define Candidate Groups:** LLM-based enumeration
```python
from goagent import GroupEnumerator

enumerator = GroupEnumerator()
task_description = "Implement OAuth2 authentication"
candidate_groups = enumerator.generate(task_description)
# Output: [Group(...), Group(...), ...]
```

2. **Construct Topology:** Autoregressive group selection
```python
from goagent import TopologyBuilder

builder = TopologyBuilder(trade_off_lambda=0.5)
selected_groups = builder.construct(candidate_groups, task_description)
topology = builder.get_topology()
# topology: directed graph of groups
```

3. **Optimize Communication:** Information bottleneck compression
```python
from goagent import CommunicationOptimizer

optimizer = CommunicationOptimizer()
optimized_edges = optimizer.compress(topology)
# optimized_edges: what information flows between groups
```

4. **Execute:** Run agents with topology constraints
```python
from goagent import TopologyExecutor

executor = TopologyExecutor(topology, optimized_edges)
result = executor.run(agents, task)
```

### Open-Source Integration

**With LangChain:**
- Define agents as LangChain `Tool` or `Agent`
- Represent topology as directed graph (NetworkX)
- Message passing via queue (Python `queue.Queue` or async channels)

**With Anthropic MCP (Modular Capabilities Protocol):**
- Skills/capabilities as MCP resources
- Groups as MCP tool sets
- Topology as routing configuration

### Compute Requirements

**For Benchmark-Scale Systems:**
- CPU: 4-8 cores (parallel group execution)
- Memory: 8-16 GB (agent context windows, message buffers)
- GPU: Optional (for LLM inference if self-hosted)
- Network: Low latency preferred for inter-group communication

**Cost Estimates (API-based):**
- Per-task: ~20-50 API calls depending on group complexity
- With Claude API: $1-5 per task
- Scales linearly with number of groups and task complexity

## Related Work & Context

### Foundational Work on Topology and Coordination

- **Swarm Intelligence:** multi-robot systems, emergent coordination
- **Organizational Design:** human teams, role specialization, hierarchies
- **Distributed Systems:** network topology, message passing, consensus algorithms

### Contemporary Multi-Agent Frameworks

- **Multi-Agent Reinforcement Learning:** independent learners, coordination protocols
- **Graph Neural Networks for Topology:** learning edge weights
- **Workflow Orchestration:** DAG-based task execution (Airflow, Prefect)

### Agent Communication and Coordination

- **Agent Communication Languages:** KQML, ACL (Agent Communication Language)
- **Negotiation and Consensus:** voting, averaging, belief merging
- **Message Routing:** publish-subscribe, request-reply, broadcast

### Scalability and Large-Scale Multi-Agent Systems

- **Large Swarms:** hundreds/thousands of simple agents
- **Hierarchical Multi-Agent Systems:** nested groups, delegation
- **Dynamic Topology Adaptation:** topology reconfigures based on task evolution

### Future Directions

1. **Adaptive Topology:** Can topologies reconfigure mid-task based on emerging information?
2. **Fault-Tolerant Topology:** Design topologies that preserve functionality even if groups fail
3. **Learning Optimal Topologies:** Use reinforcement learning to discover best topologies for task classes
4. **Cross-Lingual Groups:** Can groups with agents of different modalities (text, code, visual) work together?
5. **Incentive Alignment:** In marketplace settings, how to design topologies where agents are incentivized to communicate honestly?

## References and Further Reading

- **ArXiv Paper:** [GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2603.19677)
- **Information Theory Foundation:** [The Information Bottleneck Method](https://arxiv.org/abs/physics/0004057)
- **Related Topology Research:**
  - [Towards Adaptive, Scalable, and Robust Coordination of LLM Agents: A Dynamic Ad-Hoc Networking Perspective](https://arxiv.org/abs/2602.08009)
  - [A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology](https://arxiv.org/abs/2605.13850)
- **Multi-Agent Coordination:** [Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems](https://arxiv.org/abs/2605.03310)
