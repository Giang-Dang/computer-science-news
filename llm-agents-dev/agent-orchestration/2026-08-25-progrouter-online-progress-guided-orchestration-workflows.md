# ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs

**ArXiv ID:** 2608.25992  
**Authors:** Songyuan Li, Ahmed M. Abdelmoniem, Shiqiang Wang  
**Submission Date:** August 25, 2026  
**Venue:** Findings of the Association for Computational Linguistics: EMNLP 2026  
**Category:** Agent Orchestration, Multi-Agent Workflows

## Executive Summary

ProgRouter addresses a fundamental challenge in multi-agent LLM systems: dynamically selecting which agent (LLM model) should execute each step of a multi-step workflow to maximize task quality while adhering to strict time and cost budgets. Existing orchestration methods make static, query-level decisions about agent assignment, but real workflows are dynamic—the optimal agent at each step depends on evolving task progress, remaining difficulty, and budget constraints. ProgRouter introduces an online, progress-guided routing framework that adaptively selects among specialized LLM agents across workflow steps, significantly improving quality-cost efficiency. This work directly addresses the practical deployment challenge of multi-agent orchestration in cost-sensitive production environments.

## Problem Statement

### The Challenge of Quality-Cost Tradeoffs in Multi-Agent Workflows

Multi-agent LLM systems promise higher quality through specialization and collaboration, but they impose substantial operational costs:

1. **Repeated LLM Invocations:** Each workflow step requires an LLM call, multiplying token costs
2. **Long-Horizon Context:** Multi-step workflows accumulate context over many steps, increasing token consumption per call
3. **Model Heterogeneity:** Different models have different cost-quality-speed characteristics
   - Frontier models (Claude 3.5 Opus, GPT-4): High quality, high cost
   - Mid-tier models (Claude 3.5 Sonnet, GPT-4o): Good quality, moderate cost
   - Open-weight models (Llama 70B, Mistral): Faster, lower cost, potentially lower quality
4. **Quality Uncertainty:** Need to route intelligently without knowing future task difficulty or whether a step requires frontier model capabilities

### Existing Limitations

**Cascade Routing Methods:**
- Make one-shot, query-level decisions: "Use this model for entire workflow"
- Cannot adapt to discovered difficulty during workflow execution
- Miss opportunities to use cheaper models early, expensive models only when necessary

**Fixed Agent Assignment:**
- Static assignment of agents to workflow steps
- No adaptation to actual task progress or budget consumption
- Suboptimal for tasks where early steps are easy (use cheap agent) but later steps require frontier capabilities

**Uniform Model Usage:**
- Use same model for all steps (simplest approach)
- Wastes resources on early steps; insufficient capability on hard steps
- No cost-quality optimization

### Research Gap

No prior work addresses:

1. **Online Routing in Multi-Step Workflows:** Real-time agent selection based on evolving task progress
2. **Quality-Cost Joint Optimization:** Simultaneously optimizing quality and cost within explicit budget constraints
3. **Progress-Aware Routing:** Using step completion quality as signal for future step difficulty prediction
4. **Budget-Aware Adaptation:** Adjusting routing strategy when approaching time/cost limits

## Core Concepts & Theory

### Online Progress-Guided Routing Framework

ProgRouter operates as a dynamic routing layer above a multi-agent LLM system:

```
┌──────────────────────────────────────────────────┐
│            Multi-Step Workflow Input              │
│  (Step 1, Step 2, Step 3, ... Step N)            │
└────────────────┬─────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼────────────────────────┐
    │  ProgRouter (Online Router)  │
    │                              │
    │  • Estimate step difficulty  │
    │  • Select agent model        │
    │  • Track budget consumption  │
    │  • Update progress state     │
    └────┬─────────────────────────┘
         │ Route Decision
         │
    ┌────▼──────────────────────────────┐
    │  Multi-Agent LLM Pool              │
    │  ├─ Claude 3.5 Opus (Frontier)   │
    │  ├─ Claude 3.5 Sonnet (Mid)      │
    │  ├─ Gemini 2.0 Ultra (Frontier)  │
    │  ├─ GPT-4o (Mid)                 │
    │  └─ Llama 70B (Open-weight)      │
    └────┬──────────────────────────────┘
         │
    ┌────▼────────────────┐
    │  Workflow Executor   │
    │  Execute step with   │
    │  selected agent      │
    └────┬─────────────────┘
         │ Execution Result
         │
    ┌────▼──────────────────┐
    │ Feedback Integration   │
    │ • Quality score       │
    │ • Tokens consumed     │
    │ • Time elapsed        │
    │ • Update progress     │
    └──────────────────────┘
```

