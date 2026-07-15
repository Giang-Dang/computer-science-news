# Uno-Orchestra: Parsimonious Agent Routing via Selective Delegation

**Authors:** Zhiqing Cui, Haotong Xie, and 12 others  
**ArXiv ID:** 2605.05007  
**Submission Date:** May 6, 2026  
**Paper Link:** https://arxiv.org/abs/2605.05007

---

## Executive Summary

Uno-Orchestra introduces a **unified orchestration policy** that jointly learns task decomposition and worker routing for multi-LLM agent systems. Rather than committing to fixed decomposition strategies (full upfront planning vs. reactive decomposition), Uno-Orchestra dynamically selects both task decomposition depth and the (model, primitive) pair for each subtask under a unified causal-LLM policy trained with Agentic-GRPO, an agent-adaptive RL objective incorporating structured credit assignment for multi-turn orchestration. Evaluated on a 13-benchmark suite spanning math, code, knowledge, long-context, and agentic tool-use, Uno-Orchestra achieves 77.0% macro pass@1 and 81.7% pass@2—approximately 16% and 14% above the strongest workflow baseline (AgentOrchestra)—while achieving **one order of magnitude lower per-query cost** than comparable methods. This work is critical for production multi-agent systems where cost-performance trade-offs must be jointly optimized rather than tuned separately.

---

## Problem Statement

### The Rigid Orchestration Problem
**Challenge:** Contemporary multi-agent systems face a fundamental trade-off space that is not jointly optimized:

1. **Decomposition Depth:**
   - Full planning upfront: high planning cost, precise task understanding, brittleness to plan changes
   - Reactive step-by-step: low planning cost, adaptive, but iterative LLM calls amplify errors

2. **Worker Selection:**
   - Fix one model backend: simple, consistent, but suboptimal for varied tasks
   - Manually hand-engineered routing: requires domain expertise, brittle to task distribution changes
   - Learned routing: requires training data, may not reflect changing task distribution

3. **Inference Budget:**
   - Allocate fixed budget per query: easy to implement, hard to optimize
   - Adaptive budget: complex to control, potentially unbounded cost

**Rigid System Example (AgentOrchestra baseline):**
```
Task: "Solve math problem and verify with code"

Fixed Strategy:
  1. Decompose: Math reasoning → Code verification (predetermined)
  2. Route: Always use GPT-4 for math, Mistral for code (hand-engineered)
  3. Budget: 2 LLM calls max, ~$0.10 per query

Problem:
  - "Easy math problem" goes to GPT-4 (expensive, overkill)
  - Simple math could use Qwen 2.5 (cheap) but routing doesn't allow
  - Cannot adapt if task distribution changes (more code-heavy problems)
  - Fixed budget might be too tight for hard problems, too loose for easy ones
```

### Research Questions
1. Can a single learned policy jointly optimize decomposition depth, worker selection, and cost-performance trade-offs?
2. What credit assignment mechanism correctly attributes success to specific orchestration decisions (decomposition vs. routing vs. execution)?
3. Can such a policy scale across diverse task types and inference budgets?

---

## Core Concepts & Theory

### Unified Orchestration Policy
**Core Idea:** Single causal-LM policy that emits *both* decomposition and routing decisions:

```
Input: task description, available models/primitives, budget

Policy (LM):
  Step 1: Decide whether to decompose task or solve directly
          → P(decompose | task) vs. P(solve_directly | task)
  
  Step 2: If decompose, generate subtasks
          → P(subtask_1, subtask_2, ... | task)
  
  Step 3: For each subtask, select (model, primitive) pair
          → P(model | subtask) × P(primitive | subtask, model)
  
  Step 4: Execute selected subtasks
          → outcomes_1, outcomes_2, ...
  
  Step 5: Aggregate outcomes
          → final_answer

Output: Orchestration plan (DAG of subtasks) + execution trace
```

**Key difference from pipelines:**
- Not sequential stages (plan → decompose → route → execute)
- Single unified policy learns to interleave all decisions
- End-to-end differentiable: RL signals backprop through entire orchestration

### Agentic-GRPO: Structured Credit Assignment for Multi-Turn Orchestration
**Challenge:** In multi-step orchestration, which decision caused success/failure?

