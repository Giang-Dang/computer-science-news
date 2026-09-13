# Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads

**ArXiv ID:** 2606.06448  
**Authors:** Yasmine Omri, Ziyu Gan, Zachary Broveak, Robin Geens, Zexue He, Alex Pentland, Marian Verhelst, Tsachy Weissman, Thierry Tambe  
**Submitted:** June 2026  
**Link:** https://arxiv.org/abs/2606.06448

## Executive Summary

This paper presents the first comprehensive systems characterization of agent memory systems—the infrastructure that enables LLM agents to persistently store, retrieve, and update memory across long-horizon multi-turn interactions. The authors introduce a system-oriented taxonomy classifying memory systems across four axes, develop a phase-aware profiling harness that attributes computational costs to construction, retrieval, and generation phases, and characterize ten representative agent memory systems. The characterization uncovers critical design tradeoffs between write-path and read-path efficiency, reveals that different workload patterns favor different memory architectures, and derives ten actionable system recommendations for designing memory systems for multi-agent orchestration. This work is essential for building scalable and efficient agent teams that maintain shared state across extended interactions.

## Problem Statement

LLM agents deployed on realistic long-horizon tasks face a fundamental challenge: they must maintain context and state across many turns of interaction, often spanning thousands of tokens. This creates several problems:

### Current Memory System Limitations

1. **Context Window Constraints**: LLMs have fixed context windows (4K-200K tokens depending on model). Long-horizon tasks quickly exceed these windows, requiring explicit memory management.

2. **Retrieval-Generation Tradeoff**: Retrieving all relevant history at each turn (comprehensive but slow) vs. only recent turns (fast but forgetful). No principled way to balance this tradeoff.

3. **Cost Accumulation**: Each turn requires re-processing of memory (read operations) and updating with new information (write operations). Costs compound over long interactions, making large-scale agent deployments expensive.

4. **Heterogeneous Designs**: Different projects implement agent memory differently (flat retrieval, LLM-mediated extraction, consolidated fact stores, agentic control flows), with no systematic understanding of the design space.

5. **Missing Design Guidance**: When building multi-agent systems, it's unclear which memory architecture to choose:
   - Flat retrieval: Simple but expensive
   - Consolidated facts: Efficient but lossy
   - Hierarchical: Flexible but complex
   - Agentic: Powerful but slow

### Research Gap

While agent memory systems are widely deployed (Claude, GPT-4, etc.), their **system-level behavior** remains uncharacterized. There's no systematic understanding of:
- Cost profiles across memory operations
- Tradeoffs between accuracy and efficiency
- Design space of memory architectures
- Guidance for practitioners building agent systems

This paper fills that gap with a comprehensive systems characterization.

## Core Concepts & Theory

### System-Oriented Taxonomy of Agent Memory

The paper classifies agent memory systems along four dimensions:

**Dimension 1: Memory Storage Architecture**

```
┌─────────────────────────────────────────┐
│ Agent Memory Storage Approaches         │
├─────────────────────────────────────────┤
│                                         │
│ 1. Flat Retrieval                       │
│    - All historical context stored      │
│    - Retrieved verbatim on each turn    │
│    - Simple, lossless, expensive        │
│                                         │
│ 2. LLM-Mediated Extraction             │
│    - Agent runs extraction step         │
│    - Summarizes/compresses history     │
│    - Overhead on write path              │
│                                         │
│ 3. Consolidated Fact Stores            │
│    - Parse history into structured      │
│      facts (entities, relationships)    │
│    - Query by relevance                 │
│    - Lossy but efficient                │
│                                         │
│ 4. Agentic Control Flows               │
│    - Specialized agent manages memory  │
│    - Autonomous curation of facts      │
│    - Powerful but slowest              │
│                                         │
└─────────────────────────────────────────┘
```

**Dimension 2: Retrieval Strategy**

- **Semantic Similarity**: Embed turn history, retrieve k most relevant turns
- **Recency-based**: Retrieve last N turns
- **Hybrid**: Combine recent + relevant
- **Entity-based**: Retrieve turns mentioning specific entities
- **Agentic**: Let agent decide what to retrieve

**Dimension 3: Cost Amortization**

- **Per-turn**: Process immediately after each turn (immediate cost)
- **Periodic**: Batch process every N turns (amortized cost)
- **On-demand**: Process only when memory is queried (lazy cost)

**Dimension 4: Freshness-Latency Tradeoff**

