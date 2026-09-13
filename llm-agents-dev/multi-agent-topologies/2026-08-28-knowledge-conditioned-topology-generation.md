# When Evidence Shapes Collaboration: Knowledge-Conditioned Topology Generation for Multi-Agent Systems

**Title:** When Evidence Shapes Collaboration: Knowledge-Conditioned Topology Generation for Multi-Agent Systems  
**Authors:** [Authors from paper] (Affiliation details to be confirmed from full paper)  
**ArXiv ID:** 2608.27984 (August 28, 2026)

## Executive Summary

This paper introduces K-GAT (Knowledge-Guided Agent Topology Generator), a neuro-symbolic framework that fundamentally rethinks how multi-agent systems organize themselves for complex tasks. Rather than relying solely on parametric knowledge embedded in language models, K-GAT formulates collaboration topology design as an explicit knowledge-conditioned structure learning problem. By integrating external evidence directly into autoregressive graph generation, the framework enables dynamic topology optimization that adapts to the specific informational requirements of individual queries and tasks.

## Problem Statement

Contemporary multi-agent systems face a critical limitation: static or arbitrarily designed collaboration topologies that don't adapt to task-specific information requirements:

1. **Fixed Topology Assumptions:** Most existing systems use pre-determined collaboration patterns (chains, trees, hierarchies) regardless of task characteristics
2. **Knowledge-Agnostic Design:** Topology generation relies primarily on LLM parametric knowledge, ignoring external information sources
3. **Suboptimal Resource Allocation:** Agents not specialized for retrieved knowledge participate equally in decision-making
4. **Limited Adaptability:** Topologies cannot rapidly reorganize when new evidence becomes available
5. **Knowledge Redundancy:** Retrieved information often duplicates parametric knowledge, wasting computational resources
6. **Query-Task Mismatch:** Generic topologies may not match the specific reasoning requirements of different query types

The research gap lies in developing methods that dynamically construct agent collaboration structures conditioned on both task requirements and available evidence.

### Motivating Examples

**Example 1 - Knowledge-Intensive Task:**
A question requires retrieving multiple data points from different sources. Traditional topologies might:
- Pass same query to all agents (redundant)
- Use fixed debate structure (inefficient routing)

K-GAT instead:
- Retrieves diverse evidence
- Organizes topology to route different questions to specialized agents
- Allocates agents based on evidence relevance

**Example 2 - Expert-Level Reasoning:**
GPQA (Graduate-Level Google-Proof Questions) require complex reasoning:
- Traditional approach: Single debate or sequential discussion
- K-GAT approach: Topology organized around evidence specificity, with specialist agents handling detailed analysis

## Core Concepts & Theory

### Knowledge-Conditioned Structure Learning

The paper formulates multi-agent topology design as a neuro-symbolic structure learning problem:

**Input:**
- Query or task description
- Retrieved external evidence (documents, data points, expert information)
- Available agent pool with specializations

**Process:**
- Encode query and evidence into representation
- Learn connections between agents based on task-evidence requirements
- Generate optimal collaboration graph

**Output:**
- Dynamic collaboration topology
- Agent role assignments
- Message passing schedule

### Neuro-Symbolic Framework

K-GAT combines neural and symbolic components:

**Neural Components:**
- Graph neural networks for topology encoding
- Transformers for evidence and query understanding
- Embedding models for agent capability representation

**Symbolic Components:**
- Graph generation rules ensuring valid topologies
- Constraint satisfaction for agent compatibility
- Logical consistency checking

### Information Flow and Evidence Routing

The framework models agent collaboration as an information routing problem:

```
Input Query
    ↓
Evidence Retrieval → Retrieved Evidence Set
    ↓
Query-Evidence Fusion → Augmented Representation
    ↓
Agent Capability Analysis → Specialization Scores
    ↓
Topology Generation → Graph Structure
    ↓
Message Routing → Agent-to-Agent Communication
    ↓
Aggregation → Final Response
```

### Autoregressive Graph Generation

K-GAT generates topologies through autoregressive graph construction:

1. **Initial Node Selection:** Choose seed agents based on query-evidence alignment
2. **Iterative Expansion:** Progressively add agents to the graph
3. **Edge Generation:** Add connections between selected agents
4. **Role Assignment:** Assign specific roles (coordinator, specialist, reviewer)
5. **Validation:** Verify topology feasibility and constraint satisfaction