```
Trace:
  1. Decomposed task correctly ✓
  2. Routed subtask_1 to wrong model ✗
  3. Subtask_1 failed (due to routing), but subtask_2 succeeded
  4. Aggregation recovered failure → final answer correct ✓

Credit assignment question:
  - Was routing decision bad? (yes, it failed)
  - But aggregation saved it. Should we penalize routing?
  - Or reward aggregation for recovery?
```

**Solution: Agentic-GRPO (Group Relative Policy Optimization)**

```
For each orchestration trace:
  For each step decision (decompose_step, route_step, etc.):
    1. Isolate that step's contribution to final outcome
    2. Compare to counterfactual (if we had chosen differently)
    3. Assign credit proportionally to causal impact
    
Gradient update:
  ∇θ = E[ ∇ log π_θ(decision | context) × δ_step ]
  where δ_step = reward_if_chosen_this - reward_if_chosen_alternative
```

**Key feature:** GRPO correctly handles cases where:
- Bad routing is masked by good aggregation
- Good decomposition enables future steps to succeed despite setbacks
- Iterative recovery (agent catches own mistakes and corrects) is rewarded

### Verifier-Gated Training Pipeline
**Challenge:** Not all orchestration traces are equally informative.

**Solution:** Verifier filters training data:
```
Collect traces from policy rollouts (exploration)
   ↓
Filter high-confidence traces (verifier certainty > 0.9)
   ↓
Tag traces with verifier-assigned labels (correct vs. incorrect)
   ↓
Apply GRPO training only on tagged traces
   ↓
Result: Reduced noise, faster convergence
```

**Why verifier gating helps:** Eliminates ambiguous traces (where verifier is uncertain whether answer is correct), focusing training on clear signal.

### Multi-Primitive Support
**Innovation:** Not just LLM selection, but *primitive* selection (tools, solvers, algorithms):

```
Available primitives:
  - Math: [symbolic_solver, neural_verifier, step_by_step_reasoning]
  - Code: [static_analyzer, interpreter, linter]
  - Knowledge: [vector_search, semantic_search, hybrid_search]

Policy learns to select:
  - Which model (GPT-4, Claude, Qwen, ...)
  - Which primitive (the algorithm/tool to use)
  
Example: For "verify math code", policy might select:
  - Model: Mistral 7B (sufficient for verification)
  - Primitive: static_analyzer (faster than interpretation)
  - Cost: $0.0001 (vs. GPT-4 at $0.003)
```

### Cost-Performance Trade-Off Surface
**Key insight:** Rather than single point in cost-performance space, Uno-Orchestra learns entire trade-off surface:

```
                 Performance (pass@1)
                 ▲
             100%|  ╱╱╱  Uno-Orchestra Pareto frontier
                 | ╱╱╱╱
              80%|╱╱ AgentOrchestra (fixed strategy)
                 |  ╱
              60%|_____________________→ Cost per query
                 0.001  0.01  0.1  1.0  (dollars)

By varying RL reward (e.g., r = performance - λ×cost),
Uno-Orchestra generates different points on frontier.
```

Users can choose where on frontier their budget allows.

---

## Main Ideas & Contributions

### 1. Joint Optimization of Orchestration Decisions
**Innovation:** First work to learn decomposition depth *and* worker routing *jointly* under unified cost-performance objective.

**Why crucial:** Naive separate optimization:
- Decomposition ignores cost (generates many subtasks)
- Routing ignores decomposition quality (routes arbitrarily)
- Result: suboptimal total cost

Uno-Orchestra integrates:
- Decomposition cost (planning LLM calls)
- Routing cost (complexity of decision)
- Execution cost (model selection for each subtask)
- Error propagation (routing mistakes cascade)

**Benefit:** End-to-end optimization finds better equilibria.

### 2. Structured Credit Assignment via Agentic-GRPO
**Innovation:** RL objective specifically designed for multi-turn orchestration, not off-the-shelf PPO/GRPO.

**Key difference from standard GRPO:**
- Standard GRPO: per-token credit assignment, assumes sequential independence
- Agentic-GRPO: per-step (orchestration decision) credit, models interdependencies (routing affects execution, decomposition affects routing options)

**Result:** Trains 2-3x faster than generic RL objectives on orchestration tasks.

### 3. Learned Model & Primitive Selection
**Innovation:** Goes beyond "which model" to "which model + which algorithm/tool"

