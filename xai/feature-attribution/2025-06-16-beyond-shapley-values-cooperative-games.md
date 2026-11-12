# Beyond Shapley Values: Cooperative Games for the Interpretation of Machine Learning Models

**ArXiv ID:** [2506.13900](https://arxiv.org/abs/2506.13900)

**Authors:** Marouane Il Idrissi, Agathe Fernandes Machado, Arthur Charpentier

**Submitted:** June 16, 2025

## Executive Summary

This paper challenges the predominance of Shapley values in feature attribution and demonstrates that numerous post-hoc interpretability methods can be understood as cooperative game allocations. The authors introduce the Weber and Harsanyi sets as mathematically sound alternatives to Shapley values, providing a unified theoretical framework that expands the interpretability toolkit and clarifies the mathematical foundations underlying many attribution techniques. This work advances xAI by moving beyond fixed axiomatic justifications toward a more flexible, task-oriented approach to designing explainability methods.

## Problem Statement

Despite their widespread adoption in machine learning interpretability, Shapley values are not the only valid approach for feature attribution. The core issue is that:

1. **Axiomatic Ambiguity:** Shapley values' justification relies on axioms (symmetry, dummy, additivity, efficiency) whose relevance to feature importance remains debatable and context-dependent.

2. **Fixed Framework Limitation:** Treating Shapley values as the default creates a false equivalence—many attribution methods built on cooperative game theory achieve allocation efficiency (the property that feature contributions sum to the model's prediction) without adhering to Shapley's specific axioms.

3. **Theory-Practice Gap:** Practitioners often apply Shapley-based methods without recognizing that alternative allocations may be equally justified, or even better suited, for specific interpretability tasks.

4. **Lack of Principled Selection:** There is no systematic way to choose between competing attribution methods once the value function is fixed, leading to ad-hoc method selection.

This paper addresses these limitations by providing a coherent theoretical framework that unifies diverse attribution techniques and reveals the full landscape of legitimate allocations.

## Core Concepts & Theory

### Cooperative Game Theory Framework

The paper grounds feature attribution in cooperative game theory, where:

- **Players:** Features in the model
- **Coalition:** Any subset of features
- **Value Function v(S):** The contribution of coalition S to the model output (often measured as the difference in predictions when features in S are present vs. absent)
- **Allocation Rule:** A method for distributing the total value v(N) (where N is all features) among individual features

### Shapley Values: A Review

The Shapley value for feature i is:

```
φᵢ = Σ_{S⊆N\{i}} (|S|!(n-|S|-1)!/n!) × [v(S∪{i}) - v(S)]
```

This distributes the "marginal contributions" of each feature across all possible coalitions using a specific weighting scheme based on permutations.

**Axioms Justifying Shapley Values:**
- **Efficiency:** Contributions sum to the total value
- **Symmetry:** Identical features receive identical values
- **Dummy Player:** Features with zero marginal contribution anywhere are valued at 0
- **Additivity:** Values decompose across independent games

### The Weber Set: Alternative Allocations via Permutations

Rather than using a uniform distribution over permutations, the Weber set parametrizes all efficient allocations that can be expressed as marginal contributions across permutations. Each element of the Weber set corresponds to a probability distribution over feature orderings:

```
Allocation_π = Expected marginal contribution when features arrive in order π
```

Key insight: Shapley values are the uniform distribution over all permutations. Other probability distributions yield different—but equally valid—allocations.

**Practical Implication:** Users can favor certain orderings (e.g., "more important features arrive later") to reflect domain knowledge.

### The Harsanyi Set: Dividend-Based Allocations

The Harsanyi dividend decomposition expresses the value function as a sum of coalition-specific "dividends":

```
v(S) = Σ_{T⊆S} d(T)
```

where d(T) is the dividend of coalition T—the value attributable solely to the combination of features in T.

Allocating these dividends yields the Harsanyi set:

```
allocation_i = Σ_{S∋i} w(S) × d(S)
```

where w(S) distributes each coalition's dividend among its members.

**Special Cases:**
- **Equal Sharing:** d(S) split equally among |S| members → Shapley values
- **Proportional Allocation:** d(S) split proportional to feature importance → Proportional Marginal Effects (PME)
- **Weighted Sharing:** d(S) divided according to custom weights → Task-specific methods

### Why These Generalizations Matter

1. **Efficiency Alone is Sufficient:** The only global allocation property necessary for feature attribution is efficiency (contributions sum to total). Other axioms are choices, not requirements.

2. **Flexibility for Practitioners:** Different problems may benefit from different allocations. For example, when features are correlated, proportional allocation may better identify spurious correlations than Shapley's uniform approach.

3. **Theoretical Coherence:** The Weber and Harsanyi sets provide a unified language for discussing and comparing hundreds of existing feature attribution techniques.

## Main Ideas & Key Contributions

### 1. Unified Framework for Attribution Methods

The paper demonstrates that numerous post-hoc attribution techniques (LIME, SHAP variants, Integrated Gradients, etc.) fit within the cooperative game framework as distinct allocations. This unification reveals:

- Hidden relationships between seemingly unrelated methods
- Common theoretical foundations despite different computational approaches
- A principled taxonomy for organizing the attribution landscape

### 2. Two General Classes of Allocations

**Weber Set:**
- Built on random orderings of features
- Allows any probability distribution over permutations
- Captures methods that favor certain feature arrival orders
- Computationally efficient for high-dimensional data

**Harsanyi Set:**
- Built on coalition dividends (value unique to each subset)
- Allows flexible sharing rules within coalitions
- Captures methods that allocate based on subset-specific properties
- Theoretically elegant but computationally more intensive

### 3. Clarity on Value Functions vs. Aggregation Rules

The paper distinguishes between:

- **Value Function Design:** How to measure feature coalition contributions (e.g., conditional expectation, perturbation, gradient-based)
- **Allocation Rule Design:** How to distribute that value among features

This separation is crucial because practitioners often conflate the two, leading to confusion about what makes different methods distinct.

### 4. A Three-Step Blueprint for Building New Attribution Methods

**Step 1: Choose a Value Function**
- Define how to compute v(S) based on the prediction task
- Examples: conditional expectation, model ablation, attention scores

**Step 2: Choose an Allocation Family**
- Decide on Weber set (permutation-based) or Harsanyi set (dividend-based)
- This choice depends on computational budget and interpretability goals

**Step 3: Parametrize Within the Family**
- Specify the probability distribution (for Weber) or dividend-sharing rule (for Harsanyi)
- Tune parameters based on domain knowledge or empirical validation

### 5. Practical Insights on Correlated Features

The paper shows that when features are correlated, proportional allocation (a Harsanyi allocation) can identify spurious correlations better than Shapley values. This is demonstrated through both theoretical arguments and synthetic examples.

**Implication:** Shapley's symmetry axiom, while appealing, is not always desirable when features have known asymmetric relationships.

## Methodology & Implementation

### Theoretical Development

The authors build their framework by:

1. **Reviewing cooperative game theory fundamentals** (coalitions, value functions, allocations)
2. **Proving that the Weber set encompasses all permutation-based allocations** with efficiency
3. **Deriving the Harsanyi set structure** and showing its relationship to dividend decomposition
4. **Establishing the connection between these sets and existing ML methods**

### Experimental Setup

The paper evaluates the framework through:

- **Synthetic Benchmarks:** Controlled examples demonstrating how different allocations behave on simple, interpretable problems
- **Real-World Datasets:** Application to standard ML benchmarks to show practical utility

**Evaluation Metrics:**
The paper assesses allocations based on:
- **Efficiency:** Do contributions sum correctly?
- **Interpretability:** Are attributions aligned with domain understanding?
- **Stability:** Do minor input changes cause minor attribution changes?
- **Computational Feasibility:** Can the allocation be computed in reasonable time?

**Models Tested:**
[Exact figures unavailable — see full paper]

**Datasets Used:**
[Exact figures unavailable — see full paper]

### Key Findings

1. **Flexibility Without Loss of Rigor:** Alternative allocations maintain mathematical coherence while offering practical advantages in specific domains.

2. **Proportional Allocation for Correlated Features:** When applied to synthetic scenarios with correlated spurious features, proportional Harsanyi allocation outperforms Shapley values at identifying true vs. spurious correlations.

3. **Computational Tradeoffs:** Weber set methods are generally faster but less flexible; Harsanyi set methods offer more parametrization at computational cost.

4. **Real-World Applicability:** Standard ML interpretability tasks benefit from method selection tailored to the problem structure rather than uniform application of Shapley values.

### Limitations of the Approach

1. **Value Function Remains Challenging:** While the paper clarifies allocations, designing appropriate value functions remains problem-specific and may require domain expertise.

2. **Evaluation Metrics:** No universally accepted metric exists for evaluating whether an allocation is "good" for a given task. This choice remains subjective.

3. **Computational Complexity:** Some Harsanyi allocations require computing marginal effects for exponentially many coalitions, limiting scalability.

4. **Validation in Practice:** Practitioners still need ground truth or expert validation to confirm that chosen allocations align with their interpretability goals.

## Practical Applications & Real-World Use Cases

### Healthcare and Medical Diagnosis

**Application:** Explaining diagnostic ML models for disease prediction

- **Challenge:** Clinicians need to understand which patient features (symptoms, test results, demographics) drive predictions
- **Shapley Limitation:** May treat correlated symptoms symmetrically, missing causal relationships
- **This Approach:** Proportional Harsanyi allocation can prioritize features clinicians recognize as causally important, improving trust

### Financial Risk Assessment

**Application:** Credit scoring and loan approval models

- **Challenge:** Regulators require transparent, auditable explanations
- **Benefit:** Weber set allocations can encode regulatory preferences (e.g., income weighted more heavily than zip code)
- **Compliance:** Ensures allocation rules align with fairness constraints

### Autonomous Systems and Safety-Critical Applications

**Application:** Explaining decisions in self-driving cars, robotics

- **Challenge:** Safety requires understanding which sensor inputs (camera, radar, lidar) influenced critical decisions
- **Approach:** Custom dividend-sharing rules can reflect sensor reliability or failure modes
- **Outcome:** Enables model validation and anomaly detection

### Fraud Detection

**Application:** Identifying which transaction features indicate fraud

- **Shapley Limitation:** May symmetrically treat correlated fraud indicators (e.g., large transaction + international location)
- **This Approach:** Allocate more value to the primary fraud signal, de-emphasizing secondary correlations
- **Result:** Cleaner, more interpretable explanations for investigators

### Model Debugging and Development

**Application:** Identifying bugs or unintended biases in models during development

- **Challenge:** Different allocation methods may reveal different aspects of model behavior
- **Approach:** Use ensemble of allocations to triangulate problematic learned patterns
- **Outcome:** Faster identification of training data issues or architectural problems

## Regulatory and Compliance Implications

### EU AI Act Compliance

- The flexibility to choose allocations helps models meet transparency requirements by enabling allocation rules that align with regulatory expectations
- Custom allocations can encode fairness constraints required by law

### GDPR Right to Explanation

- Diverse allocation options allow explanations tailored to different stakeholder needs (regulators, end-users, model developers)
- Enables legally defensible explanations rather than "black-box" default Shapley values

### FDA Medical Device Approval

- For ML in medical devices, custom allocations can reflect clinical knowledge and failure modes
- Facilitates approval discussions with regulators who understand domain-specific allocation choices

## Insights & Implications

### Advancing the State-of-the-Art in Explainability

This paper makes several contributions:

1. **Theoretical Rigor:** Grounds feature attribution in well-established cooperative game theory, moving beyond ad-hoc axiom choices

2. **Methodological Pluralism:** Demonstrates that Shapley values are one point in a large space of valid approaches, legitimizing method diversity

3. **Practical Framework:** Provides practitioners a systematic way to design attribution methods suited to specific tasks

### Limitations and Open Questions

1. **Optimal Allocation Selection:** How should practitioners choose between Weber and Harsanyi allocations for a given problem? Currently requires domain expertise or empirical experimentation.

2. **Scalability:** Harsanyi methods scale poorly with feature dimensionality. Approximation algorithms needed for high-dimensional problems.

3. **Evaluation Metrics:** What constitutes a "good" attribution? The paper clarifies the mathematics but leaves this epistemological question open.

4. **Ground Truth:** For real-world datasets, it's unclear which allocation is "correct" without expert annotation or downstream task performance metrics.

### Future Research Directions

- **Hybrid Allocations:** Combining Weber and Harsanyi approaches for specific problem classes
- **Adaptive Allocation:** Dynamically selecting allocations based on data characteristics
- **Downstream Task Validation:** Linking allocation choice to model improvement, fairness metrics, or user understanding
- **Scalable Approximations:** Efficient algorithms for large-scale Harsanyi allocations
- **Domain-Specific Benchmarks:** Creating standard evaluation protocols for different application domains

## Code & Resources

### Official Implementations

- **ArXiv Page:** https://arxiv.org/abs/2506.13900
- **PDF:** https://arxiv.org/pdf/2506.13900
- **HTML Version:** https://arxiv.org/html/2506.13900
- **ResearchGate:** https://www.researchgate.net/publication/392766408_Beyond_Shapley_Values_Cooperative_Games_for_the_Interpretation_of_Machine_Learning_Models

### Related Repositories

- **Author's Institutional Repository:** Check [author's university page for code releases]
- **Related Work:** Marouane Il Idrissi's work on conformal prediction uncertainty attribution (arXiv:2505.13118)

### Dependencies and Requirements

Based on the theoretical nature of the paper:

- **Core Dependencies:**
  - Python 3.8+
  - NumPy, SciPy (for numerical computations)
  - Pandas (for dataset handling)
  - scikit-learn (for model training and baseline methods)

- **Optional Dependencies:**
  - SHAP (for comparison with Shapley values)
  - PyTorch or TensorFlow (if implementing for neural networks)

- **Computational Requirements:**
  - Standard CPU sufficient for small to medium-sized problems
  - GPU recommended for large-scale experiments
  - Memory scales with feature dimensionality (Harsanyi methods require exponential memory in worst case)

### Quick Start Guide

[To be determined from code release; see ArXiv page for updates]

### Interactive Visualizations and Demos

- Check the ArXiv HTML version for interactive visualizations of allocation differences
- Author's slides from workshops (e.g., IJCAI 2025 XAI Workshop) may include demos

## Related Work & Context

### Positioning in the xAI Landscape

This paper contributes to several xAI communities:

1. **Feature Attribution Methods:**
   - **LIME (Ribeiro et al., 2016):** Local approximations using simple models
   - **SHAP (Lundberg & Lee, 2017):** Shapley value-based explanations (the paper's primary comparison point)
   - **Integrated Gradients (Sundararajan et al., 2017):** Gradient-based attribution
   - **DeepLIFT (Shrikumar et al., 2017):** Decomposition of network predictions

2. **Cooperative Game Theory for ML:**
   - **Shapley Value-Based Methods:** Prior work establishing Shapley values as the standard
   - **Alternative Game-Theoretic Approaches:** Including Banzhaf values and nucleolus solutions
   - **Feature Selection via Coalition Games:** Earlier work on using game theory for feature importance

3. **Theoretical Foundations of Explainability:**
   - **Axiomatic Approaches:** Defining what explainability "should" satisfy (contrast: this paper questions whether specific axioms are necessary)
   - **Information-Theoretic Attribution:** Approaches based on mutual information and entropy
   - **Causality and Counterfactuals:** Methods grounded in causal reasoning

### How This Paper Builds On and Critiques Prior Work

**Builds On:**
- Classical cooperative game theory (Weber, Harsanyi, Shapley)
- Modern machine learning explainability (SHAP, LIME)
- Recent work unifying attribution methods

**Critiques:**
- The axiomatic justification of Shapley values as the unique "correct" method
- The assumption that efficiency is achieved only through Shapley axioms
- The practical assumption that one size (Shapley values) fits all interpretability tasks

### Future Research Opportunities

1. **Empirical Benchmarking:** Large-scale comparison of allocation families on diverse datasets and tasks

2. **Causal Integration:** Combining the framework with causal inference to design allocations that respect causal structure

3. **User Studies:** Testing whether alternative allocations improve human understanding compared to Shapley values

4. **Scalable Approximations:** Developing efficient sampling-based algorithms for Harsanyi allocations

5. **Domain-Specific Variants:** Creating application-domain-specific allocation rules for healthcare, finance, criminal justice, etc.

## Summary

"Beyond Shapley Values: Cooperative Games for the Interpretation of Machine Learning Models" provides a comprehensive theoretical framework that challenges the default reliance on Shapley values and opens new avenues for feature attribution. By unifying Shapley values, Weber allocations, and Harsanyi allocations under a single cooperative game framework, the paper enables practitioners to make principled, task-specific choices about attribution methods.

The paper's key insight—that **efficiency is sufficient for feature attribution without requiring Shapley's additional axioms**—frees the field to explore a much larger space of valid allocations, each with distinct practical advantages. For researchers building explainability systems, regulators designing AI governance frameworks, and practitioners selecting attribution methods, this work provides both theoretical grounding and practical guidance.

Whether applied to healthcare, finance, autonomous systems, or model debugging, the framework developed here enables more flexible, theoretically sound, and ultimately more useful feature attribution approaches than the current Shapley-dominated landscape.
