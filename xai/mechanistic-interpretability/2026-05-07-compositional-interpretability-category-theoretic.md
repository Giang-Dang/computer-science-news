# From Mechanistic to Compositional Interpretability: A Category-Theoretic Framework

**ArXiv ID:** 2605.08934  
**Authors:** Ward Gauderis, Thomas Dooms, Steven T. Holmer, Kola Ayonrinde, Geraint A. Wiggins  
**Published:** May 2026  
**Category:** Mechanistic Interpretability

## Executive Summary

This paper introduces **compositional interpretability**, a category-theoretic framework that provides formal mathematical foundations for mechanistic interpretability. By treating mechanistic explanations as syntactic-semantic pairs that must satisfy commutative diagrams, the work addresses the critical challenge of verifying, comparing, and composing neural network explanations in a principled, objective manner. This theoretical advance enables automating the discovery and evaluation of mechanistic explanations while providing theoretical guarantees about explanation quality and human interpretability.

## Problem Statement

Despite significant advances in mechanistic interpretability—the field focused on reverse-engineering neural networks to understand their internal computations—a fundamental gap remains: **how can we objectively verify, compare, and compose mechanistic explanations?**

Current mechanistic interpretability approaches suffer from several critical limitations:

1. **Lack of Formal Framework**: Most mechanistic methods (circuit analysis, sparse autoencoders, attention head dissection) operate intuitively without formal verification mechanisms. Different researchers may propose conflicting explanations for the same phenomenon with no principled way to adjudicate between them.

2. **Compositionality Problem**: Neural network explanations are typically isolated, describing individual components or circuits. But the field lacks a systematic way to compose these local explanations into comprehensive global understanding of model behavior.

3. **Verification Absence**: Without formal criteria, there's no objective way to validate that a discovered mechanistic explanation is correct, complete, or truly explains the behavior it claims to account for.

4. **Interpretability-Fidelity Tradeoff**: Current mechanistic explanations often prioritize fidelity to model behavior over human understandability. There's no principled framework to optimize for human-aligned interpretability while maintaining explanatory power.

5. **Non-Uniform Evaluation**: Different mechanistic interpretability papers use different evaluation criteria, making it difficult to assess progress and compare methods systematically.

These limitations prevent mechanistic interpretability from becoming a rigorous scientific discipline with cumulative progress and shared standards.

## Core Concepts & Theory

### 1. **Category Theory Foundations**

The paper applies category theory—a branch of mathematics focused on abstract structure and relationships—to mechanistic interpretability. Key concepts include:

**Categories**: A category consists of objects and morphisms (arrows) between them that satisfy composition and identity properties. In this framework:
- Objects represent neural network components or behaviors
- Morphisms represent transformations or mappings between them

**Functors**: Structure-preserving mappings between categories that enable translation between different representations of the same phenomenon.

**Commutative Diagrams**: Visual representations where multiple paths through different morphisms produce the same result. This ensures consistency across different explanations.

### 2. **Syntactic-Semantic Duality**

The framework treats mechanistic explanations as pairs (S, Σ) where:

- **Syntactic mapping (S)**: A compression or description of the neural network's computational structure (e.g., identifying key neurons, weights, or circuits)
- **Semantic mapping (Σ)**: A human-interpretable interpretation or meaning assigned to the syntactic elements

**Critical Requirement**: For a valid explanation, these must **commute** in a categorical sense—the semantic interpretation derived from the syntax should match the semantic interpretation of the original behavior.

Formally, if we have a neural network N with input X and output Y:

```
              N
    X ─────────────→ Y
    │               │
    S               Σ
    ↓               ↓
Syntax Rep ─Sem─→ Semantic Rep
```

The commutative property ensures: S(X) semantic-interpretation should equal Σ(Y).

### 3. **Minimum Description Length (MDL) Principle**

The paper grounds compositional interpretability in MDL, which states that the best explanation is the one that compresses the data most efficiently. In this context:

- **Parsimony**: Shorter syntactic descriptions are preferred (fewer neurons, simpler circuits)
- **Compression Guarantee**: Under certain conditions, syntactic compression theoretically guarantees more concise, human-aligned explanations
- **Trade-off**: Balance between compression (simplicity) and semantic fidelity (correctness)

### 4. **Refinement and Specification**

The framework enables formal relationships between explanations:

- **Refinement**: Explanation E₂ refines E₁ if it provides more detailed decomposition while maintaining consistency
- **Specification**: An explanation at multiple levels of abstraction (coarse-grained circuits vs. fine-grained neurons)
- **Composability**: Refined explanations can be composed from simpler explanations through morphism composition

This enables a hierarchy of mechanistic understanding, from high-level behavioral descriptions to low-level implementation details.

## Main Ideas & Key Contributions

### 1. **Formal Foundations for Mechanistic Interpretability**

The paper's primary contribution is elevating mechanistic interpretability from an engineering discipline to a formal science by providing:

- Mathematical definitions of what constitutes a valid mechanistic explanation
- Objective criteria for comparing competing explanations
- Principled methods for verifying explanation correctness

### 2. **Theoretical Justification for Existing Methods**

By formalizing the framework, the paper shows that many existing mechanistic interpretability methods can be understood as specific instances of compositional interpretability:

- **Sparse Autoencoders (SAEs)**: Perform syntactic compression by discovering sparse, interpretable features
- **Circuit Analysis**: Identify syntactic patterns (attention heads, feed-forward neurons) that compose into meaningful circuits
- **Attention Analysis**: Maps attention patterns (syntax) to information flow interpretations (semantics)

The framework explains *why* the compression heuristics used by these methods tend to align with human interpretability—it's not accidental but follows from MDL principles.

### 3. **Automation and Discovery Framework**

The category-theoretic structure enables automated:

- **Explanation Discovery**: Systematically search the space of possible explanations for those that satisfy parsimony and compositionality constraints
- **Consistency Checking**: Verify that proposed explanations commute correctly
- **Explanation Refinement**: Decompose coarse-grained explanations into more detailed compositional structures

### 4. **Composability of Explanations**

Unlike prior work that treats explanations as isolated insights, the framework enables:

- **Hierarchical Understanding**: Build explanations from simple components to complex behaviors
- **Local-to-Global**: Compose local circuit explanations into comprehensive model understanding
- **Modular Reasoning**: Reuse verified explanation components across different analyses

### 5. **Reconciling Competing Goals**

The framework provides formal mechanisms to balance:

- **Fidelity vs. Interpretability**: Mathematical trade-offs rather than ad-hoc compromises
- **Compression vs. Completeness**: Principled optimization between simplicity and thoroughness
- **Different Stakeholders**: Formal specification allows adaptation for different audiences (researchers vs. practitioners)

## Methodology & Implementation

### 1. **Explanation Specification Process**

The practical workflow for generating compositional interpretations:

```
1. Initialize: Select neural network component to explain
   ↓
2. Syntactic Discovery: Identify key components (neurons, circuits)
   ↓
3. Semantic Mapping: Assign interpretations to components
   ↓
4. Commutativity Check: Verify explanation consistency
   ↓
5. Compression Analysis: Evaluate parsimony (MDL score)
   ↓
6. Refinement: Decompose into more detailed explanations
   ↓
7. Composability: Check compatibility with other explanations
```

### 2. **Evaluation Metrics**

The framework provides formal evaluation criteria:

**Syntactic Quality:**
- **Compression Ratio**: Size of explanation representation vs. original network
- **Sparsity**: Proportion of model components involved in explanation
- **Modularity**: Independence of explanation components

**Semantic Quality:**
- **Commutativity Score**: How well does the semantic interpretation match model behavior?
- **Human Alignment**: Do human evaluators find the explanation intuitive?
- **Actionability**: Can the explanation be used to predict model behavior in new contexts?

**Compositional Quality:**
- **Consistency**: Do multiple interpretations of the same phenomenon agree?
- **Composability**: Can explanations be combined without contradiction?
- **Completeness**: Does the compositional explanation account for model behavior?

### 3. **Formal Definitions**

**Valid Compositional Explanation**: A pair (S, Σ) where:
- S is a syntactic compression of model computation
- Σ is a semantic interpretation mapping
- The diagram S → Σ commutes with the original behavior
- Compression ratio satisfies MDL bound
- Explanation components form a composable structure

**Refinement Relation**: E₂ refines E₁ if:
- E₂ provides more detailed decomposition of E₁'s components
- All compositional properties are preserved
- Compression increases minimally (ε-bounded)

**Composition Operation**: Explanations E₁ and E₂ compose if:
- Their syntactic components don't conflict
- Their semantic interpretations are compatible
- The resulting composition satisfies commutativity