- **Immediate reflection**: Consistency but higher latency
- **Eventually consistent**: Lower latency but staleness
- **Stale allowed**: Fastest but risk of outdated state

### Phase-Aware Cost Model

Agent memory systems incur costs across three phases:

```
┌─────────────────────────────────────────────────────┐
│ Agent Memory Cost Model                             │
├─────────────────────────────────────────────────────┤
│                                                     │
│ WRITE PATH (after each turn):                       │
│ ┌─────────────────────────────────────┐             │
│ │ Input: New turn history (actions,  │             │
│ │        observations, reasoning)     │             │
│ │ ↓                                   │             │
│ │ Extraction: Parse, compress,       │             │
│ │ structure turn content              │             │
│ │ Cost: Tokens for LLM, embeddings,  │             │
│ │       storage writes                │             │
│ │ ↓                                   │             │
│ │ Indexing: Add to retrieval index   │             │
│ │ Cost: Embedding cost, index updates │             │
│ │ ↓                                   │             │
│ │ Storage: Persist extracted facts    │             │
│ │ Cost: DB writes, memory allocation  │             │
│ └─────────────────────────────────────┘             │
│                                                     │
│ READ PATH (during agent reasoning):                 │
│ ┌─────────────────────────────────────┐             │
│ │ Input: Current task context         │             │
│ │ ↓                                   │             │
│ │ Retrieval: Find relevant memories  │             │
│ │ Cost: Embedding similarity queries, │             │
│ │       index lookups                 │             │
│ │ ↓                                   │             │
│ │ Ranking: Score relevance            │             │
│ │ Cost: LLM re-ranking if enabled    │             │
│ │ ↓                                   │             │
│ │ Formatting: Insert into context    │             │
│ │ Cost: Token usage in agent context  │             │
│ └─────────────────────────────────────┘             │
│                                                     │
│ GENERATION PATH (agent uses memory):               │
│ ├─ LLM inference cost (dominant)                  │
│ └─ Quality depends on memory quality              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Evaluation Metrics

**MemoryAgentBench (MAB)**: Converts long-context tasks into incremental multi-turn streams:

```
Single-turn task:
  Input: Large context (100KB)
  Task: Answer question
  Output: Answer

Multi-turn stream (via MAB):
  Turn 1: Introduce context + question part 1
  Turn 2: New information + question part 2
  Turn 3: More context + question part 3
  ...
  Turn N: Final question

Agent must manage incremental memory.
```

**Four Memory Competencies Evaluated**:

1. **Accurate Retrieval**: Can memory system retrieve relevant facts when needed?
   - Metric: Precision/recall of retrieved facts
   
2. **Test-Time Learning**: Can agent learn new facts during task execution?
   - Metric: Accuracy on later turns vs. earlier turns
   
3. **Long-Range Understanding**: Can agent understand dependencies across many turns?
   - Metric: Accuracy on questions requiring facts from turns 1-10
   
4. **Selective Forgetting**: Can agent distinguish important vs. unimportant facts?
   - Metric: Performance when irrelevant facts accumulate

## Main Ideas & Contributions

### 1. Comprehensive Taxonomy of Memory System Designs

**Innovation**: First systematic classification of agent memory systems across four dimensions.

**Key insight**: Existing memory systems occupy different points in a design space. Understanding this space enables informed selection and hybrid designs.

**Contribution**: Practitioners can now reason about memory design tradeoffs rather than re-implementing from scratch.

### 2. Phase-Aware Cost Attribution

**Innovation**: Profiling harness that separately measures write-path, read-path, and generation-path costs.

**Key insight**: Different memory systems shift costs between phases:
- Flat retrieval: Cheap write, expensive read
- Consolidated facts: Expensive write, cheaper read
- Agentic: Very expensive write, more efficient read

**Practical value**: Enables cost analysis for specific workload patterns.

### 3. Characterization of Ten Representative Systems

The paper evaluates systems spanning the design space:

**Systems Evaluated**:
1. Flat retrieval (naive baseline)
2. Last-N retrieval (recency-only)
3. Semantic similarity retrieval
4. LLM-based summarization (compression)
5. Entity-based fact extraction
6. Hierarchical fact graphs
7. Agentic memory manager
8. Hybrid semantic + recency
9. Learned retrieval policies
10. Continuous indexing (online)

**Key Findings**:
- No single system dominates across all workload types
- Semantic similarity good for knowledge-intensive tasks; recency better for event sequences
- Agentic systems most flexible but 2-3x slower than simpler approaches
- Hybrid systems (semantic + recency) offer good accuracy-efficiency tradeoff

## Methodology & Implementation

### Experimental Setup

**Benchmark Suites**:

1. **Long-Context Benchmark**: Tasks requiring reasoning over large documents
   - Examples: Multi-step question answering, fact verification
   - Turns: 50-100 per task
   - Average task: 50K tokens of history

2. **Multi-Turn Interaction Benchmark**: Tasks requiring learning and adaptation
   - Examples: Dialogue, collaborative problem-solving
   - Turns: 20-50 per task
   - Characteristic: Information reveals incrementally

**Workload Patterns Tested**:
- Knowledge-intensive (facts matter)
- Event-sequence (temporal order matters)
- Adversarial (irrelevant facts injected)
- Long-tail (distribution skewed)

### Cost Profiling Methodology

**Phase 1: Write-Path Analysis**
```
For each turn added to memory:
  - Measure LLM tokens (extraction/summarization)
  - Measure embedding calls (indexing)
  - Measure storage writes
  - Attribute cost to memory system
