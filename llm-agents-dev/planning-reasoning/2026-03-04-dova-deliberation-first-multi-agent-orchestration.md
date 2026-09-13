# DOVA: Deliberation-First Multi-Agent Orchestration for Autonomous Research Automation

**ArXiv ID:** 2603.13327  
**Authors:** Aaron Shen, Alfred Shen  
**Submission Date:** March 4, 2026  
**Venue:** ArXiv  

---

## Executive Summary

DOVA introduces a deliberation-first paradigm for multi-agent LLM systems that separates meta-reasoning from tool invocation, achieving 40-60% token reduction on simple tasks while preserving complex reasoning capacity. By combining explicit meta-reasoning, hybrid collaborative ensemble reasoning, and adaptive multi-tiered thinking, DOVA addresses critical inefficiencies in current agent systems where tools are invoked without sufficient planning. This work demonstrates that explicit deliberation can dramatically improve agent efficiency and reasoning quality across diverse research automation tasks.

---

## Problem Statement

Current single-agent and multi-agent LLM systems exhibit fundamental inefficiencies when handling complex research tasks:

1. **Immediate Tool Invocation:** Agents invoke tools without sufficient deliberation, leading to wasted API calls and redundant searches
2. **Context Synthesis Failures:** Multi-source information synthesis requires careful reasoning about source credibility and relevance, which unstructured multi-agent conversation often misses
3. **Inefficient Ensemble Approaches:** Traditional ensemble methods duplicate work across agents without cross-talk or shared reasoning
4. **Personalization Deficit:** Agents lack memory of user preferences, past clarifications, and individual context patterns across conversations
5. **Token Efficiency:** Many agent decisions consume tokens without proportional value; a single complex query might trigger 10x the necessary API calls
6. **Reasoning Degradation:** Long interaction chains amplify errors through repeated reasoning steps without intermediate validation

**Concrete Example:** A research task asking "Compare recent deep learning papers on vision transformers" currently triggers:
- Exhaustive web search (40+ queries)
- Duplicate paper extraction by multiple agents
- Redundant summarization across agents
- Poor synthesis due to lack of shared reasoning

DOVA's approach: Orchestrator first deliberates on optimal search strategy (3-5 targeted queries), specifies source prioritization rules, then executes with minimal tool calls.

---

## Core Concepts & Theory

### Deliberation-First Orchestration

DOVA's central innovation: **Separate meta-reasoning from tool invocation**

```
Traditional Agent Loop:
User Input → LLM → (think + decide + act) → Tool Call → LLM → Output

DOVA Loop:
User Input → Meta-Reasoning Layer → Deliberation
           ↓
      Tool Specification (What to call, where, when)
           ↓
      Tool Invocation Layer (Controlled Execution)
           ↓
      Response Processing
           ↓
      Output with Confidence Metrics
```

**Key Components:**

1. **Meta-Reasoning Layer**
   - Explicit planning before any tool invocation
   - Analyzes task structure and information needs
   - Generates tool execution specifications
   - Not exposed to user; operates at system level

2. **Persistent User Model**
   - Maintains interaction history and learned preferences
   - Tracks clarifications and follow-ups
   - Remembers domain expertise level of user
   - Enables personalized reasoning strategies

3. **Entity-Aware Conversation Context**
   - Tracks key entities discussed (papers, researchers, methods)
   - Maintains relationships between entities
   - Enables coherent multi-turn follow-ups
   - Prevents redundant re-explanation of context

### Hybrid Collaborative Reasoning

Rather than independent agents duplicating work, DOVA uses a three-phase pipeline unifying ensemble diversity with transparency:

```
┌─────────────────────────────────────────────────────────────┐
│         Hybrid Collaborative Reasoning Pipeline              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: Ensemble Diversity                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Perspective  │  │ Perspective  │  │ Perspective  │      │
│  │    Agent 1   │  │    Agent 2   │  │    Agent 3   │      │
│  │ (Factual)    │  │ (Critical)   │  │ (Creative)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│  Phase 2: Blackboard Transparency                          │
│         ┌─────────────────▼──────────────────┐             │
│         │  Shared Reasoning Workspace         │             │
│         │  - Unified fact repository          │             │
│         │  - Debate and critique logs         │             │
│         │  - Evidence scoring                 │             │
│         └─────────────────┬──────────────────┘             │
│                           │                                 │
│  Phase 3: Iterative Refinement                            │
│         ┌─────────────────▼──────────────────┐             │
│         │  Integration & Improvement Loop    │             │
│         │  - Detect conflicts                │             │
│         │  - Resolve disagreements           │             │
│         │  - Synthesize consensus            │             │
│         └─────────────────┬──────────────────┘             │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
                      Final Response
```