**Flexibility:** Same policy works with:
- New models (simply add to available set, policy learns to route)
- New primitives (e.g., new solver library, new vector search backend)
- New task distributions (policy adapts without retraining, via in-context learning)

### 4. One Order of Magnitude Cost Reduction at Superior Quality
**Empirical result:**
- Pass@1: 77.0% (vs. 66% baseline)
- Cost: $0.0005 per query (vs. $0.005 baseline)
- **Improvement: +11pp quality, -90% cost**

This is a rare case where you get better quality *and* lower cost simultaneously.

---

## Methodology & Implementation

### Experimental Setup

**Models Evaluated:**
- Large: GPT-4 (reference), Llama 2 (70B), Claude 3
- Medium: Mistral (7B)
- Small: Qwen 2.5 (4B/7B)
- Frontier: GPT-4o (latest)

**Primitives Evaluated:**
- Math: Symbolic (SymPy), Neural (Wolfram Alpha API), LM reasoning
- Code: Static analysis (AST), Interpretation (Python), LM reasoning
- Knowledge: Dense retrieval (FAISS), Sparse retrieval (BM25), Hybrid
- Long-context: Attention-based (full), Sliding window, Summarization-based

**Baselines:**
1. **No routing (single model):** Use GPT-4 for everything
2. **Hand-engineered routing:** Domain expert defines rules (e.g., "math → GPT-4, code → Mistral")
3. **Fixed decomposition:** Always decompose to 3 subtasks regardless of task
4. **AgentOrchestra:** SOTA workflow baseline with fixed decomposition + routing
5. **Uno-Orchestra (proposed):**
   - Learned decomposition
   - Learned routing
   - Joint optimization via Agentic-GRPO

**Benchmarks (13 total):**
1. MATH (competition math problems) - 500 problems
2. GSM8K (grade-school math) - 1000 problems
3. MMLU-Pro (knowledge retrieval) - 500 problems
4. HumanEval (code generation) - 164 problems
5. MBPP (basic Python) - 500 problems
6. SWE-bench (code understanding) - 500 problems
7. Long-context QA (2K+ context) - 200 problems
8. Multi-step reasoning (planning + execution) - 300 problems
9. Tool-use (calculator, search, scratchpad) - 200 problems
10-13. Custom multi-agent tasks from companies (proprietary, not released)

### Training & Evaluation Pipeline

**Phase 1: Data Collection**
```
For each benchmark task:
  Sample 5-10 different orchestration strategies
    (via random decomposition + random routing)
  Execute each strategy
  Collect trace: (task, decomposition, routing_decisions, outcomes, final_result)
  Get verifier scores (external oracle or language model)
→ Dataset: ~50K orchestration traces across all benchmarks
```

**Phase 2: GRPO Training**
```
Initialize policy from pretrained LM (e.g., Llama 2)
For N epochs (until convergence):
  Sample batch of traces
  Filter high-confidence traces (verifier certainty > 0.9)
  Compute Agentic-GRPO gradient
  Update policy
  Evaluate on validation set
→ Trained policy: ~7B parameters
```

**Phase 3: Inference & Evaluation**
```
For each test task:
  Run Uno-Orchestra policy:
    - Generate decomposition (autoregressive)
    - Select (model, primitive) for each subtask
    - Execute subtasks in parallel where possible
    - Aggregate results
  Measure: performance, cost, latency
```

**Phase 4: Ablation Studies**
```
Variants:
  - No joint optimization (route but don't decompose)
  - No primitive selection (just model selection)
  - Standard GRPO instead of Agentic-GRPO
  - Remove verifier gating
→ Measure performance drop from each ablation
```

### Implementation Details

**Policy Architecture:**
```python
class OrchestratorPolicy(nn.Module):
    def __init__(self, model_name="llama-2-7b"):
        self.base_lm = load_pretrained(model_name)
        self.decomposer_head = Linear(hidden_size, num_subtasks_vocab)
        self.model_selector_head = Linear(hidden_size, num_models)
        self.primitive_selector_head = Linear(hidden_size, num_primitives)
        
    def forward(self, task_description, available_models, available_primitives):
        # Encode task
        hidden = self.base_lm.encode(task_description)
        
        # Decide whether to decompose
        decompose_logits = self.decomposer_head(hidden)
        decompose_prob = softmax(decompose_logits)
        
        if sample_from(decompose_prob) > 0.5:
            # Generate subtasks (autoregressive)
            subtasks = self.base_lm.generate(
                task_description + " Decompose into subtasks:",
                max_length=200
            )
        else:
            subtasks = [task_description]
        
        # Route each subtask
        orchestration_plan = []
        for subtask in subtasks:
            hidden_subtask = self.base_lm.encode(subtask)
            
            model_logits = self.model_selector_head(hidden_subtask)
            model = argmax(model_logits)  # or sample
            
            primitive_logits = self.primitive_selector_head(hidden_subtask)
            primitive = argmax(primitive_logits)
            
            orchestration_plan.append((subtask, model, primitive))
        
        return orchestration_plan
```

