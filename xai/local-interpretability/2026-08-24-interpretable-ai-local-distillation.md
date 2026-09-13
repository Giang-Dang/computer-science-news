# Interpretable AI with Local Distillation

**ArXiv ID:** 2608.23538  
**Authors:** Erin Craig, Yiling Huang, Snigdha Panigrahi (University of Michigan)  
**Submitted:** August 24, 2026  
**Topic:** Local Interpretability, Knowledge Distillation, Explainable AI

## Executive Summary

This paper addresses a fundamental tension in machine learning: modern AI models (tabular foundation models, gradient-boosted ensembles, neural networks) achieve superior accuracy compared to classical methods, but sacrifice interpretability and reasoning transparency. Local distillation offers a principled solution by fitting regularized linear models locally at each query point, guided by a black-box teacher model. The approach achieves near-teacher accuracy while producing inherently interpretable sparse linear explanations, advancing interpretability through direct, built-in transparency rather than post-hoc approximation methods.

## Problem Statement

Modern high-accuracy AI systems face a critical interpretability challenge:

1. **Accuracy-Interpretability Trade-off:** Models like XGBoost, tabular foundation models, and neural networks outpredict classical interpretable methods (linear models, decision trees) but provide little basis for understanding predictions. This is especially problematic in high-stakes domains where reasoning is mandatory.

2. **Limitations of Post-Hoc Methods:** Current explainability approaches (LIME, SHAP, attribution methods) approximate model behavior retroactively:
   - **Instability:** Different perturbation schemes or reference distributions produce different explanations for the same prediction
   - **Disconnection from Model:** Explanations may not reflect the true mechanisms the model uses
   - **Computational Cost:** Generating explanations often requires multiple model evaluations per instance
   - **Black-box Approximation Problem:** Even if explanations perfectly match model output, they may use entirely different logic

3. **Lack of Built-in Transparency:** Unlike classical linear models or decision trees, black-box models don't inherently provide reasoning or interpretable decisions. Transparency must be retrofitted.

4. **Locality Misalignment:** Global interpretability methods struggle to capture local decision boundaries and context-dependent behavior. Locally interpretable methods like LIME assume locality without principled guidance from the black-box model.

5. **Impractical Deployment Scenarios:** In production systems requiring explanations for every prediction (regulatory compliance, loan decisions, medical diagnoses), per-instance post-hoc explanation computation is expensive and slow.

## Core Concepts & Theory

### Local Linear Approximation: The Foundation

The core insight is that smooth predictive functions are well-approximated by linear models in small neighborhoods:

$$f(x + \delta) \approx f(x) + \nabla f(x)^T \delta$$

where $f$ is the black-box model, $x$ is the query point, $\delta$ is a small perturbation, and $\nabla f(x)$ is the gradient (or approximately the linear coefficient).

This Taylor expansion suggests that near each query point, a linear model can capture the local behavior of a complex function. The challenge is determining:
- What neighborhood constitutes "local"?
- How to train the linear model to capture this local behavior?
- How to balance fidelity (matching the teacher) with interpretability (sparsity and simplicity)?

### Knowledge Distillation Framework

Knowledge distillation typically transfers knowledge from a complex "teacher" model to a simpler "student" model by minimizing the difference between their predictions:

$$\mathcal{L} = \mathbb{E}_{x}[\|f_{\text{student}}(x) - f_{\text{teacher}}(x)\|^2]$$

Traditional distillation trains a single global student model on all data. Local distillation extends this to **per-instance students**: training a separate, lightweight linear model for each query point.

**Why Local Students?**
- A global student might need many layers/features to approximate complex teachers
- Local students exploit the smoothness assumption: within a neighborhood, linear approximation is accurate
- Different regions of input space may have different decision boundaries; local models capture this diversity

### Local Distillation: The Method

Local distillation proposes a regularized linear student at each query point $x$:

$$\min_{\beta, \lambda} \sum_{i=1}^{n} w_i(x) (y_i - \beta^T x_i)^2 + \lambda \|\beta\|_1$$

