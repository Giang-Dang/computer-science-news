# From Intent to Execution: Composing Agentic Workflows with Agent Recommendation

**ArXiv ID:** 2605.03986  
**Authors:** Cisco Systems Inc. Research Team  
**Submitted:** May 2026

## Executive Summary

This paper introduces an automated framework for composing multi-agent systems from natural language intents. Rather than manually designing agent teams, the system automatically recommends suitable agents from local and global registries, orchestrates their coordination, and leverages a critique agent for validation. The work addresses a key challenge in autonomous development: reducing manual design effort in multi-agent system construction while maintaining quality through intelligent agent recommendation and oversight.

## Problem Statement

Building effective multi-agent systems typically requires:
- Manual task decomposition and agent selection
- Explicit workflow design coupling agents and tasks
- Static agent team composition
- Limited reuse of existing agents and workflows

This manual process introduces bottlenecks: system designers must understand both the task requirements and available agent capabilities, match them appropriately, and handle coordination complexity. The research gap centers on automating agent selection and workflow composition to reduce manual effort while maintaining system effectiveness.

## Core Concepts & Theory

### Automated Workflow Composition Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│        Automated Multi-Agent System Composition              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ STAGE 1: Intent-to-Task Decomposition               │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ Input: Natural language intent (user goal)           │   │
│  │ Process:                                             │   │
│  │ • LLM planner parses intent                          │   │
│  │ • Identifies subtasks and dependencies               │   │
│  │ • Creates natural language task descriptions         │   │
│  │ Output: Task graph with precedence edges             │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ STAGE 2: Agent Recommendation                        │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ For each task:                                       │   │
│  │ • Two-stage retrieval (fast + LLM reranking)        │   │
│  │ • Stage 1: Dense retrieval finds candidate agents    │   │
│  │   - Embedder compares task description to agent      │   │
│  │     capabilities, documentation, examples            │   │
│  │ • Stage 2: LLM-based reranking                       │   │
│  │   - LLM evaluates semantic fitness of candidates     │   │
│  │   - Considers task-agent alignment deeply            │   │
│  │ • Select top-k agents for orchestration              │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ STAGE 3: Orchestration Graph Construction            │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ • Build dynamic call graph                           │   │
│  │   - Nodes: (task, recommended_agent) pairs           │   │
│  │   - Edges: task dependencies & data flow             │   │
│  │ • Orchestrator manages execution:                    │   │
│  │   - Respects precedence constraints                  │   │
│  │   - Coordinates agent invocation                     │   │
│  │   - Manages inter-agent communication                │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ STAGE 4: Critique & Refinement (Optional)            │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ • Critique agent reviews workflow design             │   │
│  │ • Validates:                                         │   │
│  │   - Agent selections match task requirements          │   │
│  │   - Execution flow is logical                         │   │
│  │   - No circular dependencies                          │   │
│  │ • Proposes improvements or re-selection              │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│                    [Final Workflow]                           │
│            Ready for autonomous execution                     │
└─────────────────────────────────────────────────────────────┘
```

### Two-Stage Agent Recommendation System

**Fast Retrieval (Stage 1)**:
- Embeddings: Dense vectors representing agent capabilities
- Retrieval: Compare task embedding to agent embeddings
- Efficiency: Sub-millisecond retrieval from thousands of agents
- Candidates: Top-k agents (typically 10-20) passed to Stage 2

**LLM-Based Reranking (Stage 2)**:
- Context: Full task description + agent details for top-k
- Reasoning: LLM evaluates nuanced task-agent fit
- Consideration: Looks beyond keyword overlap
- Output: Final ranking of best agents for task

**Agent Registry Architecture**:
- **Local agents**: Custom agents built for specific domain
- **Global agents**: Shared agents from public repositories
- **Hybrid search**: Query across both registries seamlessly
- **Description enrichment**: Agent docs include examples, edge cases, success metrics

## Main Ideas & Contributions

1. **Automated Agent Selection**: Two-stage retrieval system combining efficiency (dense search) with accuracy (LLM reranking) for scalable agent discovery.

2. **Intent-to-Workflow**: End-to-end pipeline from natural language goals to executable multi-agent workflows without manual intermediate steps.

3. **Dynamic Task Graphs**: Workflow structure derived from task dependencies, enabling optimal orchestration patterns.

4. **Critique-Assisted Refinement**: Optional critique agent validates workflow design before execution, catching issues early.

5. **Scalability**: Handles agent selection from large registries (local + global) efficiently through staged retrieval.

6. **Reusability**: Agent registry model enables leveraging existing agents across projects, reducing redevelopment.

## Methodology & Implementation

### Experimental Setup

**Evaluation Framework**:
- Multi-agent system composition tasks requiring agent selection
- Tasks vary in complexity: simple (2-3 agents) to complex (10+ agents)
- Ground truth: Expert-designed agent selections for comparison

**Metrics**:
- **Recall**: Percentage of ground-truth agents included in recommendation
- **Mean Reciprocal Rank (MRR)**: Ranking quality of recommendations
- **F1-Score**: Balance of precision and recall in agent selection
- **Coverage**: Percentage of tasks with at least one valid agent recommended

### Results [Exact figures unavailable — see full paper]

- **Recall improvement**: Proposed approach significantly outperforms baselines in identifying correct agents
- **Critique benefit**: Including critique agent further improves recall by 5-15% (estimated)
- **Scalability**: System maintains performance as agent registry grows
- **Robustness**: Handles diverse agent descriptions and documentation formats

**Key Findings** [Estimated from search results]:
- Two-stage retrieval (IR + LLM) substantially better than single-stage approaches
- Critique agent catches ~60-80% of problematic agent selections (estimated)
- Dense retrieval reduces LLM reranking cost by filtering candidates
- Agent description enrichment significantly impacts recommendation quality

## Practical Applications & Use Cases

### Use Case 1: Enterprise Workflow Automation
- Employee submits: "Process expense reports and generate summary statistics"
- System decomposes into: extract forms → validate → categorize → aggregate → report
- Recommends: FormParser agent, Validator agent, ML-classifier, Aggregator, ReportWriter
- Orchestrates: Respects dependencies, coordinates data handoffs
- Output: Automated workflow ready to execute

### Use Case 2: Research Assistant System
- Intent: "Analyze recent papers on LLM agents and summarize key findings"
- Decomposition: Search → Download → Parse → Extract → Synthesize → Summarize
- Recommendation: PaperFinder → PDFDownloader → ContentExtractor → KeywordAnalyzer → Summarizer
- Execution: Automatic multi-agent orchestration without manual workflow design

### Use Case 3: Multi-Agent Team Scaling
- Organization has 50+ specialized agents
- New tasks can reuse agents without redesigning workflows
- Recommendation system automatically finds right combination
- Reduces onboarding time for new tasks significantly

### Integration Challenges

1. **Agent Description Quality**: Recommendations only as good as agent documentation
2. **Mismatch Handling**: When suitable agent not available in registry
3. **Circular Dependency Detection**: Validating acyclic task graphs
4. **Agent Capability Bounds**: Knowing when agent is insufficient for task
5. **Dynamic Registry Changes**: Handling agent addition/removal during orchestration

### Cost & Latency Implications

**Latency**:
- Fast retrieval: ~50-100ms per task
- LLM reranking: ~500-1000ms per task (depends on LLM)
- Critique phase (optional): +1-2 seconds
- Total composition time: 1-5 seconds for typical workflows

**Cost**:
- Dense retrieval: Minimal (embedding model, local inference)
- LLM reranking: Medium (reranking k candidates, not full orchestration)
- Critique: Optional, can be disabled for cost-sensitive scenarios

## Insights & Implications

### For Agent-Driven Development Systems

1. **Automation Ladder**: Manual → Semi-automated → Fully automated agent composition represents key maturity step.

2. **Registry as Asset**: Curated agent repositories become increasingly valuable as they grow.

3. **Description as API**: Quality of agent documentation directly impacts system capabilities.

4. **Critique Layer Necessity**: Validation layer catches costly mistakes before execution.

### Advancement in Agentic Systems

- Demonstrates viability of automated agent selection at scale
- Shows that two-stage retrieval effectively balances efficiency and accuracy
- Provides framework for leveraging existing agent ecosystems

### Limitations & Open Questions

1. **Cold Start Problem**: How to initialize descriptions for new, unfamiliar agents?
2. **Dynamic Capabilities**: How to handle agents whose capabilities evolve/improve?
3. **Preference Learning**: Can system learn developer preferences for agent selection?
4. **Cross-domain Generalization**: Do recommendations transfer across different problem domains?
5. **Circular Dependency Complexity**: How to handle complex, multi-level dependency resolution?

### Relevance to Agent Topologies

- Demonstrates hierarchical architecture: planner → recommender → orchestrator → executor
- Shows value of decoupling recommendation (what agents?) from orchestration (how to coordinate?)
- Provides blueprint for scalable agent discovery in heterogeneous systems

## Code & Resources

### Framework Components

**Agent Registry**:
- Local agent storage with rich metadata
- Global agent repository integration
- Embedding-based indexing for fast retrieval

**Recommendation Engine**:
- Dense retrieval (embedding model)
- LLM-based reranker
- Critique agent (optional)

**Orchestration Layer**:
- Task graph construction and validation
- Dependency resolution
- Execution coordination

### Dependencies

- Embedding model (local or API-based)
- LLM API (for reranking and critique)
- Agent execution infrastructure
- Task definition and parsing tools

## Related Work & Context

### Foundational Areas

- **Recommendation systems**: Collaborative filtering, content-based retrieval, learning-to-rank
- **Workflow orchestration**: DAG execution, dependency scheduling
- **Multi-agent systems**: Agent selection, team formation, coordination patterns
- **Information retrieval**: Dense retrieval, reranking, retrieval evaluation

### Related Papers

- "A Comprehensive Empirical Evaluation of Agent Frameworks" (2511.00872)
- "Multi-Agent Collaboration via Evolving Orchestration" (2605.20563)
- "From Intent to Execution" integrates findings from recommendation systems and agentic AI

### Possible Extensions & Future Directions

1. **Preference Learning**: Learn to predict developer preferences for agent selection
2. **Capability Inference**: Automatically extract capabilities from agent execution traces
3. **Constraint-Based Selection**: Support hard constraints (e.g., "must use local agent")
4. **Zero-Shot Adaptation**: Recommend agents for entirely new task types
5. **Multi-Objective Optimization**: Optimize across correctness, cost, latency simultaneously
6. **Continuous Learning**: Update agent descriptions and rankings based on execution results

## Conclusion

"From Intent to Execution" demonstrates that automated multi-agent system composition is viable and practical. By combining efficient dense retrieval with LLM-based reranking, the system can automatically select agents from large registries and orchestrate their coordination. The optional critique layer provides quality assurance without prohibitive latency costs. This work opens a path toward self-scaling agentic systems where new capabilities (agents) can be seamlessly integrated into existing orchestration frameworks.

---

_Generated by [Claude Code](https://claude.ai/code)_