### Progress State Representation

ProgRouter maintains a **progress state vector** tracking:

```
Progress State = {
  step_index: int,
  completed_steps: int,
  quality_history: [q1, q2, ..., q_{t-1}],  // Quality scores of prior steps
  token_consumption: int,                     // Cumulative tokens used
  time_elapsed: float,                        // Cumulative time used
  budget_remaining: {
    tokens_max: int,
    time_max: float,
    cost_max: float
  },
  task_characteristics: {
    domain: str,  // "code", "reasoning", "writing"
    length: int,  // Number of workflow steps
    complexity: float  // Initial estimate
  }
}
```

### Difficulty Estimation Function

ProgRouter estimates step difficulty based on:

1. **Prior Step Quality:** If previous steps solved cleanly, likely next step is easier
2. **Quality Trends:** Rising quality suggests increasing task difficulty (improvement margin exists); declining suggests problem area
3. **Task Characteristics:** Long workflows often require sustained focus; complex domains may have hard later steps
4. **Budget State:** Approaching budget limits may require difficulty reassessment

$$\text{Estimated Difficulty}_{t} = f(\text{Quality History}, \text{Budget State}, \text{Task Char})$$

### Agent Selection Policy

At each step, ProgRouter selects agent model $m$ to maximize expected quality within budget:

$$\text{Selected Agent} = \arg\max_m \mathbb{E}[\text{Quality}(m) \mid \text{Progress State}]$$

**Constrained by:**
- Time remaining: Does agent latency fit budget?
- Cost remaining: Do agent tokens fit budget?
- Quality threshold: Does agent quality exceed acceptable minimum?

### Quality-Cost Efficiency Frontier

Different models occupy different points on quality-cost curve:

```
Quality
    │
    │  ◆ Frontier Models (GPT-4, Claude Opus)
    │   High quality, high cost
    │
    │  ● Mid-Tier Models (Sonnet, GPT-4o)
    │   Good quality, moderate cost
    │
    │  ▲ Open-Weight Models (Llama, Mistral)
    │   Fast, low cost, variable quality
    │
    ├──────────────────────────────────── Quality Threshold
    │
    └────────────────────────────────────► Cost (tokens/time)
```

ProgRouter dynamically selects along this frontier based on progress state and budget constraints.

## Main Ideas & Contributions

### 1. Online Progress-Guided Routing

The core innovation is routing agent selection in **real-time** based on **actual task progress** rather than static, upfront decisions. This enables:

- **Adaptive Difficulty Response:** Easy steps use cheap agents; hard steps use capable agents
- **Quality-Cost Optimization:** Maximize quality given budget constraints
- **Budget Awareness:** Adjust routing when approaching limits
- **Feedback Integration:** Each step's outcome informs next step's agent selection

### 2. Quality Prediction from Progress History

Rather than treating quality as unpredictable noise, ProgRouter learns to predict when a step will be difficult:

- **Trajectory-Based Prediction:** Quality trends reveal problem structure
- **Domain-Aware Estimation:** Different domains have characteristic difficulty patterns
- **Budget-Aware Thresholds:** When budget is tight, use more capable agents proactively

### 3. Multi-Model Orchestration

ProgRouter treats multi-agent selection as an **optimization problem** rather than a binary decision:

- **Continuous Efficiency Space:** Agents differ along multiple dimensions (quality, cost, speed)
- **Step-Granular Selection:** Optimal agent differs per step, not per task
- **Compositional Quality:** Quality of entire workflow is function of per-step agent choices

### 4. Practical Deployment Framework

ProgRouter provides a **deployable framework** for multi-agent workflows in production:

- **No Training Required:** Progress estimation uses simple heuristics, not learned models
- **Model-Agnostic:** Works with any LLM API (OpenAI, Anthropic, Google, open-weight)
- **Budget-Enforceable:** Hard constraints on time and cost prevent runaway expenses

## Methodology & Implementation

### Experimental Setup

**Benchmark:** Multi-agent workflows across different task types

