# Feature Attribution from First Principles

**Authors:** Magamed Taimeskhanov, Damien Garreau  
**ArXiv ID:** [2505.24729](https://arxiv.org/abs/2505.24729)  
**Affiliation:** Julius-Maximilians Universität Würzburg, CAIDAS (Center for Artificial Intelligence and Data Science)  
**Publication Date:** May 30, 2025  
**Paper Length:** 30 pages, 3 figures  
**Subject Area:** Machine Learning (cs.LG)

## Executive Summary

This paper proposes a fundamental reconceptualization of feature attribution by building from first principles rather than imposing restrictive axioms. The authors introduce the **Functional-Measure Attribution (FMA)** framework grounded in measure theory and classical approximation theory, showing that existing methods (SHAP, Integrated Gradients, Partial Dependence Plots) are special cases of this unified framework. By requiring only the Linearity axiom instead of multiple restrictive constraints, this work removes artificial limitations on valid attribution methods while providing mathematical completeness, enabling principled development of new interpretability techniques.

## Problem Statement

### The Feature Attribution Challenge

Feature attribution methods assign importance scores to input features, quantifying how much each influences model predictions. This is essential for model debugging, regulatory compliance, and building trustworthy AI systems. However, the field faces critical theoretical issues:

1. **Lack of Unified Definition:** Different attribution methods (LIME, SHAP, Integrated Gradients) use different underlying assumptions, making it unclear which method is "correct" or when each should apply
2. **Restrictive Axioms:** Prior axiomatic frameworks impose multiple constraints (symmetry, dummy axiom, additivity, efficiency, monotonicity, etc.) that together are often too restrictive, eliminating valid attribution approaches
3. **Inconsistent Results:** The same model and input produce different attributions depending on method choice, with no principled framework for understanding these differences
4. **Method Proliferation:** Without unified theory, new attribution methods are developed ad hoc without clear relationship to existing approaches

### Research Gap

Prior work attempted to establish axiomatic systems that any feature attribution should satisfy. However, these constraints are often unnecessarily restrictive and eliminate valid methods. The field needs a foundational framework that:

- Avoids overly restrictive axioms
- Provides unified mathematical foundation
- Recovers existing methods as special cases
- Explains why different methods work and when they differ
- Offers flexibility for designing new methods

## Core Concepts & Theory

### Building from Indicator Functions

Rather than imposing axioms, the paper builds a feature attribution framework from the simplest possible models: **indicator functions** (binary functions that equal 1 in a region and 0 elsewhere).

**Why indicator functions?**

Classical approximation theory provides the justification: **Any continuous function defined on a compact set can be approximated arbitrarily well by a finite sum of indicator functions** (Weierstrass Approximation Theorem variant).

This theoretical foundation ensures:
- Indicator functions provide complete coverage (can approximate any continuous function)
- They serve as natural building blocks for more complex attribution methods
- The resulting framework is mathematically complete and constructive

### The FMA Framework: Functional-Measure Attribution

**Core Construction:**

1. **Step 1 - Atomic Attributions:** Define attributions for indicator functions (simplest models), establishing baseline importance scores
2. **Step 2 - Extension via Linearity:** Extend to complex models using linear combinations (respecting the Linearity axiom)
3. **Step 3 - Measure-Theoretic Formulation:** The natural extension yields a measure-theoretic framework expressed as Lebesgue–Stieltjes integrals

**Mathematical Representation:**

$$\text{Attribution} = \int \text{atomic\_attribution} \, d\mu$$

Where:
- The integral is over measure families (abstract integration tool)
- Different measure choices yield different classical methods
- Functions of bounded variation (BV) are sufficient (not requiring smoothness/differentiability)

### Key Mathematical Concepts

**Lebesgue–Stieltjes Integrals:**
- Generalization of standard Riemann integrals
- Allows integration with respect to more general measures
- Natural framework for aggregating atomic attributions
- Works with functions that are not necessarily differentiable

**Measure Theory:**
- Atomic attributions define measure families
- Integration aggregates measures across features
- Provides mathematical rigor and completeness
- Connects to probability theory (feature distributions)

**Bounded Variation:**
- Functions need not be smooth or continuous everywhere
- Only requirement: well-defined total "variation"
- Works with realistic model outputs (including step functions, decision trees)

### Why This Approach Is Principled

Unlike LIME (arbitrary local approximation) or SHAP (Shapley paths), the FMA framework:

- **Grounds all attributions in approximation theory:** Indicator functions justified by Weierstrass theorem
- **Requires minimal axioms:** Only Linearity is externally imposed; other properties emerge from measure theory
- **Mathematically complete:** All attributions expressible as Lebesgue–Stieltjes integrals
- **Avoids artificial constraints:** Previous axiomatic systems had 5+ axioms that often contradicted each other

## Main Ideas & Key Contributions

### 1. Paradigm Shift: From Axioms to First Principles

**Previous approach:**
- Propose axioms that any attribution should satisfy
- Show which methods violate axioms
- Problem: Axioms often eliminate valid methods or contradict each other

**New approach:**
- Start with simplest models (indicator functions)
- Build naturally toward complex models via linearity
- Let mathematics determine what properties emerge
- Axioms are minimal and justified, not imposed

### 2. Unified Framework: All Major Methods as Special Cases

The FMA framework shows that major attribution methods are instances of the same underlying framework with different parameter choices:

**SHAP (SHapley Additive exPlanations):**
- Recovered via: Shapley value-based atomic attributions
- Integration measure: Probability over coalitions
- Framework insight: Game-theoretic approach is one valid parameterization

**Integrated Gradients:**
- Recovered via: Path-integral-based atomic attributions
- Integration measure: Uniform measure along gradient baseline
- Framework insight: Gradient methods are natural measure-theoretic choice

**Partial Dependence Plots:**
- Recovered via: Marginal distribution-based atomic attributions
- Integration measure: Marginal probability measure
- Framework insight: Averaging is measure-theoretic integration

**LIME (Local Interpretable Model-agnostic Explanations):**
- Recovered via: Local region-specific measure families
- Framework insight: Local vs. global trade-off made mathematically explicit

### 3. Minimal Axiomatization: Only Linearity Required

Previous frameworks required multiple axioms:
- Symmetry, Dummy axiom, Additivity, Efficiency, Monotonicity, etc.
- These often contradicted each other
- Led to "forcing" methods into frameworks

**FMA approach:**
- Requires only **Linearity axiom:** Attributions should respect linear transformations
- For linear model f(x) = w·x + b, attribution must measure feature weights
- Other properties (stability, universality, consistency) **emerge from mathematics**, not imposed

**Result:** Derived Properties

| Property | Why It Matters |
|----------|----------------|
| **Stability** | Small changes in model → small changes in attribution; ensures robust explanations |
| **Constructive Universality** | Any attribution representable in framework; proves framework completeness |
| **Consistency** | Different methods consistent within framework; enables principled comparison |

### 4. Mathematical Completeness and Rigor

The measure-theoretic foundation provides:

- **Lebesgue–Stieltjes Integral Representation:** All attributions cast as integrals over atomic attributions
- **Universal Approximation:** Indicator functions enable approximation of arbitrary continuous functions
- **Rigorous Basis:** Grounded in established mathematical theory (measure theory, approximation theory)
- **Flexibility:** Works with non-smooth functions (decision trees, ReLU networks)

### 5. Practical Implications for Method Selection

The framework explains:

- **Why methods differ:** Different measure families yield different attributions
- **When they agree:** Methods agree when they correspond to same measure choice
- **How to choose:** Select atomic attribution and measure based on application needs
- **What's valid:** Any method fitting the FMA structure with Linearity is mathematically justified

## Methodology & Implementation

### Algorithmic Construction

**Phase 1: Atomic Attribution Definition**
```
For each atomic indicator function I_A(x):
  Define attribution score φ(I_A)
  This specifies the atomic attribution family
  Different families → different methods
```

**Phase 2: Extension to Complex Models**
```
For any model f(x) with regularity properties:
  Decompose f as integral of atomic attributions
  f(x) = ∫ φ(I_A) dμ
  Computation via Lebesgue–Stieltjes integration
  Result: Attribution scores for each feature
```

### Measure Family Selection

The framework doesn't prescribe which measure to use; instead, practitioners choose based on:

1. **Application domain:** Healthcare, finance, autonomous systems have different needs
2. **Model type:** Neural networks, trees, ensembles benefit from different measures
3. **Desired properties:** Local vs. global explanations, gradient-based vs. distribution-based
4. **Computational constraints:** Some integrals easier to compute than others

### Implementation Variants

**Gradient-Based Integration (Integrated Gradients):**
- Measure: Uniform along path from baseline to instance
- Computation: Path integral, feasible for differentiable models

**Game-Theoretic Integration (SHAP):**
- Measure: Coalition-based via Shapley values
- Computation: May require sampling for large feature spaces

**Distribution-Based Integration (PDP-style):**
- Measure: Marginal feature distribution
- Computation: Averaging over dataset

**Local Region Integration (LIME-style):**
- Measure: Localized around query point
- Computation: Weighted regression in local neighborhood

### Theoretical Guarantees

1. **Linearity Preservation:** For any linear model, attributions correctly measure feature weights
2. **Stability:** Small model perturbations → small attribution changes (inherited from measure-theoretic foundation)
3. **Universality:** Any continuous attribution function approximable by framework
4. **Consistency:** Results consistent across different instantiations within framework

## Practical Applications & Real-World Use Cases

### Interpretable ML Systems

**Healthcare Diagnostics:**
- Select attribution method balancing fidelity and computational cost
- Use stability guarantees to validate explanations in clinical context
- Framework provides theoretical justification for regulatory approval

**Credit Risk Assessment:**
- Choose measure family reflecting business logic
- Explain decisions based on theoretical properties
- Demonstrate compliance with fair lending laws via principled attribution

### Model Debugging and Development

**Identifying Model Biases:**
- Different measure choices reveal different potential biases
- Compare results across measures to understand failure modes
- Framework explains why methods sometimes disagree

**Hypothesis Validation:**
- Test model behavior using different parameterizations
- Use measure-theoretic foundation to validate hypotheses
- Ensure explanations are not artifacts of method choice

### Regulatory and Compliance Contexts

**Right to Explanation Requirements:**
- Framework provides theoretical justification for attribution choices
- Regulators understand principled mathematical foundation
- Documentation shows why specific method was selected

**Algorithmic Accountability:**
- Demonstrate that attribution method fits rigorous framework
- Show that explanations have mathematical guarantees (stability, linearity)
- Connect to established theory, not ad hoc heuristics

### Research and Innovation

**Designing New Attribution Methods:**
- Framework shows how to construct valid new methods
- Select atomic attribution family and measure based on problem structure
- Guarantee method satisfies Linearity and stability properties

**Domain-Specific Customization:**
- Tailor measures to domain requirements
- Combine multiple measures for specific applications
- Systematically explore method design space

## Insights & Implications

### Advancing Theoretical Understanding

1. **Explains Method Relationships:** Framework reveals why SHAP, IG, and PDP work and how they relate
2. **Removes Arbitrary Restrictions:** Shows that many prior constraints were overly limiting
3. **Enables Systematic Comparison:** Different methods become comparable within unified framework
4. **Grounds Attribution in Mathematics:** Connects feature importance to rigorous mathematical theory

### Limitations and Open Questions

**Computational Challenges:**
- Lebesgue–Stieltjes integration can be computationally expensive
- Some measure families lack closed-form solutions
- Choosing optimal measure families requires expertise
- Scalability to very high-dimensional problems not fully addressed

**Guidance and Validation:**
- Framework explains WHY methods work, not WHICH to prefer
- Non-uniqueness: Multiple valid measures exist, user must choose
- Domain-specific validation still needed despite theoretical foundation
- Human interpretability of measure-theoretic explanations unclear

**Research Frontiers:**
- **Optimal Measure Selection:** Which measures best for specific domains?
- **Computational Optimization:** Efficient integration algorithms?
- **Automated Method Selection:** Can framework suggest measures?
- **Extensions to New Learning Paradigms:** Unsupervised, reinforcement learning, generative models?
- **Human-Centered Evaluation:** Do practitioners find measure-theoretic explanations useful?

## Code & Resources

### Implementation Status

Code availability details from search results are limited. Based on the comprehensive nature of the work, implementation would require:

**Core Components:**
- Atomic attribution function specifications
- Measure family definitions
- Lebesgue–Stieltjes integration routines
- Numerical integration optimizations

**Validation Tools:**
- Recovery demonstrations (showing SHAP, IG, PDP from FMA)
- Stability verification under perturbations
- Comparative analysis with standard methods

### ArXiv and Publication

**ArXiv:** [https://arxiv.org/abs/2505.24729](https://arxiv.org/abs/2505.24729)
- Full PDF: https://arxiv.org/pdf/2505.24729
- Abstract: https://arxiv.org/abs/2505.24729

**Institutional Resources:**
- Julius-Maximilians Universität Würzburg CAIDAS
- Authors: Taimeskhanov (primary), Garreau (advisor/collaborator)

### Quick Start Approach

For practitioners wanting to apply the framework:

1. **Understand Your Model Type:** Differentiable? Tree-based? Neural network?
2. **Select Measure Family:** Based on model type and domain needs
3. **Implement Atomic Attribution:** Define how to score indicator functions
4. **Compute Integration:** Use numerical integration with chosen measure
5. **Validate Results:** Compare against known methods (SHAP/IG baseline)

## Related Work & Context

### Position in Attribution Literature

**Local Approximation Methods (LIME):**
- Traditional: Local linear model around query point
- In FMA: Special case with localized measure families
- Insight: Framework explains local vs. global trade-off

**Game-Theoretic Approaches (SHAP):**
- Traditional: Shapley values from cooperative game theory
- In FMA: Specific atomic attribution with coalition-based measure
- Unification: Game theory becomes one valid parameterization

**Gradient-Based Methods (Integrated Gradients):**
- Traditional: Path integrals through gradient space
- In FMA: Gradient-derived measures for atomic attributions
- Connection: Reveals why gradients are natural for attribution

**Marginal Methods (Partial Dependence):**
- Traditional: Average model output changes
- In FMA: Marginal probability measure-based integration
- Framework view: Natural and complete within FMA

### Key Related Works

**Foundational Papers:**
- Integrated Gradients (Sundararajan et al., 2017) - Axioms for gradient-based attribution
- SHAP (Lundberg & Lee, 2017) - Game-theoretic unification
- LIME (Ribeiro et al., 2016) - Local approximation approach

**Related Theoretical Work:**
- Axiomatizations of attribution methods
- Feature importance theory
- Model interpretability frameworks
- Approximation theory applications

**Mathematical Foundations:**
- Measure theory and Lebesgue–Stieltjes integration
- Approximation theory (Weierstrass theorem)
- Bounded variation function theory
- Functional analysis

### How This Advances the Field

1. **Solves the "Axiom Problem":** Replaces restrictive axiomatic systems with minimal foundation
2. **Enables Theory-Driven Innovation:** Clear structure for designing new methods
3. **Provides Unified Language:** All attribution methods become comparable within framework
4. **Grounds in Rigor:** Measure-theoretic foundation is mathematical bedrock, not heuristic

## Key Takeaways

### Main Contributions Summary

| Contribution | Impact |
|--------------|--------|
| **FMA Framework** | Unified mathematical foundation for all feature attribution methods |
| **Minimal Axiomatization** | Reduces axioms to single requirement (Linearity), removing artificial constraints |
| **Method Recovery** | Shows SHAP, IG, PDP are special cases of same framework |
| **Constructive Universality** | Proves any continuous attribution function approximable |
| **Flexibility** | Framework works with non-smooth models (trees, ReLU networks) |

### Why This Matters

- **For Researchers:** Establishes theoretical foundations for interpretability, enabling systematic method design
- **For Practitioners:** Provides principled approach to selecting attribution methods with mathematical guarantees
- **For the Field:** Moves attribution from collection of heuristics to unified theory
- **For Future Work:** Enables innovation based on framework structure rather than ad hoc proposals

### Critical Insight

The paper reveals that **restrictive axioms in prior frameworks were unnecessary and self-imposed**. By building from first principles using indicator functions and measure theory, the framework achieves:

- **Unification:** All major methods fit naturally
- **Flexibility:** Minimal constraints allow broader applicability
- **Rigor:** Measure-theoretic foundation provides mathematical completeness
- **Innovation:** Clear structure for developing new methods

This represents a **paradigm shift** from external axiomatization to natural mathematical construction.

## Citation

Taimeskhanov, M., & Garreau, D. (2025). Feature Attribution from First Principles. arXiv preprint arXiv:2505.24729.

**ArXiv:** https://arxiv.org/abs/2505.24729

## Further Reading

**Foundational Attribution Papers:**
- Sundararajan, M., Taly, A., & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *ICML*.
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. *NIPS*.
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *KDD*.

**Related Theoretical Works:**
- Simonyan, K., Vedaldi, A., & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps.
- Bach, S., et al. (2015). Pixel-wise Explanation with Deep Attention.

**Mathematical Background:**
- Approximation Theory: Classical foundations for indicator function universality
- Measure Theory and Functional Analysis: Mathematical framework for integration
- Bounded Variation Functions: Generalization enabling non-smooth models