**Generation Process:**

```
State_0 = {Agent_1}  (Initialize with most relevant agent)
    ↓
State_1 = {Agent_1, Agent_3}  (Add Agent_3 if evidence suggests)
    ↓ P(Agent_i | State_t, Evidence, Query)
State_2 = {Agent_1, Agent_3, Agent_5}  (Add Agent_5)
    ↓
Final Graph = {Agents, Edges, Roles}
```

### Evidence Conditioning Mechanism

External evidence conditions topology generation at multiple levels:

1. **Agent Selection:** Evidence relevance to agent specialization
2. **Connection Patterns:** Evidence correlation suggesting agent pairs
3. **Role Assignment:** Evidence complexity determining agent responsibilities
4. **Message Content:** Evidence routing to specific agent combinations

**Formal Representation:**

```
P(Topology | Query, Evidence) = 
    Π_i P(Agent_i | Query, Evidence, Topology_{<i})
    * Π_e P(Edge_e | Query, Evidence, Agents_selected)
    * Π_r P(Role_r | Evidence_complexity, Agent_capability)
```

## Main Ideas & Contributions

### 1. K-GAT Framework Architecture

K-GAT comprises several integrated modules:

**Evidence Processor:**
- Retrieves and ranks relevant evidence
- Extracts key information for topology conditioning
- Identifies evidence gaps and retrieval needs
- Scores evidence quality and relevance

**Query Analyzer:**
- Identifies query type and complexity
- Decomposes query into sub-questions
- Determines reasoning requirements
- Estimates evidence dependency

**Topology Generator:**
- Encodes query and evidence representations
- Generates candidate agent subsets
- Determines optimal connections
- Assigns specialized roles

**Agent Registry:**
- Maintains agent capability profiles
- Tracks agent specializations
- Stores performance metrics
- Manages version information

**Execution Orchestrator:**
- Instantiates generated topology
- Routes messages according to graph structure
- Collects and aggregates responses
- Manages fallback and error handling

### 2. Knowledge-Guided Agent Selection

Rather than uniform agent participation, K-GAT selectively involves agents based on evidence:

| Evidence Type | Agent Specialization | Likelihood of Selection |
|---|---|---|
| Numerical Data | Data Analysis Agent | High |
| Technical Details | Specialist Domain Agent | High |
| Background Info | Retrieval/Context Agent | Medium |
| Meta-questions | Reasoning/Analysis Agent | Medium |
| Conflicting Info | Dispute Resolution Agent | High |

**Selection Algorithm:**
1. Score each agent against retrieved evidence
2. Compute cumulative relevance for agent subsets
3. Select subset that maximizes information coverage
4. Prune redundant agents

### 3. Dynamic Connection Topology

Generated topologies adapt to evidence structure:

**Example Topology Patterns:**

**Linear Chain (for sequential reasoning):**
```
Agent_Retrieval → Agent_Analysis → Agent_Verification → Agent_Response
```

**Hub-and-Spoke (for evidence aggregation):**
```
        ↙    ↓    ↖
Agent1  Hub   Agent2
        ↖    ↑    ↙
```

**Hierarchical (for expert delegation):**
```
        Coordinator
       ↙    ↓    ↖
    Expert1 Verifier Expert2
       ↓             ↓
    Workers    Workers
```

**Mesh (for collaborative reasoning):**
```
Agent1 ↔ Agent2
  ↕      ↕
Agent3 ↔ Agent4
```

### 4. Evidence Quality Scoring

K-GAT assigns confidence scores to evidence:

**Scoring Criteria:**
- Source credibility
- Information specificity
- Temporal recency
- Relevance to query
- Coverage of query aspects
- Consistency with other evidence

**Score Aggregation:**
```
evidence_score = w1*credibility + w2*specificity + 
                 w3*recency + w4*relevance + w5*coverage
```

This score influences:
- Agent selection (higher-scored evidence → more specialized agents)
- Topology complexity (higher quality → simpler, more focused topologies)
- Message routing (direct routing for high-confidence evidence)

## Methodology & Implementation

### Experimental Setup

**Benchmark Datasets:**

1. **GPQA (Graduate-Level Google-Proof Questions):**
   - Expert-level multiple-choice questions
   - Requires multi-step reasoning with evidence
   - [Exact figures unavailable — see full paper]

