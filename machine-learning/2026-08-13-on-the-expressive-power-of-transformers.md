# On the Expressive Power of Transformers

**ArXiv ID:** 2608.12671  
**Authors:** Phokion Kolaitis, Rik Sengupta  
**Submitted:** August 13, 2026  
**Pages:** 13 (with 2 figures)

## Executive Summary

This paper provides a comprehensive theoretical analysis of transformer expressive power using circuit complexity, a foundational framework from computational complexity theory. By precisely characterizing what transformers can and cannot compute as language recognizers, the work establishes connections between transformer capabilities and established computational complexity classes. This theoretical foundation is essential for understanding the capabilities and limitations of large language models, which are ubiquitously built on transformer architectures.

## Problem Statement

Understanding transformer expressive power addresses fundamental questions about LLMs:

1. **What Can Transformers Compute?** What computational problems can transformers solve? Are there inherent limitations?

2. **Comparison with Other Models:** How do transformers compare to:
   - Recurrent neural networks (RNNs)
   - Classical automata (finite automata, pushdown automata)
   - Standard complexity classes (P, NP, NC)

3. **Resource-Complexity Trade-offs:** How do transformer capabilities scale with:
   - Number of layers (depth)
   - Attention head count
   - Model precision
   - Sequence length

4. **Theoretical Gaps:** Current understanding relies on empirical observations; formal theoretical characterization is lacking

5. **Design Implications:** Understanding expressive power can inform architectural choices for specific applications

Previous work on transformer expressiveness was fragmented, using different theoretical frameworks. This work unifies understanding through circuit complexity.

## Core Concepts & Theory

### Circuit Complexity Framework

**Why Circuit Complexity?**

Circuit complexity is the natural framework because:
- Parameterizes computational devices by physical constraints (size, depth, gate types)
- Transformers naturally map to circuits with specific resource constraints
- Provides precise characterization of what can/cannot be computed under resource limits

**Basic Definitions:**

A boolean circuit is a directed acyclic graph (DAG) where:
- **Inputs:** Input variables x₁, x₂, ..., xₙ
- **Gates:** Operations (AND, OR, NOT, etc.)
- **Outputs:** Final computed values
- **Complexity Measures:**
  - **Size:** Total number of gates
  - **Depth:** Longest path from input to output

### Transformer-to-Circuit Mapping

Transformers can be viewed as circuits with specific constraints:

```
Transformer Component → Circuit Equivalent
─────────────────────────────────────────
Self-attention layer → Permutation matrix + weighted sum
Feed-forward network → Polynomial threshold function
Layer composition → Circuit composition (depth)
Multi-head attention → Circuit with parallelism
Positional encoding → Additional input channels
```

### Complexity Classes

**Key Complexity Classes for Transformers:**

1. **AC⁰ (Constant-depth circuits):** Polynomial-size circuits with constant depth using AND, OR, NOT gates
   - Can compute basic operations (parity with unbounded fan-in)
   - Cannot compute certain functions (general sorting)