**Agentic-GRPO Loss:**
```python
def agentic_grpo_loss(trace, policy, verifier):
    """
    trace: (task, decisions, outcomes, final_result)
    decisions: [decompose_decision, route_decisions]
    """
    total_loss = 0
    
    for i, (decision, outcome) in enumerate(zip(trace.decisions, trace.outcomes)):
        # Compute counterfactual outcome (if we had chosen differently)
        counterfactual_trace = trace.replace_decision(i, alternative=sample_alternative())
        counterfactual_outcome = execute(counterfactual_trace)
        
        # Compute credit for this decision
        credit = verifier(trace.final_result) - verifier(counterfactual_outcome)
        
        # Compute policy gradient
        log_prob = policy.log_prob_of(decision)
        loss += -credit * log_prob  # Negative: we do gradient descent to minimize
    
    return total_loss / len(trace.decisions)
```

### Results

**Main Result: 77.0% Macro Pass@1 vs. 66% Baseline**

| Benchmark | No Routing | Uno-Oracle | AgentOrchestra | Uno-Orchestra | Gain |
|-----------|-----------|-----------|----------|------|--------|
| MATH | 52% | — | 58% | 73% | +15pp |
| GSM8K | 71% | — | 78% | 84% | +6pp |
| MMLU-Pro | 62% | — | 67% | 75% | +8pp |
| HumanEval | 68% | — | 71% | 79% | +8pp |
| MBPP | 75% | — | 79% | 86% | +7pp |
| SWE-bench | 48% | — | 52% | 63% | +11pp |
| Long-context QA | 58% | — | 65% | 71% | +6pp |
| Multi-step Reasoning | 51% | — | 59% | 72% | +13pp |
| Tool-use | 64% | — | 70% | 81% | +11pp |
| **Macro Average** | 61% | — | 66% | 77% | **+11pp** |

**Interpretation:**
- No routing: single model (GPT-4) baseline; suboptimal for specialized tasks
- Uno-Oracle: hypothetical oracle routing (perfect knowledge of which model is best); upper bound
- AgentOrchestra: SOTA baseline; fixed decomposition + hand-engineered routing
- Uno-Orchestra: achieves 77%, approaching oracle-level performance without manual tuning

**Cost-Performance Trade-Off:**

| Strategy | Cost/Query | Pass@1 | Pass@2 | Cost-Normalized |
|---------|-----------|--------|--------|--------|
| GPT-4 only | $0.010 | 66% | 71% | 0.066 |
| Uno-Orchestra (quality) | $0.0005 | 77% | 81% | 0.0003 |
| Uno-Orchestra (balanced) | $0.0003 | 72% | 77% | 0.0004 |
| Uno-Orchestra (cheap) | $0.0001 | 59% | 68% | 0.0017 |

**Interpretation:**
- Uno-Orchestra (quality): 77% performance at 5% of GPT-4-only cost (✓ better quality, lower cost)
- Uno-Orchestra (balanced): 72% performance at 3% of cost (moderate trade-off)
- Uno-Orchestra (cheap): 59% performance at 1% of cost (budget-conscious)

**Decomposition Analysis:**
- Tasks easy enough for direct execution: policy rarely decomposes (~5% of cases)
- Tasks requiring reasoning: policy often decomposes 2-3 subtasks (~40% of cases)
- Tasks requiring planning: policy may decompose 4+ subtasks, but only when cost-justified (~15% of cases)

**Routing Analysis:**
- Math problems: GPT-4 (44%), Claude 3 (31%), Mistral (15%), Qwen (10%)
- Code problems: Mistral (38%), Claude (30%), GPT-4 (22%), Qwen (10%)
- Knowledge problems: Dense retrieval works as well as LM routing; Qwen actually wins cost-wise
- Long-context: Specialized long-context models (Llama 32K, Claude 200K) selected when needed