### 4. **Automation Algorithms**

The framework enables algorithmic approaches:

**Automated Discovery**: Use constraint satisfaction or optimization to find explanations that:
- Maximize compression (minimize description length)
- Maximize commutativity (explanation-behavior match)
- Maximize composability (compatibility with existing explanations)

**Consistency Verification**: Automated checking of commutativity properties through:
- Intervention analysis (perturb syntax, measure semantic impact)
- Cross-validation (test explanation on held-out behaviors)
- Redundancy analysis (verify no over-specification)

**Refinement Recommendation**: Suggest decompositions that:
- Improve human interpretability without sacrificing fidelity
- Increase modularity and composability
- Enable more detailed understanding

## Practical Applications & Real-World Use Cases

### 1. **Safety-Critical AI Systems**

**Healthcare Diagnosis**: Mechanistic explanations of clinical AI models

- Use compositional interpretability to verify decision-making processes
- Decompose high-stakes predictions into verified components
- Enable physicians to understand model reasoning for regulatory compliance
- Application: FDA approval of clinical AI systems requires formal verification of decision logic

**Autonomous Systems**: Explain vehicle behavior in edge cases

- Compose explanations of sensor processing, threat detection, and action selection
- Verify that explanations remain consistent across scenarios
- Formal proof that critical components operate as intended
- Regulatory compliance for autonomous vehicle certification

### 2. **Scientific Discovery**

**Physics-Informed ML**: Interpret models trained on physical simulations

- Use compositional framework to verify that models discover intended physical principles
- Identify when models exploit spurious correlations vs. learning true physics
- Compose local mechanistic insights into unified physical understanding
- Accelerate discovery of physical laws by analyzing learned mechanisms

**Biology & Genomics**: Understand neural models of biological systems

- Explain how models represent genes, proteins, regulatory networks
- Verify biological plausibility of learned representations
- Compose cellular-level mechanisms into systems-level understanding
- Validate that model insights match experimental biology

### 3. **Adversarial Robustness**

**Attack Analysis**: Understand mechanistic basis of adversarial vulnerability

- Explain which circuits are exploited by adversarial examples
- Use compositionality to trace adversarial perturbations through model layers
- Verify that defenses eliminate vulnerable circuits
- Identify minimum-sufficient mechanisms for robustness

**Defense Verification**: Formally verify robustness claims

- Prove that proposed defenses eliminate all attack paths
- Compose robustness properties across model layers
- Detect cases where defense breaks important non-adversarial functionality

### 4. **Model Editing and Control**

**Mechanistic Intervention**: Modify models based on causal understanding

- Identify causal circuits responsible for undesired behavior
- Edit neurons/connections with confidence (verified through compositionality)
- Ensure edits don't break other model capabilities via compositional checking
- Example: Remove bias circuits while preserving utility

**Steering and Alignment**: Direct model behavior toward human values

- Mechanistically identify value-relevant circuits
- Compose value-alignment mechanisms across model layers
- Verify that steering interventions preserve general capability
- Enable interpretable AI alignment methods

### 5. **Regulatory Compliance**

**AI Governance**: Provide verifiable explanations for regulatory bodies

- EU AI Act compliance: Demonstrate high-risk systems are interpretable
- FDA approval: Provide formal verification of clinical AI decisions
- Fair lending compliance: Trace credit decisions to verified decision logic
- DPA/GDPR: Right to explanation with formal guarantees

### 6. **Model Debugging and Improvement**

**Root Cause Analysis**: Diagnose model failures mechanistically

- When model fails, trace failure to specific circuits/components
- Understand interaction of multiple circuits causing failure
- Fix underlying mechanisms rather than patching with more data
- Reduce debugging time and improve model reliability

**Capability Discovery**: Understand what models can do and why

- Systematically catalog model capabilities by mechanistic component
- Predict performance on new tasks based on mechanism analysis
- Identify transfer learning opportunities through circuit reuse
- Accelerate model design by understanding successful patterns

## Insights & Implications

### 1. **Paradigm Shift in Interpretability**

This work represents a fundamental shift from viewing interpretability as a post-hoc explanation problem to understanding it as a **formal scientific discipline with rigorous standards**.

- **Before**: Interpretability = producing plausible-sounding explanations
- **After**: Interpretability = verifiable, composable, formally grounded understanding

This changes how the field evaluates and communicates mechanistic insights.

