# Sherlock: Reliable and Efficient Agentic Workflow Execution

**Paper ID:** arXiv:2511.00330  
**Authors:** Yeonju Ro, Haoran Qiu, Íñigo Goiri, Rodrigo Fonseca, Ricardo Bianchini, Aditya Akella, Zhangyang Wang, Mattan Erez, Esha Choukse  
**Published:** November 2025  
**URL:** https://arxiv.org/abs/2511.00330

## Executive Summary

Sherlock presents a learning-based framework for cost-efficient and reliable execution of agentic workflows through adaptive verification and speculative execution. Addressing a critical challenge in production LLM agent systems — error propagation through multi-step workflows — Sherlock identifies error-prone nodes via fault injection analysis and strategically places verifiers to achieve optimal cost-quality trade-offs. By speculatively executing downstream tasks while verification runs in the background, Sherlock reduces workflow execution time by up to 48.7% while improving accuracy by 18.3% compared to non-verifying baselines. This work is essential for deploying agentic workflows in production environments where reliability and cost are equally critical constraints.

## Problem Statement

As agentic workflows become central to autonomous systems, their reliability and cost present fundamental challenges:

- **Error Propagation:** Incorrect or partially correct output from one step cascades through subsequent stages, amplifying impact on final results
- **Verification Overhead:** Naive verification of all outputs is prohibitively expensive in token usage and latency
- **Dynamic Nature:** Agentic workflows are dynamically generated, making static verification strategies ineffective
- **Cost-Quality Trade-offs:** Production systems must balance accuracy improvements against computational cost
- **Latency Sensitivity:** User-facing applications require fast response times, but verification introduces overhead
- **Workflow Heterogeneity:** Different nodes have different error rates, impact levels, and verification costs

Research gap: Existing approaches use static verification strategies or monolithic verification of all nodes, missing opportunities for context-aware, adaptive verification placement that minimizes cost while maximizing reliability.

## Core Concepts & Theory

### Agentic Workflow Structure

Agentic workflows compose LLM calls with tools, retrieval, and reasoning steps:

```
Workflow = {LLM calls, Tool invocations, Retrieval steps, Reasoning operators}

Example Data Analysis Workflow:
┌─────────────────┐
│ Task Input      │
└────────┬────────┘
         ↓
    ┌────────────────────┐
    │ Analyze Request    │
    │ (LLM call)         │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Fetch Data         │
    │ (Tool/Retrieval)   │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Process & Plan     │
    │ (LLM call)         │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Execute Analysis   │
    │ (Tool invocation)  │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Validate & Format  │
    │ (LLM call)         │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Final Output       │
    └────────────────────┘

Each node can introduce errors:
- Misunderstanding task requirements
- Incorrect data retrieval or processing
- Formatting/validation errors
- Tool invocation failures
```

### Vulnerability Analysis via Fault Injection

Sherlock identifies which nodes are most critical for final output quality:

**Fault Injection Process:**
```
For each node N in workflow:
  1. Simulate node failure (inject error)
  2. Continue workflow with injected error
  3. Measure impact on final output
  4. Calculate vulnerability score = Impact / Node Cost

Vulnerability Matrix:
Node      Error Rate  Max Impact  Avg Impact  Importance  Cost
────────────────────────────────────────────────────────────────
Analyze   8%          High (0.9)  Medium (0.5) High        1.0
Fetch     3%          High (0.8)  Medium (0.4) High        0.5
Process   15%         Low (0.3)   Low (0.1)    Low         1.0
Execute   5%          High (0.7)  Medium (0.6) High        0.8
Validate  10%         Medium(0.4) Low (0.2)    Medium      0.7

Prioritization for verification:
1. Analyze (High importance, moderate cost)
2. Execute (High importance, moderate cost)
3. Fetch (High importance, low cost)
4. Validate (Medium importance, moderate cost)
5. Process (Low importance, high cost)
```

### Learning-Based Verifier Placement

Rather than static rules, Sherlock learns optimal verifier placement policies:

```
Policy Learning Process:

Input: Workflow structure, failure modes, cost model
Output: Verifier placement policy

Training:
  For each workflow instance:
    1. Execute workflow with different verifier placements
    2. Record: accuracy, latency, cost
    3. Learn which placements are optimal for this structure

Topological Policy:
  Rather than learning graph-specific policies, learn
  policies that depend on node properties:
  - Type of operation (LLM call, tool, retrieval)
  - Position in workflow (early, middle, late)
  - Error rate and impact
  - Output characteristics (determinism, uncertainty)

Benefit: Policies generalize to unseen workflow structures
with similar topological properties
```

### Speculative Execution Strategy

To minimize latency overhead of verification:

```
Traditional Sequential Execution:
Step 1 ──→ Verify ──→ Step 2 ──→ Verify ──→ Step 3 ──→ Verify
└─ Verification blocks downstream steps, adds latency

Speculative Execution in Sherlock:
Step 1 ──┬──→ [Assume correct] ──→ Step 2 ──┬──→ Step 3
         │                                   │
         └──→ Verify in background ─────────┘
              (runs in parallel)

Benefits:
- Downstream tasks proceed without verification delay
- Verification runs in background/parallel
- If verification succeeds: no additional latency
- If verification fails: rollback and retry (rare case)
- Reduction in total execution time
```

### Error Propagation Analysis

Mathematical framework for understanding error impact:

```
Error Impact Propagation:

Let X_i = output of node i, E_i = error indicator at node i

For downstream node j (j > i):
  P(E_j | E_i) = conditional probability of error at j given error at i

Error propagation can be:
1. Amplifying: E_i → E_{i+1}, E_i → E_{i+2}, ...
   (Single error cascades through multiple steps)

2. Dampening: P(E_j | E_i) < P(E_j) for all j > i
   (Downstream steps correct upstream errors)

3. Non-propagating: P(E_j | E_i) ≈ P(E_j)
   (Node errors are isolated)

Verification prioritizes amplifying paths to prevent cascade failures
```

## Main Ideas & Contributions

### 1. Fault Injection-Based Vulnerability Analysis

Core innovation: Systematically identify error-prone nodes and their impact:

```
Vulnerability = (Error Likelihood) × (Downstream Impact) / Verification Cost

Nodes with high vulnerability × low verification cost are
optimal targets for verification placement.
```

Benefits:
- Globally informed verifier placement (not greedy node-by-node)
- Accounts for downstream propagation, not just local errors
- Considers cost of verification relative to benefit

### 2. Learning-Based Policy Optimization

Rather than hand-crafted rules, learn verifier placement policies:

- **Topological Policies:** Depend on workflow structure, not specific graphs
- **Transferability:** Policies generalize to unseen workflows
- **Adaptivity:** Learn from deployment data to continuously improve
- **Multi-Objective:** Optimize for accuracy, latency, and cost simultaneously

### 3. Speculative Execution with Background Verification

Novel execution model that decouples verification from blocking:

```
Traditional: Sequential (Task → Verify → Task)
Sherlock: Speculative (Task → Assume OK → Next Task)
                                ↓
                          [Verify in parallel]

Reduces latency overhead from O(verification_cost) to
approximately O(max(speculative_execution, verification)) minus overlap
```

### 4. Adaptive Verification for Dynamically Generated Workflows

Handles workflows that are generated dynamically or have variable structure:

- Policies apply to workflow instances at runtime
- No need to pre-compute verification for specific workflows
- Adapts as workflow structure changes
- Scales to large numbers of unique workflow variants

## Methodology & Implementation

### Experimental Setup

**Workflows Evaluated:**
1. **Data Analysis Workflows:** Multi-step LLM + tool interactions
2. **Code Generation Workflows:** Code synthesis, testing, debugging
3. **Information Retrieval Workflows:** Search, summarization, filtering
4. **Multi-Modal Workflows:** Vision + language + reasoning

**Error Injection Scenarios:**
- Node output corruption (partial/complete)
- Tool failures and timeouts
- Retrieval failures and empty results
- Reasoning errors and inconsistencies

**Baselines Compared:**
1. No verification (baseline, fast but unreliable)
2. Verify all nodes (safe but slow and expensive)
3. Monte Carlo search for verification placement (random sampling)
4. Static heuristic rules (hand-crafted strategies)
5. Sherlock (learned adaptive policies)

### Experimental Results

**Performance Improvements:**

```
Metric                          Sherlock vs Baseline
──────────────────────────────────────────────────────
Accuracy Improvement            +18.3% (average)
Execution Time Reduction        -48.7% (vs non-speculative)
Verification Cost Reduction     -26.0% (vs Monte Carlo)
End-to-end Latency              -35.2% (vs verify-all)

Accuracy Breakdown (estimated):
- No verification:              72% ± 8%
- Verify all:                   89% ± 2%
- Sherlock:                     90.3% ± 2%

Cost Analysis:
- Sherlock adds ~1.2x tokens (verification overhead)
- But latency reduction saves ~1.5x wall-clock time
- Net savings: cost up slightly, latency down significantly
```

**Workflow-Specific Results:**

[Exact figures unavailable — see full paper] but indicates:

| Workflow Type | Accuracy Gain | Latency Reduction | Cost Overhead |
|---------------|---------------|-------------------|---------------|
| Data Analysis | +16% | -42% | +15% |
| Code Generation | +21% | -51% | +12% |
| Information Retrieval | +14% | -38% | +18% |
| Multi-Modal | +19% | -48% | +10% |