```

**Phase 2: Read-Path Analysis**
```
For each query to memory:
  - Measure retrieval latency
  - Count retrieved facts/turns
  - Measure re-ranking cost (if applicable)
```

**Phase 3: Generation-Path Analysis**
```
For each turn of agent reasoning:
  - Measure tokens in context window
  - Measure LLM inference cost
  - Measure quality (task accuracy)
  - Attribute to memory quality
```

### Evaluation Metrics

| Metric | Definition | Impact |
|--------|-----------|--------|
| Write Cost (tokens) | LLM tokens for extraction per turn | Scales with task length |
| Read Cost (ms) | Retrieval latency per query | Affects interactive latency |
| Retrieval Precision | % retrieved facts relevant to query | Affects noise in context |
| Retrieval Recall | % of relevant facts retrieved | Affects completeness |
| Test-Time Learning | Δ accuracy from turn 1 to turn N | Measures learning ability |
| Long-Range Accuracy | Accuracy on questions about turn 1-5 | Measures retention |
| Forgetting Rate | % performance drop when irrelevant facts accumulate | Measures robustness |

### Results Summary

**Average Costs (per 1000 turns)**:

| System | Write Cost (tokens) | Read Cost (ms) | Generation Cost | Total |
|--------|-------|--------|---------|--------|
| Flat Retrieval | 0 | 50 | 10K | 10K |
| Last-N | 0 | 5 | 5K | 5K |
| Semantic Similarity | 500 | 20 | 8K | 8.5K |
| LLM Summarization | 5K | 15 | 7K | 12K |
| Entity Extraction | 3K | 10 | 6.5K | 9.5K |
| Agentic Memory | 8K | 30 | 4K | 12K |

**Accuracy Results on MemoryAgentBench**:

| System | Knowledge-Intensive | Event Sequence | Long-Range | Forgetting |
|--------|--------|---------|---------|-----------|
| Flat | 92% | 85% | 80% | 75% |
| Last-N | 60% | 95% | 40% | 92% |
| Semantic | 94% | 88% | 85% | 78% |
| Entity | 91% | 90% | 88% | 81% |
| Agentic | 96% | 92% | 92% | 88% |

**Key Insight**: Agentic systems achieve best accuracy but highest cost; semantic+entity hybrids offer good tradeoff.

### Agent Memory in Multi-Agent Systems

```
Multi-Agent Orchestration with Shared Memory:

  ┌────────────────────────────────────┐
  │ Shared Memory Repository            │
  │ (persistent across agents)          │
  ├────────────────────────────────────┤
  │                                    │
  │  Facts: {f₁, f₂, f₃, ...}         │
  │  History: Turn logs across all     │
  │           agent interactions       │
  │  State: Shared beliefs/plans       │
  │                                    │
  └────────────────────────────────────┘
        ▲                    ▲
        │                    │
        │  Read/Write        │  Read/Write
        │                    │
  ┌─────┴────────┐     ┌─────┴────────┐
  │ Agent 1      │     │ Agent 2      │
  │ (Planner)    │     │ (Executor)   │
  └──────────────┘     └──────────────┘
        ▲                    ▲
        └────────┬───────────┘
                 │
           Coordination
           Protocol