**LLM Models Tested:**
- Frontier: GPT-4 Turbo, Claude 3.5 Opus, Gemini 2.0 Ultra
- Mid-tier: Claude 3.5 Sonnet, GPT-4o
- Open-weight: Llama 70B, Mistral Large

**Workflow Types:**
- Multi-step code generation
- Complex reasoning and planning
- Long-form writing and summarization

### Comparison Baselines

1. **Single Model (Frontier):** Use GPT-4/Opus for all steps
2. **Single Model (Budget):** Use cheaper model for all steps
3. **Cascade Routing:** Query-level decision (same model for entire workflow)
4. **Random Routing:** Randomly select agent at each step
5. **ProgRouter:** Online progress-guided routing (proposed)

### Evaluation Metrics

- **Quality Score:** Task completion, correctness, user satisfaction (domain-specific)
- **Token Efficiency:** Quality per token (quality/cost ratio)
- **Time Efficiency:** Quality per second
- **Cost:** Total token consumption
- **Budget Adherence:** Percentage of runs completing within budget limits

### Results Summary

**Key Findings (Confirmed from venue acceptance to EMNLP 2026):**

- ProgRouter achieves higher quality-cost efficiency than baselines
- Online routing significantly outperforms static query-level decisions
- Progress-guided estimation enables effective adaptation
- Frontier model selection on hard steps, cheap models on easy steps (Pareto optimal behavior learned automatically)

[Exact figures unavailable — see full paper for complete quantitative results]

### Challenges Addressed

1. **Sparse Feedback:** Only observe quality at step completion; must predict next step difficulty
2. **Budget Uncertainty:** Don't know total workflow cost upfront; must adapt online
3. **Model-Specific Behavior:** Quality of same agent varies across problem types
4. **Latency Constraints:** Frontier models may be slower; time budget may prefer faster agents

## Practical Applications & Use Cases

### 1. Enterprise Code Generation at Scale

**Scenario:** Company deploying multi-agent code generation to thousands of developers

**Challenge:** Frontier model costs are prohibitive; cheap models insufficient for hard tasks

**ProgRouter Solution:** Route easy refactoring/boilerplate to cheap agents; complex architectural changes to frontier models. Automatically optimize within cost budget while maintaining quality.

### 2. Cost-Aware Assistance Services

**Scenario:** SaaS coding assistance service charged per API call

**Challenge:** Different users have different budgets; must balance quality and cost per user

**ProgRouter Solution:** Adapt routing to user's budget constraint. Users with low budgets get reasonable quality from cheaper models; high-budget users get frontier quality.

### 3. Multi-Step Reasoning Systems

**Scenario:** Complex problem requiring planning, reasoning, and execution steps

**Challenge:** Early steps (planning) may be easier; later steps (implementation) require more capability

**ProgRouter Solution:** Allocate budget strategically: cheap agents for planning, expensive agents for complex implementation.

### 4. Research Automation

**Scenario:** Autonomous research agent running hundreds of experiments

**Challenge:** Early experiments may be routine; later experiments may be novel/difficult

**ProgRouter Solution:** Learn difficulty patterns; allocate computation dynamically based on observed task characteristics.

### 5. Real-Time Adaptive Assistance

**Scenario:** IDE assistant helping developer write code in real-time

**Challenge:** Latency constraints; must balance quality and responsiveness

**ProgRouter Solution:** Use fast open-weight agents when latency critical; switch to frontier models for complex reasoning when developer is thinking.

## Insights & Implications

### For Multi-Agent System Design

1. **Static Assignment is Suboptimal:** Assigning same agent to entire workflow ignores within-task difficulty variation

2. **Progress is Informative:** Tracking step-level quality enables predicting future difficulty; exploit this signal

3. **Cost-Quality Tradeoffs are Real:** Different models occupy genuinely different points on Pareto frontier; optimal agent varies by step

4. **Online Adaptation Matters:** Real-time routing significantly outperforms pre-computed decisions

### For Deployment of LLM Systems

1. **Budget Enforcement is Achievable:** Hard constraints on cost/time can be maintained while optimizing quality

2. **Model Diversity is Valuable:** Mixing models of different capabilities enables more efficient resource utilization

3. **Transparency Improves Trust:** Recording which agent executed which step enables auditing and debugging

### Limitations and Open Questions