2. **NC¹ (Nick's class):** Logarithmic-depth circuits with bounded fan-in
   - More powerful than AC⁰
   - Can compute tree-like structures

3. **NC (Nick's class):** Logarithmic-depth, polynomial-size circuits
   - Captures "efficiently parallelizable" problems

4. **P:** Polynomial-time solvable problems
   - Upper bound on transformer capability (polynomial in sequence length)

### Attention Mechanism Analysis

Self-attention can be viewed as:

```
Attention(Q, K, V) = softmax(QK^T / √d_k)V

Circuit equivalent:
- Matrix multiplication → Polynomial threshold gates
- Softmax → Approximated by threshold functions
- Output selection → Multiplexer circuits
```

**Key Properties:**
- Single attention head can implement O(n²) comparisons
- Multiple heads enable parallel computation
- Attention pattern can vary with input (dynamic structure)

## Main Ideas & Contributions

### 1. **Unified Theoretical Framework**

The paper establishes a systematic framework for analyzing transformer expressive power:
- **Precise Definitions:** Formal characterization of transformer families parameterized by resources
- **Complexity Bounds:** Formal upper and lower bounds on computable functions
- **Unified Notation:** Consistent terminology across different transformer variants

### 2. **Expressive Power Characterization**

Key theoretical results on what transformers can compute:

**With Bounded Precision:**
- Transformers with O(log n) precision can compute problems in NC hierarchy
- Limited precision leads to NC¹ (logarithmic depth) capability ceiling

**With Full Precision:**
- Transformer depth d can access information from all previous layers (polynomial depth)
- Upper bound: Anything computable in polynomial time

**With Specific Attention Patterns:**
- Sparse attention (local windows) → NC-level complexity
- Dense attention (all-to-all) → Higher complexity potential

### 3. **Separation Results**

The paper proves separation results showing inherent limitations:
- Some functions require exponential number of layers
- Attention heads provide parallelism but limited computational benefit beyond O(log n)
- Sequence length limitations emerge from circuit depth considerations

### 4. **Comparison with Other Models**

Establishes relationships between transformer complexity and:
- Classical automata (finite automata ⊂ bounded-depth transformers ⊂ general transformers)
- RNNs (Turing completeness vs. transformer limitations)
- Neural networks (depth vs. width trade-offs)

## Methodology & Implementation

### Theoretical Analysis Approach

1. **Circuit Encoding:** Map transformer computations to boolean circuits with specific resources
2. **Lower Bounds:** Prove what cannot be computed using adversarial arguments
3. **Upper Bounds:** Construct circuits showing what can be computed
4. **Complexity Reduction:** Establish relationships between known complexity classes

### Key Proof Techniques

**Depth Reduction:**
- Show that k-layer transformer can be simulated by constant-depth circuit with exponential size
- Establish minimum depth requirements for certain problems

**Information Flow Analysis:**
- Track what information is available at each layer
- Prove that some long-range dependencies require linear depth

**Hardness Proofs:**
- Use known lower bounds from circuit complexity
- Show transformers inherit these limitations

### Experimental Validation (Theoretical)

While primarily theoretical, the paper validates insights through:
- Consistency checks against known transformer behavior
- Verification that theoretical bounds align with empirical observations
- Analysis of published transformer results in light of expressive power

**[Exact figures unavailable — see full paper]** regarding:
- Specific complexity bounds for common transformer sizes
- Quantitative trade-offs between precision and depth
- Empirical validation on standard benchmarks

## Practical Applications & Use Cases

### 1. **Architecture Design Guidance**

Understanding expressive power informs design choices:
- **Depth Requirements:** How many layers needed for target problem class?
- **Width vs. Depth:** Trade-offs in model design for given compute budget
- **Attention Configuration:** Sparse vs. dense attention implications

### 2. **Capability Assessment**

For domain practitioners:
- **Problem Complexity:** Assess whether problem is in transformer's capability class
- **Fundamental Limits:** Identify if problem may be hard even with bigger models
- **Hybrid Approaches:** Determine when transformers need augmentation with other techniques

### 3. **Model Compression and Optimization**

- **Depth Reduction:** Theoretical guidance for depth-to-width conversion
- **Precision Quantization:** Understanding minimum precision requirements
- **Layer Pruning:** Identifying less critical computational layers

### 4. **Verification and Safety**

- **Certified Bounds:** Establish formal guarantees on model behavior
- **Uncertainty Quantification:** Theoretical backing for confidence in predictions
- **Out-of-Distribution Detection:** Understanding when transformers reach capability limits

### Practical Challenges

- **Theory-Practice Gap:** Theoretical bounds may be loose compared to actual performance
- **Approximation vs. Exact:** In practice, transformers use approximate functions (softmax), not exact circuits
- **Stochasticity:** Training introduces randomness not captured in circuit model

## Insights & Implications

### Theoretical Insights

1. **Fundamental Limitations:** Transformers have inherent computational boundaries despite impressive empirical performance

2. **Depth-Expressiveness Trade-off:** Expressive power fundamentally requires depth; width alone cannot compensate

3. **Precision Sensitivity:** Model precision (bit-width) critically affects computable function class

4. **Attention's Role:** While critical for practical efficiency, attention doesn't fundamentally expand computable class beyond what circuits can do

### Field Impact

1. **Foundation for Understanding LLMs:** Provides theoretical grounding for understanding why LLMs work and where they have limits

2. **State-of-the-Art in Theory:** Advances complexity-theoretic understanding to match practical transformer ubiquity

3. **Guidance for Future Architectures:** Informs design of next-generation models beyond transformers

### Limitations and Open Questions

1. **Approximation Error:** Theory assumes exact computation; practical softmax uses approximations

2. **Training Dynamics:** Expressive power doesn't guarantee effective learnability

3. **Specific Functions:** While general complexity classes are characterized, specific problem complexities may be harder

4. **Scale Effects:** Theory may not capture emergent phenomena at extreme model scales

5. **Multimodal Transformers:** Theoretical framework developed for language; extensions to vision/multimodal unclear

## Code & Resources

This is a theoretical paper without code artifacts.

**Paper Resources:**
- ArXiv PDF: https://arxiv.org/pdf/2608.12671
- ArXiv HTML: https://arxiv.org/html/2608.12671

**Related Implementation Resources:**
- Circuit complexity libraries (e.g., ACiD framework for analyzing neural circuit complexity)
- Transformer architecture repositories (PyTorch transformers)
- Verification tools for neural networks (e.g., Marabou, Reluplex)

## Related Work & Context

### Prior Theoretical Work on Transformers

**Expressiveness Analysis:**
- "Transformers Provably Learn Chain-of-Thought Reasoning" (2511.07378): Studies what chain-of-thought patterns transformers can learn
- "The Expressive Power of Transformers with Chain of Thought" (2310.07923): Analyzes expressiveness with CoT reasoning
- "Transformers, Parallel Computation, and Logarithmic Depth" (2402.09268): Studies parallel computation aspects

**Circuit Complexity Connections:**
- "On the Expressive Power of Transformers for Maxout Networks and Continuous Piecewise Linear Functions" (2603.03084): Related expressive power analysis

### Foundational Complexity Theory

**Classical Results:**
- Barrington's theorem: Relating NC and circuit classes
- Razborov's lower bounds: Establishing fundamental limits on computation
- Boole's algebra: Foundation for circuit and logical analysis

### Future Research Directions

1. **Tighter Bounds:** Refining circuit complexity bounds to match empirical performance more closely

2. **Stochastic Analysis:** Extending theory to handle randomness in training and inference

3. **Architectural Variants:** Circuit complexity analysis for vision transformers, mixture-of-experts, and other variants

4. **Learning Dynamics:** Understanding how training finds solutions within expressive power boundaries

5. **Hybrid Models:** Analyzing expressive power of transformers combined with other techniques

6. **Emergent Capabilities:** Theoretical framework for understanding capability emergence at scale

---

**Keywords:** Transformers, Expressive Power, Circuit Complexity, Computational Complexity, Language Recognizers, Theory, LLMs