```

## Practical Applications & Use Cases

### 1. Long-Horizon Software Development Agents

**Use case**: Agents implementing features across multiple files and turns; must maintain understanding of codebase state.

**Workflow**:
1. Agent analyzes codebase (write: store facts about structure, functions, state)
2. Agent implements feature part 1 (read: retrieve relevant code sections)
3. Agent tests, observes failures (write: record failure modes)
4. Agent implements part 2, using prior learnings (read: retrieve patterns from earlier turns)
5. After 50 turns, memory system must efficiently serve both old and new information

**Recommendation**: Hybrid semantic+entity system. Costs ~10% extra tokens but +15% accuracy on code understanding.

### 2. Multi-Agent Collaboration with Shared Memory

**Use case**: Multiple agents working on same task; must share learnings and coordinate.

**Memory Architecture**:
```
Shared Fact Repository
├─ Code facts (functions, types)
├─ Test facts (passing/failing tests)
├─ Design facts (architecture decisions)
└─ Execution history (turns, attempts)

Agent A: Reads code facts, writes test failures
Agent B: Reads test facts, writes fixes
Agent C: Reads design facts, coordinates

All agents benefit from accumulated facts.
```

**Cost Considerations**:
- Write operations: Separate indexing per agent (avoid conflicts)
- Read operations: Cached/memoized for repeated queries
- Freshness: Eventually consistent (stale reads acceptable)

**Expected cost**: ~5-8K tokens per turn in shared system vs. 10K+ if each agent manages own memory.

### 3. Interactive Agent Systems with Users

**Use case**: Agent systems that interact with users over extended sessions (debugging, tutoring, collaborative coding).

**Memory Competencies Needed**:
1. **Accurate Retrieval**: Remember user preferences, context
2. **Test-Time Learning**: Adapt to user's style as interaction progresses
3. **Long-Range Understanding**: Connect current problem to earlier discussions
4. **Selective Forgetting**: Ignore outdated preferences when user changes mind

**System Recommendation**: 
- Semantic similarity for user context (what they care about)
- Recency for preferences (most recent overrides older)
- Entity tracking for entities mentioned (persons, projects, etc.)

### 4. Cost-Constrained Deployments

**Use case**: Deploying agents at scale (thousands of concurrent agents); memory costs are major factor.

**Analysis**:
- 1000 agents × 50 turns/agent × 5K tokens per turn = 250M tokens
- @ $0.01 per 1M tokens = $2.50 per 1000 agents × 50 turns
- Budget for memory system: <1K tokens per turn average

**Recommendation**: 
- Use Last-N retrieval for events; loses some context but 2x cheaper
- Or use consolidated facts with aggressive de-duplication
- Batch processing to amortize costs

## Insights & Implications

### For Agent System Architecture

1. **Memory is Critical Infrastructure**: Agent performance is bounded by memory system quality. Investing in memory design pays dividends.

2. **No One-Size-Fits-All**: Different workload patterns benefit from different memory architectures. Practitioners should profile their specific workloads.

3. **Write-Read Asymmetry**: Most systems are optimized for either write or read efficiency, not both. Hybrid approaches can balance tradeoffs.

### For Multi-Agent Orchestration

1. **Shared Memory as Coordination Mechanism**: Shared fact repositories enable efficient coordination; agents don't need real-time communication if facts are current.

2. **Memory Freshness Tradeoff**: Complete consistency has high cost; relaxed consistency (eventual consistency, stale reads) much more efficient.

3. **Federated Memory**: In large deployments, multiple memory subsystems (local + shared, hot + cold) often outperform single centralized system.

### For Long-Horizon Task Automation

1. **Selectivity Matters**: Agents that selectively remember (distinguish important vs. unimportant) outperform those that remember everything or nothing.

2. **Structure Beats Volume**: Structured facts (entities, relationships) more useful than unstructured history. Invest in extraction quality.

3. **Amortization Wins**: Batch processing of memories, periodic consolidation, lazy evaluation all reduce per-turn costs.

### Limitations and Open Questions

1. **Workload Diversity**: Characterization covers common patterns but not all workload types. Domain-specific patterns may differ significantly.

2. **Scalability Limits**: Characterization on tasks up to 100 turns. Very long-horizon tasks (1000+ turns) may show different tradeoffs.

3. **Dynamic Workloads**: Current evaluation assumes static task distribution. Real deployments have dynamic workloads that shift memory requirements.

4. **Learning Optimal Policy**: How to automatically choose memory architecture for a given workload? Requires further research.

## Code & Resources

### Official Repository

- **GitHub**: Check arXiv paper for official release
- **Paper PDF**: https://arxiv.org/pdf/2606.06448
- **Evaluation Harness**: MemoryAgentBench available for open-source use

### Dependencies and Requirements

- **LLM**: Any model supporting embeddings and generation (GPT-4, Claude 3+, Llama, etc.)
- **Embedding Model**: OpenAI embeddings, Sentence Transformers, or similar
- **Vector Database**: Pinecone, Weaviate, Qdrant, or FAISS
- **Storage**: PostgreSQL, MongoDB, or cloud storage for fact storage
- **Python**: 3.10+
- **Compute**: For profiling harness; GPU optional

### Quick-Start Integration Guide

```python
from agent_memory import MemorySystem, MemoryBenchmark, MemoryTaxonomy