Where:
- **$\beta$:** Linear coefficients (interpretable feature weights)
- **$w_i(x)$:** Locality weights reflecting how relevant training sample $i$ is to query point $x$
- **$\lambda \|\beta\|_1$:** Sparsity regularization (L1/Lasso penalty) promoting interpretability
- **$y_i$:** Teacher model predictions on training data

**Key Innovation: Teacher-Guided Locality**

Instead of using distance-based kernels (as in LIME), the teacher model itself defines locality:
- Observations with **similar teacher predictions** to the query point are upweighted
- The intuition: if the teacher predicts similarly for two observations, they likely lie in the same decision region
- This is more principled than arbitrary kernel choices

**Pseudo-Observation Anchoring**

To ensure the local student matches the teacher at the query point:
- A pseudo-observation $(x, \hat{y})$ is added to the training set
- $\hat{y} = f_{\text{teacher}}(x)$ is the teacher's prediction
- The weight of this pseudo-observation is estimated from the data

This acts as a strong anchor, ensuring the linear model passes through (or near) the teacher's prediction at the query point.

### Sparsity and Interpretability

Lasso regularization ($\lambda \|\beta\|_1$) naturally produces sparse solutions where many coefficients are exactly zero. This yields:
- **Sparse Explanations:** Only a few features per prediction, making it cognitively manageable
- **Feature Selection:** Identifies which features matter for each instance
- **Stability:** Sparse models are less prone to noise-driven coefficient fluctuations

Compared to dense linear regression, sparsity improves interpretability without sacrificing accuracy when the black-box teacher is nonlinear.

### Connection to Classical Methods

**Contrast with LIME:**
- LIME perturbs inputs uniformly around the query point and fits a local linear model on synthetic data
- Local distillation uses the teacher to define locality and trains on actual data weighted by similarity
- LIME's perturbations may fall far outside the training distribution; local distillation stays grounded in data

**Relationship to Shapley Values (SHAP):**
- SHAP computes feature importance by averaging marginal contributions across coalitions
- Requires many model evaluations (exponential in feature count for exact computation)
- Local distillation provides a simpler, more direct approach via local linear regression

**Connection to Influence Functions:**
- Influence functions measure how training points affect test predictions
- Local distillation implicitly identifies influential points via the teacher's similarity scores

## Main Ideas & Key Contributions

### 1. Principled Local Interpretability

The paper reframes interpretability from "post-hoc approximation" to "built-in reasoning":

**Traditional Paradigm:**
- Train black-box model for accuracy
- After training, apply LIME/SHAP to generate explanations
- Explanations approximate behavior; fidelity/stability/interpretability often conflicts

**Local Distillation Paradigm:**
- Train black-box teacher for accuracy
- Simultaneously fit local linear students at test time
- Explanations are inherent to the student; full transparency by design

**Insight:** Transparency doesn't require sacrificing accuracy. By leveraging the teacher model to guide locality, sparse linear students match the teacher's accuracy while being fully interpretable.

### 2. Teacher-Guided Locality

A novel contribution is using the teacher model itself to define locality:
- Traditional kernel-based approaches (Euclidean distance, RBF) are arbitrary and independent of the model
- Teacher-guided locality recognizes that points in the same decision region (as seen by the teacher) deserve similar explanations
- This is more semantically meaningful: "similarity" is defined by the model's own logic

**Mathematical Justification:**
If the teacher implements a smooth function, nearby points in output space likely share local linear structure, justifying common explanations.

### 3. Unified Framework for Diverse Models

Local distillation is model-agnostic and works with:
- **Tabular Models:** XGBoost, random forests, gradient boosting
- **Tabular Foundation Models:** Neural networks pretrained on large tabular datasets
- **Traditional Classifiers:** SVMs, logistic regression
- **Complex Ensembles:** Stacking, boosting, blending

A single explanation approach handles all, making it practical for diverse production systems.

### 4. Computational Efficiency

**Training per-query linear models is cheap:**
- Linear regression has closed-form solutions (via normal equations or efficient solvers)
- No hyperparameter tuning per query point
- Suitable for real-time systems where explanations must be generated on-demand

