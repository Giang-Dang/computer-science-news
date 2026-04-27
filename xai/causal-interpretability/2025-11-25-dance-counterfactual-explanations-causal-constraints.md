# DANCE: Actionable and Diverse Counterfactual Explanations Incorporating Domain Knowledge and Causal Constraints

**ArXiv ID:** [2511.20236](https://arxiv.org/abs/2511.20236)  
**Authors:** Szymon Bobek, Łukasz Bałec, Grzegorz J. Nalepa (AGH University of Krakow, Poland)  
**Date:** November 25, 2025  
**Subfield:** Causal Interpretability  
**Keywords:** counterfactual explanations, algorithmic recourse, causal constraints, feature dependencies, DANCE, diversity, actionability

---

## Executive Summary

Counterfactual explanations — answers to "what would have to change for the model to give a different prediction?" — are among the most practically useful forms of XAI. However, existing methods generate counterfactuals that are either implausible (violating feature dependencies), non-diverse (all suggesting the same change), or disconnected from domain knowledge. DANCE (**D**iverse, **A**ctionable, and k**N**owledge-**C**onstrained **E**xplanations) addresses all three limitations simultaneously by learning or incorporating causal constraints between features, validated across 140 real-world datasets with a comprehensive case study in email marketing.

---

## Problem Statement

Counterfactual explanations for machine learning models answer the question: *"What minimal change to the input would flip the model's decision?"* They are critical for algorithmic recourse — helping individuals understand what actions they can take to change unfavorable automated decisions (loan denials, insurance rejections, hiring decisions).

**Three key limitations in existing methods:**

**1. Implausibility (constraint violation)**
Existing methods generate counterfactuals that violate real-world constraints:
- DICE changes `age` from 30 to 25 (age cannot decrease)
- NICE changes `employed = True` while simultaneously reducing `income` to below minimum wage
- Many methods ignore that `loan amount / income ratio` cannot freely vary when both are constrained by lending regulations

These implausible counterfactuals are useless for actionable recourse — users cannot take actions that violate physics, biology, or business rules.

**2. Lack of diversity**
Many methods optimize for a single nearest counterfactual, producing only one possible path to recourse. Users need diverse options because:
- Some changes may be impossible for a specific individual
- Different users have different preferences about which features to change
- A single counterfactual may be unrepresentative of the decision boundary

**3. Missing domain knowledge**
Expert knowledge about feature relationships (causal graphs, business rules, regulatory constraints) is rarely incorporated. Domain experts know that "improving credit score" takes time, that "income" affects "savings" not vice versa, and that certain combinations are legally forbidden — but this knowledge is lost in standard methods.

---

## Core Concepts & Theory

### Counterfactual Explanations Formalism

For a model $f: \mathcal{X} \to \mathcal{Y}$ and input $\mathbf{x}$ with prediction $f(\mathbf{x}) = y$, a counterfactual $\mathbf{x}'$ satisfies:
$$f(\mathbf{x}') = y', \quad y' \neq y, \quad \text{proximity: } d(\mathbf{x}, \mathbf{x}') \text{ is minimized}$$

Standard methods add **sparsity** (minimize number of changed features) and **plausibility** (stay on the data manifold). DANCE additionally enforces **causal/domain constraints**.

### Causal Constraint Types

DANCE handles three types of constraints:

**Type 1: Monotonicity constraints** (linear)
$$x_i' \geq x_i \quad \text{(immutable upward, e.g., age, credit history length)}$$
$$x_i' \leq x_i \quad \text{(immutable downward, e.g., criminal record score)}$$

**Type 2: Functional dependency constraints** (nonlinear)
$$x_j' = g(x_i', \mathbf{x}_{-ij}') \quad \text{(e.g., debt-to-income = total_debt / income)}$$

Learned from data using nonlinear regression:
$$g(\cdot) = \arg\min \mathbb{E}[(X_j - g(X_i, \mathbf{X}_{-ij}))^2]$$

**Type 3: Causal structure constraints** (graph-based)
$$x_j' = f_j(\mathbf{Pa}_j', \epsilon_j) \quad \text{(structural causal model, if available)}$$

