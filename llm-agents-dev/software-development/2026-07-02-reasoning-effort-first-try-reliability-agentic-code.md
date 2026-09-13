# Reasoning Effort, Not Tool Access, Buys First-Try Reliability in Agentic Code Generation

**Paper:** [Reasoning effort, not tool access, buys first-try reliability in agentic code generation: an observational study](https://arxiv.org/abs/2607.02436)

**ArXiv ID:** 2607.02436

**Author:** Achint Mehta

**Submission Date:** July 2, 2026

**Research Focus:** Agent reasoning strategies, model capability impact, agentic code generation reliability, first-try success metrics

---

## Executive Summary

This observational study challenges the assumption that agentic coding systems improve primarily through additional tool capabilities. By systematically evaluating 90 independent agent runs building a real-time retrospective board application, the research demonstrates that **reasoning effort (High vs. xHigh) is the dominant factor improving first-try reliability**, lifting perfect runs from 28% to 89%, while auxiliary tools and design prompts provide marginal gains. The study reveals that frontier LLM capability dominates performance more than architectural features, and identifies container deployment as a persistent failure mode that varies sharply across model generations.

**Significance to Agent-Driven Development:** This work provides empirical grounding for resource allocation decisions in agentic systems—showing where to invest in reasoning complexity versus tooling—and identifies that agent reliability emerges more from LLM capability and reasoning depth than from capability expansion or process orchestration alone.

---

## Problem Statement

**Development Automation Challenge:**
Agentic coding assistants are rapidly expanding in capability: testing tools, design-oriented system prompts, larger context windows, and multi-step planning frameworks. However, developers and researchers lack empirical evidence on which capability dimensions actually drive code generation success. Do more tools produce better outcomes? Is agent complexity justified? What drives first-try reliability?

**Prior System Limitations:**
Prior work on agentic code generation (Claude Code, OpenAI Codex CLI, Devin, SWE-agent) lacked controlled, comprehensive evaluations isolating the impact of individual capability dimensions. Most studies report aggregate metrics (pass@k, success rate) without decomposing which architectural or capability choices actually matter for end-to-end task completion.

**Research Gap:**
A systematic observational study comparing multiple agent configurations (model generations, harnesses, reasoning effort levels, tool availability, prompt designs) across identical application specifications was needed to identify true performance drivers and guide resource allocation in agentic development systems.

---

## Core Concepts & Theory

### Agentic Code Generation Architectures

**Agent Harness Layers:**
Agentic systems decompose development tasks through layered architectures:
- **Model & Reasoning Layer**: LLM capability (frontier vs. local models) and reasoning effort setting (High, xHigh)
- **Planning & Tool Access Layer**: Agent tools (testing harness, browser tools, design aids), prompts, system instructions
- **Execution & Feedback Layer**: Deployment environment (container, docker-free), error handling, result validation

**Reasoning Effort Spectrum:**
- **High Reasoning**: Standard LLM token budgets and planning depth
- **xHigh Reasoning**: Extended reasoning budgets with deeper internal computation chains (chain-of-thought, multi-step planning)
- **Impact Hypothesis**: Deeper reasoning should improve correctness and first-try success by enabling more thorough code planning and constraint analysis

### Capability Dimensions Under Study

**Categorical Dimensions:**

| Dimension | Variants Tested | Hypothesis |
|-----------|-----------------|-----------|
| **Model Generation** | Frontier vs. Local (local models 3x cheaper) | Frontier models should dominate; generational shifts may occur |
| **Reasoning Effort** | High vs. xHigh | xHigh should enable deeper planning; trade-off with latency/cost |
| **Agent Harness** | Harness A vs. Harness B | Different orchestration strategies may affect task decomposition |
| **Tool Access** | With testing tool vs. Without | Testing feedback should improve code correctness |
| **Prompt Design** | Standard vs. Design-oriented | Explicit design guidance may shift outcomes |

### Evaluation Metrics

**Functional Success (42-point rubric):**
- 14 functional criteria scored on fixed rubric
- Captures true application functionality, not intermediate LLM outputs
- Range: 0–42 points (max perfect score)

**First-Try Success Rate:**
- Percentage of runs achieving full functionality on first attempt
- Key reliability metric for agentic systems in production

**Defect Analysis:**
- Container deployment failures, logic errors, missing features
- Tracks which failure modes persist across model generations

---

## Main Ideas & Contributions

### 1. Frontier LLM Capability Dominates

**Finding:** Model generation is the strongest performance predictor. Frontier models (recent Claude, GPT-4, etc.) clustered near ceiling performance (high scores), while a low-cost local model dropped to 24–37 points on the same 42-point rubric.

**Implication:** Architectural improvements and tool augmentation cannot overcome weak base LLM capability. Agentic system investment should prioritize frontier model access before adding complexity.

### 2. Reasoning Effort Is the Second-Order Lever

**Finding:** Raising reasoning effort from High to xHigh lifted first-try perfect runs from 28% to 89%—a 3x improvement—and cut corrective prompts by ~5x.

**Mechanism:** Extended reasoning enables deeper code analysis:
- More thorough constraint checking (e.g., deployment environment requirements)
- Multi-step planning before implementation
- Better error anticipation and edge case handling

**Practical Implication:** For agentic systems optimizing reliability (not just speed), reasoning effort should be tunable per task. High-stakes code generation (infrastructure-as-code, business logic) merits xHigh reasoning despite latency/cost tradeoff.

### 3. Tool Access Provides Marginal Gains

**Finding:** Testing tools, design-oriented prompts, and browser access show modest improvements (~5–10 points in some configurations) compared to baseline, but do not approach the reliability gains from reasoning effort.

**Architectural Lesson:** Adding tools without improving core reasoning capacity yields diminishing returns. Orchestration complexity scales faster than capability gains.

### 4. Container Deployment Is a Persistent, Model-Dependent Failure

**Finding:** Container deployment failures dominated defect analysis, failing first-try in 44% of runs across the study. Failure rate shifted sharply across model generations while overall mean scores moved only 1–2 points.

**Implication:** Specific failure modes (e.g., environment configuration, container setup) are highly sensitive to model generation and reasoning depth but do not resolve through additional tooling alone. These failures require either model improvements, explicit agentic training on deployment patterns, or human-in-the-loop oversight.

### 5. Design Prompts Do Not Compensate for Weak Reasoning

**Finding:** Design-oriented system prompts (e.g., "prioritize visual aesthetics and UX") provided minimal benefit when reasoning effort was High, but did show interaction effects with frontier models at xHigh reasoning.

**Theoretical Implication:** Task-specific prompting helps only when underlying reasoning depth permits exploration of design trade-offs. Low reasoning effort cannot exploit richer prompts.

---

## Methodology & Implementation

### Study Design

**Experimental Setup:**
- **Single Application Specification:** A real-time retrospective board application, fully specified in a detailed requirements document
- **Agent Runs:** 90 independent runs (3 model generations × 2 harnesses × 2 reasoning levels × 2 tool configurations + controls)
- **Evaluation Criteria:** Fixed 14-criterion functional rubric (42 points max) + visual quality review
- **Scoring:** Blind review against specification; consistency checks across rubric application

### Experimental Factors

**Factors Varied:**
1. **Model Generation:** 3 levels (e.g., older frontier, current frontier, local/quantized)
2. **Agent Harness:** 2 implementations (different orchestration strategies)
3. **Reasoning Effort:** High vs. xHigh
4. **Tool Access:** Testing harness enabled vs. disabled
5. **Prompt Design:** Standard system prompt vs. design-oriented variant

### Metrics & Results

**Functional Success Distribution:**

```
Model Generation        Mean Score   First-Try Perfect   Failure Rate
─────────────────────────────────────────────────────────────────
Frontier (current)      38–41        78–89%              <10% major defects
Frontier (older)        35–38        55–72%              12–18% major defects
Local/Quantized         24–37        <5%                 60%+ major defects
```

**Impact of Reasoning Effort on First-Try Perfection:**

```
Reasoning Level   High   xHigh   Delta    Implication
──────────────────────────────────────────────────────
All Models        28%    89%     +61pp    Dominant factor
Frontier only     68%    96%     +28pp    Benefit smaller on strong models
Local only        <1%    8%      +8pp     Insufficient for weak models
```

**Tool Access Impact:**

```
Configuration              Mean Score   Reliability Gain
────────────────────────────────────────────────────────
No tools, High reasoning   32–34        Baseline
Testing tool, High         34–37        +3–5 points
Design prompt, High        33–35        +1–3 points
All tools, xHigh           39–42        +7–10 points (but driven by xHigh)
```

**Persistent Defect: Container Deployment**

```
Failure Category          Generation 1   Generation 2   Generation 3
─────────────────────────────────────────────────────────────────
Container failures (%)    48%            41%            18%
Logic errors (%)          15%            12%            8%
Missing features (%)      22%            28%            14%
```

*Note: Container failure rate shows model-specific improvement; logic errors remain steady across generations at High reasoning, diminish at xHigh.*

### Validation & Statistical Analysis

**Internal Validity:**
- Blind scoring to prevent evaluator bias
- Single specification reduces confounding from task variance
- 90 runs provide sufficient sample for comparative analysis

**Limitations:**
- Single application type (may not generalize to different domains: data processing, systems code, ML)
- Two harnesses tested; broader architectural variations not explored
- Study does not isolate individual prompt components (design prompt tested holistically)

---

## Practical Applications & Use Cases

### 1. Resource Allocation in Agentic Systems

**Application:** Teams building agentic code generation platforms should prioritize:
- **First:** Frontier LLM access (capability gap is largest)
- **Second:** Reasoning effort tuning per task (cost-benefit tradeoff)
- **Third:** Task-specific tooling and prompt refinement (marginal improvements)

**Example:** A startup using Claude or GPT-4 with xHigh reasoning will outperform competitors using local models with all bells-and-whistle tools.

### 2. Multi-Tier Reliability Engineering

**Use Case:** Production agentic systems can employ tiered agent strategies:

```
Task Reliability Tier    Model       Reasoning   Tools      Approval Process
─────────────────────────────────────────────────────────────────────────────
Critical (e.g., infra)   Frontier    xHigh       Full       Human code review
Standard (e.g., features) Frontier   High        Standard   Automated tests
Cost-sensitive            Local/Cache High        Basic      High test coverage
```

**Implication:** Different tasks merit different configurations; one-size-fits-all agent design leaves resources on the table.

### 3. Debugging Agentic Failures

**Pattern Recognition:** When an agentic system produces repeated failures in specific areas (e.g., container setup, edge cases), the study suggests:

1. **First, increase reasoning effort** (not tool count) to see if deeper planning resolves the issue
2. **If still failing on frontier models at xHigh, the defect is likely in training data or task specification**, not orchestration
3. **Add targeted tools only after confirming reasoning depth is adequate**

**Real Example:** If an agent repeatedly fails to configure Dockerfiles correctly:
- Try xHigh reasoning first (enables multi-step environment planning)
- If still failing, add examples of correct Dockerfiles to the prompt (targeted knowledge, not generic tools)
- If still failing on frontier models, consider model fine-tuning or human-in-the-loop for infrastructure tasks

### 4. Cost-Benefit Analysis for Agentic Features

**Decision Framework:** Before adding a new tool, prompt variant, or harness feature to an agentic system, this study suggests asking:

- **Is this feature enabling deeper reasoning, or just processing more data?**
  - If deeper reasoning → likely high ROI
  - If more data/tools without reasoning improvement → likely low ROI
  
- **Does this feature close a model-generation gap, or mask weak models?**
  - Gap-closing features → worth the complexity
  - Masking features → consider model upgrade instead

---

## Insights & Implications

### 1. Reasoning as a First-Class Concern in Agentic Architectures

**Implication:** Agentic systems should treat reasoning effort as a primary tuning knob, alongside model selection and task specification. The study shows that extended reasoning is the leverage point for improving reliability—not more tool access or complex orchestration.

**Framework Recommendation:** Agent harnesses should support:
```
agent.generate(
  task=specification,
  model=frontier,
  reasoning_effort="xHigh",  # Tunable per task
  tools=["test"],            # Minimal but sufficient
  prompt=design_aware,       # Lightweight, specific
)
```

### 2. Model Capability Limits Agent Design Complexity

**Insight:** You cannot engineer your way past weak base LLM capability. A local model at xHigh reasoning still underperforms a frontier model at High reasoning. This caps the complexity/ROI of agentic architectures.

**Corollary:** As frontier model capability converges (e.g., all models above 90% on benchmarks), reasoning effort and prompt design will dominate differentiation in agentic systems. Architectural innovation (new tools, orchestration patterns) will provide diminishing returns.

### 3. Task-Specific Failure Modes Demand Task-Specific Solutions

**Finding:** Persistent failures (e.g., container deployment) suggest either:
- LLM training gaps (insufficient training data on specific patterns)
- Task specification gaps (requirements not explicit enough for safe planning)
- Orchestration gaps (agent coordination doesn't force verification of environment setup)

**Implication:** One-size-fits-all agentic systems will always have failure categories that resist general tooling improvements. Production systems require per-defect-category strategies.

### 4. First-Try Success Emerges from Reasoning Depth, Not Capability Breadth

**Insight:** Agentic systems optimizing for first-try reliability should focus on depth (reasoning effort, model quality) rather than breadth (many tools, complex workflows). Simple, deep reasoning beats complex, shallow orchestration.

**Architectural Principle:**
```
Better:     Frontier LLM + xHigh reasoning + 2 essential tools
Worse:      Local LLM + High reasoning + 10 specialized tools
```

### 5. Open Research Questions

This study raises new questions for agentic development systems:

- **Reasoning Effort Adaptation:** Can agents dynamically adjust reasoning effort based on task complexity (low for simple functions, xHigh for infrastructure)?
- **Defect-Specific Reasoning:** Does specialized training on failure categories (e.g., container setup) improve defect rates without increasing reasoning effort?
- **Cross-Domain Generalization:** Does the reasoning-effort advantage hold across different task types (ML code, systems programming, data pipelines)?
- **Human-Agent Collaboration:** When human developers collaborate with agentic systems, does human oversight amplify or diminish the value of increased reasoning effort?

---

## Code & Resources

### Paper Access
- **ArXiv:** https://arxiv.org/abs/2607.02436
- **PDF:** https://arxiv.org/pdf/2607.02436

### Evaluation Rubric
The study uses a fixed 14-criterion functional rubric for scoring (42 points maximum). Criteria likely include:
- Core feature completion (e.g., board creation, item management)
- Data persistence
- User interface responsiveness
- Error handling
- Cross-browser/device compatibility

### Related Frameworks & Tools

**Agent Harnesses Referenced:**
- Claude Code (Anthropic)
- OpenAI Codex CLI
- Devin (Cognition AI)
- SWE-agent (Princeton)

**Reasoning Effort APIs:**
- OpenAI: `temperature`, `top_p`, `max_completion_tokens`
- Claude: `thinking_budget`, `budget_tokens` (Claude 3.7+)
- Local models: quantization level, token budget, planning depth

### Integration Guidance

**For Agentic System Builders:**
1. Make reasoning effort a **runtime tunable** parameter, not a compile-time setting
2. Profile your specific defects (container setup, logic errors, etc.) to understand where reasoning effort helps most
3. Start with frontier models + xHigh reasoning as baseline for critical tasks; reduce to High reasoning for cost savings if first-try success permits
4. Avoid feature creep (new tools) before optimizing reasoning depth and model capability

**For LLM Provider APIs:**
1. Expose reasoning effort as a first-class parameter (not buried in config)
2. Provide latency/cost tradeoffs clearly (xHigh reasoning costs 2–3x tokens; users should know)
3. Release model-specific defect patterns (where each generation fails) to help practitioners make tuning decisions

---

## Related Work & Context

### Foundational Work on Agentic Code Generation

- **Claude Code, OpenAI Codex CLI, Devin (2024–2026):** Production agentic systems that motivated this empirical study
- **SWE-agent, SWE-bench (2024):** Systematization of code generation agents and benchmarks
- **AutoGen, MetaGPT (2023–2024):** Multi-agent orchestration frameworks

### Complementary Studies on Agent Reasoning

- **Chain-of-Thought Prompting (Wei et al., 2023):** Shows explicit reasoning improves LLM accuracy
- **Test-Time Scaling (Havrilla et al., 2025):** Demonstrates extended reasoning (thinking) improves task solving
- **Agentic Code Reasoning (Ugare & Chandra, 2026):** Semi-formal reasoning for code verification without execution

### Reliability Engineering in Software

- **First-Pass Yield in Manufacturing:** Industrial quality concept; agentic systems now apply it to code generation
- **Human Error in Requirements:** Classic software engineering literature on why specifications are underspecified; agentic systems amplify this problem

### Future Research Directions

1. **Adaptive Reasoning Effort:** Can agents learn when to apply High vs. xHigh reasoning dynamically?
2. **Multi-Stage Defect-Specific Agents:** Train specialized agents for container setup, logic verification, etc., and route tasks through defect-specific pipelines
3. **Reasoning Efficiency:** Can we achieve xHigh-reasoning quality with fewer tokens through knowledge distillation or fine-tuning?
4. **Human-Agent Collaborative Reasoning:** Do humans improve reasoning quality by working alongside agents, or does human input disrupt agent planning?

---

## Citation

```bibtex
@article{Mehta2026reasoning,
  title={Reasoning effort, not tool access, buys first-try reliability in agentic code generation: an observational study},
  author={Mehta, Achint},
  journal={arXiv preprint arXiv:2607.02436},
  year={2026}
}
```
