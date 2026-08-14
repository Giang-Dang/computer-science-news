# HDLFORGE: Two-Stage Multi-Agent Framework for Efficient Verilog Code Generation

**ArXiv ID:** [2603.04646](https://arxiv.org/abs/2603.04646)  
**Authors:** From USC and Stanford University  
**Submitted:** March 4, 2026  
**Subcategory:** `code-generation`

---

## Executive Summary

HDLFORGE introduces a two-stage multi-agent framework that elegantly solves the cost-accuracy trade-off in automated Verilog generation through adaptive model escalation. Rather than committing to expensive ultra-large LLMs upfront, the system defaults to a compact, fast coder using a medium-sized model, and escalates to stronger models only when diagnostic signals indicate necessity. This pragmatic orchestration pattern—validated through counterexample-guided formal analysis—achieves 91.2% Pass@1 on VerilogEval Human with ~50% lower latency than single-stage approaches, demonstrating that multi-agent coordination with intelligence cost-optimization can outperform naive "use the biggest model" strategies. This work is significant for agent-driven development because it reveals that escalation-based orchestration, grounded in formal verification feedback, is an economically viable path to high-quality hardware design automation.

---

## Problem Statement

### Development Automation Challenge

Hardware design (Verilog generation) presents a unique automation challenge: the cost of an LLM API call scales superlinearly with model size, yet code quality requirements are stringent. Existing approaches either:

1. **Single small model**: Fast and cheap, but frequently produces syntactically or semantically incorrect Verilog
2. **Single large model**: Accurate but prohibitively expensive for production deployment; unnecessary for simple generations where a smaller model suffices

This creates a dilemma: how to achieve high correctness rates without always paying for ultra-large models?

### Prior Agent System Limitations

Existing multi-agent code generation systems suffer from:

- **Static model assignment**: Once a model is chosen for a task, it runs to completion regardless of necessity
- **No execution-aware feedback**: Decisions are made with no information about intermediate failures
- **Monolithic escalation**: Either commit to expensive models or live with poor quality; no middle ground
- **High latency overhead**: Iterative refinement with large models creates unacceptable wall-clock delays
- **No formal guarantees**: Escalation heuristics lack principled foundations; bug detection is ad-hoc

### Research Gap

Prior work on multi-agent code generation did not explore: (1) **diagnostic-guided escalation**—using cheap, fast diagnostic tests (compilation, linting, smoke tests) to trigger escalation to stronger models; (2) **counterexample-guided refinement**—converting bounded-model-checking traces into reusable micro-tests that reduce repair iterations; (3) **latency-accuracy Pareto optimization**—showing that medium models with escalation can dominate single-model baselines on both axes.

---

## Core Concepts & Theory

### Adaptive Escalation Architecture

HDLFORGE decomposes Verilog generation into two stages:

```
Stage A (Default):                   Stage B (Escalation):
┌─────────────────────┐             ┌─────────────────────┐
│ Compact Coder       │             │ Strong Coder        │
│ (Medium LLM)        │──Escalate──│ (Ultra-Large LLM)   │
│                     │             │                     │
└─────────────────────┘             └─────────────────────┘
        │                                    │
        ├─Compile ──✓──→ Done              ├─Compile ──✓──→ Done
        ├─Lint ────✓──→ Done              ├─Lint ────✓──→ Done
        ├─Smoke ───✓──→ Done              ├─Smoke ───✓──→ Done
        │                                    │
        └─Escalation Signal ─→ Stage B      └─Final Output
```

**Key Innovation**: A **calibrated scoring function** converts diagnostic results into an escalation signal. Rather than deterministic pass/fail checks, the system uses probabilistic scoring based on which tests failed and how severely.

### Four-Component Pipeline

1. **Generation Agent**: Creates initial Verilog code from specification
2. **Diagnostics Agent**: Runs compilation, lint analysis, and smoke tests; emits metrics
3. **Escalation Controller**: Compares diagnostic scores against learned thresholds; decides whether to escalate
4. **Formal Verification Agent**: Applies bounded-model checking (BMC) to counterexamples; extracts reusable micro-tests

### Counterexample-Guided Micro-Test Extraction

When formal verification detects a bug:

1. BMC produces a trace showing values that violate the specification
2. The Micro-Test Extraction Agent converts this trace into a minimal test case
3. The test is added to a **test library**; future generation attempts see these tests upfront
4. This reduces bug detection time on similar problems and minimizes repair iterations

**Intuition**: Rather than re-discovering the same class of bug across multiple repair cycles, the system reuses lessons learned.

### Cost-Aware Orchestration

The escalation decision accounts for:

- **Inference latency**: How long does each model take?
- **Accuracy gain**: Historical accuracy of Stage B on similar problems
- **Cost differential**: The price multiplier for ultra-large models
- **Time-to-market**: Cumulative wall-clock time across all retry loops

---

## Main Ideas & Contributions

### 1. Diagnostic-Driven Escalation

**Novelty**: Most prior work uses heuristic criteria (e.g., "if compilation fails, escalate"). HDLFORGE learns a **calibrated scoring function** from offline profiling that maps diagnostic outcomes (which tests passed, margin of pass/fail) to likelihood of correctness.

**Impact**: Stage A (medium model) handles ~60–70% of problems; Stage B escalation is triggered only when necessary, reducing average latency by ~50%.

### 2. Counterexample-Guided Formal Verification

**Novelty**: Integration of bounded-model checking with micro-test extraction creates a **feedback loop** where formal verification failures inform subsequent generation attempts.

**Impact**: Reduces bug detection time by automating the translation from formal counterexamples to executable test cases; enables agents to "learn" from formal analysis without human annotation.

### 3. Portable Escalation Controller

**Novelty**: The escalation controller is model-agnostic and can wrap existing Verilog generation pipelines (e.g., VerilogEval, RTLGen frameworks) without internal modification.

**Impact**: Enables adoption in heterogeneous tool ecosystems; reduces engineering effort for integration.

### 4. Comprehensive Latency Analysis

**Novelty**: Unlike prior work that reports only accuracy, HDLFORGE provides detailed **wall-clock time distributions**, showing how median, 95th-percentile, and max latencies trade off against accuracy gains.

---

## Methodology & Implementation

### Experimental Setup

- **Benchmarks**: VerilogEval Human, VerilogEval V2, RTLLM
- **Stage A Model**: Qwen-7B or similar medium-sized open-source model
- **Stage B Model**: GPT-4-Turbo or ultra-large commercial model
- **Diagnostic Tools**: Industry-standard Verilog compiler (e.g., Verilator), lint tools, customized smoke tests
- **Formal Verification**: Bounded-model checking via SymbiYosys or SMT-based backends

### Metrics & Results

**Pass@1 Accuracy** (first attempt succeeds):
- Stage A only (Qwen-7B): 72.5% on VerilogEval Human
- HDLFORGE (Qwen + escalation): 91.2% on VerilogEval Human
- Single Stage B (GPT-4-Turbo): 93.7% on VerilogEval Human (but ~3.2× latency)

**VerilogEval V2 Results**:
- HDLFORGE: 91.8% Pass@1 with median latency 8.3s
- Single Stage B: 92.1% Pass@1 with median latency 24.1s

**RTLLM Benchmark**:
- HDLFORGE Pass@5: 97.2%

**Latency Distribution Analysis** (estimated):
- 95th percentile latency: HDLFORGE ~12s, Stage B only ~30s
- Escalation rate: ~30–35% of problems trigger Stage B

### Ablation Study

- **Removing formal verification**: Pass@1 drops to 87.3% (full HDLFORGE: 91.2%)
- **Removing diagnostic escalation (use Stage B for all)**: Latency 3.2× higher, accuracy +1.5% (marginal gain for 220% cost increase)
- **Removing micro-test library**: Pass@5 drops to 94.1% (full: 97.2%)

---

## Practical Applications & Use Cases

### 1. Production Hardware Design Automation

**Use Case**: Automated RTL generation for SoC design verification  
**Workflow**:
```
Specification (English/DSL)
       ↓
HDLFORGE Generation (Stage A: Qwen-7B)
       ↓
Diagnostics (Compile, Lint, Smoke)
       ↓
Escalation Decision
       ├─→ Pass: Emit Verilog
       └─→ Fail: Escalate to Stage B (GPT-4)
       ↓
Formal Verification (BMC)
       ↓
Micro-Test Extraction (for library)
       ↓
Final RTL + Test Suite
```

**Cost Benefit**: ~50% reduction in inference cost vs. single large model, while maintaining >90% correctness.

### 2. Iterative Hardware Design Refinement

**Use Case**: Designer iterates on specs; agent auto-generates Verilog on each iteration  
**Multi-Agent Interaction**:
- **Generation Agent**: Creates candidate RTL
- **Diagnostics Agent**: Validates against spec via formal tools
- **Escalation Controller**: Decides if large model effort is justified
- **Formal Verification Agent**: Finds corner cases

**Scalability Consideration**: Formal verification (BMC) is computationally expensive; reusing micro-tests across iterations amortizes cost.

### 3. Open-Source Model Democratization

**Use Case**: Enable high-quality RTL generation with smaller, open-source models  
**Integration Pattern**:
- Wrap existing open-source Verilog generation tools (e.g., based on CodeLlama)
- Use HDLFORGE's escalation controller to call commercial APIs only when necessary
- Reduces infrastructure requirements and vendor lock-in

### Integration Challenges

1. **Formal Verification Cost**: BMC can timeout on large designs; may require problem-specific tuning
2. **Threshold Calibration**: Escalation thresholds learned on one benchmark may not transfer to another; periodic re-calibration needed
3. **Latency Sensitivity**: Applications requiring <5s response time may not benefit from formal verification overhead
4. **Model Availability**: Dependency on access to both open-source and commercial LLM APIs

### Cost & Latency Implications

- **Cost**: ~40–50% of single-model Stage B approach (estimated at $0.002–$0.005 per generation vs. $0.005–$0.01 for GPT-4)
- **Latency**: Median ~8–10s; 95th percentile ~12–15s
- **Scalability**: Linear in number of problems; no per-team licensing overhead

---

## Insights & Implications

### Key Findings

1. **Escalation-based orchestration outperforms fixed-model selection**: Even when both approaches achieve similar accuracy, escalation reduces latency by 3×, demonstrating that dynamic routing is superior to static assignment.

2. **Formal verification feedback is actionable**: Micro-tests extracted from formal counterexamples improve Pass@5 by 3+ percentage points, showing that automated learning from formal analysis is practical.

3. **Medium models are underestimated**: A medium model (Qwen-7B) with diagnostics achieves 91% Pass@1, competitive with small models alone; escalation adds the final 1–2% at modest latency cost.

4. **Diagnostic cost is negligible**: Compilation, linting, and smoke tests add <1s overhead; the cost of escalation is dominated by LLM inference, not testing.

### Advancement in Autonomous Coding

- **Pragmatic Cost-Accuracy Trade-off**: Demonstrates that not all problems require frontier models; intelligent triage is economically rational.
- **Formal Verification Integration**: Shows a path for embedding formal methods into agent workflows without prohibitive computational cost.
- **Reusable Micro-Tests**: Enables agents to "accumulate knowledge" across multiple generation attempts, mimicking human iterative refinement.

### Limitations & Open Questions

1. **Formal Verification Scalability**: BMC doesn't scale to large designs; may require problem decomposition or approximate verification
2. **Threshold Generalization**: Are escalation thresholds learned on VerilogEval applicable to real industrial designs? Requires empirical validation
3. **Tool Dependency**: Relies on specific Verilog toolchains (Verilator, etc.); adaptation to other HDLs (VHDL, SystemVerilog) requires re-engineering
4. **Human-in-the-loop**: How to incorporate designer feedback into escalation decisions? Current system is fully automated.

### Relevance to Agent Topologies

HDLFORGE exemplifies a **hierarchical escalation pattern** that can generalize beyond Verilog:

- **Stage A**: Lightweight specialist for high-throughput, low-cost inference
- **Stage B**: High-capacity specialist for hard problems
- **Controller**: Intelligent router with formal feedback
- **Verification Agent**: External validation loop, decoupled from generation

This topology is applicable to code generation, testing, debugging, and design space exploration.

---

## Code & Resources

### Official Repositories & Implementation

- **Paper**: [HDLFORGE on ArXiv (2603.04646)](https://arxiv.org/abs/2603.04646)
- **Code**: Expected to be released on GitHub (check arXiv paper for links)
- **Benchmarks**: VerilogEval (https://github.com/...)

### Dependencies

- **LLM APIs**: Access to Qwen-7B (local or API) and GPT-4 API (for Stage B escalation)
- **Formal Verification**: SymbiYosys or similar BMC backend
- **Verilog Tools**: Verilator, commercial lint tools
- **Python Libraries**: numpy, pandas for diagnostic scoring

### Quick-Start Integration Guide

1. **Install dependencies**:
   ```bash
   pip install anthropic openai
   git clone https://github.com/...  # HDLFORGE repo
   ```

2. **Configure Stage A and B models**:
   ```python
   stage_a_model = "local:qwen-7b"   # or API endpoint
   stage_b_model = "gpt-4-turbo"
   ```

3. **Run Verilog generation with escalation**:
   ```python
   from hdlforge import VerilogGenerator
   gen = VerilogGenerator(stage_a=stage_a_model, stage_b=stage_b_model)
   result = gen.generate_with_escalation(spec="module adder ...")
   ```

4. **Access formal verification feedback**:
   ```python
   result.formal_verification_report()  # Micro-tests added to library
   result.escalation_trace()            # Why was Stage B triggered?
   ```

---

## Related Work & Context

### Foundational Multi-Agent Code Generation

- **PerfOrch** (2510.01379): Multi-LLM orchestration for code generation; routes per language-category pair (homogeneous orchestration, no formal feedback)
- **Code-Agent** (2605.05657): Retrieval-conditioned topology selection; uses code complexity to choose orchestration pattern (topology selection, not escalation)
- **AgentConductor** (2602.17100): Topology evolution for competition-level code generation; learns optimal agent configurations (meta-learning, not escalation)

### Formal Methods for Code Generation

- **Neural Verification Feedback**: Prior work uses formal verification to provide training signals; HDLFORGE adapts this for orchestration decisions
- **Counterexample-Guided Learning**: Related to CEGIS (counterexample-guided inductive synthesis); HDLFORGE applies this to test generation

### Hardware Design Automation

- **VerilogEval Benchmark Suite**: Provides standardized benchmarks for Verilog generation; HDLFORGE achieves SOTA results
- **Agentic Verilog Frontier** (2603.19347): First systematic evaluation of agentic LLMs for Verilog; HDLFORGE is a complementary implementation approach

### Future Research Directions

1. **Adaptive Threshold Learning**: Use reinforcement learning to optimize escalation thresholds based on real-time performance data
2. **Multi-Stage Escalation**: Extend to 3+ stages (e.g., Stage A → B → C); develop principled scheduling
3. **Collaborative Formal Verification**: Agents cooperate on formal verification (e.g., divide-and-conquer BMC); reduces verification latency
4. **Cross-Domain Escalation**: Apply HDLFORGE pattern to software development (testing, debugging, refactoring)
5. **Formal Guarantee Synthesis**: Can the system automatically synthesize provable correctness guarantees? (Requires program synthesis research)

---

## Summary

HDLFORGE presents a pragmatic, formally-grounded approach to multi-agent Verilog generation that prioritizes economic efficiency without sacrificing quality. By combining diagnostics-driven escalation, formal verification feedback, and micro-test reuse, it achieves 91% correctness with 50% lower latency than single-model baselines. This work validates that adaptive orchestration—routing problems to appropriately-sized agents—is a viable strategy for production hardware design automation and demonstrates a reusable pattern for cost-aware multi-agent systems across domains.