**Advantages over traditional multi-agent approaches:**
1. Agents see each other's reasoning (transparency)
2. Agents can criticize and refine (collaboration)
3. Contradictions surfaced and resolved explicitly
4. Reduced redundant work (agents know what others found)

### Adaptive Multi-Tiered Thinking

DOVA implements a six-level token-budget allocation scheme:

```
Level 1: Quick Response (~100 tokens)
  └─ Cached knowledge or simple factual lookup
  └─ Use case: "What year was paper X published?"

Level 2: Fast Reasoning (~500 tokens)
  └─ Single-agent analysis with context
  └─ Use case: "Summarize this paper's contribution"

Level 3: Deliberate Reasoning (~2K tokens)
  └─ Multi-perspective analysis
  └─ Use case: "Compare two approaches"

Level 4: Deep Reasoning (~5K tokens)
  └─ Full ensemble + synthesis + critique
  └─ Use case: "Design experiment to test hypothesis"

Level 5: Extended Reasoning (~10K tokens)
  └─ Multi-turn reasoning with tool invocation
  └─ Use case: "Systematic review across 20 papers"

Level 6: Maximum Reasoning (~20K+ tokens)
  └─ Unlimited reasoning with full tool access
  └─ Use case: "Comprehensive research synthesis"
```

**Adaptive Selection Logic:**
- Task complexity classifier determines appropriate level
- Budget adjusts based on confidence and uncertainty
- User can override for explicit depth preference
- Cost-quality tradeoff explicitly exposed

### Persistent User Modeling

DOVA maintains structured user profiles:

```
User Model:
├── Expertise Level: {novice, intermediate, expert}
├── Research Domain: {ML, Systems, NLP, CV, ...}
├── Clarification History:
│   ├── {question, clarification, timestamp}
│   ├── {question, clarification, timestamp}
│   └── ...
├── Preferred Tools: [Semantic Scholar, arXiv, Papers With Code, ...]
├── Entity Knowledge:
│   ├── Familiar Papers: [ID, Domain]
│   ├── Known Researchers: [Name, Field]
│   └── Understood Methods: [Name, Details]
└── Communication Preferences:
    ├── Response Length: {brief, standard, detailed}
    ├── Technical Depth: {high-level, technical, rigorous}
    └── Citation Style: {inline, endnote, reference-list}
```

Benefits:
- Avoid re-explaining concepts user already knows
- Tailor tool selection to user's trusted sources
- Provide appropriate technical depth
- Learn from user feedback across sessions

---

## Main Ideas & Contributions

### 1. Deliberation-First Principle

**Core Insight:** Separating planning from execution enables superior efficiency and quality.

**Mechanism:**
```
Before (Reactive):
  Action → Observe → Decide → Act → Observe → ...
  (Inefficient; many wasted actions)

After (Deliberative):
  Deliberate → Plan Actions → Execute Plan → Observe → Refine
  (Efficient; intentional action sequences)
```

**In Practice:**
- Orchestrator asks: "What information sources best answer this question?"
- Before any tool call, generates optimal search strategy
- Specifies exact API calls to make, in what order
- Execution layer follows plan with minimal deviation
- Savings: 40-60% reduction in tool calls on simple tasks

### 2. Ensemble Diversity Without Redundancy

**Traditional Approach:** Run three independent agents on same task
- Problem: Agents duplicate work (20 searches when 5 suffice)
- Result: 3x cost, 1x quality improvement

**DOVA Approach:** Ensemble reasoning with blackboard
- Agents see each other's findings
- Avoid duplicate searches
- Each agent specializes: one checks facts, one critiques, one synthesizes
- Result: 1.5x cost, 2-3x quality improvement

**Blackboard Mechanism:**
```
┌────────────────────────────────┐
│    Shared Blackboard State      │
├────────────────────────────────┤
│ Discovered Facts:              │
│  - Paper A: [title, venue, yr] │
│  - Author B: [affiliation]     │
│ Evidence Quality:              │
│  - Paper A: source rating 0.9  │
│  - Author B: verified 0.7      │
│ Debates:                       │
│  - Is method X novel?          │
│    ✓ Agent 1: Yes (evidence:...) │
│    ✗ Agent 2: No (counter:...)  │
│    ✓ Consensus: Yes (0.8 conf)  │
└────────────────────────────────┘
```