### 2. **Theoretical Guarantees for Human Alignment**

The paper proves that under MDL principles, syntactic compression provides theoretical guarantees about human interpretability:

- Simple, compressed explanations are more likely to match human intuitions
- This explains (rather than assumes) why practitioners' heuristics work
- Opens path to formally optimizing for human understanding, not just model behavior

### 3. **Mechanistic Methods as Compression Algorithms**

The framework reveals that existing mechanistic interpretability methods fundamentally perform **compression**:

- SAEs discover sparse features (compression of activations)
- Circuits identify relevant subgraphs (compression of connections)
- Attention analysis finds information pathways (compression of computation)

Understanding this unifies the field and suggests new compression-based methods.

### 4. **Unresolved Challenges and Limitations**

Despite the theoretical framework, important challenges remain:

**Empirical Verification**: How do we validate that compositional explanations are actually correct? Category theory provides structure, but empirical validation is non-trivial.

**Scalability**: Compositionality enables understanding but may not scale to very large models (billions of parameters). How do we maintain composability at scale?

**Semantic Specification**: The framework is agnostic about what constitutes a valid semantic interpretation. Different stakeholders may have different semantic requirements.

**Computational Complexity**: Automated discovery of optimal compositional explanations may be NP-hard. Practical algorithms may require heuristics.

**Human Evaluation**: While the framework claims to optimize for human interpretability, actual human studies comparing competing compositional explanations are limited.

### 5. **Future Research Directions**

The framework opens several promising research avenues:

**Automated Mechanism Discovery**: Use the compositional structure to automatically discover new mechanistic insights without human guidance.

**Cross-Model Composition**: Compose mechanisms across different architectures and model families, enabling transfer of interpretability insights.

**Compositional Alignment**: Use compositional structure to more efficiently align models with human values and preferences.

**Formal Verification for ML**: Extend formal verification techniques from software engineering to ML systems based on mechanistic understanding.

**Interpretability-Performance Tradeoff**: Systematically study how different levels of interpretability (coarse compositional vs. fine-grained mechanistic) affect model performance and robustness.

## Code & Resources

### Official Implementation and Artifacts

**Paper Repository**: The authors have provided resources for implementation of compositional interpretability:
- ArXiv Paper: https://arxiv.org/abs/2605.08934
- Potential Implementation: https://github.com/CompInterp (Compositional Interpretability community)

### Related Open-Source Projects

