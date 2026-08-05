# When Interpretability Is Unequally Distributed: Fairness in Hybrid Interpretable Models

## Executive Summary

This paper exposes a critical yet overlooked fairness vulnerability in hybrid interpretable models: "Interpretability Coverage Disparity" (ICD). While hybrid models—which combine transparent decision-making with black-box fallback components—offer flexible accuracy-interpretability tradeoffs, demographic groups may systematically receive unequal access to interpretability. Some individuals consistently receive explainable decisions while others are disproportionately routed to opaque black-box components. This work formalizes ICD as a procedural fairness metric and demonstrates that simple coverage-disparity constraints can eliminate these disparities while maintaining model accuracy and performance.

## Problem Statement

### The Gap in Hybrid Interpretable Models

Hybrid interpretable models represent a pragmatic approach to the accuracy-interpretability tradeoff: they route some instances to inherently interpretable components (e.g., decision trees, rule-based systems, linear models) while deferring harder cases to high-performing black-box components (e.g., neural networks). This flexibility has made hybrid models increasingly popular in high-stakes domains like healthcare, credit lending, and legal decision-making.

However, this flexibility introduces a subtle but severe fairness problem: the **routing decision itself**—which determines whether an individual receives an interpretable or black-box decision—becomes a new point of algorithmic discrimination. The paper asks: *Are certain demographic groups (defined by protected attributes like gender, race, age) systematically steered toward more or less interpretable components?*

### Why This Matters

Unlike traditional algorithmic fairness metrics (accuracy parity, equalized odds), which measure disparities in *predictions*, ICD measures disparities in *explainability access*. This distinction is critical:

- **Procedural Justice**: Even if predictions are statistically fair, denying interpretability to some groups violates procedural fairness principles and erodes trust.
- **Regulatory Compliance**: GDPR, the EU AI Act, and emerging regulations increasingly mandate the right to explanation. Systematically denying explanations to demographic groups creates legal and ethical violations.
- **Accountability Gap**: When black-box components make errors, only those routed to transparent components can scrutinize and contest decisions. Disparities in routing create accountability disparities.

### Related Work and Prior Limitations

Prior fairness research has focused on **outcome fairness** (are predictions equitable?) but rarely examined **explainability access fairness** (is interpretability equitable?). The intersection of fairness and interpretability remains underexplored:

- **Fairness work** assumes all decisions receive equal scrutiny; it doesn't account for routing to opaque systems.
- **Interpretability work** assumes users have equal access to explanations; it doesn't model fairness constraints.
- **Hybrid model work** treats routing as a technical optimization problem, not a fairness concern.

This paper bridges these three areas, introducing a fairness lens to hybrid interpretable model design.

## Core Concepts & Theory

### Hybrid Interpretable Models: Architecture and Routing

A hybrid interpretable model $M_H$ consists of:
- **Transparent Component** ($M_T$): Inherently interpretable, provides natural explanations (e.g., decision trees, sparse linear models, rule-based systems)
- **Black-Box Component** ($M_B$): High-performance but opaque (e.g., neural networks, ensemble methods)
- **Routing Function** ($R$): Assigns instances to either $M_T$ or $M_B$ based on learned or heuristic criteria

The overall prediction is:
$$\hat{y} = M_T(x) \text{ if } R(x) = \text{transparent, else } M_B(x)$$

Routing typically balances:
- **Accuracy**: Send hard instances to $M_B$ for better performance
- **Interpretability**: Send easy instances to $M_T$ for explainability
- **Coverage**: Ensure $M_T$ handles enough instances to be useful

### Interpretability Coverage Disparity (ICD)

ICD formalizes the fairness concern using a demographic-parity lens. For a protected attribute $A$ (e.g., gender) with groups $a_1, a_2, \ldots, a_k$:

$$\text{ICD}(A) = \max_{i,j} \left| P(R(X) = \text{transparent} | A = a_i) - P(R(X) = \text{transparent} | A = a_j) \right|$$

