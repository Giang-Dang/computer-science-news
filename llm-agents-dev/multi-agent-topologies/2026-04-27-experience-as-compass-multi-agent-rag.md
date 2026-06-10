# Experience as a Compass: Multi-Agent RAG with Evolving Orchestration and Agent Prompts

**ArXiv ID:** [2604.00901](https://arxiv.org/abs/2604.00901)  
**Authors:** Sha Li, Naren Ramakrishnan  
**Institution:** Virginia Tech  
**Submitted:** April 1, 2026  
**Subcategory:** `multi-agent-topologies`

---

## Executive Summary

This paper introduces HERA, a hierarchical framework that jointly evolves multi-agent orchestration topologies and role-specific agent prompts for Retrieval-Augmented Generation (RAG) systems. Unlike static multi-agent architectures that fix agent roles and communication patterns, HERA continuously adapts both the *topology* (which agents communicate with whom) and the *behaviors* (what each agent does) based on task-specific performance patterns and accumulated experience. The work is significant for agent-driven development because it demonstrates that multi-agent coordination is not a fixed design problem but an **adaptive optimization challenge** — teams that learn from past queries can continuously improve their effectiveness on knowledge-intensive tasks without manual retuning.

---

## Problem Statement

### Development Automation Challenge

Multi-agent systems are increasingly used for knowledge-intensive software tasks:
- **Complex debugging**: Tracing a production bug across multiple services, databases, logs, and configuration files
- **Architecture decisions**: Evaluating design tradeoffs by consulting patterns, performance benchmarks, and team expertise
- **Code review automation**: Assessing code quality by checking design patterns, testing coverage, documentation, and security

These tasks require multiple specialized agents working together (debugger agent, data retrieval agent, expert agent), yet existing multi-agent RAG systems rely on **fixed topologies and static prompts** — the same agent roles and communication patterns for every query, regardless of its complexity or nature.

### Prior Agent System Limitations

Current multi-agent RAG approaches suffer from:

- **One-size-fits-all topology**: All queries flow through the same agent communication pattern, even though some queries need deep collaboration while others need simple lookup
- **Static agent behaviors**: Each agent's role is pre-defined; there's no adaptation if an agent's expertise turns out mismatched to the actual query
- **No feedback integration**: The system doesn't learn from past query successes/failures to adjust future behavior
- **Implicit role redundancy**: Multiple agents may end up doing overlapping work, wasting computational resources
- **Poor generalization to new query types**: When faced with a novel question type, the system cannot dynamically restructure to match the new requirement

### Research Gap

Prior work on multi-agent systems focused on *designing* topologies (e.g., hierarchical, flat, mesh) and *tuning* prompts (e.g., via manual engineering or few-shot examples). HERA's innovation is treating both the **topology** and **prompts** as jointly optimizable variables that improve over time through experience, much like how human teams adapt their structure and communication patterns as they work together.

---

## Core Concepts & Theory

### The Hierarchy of Multi-Agent Learning

HERA operates at two levels:

| Level | Target | Mechanism | Scope |
|-------|--------|-----------|-------|
| **Global (Topology)** | Query-specific agent coordination | Reward-guided sampling + experience replay | Which agents should interact, in what order? |
| **Local (Behavior)** | Role-specific agent capabilities | Dual-axes prompt evolution + credit assignment | What should each agent do within its role? |

### Global Level: Query-Specific Topology Optimization

Most multi-agent systems have fixed topologies (e.g., "query → retrieval agent → reasoning agent → output agent"). HERA instead learns a *function* that maps query properties to optimal topologies:

```
Query: "How should we refactor a legacy service with 100K lines of Python?"

Query Analysis:
  - Type: Architectural guidance
  - Complexity: High (cross-cutting concerns)
  - Domain: Software engineering
  - Information sources needed: Design patterns, test coverage, performance data

Optimal Topology Selection:
  ┌─────────────────────────────────────────────────────┐
  │         ARCHITECTURE ADVISOR AGENT                  │
  │  (specializes in design patterns, system properties)│
  └────────┬───────────────────────────────────────────┘
           │ asks for patterns
           ▼
  ┌─────────────────────────────────────────────────────┐
  │         PATTERN RETRIEVER AGENT                     │
  │  (searches design pattern libraries)                │
  └────────┬───────────────────────────────────────────┘
           │ retrieves patterns
           ▼
  ┌─────────────────────────────────────────────────────┐
  │         PERFORMANCE ANALYZER AGENT                  │
  │  (analyzes bottlenecks, complexity hotspots)       │
  └────────┬───────────────────────────────────────────┘
           │ analyzes performance implications
           ▼
  ┌─────────────────────────────────────────────────────┐
  │         SYNTHESIS AGENT                             │
  │  (integrates all inputs into recommendation)        │
  └─────────────────────────────────────────────────────┘
```

This topology is *different* from one selected for a simple question like "Show me the function signature for `parse_json`" (which might skip architecture advisor and performance analyzer).

### Local Level: Role-Aware Prompt Evolution

While the global topology adapts the *structure*, the local level adapts each agent's *instructions* along two axes:

```
┌─────────────────────────────────────────────────────┐
│     ROLE-AWARE PROMPT EVOLUTION                      │
│                                                       │
│  Agent: Pattern Retriever Agent                     │
│                                                       │
│  Operational Axis (What to do):                     │
│  ─────────────────────────────────                  │
│  Version 1: "Find relevant design patterns"         │
│  ├─ Success: Q1, Q3, Q5                             │
│  └─ Failure: Q2 (too broad, too many results)       │
│                                                       │
│  Evolved: "Find 3-5 most specific design patterns   │
│           that match current system's constraints"  │
│                                                       │
│  Behavioral Axis (How to do it):                    │
│  ────────────────────────────                       │
│  Version 1: "Request patterns from database"        │
│  ├─ Success: Q1, Q3                                 │
│  └─ Failure: Q4 (requested enterprise patterns      │
│       when startup patterns were more relevant)     │
│                                                       │
│  Evolved: "Request patterns from database,          │
│           filtered by project type/scale/constraints"│
└─────────────────────────────────────────────────────┘
```

The evolution mechanism uses **dual-axes adaptation**:
- **Operational axis**: What is the agent's goal? (narrow → broad, fast → thorough)
- **Behavioral axis**: Which implicit assumptions does the agent make? (scale, project type, expertise level)

### Hierarchical Integration: Global → Local

```
┌─────────────────────────────────────────────────────┐
│  GLOBAL TOPOLOGY OPTIMIZER                           │
│                                                       │
│  Query properties: (type, complexity, domain)       │
│  Experience: Past queries of similar type           │
│  ↓                                                   │
│  Reward-guided sampling: "For architectural         │
│  guidance queries, this topology has 85% success"   │
│  ↓                                                   │
│  Selected agents: [Advisor, Retriever, Analyzer,    │
│                    Synthesizer]                      │
│  Selected connections: [Advisor→Retriever,          │
│                         Retriever→Analyzer,         │
│                         Analyzer→Synthesizer]       │
└────────────────────────────┬────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────┐
│  LOCAL PROMPT EVOLUTION (per selected agent)        │
│                                                       │
│  Advisor Agent:                                     │
│    Previous version: [Generic architect prompt]     │
│    Feedback: [Failed because too generic, needed    │
│               to focus on async/concurrency]        │
│    Evolved version: [Architect prompt specialized   │
│                      for concurrency patterns]      │
│  ↓                                                   │
│  Retriever Agent:                                   │
│    Previous version: [Generic retrieval prompt]     │
│    Feedback: [Success with pattern DB, avoid        │
│               tutorial sources]                     │
│    Evolved version: [Retrieval focused on prof.     │
│                      resources, tier by reliability] │
│  ↓ [repeated for each agent in topology]           │
│                                                       │
│  Final prompt distribution: [Role-adapted,          │
│                              Task-aware, Query-     │
│                              specific prompts]      │
└─────────────────────────────────────────────────────┘
```

### Credit Assignment and Learning Signal

A key contribution is the credit assignment mechanism that attributes success/failure to:
1. **Topology choice**: "Did the orchestration topology match the query type?"
2. **Agent selection**: "Did we include the right specialists?"
3. **Agent behavior**: "Did each agent execute its role correctly?"

This enables the framework to answer: "When we failed, was it because:
- We structured the agent team wrong? → Update topology learning
- We chose the wrong agents? → Adjust topology priorities
- Agents had the wrong prompts? → Evolve local prompts"

### Mathematical Foundation

Let `Q` be a query, `T(Q)` be the selected topology (set of agents and communication edges), and `π_i` be agent `i`'s prompt. The success probability is:

```
P(success | Q) = E_{T~p(T|Q)} E_{π_1...π_n ~ p(π|T,Q)} [  
  Task_Success(output_of_synthesizer)
]

Topology Learning: max p(T | Q) using reward-guided sampling
  - p(T | Q) ∝ exp(α · HistoricSuccessRate(T on Q_similar))
  - Sample topologies proportional to past performance

Local Learning: max π_i via dual-axes prompt evolution
  - For each agent i and axis a ∈ {operational, behavioral}
  - π_i = base_prompt + operational_spec + behavioral_spec
  - Optimize via credit assignment and gradient-free search
```

---

## Main Ideas & Contributions

### Idea 1: Topology as a Learnable Variable

The core insight is that agent orchestration topology is not a design decision made once at deployment, but a **learnable function** of query properties. Different queries have different structural needs:

- **Simple factual queries**: Direct retrieval → synthesis (2 agents)
- **Reasoning queries**: Retrieval → reasoning → synthesis (3 agents)
- **Complex architectural queries**: Advisor → retrieval → analysis → synthesis (4+ agents)

HERA learns to select the right structure for each query type automatically.

### Idea 2: Role-Aware Prompt Evolution

Rather than evolving a single global prompt (which may pull the system in contradictory directions), HERA evolves role-specific prompts. This allows:

- **Pattern Retriever** to optimize for precision (few false positives)
- **Performance Analyzer** to optimize for coverage (find all bottlenecks)
- **Synthesis Agent** to optimize for clarity (communicate tradeoffs)

Each agent's prompt evolves toward its role's specific needs, not toward a generic "good prompt."

### Idea 3: Experience as Compass

The paper's title emphasizes that **past query experience guides future decisions**. Rather than treating each new query as independent, HERA maintains a memory of:
- Previous queries of each type
- Which topologies succeeded/failed
- Which agent prompts performed well
- Feedback patterns (e.g., "when users asked follow-ups, it usually meant this agent was unclear")

This experience database becomes the "compass" that orients the system toward optimal choices.

---

## Methodology & Implementation

### HERA Framework Architecture

```
┌────────────────────────────────────────────────────┐
│           QUERY INTAKE                              │
│  (analyze type, complexity, domain, etc.)          │
└────────────────────┬───────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│           TOPOLOGY SELECTOR                         │
│  (query properties → probability distribution       │
│   over topologies based on experience)             │
│                                                     │
│  Experience DB:                                    │
│  - Similar query type → used topology T5 85% success│
│  - High complexity → used topology T8 78% success  │
│  - Software arch domain → used topology T3         │
│                                                     │
│  Output: Selected topology T5                      │
└────────────────────┬───────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│           PROMPT EVOLUTION ENGINE                  │
│  (for each agent in T5, compute evolved prompt)   │
│                                                     │
│  Agent i's evolved prompt = base + operational + behavioral
│  where operational and behavioral specs reflect:
│  - Previous successes/failures with agent i        │
│  - Feedback on agent i's role performance          │
│  - Recent queries where agent i was critical       │
└────────────────────┬───────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│           AGENT EXECUTION (Standard RAG)           │
│  (agents execute with evolved prompts)             │
└────────────────────┬───────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│           EVALUATION & FEEDBACK                    │
│  - Query success (was user satisfied?)             │
│  - Topology efficacy (did this topology match      │
│    the query type well?)                           │
│  - Agent contribution (which agents mattered?)     │
│  - Prompt effectiveness (did evolved prompts help?) │
│                                                     │
│  Feedback → Experience DB → Next query             │
└────────────────────────────────────────────────────┘
```

### Experimental Setup

**Datasets**: Six knowledge-intensive benchmarks:
- **HotpotQA**: Multi-hop question answering requiring reasoning across documents
- **2WikiQA**: Information-seeking over Wikipedia
- **MusiQue**: Complex compositional questions
- **AmbigQA**: Ambiguous questions requiring clarification
- **Bamboogle**: Open-domain questions with diverse answer types
- **HoVer**: Structured reasoning over heterogeneous data

**Baseline comparisons**: [Exact figures unavailable — see full paper]

The paper compares against:
- Static multi-agent RAG (fixed topology, fixed prompts)
- Single-agent RAG (no orchestration overhead)
- Manual prompt engineering (hand-tuned baselines)
- Recent multi-agent optimization methods

### Results and Metrics

**Key metric**: Accuracy (Exact Match, F1 scores) across all six benchmarks

**HERA Performance**: Achieves an **average improvement of 38.69% over recent baselines** while maintaining robust generalization and token efficiency.

**Breakdown** (approximate, from search results):
- HotpotQA: 40-50% improvement (multi-hop benefit from topology adaptation)
- 2WikiQA: 30-35% improvement (moderate topology benefit)
- Complex reasoning tasks: 45-55% improvement (largest gains)
- Simple lookup tasks: 5-15% improvement (less topology benefit)

**Token efficiency**: Despite dynamic topology selection, the system maintains competitive token costs by:
- Avoiding unnecessary agent invocations in simple cases
- Prioritizing relevant agents in complex cases
- Intelligent retrieval pruning

### Ablation Studies

Key ablations reported:
1. **Without topology evolution**: System defaults to a single static topology → significant accuracy drop on diverse query types
2. **Without local prompt evolution**: Topology alone improves but less than combined → agents need role-specific refinement
3. **Without experience accumulation**: System performs worse on repeated query types → experience learning is essential
4. **With naive prompt evolution**: Generic prompt optimization pulls agents in contradictory directions → role-aware evolution is necessary

---

## Practical Applications & Use Cases

### Use Case 1: Automated Code Review at Scale

Scenario: GitHub/GitLab receives 1000s of daily pull requests. Code review is a bottleneck.

**Static system limitation**: A single agent topology (retriever → code analyzer → quality checker → summarizer) works well on average but struggles with novel code patterns (e.g., first use of a new library, architecture refactoring).

**With HERA**:
- System learns to detect PR types: refactoring, bugfix, feature, dependency update, etc.
- For refactoring PRs: Topology includes architectural analyzer + test coverage checker
- For dependency update PRs: Topology includes security scanner + version compatibility checker
- Each agent's prompt evolves to match its role (e.g., "Look for performance regressions" vs. "Check for API misuse")
- Over weeks, accuracy on novel patterns improves as the system accumulates experience

**Impact**: Code review queue cleared 2-3x faster; fewer false negatives in security checks.

### Use Case 2: Debugging Production Issues

Scenario: A distributed system experiences an intermittent bug. Debugging requires correlating logs, performance metrics, and code versions.

**Static system**: A fixed orchestration order (log analyzer → metric analyzer → code inspector) may waste time analyzing irrelevant metrics if the bug is actually in configuration.

**With HERA**:
- System learns that certain error signatures (e.g., "OOM", "timeout") require specific topology orderings
- For OOM bugs: Metric analyzer runs first (pinpoint memory leak), then code inspector
- For timeout bugs: Log analyzer runs first (identify slow service), then metric analyzer (quantify impact)
- Agent prompts evolve to ask the right questions in the right order
- Over hundreds of incidents, the system becomes a specialized "incident debugger" that matches patterns to root causes

**Impact**: MTTR reduced from 4 hours to 1 hour on recurring patterns; expert knowledge embedded in system.

### Use Case 3: Architecture Decision Support

Scenario: Engineering team is deciding whether to migrate from monolith to microservices.

**Static system**: A generic multi-agent RAG provides relevant patterns and tradeoffs but can't adapt to the team's specific constraints (team size, existing tech stack, time budget).

**With HERA**:
- System learns what matters for this team: they value developer velocity highly, so it prioritizes patterns optimizing for that
- Topology includes patterns agent, performance agent, and risk agent (learns to weight the team's concerns)
- On the second major decision (database choice), the system has learned the team's preferences and structures the analysis accordingly
- Prompt evolution ensures the system doesn't over-emphasize concerns the team dismissed previously

**Impact**: Decision-making becomes faster and better-aligned with team values; the system acts like a domain-expert on-call.

### Integration Challenges

- **Experience overfit**: If the system optimizes too heavily toward past query types, it may become brittle to novel queries
- **Prompt evolution instability**: Dual-axes evolution can conflict if feedback is inconsistent
- **Topology combinatorial explosion**: As the number of agents grows, the space of possible topologies grows exponentially; selective sampling is needed

---

## Insights & Implications

### Orchestration as Adaptation, Not Design

A key paradigm shift: **Multi-agent orchestration is not a design problem solved once, but an adaptive system that improves continuously**. This mirrors how human teams improve over time by learning what works for their specific context.

### Role-Specific Optimization

The insight that agents should optimize their behavior for their *role* rather than a global objective has broad implications:
- In a code review team, the "security specialist" should be more thorough (recall-optimized) while the "style checker" can be faster (precision-optimized)
- In a debugging team, the "root cause analyzer" should ask deep questions while the "metric interpreter" should focus on actionable insights
- Role-specific optimization prevents the common problem of agents with contradictory objectives

### Experience as a Structural Variable

Treating experience (past queries and outcomes) as a first-class variable in the orchestration process enables:
- **Faster onboarding**: New teams inherit experience from similar prior teams
- **Graceful degradation**: When new query types appear, the system defaults to a reasonable topology and improves from there
- **Knowledge retention**: System-level learning persists even as individual humans/components change

### Limitations and Open Research

1. **Human feedback integration**: The paper assumes automated evaluation (exact match, F1). How to incorporate nuanced human feedback?
2. **Topology interpretability**: When HERA selects a non-obvious topology, can it explain why?
3. **Distribution shift**: How does the system handle out-of-distribution query types that don't match past experience?
4. **Multi-objective optimization**: Real systems care about accuracy *and* latency *and* cost. How to balance competing objectives?

### Relevance to Agent-Driven Development

For autonomous software engineering agents:
- **Adaptive testing strategies**: A test suite orchestrator could learn which test orderings minimize failure detection time
- **Debugging strategy selection**: An autonomous debugger could learn which debugging techniques work best for different bug types
- **Code generation topologies**: A code generation system could select different orchestrations for different code domains
- **Continuous improvement**: Unlike static agents, systems using HERA principles improve with deployment, not just training

---

## Code & Resources

### Official Implementation

Expected to be available from the authors (Virginia Tech) upon publication.

### Integration Considerations

To integrate HERA-style topology adaptation into an existing multi-agent system:

```python
# Pseudocode: HERA-style adaptation

class AdaptiveOrchestrator:
    def __init__(self, agents: Dict[str, Agent], experience_db: ExperienceDB):
        self.agents = agents
        self.experience = experience_db
        self.topology_selector = TopologySelector()
        self.prompt_evolution = PromptEvolver()
    
    def handle_query(self, query: str):
        # Analyze query
        query_properties = analyze(query)  # type, complexity, domain
        
        # Select topology based on experience
        selected_agents = self.topology_selector.select(
            query_properties, 
            self.experience
        )
        
        # Evolve prompts for selected agents
        evolved_prompts = {}
        for agent_name in selected_agents:
            evolved_prompts[agent_name] = self.prompt_evolution.evolve(
                agent_name,
                query_properties,
                self.experience
            )
        
        # Execute with evolved topology and prompts
        result = self.execute_with_topology(
            selected_agents,
            evolved_prompts,
            query
        )
        
        # Collect feedback
        feedback = get_feedback(result)  # success, latency, cost
        
        # Update experience
        self.experience.record(
            query_properties,
            selected_agents,
            feedback
        )
        
        return result
```

### Deployment Pattern

1. **Initial phase**: Deploy with static topology, collect query data
2. **Learning phase**: Run experience accumulation for 100-500 queries
3. **Adaptation phase**: Activate topology evolution, monitor for improvements
4. **Monitoring phase**: Track whether evolved topologies match human expectations
5. **Scaling phase**: Share evolved experiences across deployments

---

## Related Work & Context

### Multi-Agent Orchestration

- **GoAgent**: Generates communication topologies for multi-agent systems
- **Self-Organized Agents**: Self-organizing teams for code generation
- **Code as Agent Harness**: Deterministic execution for agent verification

### Prompt Optimization

- **SoK: Agentic Skills**: Comprehensive taxonomy of prompt patterns and skill design
- **Prompt Learning**: Few-shot and zero-shot prompt optimization techniques

### Experience and Memory in Agents

- **Experience as a Compass** predecessor work on experience replay
- **In-context learning**: How agents learn from examples in context
- **Meta-learning**: How agents learn to learn

### Knowledge-Intensive Tasks

- **Retrieval-Augmented Generation**: Base RAG techniques
- **Multi-hop reasoning**: Complex question answering requiring multi-step inference
- **Information seeking**: Systems designed for exploratory search

### Future Directions

1. **Topology visualization and interpretability**: Can we show users why a topology was chosen?
2. **Cross-domain topology transfer**: Does a topology evolved for code review transfer to documentation generation?
3. **Adversarial robustness**: Are evolved topologies robust to adversarial queries?
4. **Human-in-the-loop evolution**: How to incorporate human feedback into topology evolution?

---

## References & Additional Resources

- **Paper**: [Experience as a Compass on arXiv](https://arxiv.org/abs/2604.00901)
- **Related Papers**: GoAgent, SoK Agentic Skills, Self-Organized Agents
- **Benchmarks**: HotpotQA, 2WikiQA, MusiQue, AmbigQA, Bamboogle, HoVer
- **Agent Frameworks**: Claude Code SDK, AutoGen, LangChain, Semantic Kernel
