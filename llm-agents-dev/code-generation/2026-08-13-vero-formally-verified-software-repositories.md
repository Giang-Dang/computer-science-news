# Vero: Can AI Agents Build Formally Verified Software Repositories?

**ArXiv ID:** 2608.13522  
**Authors:** Zhe Ye, Hantao Lou, Yuechun Sun, Peiyang Song, Zhengxu Yan, Timothe Kasriel, Qingyang Zhang, Kaiyu Yang, Soonho Kong, Jingxuan He, Dawn Song  
**Affiliations:** UC Berkeley and collaborating institutions  
**Submission Date:** August 2026  
**URL:** https://arxiv.org/abs/2608.13522  
**Subject Areas:** Machine Learning, AI, Logic in Computer Science, Programming Languages, Software Engineering

## Executive Summary

Vero introduces the first repository-level benchmark for evaluating AI agents' ability to generate not just code, but formally verified software implementations. While current coding agents excel at generating functional code, they provide no guarantees of correctness—a critical limitation for safety-critical systems. Vero addresses this gap by evaluating agents on joint implementation and proof synthesis across 43 real-world multi-module repositories spanning Python, Dafny, Verus, and Coq, with formal specifications and reference implementations. The benchmark reveals that even frontier agents achieve only 62.8% pass rates on full problems, with near-zero performance on the hardest instances, highlighting significant technical challenges in automated formal verification. This work is significant for agent-driven development because it establishes correctness as an evaluable property and provides a standard benchmark for advancing trustworthy, verifiable code generation.

## Problem Statement

### Development Automation Challenge

Modern AI coding agents can generate functional code and fix bugs, but they operate without any correctness guarantees. In safety-critical domains—cryptographic protocols, distributed systems, medical software, autonomous vehicles—code correctness is non-negotiable:

- **Cryptographic Protocols**: Subtle implementation errors break security properties
- **Distributed Systems**: Concurrency bugs cause data corruption and inconsistency
- **Medical/Safety Software**: Logic errors can cause harm or death
- **Financial Systems**: Off-by-one errors lead to computational losses

Current practice relies on:
1. Manual code review (time-consuming, error-prone)
2. Extensive testing (insufficient for proving correctness)
3. Formal verification by experts (expensive, requires specialized knowledge)

### Prior Agent System Limitations

Existing coding agent evaluation focuses on:
- **Functional correctness**: Does the code run without errors?
- **Test coverage**: Do passing tests validate expected behavior?
- **Code quality**: Is the code readable and maintainable?

Missing:
- **Formal guarantees**: Can we prove the code satisfies its specification?
- **Repository-scale verification**: Do implementations handle module interactions correctly?
- **Multi-language verification**: Does the agent work across formal frameworks?
- **Real-world complexity**: Can agents handle cryptographic and distributed systems code?

### Research Gap

The lack of a repository-level formal verification benchmark prevents:
- Systematic evaluation of agent capability for verified code generation
- Comparison of approaches for joint implementation and proof synthesis
- Understanding of what makes formal verification synthesis hard
- Development of agents specifically designed for correctness assurance

## Core Concepts & Theory

### Formal Verification Foundations

**Formal Specification**: A machine-readable mathematical description of what code should do
```
Example (Lean 4):
def sum_array (arr : Array Int) : Int :=
  arr.foldl (· + ·) 0

-- Specification: sum of empty array is 0
theorem sum_empty : sum_array #[] = 0 := rfl

-- Specification: sum of [a, b] equals a + b
theorem sum_two (a b : Int) : sum_array #[a, b] = a + b := by
  simp [sum_array]
```

**Proof Synthesis**: Automatic generation of formal proofs that implementations satisfy specifications
- **Automated reasoning**: SMT solvers, SAT solvers
- **Tactic-based proving**: Interactive theorem provers (Lean, Coq)
- **Hybrid approaches**: Combining automation with guided search

### Multi-Module Repository Challenges

Real-world software rarely exists in isolation. Verification must handle:

```
Repository Structure:
├── core/
│   ├── crypto.lean      (cryptographic primitives)
│   ├── spec_crypto.lean (cryptographic specs)
│   └── proof_crypto.lean (correctness proofs)
├── applications/
│   ├── protocol.lean    (uses crypto primitives)
│   ├── spec_protocol.lean
│   └── proof_protocol.lean
└── tests/
    └── test_protocol.lean (integration tests)

Challenges:
1. API Interface Consistency: Each module must respect API contracts
2. Cross-Module Proofs: Proofs at module boundaries
3. Dependency Resolution: Handling module imports and dependencies
4. Specification Composition: How do module specs compose?
```

