# HDLFORGE: A Two-Stage Multi-Agent Framework for Efficient Verilog Code Generation with Adaptive Model Escalation

**ArXiv ID:** [2603.04646](https://arxiv.org/abs/2603.04646)  
**Authors:** Armin Abdollahi, Saeid Shokoufa, Negin Ashrafi, Mehdi Kamal, Massoud Pedram  
**Institutions:** University of Southern California, Stanford University  
**Submission Date:** March 4, 2026  
**Focus Area:** Hardware Code Generation, Multi-Agent Orchestration, Model Escalation

---

## Executive Summary

HDLFORGE introduces a pragmatic two-stage multi-agent framework for hardware description language (Verilog) code generation that dynamically escalates model capacity based on generation difficulty. By combining efficient medium-sized models with powerful large models only when necessary, HDLFORGE achieves 91.2% Pass@1 on VerilogEval with 50% lower latency than baseline approaches. The system represents a significant advancement in cost-aware multi-agent orchestration for specialized code generation domains.

---

## Problem Statement

Hardware code generation with LLMs presents unique challenges that distinguish it from general software development:

- **Specification Complexity:** Verilog specifications require strict adherence to hardware semantics, timing constraints, and synthesis correctness that cannot be easily verified at runtime like application code.
- **Latency vs. Accuracy Trade-off:** Larger models (GPT-4o, ultra-large variants) achieve higher accuracy but incur significant inference costs and latency penalties unsuitable for iterative development.
- **Verification Bottleneck:** Hardware designs require formal verification and synthesis testing to detect subtle bugs in logic, timing, and resource utilization—traditional debugging feedback loops are expensive.
- **Generalization Gap:** Medium-sized models (7B parameters) struggle with complex specifications, yet using large models exclusively is computationally prohibitive at scale.
- **Prior Limitations:** Existing approaches either default to expensive large models or accept high error rates from smaller models without adaptive fallback mechanisms.

HDLFORGE addresses this by introducing **staged, evidence-driven model escalation**—a principled approach to decide when to invest in larger model capacity based on diagnostic signals rather than static model selection.

---

## Core Concepts & Theory

### Multi-Agent Architecture with Staged Escalation

HDLFORGE decomposes Verilog generation into two coordinated stages, each with specialized agents:

**Stage A (Default Execution):**
- Agent: Compact Coder with medium-sized LLM (e.g., Qwen-7B, Qwen-14B)
- Role: Fast, resource-efficient initial code generation
- Cost: Low inference latency and compute
- Target: Most specifications (estimated 60-70% of tasks)

**Stage B (Escalation Execution):**
- Agent: Powerful Coder with ultra-large LLM (e.g., GPT-4o, Qwen-32B)
- Role: High-accuracy generation for complex or previously failed specifications
- Cost: High inference cost, reserved for difficult cases
- Trigger: Diagnostic signals indicate Stage A solution insufficient

### Diagnostic Assessment Layer

The framework incorporates a **Calibrated Diagnostic Module** that evaluates Stage A outputs without requiring full synthesis or formal verification:

1. **Compilation Check:** Verilog syntax validation
2. **Lint Analysis:** Code quality and potential issues (unused variables, undefined nets)
3. **Smoke Tests:** Lightweight functional simulation on simple test vectors
4. **Counterexample-Guided Feedback:** Formal model-checking traces converted into micro-tests for repair

These diagnostics are inexpensive and provide rapid signal for escalation decisions.

### Counterexample-Guided Formal Agent

A novel contribution is the formal verification agent that:
- Performs bounded model checking on generated Verilog
- Extracts counterexamples from failed verification runs
- Converts counterexamples into reusable test vectors (micro-tests)
- Significantly reduces iteration cycles by providing specific repair guidance

This closes the loop between verification and repair without expensive re-running of synthesis.

### Escalation Decision Policy

The escalation controller uses a **calibrated scoring function** that combines:
- Compilation success/failure status
- Lint violation counts and severity
- Smoke test pass/fail results
- Formal verification trace feedback

Decision rule: If combined diagnostic score exceeds threshold, escalate to Stage B. Otherwise, accept Stage A result or request repair within Stage A.

---

## Main Ideas & Contributions

### 1. **Adaptive Two-Stage Orchestration**
   - First contribution: A practical framework that separates "fast but good enough" (Stage A) from "slow but accurate" (Stage B) codegens.
   - Insight: Not all specifications are equally difficult; proportional resource allocation yields better cost-quality trade-offs than static model selection.
   - Benefit: Achieves GPT-4o-level accuracy with 40-50% reduced latency and lower cost due to Stage A handling majority of cases.

### 2. **Portable Escalation Controller**
   - The escalation mechanism is decoupled from the underlying coder implementations.
   - Can wrap existing Verilog LLM pipelines (AutoVCoder, MAGE, CooperativeV) without internal modifications.
   - Enables incremental deployment and compatibility with legacy systems.

### 3. **Counterexample-Guided Repair Integration**
   - Extracts concrete failure traces from formal verification runs.
   - Converts bounded-model-checking counterexamples into targeted micro-tests.
   - Dramatically reduces bug repair iterations (estimated 40-60% fewer attempts needed).
   - More effective than generic retry-based approaches because feedback is problem-specific.

### 4. **Calibrated Diagnostic Heuristics**
   - Inexpensive compilation, lint, and smoke test signals serve as proxy for escalation decision.
   - Empirically calibrated thresholds derived from development set performance.
   - Avoids expensive formal verification in early screening while maintaining decision quality.

---

## Methodology & Implementation

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│             Input Specification (Natural Language)       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────────┐
         │  Stage A: Compact Coder   │
         │   (Medium LLM, e.g. 7-14B)│
         └────────────┬─────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │  Diagnostic Assessment   │
         │  - Compilation Check     │
         │  - Lint Analysis         │
         │  - Smoke Tests           │
         └────────┬─────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
     [Pass]             [Escalate]
        │                   │
        ▼                   ▼
    [Output]    ┌──────────────────────────┐
                │  Stage B: Powerful Coder  │
                │  (Ultra-large LLM, e.g.   │
                │   GPT-4o, Qwen-32B)       │
                └────────────┬─────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │  Formal Verification     │
              │  & Counterexample Extact │
              └────────────┬─────────────┘
                           │
                    [Repair Guidance]
                           │
                           ▼
                    ┌───────────────┐
                    │ Final Output  │
                    └───────────────┘
```

### Implementation Details

**Stage A Coder:**
- Uses instruction-tuned medium-sized LLM
- Prompt engineering optimized for Verilog style and patterns
- Few-shot examples from high-quality Verilog repositories
- Temperature tuning for consistency vs. diversity balance

**Escalation Controller:**
- Runs diagnostic checks on generated Verilog
- Scoring function: `score = f(compilation_pass, lint_count, test_pass_rate, formal_traces)`
- Threshold calibration via validation set performance
- Time-budget aware (escalates if Stage A latency budget exceeded)

**Stage B Coder:**
- Inherits same prompting structure but with larger model capacity
- Access to Stage A generated code as reference (in-context learning)
- Diagnostic feedback from Stage A failures incorporated into prompt
- Formal verification loop integrated

**Formal Verification Integration:**
- Uses bounded model checking with timeouts (typically 30-60s per property)
- Counterexample extraction via SMT solver (Z3)
- Micro-test generation: for each counterexample, create minimal test case exposing failure
- Test-driven repair: Stage B regenerates code given micro-tests as guidance

### Datasets & Benchmarks

1. **VerilogEval Human:** 156 hand-crafted specifications from hardware engineers
2. **VerilogEval V2:** Larger benchmark with diverse difficulty levels
3. **RTLLM:** Hardware design competition benchmark with complex specifications
4. **Internal Dataset:** Proprietary USC/Stanford RTL design tasks for calibration

### Experimental Setup

**Baselines:**
- Stage A only (compact model baseline)
- Stage B only (expensive large model baseline)
- AutoVCoder (prior work on Verilog generation)
- MAGE (multi-agent generation)
- CooperativeV (cooperative framework)

**Metrics:**
- Pass@1: Percentage of correct solutions on first attempt
- Pass@5: Percentage with correct solution within 5 attempts
- Latency: Median end-to-end inference time
- Cost: Relative API/compute cost compared to baselines

---

## Results & Performance

### Quantitative Results

**HDLFORGE-Qwen (Medium Model Variant):**
| Benchmark | Pass@1 | Pass@5 | Median Latency | Relative Cost |
|-----------|--------|--------|-----------------|---------------|
| VerilogEval Human | 91.2% | 96.4% | -50% vs GPT-4o | ~30% of GPT-4o |
| VerilogEval V2 | 91.8% | 96.8% | -48% | ~32% of GPT-4o |
| RTLLM | 97.2% | 99.1% | -52% | ~25% of GPT-4o |

**HDLFORGE-GPT-4o (Ultra-Large Model Variant):**
| Benchmark | Pass@1 | Pass@5 | Comparative to SOTA |
|-----------|--------|--------|---------------------|
| VerilogEval Human | 95.5% | 99.2% | +0.6% vs CooperativeV |
| VerilogEval V2 | 96.8% | 99.4% | +0.8% vs CooperativeV |
| RTLLM | 99.8% | 100% | Matches SOTA |

### Stage A vs Stage B Escalation Rate

- Percentage of specifications handled by Stage A: 68-72% across benchmarks
- Escalation rate: 28-32% requiring Stage B escalation
- Of escalated cases, 91% passed with Stage B alone (minimal re-escalation)

### Counterexample-Guided Repair Effectiveness

- Average iterations to fix bugs: 1.3 with counterexample-guided repair vs 4.2 with standard retry
- Repair success rate: 87% of failed specifications fixed via micro-tests without escalation
- Formal verification time: ~45s per specification (within practical synthesis workflow)

### Comparison with Baselines

**AutoVCoder (7B):**
- Pass@1: 48.5% (VerilogEval Human) → HDLFORGE: +42.7pp

**CodeV (14B):**
- Pass@1: 53.2% (VerilogEval Human) → HDLFORGE: +38.0pp

**OriGen (7B):**
- Pass@1: 54.4% (VerilogEval Human) → HDLFORGE: +36.8pp

**MAGE (Baseline):**
- Pass@1: 88.3% → HDLFORGE: +2.9pp with same model size

**Inference Efficiency:**
- HDLFORGE-Qwen provides 91.2% accuracy at 50% lower latency than GPT-4o baseline
- Cost per specification: Stage A avg ~$0.08, Stage B avg ~$0.32, blended avg ~$0.12 (vs GPT-4o flat $0.25)

---

## Practical Applications & Use Cases

### 1. **Hardware Design Automation at Scale**
   - Chip design teams can generate RTL from high-level specifications at lower cost
   - Parallel generation of multiple design candidates with cost-aware allocation
   - Integration into continuous hardware deployment pipelines

### 2. **EDA Tool Integration**
   - Portable escalation controller wraps existing RTL generation tools (Vivado, Synopsys)
   - Diagnostic module integrates with existing lint/synthesis toolchains
   - No modification required to legacy tool infrastructure

### 3. **Interactive Hardware Development**
   - Rapid prototyping: Stage A provides fast feedback loop for iterative design
   - Complex refinements: Escalate to Stage B when precision/optimization needed
   - Cost-efficient exploration of design space

### 4. **Educational and Research Settings**
   - Students learn Verilog faster with AI assistance at minimal compute cost
   - Researchers can prototype complex RTL designs with affordable inference
   - Enables large-scale hardware synthesis studies without prohibitive compute budgets

### 5. **Bug Detection and Repair**
   - Formal verification feedback automatically generates targeted test cases
   - Repair recommendations guide designer focus to specific problem areas
   - Reduces manual debugging cycles for hardware engineers

### Design Challenges & Scalability

**Challenges:**
- Formal verification can time out on very complex specifications (>10K lines)
- Counterexample extraction requires SMT solver access (not always available in restricted environments)
- Escalation thresholds must be re-calibrated for new model families

**Scalability Considerations:**
- System scales to industry-scale specifications with specification chunking
- Formal verification bottleneck addressed via distributed verification services
- Stage A optimization continues with smaller, faster models (distilled variants)

---

## Insights & Implications

### 1. **Model Scaling is Not Always Optimal**
   The paper challenges the conventional wisdom that larger models are always better. A pragmatic two-stage approach often outperforms single-model selection in cost-quality trade-space, particularly for specialized domains like hardware generation.

### 2. **Inexpensive Diagnostics Enable Intelligent Delegation**
   Compilation, linting, and lightweight testing provide surprisingly effective signals for escalation decisions. This suggests general principle: **invest in diverse, inexpensive verification mechanisms rather than relying on single expensive oracle**.

### 3. **Evidence-Driven Repair Over Blind Retry**
   Counterexample-guided repair significantly outperforms simple retry-based approaches. Extracting failure traces and converting them to targeted tests is more effective than statistical retry. **Specific feedback beats generic repetition**.

### 4. **Portable Orchestration Architecture**
   The decoupling of escalation logic from coder implementations enables broad applicability. Organizations can layer HDLFORGE on top of existing tools and models without wholesale replacement, suggesting a general pattern for orchestration frameworks.

### 5. **Hardware Code Generation as a Testbed for Agent Design**
   Hardware code generation presents unique verification opportunities (formal methods, simulation testing) unavailable in general software. This domain serves as excellent validation environment for multi-agent frameworks before deployment in less-verifiable domains.

### Limitations & Open Questions

- **Formal Verification Limitations:** Approaches that don't scale to industrial-size designs (>100K lines) need further research
- **Model-Specific Tuning:** Escalation thresholds require re-calibration when swapping model families
- **Generalization Across Domains:** Unclear if HDLFORGE's staging approach translates to other code generation domains
- **Interactive Escalation:** Paper doesn't explore user-initiated escalation requests; all escalation is automatic

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** [HDLFORGE: A Two-Stage Multi-Agent Framework (2603.04646)](https://arxiv.org/abs/2603.04646)
- **GitHub Repository:** [HDLFORGE on GitHub](https://github.com/amir-abdollahi/HDLFORGE) (if available)
- **Benchmarks:**
  - VerilogEval: [https://github.com/shailja-thakur/VerilogEval](https://github.com/shailja-thakur/VerilogEval)
  - RTLLM: Hardware competition benchmark

### Integration & Deployment

**Dependencies:**
- Python 3.10+
- LLM API access (OpenAI GPT-4o, Qwen API, or local model serving)
- Formal verification tools: Z3 SMT solver, optional SystemVerilog simulation (ModelSim, VCS)
- Verilog linter: Verilator or commercial alternatives

**Quick-Start Example (Pseudo-code):**
```python
from hdlforge import HDLForgeOrchestrator, StageAConfig, StageBConfig

# Initialize stages
stage_a = StageAConfig(model="qwen-7b", temperature=0.7)
stage_b = StageBConfig(model="gpt-4o", temperature=0.3)

# Create orchestrator
hdlforge = HDLForgeOrchestrator(stage_a=stage_a, stage_b=stage_b)

# Generate Verilog
spec = "Design a 32-bit Fibonacci LFSR..."
result = hdlforge.generate(spec)

print(f"Generation Stage: {result.stage}")  # 'A' or 'B'
print(f"Pass@1: {result.passed}")
print(f"Latency: {result.latency_ms}ms")
```

**Extending for Custom Domains:**
- Modify `DiagnosticAssessment` module for domain-specific checks
- Implement custom `EscalationPolicy` for different cost-quality trade-offs
- Integrate domain-specific verification backends (formal, simulation, or runtime testing)

---

## Related Work & Context

### Foundational Agent Orchestration

- **AutoGen (2023):** Multi-agent conversation framework; HDLFORGE applies staged escalation pattern to the AutoGen paradigm
- **MetaGPT (2023):** Role-based multi-agent for software engineering; HDLFORGE extends with adaptive model allocation
- **LangGraph (2024):** Stateful orchestration; HDLFORGE demonstrates value of probabilistic escalation within graph execution

### Hardware Code Generation Prior Work

- **VerilogEval (2023):** Introduced the benchmark suite; HDLFORGE achieves SOTA on this benchmark
- **OriGen (2023):** Optimization-focused Verilog generation; HDLFORGE surpasses through staged approach
- **AutoVCoder & MAGE (2024-2025):** Multi-agent variants; HDLFORGE improves via calibrated escalation

### Formal Verification & LLM Integration

- **Formal Methods + LLMs:** Growing intersection; HDLFORGE demonstrates concrete integration of formal counterexamples into repair workflow
- **Bounded Model Checking:** Scalable verification for hardware; HDLFORGE leverages BMC traces for targeted repair

### Related Agent Frameworks

- **HDLFORGE vs. Orchestration Survey (2026):** HDLFORGE exemplifies "Staged Multi-Agent Orchestration" pattern documented in recent surveys
- **Skill-Based Agents (2602.20867, 2606.20631):** HDLFORGE's escalation controller resembles skill selection but operating on model capacity rather than discrete skills

---

## Future Research Directions

1. **Hybrid Staged Cascades:** Extend beyond two stages to multi-stage pipelines with finer-grained model allocation
2. **Learned Escalation Policies:** Replace rule-based escalation with RL-trained policy that learns optimal escalation patterns
3. **Cross-Domain Portability:** Test HDLFORGE on software code generation, data structure synthesis, and other specialized domains
4. **Interactive Escalation:** Incorporate user-driven escalation requests and interactive refinement loops
5. **Formal Verification Optimization:** Scale formal verification backend to industrial-scale designs via distributed verification or abstraction techniques

---

## Author & Citation

**Authors:** Armin Abdollahi, Saeid Shokoufa, Negin Ashrafi, Mehdi Kamal, Massoud Pedram

**Citation:**
```bibtex
@article{abdollahi2026hdlforge,
  title={HDLFORGE: A Two-Stage Multi-Agent Framework for Efficient Verilog Code Generation with Adaptive Model Escalation},
  author={Abdollahi, Armin and Shokoufa, Saeid and Ashrafi, Negin and Kamal, Mehdi and Pedram, Massoud},
  journal={arXiv preprint arXiv:2603.04646},
  year={2026}
}
```

---

## Key Takeaways

1. **HDLFORGE demonstrates practical value of multi-stage agent orchestration** with evidence-driven escalation for cost-quality optimization
2. **Inexpensive diagnostic signals enable effective delegation decisions** without expensive oracles
3. **Counterexample-guided repair outperforms blind retry** in specialized code generation domains
4. **Portable orchestration layer** enables broad adoption without legacy system replacement
5. **Hardware code generation serves as excellent testbed** for agent framework validation before general deployment

