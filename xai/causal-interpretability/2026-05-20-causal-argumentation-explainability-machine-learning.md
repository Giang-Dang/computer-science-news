# A Causal Argumentation Method for Explainability of Machine Learning Models

**ArXiv ID:** [2605.21758](https://arxiv.org/abs/2605.21758)  
**Authors:** Henry Salgado, Meagan R. Kendall, Martine Ceberio  
**Affiliation:** Department of Computer Science, The University of Texas at El Paso  
**Submission Date:** May 20, 2026

## Executive Summary

This paper presents a novel explainable AI (XAI) method that bridges causal discovery with abstract argumentation frameworks to provide structured, interpretable explanations of why machine learning models make their predictions. Unlike traditional XAI methods that identify which features are relevant, this approach clarifies why certain features lead to specific outcomes by representing causal relationships through a Bipolar Argumentation Framework (BAF), offering a complementary perspective in the landscape of interpretable machine learning.

## Problem Statement

Current explainable AI methods face a critical limitation: they excel at identifying which features influence a model's predictions but fail to clarify why certain decisions are made. Methods like SHAP and LIME provide feature importance scores and local linear approximations, yet they do not inherently explain the causal mechanisms underlying a model's reasoning. This creates a gap in explainability, particularly important for high-stakes applications in healthcare, finance, and legal domains where understanding not just what features matter, but why they matter and how they interact causally, is essential for building trust and ensuring regulatory compliance.

The paper addresses the need for explanations that articulate:
1. **Causal relationships** between input features and outputs (not just correlations)
2. **Feature interactions** and their supportive or opposing roles
3. **Structured reasoning** about model decisions in a human-understandable format

## Core Concepts & Theory

### Causal Discovery

Causal discovery aims to identify causal relationships among variables from observational data. The method employs constraint-based causal discovery algorithms such as:

- **PC Algorithm**: Constraint-based method using conditional independence tests to identify adjacencies and orient edges. Applicable to linear Gaussian data (Fisher Z test), discrete multinomial data (Chi-square test), and mixed data (Conditional Gaussian test).

- **FCI Algorithm (Fast Causal Inference)**: Relaxes the assumption of causal sufficiency (allowing latent confounders) by introducing bidirected edges to represent uncertainty from hidden variables. Provides a more conservative representation when confounding variables are present.

- **GES (Greedy Equivalence Search)**: Score-based approach that searches over the space of equivalence classes of Directed Acyclic Graphs (DAGs) in two phases—forward equivalence search (adding edges) and backward equivalence search (removing edges).

These algorithms produce Directed Acyclic Graphs (DAGs) representing causal structures that preserve the directional relationships discovered from observational data.

### Bipolar Argumentation Framework (BAF)

The Bipolar Argumentation Framework is an extension of abstract argumentation that explicitly models:

- **Support relations**: Arguments that strengthen a conclusion
- **Attack relations**: Arguments that weaken or contradict a conclusion
- **Arguments**: Each feature or combination of features represents an argument

In the context of explainability:
- Each feature activation (or feature value) acts as an argument
- Positive feature contributions are represented as support
- Negative feature contributions or feature interactions are represented as attacks
- The framework determines which combinations of features (argument extensions) justify a particular model outcome

**Semi-Stable Semantics**: The method uses semi-stable semantics to evaluate argumentation extensions:
- Identifies sets of arguments (features) that are conflict-free and defend themselves against attacks
- Among multiple possible extensions, selects the one that minimizes unexplained attacks
- Provides multiple possible explanations when several equally valid interpretations exist

### Integration: From Causality to Argumentation

The pipeline translates causal discoveries into argumentation frameworks by:

1. **Extracting causal paths**: From DAG representations, identify which causal paths lead to the predicted outcome
2. **Mapping to arguments**: Each variable in a causal path becomes an argument; causal edges become support/attack relations
3. **Reasoning about interactions**: Argumentation semantics naturally capture feature interactions (synergistic or antagonistic relationships)
4. **Computing extensions**: Apply semi-stable semantics to find argument extensions (sets of features) that collectively justify the prediction

## Main Ideas & Key Contributions

### Novel Integration of Causal Reasoning and Argumentation

The paper's primary contribution is demonstrating that **causal reasoning and argumentation frameworks complement each other in explainability**:

- **Causal discovery** provides the structure (which variables influence which)
- **Argumentation frameworks** provide the reasoning mechanism (how those variables justify an outcome)

This combination offers advantages over either approach alone:
- Causal discovery without argumentation may produce complex graphs hard to interpret
- Argumentation without causality cannot guarantee meaningful reasoning structures

### Structured, Causal Explanations vs. Feature Attribution

Unlike feature importance methods (SHAP, LIME):
- **Traditional approach**: "Feature X has importance score 0.75"
- **This approach**: "Feature X supports the outcome because it causally affects Feature Y, which in turn influences the model's prediction"

This provides *narratives* rather than mere scores—explanations that humans can validate and reason about.

### Treatment of Feature Interactions

The BAF naturally models:
- **Synergistic effects**: When Feature A and Feature B together have more impact than separately
- **Antagonistic effects**: When Feature A reduces the impact of Feature B
- **Redundancy**: When multiple paths lead to the same conclusion

### Comparison to Existing XAI Paradigms

| Aspect | SHAP/LIME | This Method | Advantage |
|--------|-----------|------------|-----------|
| **Explanation type** | Feature importance scores | Causal narratives | Answers "why," not just "what" |
| **Feature interactions** | Implicit or ignored | Explicit via BAF relations | Better for interdependent features |
| **Causal structure** | None | Via causal discovery | Captures true mechanisms |
| **Human interpretability** | Moderate (numbers) | High (structured reasoning) | More aligned with human cognition |
| **Computational cost** | Lower | Higher (causal discovery + BAF evaluation) | Tradeoff for greater insight |

## Methodology & Implementation

### Algorithm Pipeline

**Step 1: Causal Discovery**
- Input: Feature matrix X and target variable y
- Apply causal discovery algorithm (PC, FCI, or GES) to estimate causal structure
- Output: Directed Acyclic Graph (DAG) representing causal relationships among features
- Challenge: Limited to observational data; estimates are subject to identifiability assumptions

**Step 2: Feature Attribution & Sign Determination**
- Compute feature importance using SHAP, LIME, or other methods
- Determine whether each feature contributes positively (support) or negatively (attack) to the prediction
- This information, combined with the causal structure, drives the mapping to argumentation

**Step 3: BAF Construction**
- For each feature in the causal graph, create a corresponding argument
- For each causal edge:
  - If source feature importance is positive and target feature matters to outcome → support relation
  - If source feature importance is negative or antagonistic → attack relation
- Include higher-order interactions based on causal paths

**Step 4: Semi-Stable Semantics Evaluation**
- Compute argument extensions under semi-stable semantics
- An extension is a conflict-free set of arguments where:
  - No two arguments in the extension attack each other
  - The extension is maximally defended (minimizes unexplained attacks)
- Return all valid extensions as alternative explanations

**Step 5: Narrative Generation**
- For each extension, generate human-readable explanations
- Articulate which features (arguments) together justify the prediction
- Explain the causal mechanisms: "Feature A → Feature B → Outcome"

### Experimental Setup

**Datasets:**
- Binary classification benchmarks used for validation
- Evaluation compared against standard baseline methods (SHAP, LIME, pruned decision trees)
- [Exact datasets not specified in available sources — see full paper]

**Baselines for Comparison:**
- SHAP (SHapley Additive exPlanations)
- LIME (Local Interpretable Model-agnostic Explanations)
- Decision tree pruning methods

**Metrics for Evaluation:**
- **Convergence/Alignment**: Correlation between causal-argumentation explanations and baseline feature importance
- **Fidelity**: How well explanations reflect actual model behavior (planned for future work)
- **Consistency**: Whether explanations change appropriately under feature interventions (counterfactual consistency, planned)

### Implementation Considerations

**Causal Discovery Tools:**
- **causal-learn**: Python library implementing PC, FCI, and GES algorithms
- **CDT (Causal Discovery Toolbox)**: Comprehensive Python package for causal discovery
- **gCastle**: Alternative Python implementation of multiple causal discovery algorithms

**Argumentation Framework Tools:**
- Argumentation solvers for computing semi-stable extensions
- Custom implementations may be required for BAF-specific semantics

**Computational Requirements:**
- Causal discovery: O(p³) for p features in constraint-based methods
- BAF evaluation: Exponential in worst case, but polynomial for restricted argumentation structures
- Practical limitation: Best suited for datasets with moderate feature dimensionality (< 100 features)

### Results and Evaluation

**Key Findings:**
- Causal-argumentation explanations align with SHAP and decision tree baselines while preserving causal structure
- The method successfully identifies both individual feature contributions and feature interactions
- Multiple valid explanations (argument extensions) provide flexibility when causal structure is ambiguous
- Results demonstrate strong convergence between the proposed method and standard interpretability techniques

**Limitations:**
- Causal discovery from observational data is subject to identifiability assumptions; true causal structure may not be uniquely identifiable
- Computational cost increases significantly with feature dimensionality; practical application limited to moderate-dimensional datasets
- Quantitative evaluation metrics (fidelity, counterfactual consistency) remain as future work
- Performance on highly non-linear relationships or complex feature interactions not fully characterized
- Requires sufficient data for reliable causal discovery; small-sample performance not thoroughly evaluated

## Practical Applications & Real-World Use Cases

### Healthcare

**Example: Clinical Risk Assessment**
- **Problem**: Hospital admissions decision based on patient features (age, comorbidities, lab values, medication history)
- **Application**: Instead of knowing "Feature X (admission risk score) matters most," clinicians learn "Patient's age AND kidney function (correlated via common cause: hypertension) together increase admitted-patient risk due to complications pathway"
- **Benefit**: Enables intervention at causal mechanisms (e.g., treating hypertension) rather than just addressing risk scores
- **Regulatory**: Supports HIPAA and FDA transparency requirements for algorithmic decision-making

### Finance

**Example: Credit Risk Decisions**
- **Problem**: Loan approval decisions must be explicable to regulatory bodies and customers
- **Application**: Explaining rejections as "Your income was stable (support) but debt-to-income ratio was high (attack) due to recent large purchases; these together determined approval denial"
- **Benefit**: More meaningful explanations than SHAP scores; supports fair lending compliance under fair lending laws (FCRA, ECOA)
- **Compliance**: Meets EU AI Act requirements for high-risk financial AI systems

### Legal & Criminal Justice

**Example: Bail or Sentencing Recommendation Systems**
- **Problem**: Controversial algorithmic recommendations in criminal justice require non-discriminatory, interpretable explanations
- **Application**: Articulating "Prior convictions (attack current good standing) and employment instability (causal link to recidivism) together increase risk assessment" versus treating each feature independently
- **Benefit**: Enables courts to understand whether systems are capturing true causal risk factors versus statistical proxies for protected attributes
- **Regulatory**: Supports fairness audits and explainability mandates under state criminal justice transparency laws

### Autonomous Systems

**Example: Failure Mode Analysis in Self-Driving Cars**
- **Problem**: When models reject certain road scenarios (e.g., "Don't drive here"), autonomous systems need explainable reasoning
- **Application**: Articulating causal chains: "Wet road surface → reduced tire grip → increased braking distance → collision risk"
- **Benefit**: Safety engineers can identify which causal pathways are most critical to improve
- **Regulatory**: Supports autonomous vehicle certification requirements for interpretability

## Insights & Implications

### Advancing Trustworthy AI

This work contributes to trustworthy AI by:

1. **Addressing the "Why" Question**: Moving beyond "which features matter" to "why these features matter" and "how do they interact"
2. **Incorporating Causal Reasoning**: Aligns model explanations with human causal reasoning, making them more intuitive
3. **Structured Reasoning**: Provides formal, verifiable explanations through argumentation semantics rather than opaque feature scores
4. **Complementary Perspective**: Offers an alternative to correlational explanations, particularly valuable in domains where causal understanding drives decisions

### State-of-the-Art Advancement

- **Novelty**: First systematic integration of causal discovery with argumentation frameworks for model interpretability
- **Expressiveness**: Can represent feature interactions and competing causal pathways more naturally than methods that treat features independently
- **Flexibility**: Multiple explanation extensions allow for uncertainty in causal structure without forcing a single explanation

### Limitations and Open Questions

1. **Identifiability**: Causal discovery from observational data faces fundamental limits; true causal structure may not be identifiable from data alone
2. **Scalability**: Current approach computationally intensive for high-dimensional datasets; efficient algorithms for large-scale application remain open
3. **Validation**: How to validate that discovered causal structures are correct without intervention experiments?
4. **Fidelity Trade-offs**: Does enforcing causal structure sacrifice predictive fidelity? Not fully explored
5. **Human Evaluation**: Quantitative metrics for human understanding of causal explanations versus feature scores need development

### Future Research Directions

1. **Hybrid Approaches**: Combining observational causal discovery with small-scale randomized experiments for hybrid identification
2. **Counterfactual Integration**: Incorporating counterfactual reasoning ("what if I changed X?") with argumentation for actionable explanations
3. **Scalable Algorithms**: Developing polynomial-time approximations for BAF evaluation on high-dimensional problems
4. **Interactive Explanation**: User studies on whether causal-argumentation explanations improve human trust and decision-making
5. **Domain-Specific Customization**: Tailoring causal and argumentation models to domain-specific constraints (e.g., legal requirements, scientific principles)

## Code & Resources

### Official Resources

- **Paper ArXiv Link**: [https://arxiv.org/abs/2605.21758](https://arxiv.org/abs/2605.21758)
- **Authors' Affiliation**: Department of Computer Science, The University of Texas at El Paso
- [Official implementation repository — likely available upon paper publication]

### Dependencies and Libraries

**For Causal Discovery:**
- **causal-learn**: [https://pypi.org/project/causal-learn/](https://pypi.org/project/causal-learn/) — Implements PC, FCI, GES algorithms
- **CDT (Causal Discovery Toolbox)**: Comprehensive Python package for causal discovery methods
- **gCastle**: Alternative implementations for multiple causal discovery algorithms

**For Feature Attribution:**
- **SHAP**: [https://github.com/slundberg/shap](https://github.com/slundberg/shap) — SHapley Additive exPlanations
- **LIME**: [https://github.com/marcotcr/lime](https://github.com/marcotcr/lime) — Local Interpretable Model-agnostic Explanations

**For Argumentation Frameworks:**
- Argumentation solvers and BAF evaluation tools (implementation details to be confirmed from paper)
- Custom implementations may be required for semi-stable semantics computation

### Quick Start Guide

1. **Install Causal Discovery Tools**:
   ```bash
   pip install causal-learn
   ```

2. **Perform Causal Discovery**:
   ```python
   from causallearn.search.ConstraintBased import pc
   
   # X is your feature matrix, suffStat contains test parameters
   cg = pc(data, alpha=0.05)  # Returns a causal graph
   ```

3. **Compute Feature Attribution**:
   ```python
   import shap
   
   explainer = shap.TreeExplainer(model)
   shap_values = explainer.shap_values(X)
   ```

4. **Construct BAF and Evaluate**:
   - Map causal edges and feature attributions to argumentation relations
   - Compute semi-stable extensions
   - Generate structured explanations

5. **Validate Explanations**:
   - Compare with SHAP/LIME baselines
   - Conduct human evaluation for interpretability
   - Test counterfactual consistency

### Computational Requirements

- **CPU**: Standard multi-core CPU (causal discovery benefits from parallelization)
- **Memory**: Moderate (depends on feature dimensionality; 8GB+ recommended for large datasets)
- **Time**: Causal discovery: minutes to hours depending on dataset size and feature count
- **Scalability Limitations**: Best suited for datasets with < 100 features; high-dimensional data may require dimensionality reduction

## Related Work & Context

### Relationship to Other XAI Approaches

**Feature Attribution Methods (SHAP, LIME):**
- **Comparison**: Both identify influential features; this method adds causal structure and interaction modeling
- **Complementarity**: Could be combined—use SHAP/LIME for importance, BAF for causal reasoning about importance

**Concept-Based Explanations (TCAV, ProtoNet):**
- **Relationship**: Both seek human-understandable explanations; this method focuses on feature causality rather than learned concepts
- **Potential Integration**: Concepts could be mapped to arguments in the BAF

**Counterfactual Explanations:**
- **Overlap**: Both address "why" questions; counterfactuals ask "what if I changed X?", causality-BAF asks "why did changing X matter?"
- **Potential Fusion**: Combining counterfactual generation with causal-argumentation explanations could yield more actionable insights

**Fairness and Bias in ML:**
- **Connection**: Understanding causal mechanisms helps identify whether models capture true causal risk factors versus proxies for protected attributes
- **Application**: Causal-argumentation explanations could support fairness audits by revealing causal pathways driving decisions

### Prior Work in Causal Interpretability

- **Causal Discovery**: Decades of work in PC, FCI, GES algorithms from causal inference literature
- **Structural Causal Models (SCMs)**: Formal framework for causal reasoning, increasingly applied to ML
- **DoCode** (Salgado et al., related work): Post-hoc interpretability using causal inference for code models
- **Causal Argumentation**: Historical work in abstract argumentation extended to interpretability context

### XAI Communities and Paradigms

This work bridges multiple communities:

1. **Causal Inference Community**: Bringing causal discovery methodology into XAI
2. **Abstract Argumentation Community**: Applying formal argumentation to practical ML interpretability
3. **XAI/Interpretability Community**: Contributing a novel fusion approach combining causality and structured reasoning
4. **Fairness & Transparency in AI**: Supporting regulatory compliance and trustworthy AI goals

### Future Research Connections

- **Mechanistic Interpretability**: Could causal-argumentation frameworks help interpret transformer internals or neural circuit discovery?
- **Feature Attribution Improvements**: Hybrid methods combining causal discovery with improved SHAP/LIME estimation
- **Causal Representation Learning**: Learning representations that align with causal structure for inherently interpretable models
- **Probabilistic Explanations**: Incorporating uncertainty from causal discovery into argumentation (e.g., probabilistic argumentation)

## References

- [A Causal Argumentation Method for Explainability of Machine Learning Models](https://arxiv.org/abs/2605.21758) (arXiv:2605.21758)
- [Causal-learn: Causal Discovery in Python](https://arxiv.org/pdf/2307.16405)
- [A Survey on Causal Discovery Methods for I.I.D. and Time Series Data](https://arxiv.org/pdf/2303.15027)
- [Abstract Argumentation Framework](https://en.wikipedia.org/wiki/Argumentation_framework)
- [SHAP: A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874)
- [LIME: Local Interpretable Model-Agnostic Explanations](https://arxiv.org/abs/1602.04938)

---

**Paper Documentation Date**: 2026-06-10  
**Status**: Primary research paper on causal argumentation for model explainability