### Dual Evaluation Modes

**Proof-Only Mode**: Agent is given correct implementation, must generate formal proof
- Tests theorem proving capability
- Isolates verification challenges from code generation
- Useful for systems where reference implementation exists

**Code-and-Proof Mode**: Agent must generate both implementation and proof
- Tests full synthesis capability
- Reflects real development workflow
- More challenging, but more realistic

### Formal Languages in Vero

1. **Lean 4**
   - Interactive theorem prover
   - Tactic-based proof construction
   - Good for software verification
   - Example: Cryptographic protocol proofs

2. **Dafny**
   - Automated program verifier
   - Built-in SMT solver integration
   - Specification and annotation language
   - Example: Algorithm correctness proofs

3. **Verus**
   - Systems verification language
   - Combines Rust-like syntax with formal verification
   - Designed for low-level systems code
   - Example: Kernel and concurrency verification

4. **Coq**
   - Proof assistant with powerful tactics
   - Rich specification language
   - Example: Mathematical and algorithm proofs

### Agent Architecture for Verified Synthesis

```
┌─────────────────────────────────────────────────────┐
│        Coding Agent with Verification               │
│                                                     │
│  ┌──────────────┐  ┌────────────────┐             │
│  │ Code Gen     │  │ Proof Gen      │             │
│  │ (LLM)        │  │ (LLM + Tools)  │             │
│  └──────┬───────┘  └────────┬───────┘             │
│         │                   │                      │
│  ┌──────▼────────────────────▼─────┐              │
│  │  Specification Parsing          │              │
│  │  (extract types, properties)    │              │
│  └──────────┬──────────────────────┘              │
│             │                                     │
│  ┌──────────▼──────────────┐                     │
│  │ Module Resolution       │                     │
│  │ API Contract Matching   │                     │
│  │ Dependency Validation   │                     │
│  └──────────┬──────────────┘                     │
│             │                                     │
│  ┌──────────▼──────────────────────────┐         │
│  │ Formal Verification Backend        │         │
│  │ (Lean 4 / Dafny / Verus / Coq)    │         │
│  └──────────┬──────────────────────────┘         │
│             │                                     │
│             ▼                                     │
│  Result: ✓ Verified  or  ✗ Failed               │
│                                                     │
└─────────────────────────────────────────────────────┘

Error Handling Loop:
Code/Proof Error → Error Message → Agent Revision →
  Verification → Repeat until success or max attempts
```

### Correctness Guarantee Levels

1. **Functional Correctness**: Implementation satisfies specification
2. **Type Correctness**: Code adheres to type system
3. **Safety Properties**: No buffer overflows, null derefs, data races
4. **Liveness Properties**: Termination, progress guarantees
5. **Module Correctness**: Inter-module contracts satisfied

## Main Ideas & Contributions

### Primary Contribution: Repository-Level Benchmark

**Vero Benchmark Characteristics**:

| Dimension | Details |
|-----------|---------|
| **Size** | 43 multi-module repository instances |
| **Languages** | 4 formal languages (Python, Dafny, Verus, Coq) |
| **Domains** | Cryptography, distributed systems, algorithms, data structures |
| **Realism** | Sourced from real-world repositories |
| **Specification** | Manually curated formal specs with reference implementations |
| **Evaluation Modes** | Proof-only and code-and-proof synthesis |
| **Audit Mechanism** | Formal verification of benchmark correctness itself |

### Key Innovation: Joint Implementation and Proof Synthesis

Rather than evaluating code generation and verification separately, Vero evaluates agents on their ability to generate code **and** proofs that the code is correct:

**Why This Matters**:
- Mirrors real development workflow (write code, then verify)
- Tests agent's understanding of specification requirements
- Evaluates ability to construct non-trivial proofs
- Reveals gaps in reasoning about code correctness

### Benchmark Curation & Quality Assurance

The benchmark itself undergoes formal verification:

