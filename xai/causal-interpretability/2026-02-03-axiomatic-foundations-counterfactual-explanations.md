# Axiomatic Foundations of Counterfactual Explanations

**ArXiv ID:** [2602.04028](https://arxiv.org/abs/2602.04028)

**Authors:** Leila Amgoud, Martin Cooper

**Submission Date:** February 3, 2026

**Venue:** Published at AAMAS 2026 (pp. 282–290)

**Cross-lists:** cs.AI, cs.LG, stat.ME

---

## Executive Summary

This paper introduces the first formal axiomatic framework for counterfactual explainers, addressing a critical gap in the literature: the lack of systematic study of alternative counterfactual types and global explanations. By establishing nine axioms defining desirable properties for counterfactual explainers, the authors distinguish five fundamentally different types of counterfactual explanations, formalize key properties like minimality and actionability, and analyze the computational complexity of generating such explanations. This work provides both theoretical foundations and practical guidance for developing and evaluating counterfactual explainability methods across diverse machine learning applications.

---

## Problem Statement

Explainability in machine learning has become critical for deploying trustworthy AI systems, particularly in high-stakes domains like healthcare, finance, and criminal justice. Among explainability approaches, counterfactual explanations—statements of the form "if the input had been different in X ways, the model's output would have changed"—offer intuitive and actionable insights compared to feature attribution methods like LIME and SHAP.

However, prior work in counterfactual explanations suffers from significant limitations:

1. **Lack of theoretical foundation:** Most existing explainers are developed ad hoc without grounding in formal principles or axioms.
2. **Limited type coverage:** Prior work focuses on a single type of counterfactual explanation (usually local), neglecting alternatives.
3. **No global explanations:** The literature lacks systematic treatment of global counterfactual explanations that characterize model behavior across the entire input space.
4. **Inconsistent properties:** Different methods claim to satisfy properties like "minimality" or "actionability" but define them differently, making comparison difficult.
5. **Complexity analysis gaps:** There is no systematic study of the computational complexity of generating different counterfactual types.

This paper addresses all these gaps by proposing the first comprehensive axiomatic framework for counterfactual explainers.

---

## Core Concepts & Theory

### What Are Counterfactual Explanations?

Counterfactual explanations explain a classifier's decision by describing minimally perturbed versions of the input that would change the prediction. They are grounded in causal thinking: they ask "what if" questions about the input space and answer why the model made a particular prediction.

**Example:** A loan rejection can be explained by a counterfactual: "If your income were $5,000 higher and your debt-to-income ratio were 10% lower, the loan would have been approved."

### Two Fundamental Forms

The paper distinguishes counterfactual explanations into two basic forms, each with multiple types:

#### 1. **Necessary Reasons (Necessary Counterfactuals)**
These are features that must change to reach a desired outcome. They answer: "What features are absolutely essential to change to flip the prediction?"

- Example: "To get the loan approved, your income and debt ratio must both change."
- These are **sufficient as sets**: if all necessary features change together, the outcome flips.
- Mathematically, a set S of features is a necessary reason if no subset of S can achieve the outcome change alone.

#### 2. **Sufficient Reasons (Sufficient Counterfactuals)**
These describe features that, if changed, are enough by themselves to flip the prediction. They answer: "What individual changes would be sufficient to flip the prediction?"

- Example: "If we increased your income by $10,000, the loan would be approved; alternatively, if we reduced your debt by $20,000, it would also be approved."
- Each is individually sufficient; the model could act on any single change.

### Nine Axioms for Counterfactual Explainers

The paper grounds its framework in a set of nine axioms defining properties that counterfactual explainers should ideally satisfy:

1. **Success:** The returned counterfactuals must actually lead to a different prediction when applied to the model.
2. **Minimality:** Counterfactuals should involve the smallest possible change to the input.
3. **Feasibility:** The counterfactual must be plausible and realistic (e.g., not suggesting a person become 10 years younger).
4. **Actionability:** The suggested changes should be achievable by the entity being explained (e.g., actionable for a loan applicant but not for immutable features like race or gender).
5. **Diversity:** Multiple distinct counterfactuals should be generated to offer different perspectives.
6. **Sparsity:** Favor counterfactuals that modify fewer features.
7. **Contrastiveness:** The counterfactual should highlight what changed, not just what the new prediction is.
8. **Validity:** Counterfactuals should correspond to realistic scenarios respecting feature correlations and constraints.
9. **Interpretability:** The counterfactuals should be understandable and human-interpretable.

Different combinations of axioms characterize different counterfactual types, allowing for systematic taxonomy.

### Five Types of Counterfactuals

The framework distinguishes five types based on axiom combinations:

| **Type** | **Scope** | **Key Properties** | **Use Case** |
|----------|-----------|-------------------|------------|
| **Type 1: Local Minimal** | Local (single instance) | Success, Minimality, Feasibility | Understanding individual decisions |
| **Type 2: Local Minimal + Actionable** | Local | Success, Minimality, Feasibility, Actionability | Decision support (e.g., loan applicants) |
| **Type 3: Local Diverse** | Local | Success, Diversity, Feasibility | Offering multiple perspectives |
| **Type 4: Global Characteristic** | Global (entire model behavior) | Success, Validity | Model-level understanding |
| **Type 5: Global Actionable** | Global | Success, Validity, Actionability | Model-level decision support |

Local explanations explain individual predictions, while global explanations characterize model behavior across the entire input space (e.g., "for most users, increasing income by 20% flips a loan decision").

---

## Main Ideas & Key Contributions

### 1. First Formal Axiomatic Framework

The paper's primary contribution is establishing the first rigorous axiomatic foundation for counterfactual explanations. Rather than designing explainers ad hoc, this framework provides:

- **Formal axioms:** Nine mathematically defined properties that explainers should satisfy.
- **Characterization theorems:** Which axiom combinations define which types of counterfactuals.
- **Completeness:** The framework is comprehensive—most existing explainers can be situated within it.

### 2. Systematic Taxonomy of Counterfactual Types

By formalizing axioms, the paper reveals that counterfactual explanations fall into fundamentally different types. This addresses the literature's confusion where different papers use "counterfactual" to mean different things:

- **Local vs. global:** Most prior work addresses only local explanations; this framework systematically covers both.
- **Actionability:** The paper distinguishes actionable counterfactuals (practically implementable) from feasible ones (plausible but perhaps not actionable).
- **Minimality vs. diversity:** A key trade-off: smaller, minimal counterfactuals may not reveal the full solution space; diverse counterfactuals offer more options.

### 3. Computational Complexity Analysis

The paper analyzes the computational complexity of generating each counterfactual type. Key insights include:

- **NP-hardness:** Generating minimal counterfactuals is NP-hard in general, but specific problem structures or constraints can permit efficient algorithms.
- **Tractability conditions:** Under certain conditions (e.g., specific decision boundaries, feature constraints), efficient algorithms exist.
- **Approximation algorithms:** When exact computation is intractable, approximation schemes with bounded error are possible.

[Exact figures unavailable — see full paper]

### 4. Evaluation Framework

The paper proposes a unified evaluation framework for counterfactual explainers:

- **Axiom compliance:** Does the explainer satisfy the axioms it claims?
- **Practical evaluation:** Measures like minimum perturbation, feature sparsity, and actionability.
- **User studies:** Assessing human interpretability and usefulness of the explanations.

---

## Methodology & Implementation

### Formal Framework

The authors build their axiomatic framework on a mathematical foundation:

1. **Representation:** An input instance is a tuple of features with values; counterfactuals are sets of feature-value pairs differing from the original.
2. **Counterfactual explainer:** Formally defined as a function mapping an instance and a decision to a set of partial assignments (counterfactuals).
3. **Axiom formalization:** Each axiom is stated as a logical constraint on the counterfactual explainer function.

### Axiom Validation

For each proposed axiom, the authors:

1. Justify why it should be a property of counterfactual explainers.
2. Show how existing explainers satisfy or violate it.
3. Analyze interactions between axioms (e.g., can Success and Minimality always be satisfied together?).

### Complexity Analysis Method

The computational complexity is analyzed using standard techniques:

- **Reductions from known hard problems:** Showing NP-hardness by reduction from 3-SAT or similar.
- **Algorithm design:** For tractable cases, polynomial-time algorithms are presented.
- **Approximation bounds:** For intractable cases, algorithms with approximation guarantees are proposed.

### Practical Applications

The paper demonstrates the framework's utility by:

- **Categorizing existing explainers:** Methods like DiCE, WACHTER, and others are placed within the taxonomy.
- **Identifying gaps:** Showing which axiom combinations are under-explored.
- **Guiding development:** Using axioms to design new explainers targeting underserved combinations.

---

## Practical Applications & Real-World Use Cases

### 1. Credit and Loan Decisions

**Domain:** Banking and financial services

**Use Case:** A loan applicant is denied credit. The bank can use counterfactual explanations to tell the applicant: "If you increase your income by $5,000 or reduce your debt by $10,000, your loan would be approved."

**Key Properties:**
- Actionable (borrower can work toward these changes)
- Minimal (smallest necessary change)
- Diverse (multiple paths to approval)

**Regulatory Benefit:** Satisfies explainability requirements under regulations like GDPR and the Algorithmic Accountability Act.

### 2. Medical Diagnosis and Treatment

**Domain:** Healthcare and clinical decision support

**Use Case:** A patient has a risk score for a disease (e.g., diabetes, heart disease). A clinician can use counterfactual explanations: "If your BMI decreased by 2 units and your blood sugar levels improved, your risk would drop below the threshold."

**Key Properties:**
- Actionable (patient and clinician can influence these factors)
- Feasible (realistic health changes)
- Diverse (multiple intervention strategies)

**Regulatory Benefit:** FDA guidance on algorithmic transparency and clinical validation increasingly requires interpretable AI explanations.

### 3. Hiring and Recruitment

**Domain:** Human resources and employment

**Use Case:** A job applicant is rejected by an AI screening system. The HR department can explain: "With 2 more years of experience or a higher degree in a related field, you would have passed the screening."

**Key Properties:**
- Actionable (applicant knows what could improve their prospects)
- Fair (explanations reveal potential biases)
- Diverse (multiple paths to acceptance)

**Fairness Consideration:** Identifying and addressing disparate impact in hiring algorithms through counterfactual analysis.

### 4. Criminal Justice and Risk Assessment

**Domain:** Judiciary, parole, and sentencing

**Use Case:** Sentencing algorithms predict recidivism risk. Counterfactual explanations can inform: "With stable employment and no substance abuse treatment violations, your risk score would decrease significantly."

**Key Properties:**
- Actionable (individuals can work toward these goals)
- Minimality (avoid suggesting unrealistic changes)
- Fairness (highlight potential algorithmic bias)

**Regulatory Impact:** Criminal justice agencies increasingly adopt explainability standards (see COMPAS algorithm scrutiny).

### 5. E-Commerce and Content Recommendation

**Domain:** Retail and digital platforms

**Use Case:** A customer sees why they were shown a particular product: "Based on your browsing history and similar customers' purchases, you'd see more home automation products if you clicked on smart home items more frequently."

**Key Properties:**
- Interpretable (customers understand recommendation logic)
- Actionable (users can influence recommendations)
- Privacy considerations (not exposing personal data)

---

## Insights & Implications

### 1. Theoretical Impact

- **Foundations for XAI:** This work establishes rigorous mathematical foundations for a major XAI methodology, bringing formal methods to a field that often operates heuristically.
- **Connecting to AI safety:** Counterfactual explanations are tools for understanding and potentially controlling AI behavior, relevant to alignment and safety research.
- **Beyond post-hoc explanations:** The framework suggests that some properties of explanations are intrinsic to the explanation type, not dependent on the underlying model.

### 2. Practical Implications

- **Standardization:** The taxonomy enables stakeholders (regulators, practitioners, users) to agree on what type of explanation is appropriate for a given context.
- **Algorithm design guidance:** Developers can use the axiom framework to design explainers targeting specific combinations of desirable properties.
- **Tradeoff analysis:** The framework makes explicit the tradeoffs (e.g., minimal vs. diverse, local vs. global) so practitioners can make informed choices.

### 3. Limitations and Open Questions

- **Implementation complexity:** While the axiomatic framework is elegant, actually building explainers that satisfy multiple axioms simultaneously (especially under constraints) remains challenging.
- **Feature interactions:** The framework assumes features can be modified independently; real-world feature correlations and causal structures complicate this.
- **Scalability:** Generating counterfactuals for high-dimensional spaces or complex models remains computationally expensive.
- **Global explanations:** Defining and computing global counterfactuals is less developed than local versions; this remains an open challenge.
- **User studies:** The framework is theory-driven; empirical validation of which axiom combinations matter most to humans is limited.

### 4. Future Research Directions

- **Empirical validation:** Large-scale user studies to assess which axiom combinations practitioners and stakeholders actually value.
- **Hybrid frameworks:** Combining counterfactual explanations with other XAI methods (e.g., feature attribution, prototype explanations) for richer understanding.
- **Fairness integration:** Formalizing fairness properties and their interaction with counterfactual axioms.
- **Causal discovery:** Using counterfactual reasoning to discover causal structures in data, connecting counterfactual XAI to causal inference.
- **Adversarial robustness:** Investigating whether counterfactual explanations are robust to adversarial perturbations or model poisoning.

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2602.04028](https://arxiv.org/abs/2602.04028)
- **PDF:** [https://arxiv.org/pdf/2602.04028](https://arxiv.org/pdf/2602.04028)
- **HTML Version:** [https://arxiv.org/html/2602.04028](https://arxiv.org/html/2602.04028)
- **AAMAS 2026 Version:** Published at AAMAS 2026 (pp. 282–290)

### Implementations & Tools

As this is a theoretical paper, no official reference implementation is provided. However, the framework can guide implementations of counterfactual explainers:

**Recommended Existing Tools:**
- **DiCE** (Diverse Counterfactual Explanations): Generates diverse counterfactuals for black-box models
- **WACHTER:** Gradient-based counterfactual generation
- **SHAP:** While primarily feature-attribution, also supports counterfactual-style explanations

**Framework Application:**
1. Identify which axioms your problem requires
2. Select or design an algorithm satisfying that axiom combination
3. Evaluate using the properties defined in the framework

### Computational Requirements

- **Theory paper:** No significant computational requirements for the framework itself
- **Implementation:** Depends on the specific algorithm chosen; counterfactual generation is typically polynomial to NP-hard depending on the problem constraints

### Quick Start

1. Read the AAMAS version or arXiv paper for the formal framework
2. Consult Table 1 (or equivalent) to map your use case to a counterfactual type
3. Review the axiom combinations that type satisfies
4. Use those as design criteria for your explainer or evaluation checklist

---

## Related Work & Context

### Prior Counterfactual Explanation Work

- **Wachter et al. (2017):** Introduced gradient-based counterfactual explanations, one of the first systematic approaches
- **DiCE (Mothilal et al., 2020):** Proposed diverse counterfactual explanations to address diversity-minimality tradeoffs
- **CycleGAN-based approaches:** Generate realistic counterfactuals using generative models
- **Concept-based counterfactuals:** More recent work using semantic concepts instead of raw features

### Relationship to Other XAI Methods

| **Method** | **Explanation Type** | **Local/Global** | **Model Type** |
|------------|-------------------|------------------|----------------|
| **Feature Attribution (LIME, SHAP)** | Feature importance | Local/Global | Model-agnostic |
| **Counterfactual** | "What-if" scenarios | Local/Global (this paper) | Model-agnostic |
| **Prototype-based** | "Similar to" examples | Local | Model-agnostic |
| **Saliency Maps** | Feature importance (visual) | Local | Vision models |
| **Attention Visualization** | Model internals | Local | Transformers |

Counterfactuals differ from feature attribution by being **prescriptive** (suggesting changes) rather than purely **descriptive** (explaining past decisions).

### Connection to Causal Inference

Counterfactual explanations are fundamentally causal in nature:
- They reason about **interventions** (changing features)
- They answer **"what if"** questions grounded in causal graphs
- They connect to **causal do-calculus** (Pearl's framework)

This paper bridges formal XAI and causal reasoning, relevant to growing work in causal machine learning and interpretable causal inference.

### Relationship to AI Safety and Alignment

- **Mechanistic understanding:** Like mechanistic interpretability (circuits, attention patterns), counterfactual frameworks aim to understand and control model behavior
- **Alignment through explanation:** If we can explain what changes inputs to outputs, we can potentially steer or align model behavior
- **Robustness verification:** Counterfactual explanations can be used to identify and mitigate adversarial vulnerabilities

### Community Context

- **Venues:** Published at AAMAS 2026 (a top AI conference); related workshops include FAccT, AIES (Fairness, Accountability, and Transparency in AI)
- **Trends in XAI:** 2026 sees renewed focus on theoretical foundations after years of ad-hoc method development
- **Cross-disciplinary relevance:** Counterfactual reasoning is studied in philosophy (Lewis), cognitive science, and law, making this work internationally relevant

---

## Note

This documentation synthesizes information from the arXiv abstract, HTML version, and broader context in the counterfactual explanations and XAI literature. For complete formal axiom definitions, complexity proofs, full experiments, and detailed algorithm descriptions, consult the full paper at [https://arxiv.org/pdf/2602.04028](https://arxiv.org/pdf/2602.04028).

---

**Last Updated:** November 20, 2026