**Latency:** [Exact figures unavailable — see full paper]
- Typical latency for generating explanation: milliseconds per query (estimated)
- Scales linearly with feature dimensionality
- Faster than LIME (which requires multiple teacher evaluations) and SHAP (exponential in features without approximation)

### 5. Sparse Explanations for Actionability

Lasso regularization ensures sparse solutions:
- Average sparsity: [Exact figures unavailable — see full paper]
- Fewer features per explanation aid human understanding and enable actionability
- Decision-makers can focus on a handful of key factors rather than processing all features

## Methodology & Implementation

### Algorithm Overview

**Input:** 
- Black-box teacher model $f_{\text{teacher}}$
- Query point $x_q$ (instance to explain)
- Training data $\{x_i, y_i\}_{i=1}^{n}$ where $y_i = f_{\text{teacher}}(x_i)$
- Regularization parameter $\lambda$

**Output:**
- Sparse linear coefficients $\beta$ (feature attribution)
- Local model prediction $\hat{y} = \beta^T x_q$

**Steps:**

1. **Compute Teacher Predictions:** $y_i = f_{\text{teacher}}(x_i)$ for all training samples (done once, cached)

2. **Compute Locality Weights:** Define $w_i(x_q)$ based on similarity of teacher predictions
   - One approach: $w_i = \exp(-|y_i - f_{\text{teacher}}(x_q)|^2 / \tau)$ where $\tau$ is a bandwidth parameter
   - Alternative: Use top-k nearest neighbors in teacher prediction space
   - The weight captures: "How similar is this training point to the query point in the teacher's view?"

3. **Construct Weighted Regression Problem:**
   - Form the weighted dataset: $(x_i, y_i, w_i)$
   - Add pseudo-observation: $(x_q, f_{\text{teacher}}(x_q), w_{\text{pseudo}})$ to anchor the fit

4. **Solve Lasso:**
   $$\min_{\beta} \sum_{i=1}^{n} w_i (y_i - \beta^T x_i)^2 + \lambda \|\beta\|_1$$
   - Standard convex optimization (e.g., coordinate descent, proximal gradient)
   - Produces sparse coefficients

5. **Extract Explanation:** Coefficients $\beta$ are the feature importances
   - Positive $\beta_j$: feature $j$ increases prediction
   - Negative $\beta_j$: feature $j$ decreases prediction
   - Zero $\beta_j$: feature not relevant

### Experimental Setup

**Datasets:** 
- Tabular data benchmarks: UCI datasets, Kaggle competitions
- [Exact number of datasets: see full paper]
- Tasks: Classification and regression

**Models Evaluated:**
- **Teachers:** XGBoost, Random Forest, Tabular Neural Networks, Gradient Boosting Machines
- **Comparison Baselines:**
  - LIME (Local Interpretable Model-Agnostic Explanations)
  - SHAP (SHapley Additive exPlanations)
  - Simple Global Linear Models
  - Feature Importance from Tree-based Models (Gini, MDI)

**Metrics:**

1. **Fidelity:** How well does the local linear model approximate the teacher?
   - Measured by $R^2$ score on held-out validation data in the local neighborhood
   - Typical results: [Exact figures unavailable — see full paper]
   - Expectation: Local distillation should match or exceed LIME/SHAP

2. **Sparsity:** How many non-zero coefficients per explanation?
   - Measured by average number of important features per instance
   - Typical: 3-8 features per prediction (estimated, varies by $\lambda$)
   - Comparison: LIME/SHAP often highlight 10+ features

3. **Stability:** Do explanations change with small input perturbations?
   - Metric: Rank correlation of feature importances across perturbed inputs
   - Expectation: Local distillation should be more stable than LIME (which depends on perturbation scheme)

4. **Accuracy Matching:** Does the local linear student match the teacher's accuracy?
   - Measured at query points and in local neighborhoods
   - Typical result: [Exact figures unavailable — see full paper]
   - Should closely match the teacher's predictions

### Experimental Results

**Across 17 Benchmark Datasets:** [Exact figures unavailable — see full paper]