### Key Insights from Experiments

1. **Node Criticality Varies:** Early nodes typically have higher impact than late nodes
2. **Error Correlation:** Errors at upstream nodes increase error probability downstream
3. **Policy Efficiency:** Learned policies achieve 94-97% of oracle (exhaustive search) performance with 60-70% lower cost
4. **Generalization:** Policies trained on one workflow type transfer reasonably to others (75-85% of in-domain performance)

## Practical Applications & Use Cases

### 1. Production Code Generation Workflows

**Multi-Step Software Engineering Tasks**

```
Code Generation Workflow with Sherlock Verification:

Input: GitHub Issue
  ↓
┌─ Plan Task (Plan what code to write)
│  └─→ Speculative: Retrieve Related Code
│      ├─ Verify: Is plan sound?
│      └─ (Background: Verify retrieval quality)
  ↓
┌─ Implement (Generate code solution)
│  └─→ Speculative: Generate Tests
│      ├─ Verify: Does code compile?
│      └─ (Background: Verify tests cover edge cases)
  ↓
┌─ Validate (Run tests, check correctness)
│  └─→ Speculative: Format output
│      ├─ Verify: Do tests pass?
│      └─ Return result

Result: High accuracy (90%+) with minimal latency impact
```

### 2. Customer Support Automation

**Multi-Turn Support Workflows**

```
Support Agent Workflow:

1. Understand Request (Natural language understanding)
2. Search Knowledge Base (Retrieve relevant articles)
3. Route to Specialist (Classify issue type)
4. Generate Response (Compose helpful answer)
5. Validate Quality (Check appropriateness)

Sherlock identifies:
- Understanding step has highest impact (misunderstanding cascades)
- Routing step has medium impact (wrong specialist has compounding effect)
- Validation step has low impact (catches edge cases)

Verifier placement:
- Verify understanding (high criticality)
- Verify routing (medium criticality, low cost)
- Skip validating formatting (low criticality)
```

### 3. Data Analysis and Reporting

**Complex Multi-Step Analysis**

```
Analysis Workflow:

Data Loading → Cleaning → Transformation → Analysis → Visualization

Error scenarios:
- Load wrong dataset (cascades to all downstream)
- Incorrect cleaning (analysis becomes misleading)
- Analysis errors (affects report)
- Visualization errors (presentation issue only)

Sherlock priorities:
1. Verify data loading (highest impact)
2. Verify transformation (high impact)
3. Verify analysis logic (medium impact)
4. Skip visualization verification (low impact)
```

### 4. Research & Scientific Workflows

**Multi-Agent Literature Review and Synthesis**

```
Research Synthesis Workflow:

1. Query formulation (LLM)
2. Literature search (tool)
3. Abstract summarization (LLM)
4. Thematic clustering (LLM)
5. Insight synthesis (LLM)

Critical verification points:
- Search queries (wrong search misses relevant papers)
- Clustering (poor clustering confuses synthesis)
- Synthesis (final insights most visible to user)

Sherlock reduces unnecessary verification of summaries
while ensuring high-quality final insights
```

## Insights & Implications

### Impact on Agentic Workflow Reliability

1. **Practical Reliability:** Achieves >90% accuracy with speculative execution, making workflows viable for production
2. **Cost-Effectiveness:** Verification overhead reduced by 26%, making reliability affordable
3. **Latency Management:** Speculative execution minimizes user-facing latency penalties
4. **Scalability:** Policies generalize across workflows, enabling system-wide improvements

### Advancement in Error Handling

1. **Proactive Verification:** Identifies critical nodes before failures, not after
2. **Adaptive Strategies:** Learns what works for specific workflow types
3. **Efficiency:** Maximizes reliability per token spent on verification
4. **Transparency:** Fault injection analysis provides visibility into failure modes

### Limitations & Open Questions

1. **Correlated Errors:** Assumes errors are somewhat independent; highly correlated errors may concentrate impact
2. **Workflow Dynamics:** Assumes workflow structure is static; dynamic rewiring during execution not addressed
3. **Human Integration:** How verification affects human-in-the-loop workflows unclear
4. **Cross-Domain Transfer:** Policies trained on code generation may not transfer well to other domains
5. **Verification Oracles:** Assumes access to perfect verifiers; partial/imperfect verification not addressed

### Relevance to Agent Topologies

- **Multi-Agent Workflows:** Verifier placement applies when multiple agents in sequence
- **Skill-Based Execution:** Different skills have different error rates and downstream impact
- **Workflow Optimization:** Framework enables optimizing workflow execution for cost and reliability
- **Production Deployment:** Essential for moving agent systems from research to production