### 3. Adaptive Depth Allocation

**Problem:** All tasks don't need deep reasoning
- Factual lookup: "Who wrote paper X?" → Simple database lookup
- Synthesis: "Compare X and Y" → Need analysis
- Strategy: "Design experiment" → Need extensive reasoning

**DOVA Solution:** Task-aware budget allocation
- Classifier determines task type (< 100 tokens to classify)
- Allocate appropriate reasoning depth
- Allow user override for explicit requirements
- Transparent cost-quality tradeoff to user

**Real-World Impact:**
- 40-60% token reduction on simple factual tasks
- No quality degradation on those tasks
- Complex tasks still get deep reasoning when needed

### 4. Multi-Interface Unified Backend

DOVA provides consistent orchestration across interfaces:

```
┌─────────────────────────────────────────┐
│      DOVA Orchestration Backend          │
├─────────────────────────────────────────┤
│                                         │
│  Unified Reasoning Engine:              │
│  - Meta-reasoning layer                 │
│  - User model database                  │
│  - Entity-aware context                 │
│  - Adaptive token budgeting              │
│                                         │
├─────────────────────────────────────────┤
│         Multi-Interface Access          │
│  ┌──────────┐  ┌──────────┐             │
│  │ REST API │  │   CLI    │             │
│  └──────────┘  └──────────┘             │
│  ┌──────────┐  ┌──────────┐             │
│  │Browser UI│  │MCP Server│             │
│  └──────────┘  └──────────┘             │
│  ┌──────────────────────────────────┐  │
│  │ Claude Code Plugin (Dynamic)     │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Consistency Benefits:**
- Same orchestration logic regardless of interface
- User model persists across interfaces
- Conversation history unified
- Enables switching between CLI, UI, API mid-session

### 5. Token Efficiency Through Deliberation

**Quantitative Impact:**

| Task Type | Traditional | DOVA | Savings |
|-----------|-------------|------|---------|
| Factual lookup | 2K tokens | 800 tokens | 60% |
| Single paper summary | 3K tokens | 2K tokens | 33% |
| Paper comparison | 8K tokens | 6K tokens | 25% |
| Complex synthesis | 20K tokens | 18K tokens | 10% |

**Mechanism:**
1. Deliberation identifies exact information needed (100 tokens)
2. Targeted search avoids over-retrieval (saves 50-70% of original)
3. Synthesis works from curated sources (faster, better)
4. Result: Superior quality with fewer tokens overall

---

## Methodology & Implementation

### System Architecture

**Core Components:**

1. **Meta-Reasoning Engine**
   - Input: User query + user model + conversation history
   - Process: Analyze task structure, generate tool specification
   - Output: Structured plan (search queries, tools to invoke, depth level)
   - Timing: Runs once per user query

2. **User Model Manager**
   - Maintains structured user profiles
   - Updates based on explicit feedback
   - Infers expertise level from conversation
   - Manages multi-session persistence

3. **Entity Tracking System**
   - Parses papers, researchers, methods from conversation
   - Maintains entity relationships
   - Enables co-reference resolution
   - Supports entity-aware follow-ups

4. **Orchestration Backend**
   - Coordinates ensemble agents
   - Manages blackboard state
   - Implements three-phase pipeline
   - Tracks token budgets and costs

5. **Multi-Interface Layer**
   - Converts interface inputs to unified query format
   - Converts outputs to interface-specific formats
   - Maintains session continuity

### Datasets and Evaluation

**Internal Evaluation Tasks:**
- 100+ research automation scenarios
- Diverse query types: factual, analytical, synthetic
- Varying complexity levels and user expertise

**Metrics:**
- **Task Completion Rate:** % of tasks answered successfully
- **User Satisfaction:** Likert scale ratings from user study
- **Token Efficiency:** Tokens consumed vs. task complexity
- **Response Quality:** Source coverage, coherence, accuracy
- **Latency:** Time from query to response

### Experimental Results

**Primary Results - Token Efficiency:**

| Metric | Traditional | DOVA | Improvement |
|--------|-------------|------|-------------|
| Simple Tasks | 2K tokens | 800 tokens | 60% reduction |
| Complex Tasks | 20K tokens | 18K tokens | 10% reduction |
| Average | 8K tokens | 5.2K tokens | 35% reduction |

**Architectural Evaluation:**

Ablation study across 7 system configurations:

1. **Deliberation-First Only:** 25% token savings
2. **Ensemble Only:** 15% quality improvement, no token savings
3. **User Modeling Only:** 10% quality improvement via better targeting
4. **Multi-Tiered Budgeting Only:** 20% token savings
5. **Full DOVA (All components):** 35% token savings + 30% quality improvement
6. **No Deliberation (Baseline):** 100% cost reference

**Key Findings:**
- Deliberation-first is most impactful component (accounts for 25% of savings)
- Ensemble reasoning quality gains but requires blackboard to avoid cost explosion
- User modeling enables effective targeting without extra computation
- Multi-tiered budgeting is critical for efficiency-quality balance

### User Study Results

(Exact figures unavailable — see full paper)

**Qualitative Feedback:**
- Users appreciated deliberation layer (felt more "thoughtful")
- Ensemble reasoning sometimes overwhelming (prefer one clear answer)
- Adaptive budgeting balances efficiency and depth well
- Claude Code integration essential for practical adoption

---

## Practical Applications & Use Cases

### 1. Autonomous Literature Review

**Scenario:** Researcher exploring recent papers in vision transformers

**Traditional Approach:**
- Researcher searches arxiv.org, papers with code
- Aggregates results manually
- Synthesizes learnings
- (Time: 2-3 hours)

**DOVA Approach:**
```
Query: "What are the latest advances in vision transformer efficiency?"