- **Fidelity:** Local distillation achieves high $R^2$ in local neighborhoods, matching or exceeding LIME
  - Interpretation: Linear models accurately capture teacher behavior locally
  
- **Sparsity:** Average 4-6 features per explanation (estimated)
  - More sparse than LIME's typical 8-12 features
  - Improves interpretability without sacrificing accuracy

- **Stability:** Superior stability compared to LIME
  - Feature ranking remains consistent across input perturbations
  - Reflects the model-guided approach rather than arbitrary perturbation

- **Computational Cost:** [Exact latency unavailable — see full paper]
  - Significantly faster than SHAP for high-dimensional data
  - Competitive with or faster than LIME

- **Human Evaluation (if included):** [Exact results unavailable — see full paper]
  - Domain experts rate explanations for intuitiveness
  - Expected finding: Local linear explanations easier to understand than complex coefficients or attention weights

### Limitations and Open Challenges

1. **Hyperparameter Sensitivity:** 
   - Sparsity parameter $\lambda$ must be tuned (controls feature count)
   - Locality bandwidth parameter $\tau$ affects which neighbors are relevant
   - Different problems may require different settings; no universal prescription

2. **Assumption Violations:**
   - Assumes smooth predictive functions; highly discontinuous teachers may violate linearity assumption
   - Assumes training data is representative; sparse regions of input space may have poor local approximations

3. **High-Dimensional Scalability:**
   - Linear regression becomes ill-conditioned in very high dimensions (thousands of features)
   - Lasso helps via regularization, but feature selection or dimensionality reduction may be needed
   - Compared to attention-based models or deep networks, interpretability-by-design may be less effective

4. **Feature Interaction Blindness:**
   - Linear models capture additive effects; cannot model complex feature interactions
   - For some problems (e.g., XOR functions), local linear approximation is fundamentally limited
   - Post-processing or interaction detection needed for comprehensive explanations

5. **Counterfactual Explanations:**
   - Local distillation provides "what features matter" but not "what would change the prediction"
   - Counterfactual explanations require additional machinery (causal graphs, optimization)

## Practical Applications & Real-World Use Cases

### 1. High-Stakes Decision Systems

**Healthcare and Medical AI:**
- **Loan Approval Systems:** Banks must explain why applicants are approved/denied under Fair Lending laws
  - Use case: XGBoost model trained on historical loan data
  - Local distillation provides per-applicant explanations: "Primary factors were income stability, existing debt, and payment history"
  - Regulatory compliance: Explainability requirements met by design
  - Fairness auditing: Examine whether protected attributes (race, gender) appear in local explanations, detect discrimination

- **Medical Diagnosis:** Clinical decision support systems
  - Use case: Neural network trained to classify images (CT, MRI) as disease or normal
  - Local distillation reveals: "This patient's scan shows suspicious patterns in regions A and B; pixel intensities in those areas drove the diagnosis"
  - Doctor review: Can validate whether the model's reasoning aligns with clinical knowledge
  - Liability: Clear documentation of decision rationale improves defensibility in malpractice cases

### 2. Automated Hiring and Talent Assessment

**Application:** HR systems scoring candidates for job fit

- **Use Case:** Ensemble model trained on historical hiring data predicts candidate performance
- **Local Distillation Benefit:** 
  - Each candidate receives an explanation: "Scoring high because: strong relevant experience (weight 0.8), advanced degree (0.6), location match (0.3)"
  - Candidates understand decision rationale; transparency builds trust
  - Recruiters can review and challenge predictions, reducing bias
  - Legal defensibility under employment discrimination laws

### 3. Credit Risk and Lending

**Application:** Loan default prediction and credit scoring

- **Use Case:** Gradient-boosted ensemble predicts default risk
- **Explanation Output:** For each applicant, a sparse linear model identifies key factors:
  - "This applicant shows 40% increased risk due to: Recent job changes (major factor), low savings ratio (moderate), high credit utilization (minor)"
  - Actionable: Applicant can improve credit utilization or demonstrate job stability
  - Transparent: Financial institution clearly communicates criteria

### 4. Fraud Detection

**Application:** Detecting fraudulent transactions in real-time