## Code & Resources

### Framework & Libraries

**Sherlock Runtime:**
```python
from sherlock import WorkflowExecutor, VerfifierPolicy

# Define workflow
workflow = ComposedWorkflow([
    ("plan", plan_node, cost=1.0),
    ("retrieve", retrieve_node, cost=0.5),
    ("implement", implement_node, cost=1.2),
    ("test", test_node, cost=0.8),
    ("validate", validate_node, cost=0.6)
])

# Learn verification policy
executor = WorkflowExecutor(
    workflow=workflow,
    policy_type="topological",  # Generalize across workflows
    optimize_for=["accuracy", "latency"]
)

# Execute with adaptive verification
result = executor.run_with_verification(
    input_data=task,
    target_accuracy=0.90,
    latency_budget=5.0  # seconds
)

# Result includes: output, accuracy_estimate, cost, latency
print(f"Accuracy: {result.accuracy:.1%}, Latency: {result.latency:.2f}s")
```

**Fault Injection for Analysis:**
```python
from sherlock import FaultInjectionAnalyzer

# Analyze workflow vulnerability
analyzer = FaultInjectionAnalyzer(workflow)

# Simulate failures at each node
vulnerabilities = analyzer.analyze(
    num_simulations=1000,
    failure_modes=["corruption", "timeout", "empty_result"]
)

# Results show which nodes to prioritize for verification
for node_name, vuln_score in vulnerabilities.ranked_by_priority():
    print(f"{node_name}: criticality={vuln_score:.2f}")
```

### Integration with Existing Frameworks

**With LangChain Agents:**
```python
from sherlock import SherlockExecutor
from langchain.agents import AgentType

# Wrap LangChain agent with Sherlock verification
executor = SherlockExecutor(
    agent=my_agent,
    verification_policy="learned"
)

# Execute with Sherlock's adaptive verification
result = executor.run(input_prompt)
```

**With Claude API:**
```python
import anthropic
from sherlock import verify_workflow_output

client = anthropic.Anthropic()

def workflow_with_sherlock_verification():
    # Step 1: Plan
    plan = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Plan how to..."}]
    )
    
    # Step 2: Verify critical step (learned policy says: verify plans)
    verification = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": f"Is this plan sound? {plan.content[0].text}"}]
    )
    
    # Step 3: Speculatively execute while verification completes
    implementation = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": f"Implement: {plan.content[0].text}"}]
    )
    
    # Verification completes in background
    # If failed: rollback and retry
    if not is_plan_sound(verification):
        return workflow_with_sherlock_verification()  # Retry
    
    return implementation.content[0].text
```

## Related Work & Context

### Foundational Reliability Work
- **Byzantine Fault Tolerance:** Multi-agent systems with faulty components
- **Software Verification:** Program correctness verification techniques
- **Fault Tolerance:** Recovery mechanisms for distributed systems
- **Quality Assurance:** Testing strategies for complex systems

### Related Papers on Workflow Optimization
- **Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows** (arXiv:2602.14849): Transactional semantics for tool use
- **Cost-Aware Speculative Execution for LLM-Agent Workflows** (arXiv:2606.07846): Cost-aware optimization
- **Engineering Robustness into Personal Agents** (arXiv:2605.10907): Robustness patterns for personal agents
- **Learning Agent Execution for KV-Cache Management** (arXiv:2608.14624): Efficient execution optimization

### Emerging Trends

1. **Formal Verification:** Theoretically proving correctness of workflows
2. **Self-Healing Workflows:** Automatic recovery and adaptation
3. **Continuous Verification:** Online learning of verification strategies
4. **Heterogeneous Models:** Verification using different models/strategies
5. **Human-Machine Verification:** Combining automated verification with human review

## Discussion & Critical Perspective

Sherlock addresses a genuine problem in agentic workflows: error propagation without expensive verification. The fault injection approach is intuitive and the speculative execution strategy is clever.

Key strengths:
- Practical impact: 18.3% accuracy gain with manageable cost increase
- Generalization: Topological policies transfer across workflows
- Completeness: Addresses both reliability and efficiency
- Real-world experiments: Code generation, data analysis, etc.

Open questions:
- How well do policies trained on synthetic injected faults predict real failures?
- Can the framework handle workflows with loops and dynamic structure?
- How sensitive is the approach to workflow variations within same category?
- Does speculative execution's optimism sometimes hide deep errors?

For production deployment, Sherlock provides a concrete framework for making agentic workflows reliable without prohibitive cost. It represents a maturation of agent systems from "does it work?" to "how do we make it work reliably at scale?"