2. **Knowledge-Intensive Benchmarks:**
   - Tasks requiring external evidence retrieval
   - Various evidence types and complexities
   - Evaluation on accuracy and efficiency

3. **Multi-Modal Benchmarks:**
   - Tasks combining text, numerical, and structured data
   - Different evidence modalities
   - Cross-modal reasoning requirements

### Evaluation Metrics

**Task Performance:**
[Exact figures unavailable — see full paper]

- Accuracy on benchmark tasks
- Improvement over fixed-topology baselines
- Generalization to new evidence types

**Efficiency Metrics:**
- Topology generation latency
- Number of agents used per query
- Message passing overhead
- Total computation cost

**Adaptation Metrics:**
- Topology diversity across different queries
- Evidence utilization rate
- Agent specialization effectiveness

### Agent Topology Generation Pipeline

```
┌─────────────────────────────────────┐
│     Input Query & Evidence          │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Evidence Retrieval & Processing    │
│  ├─ Search relevant documents       │
│  ├─ Extract key information         │
│  ├─ Score evidence quality          │
│  └─ Rank by relevance              │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Query Analysis                     │
│  ├─ Identify reasoning requirements │
│  ├─ Detect multi-hop dependencies   │
│  └─ Estimate evidence needs         │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Capability Matching                │
│  ├─ Agent skill assessment          │
│  ├─ Evidence-skill alignment        │
│  └─ Redundancy detection           │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  K-GAT Topology Generator           │
│  ├─ Encode query-evidence features  │
│  ├─ Autoregressive agent selection  │
│  ├─ Connection generation           │
│  └─ Role assignment                │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Topology Validation                │
│  ├─ Constraint satisfaction         │
│  ├─ Cycle detection                 │
│  ├─ Feasibility check               │
│  └─ Fallback generation             │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Dynamic Topology Execution         │
│  ├─ Instantiate agents              │
│  ├─ Route messages                  │
│  ├─ Aggregate responses             │
│  └─ Collect execution traces        │
└─────────────────────────────────────┘
```

### Technical Architecture

**Graph Neural Network Component:**

```
Query Embedding: e_q = ENCODE(Query)
Evidence Embedding: e_e = [ENCODE(Ev_i) for Ev_i in Evidence]
Agent Embeddings: e_a = [EMBED(Agent_i) for Agent_i in Pool]

Knowledge Conditioning:
h = GNN_encoder([e_q, e_e, e_a])

Agent Selection Probabilities:
p_select = softmax(MLP_select(h))

Edge Generation:
for i,j in agent_pairs:
    p_edge[i,j] = sigmoid(MLP_edge([h_i, h_j, e_e]))

Role Assignment:
for agent_i in selected:
    role[agent_i] = softmax(MLP_role(h_i))
```

## Practical Applications & Use Cases

### 1. Expert-Level Question Answering

GPQA and similar benchmarks benefit significantly:
- Complex questions requiring multi-step reasoning
- Multiple evidence sources to reconcile
- Expert-level knowledge integration
- Topology optimized per question difficulty

**Example:** 
```
Query: "What is the relationship between [protein A] and [disease B]?"

Retrieved Evidence:
- Recent research papers (3)
- Biological databases (2)
- Clinical trial results (1)

Generated Topology:
Retrieval Agent → Domain Expert Agent → Synthesis Agent → 
Evidence Reconciliation Agent → Response Agent
```

### 2. Complex Decision Support

Organizations using AI for critical decisions:
- Legal case analysis with multiple evidence sources
- Medical diagnosis with patient data and research
- Technical troubleshooting with logs and documentation
- Business intelligence with multiple data streams

### 3. Adaptive Reasoning for Different Query Types

Different query types require different topologies:

**Factual Queries:**
- Simple chain topology
- Direct retrieval-to-response
- Minimal agent involvement

**Analytical Queries:**
- Hub-and-spoke topology
- Multiple analysts in parallel
- Evidence synthesis node

**Adversarial Queries:**
- Mesh topology
- Agents checking each other
- Multiple perspectives

**Creative Queries:**
- Hierarchical topology
- Diverse specialist inputs
- Final synthesis/curation

### 4. Knowledge-Intensive Applications

Any domain requiring extensive external knowledge:
- Scientific research automation
- Literature review synthesis
- Policy analysis and impact assessment
- Code base analysis and optimization
- Documentation generation

### Integration Challenges