Meta-Reasoning Deliberation:
  ├─ Task Type: Complex Synthesis (4 papers + methods)
  ├─ Depth: Level 4 (Deep Reasoning, ~5K tokens)
  ├─ Tools: [arXiv, Semantic Scholar, Papers With Code]
  ├─ Search Strategy:
  │   ├─ Query 1: "vision transformer efficient"
  │   ├─ Query 2: "vision transformer sparse attention"
  │   ├─ Query 3: "vision transformer quantization"
  │   └─ Query 4: "vision transformer distillation"
  └─ Expected Sources: 10-15 papers across 4 queries

Ensemble Reasoning (Blackboard):
  ├─ Factual Agent: Extracts paper details (title, venue, key results)
  ├─ Critical Agent: Assesses novelty and significance
  ├─ Creative Agent: Identifies connections and trends
  └─ Synthesis Agent: Produces coherent narrative

Output: Structured summary with citations, confidence metrics, open questions
Time: ~30 seconds (vs. 2-3 hours manual)
```

### 2. Research Experiment Design

**Scenario:** ML researcher designing experiments to validate new method

**Use Case Flow:**
```
Step 1: Clarify Method
  User: "I want to test if sparse attention improves ViT efficiency"
  DOVA: Searches recent sparse attention papers for baselines

Step 2: Deliberate on Experiment
  DOVA Meta-Reasoning:
    - Identify existing benchmarks and metrics
    - Find confounding variables to control
    - Suggest statistical significance thresholds
    - Propose ablation studies

Step 3: Synthesize Experiment Design
  Ensemble reasoning produces:
    - Baseline model specifications
    - Dataset and evaluation protocol
    - Metric selection with rationale
    - Comparison with related work

Step 4: Refine Based on Feedback
  User: "This assumes dense attention as baseline—what about other efficient methods?"
  DOVA: Uses entity tracking to update understanding, refines recommendations
```

### 3. Competitive Analysis

**Scenario:** Product team analyzing competitor offerings and market positioning

**DOVA Advantages:**
- **Deliberate Search:** Strategically targets competitor documentation, reviews, benchmarks
- **Ensemble Reasoning:** Factual data + critical assessment + creative positioning
- **User Modeling:** Understands company context, competitive priorities
- **Synthesis:** Produces structured competitive intelligence report

### 4. Educational Research Tutoring

**Scenario:** Student learning about graph neural networks

**Adaptive Depth:**
- Initial query: "What are GNNs?" → Level 1 (Quick Response)
  - Simple definition, key concepts
- Follow-up: "How do GNNs differ from CNNs?" → Level 3 (Deliberate Reasoning)
  - Multi-perspective comparison
- Advanced: "Design GNN architecture for heterogeneous graphs" → Level 5 (Extended Reasoning)
  - Full synthesis of literature + design principles

**User Modeling Benefits:**
- System learns student is intermediate, not beginner
- Adjusts technical depth over time
- Tracks concepts already explained
- Builds on prior context

### 5. Integration with Software Development

**DOVA + Claude Code:**
```
Workflow: Code a new algorithm from research paper