**Mechanistic Interpretability Tools**:
- **Circuits Benchmark** (OpenAI/Anthropic): Framework for mechanistic interpretability research
- **SAE Interpretability** (Anthropic): Tools for sparse autoencoder analysis
- **Transformer Circuits**: Resource for understanding transformer mechanisms (https://transformer-circuits.pub)

**Category Theory in ML**:
- **Categorical ML**: Emerging libraries implementing category-theoretic approaches
- **Computational Category Theory**: Tools for formal verification of compositional properties

### Dependencies and Requirements

**Theoretical**:
- Category theory fundamentals (ring theory, homological algebra)
- Information theory (Minimum Description Length, Kolmogorov complexity)
- Graph theory (for circuit representation)

**Computational**:
- Python 3.8+
- PyTorch or JAX (for mechanistic analysis)
- SAE training frameworks (TransformerLens, etc.)
- Graph databases for storing/querying explanations

### Quick Start

While the paper is primarily theoretical, practitioners can begin applying compositional interpretability by:

1. **Identify a mechanistic question** (e.g., "Which circuits compute gender in BERT?")
2. **Extract syntactic components** (neurons, attention heads, circuits)
3. **Define semantic mappings** (what does each component mean?)
4. **Check commutativity** (does explanation behavior match model behavior?)
5. **Compress and refine** (remove redundant components, enable decomposition)
6. **Compose hierarchically** (build larger explanations from smaller ones)

### Implementations in Development

The framework has inspired follow-up work implementing compositional interpretability:

- **PIE (Prune, Interpret, Evaluate)** (2604.16889): Cross-layer circuit discovery using feature attribution
- **Automated Interpretability with Agents** (2605.01555): Multiagent systems for automated explanation discovery
- Various university research groups implementing category-theoretic verification systems

## Related Work & Context

### 1. **Mechanistic Interpretability Foundations**

This paper builds on the mechanistic interpretability research program initiated by:

**Foundational Works**:
- "Zoom In: An Introduction to Circuits" (Olsson et al., 2020): Pioneered circuit analysis as reverse engineering of neural networks
- "Interpretability in the Wild" (Conmy et al., 2023): Extended circuit analysis to real-world models
- "Sparse Autoencoders Reveal the Structure of Neural Networks" (Bricken et al., 2023): SAE framework for discovering interpretable features

**Competing Mechanistic Approaches**:
- **Attention-Based Explanation**: Understanding through attention patterns (though attention doesn't necessarily explain computation)
- **Neuron Activation Analysis**: Feature importance through individual neuron effects
- **Influence Functions**: Tracing model predictions back to training examples

### 2. **Category Theory in AI**

The application of category theory to ML interpretability connects to broader efforts:

- **Categorical Learning Theory**: Formal frameworks for learning and inference
- **Compositional Semantics in NLP**: Using category theory for language understanding
- **Applied Category Theory**: Growing field applying abstract mathematics to practical problems

### 3. **Formal Verification in ML**

Related work on making ML systems formally verifiable:

- **Certified Robustness**: Formal guarantees about adversarial robustness
- **Specification Learning**: Automatically inferring formal specifications from models
- **Symbolic AI Integration**: Combining neural and symbolic approaches for interpretability

### 4. **Human-Centered Interpretability**

Complementary research on making explanations useful for humans:

- **Cognitive Science of Explanations**: How humans understand explanations (Lombrozo et al.)
- **Explanation Evaluation**: Metrics for measuring explanation quality beyond fidelity
- **Interactive Interpretability**: Human-in-the-loop explanation refinement

### 5. **Connection to Other xAI Paradigms**

How compositional interpretability relates to established explainability approaches:

| Approach | Focus | Contribution |
|----------|-------|--------------|
| **LIME/SHAP** | Local explanations, feature attribution | Agnostic to mechanism; complements formal verification |
| **Concept-Based** | Human-friendly concepts | Provides semantic mappings for composition |
| **Causal Inference** | Causal relationships | Compositional framework enables causal verification |
| **Attention Analysis** | Information flow | Component of syntactic-semantic mapping |
| **SAEs** | Interpretable features | Specific instance of compositional compression |

### 6. **Broader XAI Community Context**

This work advances fundamental goals shared across the xAI community:

**Interpretable ML**: The paper shows mechanistic approaches are special case of compression-based interpretability, unifying different research threads.

**Trustworthy AI**: Formal verification enables stronger trust through rigorous verification rather than empirical plausibility.

**AI Safety**: Compositional mechanisms provide new tools for alignment verification and safety property checking.

**Scientific Discovery**: Formal framework enables using mechanistic interpretability for true scientific discovery rather than just engineering explanation.

### 7. **Competing Frameworks**

While embracing the mechanistic paradigm, the paper implicitly compares to alternative approaches:

- **Symbolic reasoning**: More formally tractable but less suited to neural computation
- **Pure behavioral explanations**: Easier to verify but less insightful about mechanism
- **Statistical interpretability**: Established but may not capture causal structure
- **Black-box post-hoc methods**: Practical but lack formal guarantees

### 8. **Next Frontiers in Mechanistic Interpretability**

This paper opens doors to future work building on compositional foundations:

**Mechanistic Alignment**: Use compositional understanding to align model behavior with human values at the circuit level.

**Model Surgery**: Compositional verification enables safe, principled edits to neural networks.

**Cross-Architecture Composition**: Share mechanistic understanding across different model families.

**Formal Proof Systems for ML**: Develop formal proof verification for neural network properties.

**Mechanistic Scaling Laws**: Understand how mechanistic properties change as models scale.

---

## Summary

**"From Mechanistic to Compositional Interpretability"** provides theoretical foundations that elevate mechanistic interpretability from engineering practice to formal science. By applying category theory and information theory, the paper enables:

1. **Formal verification** of mechanistic explanations
2. **Systematic composition** of local insights into global understanding
3. **Theoretical guarantees** about explanation quality and human interpretability
4. **Automated discovery** and refinement of mechanisms
5. **Principled evaluation** and comparison of competing explanations

This work is foundational for the future of interpretable AI, enabling the field to make claims with mathematical rigor while maintaining practical applicability to real neural networks. The compositional framework will likely influence mechanistic interpretability research for years to come, providing the theoretical backbone for systematic progress toward truly interpretable AI systems.