1. **Specification Auditing**: Formal proof that specifications are satisfiable
2. **Reference Implementation Validation**: Proofs that reference implementations satisfy specs
3. **Module Consistency**: Verification that API contracts hold across modules
4. **Redundancy Checking**: Ensuring no trivial or over-specified instances

```lean
-- Example audit: Verify specification is not vacuously true
theorem spec_satisfiable : ∃ x : Nat, P x := by
  use 42
  -- Proof that witness satisfies property
  simp [P]
  -- ... proof tactics
```

### Practical Discovery: Hardness of Formal Verification for LLMs

The benchmark reveals striking performance gaps:

- **Overall Pass Rate**: 27/43 instances (62.8%) fully solved
- **Hardness Distribution**: 
  - Easiest instances: Agents solve 90%+ of cases
  - Medium difficulty: 60-70% pass rate
  - Hardest instances: 0% pass rate for strongest agents
  
This bimodal distribution suggests formal verification synthesis requires fundamentally new approaches.

## Methodology & Implementation

### Benchmark Construction

**Instance Selection Process**:
1. Identify real-world repositories with formal specifications
2. Extract multi-module subsets with clear API boundaries
3. Curate or generate formal specifications
4. Create reference implementations
5. Formally verify specifications and implementations
6. Organize into benchmark instances

**Domain Coverage**:

| Domain | Examples | Count |
|--------|----------|-------|
| Cryptography | Symmetric encryption, digital signatures, hash functions | ~10 |
| Distributed Systems | Consensus protocols, distributed algorithms | ~8 |
| Algorithms | Sorting, searching, graph algorithms | ~15 |
| Data Structures | Balanced trees, heaps, sets | ~10 |

### Experimental Setup

**Evaluation Methodology**:

1. **Agent Configuration**: Frontier LLM-based coding agents
2. **Tool Access**: Full access to Lean 4 compiler and proof checker
3. **Attempt Budget**: Limited number of generation/revision attempts per instance
4. **Evaluation Criteria**: 
   - Code compiles without type errors
   - Formal proofs pass verification
   - All modules satisfy API contracts
   - Proofs are non-trivial (not just `sorry` placeholders)

**Agent Configurations Tested**:
- Single-model agents with different frontier LLMs
- Multi-model ensembles with voting/ranking
- Agents with retrieval-augmented generation (RAG) over specification databases
- Chain-of-thought prompting with specification decomposition

### Metrics & Results

**Quantified Performance**:

```
Overall Performance:
┌────────────────────────────┐
│ Pass Rate: 27/43 (62.8%)   │
│ Failure Rate: 16/43 (37.2%)│
└────────────────────────────┘

Hardness Distribution:
Easy (1-15):    13/15 pass (86.7%)
Medium (16-30): 12/16 pass (75.0%)
Hard (31-43):   2/12 pass (16.7%)

Instance 43 (Hardest):
├─ Code Generation: 90% success rate
├─ Individual Module Proofs: 70% success rate
└─ Full Proof Completion: 0% success rate
```

**Failure Analysis**:

| Failure Type | Frequency | Severity |
|-------------|-----------|----------|
| Type/compilation errors | 15% | Easy (fixable with revision) |
| Incomplete proofs | 45% | Medium (proof strategy issues) |
| Incorrect module interactions | 20% | High (requires semantic understanding) |
| Specification misunderstanding | 15% | High (fundamental misalignment) |
| Timeout/resource limits | 5% | Technical (may improve with better tools) |

**Statistical Significance**:
- Performance gaps between models: Statistically significant (p < 0.001)
- Hardness effect: Highly significant (ANOVA F-statistic: 45.2)
- Correlation between code generation and proof success: r = 0.73

### Multi-Module Orchestration

Agents must handle orchestration challenges:

```
Agent Workflow for Multi-Module Synthesis:

1. Parse Specifications
   ├─ Extract module interfaces
   ├─ Identify interdependencies
   └─ Build module graph

2. Plan Verification Order
   ├─ Topological sort by dependencies
   ├─ Identify independent modules
   └─ Plan parallel verification (if applicable)

3. Generate Module Implementations
   ├─ Generate module code
   ├─ Type-check against interfaces
   └─ Verify API contracts hold

4. Synthesize Proofs
   ├─ Generate per-module proofs
   ├─ Synthesize cross-module lemmas
   └─ Compose proofs into repository proof

5. Validation & Iteration
   ├─ Run formal verification
   ├─ Extract error messages
   ├─ Revise failed components
   └─ Repeat until success
```

