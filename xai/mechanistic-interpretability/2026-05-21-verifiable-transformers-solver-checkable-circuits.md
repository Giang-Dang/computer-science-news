# Towards Verifiable Transformers: Solver-Checkable Circuit Explanations

**ArXiv ID:** [2605.24033](https://arxiv.org/abs/2605.24033)

**Authors:** Neel Somani

**Submitted:** May 21, 2026

## Executive Summary

This paper addresses a fundamental challenge in mechanistic interpretability: while circuit discovery methods identify computational structures inside Transformers, proving what those circuits actually do remains difficult. The work introduces **Verifiable Transformers**, a framework that converts task-localized Transformer circuits into bounded, formal claims that can be automatically verified using Satisfiability Modulo Theories (SMT) solvers. By bridging the gap between circuit identification and formal verification, this work advances trustworthy AI through rigorous mechanistic understanding.

## Problem Statement

Mechanistic interpretability has made significant progress in identifying "circuits"—minimal computational subgraphs within neural networks that perform specific functions. However, current validation methods rely on:

- **Ad-hoc examples**: Testing circuits on a few representative cases
- **Ablation studies**: Removing edges and observing behavioral changes
- **Manual reasoning**: Inspecting attention patterns and weight structures

These approaches are limited because:
1. They don't provide **formal guarantees** about circuit behavior
2. The gap between "plausible" and "proven" circuits remains large
3. Circuits identified for one task may not generalize or be robust to perturbations
4. Existing circuit verification techniques cannot scale beyond toy models

The paper argues that mechanistic interpretability requires a fundamental shift: from post-hoc validation to **formal verification**, where circuit behavior is proven mathematically across bounded domains.

## Core Concepts & Theory

### Circuit Extraction and Mechanistic Interpretability

**What are circuits?** In mechanistic interpretability, a circuit is a minimal subgraph of a neural network's computational graph consisting of:
- Specific **attention heads** and **residual streams**
- **Edge connections** between these components
- A causal relationship where removing the edges degrades task performance

For a Transformer, the circuit operates on token embeddings and attention outputs to produce a task-relevant behavioral output.

### Satisfiability Modulo Theories (SMT)

SMT solvers are automated reasoning tools that can verify mathematical properties by encoding constraints and finding satisfying variable assignments. Key advantages:
- **Decidability**: For bounded domains and linear arithmetic, verification is computationally feasible
- **Completeness**: If a property holds, SMT solvers can prove it; if it doesn't, they provide counterexamples
- **Expressiveness**: Can encode complex symbolic reasoning including quantifiers and theories

The Verifiable Transformers framework encodes extracted circuits as SMT formulas, enabling automated, exhaustive verification over bounded task domains.

### Core Verification Properties

The framework verifies four key properties of circuits:

1. **Projected Functional Equivalence (PFE)**: Given an input and a candidate token projection, does the extracted circuit produce the same output as the full model?

2. **Edge Necessity**: Which edges in the circuit are essential? The framework identifies edges that, when removed, cause a measurable drop in task performance.

3. **Task-Relevant Invariance**: Are there input attributes (e.g., content vs. structural features) that the circuit ignores? This tests whether the circuit is sensitive only to task-relevant information.

4. **Final-Residual Robustness**: How robust is the circuit to small perturbations in intermediate activations? This measures whether the circuit maintains correct outputs when residual streams are slightly perturbed.

### Two-Stage Verification Strategy

The framework employs adaptive verification based on model tractability:

**Direct Verification**: When all circuit operators are exactly encodable in SMT (e.g., linear transformations, sparsemax, LeakyReLU):
- Encode the circuit directly into an SMT formula
- Query the solver exhaustively over the bounded domain
- Obtain formal proofs with zero approximation

**Surrogate-Mediated Verification**: When exact encoding is intractable (e.g., complex attention mechanisms):
- Learn an SMT-encodable **surrogate model** that approximates the circuit's behavior
- Validate the surrogate against the extracted circuit over bounded inputs
- Verify symbolic explanations against the surrogate with formal guarantees

This adaptive approach enables verification to scale from small interpretable models to realistic architectures like GPT-2.

## Main Ideas & Key Contributions

### 1. Bridging the Verification Gap

**Innovation**: The paper is the first to systematically convert extracted Transformer circuits into formal logical claims that can be automatically verified. This represents a paradigm shift from heuristic validation to formal proof.

**Why it matters**: Current mechanistic interpretability relies on manual inspection and statistical testing, which leaves room for error. Formal verification provides mathematical certainty.

### 2. SMT-Based Circuit Verification Framework

**Core Contribution**: The Verifiable Transformers framework defines:
- A **circuit extraction algorithm** that identifies task-localized subgraphs
- **Four verification properties** covering functional equivalence, necessity, invariance, and robustness
- **Two verification strategies** (direct and surrogate-mediated) for different model complexities

**Design Rationale**: 
- Direct verification works for interpretable architectures (sparsemax, LeakyReLU)
- Surrogate verification extends coverage to realistic models without sacrificing rigor
- Properties target both structural (edge necessity) and behavioral (equivalence, robustness) aspects

### 3. Scalability from Toy to Realistic Models

**Achievement**: The paper demonstrates verification on:
- **Small symbolic tasks** (up to 100 tokens): Direct SMT verification of all properties
- **GPT-2 scale** (2M parameters): Surrogate-mediated verification of quote-closing circuits over 1,280-prompt domains

**Significance**: This is the first formal verification of mechanistic interpretability at near-realistic scale, bridging the gap between interpretable toy models and practical systems.

### 4. Formal Guarantees on Circuit Robustness

**Contribution**: The framework provides **certified robustness bounds**—mathematical proofs that circuits maintain correct behavior under input perturbations. For example:
- "Circuit X is robust to perturbations of magnitude ≤ 0.01515 in residual streams"

This goes beyond ad-hoc ablation studies by quantifying precisely when circuits fail under adversarial perturbations.

## Methodology & Implementation

### Circuit Extraction Pipeline

The methodology follows this workflow:

1. **Model Training**: Train a Transformer on a task. For verification, use architectures with SMT-encodable components (e.g., sparsemax, LeakyReLU).

2. **Circuit Candidate Identification**: Specify:
   - The task behavior to explain (e.g., "predict closing quote position")
   - A candidate token projection (the output token to focus on)
   - An approximate task domain

3. **Sparse Circuit Extraction**: Extract the minimal subgraph connecting input tokens to the output, using gradient-based methods or attention-based heuristics.

4. **Verification with SMT Solver**: Encode the circuit and verify properties over the bounded domain.

### Experimental Setup

**Symbolic Task Experiments**:
- **Dataset**: Small sequence tasks with explicit ground truth (quote closing, bracket type tracking)
- **Architecture**: Custom GPT-style Transformers with 2-4 layers, 4-8 attention heads
- **Encoding**: Linear transformations, Signed L1 BandNorm, sparsemax attention, LeakyReLU
- **Solver**: Z3 (SMT solver by Microsoft Research)

**GPT-2 Scale Experiments**:
- **Model**: GPT-2 base (1.5B parameters), modified to use sparsemax and LeakyReLU
- **Dataset**: Quote-closing task on 1,280 prompts (hash-pinned for reproducibility)
- **Extraction**: Identify three-edge quote circuits
- **Verification**: Direct SMT verification for projected functional equivalence, invariance, and robustness

### Evaluation Metrics for Mechanistic Interpretability

The paper evaluates circuits using:

1. **Functional Equivalence Rate**: Percentage of domain inputs where extracted circuit output matches full model output
   - GPT-2 quote circuit: 1,280/1,280 (100% equivalence over bounded domain)

2. **Edge Necessity**: For each edge, count how many inputs become incorrect when it's removed
   - GPT-2 quote circuit: 640 edge-necessity witnesses per edge (50% of domain)

3. **Content Invariance**: Whether circuit ignores irrelevant token attributes
   - Test: Permute content while preserving structural features; circuit still produces correct output

4. **Robustness (Certified Radius)**: Minimum perturbation magnitude that causes circuit failure
   - GPT-2 quote circuit: Robustness at ε=0.01 with certified radius 0.01515

5. **Verification Time**: Computational cost of SMT verification
   - Small tasks: <1 second per property per circuit
   - GPT-2 circuit: [Exact figures unavailable — see full paper]

### Implementation Details

**Architecture Constraints**: Verification requires models with SMT-encodable operations:
- **Preferred**: Sparsemax (instead of softmax), LeakyReLU (instead of GELU)
- **Supported**: Linear layers, normalization without learnable parameters
- **Problematic**: GELU, LayerNorm, softmax (intractable for direct encoding; require surrogates)

**Bounded Domain Specification**: Verification operates over finite task domains:
- Inputs are hash-pinned to ensure deterministic, reproducible verification
- Domain size constrains computational cost: typical experiments use 100–1,280 samples

**Surrogate Learning**: When direct encoding fails:
1. Train a neural network surrogate to mimic circuit outputs over bounded domain
2. Validate surrogate fidelity against the extracted circuit (test mean squared error, etc.)
3. Encode the surrogate (a simpler model) into SMT
4. Verify properties against the surrogate with quantified error bounds

## Practical Applications & Real-World Use Cases

### 1. Trustworthy AI Systems in Critical Domains

**Healthcare**:
- Diagnostic AI systems require formal verification that decision circuits are robust to input variations
- Verifiable Transformers can certify that a medical imaging model's classification circuit is provably invariant to irrelevant image features (e.g., scanner type)
- Enables compliance with FDA requirements for AI transparency and robustness

**Finance**:
- Credit risk models must justify decisions to regulators and customers
- Formal circuit verification can prove that credit scoring circuits are not exploiting protected attributes
- Example: "Circuit X is invariant to race/ethnicity; all decisions depend only on loan history and creditworthiness"

**Law & Compliance**:
- EU AI Act requires "appropriate safeguards" for high-risk AI
- GDPR mandates explainability of automated decision-making
- Verifiable circuits provide mathematical proof of compliance, stronger than heuristic explanations

### 2. Adversarial Robustness Certification

**Use Case**: Ensure AI systems are robust to adversarial attacks on inputs

- Mechanistic interpretability reveals which circuits process adversarial perturbations
- Formal verification certifies robustness bounds (e.g., "model robust to ±0.01 perturbation")
- Example: Language model's sentiment-detection circuit remains correct even if input embeddings are slightly corrupted

**Implication**: Verifiable Transformers provide **certified adversarial robustness** at the circuit level, complementing empirical robustness techniques.

### 3. Model Debugging and Failure Analysis

**Use Case**: Identify and fix failure modes in neural networks

- Extract circuits responsible for errors (e.g., quote-matching mistakes)
- Verify whether circuits are truly minimal and necessary
- Certify fixes: after retraining, formally verify that edge modifications produce expected behavior

**Example**: If a sentiment classifier fails on sarcasm, mechanistic interpretability identifies the responsible circuits, and Verifiable Transformers formally confirm the fix works across a bounded domain.

### 4. Mechanistic Understanding for Interpretable AI Design

**Use Case**: Design inherently interpretable neural architectures

- Verifiable Transformers encourage building models with SMT-encodable components
- This incentivizes architectures using sparsemax, ReLU-like activations, and structured attention
- Result: Models that are simultaneously performant and formally verifiable

### 5. Regulatory Compliance and Auditing

**Use Cases**:
- **Algorithm Audits**: Formal verification provides independent, auditable proof of circuit behavior
- **Model Certification**: Manufacturers can provide certificates of circuit robustness to regulators
- **Continuous Monitoring**: Periodically verify circuits as models are updated or fine-tuned

**Advantage**: Unlike black-box auditing, formal verification is exhaustive over bounded domains, not sampling-based.

## Insights & Implications

### Paradigm Shift in Mechanistic Interpretability

The paper signals a maturation of mechanistic interpretability from **exploratory science** to **formal engineering**:
- Earlier work: "We found a circuit that seems to do X" (heuristic)
- Verifiable Transformers: "We prove the circuit does exactly X on this domain" (formal)

This aligns mechanistic interpretability with established practices in formal verification (used in chip design, compiler verification, etc.).

### Limitations and Failure Cases

1. **Bounded Domain Requirement**: Verification is exhaustive only within a finite task domain (typically 100–1,280 inputs). Generalization beyond this domain is not guaranteed.
   - Mitigation: Design domains to be representative of task distribution

2. **Scalability Bottleneck**: Direct SMT verification scales to ~3-10 edge circuits at GPT-2 scale. Larger circuits require surrogate-mediated verification, which introduces approximation.
   - Open question: Can verification scale to complex multi-component circuits?

3. **Architecture Constraints**: Verification requires SMT-encodable operations (sparsemax, LeakyReLU). Practical models use GELU and softmax, necessitating surrogates.
   - Trade-off: Surrogate verification is faster but loses formal guarantees on the original model

4. **Computational Cost**: Extracting and verifying circuits is computationally intensive (solver time can exceed model inference time).
   - Applicability: Best suited for high-stakes decisions where verification cost is justified

5. **Circuit Completeness**: Extracted circuits may be incomplete—they capture the "easiest" computational path, not necessarily all causal factors.
   - Risk: A verified circuit may be correct but incomplete, leading to false confidence in explainability

### Open Research Questions

1. **How can verification scale to realistic, unsimplified Transformer architectures?**
   - Current work uses simplified models (sparsemax instead of softmax). Extending to actual GPT models is an open challenge.

2. **Can we verify compositional circuits?** Can multiple verified circuits be combined and have their combined behavior verified?
   - Important for understanding hierarchical reasoning in large models

3. **How does verification relate to downstream task performance?** Does a verified circuit necessarily produce robust, generalizable behavior?
   - Formal verification guarantees correctness on bounded domain, not generalization

4. **Can interactive theorem provers be integrated** to provide even stronger guarantees (e.g., using Coq or Lean)?

### Influence on Future xAI Research

This work will likely inspire:

1. **Verifiable Circuit Extraction**: New methods designed from scratch for formal verification, not just post-hoc validation
2. **Mechanistic Alignment**: Using verified circuits to ensure AI systems align with human values and regulatory requirements
3. **Interpretable Architecture Design**: Neural architectures optimized for verifiability, not just accuracy
4. **Formal Semantics for NNs**: Developing mathematical foundations for neural network behavior, akin to programming language semantics

## Code & Resources

### Official Repository

- **GitHub**: [Neel Somani's Verifiable Transformers implementation](https://github.com/nsomani/verifiable-transformers) (if available)
- **ArXiv Preprint**: [2605.24033](https://arxiv.org/abs/2605.24033) with appendix containing implementation details

### Dependencies & Computational Requirements

**Core Libraries**:
- **PyTorch** (for model training and circuit extraction)
- **Z3 Theorem Prover** (SMT solver, open-source)
- **NumPy/SciPy** (numerical computation)

**Computational Requirements**:
- CPU-based SMT solving: 
  - Small tasks (100 prompts): 1–10 seconds per verification
  - GPT-2 scale (1,280 prompts): [Estimated computation time — see paper]
- GPU optional: Speeds up model inference during circuit extraction

**Model Training**:
- Small symbolic models: <1 minute on CPU
- GPT-2 modified architecture: Standard training infrastructure (hours on GPU)

### Quick Start Guide

1. **Install dependencies**: Z3 Python bindings, PyTorch
2. **Define task domain**: Specify inputs, ground-truth outputs, and behavioral targets
3. **Train model**: Use SMT-encodable architecture (sparsemax, LeakyReLU)
4. **Extract circuit**: Apply attention-based or gradient-based circuit extraction methods
5. **Verify with Verifiable Transformers framework**: Encode circuit as SMT formula, run solver
6. **Interpret results**: Check which properties hold, identify edge necessity

### Interactive Visualizations & Demos

- **Attention Visualization**: Tools for inspecting attention patterns within verified circuits
- **Interactive Verification UI** [if provided]: Web-based interface to explore circuit properties and verification results
- **Benchmark Datasets**: Symbolic tasks (quote closing, bracket matching) for reproducible verification experiments

## Related Work & Context

### Mechanistic Interpretability Background

The work builds on foundational mechanistic interpretability papers:

- **Circuits (Zoom In)**: Chris Olah's "Zoom In" work (2020) identifying attention-head circuits in language models
- **Circuit Motifs**: Work identifying recurring computational patterns in transformers
- **Lottery Ticket Hypothesis**: Related work on finding sparse subnetworks within neural networks

**Distinction**: Previous work identified circuits heuristically; Verifiable Transformers formalizes the validation process.

### Formal Verification in AI

Related approaches in formal verification:

1. **Certified Robustness**: Work on provably robust neural networks (e.g., Certified Defenses against Adversarial Examples)
2. **Formal Semantics**: Applying formal methods from programming languages to neural networks
3. **SAT/SMT Solvers for NNs**: Prior work using satisfiability solvers for neural network verification (Reluplex, Marabou)

**Novelty**: Verifiable Transformers applies formal verification specifically to circuit semantics, not just input-output robustness.

### Competing Interpretability Approaches

**Post-hoc Attribution Methods** (LIME, SHAP, Integrated Gradients):
- Advantage: Model-agnostic, fast
- Disadvantage: Heuristic validation, no formal guarantees
- Verifiable Transformers: Provides formal guarantees via mechanistic circuits

**Concept-Based Explanations**:
- Advantage: Human-interpretable concepts
- Disadvantage: Concepts may not compose into circuits
- Verifiable Transformers: Focuses on sub-components (circuits), not high-level concepts

**Inherently Interpretable Models**:
- Advantage: Designed for transparency from scratch
- Disadvantage: Often lower accuracy
- Verifiable Transformers: Works with powerful models but requires SMT-encodable operators

### Community Context

This work sits at the intersection of:

1. **Mechanistic Interpretability Community**: Anthropic, OpenAI, UC Berkeley Redwood Research
2. **Formal Verification Community**: Researchers from SAT/SMT, program verification, EDA (electronic design automation)
3. **Trustworthy AI/Alignment**: Focus on making AI systems more understandable and certifiable

**Broader Trend**: Mechanistic interpretability is maturing from qualitative circuit discovery to quantitative, formal circuit analysis.

## Conclusion

"Towards Verifiable Transformers" represents a significant step forward in making AI explainability rigorous and trustworthy. By introducing formal verification to mechanistic interpretability, the work bridges the gap between "plausible" and "proven" circuit behavior. While current approaches scale only to simplified models and bounded domains, the framework provides a foundation for future work on certified neural network behavior.

The implications are profound: as AI systems are deployed in high-stakes domains (healthcare, law, finance), the ability to formally verify circuit behavior offers a path toward trustworthy, regulatorily compliant AI. The work also incentivizes the design of inherently interpretable architectures optimized for formal verification.

For researchers in xAI, mechanistic interpretability, and formal verification, this paper opens new research directions: scaling verification to realistic models, verifying compositional circuits, and integrating theorem provers for even stronger guarantees.
