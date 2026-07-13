# AgentCo-op: Retrieval-Based Synthesis of Interoperable Multi-Agent Workflows

## Executive Summary

**AgentCo-op** introduces a novel retrieval-based synthesis framework that automatically composes reusable skills, tools, and external agents into executable workflows through typed artifact handoffs and bounded self-guided local repair. The framework enables multi-agent systems to tackle open-ended tasks without requiring global topology redesign or exhaustive search, making it particularly suited for scientific discovery and complex software engineering workflows. By combining retrieval with self-repair mechanisms, AgentCo-op addresses a critical challenge in autonomous agent systems: seamlessly integrating independently developed components (agents, tools, APIs) into coherent multi-agent workflows that maintain task correctness and cost efficiency.

**Authors:** Researchers from Carnegie Mellon University  
**arXiv ID:** 2605.20425  
**Submitted:** May 19, 2026

---

## Problem Statement

### The Multi-Agent Workflow Composition Challenge

Modern autonomous systems must orchestrate diverse, independently developed components:
- **Specialized Agents:** Language models fine-tuned for specific domains (e.g., genomics, software engineering)
- **Tool Repositories:** Extensive APIs and libraries with non-standardized interfaces
- **External Services:** Third-party computational resources with different protocols
- **Custom Scripts:** Legacy code and domain-specific implementations

**The Integration Bottleneck:**

Existing approaches require:
1. **Manual Workflow Design:** Humans design task decomposition and agent coordination
2. **Interface Standardization:** All agents must conform to rigid input/output schemas
3. **Global Optimization:** Finding optimal agent topologies requires exhaustive search over exponential combinations
4. **Expert Knowledge:** Successful workflows require deep domain expertise to design

### Why Existing Approaches Fall Short

**Template-Based Systems:**
- Require pre-defined task categories and fixed decomposition patterns
- Fail on novel or hybrid problems combining multiple domains
- High maintenance burden as new agents/tools emerge

**Hierarchical Multi-Agent Systems:**
- Require centralized orchestrator that knows all agent capabilities
- Don't scale to large agent repositories (N agents = O(N²) potential pairings)
- Inflexible: changing one agent may break downstream dependencies

**Global Optimization Approaches:**
- Computationally expensive (NP-hard in general case)
- Require reliable evaluation metrics (unavailable for open-ended tasks)
- No guarantees on solution quality or efficiency

### Research Gap

The key innovation need: **How can agents compose workflows dynamically, leveraging existing skills/tools without redesign, while maintaining correctness and cost efficiency?**

AgentCo-op addresses this through retrieval + local repair.

---

## Core Concepts & Theory

### Typed Artifact Handoffs

AgentCo-op's central insight is that agent communication should be **type-safe and contract-based**:

```
Agent₁ Output: {type: "gene_expression_profile", 
               schema: {genes: List[str], 
                       values: List[float]},
               metadata: {species, tissue, method}}
                           ↓
                    [TYPE MATCH]
                           ↓
Agent₂ Input:  Expects {type: "gene_expression_profile"}
```

**Key Properties:**
- **Type Compatibility:** Agents only connect if output type ⊆ input type requirements
- **Metadata Preservation:** Rich context flows through workflow (provenance, assumptions, quality)
- **Runtime Validation:** Types checked before execution; mismatches detected early

**Benefits:**
- Eliminates "impedance mismatch" where data formats don't align
- Enables partial automation: humans intervene only when types diverge
- Generalizes across domains (genomics, code, APIs, etc.)

### Retrieval-Based Synthesis

Rather than exhaustive search, AgentCo-op uses **intelligent retrieval** to propose candidate workflows:

```
┌──────────────────────────────────────────────────┐
│      Multi-Agent Workflow Synthesis Pipeline     │
├──────────────────────────────────────────────────┤
│                                                  │
│  1. Task Understanding                          │
│     Input: Natural language task description    │
│     └─ Parse task into (input_type, output_type)
│                                                  │
│  2. Candidate Retrieval                         │
│     └─ Query agent repository for components   │
│        matching input/output types             │
│     └─ Score candidates by relevance & cost    │
│     └─ Rank top-K candidates                   │
│                                                  │
│  3. Workflow Assembly                           │
│     └─ Connect agents via type-compatible      │
│        artifact handoffs                       │
│     └─ Build directed acyclic graph (DAG)      │
│     └─ Estimate end-to-end cost                │
│                                                  │
│  4. Execution & Monitoring                      │
│     └─ Run workflow on test inputs             │
│     └─ Collect execution traces               │
│     └─ Detect failure points                   │
│                                                  │
│  5. Bounded Local Repair                        │
│     └─ Identify minimal failing components    │
│     └─ Try alternative agents/tools            │
│     └─ Re-optimize sub-workflows               │
│     └─ Return to step 3 (iteration)            │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Workflow Representation

AgentCo-op represents workflows as **typed, heterogeneous DAGs**:

```
Task: "Identify disease-associated genes from single-cell RNA-seq"

Workflow DAG:
┌─────────────────┐
│  Input Data     │
│  (RNA-seq)      │
└────────┬────────┘
         │ type: "expression_matrix"
         ↓
   ┌──────────────────┐
   │ Preprocessing    │
   │ Agent: Normalize │
   └────────┬─────────┘
            │ type: "normalized_matrix"
            ↓
    ┌────────────────────────┐
    │ Cell Type Annotation   │
    │ Agent: ClusterAnalyzer │
    └────────┬───────────────┘
             │ type: "cell_annotations"
             ├─────────────────────────┐
             ↓                         ↓
     ┌──────────────┐         ┌──────────────────┐
     │ Diff. Expr.  │         │ GO Enrichment    │
     │ Analysis     │         │ (External API)   │
     └────────┬─────┘         └────────┬─────────┘
              │ type: "de_genes"       │ type: "go_terms"
              └────────────┬───────────┘
                           ↓
                   ┌──────────────────┐
                   │ Disease Mapping  │
                   │ (KnowledgeBase)  │
                   └────────┬─────────┘
                            │
                            ↓
                   ┌──────────────────┐
                   │ Final Report     │
                   │ (Output)         │
                   └──────────────────┘