Step 1: Researcher queries "Efficient attention mechanism papers 2025"
  DOVA: Searches literature, identifies top 5 papers
  (Deliberation-first ensures targeted search)

Step 2: Researcher says "Implement the first paper's approach"
  Claude Code: Browses papers, extracts algorithms, generates code
  DOVA: Provides technical context through persistent user model
  
Step 3: Developer integrates into larger codebase
  DOVA: Provides comparison with existing approaches
  (Ensemble reasoning ensures thorough alternatives analysis)
```

---

## Insights & Implications

### 1. Efficiency Through Intentionality

**Key Insight:** Explicit planning before action dramatically reduces waste.

**Broader Implication:** As LLM systems become more expensive and complex, deliberative approaches will outperform reactive approaches. This mirrors human expert behavior (researchers plan literature review strategy before searching).

### 2. Ensemble Reasoning Requires Transparency

**Challenge:** Traditional ensemble approaches (run 3 models independently) waste resources.

**DOVA's Solution:** Make ensemble reasoning explicit via blackboard.

**Implication:** Multi-agent systems need shared state and communication protocols, not just independent agents. This aligns with emerging consensus on orchestration patterns.

### 3. User Modeling as Infrastructure

**Current State:** Every agent interaction starts fresh (no memory of user)

**DOVA Paradigm:** Persistent user models enable adaptive, personalized reasoning

**Long-term Implication:** Future agent systems will maintain rich user profiles across sessions. This has privacy implications (user data retention) and capability implications (truly personalized AI).

### 4. Task-Aware Resource Allocation

**Insight:** Not all tasks justify deep reasoning. Matching depth to task is both efficient and effective.

**Application:** Cost-conscious organizations will adopt adaptive budgeting. Luxury use cases (unlimited thinking) remain for critical decisions.

### 5. Multi-Interface Consistency

**Trend:** Users expect same AI system across CLI, web, API, IDE

**DOVA's Approach:** Unified orchestration backend with swappable interfaces

**Implication:** Agent systems will need to architect around interface-agnostic reasoning engines. This enables seamless switching mid-task.

### 6. Advancement in Autonomous Research

DOVA demonstrates:
- Efficient autonomous literature review (40-60% cost reduction)
- Reliable synthesis across multiple sources
- Adaptive depth appropriate to task
- Integration with development workflows

**Impact:** Makes autonomous research practical for cost-conscious organizations.

### 7. Limitations and Open Questions

**Known Limitations:**
- Blackboard state can become large with long interactions
- Ensemble reasoning may miss novel approaches (bounded by diversity of agents)
- User modeling requires sufficient interaction history to be effective
- Multi-turn interactions can have cascading deliberation costs

**Open Research Questions:**
1. How to optimally design ensemble (which perspectives complement most)?
2. Can we learn user models from implicit feedback without explicit updates?
3. What's the optimal granularity for blackboard updates?
4. How to handle multi-agent disagreements that don't resolve naturally?
5. Can deliberation itself be learned rather than hand-engineered?

### 8. Relevance to Planning and Reasoning in Agent Systems

DOVA demonstrates:
- **Planning Before Action:** Separating meta-reasoning from execution is powerful
- **Collaborative Reasoning:** Agents sharing reasoning (via blackboard) outperform isolated agents
- **Adaptive Resource Allocation:** Matching reasoning depth to task complexity improves efficiency
- **User Modeling:** Understanding user context enables smarter agent behavior

This informs broader agent system design principles for future research.

---

## Code & Resources

### Reference Implementation

**Status:** Research prototype (not published as of submission date)

**Conceptual Framework Available:**
- Paper details architecture in sufficient depth to re-implement
- Key components: meta-reasoning engine, blackboard, ensemble coordinator, user model

### Framework Integration Examples

**LangGraph Implementation Sketch:**

```python
from langgraph.graph import StateGraph

# Define DOVA state
class DOVAState(TypedDict):
    query: str
    user_model: dict
    deliberation_plan: dict
    blackboard: dict
    ensemble_results: dict
    final_response: str