1. **Difficulty Estimation Accuracy:** Simple heuristics work well; learned models might improve further

2. **Model-Task Interaction:** Quality of agent depends on task type; ProgRouter learns aggregate patterns; specialization possible

3. **Stability and Robustness:** How does ProgRouter behave with new models or unfamiliar task types?

4. **User Control:** Should users be able to override routing decisions or specify model preferences?

### Research Opportunities

- **Learned Difficulty Prediction:** Train difficulty estimators on past task data
- **Multi-Objective Optimization:** Extend beyond quality-cost to include latency, privacy, fairness
- **Hierarchical Orchestration:** Three-tier systems (meta-controller, coordinator, executor)
- **Feedback Learning:** Learn model quality predictions from deployment feedback
- **Hybrid Workflows:** Mix multi-agent orchestration with human-in-the-loop feedback

## Code & Resources

### Official Resources

- **ArXiv:** https://arxiv.org/abs/2608.25992
- **Venue:** Findings of the Association for Computational Linguistics: EMNLP 2026
- **Implementation:** Code and experimental code available on paper's ArXiv page

### Dependencies and Requirements

- **LLM APIs:** Access to multiple LLM endpoints (OpenAI, Anthropic, Google, open-weight via Hugging Face)
- **Workflow Definition:** Framework for defining multi-step workflows (steps, success criteria, parameters)
- **Budget Tracking:** Token counters and cost tracking across LLM calls
- **Metrics Collection:** Quality scoring and efficiency calculation

### Quick-Start Integration

1. **Define Multi-Step Workflow:** List steps with success criteria and difficulty estimates
2. **Setup Agent Pool:** Configure available LLM models with quality/cost/latency profiles
3. **Initialize Progress Tracker:** Create progress state representation
4. **Run ProgRouter Loop:**
   ```
   for each step in workflow:
       estimate_difficulty(progress_state)
       select_agent = router_select(difficulty, budget)
       result = execute_step(agent, step_spec)
       update_progress(result)
       if budget_exhausted: break
   ```
5. **Optimize:** Monitor quality-cost metrics; adjust router thresholds

### Framework Integration

- Compatible with AutoGen, LangChain, Claude Code
- Requires workflow definition abstraction
- Requires budget tracking and quality scoring APIs
- Simple to add to existing multi-agent systems

## Related Work & Context

### Foundational Work

- **Online Learning (Cesa-Bianchi & Lugosi):** Real-time decision-making under uncertainty; theoretical foundation
- **Multi-Armed Bandits:** Sequential decision-making with feedback; related to routing problem
- **Resource Allocation in Distributed Systems:** Classical problem; ProgRouter applies to LLM agents

### Related Agent Orchestration Work

- **AutoGen (Wu et al., 2023):** Multi-agent conversation; ProgRouter adds explicit routing layer
- **Mixture of Experts (Shazeer et al., 2017):** Gate network selects which expert; ProgRouter applies similar idea to agent selection
- **Cost-Aware Model Selection (prior work):** Mostly query-level; ProgRouter adds step-level adaptation

### Related Efficiency and Cost Work

- **Token Budget Optimization:** Prior work on cost-conscious LLM systems; ProgRouter integrates routing
- **Model Scaling Laws (Hoffmann et al.):** Understanding quality-compute tradeoffs; informs agent quality profiles
- **Inference Optimization:** Quantization, distillation, etc.; ProgRouter complements at orchestration level

### Future Research Directions

1. **Learned Routing Policies:** Train routing policies on historical workflow executions
2. **Workflow-Specific Optimization:** Optimize routing for specific workflow types
3. **Multi-Agent Specialization:** Agents develop domain expertise over time; ProgRouter learns specializations
4. **Distributed Workflows:** Coordinate routing across distributed agents with latency constraints
5. **User Preferences:** Incorporate user quality thresholds, ethical preferences into routing

### Connection to Broader LLM Agent Development

- Part of emerging **cost-aware agentic systems** research addressing practical deployment constraints
- Supports development of **scalable multi-agent frameworks** by solving orchestration efficiency problem
- Enables **budget-constrained agentic AI** where capability-cost tradeoffs are explicitly managed
- Contributes to **adaptive agentic architectures** that learn from task progress
- Advances **quality-efficiency engineering** for production LLM systems by formalizing orchestration optimization