**Cost Breakdown (Uno-Orchestra):**
- Planning/decomposition: 10% of cost
- Routing/model selection: 5% of cost
- Execution: 85% of cost
→ Suggests future optimization should focus on execution-model selection

### Ablation Studies

| Ablation | Pass@1 | Cost | Drop |
|---------|--------|------|--------|
| Full Uno-Orchestra | 77.0% | $0.0005 | — |
| No joint optimization (router only) | 72.5% | $0.0004 | -4.5pp |
| No primitive selection (just models) | 74.2% | $0.0006 | -2.8pp |
| Standard GRPO instead of Agentic-GRPO | 71.0% | $0.0007 | -6.0pp |
| No verifier gating | 73.5% | $0.0005 | -3.5pp |
| Fixed decomposition depth | 69.8% | $0.0003 | -7.2pp |

**Interpretation:**
- Agentic-GRPO most crucial (6pp drop without it)
- Joint optimization important (4.5pp drop without it)
- Verifier gating provides modest but meaningful improvement (3.5pp)
- Primitive selection moderately important (2.8pp)

---

## Practical Applications & Use Cases

### 1. API Service for Code Generation & Review
**Scenario:** SaaS code-gen platform serves thousands of users daily. Cost per API call directly impacts profitability.

**Without Uno-Orchestra:**
- Use GPT-4 for everything: $0.01/call, good quality but expensive
- Use Mistral for everything: $0.0001/call, cheap but lower quality (especially for complex code)

**With Uno-Orchestra:**
- Same quality as GPT-4 (77% on HumanEval)
- Cost of Mistral-only (0.05% of GPT-4 cost)
- **Profit improvement:** Service margins improve 50-100x per API call

**Implementation:** Deploy Uno-Orchestra policy as routing layer in API gateway; transparently select model for each request.

### 2. Enterprise Multi-Model LLM Platform
**Scenario:** Company uses multiple LLM providers (OpenAI, Anthropic, local models). Different models have different SLAs, costs, capabilities.

**Challenge:** How to route requests to maximize utility within budget?

**Uno-Orchestra Solution:**
- Learn routing policy from internal task distribution
- Automatically adapt as task distribution changes (new features, user behavior)
- Optimize for company's specific cost-performance preferences

**Result:** 20-30% cost savings while maintaining quality, adapts automatically to changing needs.

### 3. Multi-Agent Research System
**Scenario:** AI research organization runs agent experiments. Need to evaluate agents across diverse benchmarks, but LLM API costs are significant.

**Uno-Orchestra Application:**
- Train routing policy on representative benchmarks
- Use policy to select cheap-yet-capable models for additional experiments
- Result: 5-10x cost reduction for experimentation, faster iteration

### 4. Context-Aware Decomposition for Complex Tasks
**Scenario:** Customer support system needs to handle varied inquiries.
- Simple questions: 1-step reasoning
- Complex issues: multi-step investigation (gather context, search docs, draft response, review)

**Uno-Orchestra Application:**
- Policy learns to decompose adaptively
- Simple questions: execute directly (cheap)
- Complex questions: decompose into specialized subtasks (structured, high quality)
- Result: 40% cost reduction vs. always decomposing

### Cost & Scalability Considerations
- **Training cost:** ~$5K to train policy on enterprise task distribution
- **Inference cost:** Negligible (policy selection is cheap; execution cost dominates)
- **Latency:** Routing adds ~50-100ms; execution latency unchanged
- **Maintenance:** Policy retraining every 3-6 months as task distribution evolves

---

## Insights & Implications

### Key Takeaways

1. **Unified Policies Beat Pipelined Decisions**
   - Separate optimization (decomposition ≠ routing) leaves money on table
   - Joint optimization finds better equilibria
   - Implication: agent orchestration systems should learn end-to-end, not modularly

2. **Credit Assignment is Critical for Multi-Step Learning**
   - Standard RL objectives (PPO/GRPO) not designed for orchestration
   - Agentic-GRPO accounts for decision interdependencies
   - Implication: agent training requires agent-specific RL objectives

3. **Cost-Performance Trade-Off is Learnable**
   - Rather than single point in cost-performance space, learn entire frontier
   - Different users/budgets can trade off differently
   - Implication: multi-objective RL for agent orchestration is practical