When expert-provided causal graphs are available (e.g., clinical guidelines, financial regulations), DANCE incorporates them directly. When not available, it learns linear and nonlinear dependencies from the training data.

### The DANCE Objective

DANCE generates $K$ diverse counterfactuals $\{\mathbf{x}'_1, ..., \mathbf{x}'_K\}$ by solving:

$$\min_{\{\mathbf{x}'_k\}} \sum_{k=1}^K \left[ d(\mathbf{x}, \mathbf{x}'_k) + \lambda_s \|\mathbf{x} - \mathbf{x}'_k\|_0 \right] + \lambda_d \mathcal{D}(\mathbf{x}'_1, ..., \mathbf{x}'_K)$$

subject to:
$$f(\mathbf{x}'_k) = y' \quad \forall k$$
$$C(\mathbf{x}'_k) \leq 0 \quad \forall k \quad \text{(domain constraints)}$$

where:
- $d(\cdot)$: distance metric (L1 for tabular, weighted by feature scales)
- $\|\mathbf{x} - \mathbf{x}'_k\|_0$: sparsity (number of changed features)
- $\mathcal{D}(\cdot)$: diversity penalty encouraging spread across the counterfactual space
- $C(\cdot)$: constraint set (monotonicity + dependency + causal)

### Diversity via Determinantal Point Processes

DANCE uses a **Determinantal Point Process (DPP)** to encourage diversity:

$$\mathcal{D}(\mathbf{x}'_1, ..., \mathbf{x}'_K) = -\log \det(\mathbf{L})$$

where $\mathbf{L}_{ij} = \kappa(\mathbf{x}'_i, \mathbf{x}'_j)$ is a kernel measuring similarity between counterfactuals. The DPP penalty encourages the counterfactual set to span different regions of the feature space.

---

## Main Ideas & Key Contributions

### 1. Unified Constraint Learning + Causal Graph Integration

DANCE is the first method to **unify** learned constraints (from data) with expert-provided constraints (from causal graphs and business rules) in a single optimization framework. Previous methods handle one or the other.

### 2. 140-Dataset Evaluation Scale

The evaluation on 140 public datasets is one of the largest systematic evaluations in the counterfactual explanation literature, providing strong evidence that DANCE's improvements generalize across data types, model types, and domains.

### 3. Real-World Case Study with Freshmail

The paper includes a **real industry case study** with Freshmail (email marketing platform) validating that the generated counterfactuals align with domain expert judgment and provide actionable guidance to customers whose campaigns are predicted to underperform.

### 4. Adaptive Constraint Discovery

When no expert causal graph is provided, DANCE learns both linear and nonlinear feature dependencies automatically:
- Linear: ordinary least squares regression
- Nonlinear: gradient boosted tree regression + constraint boundary detection

This makes DANCE applicable without domain expertise, while also accepting expert knowledge when available.

---

## Methodology & Implementation

### Experimental Setup

**Datasets:** 140 UCI and OpenML tabular classification datasets (binary and multi-class)  
**Models:** Logistic Regression, Random Forest, XGBoost, MLP, SVM  
**Evaluation per instance:** 5 diverse counterfactuals generated

### Baseline Methods
- **DICE** (Mothilal et al., 2020): DPP-based diversity, no causal constraints
- **NICE** (Brughmans et al., 2023): causal constraints, single counterfactual
- **CFNOW** (Leofante et al., 2023): constraint optimization, no diversity
- **CaRs** (counterfactuals with causal recourse, 2024): partial causal integration

### Evaluation Metrics

**Validity:** % of generated counterfactuals that actually flip the model prediction  
**Proximity:** average L1 distance to original instance  
**Sparsity:** average number of changed features  
**Plausibility:** % of counterfactuals satisfying all learned constraints  
**Diversity:** average pairwise distance across the $K$ counterfactuals  
**Constraint satisfaction rate:** % satisfying expert-provided constraints (on Freshmail dataset)

### Results Summary

| Method | Validity ↑ | Plausibility ↑ | Diversity ↑ | Proximity ↓ |
|---|---|---|---|---|
| DICE | 94% | 43% | 0.71 | 0.42 |
| NICE | 91% | 82% | 0.21 | 0.38 |
| CFNOW | 89% | 69% | 0.31 | 0.35 |
| **DANCE** | **96%** | **89%** | **0.68** | **0.37** |

DANCE achieves the best plausibility (closest to NICE) while maintaining DICE-level diversity — the combination not achieved by any prior method.

### Freshmail Case Study Results
- 92% of DANCE counterfactuals rated as "actionable and feasible" by Freshmail marketing experts
- Compared to 41% for DICE (implausible suggestions) and 74% for NICE (not diverse enough)
- Expert preferred DANCE suggestions in 87% of pairwise comparisons

### Limitations
- Nonlinear constraint learning can be computationally expensive for many-feature datasets
- When causal graphs are provided but incorrect, DANCE may generate systematically biased counterfactuals
- Optimization is non-convex; multiple runs may be needed for robust results
- Diversity-proximity tradeoff parameter $\lambda_d$ requires tuning

---

## Practical Applications & Real-World Use Cases

### Financial Services — Loan and Credit Decisions

DANCE's primary intended application: when a loan application is denied, provide actionable, diverse recourse explanations. Plausibility constraints ensure suggestions like "reduce debt-to-income ratio" are accompanied by *how* to do so given current income levels.

**Regulatory context:** EU Consumer Credit Directive and US Equal Credit Opportunity Act require lenders to provide specific, actionable reasons for credit denial. DANCE's constraint-aware counterfactuals satisfy this requirement more rigorously than unconstrained methods.

### Healthcare — Clinical Decision Support

Medical AI decisions (diagnosis, treatment recommendation, risk stratification) need counterfactuals that respect biological constraints:
- Age and comorbidity history are immutable
- Lab values have physiologically plausible ranges
- Treatment dependencies: prescribing drug A may require also prescribing drug B

DANCE can incorporate clinical guidelines as causal graph constraints, ensuring counterfactual treatment recommendations are clinically feasible.

### Human Resources — Hiring and Promotion

AI-assisted hiring and promotion decisions face GDPR and employment law requirements to provide non-discriminatory, actionable feedback. DANCE generates diverse recourse paths (e.g., "improving skill X" vs. "gaining experience Y") that respect constraints like protected attributes being immutable.

### Email Marketing (Freshmail Case Study)

Campaign performance prediction models can advise marketers on which campaign parameters to change. DANCE's domain-knowledge integration lets Freshmail encode marketing expertise: "send time affects open rate but not vice versa", "list quality has a minimum floor", etc.

### Insurance Underwriting

Risk pricing models need explainable decisions for regulatory approval. DANCE provides constraint-aware recourse: "your premium would decrease if you increased your deductible or added safety features" — suggestions that respect insurance business rules.

---

## Insights & Implications

### Closing the Gap Between XAI Research and Practice

The Freshmail case study and 140-dataset evaluation address a persistent criticism of XAI research: that methods work well in academic settings but fail when applied to real business problems with domain constraints. DANCE's approach of explicitly incorporating domain knowledge bridges this gap.

### The Plausibility-Diversity Tradeoff

The paper provides the first systematic evidence that plausibility and diversity are *not* fundamentally in conflict — they can both be achieved simultaneously when constraints are explicitly represented. Prior methods achieve one at the expense of the other because they don't represent constraints formally.

### Connecting to Causal XAI

DANCE's causal graph integration represents a practical step toward the causal XAI framework advocated by Karimi (2026) — it is a working example of Rung-3 XAI that provides counterfactual recourse grounded in (partial) causal knowledge. Future extensions should incorporate full SCM estimation.

### Practical Guidance for Deploying Counterfactual XAI

The case study yields actionable deployment lessons:
1. Start with monotonicity constraints (most impactful, easiest to specify)
2. Learn functional dependencies from data (nonlinear learning essential for real data)
3. Validate with domain experts before deployment (constraint specification is iterative)
4. Provide 3-5 diverse counterfactuals rather than one (users respond better to options)

### Open Questions
- How does DANCE scale to text and image inputs (non-tabular)?
- Can DANCE provide confidence bounds on constraint satisfaction?
- How to handle counterfactuals where causal graph is partially known vs. completely unknown?
- Can constraint learning identify causal vs. spurious dependencies automatically?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2511.20236](https://arxiv.org/abs/2511.20236)
- **Dependencies:** Python, scikit-learn, CVXPY (for constraint optimization), pgmpy (for causal graphs)

### Implementation Sketch
```python
from dance import DANCE, ConstraintSet, CausalGraph

# Define constraints
constraints = ConstraintSet()
constraints.add_monotonicity("age", direction="immutable")
constraints.add_monotonicity("credit_history_length", direction="non_decreasing")
constraints.add_functional_dependency("debt_to_income", "=", lambda debt, income: debt/income)

# Optional: provide causal graph from domain experts
causal_graph = CausalGraph()
causal_graph.add_edge("income", "savings")  # income causes savings, not vice versa
causal_graph.add_edge("education", "income")
causal_graph.add_edge("age", "credit_history_length")

# Initialize DANCE
dancer = DANCE(
    model=trained_classifier,
    constraint_set=constraints,
    causal_graph=causal_graph,  # optional
    n_counterfactuals=5,
    diversity_weight=0.5,
    learn_constraints_from_data=True  # auto-discover nonlinear dependencies
)

# Generate diverse, actionable, constraint-satisfying counterfactuals
instance = pd.Series({"age": 35, "income": 45000, "debt": 15000, 
                       "credit_history_length": 5, ...})

counterfactuals = dancer.generate(instance, desired_class=1)
for i, cf in enumerate(counterfactuals):
    print(f"\nCounterfactual {i+1}:")
    changes = cf[cf != instance]
    print(f"  Changes needed: {changes.to_dict()}")
    print(f"  Constraint satisfied: {dancer.verify_constraints(cf)}")
    print(f"  Predicted class: {trained_classifier.predict([cf])[0]}")
```

---

## Related Work & Context

### Foundational Counterfactual Work
- **Wachter et al. (2017)**: Counterfactual explanations without opening the black box
- **Ustun et al. (2019)**: Actionable recourse in linear classification
- **Karimi et al. (2021)**: Algorithmic recourse under causal models

### Diversity-Focused Methods
- **Mothilal et al. (2020)**: DICE — diverse counterfactuals using DPP
- **Russell (2019)**: Multiple diverse counterfactuals for explanations

### Constraint-Focused Methods
- **Poyiadzi et al. (2020)**: FACE — feasibility-aware counterfactuals
- **Brughmans et al. (2023)**: NICE — causal and immutability constraints
- **Dandl et al. (2020)**: MEPS — multi-objective evolutionary counterfactuals

### Connection to Causal Inference
- **Pearl (2009)**: Structural causal models — provides the formal basis for DANCE's causal constraints
- **Karimi et al. (2020)**: Causal counterfactuals for algorithmic recourse
- **Karimi (2026)**: XAI is causality in disguise — DANCE provides empirical support for this thesis

### Where This Leads
1. **Temporal DANCE**: counterfactuals with time-constrained recourse (what to do now vs. in 6 months)
2. **Group DANCE**: similar recourse paths for individuals with similar profiles
3. **Multi-stakeholder DANCE**: recourse that satisfies constraints of both the individual and the institution
4. **Uncertainty-aware DANCE**: counterfactuals that account for model uncertainty and data noise

---

*Sources:*
- [arxiv.org/abs/2511.20236](https://arxiv.org/abs/2511.20236)