**Interpretation**:
- **ICD = 0**: Perfect parity—all demographic groups are routed to the transparent component at the same rate.
- **ICD = 1**: Maximum disparity—some groups always use transparent decisions; others always use the black-box.
- **ICD ∈ [0, 1]**: Measures the largest gap in interpretability access between any two groups.

This extends demographic parity fairness principles (equal outcome rates across groups) to explainability routing decisions.

### Why Routing Creates Disparities

Hybrid models learn routing implicitly through:
1. **Feature-based routing**: The routing function $R$ learns to correlate model difficulty with input features. If model difficulty correlates with protected attributes (e.g., certain demographic groups' instances are systematically harder for $M_T$), routing becomes biased.
2. **Data distribution shifts**: Protected attributes correlate with data distribution shifts, which affect $M_T$'s performance. Some groups' distributions may fall outside $M_T$'s learned boundaries.
3. **Proxy discrimination**: Even if $A$ isn't used directly, highly correlated features can indirectly create ICD.

### Formalizing Coverage-Disparity Constraints

To mitigate ICD, the paper introduces coverage-disparity constraints in optimization:

$$\min_{M_T, M_B, R} \quad \text{Accuracy Loss}$$

$$\text{subject to:} \quad \text{ICD}(A) \leq \epsilon \text{ for all protected attributes } A$$

where $\epsilon$ is a fairness tolerance parameter. This constraint forces the routing function to maintain roughly equal interpretability coverage across demographic groups while maintaining accuracy.

**Solving the constrained optimization**: The paper adapts techniques from fairness-constrained learning (Lagrangian relaxation, constraint-aware loss weighting) to force balanced routing decisions.

## Main Ideas & Key Contributions

### 1. Identifying a New Fairness Dimension

**Contribution**: The paper identifies and formally defines Interpretability Coverage Disparity (ICD) as a distinct fairness concern in hybrid interpretable models—one that prior work on algorithmic fairness and interpretability has overlooked.

**Innovation**: Rather than focusing on outcome fairness (do predictions treat groups equally?), ICD shifts attention to **process fairness** (do groups receive equal access to explanation?). This is a crucial distinction for regulatory compliance and procedural justice.

**Why novel**: Prior fairness work assumes all decisions are equally scrutable; prior interpretability work assumes all users have equal access to explanations. This paper unifies these perspectives.

### 2. Empirical Demonstration of ICD in Real Models

**Contribution**: Extensive experiments across four hybrid interpretable learning methods, three standard fairness benchmarks, and multiple sensitive attributes reveal that substantial ICD exists "in the wild."

**Key finding**: ICD is most severe in intermediate transparency regimes (where both $M_T$ and $M_B$ handle significant fractions of instances), with empirical ICD values often approaching 1.0—indicating extreme disparities where certain demographic groups are systematically funneled to opaque components.

**Evidence of real harm**: The paper demonstrates that demographic groups experiencing higher ICD have systematically less accountability because they cannot scrutinize their decisions through transparent models.

### 3. Practical Solutions: Coverage-Disparity Constraints

**Contribution**: Simple coverage-disparity constraints can significantly reduce ICD in exact hybrid learning methods.

**Results**: Adding fairness constraints reduces ICD while maintaining:
- Minimal accuracy loss (often <1-2% impact)
- Marginal impact on interpretability-accuracy tradeoff curves
- In several settings, ICD mitigation also improves standard fairness metrics (e.g., equalized odds)

**Practical feasibility**: Unlike some fairness interventions, coverage-disparity constraints integrate cleanly into existing hybrid learning optimization.

### 4. Theoretical Grounding in Procedural Fairness

**Contribution**: ICD is grounded in procedural fairness theory—the principle that processes should treat individuals fairly, not just outcomes. This provides ethical and legal justification for the approach.

**Implications**: ICD violations constitute both procedural unfairness and potential regulatory violations (GDPR right to explanation, EU AI Act transparency mandates).

## Methodology & Implementation

### Experimental Setup

**Hybrid Learning Methods Tested**:
1. **Hybrid Linear Models**: Combine sparse linear regression ($M_T$) with neural network ($M_B$)
2. **Hybrid Tree Models**: Combine decision trees ($M_T$) with gradient boosting ($M_B$)
3. **Prototype-Based Models**: Classify by similarity to learned prototypes ($M_T$) or use deep learning ($M_B$)
4. **Rule-Based Models**: Disjunctive normal form rules ($M_T$) with neural fallback ($M_B$)

**Fairness Benchmarks**:
- **Adult Income Dataset**: Predict income (protected: gender, age)
- **German Credit Dataset**: Credit approval (protected: gender, age)
- **COMPAS Dataset**: Criminal recidivism (protected: race)

Each dataset contains multiple protected attributes to assess ICD across different dimensions.

**Sensitive Attributes Evaluated**:
- Gender (binary and multi-class)
- Race/Ethnicity
- Age (binned into age groups)
- Multiple intersectional combinations

### ICD Measurement Protocol

1. Train hybrid models with varying transparency budgets (fraction of instances routed to $M_T$)
2. For each trained model, compute routing decisions for all test instances
3. Calculate $P(\text{transparent} | A = a)$ for each demographic group $a$
4. Compute ICD as the maximum pairwise difference in these probabilities

### Mitigation Strategy: Constraint-Based Learning

**Algorithm**:

```
Input: Training data D, protected attribute A, fairness tolerance ε
Initialize: M_T, M_B, R as random
For each epoch:
  1. Compute routing decisions R(x) for all x ∈ D
  2. Measure current ICD(A)
  3. If ICD(A) > ε:
     - Compute fairness-violating groups
     - Upweight instances from underrepresented groups in M_T's training
     - Downweight instances from overrepresented groups
  4. Train M_T, M_B, R on reweighted data
  5. Check accuracy-fairness tradeoff
```

**Hyperparameter tuning**: Fairness tolerance $\epsilon$ (ranging from 0.0 to allow 0.3) to explore accuracy-fairness curves.

### Results Summary

[Exact figures unavailable — see full paper for detailed results]

**Key metrics evaluated**:
- **ICD reduction**: From original values (often 0.5–1.0) to near-zero with constraints
- **Accuracy impact**: Typically <2% accuracy loss when reducing ICD
- **Interpretability coverage**: Fairness constraints may reduce the interpretable component's overall coverage but balance it across groups
- **Standard fairness metrics**: Demographic parity and equalized odds also improve in several settings when ICD constraints are applied

**Robustness findings**:
- Constraint effectiveness varies by dataset and model architecture
- Exact methods (optimal optimization) achieve better ICD reduction than heuristic routing
- Larger fairness budgets (higher $\epsilon$) allow higher accuracy while maintaining fairness

## Practical Applications & Real-World Use Cases

### 1. Healthcare Decision-Making

**Application**: Clinical triage systems that route patients to rule-based diagnostic systems or deep learning models based on complexity.

**Problem**: If certain racial or age groups are systematically routed to opaque deep learning models while others receive transparent rule-based explanations, trust and accountability suffer—especially critical when treatment decisions affect health outcomes.

**Solution**: Apply coverage-disparity constraints to ensure all demographic groups receive transparent explanations of triage decisions. Patients denied explicit reasoning for referrals to specialists lose trust and may not comply with treatment.

**Regulatory context**: Under GDPR Article 22 and emerging healthcare regulations (FDA guidance on algorithmic governance), patients have a right to understand medical decisions. ICD violations create compliance risks.

### 2. Financial Services and Credit Lending

**Application**: Loan approval systems that route applications to transparent scoring models (e.g., rule-based decision trees) or black-box neural networks.

**Problem**: If applicants from certain protected groups (e.g., minorities) are disproportionately routed to opaque models, they cannot understand why their loans were denied or appeal based on reasoning—violating procedural fairness.

**Solution**: Hybrid models with ICD constraints ensure all applicants receive transparent explanations, enabling contestation and appeals. This is especially important in regulated industries like lending.

**Regulatory context**: Fair Credit Reporting Act (FCRA) and GDPR both mandate explainability for adverse decisions. ICD violations create legal liability.

### 3. Criminal Justice and Recidivism Prediction

**Application**: Risk assessment systems for parole and sentencing that combine transparent risk factors with black-box predictive models.

**Problem**: Over-reliance on opaque models for certain demographic groups (historically, minorities and vulnerable populations) reduces procedural fairness in high-stakes legal decisions.

**Solution**: ICD-constrained models ensure all defendants receive transparent risk assessments, enabling legal challenges and appeals based on explicit reasoning.

**Real-world impact**: The COMPAS recidivism case study demonstrates how algorithmic bias in routing (and outcomes) disproportionately affects minority defendants. ICD constraints directly address this routing disparity.

### 4. Content Moderation and Platform Governance

**Application**: Social media platforms use interpretable rules for marginal cases (first-time violators, borderline content) and opaque neural networks for complex moderation decisions.

**Problem**: If certain user groups (e.g., specific geographies or languages) are disproportionately subject to opaque moderation decisions, they lose recourse and transparency—creating platform governance fairness issues.

**Solution**: Enforce equal interpretability coverage so all users receive transparent explanations for moderation decisions, enabling appeals and improving trust.

## Insights & Implications

### For Trustworthy AI

**Key insight**: Trustworthiness isn't only about outcome fairness—it's about process fairness. Denying explanation access to some groups, even if outcomes are statistically fair, violates transparency principles essential to trustworthy AI.

**Implication**: AI governance frameworks must address not just prediction bias but also **explanation access bias**. Regulatory frameworks like the EU AI Act should explicitly cover ICD-type fairness concerns.

### For the Interpretability Field

**Key insight**: Interpretability research has largely assumed uniform access to explanations. In hybrid systems, explanations become a scarce resource allocated by routing functions, introducing fairness concerns.

**Implication**: Future interpretability work should consider:
- Fairness implications of routing decisions
- Explanations as a fairness resource
- Procedural fairness in hybrid model design
- Human-in-the-loop fairness evaluation

### For Algorithmic Fairness Research

**Key insight**: Fairness research has focused on outcome parity. ICD shows that fairness must also ensure equal access to **tools for contesting** outcomes (i.e., explanations).

**Implication**: Fairness definitions should be expanded to include:
- Procedural fairness in decision processes
- Explainability as a fairness dimension
- Accountability mechanisms across groups
- Intersectional fairness (how do disparities interact?)

### Limitations and Open Questions

1. **Defining "interpretability"**: The paper treats transparent models as inherently interpretable, but this assumption may not hold for all users. Interpretability is subjective; what's interpretable to experts may confuse non-technical users.

2. **Scalability to large systems**: ICD constraints are demonstrated on moderate-sized datasets and models. Scaling to large-scale systems (billions of users, massive models) remains open.

3. **Multi-objective optimization**: Balancing accuracy, interpretability, and fairness simultaneously is complex. The paper doesn't fully explore the three-way tradeoff space.

4. **Temporal fairness**: ICD is measured at a single snapshot. How do fairness constraints affect ICD stability over time as data distributions shift?

5. **Game-theoretic aspects**: Could users game the routing system if they learn which attributes trigger transparent vs. black-box treatment?

### Future Research Directions

1. **Interactive and dynamic fairness**: Develop routing functions that adapt fairness constraints based on user feedback and temporal dynamics.

2. **Fairness certification**: Can we formally verify that a hybrid model satisfies ICD constraints under worst-case scenarios?

3. **Explaining fairness constraints**: When enforcing ICD constraints requires routing decisions to be seemingly arbitrary, how do we explain fairness interventions to users?

4. **Intersectional ICD**: Extend ICD to multiple protected attributes simultaneously, measuring fairness across intersectional groups (e.g., women of color).

5. **User studies**: Empirically test whether ICD-constrained models improve user trust, contestation, and satisfaction compared to unconstrained baselines.

## Code & Resources

### Official Implementations

- **Paper repository**: Link to official code (if available) on GitHub [to be added upon publication]
- **ArXiv PDF**: [https://arxiv.org/pdf/2605.28626](https://arxiv.org/pdf/2605.28626)

### Dependencies and Environment

- **Programming language**: Python 3.8+
- **Key libraries**: scikit-learn (interpretable models), PyTorch or TensorFlow (black-box components), numpy, pandas, scipy
- **Fairness libraries**: fairlearn, AIF360 (for fairness metric computation)
- **Visualization**: matplotlib, seaborn

### Quick Start Guide

[Specific implementation details to be added from the paper's GitHub repository]

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Load benchmark datasets (Adult, German Credit, COMPAS)
4. Train hybrid models with `--fairness-constraint` flag
5. Evaluate ICD and fairness metrics using provided evaluation scripts
6. Visualize accuracy-fairness tradeoff curves

### Computational Requirements

- CPU: Multi-core processor for parallel dataset operations
- GPU: Optional; accelerates neural network training for black-box components
- Memory: 8GB+ RAM for benchmark datasets
- Training time: Minutes to hours depending on dataset size and model complexity

## Related Work & Context

### Connection to Broader xAI and Fairness Communities

This paper addresses the intersection of **explainable AI** and **algorithmic fairness**, two critical areas in trustworthy ML:

**Explainable AI (xAI) Context**:
- Builds on LIME (Local Interpretable Model-agnostic Explanations) and SHAP (Shapley Additive exPlanations) frameworks, which focus on explaining individual predictions
- Unlike local explanation methods, this work examines system-level fairness in explanation access
- Relates to inherently interpretable models (decision trees, linear models, rule-based systems)

**Algorithmic Fairness Context**:
- Extends demographic parity fairness to routing decisions
- Relates to fairness research on equalized odds, demographic parity, and calibration within groups
- Introduces procedural fairness—a less-studied but equally important fairness dimension
- Connects to regulatory fairness mandates (GDPR Article 22, EU AI Act)

### Related Papers and Concepts

1. **Hybrid Interpretable Models**: [Learning Hybrid Interpretable Models: Theory, Taxonomy, and Methods](https://arxiv.org/abs/2303.04437) provides foundational taxonomy; this work adds fairness lens.

2. **Fairness in Machine Learning**: SoK papers like [Taming the Triangle: Fairness, Interpretability, and Privacy](https://arxiv.org/abs/2312.16191) highlight tensions between these dimensions.

3. **Procedural Fairness in AI**: Related to work on recourse, contestability, and due process in algorithmic decision-making.

4. **Intersectional Fairness**: Future work should extend ICD to intersectional groups, building on foundational work by Buolamwini & Gebru and others.

### Community Relevance

- **FAccT (Fairness, Accountability, and Transparency) Community**: Directly relevant to conference topics on fairness-interpretability tradeoffs
- **ICML Fairness Track**: Accepted at ICML 2026, indicating high visibility in top ML venue
- **Responsible AI Initiative**: Contributes to frameworks for trustworthy AI deployment
- **AI Governance**: Informs regulatory thinking on explainability and fairness mandates

### Where This Might Lead

1. **Regulatory standards**: ICD could become a fairness metric required in AI governance frameworks (EU AI Act, forthcoming US AI executive orders).

2. **Industry practices**: Adoption in high-stakes domains (healthcare, finance, legal) where explainability and fairness are mandated.

3. **Methodological advances**: Spawn research on fairness-constrained hybrid learning, intersectional ICD, and dynamic fairness.

4. **Tooling**: Fairness libraries like FairLearn and AIF360 may integrate ICD measurement and mitigation.

## Summary: Why This Paper Matters for xAI

"When Interpretability Is Unequally Distributed" identifies a critical and overlooked fairness problem in hybrid interpretable models: ensuring all demographic groups receive equal access to explanation, not just equal prediction outcomes. By formalizing Interpretability Coverage Disparity (ICD) and demonstrating practical mitigation through fairness constraints, this work bridges explainability and fairness—two pillars of trustworthy AI.

The paper's insights are immediately actionable: practitioners building hybrid models can apply coverage-disparity constraints to ensure fair explanation access. Its regulatory implications are significant: ICD violations create compliance risks under GDPR, the EU AI Act, and emerging fairness legislation.

Most importantly, this work reframes an overlooked fairness dimension: **procedural justice through transparency access**. It shifts the xAI community's focus from "can we explain model predictions?" to "are explanations fairly distributed?"—a question essential to building trustworthy AI systems.