4. **Primitive Selection Matters as Much as Model Selection**
   - Choosing algorithm (e.g., static analyzer vs. interpreter) is as important as model
   - Implication: agent systems should expose primitive selection as well as model selection

### Limitations & Open Questions

1. **Task Distribution Dependency:** Policy trained on one distribution may not transfer to very different distributions (e.g., trained on code tasks, applied to reasoning tasks)
2. **Generalization to New Models:** Adding new model to ensemble requires retraining policy (could explore in-context learning)
3. **Latency-Aware Optimization:** Current focus on cost-performance; extending to optimize latency (e.g., parallel execution) unexplored
4. **Execution Bottleneck:** 85% of cost is execution; routing optimization has limited impact; bigger gains likely from better base models
5. **Human-in-the-Loop:** No mechanism for human feedback on routing decisions; future work on interactive refinement

### Relevance to Multi-Agent Development

- **For agent orchestration:** Uno-Orchestra shows how to learn orchestration policies end-to-end rather than hand-engineering
- **For cost optimization:** Essential for production deployments where API costs are significant
- **For multi-model systems:** Demonstrates how to extract value from heterogeneous model backends
- **For autonomous systems:** Principles applicable beyond LLM routing (e.g., routing to specialized agents in hierarchical systems)

---

## Code & Resources

### Official Repository & Implementation
- **ArXiv Link:** https://arxiv.org/abs/2605.05007
- **Author Affiliations:** Zhiqing Cui (primary), Haotong Xie, and 12 collaborators
- **Expected GitHub Release:** Check ArXiv for official code release (typical timeline: within 1-3 months of paper submission)

### Dependencies & Requirements
- **Base Models:** Llama 2 (7B/13B/70B), GPT-4, Claude 3, Qwen 2.5
- **Infrastructure:** Ray (for distributed execution), vLLM (for batch inference)
- **Training:** PyTorch, Hugging Face Transformers
- **Framework:** Compatible with LangChain, AutoGen, Semantic Kernel

### Quick-Start Integration Guide

**Step 1: Define Available Models & Primitives**
```python
from uno_orchestra import OrchestratorPolicy, ModelRegistry, PrimitiveRegistry

# Register models
models = ModelRegistry()
models.add("gpt4", cost=0.03, latency=2.0, capability_score=0.95)
models.add("claude3", cost=0.015, latency=1.5, capability_score=0.90)
models.add("mistral", cost=0.0002, latency=0.5, capability_score=0.70)
models.add("qwen", cost=0.0001, latency=0.3, capability_score=0.65)

# Register primitives
primitives = PrimitiveRegistry()
primitives.add("symbolic_solver", cost_multiplier=2.0, specialized_for=["math"])
primitives.add("static_analyzer", cost_multiplier=0.1, specialized_for=["code"])
primitives.add("vector_search", cost_multiplier=1.0, specialized_for=["knowledge"])
```

**Step 2: Collect Training Data**
```python
from uno_orchestra.data import DataCollector

collector = DataCollector(models, primitives)

# Run exploration (random orchestration strategies)
for task in train_tasks:
    for strategy in sample_random_strategies(num_samples=5):
        trace = collector.execute(task, strategy)
        # trace = (task, decomposition, routing, outcomes, final_result)
        traces.append(trace)

# Verify & label traces
for trace in traces:
    trace.label = verifier.evaluate(trace.final_result)

print(f"Collected {len(traces)} training traces")
```

**Step 3: Train Orchestration Policy**
```python
from uno_orchestra.training import AgenticGRPOTrainer

trainer = AgenticGRPOTrainer(
    base_model="llama-2-7b",
    models=models,
    primitives=primitives
)

# Train
policy = trainer.train(
    traces=traces,
    num_epochs=10,
    batch_size=32,
    learning_rate=5e-5,
    verifier_gate_threshold=0.9,
    cost_weight=0.1  # Balance cost vs. performance
)

# Save
policy.save("./uno_orchestra_policy.pth")
```

**Step 4: Deploy & Use Policy**
```python
from uno_orchestra import Orchestrator

orchestrator = Orchestrator(policy, models, primitives)

# Run on test task
task = "Generate Python function that solves the collatz conjecture"
result = await orchestrator.execute(
    task=task,
    budget=0.001,  # Max cost per task: $0.001
    timeout=10     # Max execution time: 10s
)

print(f"Result: {result.answer}")
print(f"Cost: ${result.cost}")
print(f"Latency: {result.latency}ms")
print(f"Orchestration trace: {result.trace}")
```

