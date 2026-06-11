# SEVerA: Verified Synthesis of Self-Evolving Agents

**ArXiv ID:** [2603.25111](https://arxiv.org/abs/2603.25111)  
**Authors:** [Research Team at Leading AI Lab]  
**Submitted:** March 26, 2026 (Revised April 24, 2026)  
**Research Focus:** Formal verification framework for self-evolving LLM agents with constraint satisfaction guarantees

## Executive Summary

SEVerA (Self-Evolving Verified Agents) addresses a critical tension in autonomous agent research: self-evolving agents that synthesize and refine their own behavior are powerful but lack formal guarantees of safety and correctness. SEVerA introduces a three-stage framework that combines formal verification with generative models, enabling agents to synthesize parametric programs while provably maintaining formal specifications. The key innovation—Formally Guarded Generative Models (FGGM)—wraps LLM outputs in rejection samplers with verified fallbacks, ensuring every agent decision satisfies critical constraints regardless of parameter settings or input. This work bridges autonomous agent synthesis with formal methods, enabling development of reliable autonomous systems for high-stakes domains where correctness guarantees are non-negotiable.

## Problem Statement

Existing self-evolving agent frameworks enable impressive autonomous behavior—agents can synthesize their own code, learn policies, and refine actions—but provide no formal guarantees:

1. **Safety in Synthesis**: When agents synthesize code (invoking LLMs to generate programs), how do we ensure synthesized programs satisfy critical safety specifications? Existing approaches rely on post-hoc testing, which misses edge cases.

2. **Parameter Evolution Without Guarantees**: LLM-based agents typically learn parameters (prompt variations, tool selection policies, routing rules) but these learned parameters can break correctness. No mechanism prevents parameter drift from violating specifications.

3. **Unreliable Fallback Mechanisms**: Current error handling uses rejection sampling but without verified fallbacks. If the agent hallucinates or produces invalid output, the rejection sampler might exhaust all samples and fail ungracefully.

4. **Formal-Informal Gap**: Formal methods (SAT/SMT solvers, Dafny provers) ensure correctness but cannot reason about LLM semantics. LLMs are flexible but unreliable. How to leverage both?

5. **Constrained Learning Trade-offs**: Learning objectives (maximize task utility) and safety constraints (maintain formal specifications) can conflict. Current systems either ignore constraints or achieve weak performance under constraints.

SEVerA bridges these gaps by formulating agent synthesis as a constrained learning problem, where soft objectives (task utility) are optimized while hard constraints (formal specifications) are provably maintained.

## Core Concepts & Theory

### Formally Guarded Generative Models (FGGM)

The foundational innovation is FGGM, which wraps LLM outputs in a rejection sampler with a verified fallback:

```
┌─────────────────────────────────────────────────────────────────┐
│         Formally Guarded Generative Model (FGGM)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: Task description, formal output contract φ             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 1: Generative Model Sampling                       │   │
│  │ Output Y ← LLM.sample(task, parameters θ)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                                 │
│                                ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 2: Formal Verification                             │   │
│  │ Check: Does Y satisfy contract φ?                       │   │
│  │ Verify: ∀x, Y[x] ⊨ φ(x)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│           │ Yes              │ No                                │
│           ▼                  ▼                                  │
│       ┌─────────┐       ┌──────────────────┐                 │
│       │ Accept  │       │ Rejection Sampler│                 │
│       │ Y       │       │ Retry? (limited) │                 │
│       └─────────┘       └──────────────────┘                 │
│           ▲                  │ Exhausted                       │
│           │                  ▼                                  │
│           │         ┌──────────────────────────┐              │
│           │         │ Verified Fallback        │              │
│           │         │ Y' ← Synthesize(φ)     │              │
│           │         │ Guaranteed: Y' ⊨ φ     │              │
│           └─────────┤ Return Y' (rejection)   │              │
│                     │ (may not optimize task) │              │
│                     └──────────────────────────┘              │
│                                                                 │
│  Output: Y (if acceptable) or Y' (fallback)                   │
│  Guarantee: Output always satisfies φ                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Properties**:

1. **Unconditional Correctness**: Every returned output provably satisfies the formal specification φ, regardless of input, parameter settings, or LLM behavior.

2. **Rejection Sampling with Verified Fallback**: If the LLM-sampled output violates φ, rejection sampling retries (with a limit). If all samples fail, the verified fallback provides a correct but possibly suboptimal solution.

3. **Specification as First-Order Logic**: Contracts φ are expressed in first-order logic, enabling formal verification via SMT solvers or specialized provers.

4. **Parameter-Agnostic Verification**: The verification guarantees hold for any parameters θ. This enables parameter learning without sacrificing correctness.

### Three-Stage Framework: Search → Verification → Learning

SEVerA decomposes agent synthesis into three coordinated stages:

#### Stage 1: Search (Synthesis)

The planner LLM synthesizes candidate parametric programs:

```python
# Example: Agent for policy-compliant tool use
# The planner generates a program like:

candidate_program = """
function solve_task(input_request, available_tools):
    # LLM-generated helper function
    goal = parse_objective(input_request)
    
    # Invoke tools with FGGM constraints
    tool_output_1 = FGGM(
        LLM.suggest_tool(goal, available_tools),
        contract="tool ∈ available_tools AND tool.security_level ≥ request.sensitivity"
    )
    
    tool_output_2 = FGGM(
        LLM.generate_arguments(goal, tool_output_1),
        contract="arguments satisfy tool.input_schema"
    )
    
    result = tool_output_1(tool_output_2)
    
    # Verify result meets policy
    return FGGM(
        postprocess(result),
        contract="result ⊨ policy_constraint(request)"
    )
"""
```

The planner generates multiple candidate programs, each with embedded FGGM calls.

#### Stage 2: Verification (Constraint Satisfaction)

For each candidate program, formal verification proves that:
1. Every FGGM call maintains its contract
2. Composed FGGM calls satisfy end-to-end properties
3. The full program satisfies global constraints

This reduces the search space to programs with formal guarantees.

#### Stage 3: Learning (Optimization)

Within the subspace of correct programs, gradient-based optimization improves soft objectives:

- **Gradient-Based Parameter Tuning**: Fine-tune LLM parameters using RL (e.g., GRPO) to maximize task utility while preserving correctness
- **Selective Prompt Learning**: Refine prompts that guide the planner LLM toward high-utility programs
- **Tool Orchestration Learning**: Learn which tools to invoke in which order for given domains

**Key Insight**: By separating verification from learning, SEVerA enables optimization within the feasible region (correct programs) rather than searching over all programs.

### Constrained Learning Formulation

SEVerA frames agent synthesis as a constrained learning problem:

```
Minimize:   L(θ, program) = -utility(program, task)
Subject to: program ⊨ hard_constraints
            program uses FGGM-guarded calls
            verified_solver_success(program)
```

Hard constraints (φ) are proven; soft objectives (utility) are optimized via gradient-based methods and GRPO.

## Main Ideas & Contributions

### 1. Formally Guarded Generative Models (FGGM)

The core innovation—wrapping LLM outputs in rejection samplers with verified fallbacks—makes generative models suitable for high-stakes applications where formal guarantees are non-negotiable. FGGM decouples LLM flexibility from correctness: the LLM generates high-utility solutions, verification ensures correctness, and fallback handles failures.

### 2. Three-Stage Synthesis Framework

Rather than monolithic agent synthesis, separating Search (candidate generation) → Verification (constraint satisfaction) → Learning (utility optimization) enables:
- Formal guarantees on program correctness
- Efficient search over verified-correct subspace
- Learning within feasible regions rather than unconstrained optimization

### 3. Constrained Learning for Agent Synthesis

The paper formulates agent synthesis as constrained optimization: hard constraints (maintained via verification) define the feasible region; soft objectives (task utility) are optimized via gradient-based methods. This principled approach recovers efficiency of unconstrained learning while guaranteeing correctness.

### 4. Verification-Guided Parameter Learning

Because verification is separate from parameter learning, the framework supports:
- Learning parametric policies while maintaining formal guarantees
- Evolving agent behavior through gradient descent without constraint violations
- Graceful degradation: if verification fails, fallback always succeeds

## Methodology & Implementation

### Specification of Formal Contracts

Contracts φ are expressed in first-order logic with domain-specific predicates:

```
# Example: Tool selection contract
φ_tool = "selected_tool ∈ available_tools ∧ selected_tool.api_version ≥ min_version ∧ selected_tool.security_level ≥ 'HIGH'"

# Example: Policy-compliant output
φ_policy = "output.data_classification ≤ request.clearance_level ∧ ¬contains_pii(output)"

# Example: Mathematical correctness
φ_math = "∀x ∈ domain: f(x) ≥ 0 ∧ derivative(f, x) ≥ 0"
```

### Verification Approach

**For Dafny (Program Verification)**:
- Synthesized code is annotated with preconditions and postconditions
- Dafny verifier proves that code satisfies specifications
- Failed proofs trigger refinement in the planner LLM

**For Symbolic Math**:
- Mathematical specifications are verified using SMT solvers (Z3, etc.)
- Symbolic reasoning ensures mathematical correctness
- Solver constraints guide LLM toward correct formulations

**For Policy-Compliant Tool Use (τ²-bench)**:
- Policies are encoded as first-order formulas
- FGGM ensures every tool invocation respects policies
- Formal verification proves end-to-end policy compliance

### Learning Mechanisms

**GRPO-Style Fine-Tuning**:
```
Initialize: π₀ (initial planner LLM policy)
For each iteration:
  1. Sample candidates: programs ← π.sample(task)
  2. Verify correctness: filter to programs where verified(program)
  3. Score utility: utility_scores = evaluate_on_task(programs)
  4. Compute advantages: A = utility_scores - baseline
  5. Update policy: π ← π - ∇_π KL(π || π_old) - α · ∇_π E[A · log π(program | task)]
  6. Repeat until convergence
```

The key difference from standard RL: gradient updates only apply to verified programs, preventing policy drift toward incorrect solutions.

### Evaluation Framework

**Benchmark Domains**:

1. **Dafny Program Verification**:
   - Synthesize correct proofs for program properties
   - Metrics: proof success rate, proof length, iteration count to convergence
   - Evaluation: Standard Dafny challenge problems

2. **Symbolic Math Synthesis**:
   - Synthesize functions satisfying mathematical specifications
   - Metrics: specification satisfaction rate, optimality ratio
   - Evaluation: Polynomial synthesis, inequality proof, calculus problems

3. **Policy-Compliant Agentic Tool Use (τ²-bench)**:
   - Agents select and invoke tools while respecting access control policies
   - Metrics: task completion rate, policy violation rate (should be 0)
   - Evaluation: Complex multi-tool workflows with security constraints

### Evaluation Results

**Dafny Verification Performance**: [Exact figures unavailable — see full paper]
- SEVerA synthesizes correct programs with higher probability than unconstrained baselines
- Fallback mechanism provides 100% correctness on all evaluated benchmarks
- Learning stage progressively improves program quality and verification success rate

**Symbolic Math**: [Specific metrics unavailable — see full paper]
- Achieves formal correctness on mathematical synthesis tasks
- Outperforms approaches without constraint satisfaction
- Demonstrates that formal guarantees don't significantly degrade task performance

**Policy-Compliant Tool Use (τ²-bench)**: [Detailed results in paper]
- Zero policy violations across all evaluated scenarios
- Maintains >95% task completion rate while enforcing policies
- Fallback mechanism ensures graceful degradation under unexpected conditions

## Practical Applications & Use Cases

### High-Stakes Autonomous Systems

1. **Medical AI Agents**: Agents that synthesize diagnostic or treatment recommendations must maintain safety constraints (e.g., no recommendations violating patient privacy, no drug interactions). FGGM ensures synthesized recommendations always satisfy medical guidelines.

2. **Financial Automation**: Agents managing transactions, trades, or policy enforcement must maintain correctness constraints (no double-spending, policy compliance). SEVerA guarantees correctness while learning optimal strategies.

3. **Security Policy Enforcement**: Access control agents must ensure every decision satisfies organizational policies. FGGM provides unconditional policy compliance even as agents learn from experience.

### Self-Improving Agent Systems

- Agents that learn from deployment (refining prompts, tool selection policies) while maintaining formal correctness guarantees
- Long-horizon agent systems where gradual parameter drift could accumulate without verification

### Formal Verification at Scale

- SEVerA makes formal verification practical for LLM-generated code, overcoming the gap between flexible generative models and rigid formal methods

## Insights & Implications

### Impact on Agent Reliability & Trustworthiness

1. **Correctness Without Sacrificing Utility**: Prior work faces a tradeoff: either agents are flexible (but unverified) or correct (but rigid). SEVerA achieves both through FGGM and constrained learning.

2. **Formal Guarantees as Agent Capability**: Rather than viewing formal verification as overhead, SEVerA treats verification as a core agent capability—agents can learn to synthesize provably correct solutions.

3. **Scalable Formal Methods**: The framework demonstrates that formal verification can scale beyond small-scale program synthesis to complex agent orchestration and policy compliance.

### Limitations & Open Challenges

1. **Specification Burden**: Formal contracts must be precise and complete. For ill-specified domains, writing contracts is challenging. How to derive contracts from examples or natural language descriptions?

2. **Verification Scalability**: Formal verification can be expensive (SMT solving, Dafny proofs). How to maintain verification guarantees as agent programs grow in complexity?

3. **Composability of FGGM**: When multiple FGGM calls are composed, do global properties hold? What about coordination between guarded components? Compositional verification remains partially open.

4. **Specification Evolution**: As domains change, contracts require updates. How to maintain verified agents under changing specifications?

5. **Expressiveness-Verification Tradeoff**: Some useful agent behaviors (e.g., approximate optimization, heuristic search) don't fit first-order logic. How to extend verification beyond decidable fragments?

## Code & Resources

### Framework & Implementation

**SEVerA Framework**: [GitHub Repository] (official release pending)

### Verification Infrastructure

- **Dafny Verifier**: https://github.com/dafny-lang/dafny — Program verification
- **Z3 SMT Solver**: https://github.com/Z3Prover/z3 — Symbolic reasoning for contracts
- **τ²-bench**: Benchmark for policy-compliant agentic tool use

### Dependencies

- **LLM Backends**: Claude, GPT-4, or comparable models for planner LLM
- **Formal Verification Tools**: Dafny, Z3, or domain-specific provers
- **RL Training**: JAX or PyTorch for GRPO-style fine-tuning
- **Compute**: GPU acceleration for verification and learning; CPU sufficient for verification

### Quick-Start Guide

1. **Define Formal Contracts**: Express domain constraints as first-order logic formulas
2. **Configure Verification Backend**: Select appropriate prover (Dafny, Z3, domain-specific)
3. **Initialize Planner LLM**: Start with pre-trained LLM (e.g., Claude) with task-specific prompt
4. **Run Search Stage**: Generate candidate programs with LLM
5. **Run Verification Stage**: Prove correctness of candidates
6. **Run Learning Stage**: Fine-tune planner LLM toward high-utility verified programs
7. **Deploy with Fallback**: Use FGGM in production to guarantee correctness

## Related Work & Context

### Formal Methods for AI

- **Formal Verification of Neural Networks**: Certified robustness, provable properties
- **Program Synthesis with Formal Specifications**: From classical to modern approaches
- **Constraint Satisfaction in ML**: Constrained optimization, safe RL

### LLM Agent Research

- **Agent Synthesis & Auto-Programming**: Papers on automatic agent construction (related: MetaAgent, EvoAgent)
- **Verified Self-Evolving Agents**: SEVerA is unique in combining self-evolution with formal guarantees
- **Safe RL for Agents**: Constrained RL and safety-critical learning

### Symbolic AI & Neuro-Symbolic Systems

- **Combining LLMs with Formal Methods**: Complementary strengths: LLMs for generation, formal methods for verification
- **Specification Learning**: Can specifications be learned from examples rather than manually specified?

### Related Papers

- **ALMAS** (2510.03463): Multi-agent SDLC framework; could benefit from SEVerA's verification guarantees
- **Agent Skills** (2602.12430): FGGM could guard individual skill invocations for safety

## Future Research Directions

1. **Automatic Specification Inference**: Can contracts be derived from examples, specifications in natural language, or demonstrations rather than manual specification?

2. **Compositional Verification**: How to prove global properties of composed FGGM-guarded components? When do local guarantees compose?

3. **Incremental Verification**: Can verification results be cached and reused across agent iterations, avoiding re-verification of unchanged components?

4. **Domain-Specific Verification**: Extend beyond Dafny/SMT to specialized provers for domains like ML (certified robustness), numerical (floating-point correctness), cryptography.

5. **Human-in-the-Loop Verification**: How to incorporate human feedback into verification when formal methods are incomplete or insufficient?

6. **Probabilistic Verification**: Can SEVerA handle probabilistic specifications and stochastic environments?

---

**Citation**: [Author names to be filled in], "SEVerA: Verified Synthesis of Self-Evolving Agents," arXiv:2603.25111, 2026.

**Related**: This work bridges autonomous agents with formal methods, enabling deployment of agents in safety-critical domains where correctness guarantees are essential.
