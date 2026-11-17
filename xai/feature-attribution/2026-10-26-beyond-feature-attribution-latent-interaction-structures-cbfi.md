# Beyond Feature Attribution: Recovering Latent Interaction Structures in Machine Learning Models via Localized CBFI

**ArXiv ID:** [2610.34962](https://arxiv.org/abs/2610.34962)

**Authors:** Sejong Oh

**Submitted:** October 26, 2026

**Subject:** Machine Learning (cs.LG)

## Executive Summary

This paper addresses a fundamental limitation in explainable AI: standard attribution methods like SHAP and LIME assign importance scores to individual features while implicitly absorbing feature interactions into those scores, making it invisible how features work together. The paper proposes a **localized case-based feature importance (CBFI) framework** that explicitly decomposes instance-level predictions into main effects and pure interactions, enabling discovery of which feature combinations truly drive model decisions. This advancement is critical for trustworthy AI, especially in high-stakes domains where understanding feature synergies can reveal hidden model logic or unintended behaviors.

## Problem Statement

### The Interaction Invisibility Problem

Conventional feature attribution methods operate under an additive assumption: they decompose a model's prediction into individual feature contributions that sum to the final output. However, real-world machine learning models often rely on **nonlinear interactions**—cases where the combined effect of two or more features is fundamentally different from the sum of their individual effects.

**Key limitations of existing approaches:**

1. **Implicit interaction folding:** Methods like SHAP and LIME compute marginal feature contributions, but when features interact, the interaction effects get absorbed into the individual feature scores, distorting the attribution landscape.

2. **Misleading feature rankings:** A feature might receive high importance due to its strong interactions with another feature, not its standalone impact. Practitioners cannot distinguish between "this feature is important on its own" and "this feature is important only when combined with another feature."

3. **Hidden model logic:** Complex interactions can reveal whether a model has learned unintended spurious patterns or Clever Hans-like artifacts that appear to work by folding dependent features into single importance scores.

4. **Limited recourse:** When explaining why a model made a certain decision to an end-user or stakeholder, saying "feature X is important" misses the actionable insight: "feature X matters only when feature Y takes a certain value."

### Motivation

The paper argues that understanding **latent interaction structures**—the hidden feature synergies that drive predictions—is essential for:
- Detecting model failures and unintended dependencies
- Building more robust and interpretable machine learning systems
- Generating actionable explanations for domain experts and regulators
- Enabling algorithmic recourse (e.g., "to change the outcome, you must change both features X and Y together")

## Core Concepts & Theory

### Additive Feature Importance vs. Interactive Decomposition

**Traditional additive model:**
A model's prediction is typically explained as:
```
Prediction = f(x) = baseline + w₁·φ₁(x) + w₂·φ₂(x) + ... + wₙ·φₙ(x)
```
where φᵢ(x) are feature contributions that sum to the final prediction. This assumes features combine additively.

**The interaction problem:**
In reality, models often exhibit:
```
f(x) = main_effects + interaction_effects
```

For example, in a medical risk model, the risk of a disease might be:
- 10 points if blood pressure is high, OR
- 5 points if cholesterol is high, BUT
- 50 points if BOTH are high (synergistic effect, not 15 points)

Standard attribution methods would distribute these 50 points among the features, failing to reveal the critical synergy.

### Case-Based Feature Importance (CBFI)

The paper builds on the CBFI framework to perform an **instance-specific decomposition**:

For each prediction instance, decompose into:
1. **G1 (main effects):** The contribution each feature makes independently, calculated by holding other features at their average/baseline values
2. **G4 (pure interactions):** The portion of the prediction that cannot be explained by individual feature contributions—the residual effect that emerges only from feature combinations

**Formal decomposition:**
```
Prediction = baseline + G1 (main effects) + G4 (interactions)
```

#### Why G1 and G4?

- **G1:** Marginal contribution when other features are at their typical values (computed via conditional expectation)
- **G4:** The "unexplained" portion after accounting for main effects—this is where feature synergies hide

The localized CBFI framework ensures these components are **locally consistent** for each instance, providing case-specific explanations rather than global averages.

### Mathematical Foundation

For a given instance, localized CBFI:

1. **Computes G1** using conditional feature importance, estimating what each feature contributes in its local neighborhood
2. **Computes G4** as the residual: `G4 = actual_prediction - baseline - G1`
3. **Identifies feature combinations** by examining which pairs or groups of features co-vary in regions where G4 is large

When G4 is high, it signals that the model's behavior in that region is driven by feature interactions, not individual feature effects.

## Main Ideas & Key Contributions

### 1. Explicit Interaction Decomposition

**Problem addressed:** Standard attribution methods hide interactions.

**Solution:** The localized CBFI framework provides a principled decomposition that:
- Separates main effects (G1) from pure interactions (G4)
- Shows clearly when a prediction is driven by feature synergies vs. independent contributions
- Enables practitioners to ask: "Is this feature important by itself, or only in combination with others?"

**Impact:** Practitioners can now audit whether models rely on spurious feature dependencies or learn robust, generalizable patterns.

### 2. Feature Interaction Graphs

**Key contribution:** Aggregating instance-level G4 values across a dataset yields a **feature interaction graph**:
- **Nodes:** Individual features
- **Edges:** Weighted by co-occurrence in high-G4 regions (instances where interactions dominate)
- **Edge weight:** Indicates interaction strength—how much G4 varies when both features co-vary

**Practical insight:** This graph reveals the "dependency network" of a model, showing which features the model relies on working together.

Example (insurance dataset):
- Edge between Age and Income might be strong if the model uses them interactively (e.g., "high income at young age" vs. "high income at old age" have different risk profiles)
- Edge between Age and Health Status might be weak if the model treats them independently

### 3. Comparison with LIME and SHAP

**Key empirical finding:** Localized CBFI reveals interactions that LIME and SHAP do not explicitly capture.

**Why LIME/SHAP miss interactions:**
- LIME uses local linear approximations (inherently additive)
- SHAP computes Shapley values, which also assume additive combination
- Both methods are designed for intuition and trust, not for capturing nonlinear dependencies

**When CBFI shines:** On datasets with known feature interactions (e.g., wine quality: acidity × pH, alcohol × residual sugar), localized CBFI shows explicitly which pairs interact, while LIME/SHAP obscure these relationships by distributing interaction effects.

### 4. Detecting Model Pathologies

**Application:** Use G4 to detect Clever Hans behavior—when a model learns spurious correlations or artifact patterns instead of causal logic.

Example: A vision model trained on artifact-contaminated MNIST (images containing background patterns correlated with class):
- Traditional attribution shows high importance for background pixels
- Localized CBFI reveals these pixels interact strongly with digit pixels
- High G4 in background regions signals that the model's decisions depend on this suspicious feature combination
- This alerts practitioners to data quality issues

## Methodology & Implementation

### Algorithm Overview

**Input:** A trained model f(x), instance x, training data D (for reference distributions)

**Step 1: Compute baseline**
```
baseline = E[f(x')] where x' is sampled from D
```

**Step 2: For each feature i, compute G1ᵢ (main effect)**
```
G1ᵢ = E[f(x with feature i varied, others at their average values)]
     - E[f(x with feature i at average, others at their average values)]
```

This isolates the marginal contribution of feature i by holding others constant.

**Step 3: Compute total G1**
```
G1_total = sum of all G1ᵢ
```

**Step 4: Compute G4 (interactions)**
```
G4 = f(x) - baseline - G1_total
```

If G4 is significantly nonzero, feature interactions are driving the prediction.

**Step 5: Identify interacting features**
Examine which pairs (i, j) have high correlation in regions where G4 is large, or use:
```
interaction_strength(i, j) = cov(feature_i, feature_j | G4 is high)
```

### Computational Complexity

- **Per-instance:** O(d²) in the number of features d (or O(d) with approximations)
- **Scalability:** Feasible for tabular data with hundreds of features; for high-dimensional data (images, text), requires dimensionality reduction or feature grouping

### Key Hyperparameters

1. **Reference distribution for baselines:** Use training data marginals or domain-specific reference points
2. **Neighborhood size for localization:** Balance between local interpretability and stability
3. **Interaction detection threshold:** Define when G4 is "large enough" to signal meaningful interactions

### Datasets and Experiments

**Tested on:**

1. **Wine Quality Classification** [Exact figures unavailable — see full paper]
   - Predict wine quality (good/bad) from physicochemical properties
   - Known interactions: acidity × pH, alcohol × residual sugar
   - Localized CBFI successfully identified these interactions; LIME/SHAP missed them

2. **Medical Insurance Regression** [Exact figures unavailable — see full paper]
   - Predict insurance charges from age, BMI, smoker status, region
   - Discovered: Age interacts strongly with Smoker status (young smokers have different charge profiles than old smokers)
   - Localized CBFI explicitly surfaced this; standard methods distributed the effect across features

3. **MNIST with Artifact Contamination**
   - Artifact-contaminated training images
   - Localized CBFI detected high G4 in background-pixel regions, alerting to data quality issues
   - Demonstrated utility for detecting Clever Hans effects

**Evaluation metrics:**
- Fidelity: How well does (G1 + G4) reconstruct the original prediction?
- Interaction specificity: Can the method identify ground-truth feature interactions?
- Stability: Consistency across similar instances

[Exact metrics and numerical results unavailable — see full paper for complete evaluation]

## Practical Applications & Real-World Use Cases

### 1. Healthcare and Clinical Risk Models

**Use case:** Predicting readmission risk or treatment outcomes

**Why interactions matter:**
- A patient's age might interact with kidney function: a 70-year-old with moderate kidney decline faces different risk than a 40-year-old with the same kidney function
- Drug interactions: the effect of Drug A depends on whether the patient is also taking Drug B

**Benefit:** Clinicians can understand not just "age and kidney function are important," but specifically "how do age and kidney function combine to determine risk?" This enables personalized, interaction-aware care plans.

**Regulatory angle:** EU AI Act and FDA regulations increasingly require explainability for high-stakes medical decisions. Showing feature interactions explicitly strengthens compliance.

### 2. Financial Services and Credit Decisions

**Use case:** Credit scoring, loan approval, fraud detection

**Why interactions matter:**
- Income interacts with debt-to-income ratio: high income with high debt is different from high income with low debt
- Geographic factors interact with transaction type: unusual transaction patterns in unfamiliar locations are more suspicious

**Benefit:** Financial institutions can defend lending decisions with interaction-aware explanations: "We approved the loan because the applicant has both high income AND low existing debt, which together indicate low risk." This reduces bias and improves fairness audits.

**Algorithmic recourse:** Instead of "increase your income by $10K," the system can suggest "either increase income or reduce debt," revealing which combinations matter.

### 3. Autonomous Systems and Safety-Critical AI

**Use case:** Autonomous vehicle decision-making, robotics

**Why interactions matter:**
- Steering decisions interact with speed and road conditions: the right action depends on combinations of these factors, not each in isolation
- Collision avoidance: the urgency to brake depends on distance AND relative velocity together

**Benefit:** Safety teams can audit whether the model correctly learns feature interactions (e.g., "brake hard when both speed is high AND object is near"), detecting failure modes early.

### 4. Manufacturing and Anomaly Detection

**Use case:** Predicting equipment failures

**Why interactions matter:**
- Sensor readings interact: temperature AND vibration together might indicate bearing failure, but neither alone is diagnostic

**Benefit:** Maintenance teams understand which sensor combinations signal trouble, enabling smarter predictive maintenance schedules.

### 5. Fairness and Bias Auditing

**Use case:** Detecting discriminatory model behaviors

**Why interactions matter:**
- A model might be fair for each demographic group separately but exhibit disparate impact when groups interact with other features
- Example: Hiring model might be fair by gender alone, but discriminatory when gender interacts with job title or location

**Benefit:** Localized CBFI reveals these hidden disparities by showing interaction-driven predictions that differ across groups.

## Insights & Implications

### 1. Beyond Additive Explanations

The paper challenges a foundational assumption in explainable AI: that explanations should be additive (sum of individual feature contributions). Real models often work multiplicatively or through complex synergies, and explanations must reflect that complexity.

**Implication:** Future xAI methods should routinely consider and surface interactions, not hide them under the guise of simplicity.

### 2. Rethinking Model Trust

Traditional feature attribution might make a model *appear* trustworthy (each feature gets a clear score), but if it hides critical interactions, it creates a false sense of understanding. Localized CBFI enables *true* trust by exposing the full logic.

**Implication:** Practitioners must move from "this method is interpretable" to "this method reveals all the mechanisms driving the model," including interactions.

### 3. Interaction-Aware Model Development

If practitioners understand which feature interactions their models rely on, they can:
- Design better features that capture these interactions explicitly
- Regularize or simplify models that over-rely on spurious interactions
- Validate whether interactions are causal or correlational

**Implication:** Localized CBFI can close the loop from post-hoc explanation to model improvement.

### 4. Limitations and Open Questions

**Acknowledged challenges:**
- **Computational cost:** Scales quadratically with features; approximations needed for high-dimensional data
- **Interpretability of G4 itself:** G4 can be large but hard to interpret if many features interact; feature interaction graphs help but can be complex
- **Stability with small samples:** Localization works best with sufficient data to estimate local neighborhoods
- **Extension to hierarchical interactions:** Current method focuses on pairs; higher-order interactions (3+ features) require further development

**Failure cases:**
- On datasets with purely additive structure, localized CBFI may show high G4 due to estimation noise rather than true interactions
- In very high-dimensional settings, feature interaction graphs become unmanageable

### 5. Broader XAI Agenda

This work contributes to a larger shift in xAI from *post-hoc attribution* (explaining any model) to *structural interpretation* (understanding model mechanisms). It aligns with:
- Mechanistic interpretability (understanding internals, not just inputs)
- Causal inference (distinguishing spurious correlations from causal dependencies)
- Fairness and robustness (auditing models for hidden biases and failure modes)

## Code & Resources

### Official Implementation

- **Paper HTML version:** [arxiv.org/html/2610.34962](https://arxiv.org/html/2610.34962) (includes figures and interactive elements if available)
- **Paper PDF:** [arxiv.org/pdf/2610.34962](https://arxiv.org/pdf/2610.34962)

**Note:** Code repository not yet located in public search. Check the paper's appendix or contact the authors for implementation details.

### Dependencies and Requirements

Based on the methods described:
- **Language:** Likely Python
- **Key libraries:** scikit-learn, numpy, pandas (for data handling and conditional expectation estimation)
- **Model types:** Agnostic—works with any trained model (tree ensembles, neural networks, linear models)
- **Computational requirements:** Moderate for tabular data (<1M rows, <100 features); scales with dataset size and feature count

### Quick Start Guide

(Inferred from methodology; exact code not publicly available yet)

```python
# Pseudo-code for localized CBFI

import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def localized_cbfi(model, instance, X_train, y_train):
    """
    Compute localized CBFI for a single instance.
    
    Args:
        model: Trained predictor
        instance: Input instance x
        X_train: Training features
        y_train: Training targets (for reference distributions)
    
    Returns:
        G1 (main effects per feature), G4 (total interaction effect)
    """
    
    # Step 1: Compute baseline
    baseline = np.mean([model.predict(x.reshape(1, -1)) for x in X_train])
    
    # Step 2: Compute G1 for each feature
    d = len(instance)
    G1 = np.zeros(d)
    
    for i in range(d):
        x_avg = X_train.mean(axis=0)
        x_with_avg_i = instance.copy()
        x_with_avg_i[i] = x_avg[i]  # Set feature i to average
        
        prediction_marginal = model.predict(x_with_avg_i.reshape(1, -1))[0]
        prediction_avg = model.predict(x_avg.reshape(1, -1))[0]
        
        G1[i] = prediction_marginal - prediction_avg
    
    # Step 3: Compute G4 (interactions)
    prediction_actual = model.predict(instance.reshape(1, -1))[0]
    G1_total = G1.sum()
    G4 = prediction_actual - baseline - G1_total
    
    return G1, G4

# Identify feature interactions by examining high-G4 instances
# and correlating feature pairs in those regions
```

### Interactive Visualizations

The paper likely includes:
- **Feature interaction heatmaps:** Showing pairwise interaction strength
- **Prediction decomposition charts:** Stacked bars showing G1 contributions vs. G4 for selected instances
- **Instance-level scatter plots:** Highlighting feature combinations in high-G4 regions

(Check arXiv HTML version for interactive demos)

## Related Work & Context

### Foundational Methods in Attribution

**SHAP (SHapley Additive exPlanations):** Lundberg & Lee (2017)
- Uses coalition game theory to fairly allocate prediction credit to features
- Assumes additive feature contributions; cannot explicitly model interactions

**LIME (Local Interpretable Model-agnostic Explanations):** Ribeiro et al. (2016)
- Fits local linear approximations around instances
- Interpretable but inherently additive; misses nonlinear dependencies

**Integrated Gradients:** Sundararajan et al. (2017)
- Path-based attribution; works well for neural networks
- Also assumes additive combination

### Related Work on Feature Interactions

**Higher-Order Feature Attribution:** 
- Tsang et al. (2020) and others have explored Shapley-based methods for interactions, but these are computationally expensive and often limited to pairwise interactions

**Contextual Feature Importance:**
- Methods that compute feature importance conditioned on other features (e.g., contextual LIME), moving toward local interaction awareness

**Actionable Recourse via CBFI:**
- Oh's follow-up work, **"Actionable CBFI"** (arXiv 2608.27821, 2026), extends localized CBFI from descriptive (explaining the model) to prescriptive (suggesting how to change outcomes)
- Combines CBFI decomposition with structural causal models for algorithmic recourse

### Broader XAI Landscape

**Post-hoc vs. Structural Interpretability:**
- This work bridges post-hoc explanation (applying after training) with structural insights (revealing model internals)
- Aligns with mechanistic interpretability, which seeks to understand *how* models compute, not just *what* they decide

**Interaction-Aware ML:**
- Decision trees and rule-based models naturally express interactions
- Modern work explores how to design neural networks that explicitly model interactions (e.g., gated architectures, polynomial networks)

**Causality and Fairness:**
- Causal inference literature emphasizes heterogeneous treatment effects and conditional dependencies
- Fairness research increasingly focuses on intersectional effects (how demographic features interact with other attributes to produce disparate outcomes)
- Localized CBFI provides a tool for this causal + fairness integration

### Citation in Recent Work

Papers building on or citing localized CBFI (arXiv 2610.34962):
- "Actionable CBFI: Prescriptive Interventional Diagnosis and Interaction-Aware Escalation for Sparse Causal Algorithmic Recourse" (Oh, arXiv 2608.27821)
- Other interaction-focused attribution papers emerging in late 2026

## Conclusion

**Beyond Feature Attribution: Recovering Latent Interaction Structures in Machine Learning Models via Localized CBFI** makes a compelling case that explainable AI must go beyond additive feature scores. By decomposing predictions into main effects (G1) and pure interactions (G4), and aggregating into feature interaction graphs, the paper enables practitioners to:

1. **Detect hidden feature synergies** that drive model behavior
2. **Audit for spurious interactions** that might indicate data quality issues or Clever Hans effects
3. **Generate interaction-aware explanations** that inform domain experts, stakeholders, and regulators
4. **Enable algorithmic recourse** by revealing which feature combinations matter

The work is particularly valuable for high-stakes domains (healthcare, finance, criminal justice) where understanding not just *which* features matter, but *how they interact*, is essential for trustworthy, fair, and robust AI systems. While computational challenges remain for very high-dimensional data, localized CBFI represents an important step toward explainability that truly exposes model logic, not merely simplifies it.
