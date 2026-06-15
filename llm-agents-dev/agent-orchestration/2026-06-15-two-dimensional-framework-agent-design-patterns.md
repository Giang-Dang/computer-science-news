# A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology

**Authors:** Jia Huang, Joey Tianyi Zhou  
**Affiliation:** Agency for Science, Technology and Research (A*STAR), Singapore & Centre for Frontier AI Research  
**ArXiv ID:** 2605.13850  
**Submitted:** March 2026

## Executive Summary

The landscape of LLM-based agent architectures is fragmented: industry frameworks describe systems by execution topology (how data flows), while cognitive science surveys focus on cognitive function (what the agent does). This creates confusion and misguided design decisions. This paper proposes a unifying two-dimensional framework that classifies agent design patterns across **Cognitive Function** (seven categories: Perception, Memory, Reasoning, Action, Reflection, Collaboration, Governance) and **Execution Topology** (six structural patterns). The framework reveals that identical topologies (e.g., Orchestrator-Workers) can realize fundamentally different patterns with vastly different failure modes and scalability characteristics. For development teams, this classification provides a systematic language for agent design, enabling principled selection of topologies for specific software engineering tasks.

## Problem Statement

**Development Automation Challenge:** Teams building multi-agent systems for software engineering lack a unified language to describe agent patterns. The same Orchestrator-Workers topology can implement Plan-and-Execute, Hierarchical Delegation, or Adversarial Verification—three patterns with different failure modes, scalability, and cost implications.

**Prior Limitations:**
- Industry guides (AutoGen, MetaGPT docs) focus on execution topology (diagram + data flow)
- Cognitive science literature focuses on cognitive function (reasoning, memory, reflection)
- No systematic mapping between function and topology
- Architects cannot reason about whether a topology "fits" a desired function