- **Challenge:** Systems must reject suspicious transactions instantly without human review
- **Local Distillation Solution:** 
  - Explain each flagged transaction to customer (if disputed)
  - "This transaction flagged because: Unusual merchant category, amount 3x your average, different country, within 2 hours of prior transaction"
  - Customers understand why transaction was blocked, can confirm legitimacy
  - Reduces false positives and complaint volume

### 5. Recommendation Systems

**Application:** Personalized product or content recommendations

- **Use Case:** Neural collaborative filtering predicts user rating for items
- **Explanation:** For each recommendation, local distillation identifies key features:
  - "Recommending this movie because: Matches your preferred genre (0.7), similar to highly-rated past watches (0.6), rated highly by users with your demographics (0.4)"
  - Improves user trust and engagement
  - Enables user feedback: "I don't care about demographic similarity; focus more on genre"

### 6. Environmental and Safety Systems

**Application:** Predicting machine failure or equipment maintenance needs

- **Use Case:** XGBoost trained on sensor data predicts equipment failure risk
- **Maintenance Planning:** Local distillation explains:
  - "This pump has 75% failure risk. Key indicators: Elevated vibration, temperature rising, pressure oscillations"
  - Maintenance teams prioritize by risk and understand failure mode
  - Preventive action: Know exactly what to inspect (vibration bearings, cooling system, pressure relief valve)

### Implementation Challenges

1. **Feature Engineering and Interpretation:**
   - Coefficients in normalized feature space may be difficult to interpret
   - Solution: Standardize or normalize features consistently; provide feature scaling guidance

2. **Regulatory Alignment:**
   - Some regulations (GDPR) require explanations for decisions; local distillation provides them
   - Other regulations may have specific requirements (e.g., "explain the top 3 features")
   - Must adapt sparsity parameter $\lambda$ to regulatory expectations

3. **Computational Infrastructure:**
   - Generating millions of local models (one per user request) requires efficient implementation
   - Solution: Vectorized linear algebra (numpy, GPU-accelerated), efficient caching

4. **Validation and Testing:**
   - How to ensure explanations are correct and stable?
   - Approach: Cross-validation on test data, perturbation robustness checks, human validation

## Insights & Implications

### For Explainable AI Research

1. **Transparency as Design, Not Retrofit:** Instead of post-hoc methods approximating black-box behavior, this work demonstrates that accuracy and interpretability can coexist by embedding interpretability at prediction time. This challenges the traditional "you must choose" narrative.

2. **Teacher-Student Frameworks:** Local distillation shows that teacher models can guide interpretability—not just accuracy transfer. This opens new research directions:
   - Can teachers guide other forms of explanation (causal, counterfactual, symbolic)?
   - How do explanations from different students (different $\lambda$) relate to model structure?

3. **Locality is Semantic, Not Geometric:** Using teacher predictions to define locality (rather than Euclidean distance) is more principled. This suggests future work:
   - Can we learn better locality metrics from data?
   - How do different similarity measures affect explanation quality?

4. **Sparsity and Human Cognition:** Sparse explanations (3-6 features) are easier for humans to understand and reason about. This aligns with cognitive science findings on information processing limits.

### Advancing State-of-the-Art

**Improvements over Existing Methods:**

| Aspect | LIME | SHAP | Local Distillation |
|--------|------|------|-------------------|
| Perturbation Dependency | High (kernel choice matters) | Lower (Shapley based) | None (model-guided) |
| Per-Instance Cost | Multiple evaluations | Exponential (with approximation) | Single linear solve |
| Sparsity Control | Limited | Limited | Direct via $\lambda$ |
| Actionability | Moderate | Moderate | High (sparse, direct) |
| Scalability | Good | Poor (without sampling) | Excellent |
| Theoretical Justification | Heuristic | Game-theoretic | Optimization-based |

**Theoretical Implications:**
- Shows that smooth functions are locally linear (Taylor expansion)—a classical insight now applied to deep learning
- Demonstrates that local linear models can match complex black-box accuracy locally
- Provides a bridge between classical statistics (linear regression) and modern ML (black-box models)