## Practical Applications & Use Cases

### Software Development Applications

1. **Critical Infrastructure Code**
   - Smart contracts (blockchain systems)
   - Financial transaction processing
   - Medical device control software
   - Aerospace systems
   
   **Workflow**: Specify desired properties → Agent generates verified code → Deploy with confidence

2. **Cryptographic Libraries**
   - Implement encryption algorithms
   - Generate proofs of protocol security properties
   - Prevent common cryptographic errors
   
   **Workflow**: Formal spec of crypto-property → Vero agent → Audited, verified implementation

3. **Distributed Systems**
   - Consensus protocols (Raft, Paxos)
   - Concurrency control mechanisms
   - Replication schemes
   
   **Challenge**: Proving safety/liveness properties at scale
   **Application**: Generate provably-correct distributed system implementations

4. **Formal Code Review**
   - Automatically verify human-written code against specifications
   - Generate missing proofs for existing implementations
   - Audit third-party libraries
   
   **Workflow**: Code + Spec → Vero → Proof of compliance or counterexample

5. **Software Evolution**
   - When specifications change, regenerate verified code
   - Maintain proof consistency during refactoring
   - Ensure backward compatibility guarantees
   
   **Use Case**: Version updates with formal guarantees

### Integration Challenges

1. **Proof Readability**: Generated proofs may be unreadable or unmaintainable
   - Solution: Proof minimization and natural language explanation
   
2. **Specification Adequacy**: Formal specs may not capture all desired properties
   - Challenge: How complete is the specification?
   - Solution: Automated specification debugging and completion

3. **Performance Overhead**: Proof verification adds latency
   - Mitigation: Incremental verification, caching proven results
   
4. **Tool Heterogeneity**: Different languages (Lean, Dafny, Verus, Coq) have different capabilities
   - Challenge: Cross-language interoperability
   - Solution: Language-agnostic intermediate representations

### Cost & Latency Implications

| Factor | Impact |
|--------|--------|
| **Proof Complexity** | O(n²) growth with code size in worst case |
| **Verification Latency** | 100ms - 10s per module depending on complexity |
| **LLM Inference** | Multiple rounds of generation/revision |
| **Development Velocity** | Trade-off between verification cost and correctness guarantee |
| **Training Data** | Requires curated formal verification examples (expensive to obtain) |

## Insights & Implications

### Impact on Agent-Driven Development

1. **Correctness as First-Class Goal**
   - Formal verification shifts from post-hoc validation to primary objective
   - Agents optimize for provable correctness, not just functional correctness
   - Enables deployment of agents in safety-critical domains

2. **New Evaluation Paradigm**
   - Benchmark focuses on what matters most: correctness guarantees
   - Reveals that agents struggle most on hardest verification problems
   - Motivates development of specialized verification-focused agents

3. **Multi-Agent Orchestration Insights**
   - Module independence enables parallel verification strategies
   - Different agents may specialize in different proof styles
   - Proof tactics may be learned and reused across repositories

### Advancement in Autonomous Coding

1. **From Functional to Trustworthy**
   - Agents graduate from "code that works" to "code that's proven correct"
   - Enables autonomous development in regulated industries

2. **New Frontier for AI**
   - Formal verification is harder than functional code generation
   - Pushing boundaries of LLM reasoning and proof synthesis
   - Opens new research directions in AI-assisted verification

3. **Integration with Development Workflows**
   - Agents can serve as verification assistants to human developers
   - Proof sketches generated by agents can be completed by humans
   - Bi-directional collaboration model

### Limitations & Challenges

1. **Scalability**
   - Current results on relatively small modules
   - Behavior on large-scale systems unknown
   - Proof complexity grows exponentially

2. **Generalization**
   - Agents may overfit to benchmark instances
   - Transfer to new domains/specifications uncertain
   - Real-world specifications may be underspecified

3. **Proof Strategy Learning**
   - Agents struggle to discover novel proof tactics
   - Limited ability to use domain-specific reasoning
   - Proof by cases/induction requires careful orchestration

4. **Human Collaboration**
   - Full autonomy is unrealistic for complex systems
   - Better models for human-AI collaborative verification needed
   - Explanation of generated proofs is critical