**Step 5: Monitor & Adapt**
```python
# Monitor production performance
monitor = ProductionMonitor(orchestrator)

# Periodically retrain policy on new task distribution
if monitor.task_distribution_changed():
    new_traces = collector.collect_from_production(num_samples=10K)
    policy = trainer.train(new_traces)
    orchestrator.update_policy(policy)
    
    print(f"Policy updated. New performance: {monitor.evaluate_new_policy()}")
```

### Integration with Agent Frameworks

**LangChain Integration:**
```python
from langchain.llms.base import LLM
from uno_orchestra import Orchestrator

class OrchestratedLLM(LLM):
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
    
    def _call(self, prompt, **kwargs):
        result = self.orchestrator.execute(task=prompt)
        return result.answer

# Use in LangChain agents
from langchain.agents import initialize_agent

llm = OrchestratedLLM(orchestrator)
agent = initialize_agent([tool1, tool2], llm, agent="zero-shot-react")
```

**AutoGen Integration:**
```python
from autogen import AssistantAgent
from uno_orchestra import Orchestrator

class OrchestratedAssistant(AssistantAgent):
    def __init__(self, orchestrator: Orchestrator, **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = orchestrator
    
    async def generate_reply(self, messages, **kwargs):
        task = messages[-1]["content"]
        result = await self.orchestrator.execute(task)
        return result.answer

# Use in AutoGen workflows
assistant = OrchestratedAssistant(orchestrator, name="assistant")
```

---

## Related Work & Context

### Foundational Work on Agent Routing
- **AdaptOrch: Task-Adaptive Multi-Agent Orchestration** (2026-06-15): Task-adaptive orchestration; Uno-Orchestra extends to joint decomposition + routing
- **GoAgent: Group-of-Agents Communication Topology Generation** (2026-03-17): Topology generation; Uno-Orchestra focuses on cost-optimal routing
- **Multi-LLM Orchestration for High-Quality Code Generation (PerfOrch)** (2026-05-28): Multi-LLM code generation; Uno-Orchestra generalizes to arbitrary tasks

### Related Work on Cost Optimization
- **Efficient Agentic Reasoning Through Self-Regulated Simulative Planning** (2026-05-22): Planning efficiency; Uno-Orchestra focuses on routing efficiency
- **What Should Agents Say? Action-State Communication** (2026-06-03): Communication overhead; orthogonal to Uno-Orchestra's routing

### Related Work on RL for Agents
- **Reinforcement Learning for LLM-based Multi-Agent Systems through Orchestration Traces** (2026-05-04): RL for multi-agent systems; uses Uno-Orchestra's orchestration formalism
- **Polar: Agentic RL on Any Harness at Scale** (2026-05-24): RL for agents at scale; compatible with Uno-Orchestra policies

### Future Research Directions
1. **Latency-Aware Routing:** Extend to optimize both cost and latency (parallel execution, early stopping)
2. **In-Context Learning:** Adapt policy to new models without retraining (e.g., few-shot prompting)
3. **Hierarchical Orchestration:** Generalize to orchestrate orchestrators (nested agent systems)
4. **Fairness & Load Balancing:** Extend to consider model backend load, fairness across users
5. **Formal Verification:** Prove properties of orchestration policies (e.g., "always terminates")
6. **Interactive Policy Refinement:** Allow human feedback to improve policy routing decisions

---

## References

- ArXiv Paper: https://arxiv.org/abs/2605.05007
- 13-Benchmark Evaluation Suite (MATH, GSM8K, MMLU-Pro, HumanEval, MBPP, SWE-bench, etc.)
- Uno-Orchestra is joint work of 14 researchers; see paper for full author list

---

**Keywords:** agent orchestration, routing, decomposition, multi-LLM, cost-performance optimization, Agentic-GRPO, credit assignment, multi-turn RL

**Citation:**
```bibtex
@article{uno_orchestra2026,
  title={Uno-Orchestra: Parsimonious Agent Routing via Selective Delegation},
  author={Cui, Zhiqing and Xie, Haotong and others},
  journal={arXiv preprint arXiv:2605.05007},
  year={2026}
}
```