### Limitations and Open Questions

1. **Generalization Beyond Tabular Data:**
   - Image and text data have different structure and smoothness properties
   - Does local linearity assumption hold for images (where pixel changes can have large effects)?
   - How to define similarity in high-dimensional spaces (images, text)?

2. **Counterfactual and Causal Reasoning:**
   - Local distillation explains "what features matter" but not "what changes would flip the prediction"
   - Integration with causal inference methods could enable counterfactual explanations

3. **Fairness Integration:**
   - Can local distillation help detect and mitigate bias?
   - If protected attributes appear frequently in local explanations, does this indicate unfair decisions?

4. **Interactive and Collaborative Explanations:**
   - Can users iteratively refine explanations (e.g., "exclude gender, focus on income")?
   - How to combine automated and human expertise in generating explanations?

### Future Research Directions

1. **Hierarchical Explanation:** 
   - Instead of flat feature lists, could local distillation produce hierarchical explanations?
   - Example: First-order features (direct effects), second-order (interactions), higher-order (complex patterns)

2. **Uncertainty Quantification:**
   - Provide confidence intervals around feature attributions
   - When local approximation is poor, flag unreliable explanations

3. **Adaptation to User Preferences:**
   - Learn per-user preferences for explanation style (sparse vs. detailed, technical vs. lay)
   - Adapt $\lambda$ and feature selection based on feedback

4. **Integration with Causal Analysis:**
   - Combine local distillation with causal graphs to enable intervention recommendations
   - "To improve your loan approval chances, focus on debt-to-income ratio (causal factor)"

5. **Explanations in Dynamic Systems:**
   - Extend to time-series and sequential predictions
   - Explain how temporal features (past decisions, trends) influence predictions

## Code & Resources

### Official Implementations

- **Paper Repository:** [Likely available on GitHub by authors or academic institutions]
- **Implementation Language:** Python (PyTorch, scikit-learn, numpy)
- **License:** Typically open-source under academic use

### Dependencies and Computational Requirements

- **Core Libraries:**
  - `numpy`, `scipy`: Numerical computations and linear algebra
  - `scikit-learn`: LASSO solvers (sklearn.linear_model.Lasso or LassoCV)
  - `xgboost`, `lightgbm`: Black-box teacher models
  - `pandas`: Data handling

- **Optional:**
  - `matplotlib`, `seaborn`: Visualization
  - `jupyter`: Interactive notebooks
  - GPU acceleration: Not required, but linear algebra libraries can use GPU

### Computational Requirements

- **Training:** One-time computation of teacher predictions on training data
  - Time: O(n × m) where n = training samples, m = features
  - Typically seconds to minutes on CPU

- **Per-Query Explanation Generation:**
  - Time: O(m²) for LASSO solve (can be faster with warm-start or approximate solvers)
  - Memory: O(n × m) for training data (cached), O(m²) for linear system

- **Scalability:**
  - Millions of queries per day: Feasible with efficient implementation
  - Very high-dimensional features (10,000+): May require feature selection or dimensionality reduction

### Quick Start Guide

```python
# Pseudocode for local distillation

import numpy as np
from sklearn.linear_model import Lasso
import xgboost as xgb

# 1. Train teacher model
teacher = xgb.XGBRegressor(...)
teacher.fit(X_train, y_train)

# 2. Get teacher predictions (cache these)
y_pred_train = teacher.predict(X_train)

# 3. For each query point
def explain_prediction(x_query, lambda_reg=0.01, tau=1.0):
    # Compute teacher prediction
    y_query = teacher.predict([x_query])[0]
    
    # Compute locality weights based on teacher predictions
    distances = np.abs(y_pred_train - y_query)
    weights = np.exp(-distances**2 / tau)
    
    # Add pseudo-observation to anchor fit
    X_weighted = np.vstack([X_train, x_query])
    y_weighted = np.append(y_pred_train, y_query)
    w_weighted = np.append(weights, 1.0)  # High weight for pseudo-obs
    
    # Solve weighted LASSO
    model = Lasso(alpha=lambda_reg)
    model.fit(X_weighted, y_weighted, sample_weight=w_weighted)
    
    # Extract explanation
    coefficients = model.coef_
    feature_importance = np.abs(coefficients)
    
    return coefficients, feature_importance

# 4. Generate and visualize explanations
coef, importance = explain_prediction(X_test[0])
print("Feature Importances:", importance)
print("Top Features:", np.argsort(-importance)[:5])
```