**Research Gap:** No unified framework exists that connects cognitive function (what agents do internally) to execution topology (how they're coordinated externally), leaving design decisions ad hoc and error-prone.

## Core Concepts & Theory

### Cognitive Function Axis

The cognitive function axis identifies seven fundamental capabilities that agents exhibit:

#### 1. **Perception**
**What it is:** Agent's ability to acquire and process input signals (code, documents, user requests, system state)

**Manifestations in development:**
- **Basic:** Parse a single code file or issue description
- **Advanced:** Analyze cross-repository dependencies, visual diagrams, commit history

**Failure modes:** Misreading problem scope, missing critical context
**Scalability:** Linear in input size; parallelizable across independent inputs

**Example:** Code review agent perceives: code syntax, style violations, logic errors

#### 2. **Memory**
**What it is:** Agent's ability to store and retrieve information across interactions

**Types:**
- **Short-term:** Current task context (tokens in LLM context window)
- **Long-term:** Project history, learned patterns, documented decisions
- **Episodic:** Specific past interactions (traces, logs)

**Manifestations in development:**
- **Basic:** Maintain conversation history within session
- **Advanced:** Cross-session memory of codebase patterns, deployment decisions

**Failure modes:** Context loss, stale information, forgotten constraints
**Scalability:** Token cost grows with memory; compression needed beyond ~10K tokens

**Example:** Debugging agent remembers: previous stack traces, related issues, known patterns

#### 3. **Reasoning**
**What it is:** Agent's ability to derive conclusions from information; internal problem-solving

**Types:**
- **Forward chaining:** "Given these facts, what follows?" (code → bugs)
- **Backward chaining:** "To achieve goal, what's needed?" (test → implementation)
- **Abductive:** "Given observations, what explains them?" (debugging)

**Manifestations in development:**
- **Basic:** Single-step inference (if code has pattern X, likely issue Y)
- **Advanced:** Multi-step planning with backtracking (SWE-bench-like problem solving)

**Failure modes:** Incorrect assumptions, missed edge cases, getting stuck in loops
**Scalability:** Token cost grows with reasoning depth; diminishing returns beyond 5–10 steps

**Example:** Testing agent reasons: "To achieve 90% coverage, I need to test paths X, Y, Z"

#### 4. **Action**
**What it is:** Agent's ability to execute decisions and interact with environment

**Types:**
- **Internal:** Code generation, analysis
- **External:** API calls, file writes, command execution
- **Observational:** Querying system state without mutation

**Manifestations in development:**
- **Basic:** Single tool invocation (write a function, run a test)
- **Advanced:** Multi-step workflows (generate → test → debug → optimize)

**Failure modes:** Wrong tool choice, unsafe execution, side effects
**Scalability:** Linear in number of actions; requires careful error handling

**Example:** Refactoring agent acts: "Write new implementation, run tests, compare metrics"

#### 5. **Reflection**
**What it is:** Agent's ability to evaluate its own performance and adapt

**Types:**
- **Introspection:** "Am I making progress?" "Did my action work?"
- **Correction:** "I made a mistake; let me fix it"
- **Learning:** "Next time, I should try approach Y instead of X"

**Manifestations in development:**
- **Basic:** Check action results, retry on failure
- **Advanced:** Learn from failure patterns, self-correct reasoning

**Failure modes:** Confirmation bias, infinite retry loops, inability to admit failure
**Scalability:** Introspection is cheap; learning (fine-tuning) expensive

**Example:** Code generation agent reflects: "My test failed; let me review the implementation logic"

#### 6. **Collaboration**
**What it is:** Agent's ability to work with other agents or humans

**Types:**
- **Peer collaboration:** Agents at same level discuss and agree
- **Hierarchical:** Subordinate agents report to coordinator
- **Adversarial:** Agents critique each other's work

**Manifestations in development:**
- **Basic:** One agent gets results from another
- **Advanced:** Multi-agent consensus, conflict resolution, role-based specialization

**Failure modes:** Deadlock, disagreement, poor communication
**Scalability:** Coordination overhead grows quadratically with agent count (from ~3 agents onward)

**Example:** Multi-agent code review: Style agent → Logic agent → Security agent → Consensus

#### 7. **Governance**
**What it is:** Rules, constraints, and policies that guide agent behavior

**Types:**
- **Safety:** "Never write to production without approval"
- **Consistency:** "Always follow coding standard X"
- **Accountability:** "Document all decisions"

**Manifestations in development:**
- **Basic:** Hard rules (no file deletion without human approval)
- **Advanced:** Soft constraints (prefer efficient algorithms, minimize token cost)

**Failure modes:** Overly rigid (prevents necessary actions), too loose (allows dangerous actions)
**Scalability:** Governance typically O(1); implemented via prompting + hard gates

**Example:** Refactoring governance: "Approve all semantic changes; auto-execute style changes"

### Execution Topology Axis

The execution topology axis describes six canonical structural patterns:

#### 1. **Sequential Chain**
```
Input → Agent1 → Agent2 → Agent3 → Output
```

**Characteristics:**
- Agents work in strict order
- Output of one feeds to next
- No parallelization

**Use cases:**
- Multi-step processes with dependencies (code review: style → logic → security)
- Pipelines with progressive refinement

**Trade-offs:**
- Latency: High (sum of all agent latencies)
- Complexity: Low (linear flow)
- Resilience: Medium (can retry individual stages)

#### 2. **Parallel Exploration**
```
        ┌→ Agent1 → Output1 ┐
Input →┤→ Agent2 → Output2 ├→ Synthesize → Output
        └→ Agent3 → Output3 ┘
```

**Characteristics:**
- Multiple agents work independently on same input
- Results synthesized at end
- Full parallelization

**Use cases:**
- Hypothesis testing (debugging: test different hypotheses in parallel)
- Multi-perspective analysis (code review: style, logic, security in parallel)

**Trade-offs:**
- Latency: Low (max of agent latencies + synthesis)
- Complexity: High (need consensus/synthesis mechanism)
- Cost: High (parallel API calls)
- Resilience: Low (failure affects synthesis quality)

#### 3. **Hierarchical Delegation**
```
             ┌─ Specialist1
Coordinator ┼─ Specialist2
             └─ Specialist3
```

**Characteristics:**
- Central coordinator distributes work to specialists
- Specialists are domain-specific
- Coordinator merges results

**Use cases:**
- Team-based orchestration (code review by role)
- Large-scale task decomposition

**Trade-offs:**
- Latency: Medium (coordinator overhead + specialist latency)
- Complexity: Medium (need coordinator logic)
- Scalability: Limited by coordinator bottleneck
- Specialization: High (agents well-suited to roles)

#### 4. **Graph (DAG)**
```
    ┌─ Task1 ─┐
    │         ├─ Task4
    └─ Task2 ─┤
              ├─ Task5 ──→ Task6
    ┌─ Task3 ─┘
```

**Characteristics:**
- Tasks form directed acyclic graph (DAG)
- Dependencies explicitly modeled
- Can be partially parallel

**Use cases:**
- Complex workflows with mixed dependencies
- Build systems, test orchestration

**Trade-offs:**
- Latency: Optimized based on critical path
- Complexity: High (need DAG solver)
- Flexibility: High (arbitrary dependency modeling)
- Overhead: Medium (depends on DAG structure)

#### 5. **Peer Network**
```
      Agent1
     / │   \
   Agent2 - Agent3
     \ │   /
      Agent4
```

**Characteristics:**
- Agents communicate bidirectionally
- No strict hierarchy
- Emergent coordination

**Use cases:**
- Consensus-based decisions (all agents weigh in)
- Decentralized problem-solving

**Trade-offs:**
- Latency: High (many messages)
- Complexity: Very high (all-to-all communication)
- Coordination: Challenging (no central authority)
- Robustness: Medium (some agent failures acceptable)

#### 6. **Single Agent + Tools**
```
    Agent ─┬─ Tool1
           ├─ Tool2
           └─ Tool3
```

**Characteristics:**
- One agent with access to multiple tools
- Agent decides tool calls sequentially
- No inter-agent communication

**Use cases:**
- Simple workflows (code formatting, linting)
- Tasks requiring sequential decisions

**Trade-offs:**
- Latency: Fast (no coordination overhead)
- Complexity: Low (standard ReAct pattern)
- Scalability: Limited (single agent bottleneck)
- Reliability: Good (simple to debug)

### The 2D Classification Matrix

The framework creates a 7×6 matrix showing how cognitive functions manifest in execution topologies:

| Cognitive Function | Sequential | Parallel | Hierarchical | Graph | Peer | Single+Tools |
|-------------------|-----------|----------|--------------|-------|------|--------------|
| **Perception** | Cumulative | Parallel | Separate | Per-agent | Broadcast | Integrated |
| **Memory** | Shared (local) | Per-agent | Central + local | Per-agent | Distributed | Local |
| **Reasoning** | Progressive | Independent | Central + local | Per-agent | Consensus | Single |
| **Action** | Chained | Parallel | Delegated | Coordinated | Autonomous | Programmed |
| **Reflection** | After each step | Post-synthesis | Coordinator | Per-agent | Collective | Built-in |
| **Collaboration** | Implicit (data flow) | Synthesis logic | Reporting | DAG solver | Messaging | N/A |
| **Governance** | Serial validation | Consensus rules | Coordinator rules | DAG rules | Group consensus | Agent rules |

### Design Pattern Examples

#### Pattern 1: Plan-and-Execute
```
Cognitive Functions:
- Perception: Understand task
- Reasoning: Break into steps
- Action: Execute each step
- Reflection: Evaluate progress

Suitable Topologies:
- Sequential: Planner → Executor
- Hierarchical: Planner (coordinator) → Executors (specialists)
```

**Example:** Code generation agent
- Step 1: Understand requirements (Perception)
- Step 2: Design solution (Reasoning)
- Step 3: Implement (Action)
- Step 4: Test and refine (Reflection)

#### Pattern 2: Adversarial Verification
```
Cognitive Functions:
- Perception: Generate candidate
- Reasoning: Evaluate quality
- Reflection: Identify weaknesses
- Collaboration: Adversarial critique

Suitable Topologies:
- Parallel: Generator vs. Critic
- Peer: Multiple critics debating
```

**Example:** Code review multi-agent
- Generator: Proposes refactoring
- Critic1: "This changes behavior"
- Critic2: "Edge case not handled"
- Synthesis: Iterate until all critics satisfied

#### Pattern 3: Hierarchical Expertise
```
Cognitive Functions:
- Perception: Detect sub-problems
- Memory: Track dependencies
- Action: Execute by expert
- Governance: Coordinator enforces rules

Suitable Topologies:
- Hierarchical: Domain-specific specialists
- Graph: Dependency ordering
```

**Example:** Multi-stage code review
- Coordinator detects 3 issues: style, logic, security
- Routes to specialists: StyleChecker, LogicAnalyzer, SecurityAuditor
- Aggregates feedback into report

## Main Ideas & Contributions

### 1. Unified Classification Framework
- Bridges industry topology focus with cognitive science function focus
- Reveals that same topology can implement different patterns
- Enables principled pattern selection for software engineering tasks

### 2. Seven Cognitive Functions for LLM Agents
- Identified core capabilities independent of architecture
- Applicable across domains (not limited to code)
- Enables capability-driven design ("I need reflection, so I choose topology X")

### 3. Six Execution Topologies
- Comprehensive but concise list (scalable from 1 to 100+ agents)
- Each has clear latency, complexity, and scalability trade-offs
- Enables topology-driven optimization

### 4. 7×6 Classification Matrix
- Shows which topologies best support which functions
- Reveals gaps (e.g., Peer networks poor for governance)
- Guides design decisions (e.g., "If I need reflection + low latency, choose Sequential")

### 5. Design Pattern Language
- Establishes named patterns (Plan-and-Execute, Adversarial Verification, Hierarchical Expertise)
- Enables team communication ("Let's use Adversarial Verification for code review")
- Facilitates pattern reuse across projects

## Methodology & Implementation

### Framework Development
- Literature review: 50+ agent frameworks (AutoGen, MetaGPT, CrewAI, etc.)
- Analysis of cognitive science: 30+ papers on reasoning, memory, collaboration
- Case studies: 10 real-world agent systems for code generation, debugging, testing
- Iterative refinement: Feedback from 25+ practitioners

### Case Studies

#### Case 1: Code Review Agent (AutoGen Implementation)

**Desired Cognitive Functions:**
- Perception: Understand code changes
- Reasoning: Identify issues in style, logic, security
- Collaboration: Aggregate feedback from multiple reviewers
- Governance: Enforce code standards

**Framework Design:**
```
Topology: Sequential Chain (3 agents)
├─ Agent1: StyleReviewer (PEP-8, formatting)
├─ Agent2: LogicAnalyzer (correctness, complexity)
└─ Agent3: SecurityAuditor (vulnerabilities, access control)

Data flow: Code → S1 → S2 → S3 → Report
```

**Why this pattern?**
- Reasoning requires cumulative understanding (S1 context → S2 → S3)
- Collaboration emerges naturally from sequential synthesis
- Governance enforced at output: "Final report must mention all 3 aspects"

#### Case 2: Bug Investigation (Parallel Hypothesis Testing)

**Desired Cognitive Functions:**
- Perception: Observe system state from multiple angles
- Reasoning: Generate independent hypotheses
- Reflection: Evaluate which hypothesis best explains symptoms
- Collaboration: Achieve consensus on root cause

**Framework Design:**
```
Topology: Parallel Exploration (4 agents)
├─ Agent1: StaticAnalyzer (code patterns)
├─ Agent2: DynamicTracer (runtime behavior)
├─ Agent3: HistoryAnalyzer (similar past issues)
└─ Agent4: Synthesizer (consensus on root cause)

Data flow: Symptoms → {A1, A2, A3} (parallel) → Synthesize → Report
```

**Why this pattern?**
- Perception needs multiple perspectives (parallel observation)
- Reasoning is hypothesis-generation (independent from each other)
- Reflection + collaboration happen in synthesis phase
- Governance: "Report only if 2+ agents agree"

#### Case 3: Multi-Step Refactoring (Hierarchical with Graph)

**Desired Cognitive Functions:**
- Perception: Detect refactoring opportunities
- Memory: Track interdependencies
- Reasoning: Plan sequence of changes
- Action: Execute safe transformations
- Reflection: Verify each change maintains semantics
- Governance: Only auto-execute safe changes; flag risky ones

**Framework Design:**
```
Topology: Hierarchical (Coordinator + Specialists) + Graph Dependencies

Coordinator:
├─ Detects opportunities
├─ Builds dependency DAG
└─ Routes to specialists (SafeRefactorer, RiskyRefactorer)

Specialists execute in DAG order:
├─ Variable Rename (safe, parallel)
├─ Function Extract (medium risk, sequential)
└─ Loop Optimization (risky, requires approval)

Governance:
├─ Auto-approve: Style changes (formatter)
├─ Require review: Logic changes
└─ Require human approval: Type signature changes
```

**Why this pattern?**
- Hierarchical coordinator enables memory of dependencies (DAG)
- Graph topology respects ordering (Extract must follow detection)
- Governance enforces safety (some changes auto, some flagged)

### Evaluation

**Coverage Analysis:**
- All 28 named design patterns mapped to the 7×6 matrix
- 90%+ coverage of patterns found in 50+ frameworks
- Remaining 10% are domain-specific variations

**Practitioner Survey:**
- 25 practitioners rated the framework's usefulness (1–5 scale)
- Average rating: 4.2/5 for design communication
- 88% found it useful for selecting topologies

**Empirical Validation:**
- Applied framework to 10 new agent designs
- Predicted failure modes with 85% accuracy
- Recommended optimizations validated by practitioners

## Practical Applications & Use Cases

### 1. Design Phase: Architecture Selection
**Scenario:** Team building a code review system

**Process:**
1. List required cognitive functions: Perception, Reasoning, Collaboration, Governance
2. Look up 7×6 matrix for compatible topologies
3. Find: Sequential Chain or Parallel are both suitable
4. Choose based on constraints:
   - Sequential: Low latency, simple implementation → preferred
5. Design: 3 sequential agents (style, logic, security)

### 2. Optimization Phase: Latency Reduction
**Scenario:** Code review system is too slow (8s target, actual 12s)

**Process:**
1. Identify bottleneck: Sequential styling check takes 4s
2. Check matrix: Can Styling be parallelized? No (depends on Logic).
3. Alternative: Parallel independent agents (style vs. logic vs. security in parallel)
   - Trade-off: Loses cumulative reasoning (style insights don't inform logic check)
4. Hybrid: Run style in parallel, then logic + security sequential
5. Result: 12s → 8s (meets target)

### 3. Robustness Phase: Failure Mode Analysis
**Scenario:** Peer network code review sometimes fails to reach consensus

**Process:**
1. Check matrix: Peer topology has "Low resilience" (from table)
2. Root cause: With odd number of agents (5), reaching consensus requires all agree (unlikely)
3. Solution: Switch to Hierarchical topology with Coordinator as tiebreaker
4. Result: Consensus success rate improves 60% → 90%

### Integration Challenges
- **Pattern mismatch:** Choosing Peer network for Governance (incompatible); hard to enforce centralized rules
- **Topology mismatch:** Hierarchical coordinator becomes bottleneck with 10+ specialists
- **Function evolution:** Adding Reflection function mid-project; requires topology redesign

### Cost and Latency Trade-offs
- **Sequential:** Low cost, high latency (sum of steps)
- **Parallel:** High cost (N agents), low latency (max of agents)
- **Hierarchical:** Medium cost, medium latency (depends on specialist count)

**ROI:** Framework helps teams avoid suboptimal patterns (e.g., Peer network for strict Governance) that waste resources.

## Insights & Implications

### Impact on Agent-Driven Development
1. **Shared Language:** Teams now have vocabulary to discuss agent design ("Let's use Plan-and-Execute pattern")
2. **Pattern Reuse:** Successful patterns from one project transfer to others (less redesign effort)
3. **Principled Decisions:** Topology selection moves from ad-hoc to systematic

### Key Findings
1. **No universal best topology:** Suitability depends on required cognitive functions
2. **Function-topology alignment matters:** Misaligned choices (e.g., Peer for strict Governance) lead to failures
3. **Hybrid patterns common:** Real systems mix topologies (Sequential + Graph + Hierarchical)

### Limitations and Open Questions
1. **Scalability bounds:** What's the maximum reasonable agent count per topology?
2. **Emerging patterns:** New cognitive functions or topologies may emerge as agents advance
3. **Cross-domain transfer:** Framework developed for code; applicability to other domains unclear
4. **Quantitative metrics:** Current framework is qualitative; quantifying function-topology fitness is open

### Relevance to Skill Frameworks
- **Skill as cognitive function:** Skills should declare which functions they implement (perception, memory, reasoning)
- **Topology-skill matching:** Orchestrator selects topologies that best support available skills
- **Skill composition:** Combining skills with complementary functions in compatible topologies

## Code & Resources

### Framework Reference Implementation
- **Repository:** [2D-Agent-Framework](https://github.com/a-star-research/agent-design-patterns)
- **Language:** Python + Markdown (reference guide)
- **Components:**
  - Classification matrix (7×6 JSON)
  - 28+ design pattern templates
  - Topology selection guide
  - LLM prompts for pattern implementation

### Dependencies
- Python 3.9+
- Framework libraries: `autogen`, `crewai`, `metagpt`, `langgraph`
- Visualization: `matplotlib`, `networkx` (for topology diagrams)

### Quick-Start Guide

#### Step 1: Identify Required Cognitive Functions
```python
from agent_patterns import CognitiveFunction, ExecutionTopology

# Define your agent system requirements
required_functions = [
    CognitiveFunction.PERCEPTION,
    CognitiveFunction.REASONING,
    CognitiveFunction.COLLABORATION,
    CognitiveFunction.GOVERNANCE,
]
```

#### Step 2: Find Compatible Topologies
```python
# Query the matrix for topologies that support all required functions
compatible_topologies = find_compatible_topologies(required_functions)
# Result: [ExecutionTopology.SEQUENTIAL, ExecutionTopology.HIERARCHICAL]
```

#### Step 3: Evaluate Trade-offs
```python
topologies = [ExecutionTopology.SEQUENTIAL, ExecutionTopology.HIERARCHICAL]
for topology in topologies:
    metrics = get_topology_metrics(topology)
    print(f"{topology}: latency={metrics.latency}, complexity={metrics.complexity}")
    
# Sequential: latency=medium, complexity=low
# Hierarchical: latency=medium, complexity=medium
```

#### Step 4: Design the System
```python
# Load pattern template for Sequential Chain
pattern = load_pattern("Plan-and-Execute")

# Customize for your domain
agents = [
    pattern.Agent1(role="CodeUnderstanding", model="gpt-4"),
    pattern.Agent2(role="DesignPlanning", model="gpt-4"),
    pattern.Agent3(role="Implementation", model="gpt-4"),
]

orchestrator = SequentialOrchestrator(agents=agents)
```

### Compute Requirements
- Framework reference: No API calls (local implementation)
- Actual agent system: Depends on topology (parallel = N×cost, sequential = 1×cost)

## Related Work & Context

### Foundational Agent Architecture Papers
- "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (Microsoft)
- "MetaGPT: Assigning Industrial-Specific Roles to LLM Agents"
- "Agentic Design Patterns: A System-Theoretic Framework" (2601.19752)

### Cognitive Science References
- "Cognition as a Foundation for Autonomous AI" (reasoning, memory, reflection)
- "Organizational Design and Hierarchy" (team structures, delegation patterns)
- "Distributed Consensus Mechanisms" (peer networks, governance)

### Related Papers on Multi-Agent Systems
- "Understanding Multi-Agent LLM Frameworks: A Unified Benchmark" (2602.03128)
- "AdaptOrch: Task-Adaptive Multi-Agent Orchestration" (2602.16873)
- "Architecting Agentic Communities using Design Patterns" (2601.03624)

### Possible Extensions
1. **Automated pattern selection:** Build a classifier that recommends patterns given a task description
2. **Dynamic pattern switching:** Agent system that changes topology mid-task based on observed challenges
3. **Pattern-specific benchmarks:** Evaluate each pattern separately to quantify trade-offs
4. **Cross-domain patterns:** Extend framework to non-code domains (science, business, healthcare)

---

**Citation:**
```
@article{huang2026two,
  title={A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology},
  author={Huang, Jia and Zhou, Joey Tianyi},
  journal={arXiv preprint arXiv:2605.13850},
  year={2026}
}
```

**Sources:**
- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2605.13850)
- [Paper on arXiv (HTML)](https://arxiv.org/html/2605.13850)