```

### Self-Repair Mechanism

AgentCo-op detects failures and attempts **bounded local repair**:

```
Repair Algorithm:
1. Execute workflow on test inputs
2. Identify failing agent A (evidence: output doesn't match expected type/quality)
3. Find alternative agents A' with same input type → output type
4. Score alternatives by:
   - Historical success rate on similar tasks
   - Cost efficiency
   - Downstream compatibility
5. Replace A with highest-scoring A'
6. Re-execute affected downstream components
7. Repeat until success or repair budget exhausted
```

**Bounded Guarantees:**
- Repair limited to local neighborhoods (avoid cascading changes)
- Cost budget enforced (don't recompute entire workflow)
- Human escalation if repair fails after K attempts

---

## Main Ideas & Contributions

### 1. Decoupled Agent Development

AgentCo-op enables **independent agent development** without centralized coordination:
- Agents publish interface contracts (input/output types, cost, quality metrics)
- New agents can be added without modifying existing workflows
- Agent owners maintain backward compatibility through versioning

**Impact:** Scales to thousands of agents without coordination overhead.

### 2. Automated Workflow Composition

The core innovation is **retrieval + assembly** rather than exhaustive search:

- **Retrieval Phase:** Use semantic similarity to propose candidates (O(log N) candidates from N agents)
- **Assembly Phase:** Type-check and connect candidates (linear in workflow size)
- **Repair Phase:** Fix failures locally (bounded cost)

**Computational Efficiency:** O(N log N) instead of exponential search space.

### 3. Typed Artifact Handoffs as Universal Interface

By standardizing data flow through typed artifacts, AgentCo-op enables **write-once, reuse-everywhere** components:
- Genomics tools integrate with code tools through artifact types
- Agents from different domains naturally compose
- New agents inherit workflow patterns without re-engineering

### 4. Cost-Aware Orchestration

AgentCo-op tracks and optimizes workflow costs:

```
Workflow Cost = Σ agent_cost(i) + Σ data_transfer_cost(edges)

Optimization Objectives:
├─ Minimize cost while maintaining > threshold success rate
├─ Minimize latency (parallel execution where possible)
└─ Minimize resource utilization (memory, compute)
```

**Practical Impact:** Multi-agent workflows become cost-efficient enough for continuous execution.

---

## Methodology & Implementation

### Experimental Evaluation

**Case Study Domains:**

1. **Genomics Workflows (Open-World Scientific Tasks)**
   - Spatial transcriptomics analysis
   - Gene-set interpretation
   - Cross-modality marker identification

2. **Software Development Tasks (Coding Benchmarks)**
   - Code generation and debugging
   - Testing and validation
   - Refactoring and optimization

3. **Mathematical & Reasoning Tasks**
   - Question answering
   - Problem solving
   - Multi-hop reasoning

### Results

**On Open-World Genomics:**
- AgentCo-op composes independently developed scientific agents without redesign
- Handles novel task combinations (e.g., spatial + expression + enrichment analysis)
- Cost efficiency: Per-task cost reduction vs. single-model approaches: [Exact figures unavailable — see full paper]

**On Unified Benchmark Suite (Coding, Math, QA):**
- **Best Result on 4/6 Benchmarks** (state-of-the-art on majority)
- **Best Average Score** under unified backbone architecture
- **Consistent Cost Reduction:** [Exact figures unavailable — see full paper] per task vs. multi-agent baselines

**Cost-Efficiency Metrics:**
- Token efficiency: [Exact figures unavailable — see full paper]
- Latency (parallel execution): [Exact figures unavailable — see full paper]
- Resource utilization: [Exact figures unavailable — see full paper]

### Comparison Baselines

- Single-LLM approaches (lower bound)
- Fixed hierarchical multi-agent topologies
- Global optimization search (upper bound on quality, lower bound on efficiency)
- Manual workflow design (expert baseline)

---

## Practical Applications & Use Cases

### 1. Scientific Discovery Workflows

**Application:** Multi-domain research combining computational biology, statistics, and knowledge bases.

**Workflow Example: Disease Gene Discovery**
```
Input: Patient RNA-seq samples

Step 1: Data Preprocessing
└─ Normalization Agent (bulk RNA-seq specialist)

Step 2: Cell Type Identification
└─ Clustering Agent (scRNA-seq specialist)

Step 3: Parallel Analysis Branches
├─ Differential Expression Agent (statistical analysis)
└─ GO Enrichment Tool (external API)

Step 4: Integration
└─ Disease Mapping Agent (biomedical knowledge base)

Output: Candidate disease genes with supporting evidence
```

**Automation Benefit:** New analyses can reuse components without redesign; new agents (e.g., GWAS integration) plug in seamlessly.

### 2. Software Engineering Automation

**Application:** Autonomous code review, testing, and refactoring.

**Workflow Example: Comprehensive Code Quality Check**
```
Input: Code commit

Agents Deployed:
├─ Code Understanding Agent (parse & AST analysis)
├─ Security Analysis Agent (vulnerability detection)
├─ Performance Agent (complexity & bottleneck analysis)
├─ Testing Agent (test coverage & quality)
├─ Style Agent (formatting & consistency)
└─ Documentation Agent (docstring completeness)

Artifact Flow:
code → [AST] → security_issues → [merged] → report
    → [metrics] → performance_issues →
    → [coverage] → testing_gaps →

Output: Comprehensive quality report
```

**Benefit:** Agents operate in parallel; results merge through typed artifacts; cost-efficient.

### 3. Multi-Modal Reasoning Systems

**Application:** Combining language, code, and tool reasoning.

**Workflow Example: Complex Problem Solving**
```
Input: Math problem with diagram

Agents:
├─ Natural Language Agent (parse text)
├─ Vision Agent (analyze diagram)
├─ Mathematical Reasoner (symbolic solving)
├─ Code Executor (verify numerically)
└─ Explanation Agent (generate answer)

Type Interfaces:
├─ NLP → Vision: "diagram_region" type
├─ Math → Code: "equation" type
├─ Code → Explainer: "verification_result" type

Output: Explained solution with verification
```

### 4. Cost-Optimized Agent Selection

**Application:** Choose agents dynamically based on task and budget constraints.

**Scenario:** "Solve this problem with <$0.10 budget"

**Workflow:**
```
1. Candidate Retrieval: Find all agents that can solve task
2. Scoring: Rank by (success_rate, cost) Pareto frontier
3. Selection: Pick cheapest agent meeting success threshold
4. Execution: Run workflow
5. Repair: If failure, try next-cheapest alternative

Cost Progression:
├─ Attempt 1: Budget = $0.05 (lightweight agent)
├─ Attempt 2: Budget = $0.03 (try different approach)
├─ Attempt 3: Budget = $0.02 (specialized tool)
└─ Success or escalate to human
```

---

## Insights & Implications

### 1. Typed Interfaces as Universal Glue

AgentCo-op demonstrates that **type-safe contracts** are sufficient to enable interoperability across domains. This mirrors Unix philosophy (everything is a file) adapted for agents (everything is a typed artifact).

### 2. Retrieval as Scalable Orchestration

Rather than solving orchestration via search or optimization, **retrieval + local repair** scales to large agent ecosystems. The insight: perfect global solutions aren't needed; good local solutions + repair suffice.

### 3. Workflow Composition as Iterative Refinement

Workflows improve through:
- More agents (larger retrieval pool)
- Better agents (higher quality matches)
- Richer artifact types (more fine-grained compatibility)
- Learning from failures (repair frequency decreases over time)

### 4. Cost Efficiency Enables Continuous Execution

By tracking and optimizing costs, AgentCo-op makes multi-agent systems practical for:
- Repeated execution of scientific workflows
- Continuous monitoring and maintenance tasks
- Real-time decision support systems

### 5. Limitations and Open Challenges

**Current Constraints:**
- Assumes artifact types are well-defined (no schema evolution)
- Repair mechanism is heuristic (no guarantees on recovery)
- Doesn't handle tasks requiring novel agent architectures
- Limited to deterministic or probabilistic tasks

**Open Questions:**
- How to automatically discover new artifact types from unlabeled agent interactions?
- Can repair mechanisms learn from failures to avoid similar issues in future?
- How do composition patterns transfer across domains?
- What's the relationship between agent diversity and workflow robustness?

---

## Code & Resources

### Official Resources

- **Paper:** arXiv:2605.20425
- **Repository:** [To be published upon acceptance]
- **Benchmarks:** Genomics use cases, coding benchmarks, QA tasks

### Implementation Dependencies

- **Agent Interface:** Defined via artifact types and I/O schemas
- **Agent Repository:** Searchable catalog of available agents and tools
- **Type System:** Structured type definitions (JSON Schema recommended)
- **Execution Engine:** DAG orchestration with fault handling
- **Repair Mechanism:** Candidate ranking and alternative selection

### Integration Checklist

```python
# Pseudocode for AgentCo-op integration

class AgentCoopWorkflowSynthesizer:
    def __init__(self, agent_repository, type_system, cost_model):
        self.repository = agent_repository
        self.types = type_system
        self.costs = cost_model
    
    def synthesize_workflow(self, task: TaskDescription) -> Workflow:
        # Step 1: Parse task into type contract
        input_type, output_type = self.types.parse_task(task)
        
        # Step 2: Retrieve candidate agents
        candidates = self.repository.retrieve(
            input_type=input_type,
            output_type=output_type,
            top_k=10
        )
        
        # Step 3: Assemble workflow
        workflow = self.types.assemble(
            candidates=candidates,
            task=task
        )
        
        return workflow
    
    def execute_with_repair(self, workflow: Workflow, test_input):
        while repair_attempts < MAX_REPAIRS:
            try:
                result = workflow.execute(test_input)
                return result
            except ExecutionError as e:
                # Bounded repair
                failing_agent = self.identify_failure(e, workflow)
                alternatives = self.repository.find_alternatives(
                    agent=failing_agent,
                    input_type=failing_agent.input_type
                )
                if alternatives:
                    # Replace and retry
                    workflow.replace(failing_agent, alternatives[0])
                    repair_attempts += 1
                else:
                    raise
    
    def cost_optimize(self, workflow: Workflow, budget: float) -> Workflow:
        """Reselect agents to fit cost budget."""
        for agent in workflow.agents:
            cheaper_alternatives = self.repository.find_alternatives(
                agent=agent,
                max_cost=budget - workflow.estimated_cost
            )
            if cheaper_alternatives:
                best = max(cheaper_alternatives, 
                          key=lambda a: a.success_rate / a.cost)
                workflow.replace(agent, best)
        return workflow
```

### Example: Genomics Workflow

```python
# Example workflow instantiation

synthesizer = AgentCoopWorkflowSynthesizer(
    agent_repository=load_genomics_agents(),
    type_system=BiologyTypeSystem(),
    cost_model=OpenAIModel()
)

task = TaskDescription(
    objective="Identify disease genes from single-cell RNA-seq",
    input_data_type="rna_seq_matrix",
    expected_output_type="disease_gene_report"
)

workflow = synthesizer.synthesize_workflow(task)

# Execute with automatic repair
results = synthesizer.execute_with_repair(
    workflow=workflow,
    test_input=load_sample_rna_seq()
)

# Optimize for cost
budget = 10.0  # dollars
optimized = synthesizer.cost_optimize(workflow, budget)
```

---

## Related Work & Context

### Foundational Multi-Agent Systems Work

- **Multi-Agent Task Decomposition:** AgentCo-op extends hierarchical decomposition with typed artifacts
- **Workflow Composition & Orchestration:** Relates to scientific workflow systems (Pegasus, Galaxy)
- **API Discovery & Composition:** Connects to API recommendation literature

### Concurrent Work (2026)

- **GoAgent (2603.17):** Group-of-agents communication topology; complements AgentCo-op's retrieval approach
- **From Static Templates to Dynamic Graphs (2603.22386):** Workflow optimization; orthogonal to AgentCo-op's synthesis
- **AgentMesh (2025):** Cooperative multi-agent framework; different coordination model

### Emerging Ecosystem

AgentCo-op is part of the **2026 workflow automation renaissance**:
- **Workflow Marketplaces:** Sharing composable workflows
- **Agent-as-a-Service:** Monetizing specialized agents
- **Type Evolution:** Dynamic schema adaptation for evolving agent ecosystems

### Future Directions

1. **Automated Type Inference:** Learn artifact types from agent I/O without manual specification
2. **Repair Learning:** Use repair outcomes to improve future composition decisions
3. **Domain Adaptation:** Transfer workflows across scientific domains
4. **Formal Verification:** Prove workflow correctness (e.g., no data loss, privacy preservation)

---

## Key Takeaways

1. **Typed Artifacts as Universal Interface:** Type-safe data flow enables seamless agent composition across domains
2. **Retrieval Scales Better Than Search:** Intelligent retrieval + local repair outperforms exhaustive optimization
3. **Decentralized Agent Development:** Agents develop independently; composition happens automatically
4. **Cost-Aware Orchestration:** Multi-agent systems become economically practical through cost optimization
5. **Workflow Robustness:** Self-repair mechanisms enable workflows to adapt to component failures

---

**Citation:**
```
[Authors TBD] (2026).
AgentCo-op: Retrieval-Based Synthesis of Interoperable Multi-Agent Workflows.
arXiv preprint arXiv:2605.20425.
```