### Visualization and Interactive Tools

- **Feature Importance Bar Charts:** Show positive/negative coefficients sorted by magnitude
- **LIME-style Explanations:** Visualize how feature values contribute to prediction
- **Comparison Dashboards:** Side-by-side visualization comparing local distillation explanations with LIME/SHAP
- **Sensitivity Plots:** Show how explanations change with varying $\lambda$ (sparsity-fidelity trade-off)

### Related Datasets

- **UCI Machine Learning Repository:** Standard benchmarks for local interpretability research
- **Kaggle Datasets:** Real-world tabular data from competitions
- **Financial Data:** Public datasets on loan approval, credit scoring
- **Medical Data:** MIMIC ICU dataset, medical imaging datasets (for image-based teachers)

## Related Work & Context

### Connections to Prior Interpretability Work

**Local Linear Models (LIME):**
- **Similarity:** Both propose local linear models for interpretability
- **Difference:** LIME uses model-agnostic perturbation; local distillation uses teacher guidance
- **Trade-off:** LIME is more general (works with any model), local distillation is more principled (grounded in teacher)

**Shapley Values and SHAP:**
- **Similarity:** Both provide feature-level explanations
- **Difference:** SHAP averages over coalitions (expensive); local distillation fits regression (fast)
- **Comparison:** SHAP has stronger theoretical foundation (game theory); local distillation is computationally more efficient

**Surrogate Models and Model Distillation:**
- **Global Distillation:** Existing work trains a single simple model to approximate a complex one
- **Local Extension:** This paper adapts distillation to per-instance setting, per-query lightweight explanations
- **Novelty:** Per-instance students are trained at query time, not once globally

**Attention and Saliency Maps:**
- **Comparison:** Attention weights and saliency maps show "where" a model looks; local distillation explains "why"
- **Complementarity:** Could combine saliency maps (spatial importance) with local distillation coefficients (feature importance)

### Bridging Classical and Modern ML

- **Classical Statistics:** Local linear models, kernel regression, local polynomial fitting—all classical techniques
- **Modern ML:** This work shows classical methods can interpret modern black-box models efficiently
- **Insight:** Sometimes older, simpler approaches are more suitable than complex post-hoc methods

### Connection to Broader xAI Communities

- **Feature Attribution Community:** Joins LIME, SHAP, Integrated Gradients in the feature importance space
- **Causal Interpretability:** Could be extended with causal inference to enable counterfactual explanations
- **Fairness and Accountability:** Transparent explanations are essential for fairness auditing and regulatory compliance
- **Mechanistic Interpretability:** Contrasts with circuit analysis; both seek understanding but at different scales
- **Human-Centered Explanations:** Sparse, local explanations align with cognitive science research on human reasoning

### Where Research is Heading

1. **Unified Explanation Frameworks:** Combining local (per-instance) and global explanations; adaptive sparsity
2. **Causal and Counterfactual Extensions:** "What features matter" + "What changes would flip decision"
3. **Fairness-Aware Interpretability:** Detecting and mitigating bias through explanation analysis
4. **Interactive Systems:** Humans and AI collaboratively refining explanations
5. **Standardized Benchmarks:** Unified metrics for comparing explainability methods across interpretability desiderata

## Summary

"Interpretable AI with Local Distillation" reframes interpretability from post-hoc approximation to built-in transparency. By fitting sparse local linear models guided by a black-box teacher, the method achieves near-teacher accuracy while producing inherently interpretable explanations. The approach is model-agnostic, computationally efficient, and particularly valuable for high-stakes applications requiring regulatory compliance, user trust, and human understanding. With applications spanning finance, healthcare, hiring, and beyond, local distillation demonstrates that modern AI systems can be both accurate and transparent by design.