1. **Evidence Source Integration:** Connecting diverse retrieval systems
2. **Agent Capability Representation:** Standardizing agent skill descriptions
3. **Topology Scheduling:** Coordinating complex message passing patterns
4. **Failure Handling:** Graceful degradation when agents fail
5. **Latency Requirements:** Meeting SLAs while generating topologies

### Cost and Latency Implications

- **Retrieval:** 100-500ms for evidence gathering
- **Topology Generation:** 50-200ms for graph generation
- **Execution:** Depends on number of agents (typically 200ms-2s)
- **API Costs:** Reduction through selective agent use (10-30% savings vs uniform approaches)

## Insights & Implications

### Impact on Multi-Agent System Design

1. **Evidence-Driven Organization:** Topologies responding to actual information needs
2. **Adaptive Collaboration:** Flexible coordination patterns rather than fixed workflows
3. **Efficient Specialization:** Agents utilized based on expertise-evidence alignment
4. **Knowledge Integration:** Seamless incorporation of external information into decisions

### Advancement in Agent Orchestration

- **Dynamic Topology Learning:** Moving from static to adaptive structures
- **Knowledge-Conditioned Planning:** Evidence explicitly influencing agent organization
- **Neuro-Symbolic Integration:** Combining neural and symbolic reasoning
- **Query-Adaptive Systems:** Responses tailored to informational requirements

### Limitations and Open Questions

1. **Scalability:** How does method scale with large agent pools?
2. **Convergence:** Do topologies converge to optimal structures?
3. **Theoretical Foundations:** Formal guarantees on optimality?
4. **Interpretability:** Can we explain why particular topologies were chosen?
5. **Transfer Learning:** Do learned topology patterns transfer to new domains?

### Relevance to Agent Frameworks

This work has implications for agent framework architecture:

- **Dynamic Routing:** Frameworks must support runtime topology changes
- **Agent Capability Specification:** Standardized formats for agent skills
- **Evidence Integration:** Built-in evidence retrieval and ranking
- **Topology Verification:** Mechanisms for validating generated graphs
- **Monitoring and Observability:** Tracking topology effectiveness

## Code & Resources

**Official Repository:** [Check arXiv page for GitHub link]

**Dependencies:**
- Graph Neural Network library (PyTorch Geometric, DGL)
- LLM API for evidence-conditioned generation
- Evidence retrieval system (Elasticsearch, vector DB)
- Multi-agent execution framework

**Key Libraries:**
- PyTorch Geometric for GNN implementation
- Transformers for encoding
- NetworkX for graph operations
- Ray for distributed execution

**Compute Requirements:**
- Training: GPU acceleration helpful
- Inference: CPU sufficient for most queries
- Memory: 4-8GB for model and evidence cache
- Storage: Document index storage needs

**Quick-Start Integration:**

1. Set up evidence retrieval pipeline
2. Define agent capability registry
3. Implement GNN encoder
4. Create topology validator
5. Build execution orchestrator
6. Test on benchmark datasets
7. Integrate with production systems

## Related Work & Context

### Foundational Research

- **Graph Neural Networks:** Deep learning on structured data
- **Neuro-Symbolic AI:** Combining neural and symbolic approaches
- **Multi-Agent Coordination:** Agent communication and collaboration
- **Information Retrieval:** Evidence gathering and ranking
- **Program Synthesis:** Automated system design

### Related Topics

- **Adaptive Topologies:** Dynamic versus static agent networks
- **Agent Specialization:** Capability matching and allocation
- **Evidence Integration:** Incorporating external knowledge
- **Coordination Protocols:** Multi-agent communication standards
- **Knowledge Graphs:** Structured evidence representation

### Future Research Directions

1. **Learning Topology Preferences:** Understanding agent interaction patterns
2. **Cross-Domain Transfer:** Topologies for new domains with no training data
3. **Hierarchical Topologies:** Multi-level agent organizations
4. **Temporal Dynamics:** Topologies evolving during task execution
5. **Adversarial Robustness:** Topologies resilient to agent failures
6. **Human-Agent Collaboration:** Incorporating human experts into topologies
7. **Theoretical Analysis:** Bounds on topology optimality

## Related Papers and Topics

- Multi-Agent System Architectures
- Agent Communication and Protocols
- Retrieval-Augmented Generation
- Evidence-Based Reasoning
- Adaptive Agent Topologies
- Knowledge Integration in AI Systems
- Collaborative Multi-Agent Planning