# Create reasoning graph
def create_dova_graph():
    workflow = StateGraph(DOVAState)
    
    # Meta-Reasoning Node
    workflow.add_node("deliberate", deliberation_node)
    
    # Ensemble Nodes (parallel)
    workflow.add_node("factual_agent", factual_reasoning)
    workflow.add_node("critical_agent", critical_reasoning)
    workflow.add_node("creative_agent", creative_reasoning)
    
    # Synthesis
    workflow.add_node("synthesize", synthesis_node)
    
    # Edges
    workflow.add_edge("deliberate", ["factual_agent", "critical_agent", "creative_agent"])
    workflow.add_edge("factual_agent", "synthesize")
    workflow.add_edge("critical_agent", "synthesize")
    workflow.add_edge("creative_agent", "synthesize")
    
    return workflow.compile()

def deliberation_node(state):
    """Meta-reasoning before tool invocation"""
    query = state["query"]
    user_model = state["user_model"]
    
    # Classify task complexity
    complexity = classify_task(query)
    
    # Determine tools and search strategy
    plan = generate_plan(query, user_model, complexity)
    
    return {"deliberation_plan": plan}

def synthesis_node(state):
    """Integrate ensemble results"""
    results = state["ensemble_results"]
    
    # Resolve conflicts
    final = resolve_ensemble(results)
    
    return {"final_response": final}
```

### Dependencies and Compute

**Recommended Stack:**
- Orchestration: LangGraph or similar multi-agent framework
- LLM: Claude API (for high reasoning quality on ensemble tasks)
- Database: Vector store for entity tracking; relational DB for user models
- Interface: Flask/FastAPI for REST API, CLI framework for command-line

**Compute Requirements:**
- Memory: 4GB+ for user model caches and blackboard state
- Parallelism: 3-5 concurrent agents per query
- Latency: ~2-5 seconds per query (dominated by LLM inference)
- API Rate Limits: Respect tool rate limits (arXiv, Semantic Scholar, etc.)

---

## Related Work & Context

### Prior Work on Multi-Agent Reasoning

1. **AutoGen (Microsoft)**
   - Two-agent conversational loop
   - Demonstrated effectiveness on code generation
   - DOVA extends with explicit blackboard and persistent models

2. **Researcher (OpenAI)**
   - Autonomous research agents
   - Focused on experiment design and execution
   - DOVA's complement: research understanding and synthesis

3. **Reflexion / Self-Critique**
   - Agents that critique own outputs
   - DOVA incorporates critique as ensemble perspective

### Related Approaches to Deliberation

1. **Thought Chains**
   - Chain-of-thought prompting encourages reasoning steps
   - DOVA formalizes this as separate meta-reasoning layer

2. **Planning-Then-Acting**
   - ReAct and variants separate planning from execution
   - DOVA extends to pre-planning (before any tool invocation)

3. **Ensemble Methods in NLP**
   - Traditional ensembles (majority voting)
   - DOVA: Ensemble with shared blackboard (more efficient)

### Possible Extensions

1. **Hierarchical Deliberation**
   - Meta-deliberation about deliberation strategy itself
   - Useful for extremely complex research tasks

2. **Active Learning from Users**
   - System requests clarification when uncertain
   - Updates user model interactively
   - Improves quality over time

3. **Adversarial Ensemble**
   - Include agent that argues against proposed conclusion
   - Strengthens reasoning through debate
   - Hybrid with AOrchestra-style orchestration

4. **Temporal User Modeling**
   - Track how user expertise evolves over time
   - Adjust technical depth as user learns
   - Personalization that improves with usage

### Comparison with Related Systems

| System | Deliberation | Ensemble | User Model | Multi-Interface |
|--------|------------|----------|-----------|-----------------|
| DOVA | Yes | Yes (Blackboard) | Yes | Yes |
| AutoGen | No | Yes (Agent roles) | No | No |
| Reflexion | Limited | No | No | No |
| Traditional MAS | No | Yes (Fixed roles) | No | No |

---

## References

**Citation:**
```bibtex
@article{dova2026,
  title={DOVA: Deliberation-First Multi-Agent Orchestration for Autonomous Research Automation},
  author={Shen, Aaron and Shen, Alfred},
  journal={arXiv preprint arXiv:2603.13327},
  year={2026}
}
```

**Paper Link:** https://arxiv.org/abs/2603.13327