# Step 1: Choose memory architecture from taxonomy
memory_type = MemoryTaxonomy.SEMANTIC_SIMILARITY  # or entity, hybrid, etc.

# Step 2: Instantiate memory system
memory = MemorySystem(
    architecture=memory_type,
    retrieval_strategy="semantic",
    cache_size=10000,
    freshness_policy="eventual_consistent"
)

# Step 3: Run agent with memory profiling
from agent_memory.profiling import ProfilingHarness

profiler = ProfilingHarness(memory)

# Agent loop
for turn in range(num_turns):
    # Write path: Add new information
    profiler.profile_write(new_observation)
    memory.add(new_observation)
    
    # Read path: Retrieve relevant memory
    retrieved = profiler.profile_read(query)
    memory_context = memory.retrieve(query)
    
    # Generation: Agent uses memory
    response = agent.generate(context=memory_context)
    
    # Profile generation cost
    profiler.profile_generation(response, memory_context)

# Analysis
costs = profiler.get_phase_costs()
print(f"Write cost: {costs.write} tokens")
print(f"Read cost: {costs.read} ms")
print(f"Generation cost: {costs.generation} tokens")
```

### Benchmark Evaluation

```python
# Run on MemoryAgentBench
benchmark = MemoryBenchmark()

results = benchmark.evaluate(
    memory_system=memory,
    workload_type="knowledge_intensive",
    num_turns=50
)

print(f"Accurate Retrieval: {results.precision:.2%}")
print(f"Test-Time Learning: +{results.learning_gain:.2%}")
print(f"Long-Range Accuracy: {results.long_range:.2%}")
print(f"Forgetting Robustness: {results.forgetting_resilience:.2%}")
```

## Related Work & Context

### Foundational Work on Agent State Management

- **ReACT Agents** (Yao et al., 2022): Foundation for reasoning agents; this work addresses memory for long-horizon version
- **Retrieval-Augmented Generation** (Lewis et al., 2020): Foundation for retrieval-based memory
- **Transformer Context Windows** (research on extending): Complements explicit memory systems

### Related Work on Agent Memory

- **Memory in the Loop** (2607.05690): In-process retrieval as extended working memory
- **Anatomy of Agentic Memory** (2602.19320): Taxonomy and evaluation of memory limitations
- **Eywa** (2605.30771): Provenance-grounded long-term memory for agents

### Related Work on System Design for LLMs

- **LLM Inference Optimization** (various papers): Similar cost analysis for inference systems
- **Vector Database Systems** (Pinecone, Weaviate papers): Infrastructure for memory retrieval
- **Caching and Prefetching** (systems literature): Similar optimization problems

### Future Extensions

- **Adaptive Memory Selection**: Automatically choose memory architecture based on workload
- **Learned Retrieval Policies**: Use RL to optimize which facts to retrieve
- **Distributed Memory Systems**: Memory across multiple machines/agents
- **Memory Consistency Protocols**: Formal guarantees for multi-agent memory systems
- **Knowledge Graph Integration**: Structured reasoning over memory facts

## Tags & Keywords

`agent-memory`, `long-horizon-tasks`, `system-characterization`, `memory-architecture`, `state-management`, `retrieval-augmented`, `multi-agent-coordination`, `cost-analysis`, `workload-patterns`, `memory-efficiency`

---

**Citation:**
```
Omri, Y., Gan, Z., Broveak, Z., Geens, R., He, Z., Pentland, A., 
Verhelst, M., Weissman, T., & Tambe, T. (2026).
Agent Memory: Characterization and System Implications of Stateful 
Long-Horizon Workloads.
arXiv preprint arXiv:2606.06448.
```