## Code & Resources

### Availability

- **Paper**: https://arxiv.org/abs/2608.13522
- **Benchmark**: Supplementary materials at arxiv.org (contact authors for access)
- **Formal Systems Used**:
  - Lean 4: https://lean-lang.org/
  - Dafny: https://dafny.org/
  - Verus: https://github.com/verus-lang/verus
  - Coq: https://coq.inria.fr/

### Dependencies & Requirements

**Software**:
- Lean 4 (latest version with Std library)
- Dafny (SMT solver backend)
- Verus (requires Rust toolchain)
- Coq (with proof automation tactics)

**Hardware**:
- SMT solver (Z3, CVC5): ~500MB RAM typical
- Proof checking: single CPU sufficient, ~1-10s per instance
- LLM inference: GPU beneficial (A100 or better for batch evaluation)

**Data Requirements**:
- Benchmark instances: ~100MB total
- Training data: Curated formal verification examples (~1GB)

### Quick-Start Integration Guide

```lean
-- 1. Define your specification in Lean 4
def binary_search (arr : Array Int) (target : Int) : Option Nat :=
  sorry

-- 2. State your correctness property
theorem binary_search_correct (arr : Array Int) (target : Int) (h : arr.Sorted) :
  match binary_search arr target with
  | some idx => arr[idx]! = target
  | none => ∀ i, arr[i]! ≠ target := by
  sorry

-- 3. Feed specification to Vero agent
-- Agent generates implementation and proof

-- 4. Verify result
#check binary_search_correct
```

### Key Papers and Baselines

- **DeepSeek-Prover**: LLM-based formal verification
- **Proof-Sketch Completion**: Human-sketched proofs completed by agents
- **Curriculum Learning for Verification**: Progressive difficulty in learning to prove

## Related Work & Context

### Foundational Work

- **Formal Verification**: Floyd-Hoare logic, program verification theory
- **Automated Reasoning**: SMT solvers, SAT solving
- **Proof Assistants**: Lean, Coq, Isabelle ecosystems
- **Theorem Proving**: Interactive and automated approaches

### Related Papers (Formal Verification + LLMs)

- **ProofNet**: Dataset and benchmarks for formal proof synthesis
- **Proof-Search in LLMs**: How language models navigate proof search spaces
- **Specification Mining**: Automatic extraction of properties from code
- **Verified Code Generation**: AI-assisted verification of generated implementations

### Complementary Work

- **Code Generation**: Software engineering with AI agents
- **Testing Strategies**: Test generation for verification
- **Specification Synthesis**: Automatic specification from examples
- **Human-AI Collaboration**: Interactive verification with human guidance

### Future Research Directions

1. **Hybrid Approaches**
   - Combine symbolic reasoning with neural networks
   - Integration of SAT/SMT solvers with LLM-based proof search
   - Neuro-symbolic formal verification

2. **Proof Automation Advances**
   - Novel tactics for difficult proof classes
   - Learning from human-written proofs
   - Domain-specific proof strategies

3. **Specification Synthesis**
   - Automatic inference of specifications from requirements
   - Discovering likely invariants
   - Specification debugging and correction

4. **Cross-Language Verification**
   - Unified frameworks for multiple formal languages
   - Translation between specification languages
   - Interoperability of different provers

5. **Scalability**
   - Techniques for verifying large systems
   - Modular verification with compositional proofs
   - Efficient proof checking and caching

## Summary

Vero represents a critical step toward trustworthy AI-driven software development by establishing formal verification as an evaluable benchmark for coding agents. The first repository-level formal verification benchmark reveals both the promise and the challenges: frontier agents achieve 62.8% pass rates overall but fail completely on the hardest instances, highlighting that formal verification requires novel approaches beyond current code generation methods.

The benchmark's significance extends beyond evaluation—it establishes a new frontier for AI in software engineering where correctness guarantees are non-negotiable. For practitioners in safety-critical domains, this work opens possibilities for AI-assisted verified code generation. For researchers, it identifies formal verification synthesis as a critical research frontier demanding advances in LLM reasoning, proof search, and module-level orchestration.

As coding agents become increasingly prevalent in development workflows, Vero's message is clear: agents must not only generate working code, but prove it correct. This shift from functional correctness to formal correctness represents a fundamental evolution in how we think about autonomous software engineering.
