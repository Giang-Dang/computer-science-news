# A Comparative Analysis of Interpretable Machine Learning Methods

**Paper**: A Comparative Analysis of Interpretable Machine Learning Methods  
**Authors**: Mattia Billa, Giovanni Orlandi, Veronica Guidetti, Federica Mandreoli  
**Institution**: Department of Physics, Informatics and Mathematics, University of Modena and Reggio Emilia, Italy  
**ArXiv ID**: [2601.00428](https://arxiv.org/abs/2601.00428)  
**Submitted**: January 1, 2026  
**xAI Subfield**: Inherently Interpretable Models  

---

## Executive Summary

This paper presents one of the most comprehensive large-scale benchmark studies of inherently interpretable machine learning methods to date, evaluating 16 distinct approaches across 216 real-world tabular datasets. Rather than asking "are interpretable models good enough?", the study asks the more nuanced question of *which* interpretable model is best suited to *which* data context — revealing that the right choice is highly context-dependent. The findings provide concrete, empirically grounded guidance for practitioners in regulated industries (healthcare, finance, law) who must balance predictive performance with transparency requirements under frameworks like GDPR and the EU AI Act.

---

## Problem Statement

### The Core Interpretability Challenge

Machine learning models deployed in high-stakes domains — credit scoring, clinical diagnosis, criminal justice, and drug discovery — face a fundamental tension: the most accurate models (deep neural networks, gradient-boosted trees) are also the hardest to explain. This has led to two dominant paradigms:

1. **Post-hoc explainability**: Train any black-box model, then apply explanation methods (SHAP, LIME, Grad-CAM) after the fact.
2. **Inherently interpretable models**: Use models whose predictions are transparent by design — the model itself *is* the explanation.

The paper focuses entirely on the second paradigm. Despite the importance of inherently interpretable models, the field lacked rigorous empirical evidence to guide model selection. Prior benchmarks suffered from three key limitations:

- **Narrow scope**: Studies typically evaluated 3–5 methods on a handful of curated datasets.
- **Aggregate rankings**: Results averaged across datasets masked critical context-dependence.
- **Missing robustness analysis**: Few studies assessed how interpretable models behave under distributional shift — a critical concern for real-world deployment.

### Prior Work Gaps

Previous evaluations (e.g., Caruana et al. 2015 on GAMs, Rudin et al. 2019 on scoring systems) established that interpretable models can match black-box performance on specific task types. However, no unified study had:
- Evaluated modern interpretable architectures (IGANNs, GOSDT, neural symbolic regression) alongside classical methods
- Stratified results by dataset structural characteristics (dimensionality, sample size, linearity)
- Assessed computational cost trade-offs systematically across the interpretability spectrum

---

## Core Concepts & Theory

### What Makes a Model "Interpretable by Design"?

Inherent interpretability means the model's decision process is directly human-readable without auxiliary explanation tools. This manifests in three structural properties:

**Simulatability**: A human can mentally simulate the model's prediction for a given input in reasonable time. A linear model with 5 features is simulatable; a decision tree with 1,000 leaves is not.

**Decomposability**: Each part of the model (feature weight, node, rule) admits an intuitive standalone explanation. Additive models achieve this by decomposing predictions into per-feature contributions.

**Algorithmic transparency**: The training algorithm is fully understood, with no opaque optimization processes that produce unpredictable behavior.

### The Interpretability Spectrum

The 16 methods evaluated span a conceptual spectrum:

```
← More Interpretable                          Less Interpretable →

Linear     Decision    Rule-based    GAMs      Symbolic    Neural
Models     Trees       Systems                 Regression  Additive
                                                           Models
(LR, Lasso) (CART)   (RIPPER, BRL) (EBM, NAM)  (PySR)   (IGANN)
```

### Key Method Families

#### 1. Linear Models

The simplest interpretable family. For a prediction $\hat{y}$, a linear model computes:

$$\hat{y} = \beta_0 + \sum_{j=1}^{p} \beta_j x_j$$

Each coefficient $\beta_j$ directly quantifies the marginal effect of feature $x_j$. Variations include:

- **Ridge Regression**: Adds L2 penalty $\lambda \sum \beta_j^2$ to reduce overfitting while keeping all features.
- **Lasso Regression**: Adds L1 penalty $\lambda \sum |\beta_j|$ to perform automatic feature selection (many $\beta_j \to 0$).
- **Logistic Regression**: Extends to binary classification via $P(y=1) = \sigma(\beta_0 + \sum \beta_j x_j)$.
- **Polynomial Regression**: Adds interaction and polynomial terms $x_j^k$, increasing expressiveness at the cost of interpretability.

**Interpretability mechanism**: Coefficients are the explanation. A positive $\beta_j$ means feature $j$ increases the predicted output; magnitude indicates importance.

**Key limitation**: Assumes a linear relationship between features and output. Fails in the presence of strong non-linearities or feature interactions.

#### 2. Decision Trees (CART)

Trees recursively partition the feature space into axis-aligned rectangular regions. A prediction traverses from root to leaf, applying if-then rules at each internal node:

```
if age < 35:
    if income > 50000: → predict "approved"
    else:              → predict "denied"
else:
    if credit_score > 700: → predict "approved"
    else:                  → predict "denied"
```

The Gini impurity for a node $t$ containing class proportions $p_k$ is:

$$\text{Gini}(t) = 1 - \sum_{k} p_k^2$$

Splits are chosen to minimize weighted Gini impurity across child nodes.

**Interpretability mechanism**: The entire decision can be traced as a path from root to leaf. Shallow trees (depth ≤ 5) are genuinely human-readable.

**Key limitation**: Instability (small data changes produce very different trees) and high variance. Deep trees required for complex data lose interpretability.

#### 3. Generalized Optimal Sparse Decision Trees (GOSDT)

GOSDT addresses classical CART's greedy split selection by using mathematical optimization to find the globally optimal sparse tree. It formulates tree construction as an integer programming problem:

$$\min_{\text{tree}} \left[ \text{Training loss} + \lambda \cdot |\text{leaves}| \right]$$

where $\lambda$ controls the sparsity penalty. This guarantees the found tree minimizes regularized loss over *all possible trees* of the given depth, not just greedily constructed ones.

**Key advantage over CART**: GOSDT finds provably optimal sparse trees, producing models that are simultaneously more accurate and more compact than CART at equivalent depth.

**Key limitation**: Exponential worst-case search space. The paper finds GOSDT exhibits pronounced sensitivity to class imbalance, degrading significantly when minority classes are underrepresented.

#### 4. Explainable Boosting Machine (EBM)

EBM is a modern GAM (Generalized Additive Model) from Microsoft's InterpretML library. It models predictions as a sum of per-feature shape functions plus pairwise interactions:

$$g(\hat{y}) = \beta_0 + \sum_{j} f_j(x_j) + \sum_{i \neq j} f_{ij}(x_i, x_j)$$

Each $f_j$ is a smoothed step function learned via cyclic gradient boosting — one feature at a time — which eliminates the multicollinearity confounding that plagues linear models.

**Why EBMs dominate on regression**: The shape functions $f_j$ can capture arbitrary non-linearities (U-shaped relationships, thresholds, saturation effects) while remaining fully decomposable. The pairwise interaction terms $f_{ij}$ capture the most important two-way interactions without compromising global interpretability.

**Interpretability mechanism**: Each $f_j(x_j)$ can be plotted as a univariate function, showing exactly how the model's prediction changes as a single feature varies. This produces intuitive visualization tools.

#### 5. Interpretable Generalized Additive Neural Networks (IGANN)

IGANN combines the additive structure of GAMs with the representational power of neural networks:

$$\hat{y} = \text{sigmoid}\left(\beta_0 + \sum_{j=1}^{p} f_j(x_j)\right)$$

where each $f_j$ is a small single-hidden-layer neural network trained to learn the shape function for feature $j$. Unlike EBMs, IGANN uses exact neural representations rather than step functions, allowing smoother and potentially more expressive shape functions.

**Key finding in the paper**: IGANNs perform particularly well in strongly non-linear regimes, where EBM's step-function approximations introduce discretization error. However, IGANN requires longer training times.

#### 6. Symbolic Regression (SR)

Symbolic Regression searches the space of mathematical expressions to find a formula that fits the data. Unlike other methods, SR does not commit to a fixed model architecture — it discovers the functional form itself.

Given data $\{(x_i, y_i)\}$, SR finds expression $f$ minimizing:

$$\min_{f \in \mathcal{F}} \left[ \text{MSE}(f(X), y) + \text{complexity}(f) \right]$$

where $\mathcal{F}$ is the space of all symbolic expressions using operators $\{+, -, \times, \div, \sin, \exp, \log, \ldots\}$.

Modern SR tools use evolutionary algorithms (genetic programming), Bayesian optimization, or neural-guided search (e.g., PySR, DSR). The result is human-readable equations like:

$$\hat{y} = 2.3 \cdot x_1^2 + \log(x_2) - 0.7 \cdot x_1 x_3$$

**Key finding**: SR excels in non-linear regimes and produces the most compact, mathematically precise explanations. However, it is computationally expensive and can struggle with high-dimensional datasets.

#### 7. Rule-Based Systems

Methods like **RuleFit** combine decision rules (if-then conditions derived from trees) with a sparse linear model:

$$\hat{y} = \beta_0 + \sum_{k} \beta_k r_k(x) + \sum_{j} \gamma_j x_j$$

where $r_k(x) \in \{0,1\}$ are binary indicators for whether rule $k$ is satisfied. Lasso selection ensures only the most important rules and features appear in the final model.

**Bayesian Rule Lists (BRL)** take a different approach, learning an ordered list of if-then-else rules using a probabilistic generative model, optimized for human readability with pre-mined frequent pattern antecedents.

**FasterRisk** focuses on building optimal sparse logistic scoring systems — integer-valued weighted sums with a lookup table format used by physicians and judges in the real world.

---

## Main Ideas & Key Contributions

### Contribution 1: The Largest Systematic Benchmark in Inherently Interpretable ML

The study is unprecedented in scope:
- **16 methods** covering the full spectrum of inherently interpretable approaches
- **216 real-world tabular datasets** from UCI, OpenML, and domain-specific repositories covering classification (binary and multiclass) and regression tasks
- **Stratified analysis** by dataset characteristics: dimensionality (features), sample size (rows), degree of non-linearity, and class imbalance ratio

### Contribution 2: Context-Dependent Performance Profiles

The central finding is that no single method dominates across all conditions. The study maps out performance "niches" for each method:

| Method | Best Context | Weakness |
|--------|-------------|---------|
| EBM | Regression, moderate non-linearity, large data | Slower than linear models |
| Linear/Lasso | Linear data, very high dimensions | Fails under non-linearity |
| IGANN | Strongly non-linear, medium data | Longest training time |
| SR | Non-linear, low-to-medium dimensions | Scales poorly to high-d |
| GOSDT | Balanced classification | Severe class imbalance |
| Decision Tree | Small data, need for verbatim rules | High variance, depth-accuracy trade-off |

### Contribution 3: Interpretability-Speed Trade-offs Quantified

A key practical finding: the paper quantifies the training time cost of each method, revealing that:
- EBMs and Decision Trees offer the best **accuracy-per-second** trade-off
- IGANN and GOSDT require substantially more computation for their accuracy gains
- SR has highly variable training time (seconds to hours) depending on dataset complexity and search configuration

### Contribution 4: Robustness Under Distribution Shift

The paper evaluates all methods under controlled covariate shift, systematically moving test data distribution away from training distribution. This is critical for real-world deployment where data drift is inevitable. The findings reveal:
- Linear models, despite lower average accuracy, show the most **stable** performance under shift
- Tree-based methods (CART, GOSDT) degrade faster than additive models when shift is large
- EBMs maintain competitive performance across mild to moderate distributional changes

---

## Methodology & Implementation

### Experimental Setup

**Dataset collection**: 216 tabular datasets were sourced from public repositories (UCI Machine Learning Repository, OpenML). Datasets were stratified along four structural dimensions:
- **Dimensionality**: Low (< 10 features), medium (10–50), high (> 50)
- **Sample size**: Small (< 1,000), medium (1,000–10,000), large (> 10,000)
- **Linearity**: Measured using a linear separability score
- **Class imbalance**: Imbalance ratio (minority class fraction)

**Implementation**: Each method was implemented using its standard open-source library (scikit-learn, InterpretML, PySR, IGANN, gosdt-sklearn, etc.) with hyperparameter tuning via nested cross-validation (inner 5-fold for hyperparameter search, outer 5-fold for evaluation).

**Robustness testing**: Distributional shift was simulated by applying covariate shift perturbations (Gaussian noise injection, subset selection mimicking domain shift) to the test sets.

### Evaluation Metrics

For **classification**:
- **AUC-ROC**: Primary metric for imbalanced datasets
- **Balanced Accuracy**: Corrects for class imbalance in aggregate rankings
- **F1 Score**: Harmonic mean of precision and recall

For **regression**:
- **RMSE**: Root Mean Squared Error (scale-dependent)
- **R²**: Coefficient of determination (scale-independent comparison)
- **MAE**: Mean Absolute Error (robust to outliers)

For **efficiency**:
- **Training time (seconds)**: Wall-clock time on standardized hardware
- **Model size (parameters/rules/leaves)**: Proxy for human-cognitive complexity

For **robustness**:
- **Performance drop**: Δ(metric) between clean test and shifted test
- **Rank stability**: Spearman correlation of feature importances under noise

### Key Results

**On regression tasks**: EBMs achieved the highest median R² across all dataset sizes and non-linearity levels. IGANNs matched EBMs on highly non-linear datasets but required 3–8× longer training.

**On classification tasks**: No single method dominated. GOSDT achieved competitive accuracy on balanced datasets but showed up to 15% AUC drop on heavily imbalanced datasets (imbalance ratio > 1:10).

**On linear datasets**: Lasso regression matched EBM performance in linear regimes while training 50–100× faster.

**On non-linear datasets**: SR discovered compact formulas with lower test error than any additive model on ~20% of non-linear datasets, but required up to 10 minutes per dataset for discovery.

**On distributional robustness**: Linear models showed the smallest performance degradation under all shift conditions tested (average Δ AUC = 0.03). Tree-based methods showed the highest degradation (Δ AUC = 0.08–0.12).

### Limitations

1. **No post-hoc comparisons**: The study explicitly excludes black-box + post-hoc explanation combinations. This limits conclusions about the overall interpretability landscape.
2. **Tabular data only**: All 216 datasets are tabular. Results may not generalize to image, text, or time-series domains.
3. **Synthetic distributional shifts**: The robustness evaluation uses controlled synthetic shift rather than real observed distribution drift, which may not capture all real-world degradation patterns.
4. **Computational budget**: SR methods were constrained to 5-minute search budgets; longer searches may change SR's relative ranking.
5. **Hyperparameter sensitivity**: Results are subject to the chosen hyperparameter search spaces, which may not be optimal for all methods on all datasets.

---

## Practical Applications & Real-World Use Cases

### Healthcare: Clinical Decision Support

Physicians and regulators require models whose reasoning can be audited, challenged, and documented. Inherently interpretable models are ideal for:

- **Mortality risk scoring**: Logistic regression and FasterRisk scoring systems are used in ICUs (e.g., the APACHE score). The paper's findings support EBMs as a superior alternative to logistic regression while maintaining the additive, per-factor interpretability clinicians need.
- **Diagnostic assistance**: Decision trees provide explicit if-then rules for differential diagnosis. GOSDT's optimality guarantee ensures the shortest possible rule set.
- **Drug efficacy prediction**: Symbolic regression can discover physically meaningful relationships between molecular descriptors and drug activity.

**Regulatory implication**: The FDA's AI/ML action plan for software as a medical device (SaMD) requires documentation of model logic. Inherently interpretable models satisfy this requirement directly, while black-box models require additional explanation tooling.

### Finance: Credit Scoring and Risk Assessment

Financial regulations (Equal Credit Opportunity Act, Fair Housing Act, EU GDPR) require that adverse decisions be explainable to affected individuals. The paper's benchmarks suggest:

- **Scorecard models** (FasterRisk, Logistic Regression): For consumer credit decisions requiring a point-based score that can be communicated verbally.
- **EBMs**: For internal risk modeling where analysts need to understand non-linear effects (e.g., the saturation of income's protective effect beyond a threshold).
- **RuleFit**: For fraud detection, where business analysts can review and validate the discovered rules.

### Legal: Recidivism and Bail Decision Support

One of the most controversial applications of ML, recidivism prediction requires fairness guarantees alongside interpretability. The paper shows:

- **GOSDT** produces the most compact optimal decision rules for binary classification, enabling direct human review of the decision logic.
- **BRL (Bayesian Rule Lists)** provide probabilistic rule-based explanations that can be formally verified for fairness constraints.

### Regulatory Compliance

| Regulation | Requirement | Recommended Methods |
|-----------|-------------|-------------------|
| GDPR Article 22 | Right to explanation for automated decisions | Linear models, Decision Trees, Rule systems |
| EU AI Act (High-Risk) | Transparency, human oversight, auditability | EBMs, GOSDT, Symbolic Regression |
| FDA SaMD Guidance | Algorithm documentation and validation | EBMs, Logistic Regression, Decision Trees |
| ECOA (US Financial) | Adverse action notices | Scorecard models (FasterRisk), Logistic Regression |

**Implementation challenges**: Even inherently interpretable models require careful setup. GOSDT's sensitivity to class imbalance means practitioners must apply appropriate resampling (SMOTE, class weights) before deployment. SR's computational cost makes real-time training infeasible; models must be discovered offline.

---

## Insights & Implications

### Implication 1: The Death of the "Interpretability-Accuracy Trade-off" Myth

The paper provides strong evidence that in the tabular data domain, the widely cited accuracy-interpretability trade-off is overstated. EBMs, in particular, achieve predictive performance competitive with XGBoost and Random Forests on regression tasks *while* being fully interpretable. This aligns with Rudin's (2019) "Stop Explaining Black Box Machine Learning Models" argument.

### Implication 2: Context as the Primary Selection Criterion

The paper's most important implication is methodological: model selection for interpretable ML should be driven by dataset characteristics, not general benchmarks. Practitioners should:
1. Characterize their dataset (linear/non-linear, balanced/imbalanced, sample size)
2. Use the paper's stratified results as a selection guide
3. Only then run hyperparameter optimization

### Implication 3: The Computational Cost of Optimality

GOSDT and IGANN demonstrate that provably optimal or maximally expressive interpretable models come at substantial computational cost. For high-frequency decision systems (real-time fraud detection, algorithmic trading), EBMs or logistic regression remain the practical choice. For one-time policy model development (risk scoring policy, clinical guideline), the extra computation is justified.

### Implication 4: Distributional Robustness Favors Simplicity

The surprising finding that linear models maintain the smallest performance drop under distributional shift has deep implications for AI safety and reliability. In production environments where data drift is inevitable:
- **Simpler models degrade more gracefully** — their performance drop is predictable and proportional
- **Complex interpretable models** (IGANN, GOSDT) that achieve higher peak accuracy are more brittle under shift
- **Monitoring strategy**: Deploy the simplest interpretable model that meets accuracy requirements, not the most accurate one

### Open Questions

1. **Multimodal data**: How do these results extend to settings combining tabular features with text or image data?
2. **Active learning**: Do these performance hierarchies hold when training data is acquired incrementally?
3. **Group fairness**: Which methods best preserve fairness metrics (equalized odds, demographic parity) alongside accuracy?
4. **Longitudinal stability**: How stable are the discovered interpretations (shape functions, symbolic formulas) when models are retrained on updated data?

---

## Code & Resources

### Primary Paper
- **ArXiv**: https://arxiv.org/abs/2601.00428
- **PDF**: https://arxiv.org/pdf/2601.00428

### Key Libraries for Evaluated Methods

| Method | Library | Installation |
|--------|---------|-------------|
| EBM | InterpretML | `pip install interpret` |
| IGANN | igann | `pip install igann` |
| GOSDT | gosdt-sklearn | `pip install gosdt-sklearn` |
| Symbolic Regression | PySR | `pip install pysr` |
| RuleFit | imodels | `pip install imodels` |
| BRL | imodels | `pip install imodels` |
| FasterRisk | imodels | `pip install imodels` |
| Decision Trees | scikit-learn | `pip install scikit-learn` |
| Linear Models | scikit-learn | `pip install scikit-learn` |

### Quick Start: Comparing EBM vs Logistic Regression

```python
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_breast_cancer
import numpy as np

X, y = load_breast_cancer(return_X_y=True)

# Train EBM
ebm = ExplainableBoostingClassifier(random_state=42)
ebm_score = cross_val_score(ebm, X, y, cv=5, scoring='roc_auc').mean()

# Train Logistic Regression
lr = LogisticRegression(max_iter=1000, random_state=42)
lr_score = cross_val_score(lr, X, y, cv=5, scoring='roc_auc').mean()

print(f"EBM AUC:  {ebm_score:.4f}")
print(f"LR  AUC:  {lr_score:.4f}")

# Inspect EBM shape functions
ebm.fit(X, y)
from interpret import show
ebm_global = ebm.explain_global()
show(ebm_global)  # Interactive visualization
```

### Quick Start: Symbolic Regression with PySR

```python
from pysr import PySRRegressor
from sklearn.datasets import load_diabetes

X, y = load_diabetes(return_X_y=True)

model = PySRRegressor(
    niterations=100,
    binary_operators=["+", "*", "-", "/"],
    unary_operators=["sin", "exp", "log", "sqrt"],
    complexity_of_operators={"sin": 3, "exp": 2, "log": 2},
    parsimony=0.001,
    maxsize=15,
)
model.fit(X, y)
print(model)  # Prints the discovered symbolic formula
```

### Computational Requirements

| Method | Small Data (<1K) | Medium Data (10K) | Large Data (>100K) |
|--------|-----------------|-------------------|-------------------|
| Linear/Lasso | < 1 sec | < 5 sec | < 30 sec |
| Decision Tree | < 1 sec | < 5 sec | < 1 min |
| EBM | < 10 sec | 1–3 min | 5–20 min |
| IGANN | 30 sec | 5–15 min | 30–120 min |
| GOSDT | 1–60 sec | 5–30 min | May timeout |
| Symbolic Regression | 1–5 min | 5–15 min | 15–60+ min |

---

## Related Work & Context

### Connection to Post-Hoc XAI

This paper deliberately avoids post-hoc methods (SHAP, LIME, Grad-CAM), positioning itself in contrast to a large body of literature that explains black-box models. The implicit argument echoes Rudin (2019, *Nature Machine Intelligence*): if an interpretable model achieves comparable accuracy, there is no need to explain a black box.

Key related works:
- **Rudin (2019)**: "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead" — seminal argument for inherent interpretability
- **Caruana et al. (2015)**: Early work on GAMs (EBM predecessors) showing interpretable models can match random forests on clinical data
- **Lin et al. (2020)**: GOSDT — provably optimal sparse decision trees
- **Bouchiat et al. (2023)**: IGANN — interpretable generalized additive neural networks
- **Cranmer et al. (2023)**: PySR and advances in neural-guided symbolic regression

### Connection to Broader xAI Research

- **Feature Attribution** (SHAP, Integrated Gradients): Inherently interpretable models make attribution trivial — EBM shape functions ARE the attribution. No separate attribution step needed.
- **Concept-Based Explanations** (TCAV, CBMs): Symbolic regression can directly discover concept-aligned features if the operator set includes domain-relevant functions.
- **Causal Interpretability**: Linear models and GAMs enforce additivity constraints that align with causal disentanglement assumptions.
- **Fairness**: The paper's stratified analysis implicitly connects to fairness — class imbalance sensitivity in GOSDT is directly related to group fairness under demographic disparities.

### Where This Research Leads

1. **Hybrid interpretable architectures**: Future work could combine SR's symbolic expressiveness with EBM's robustness, e.g., using SR-discovered features as inputs to an additive model.
2. **Automated model selection**: The paper's dataset characterization → method recommendation pipeline could be automated via meta-learning, producing an "interpretable AutoML" system.
3. **LLM-assisted interpretation**: Combining EBMs or symbolic expressions with LLMs to generate natural language explanations of shape functions.
4. **Fairness-aware interpretable models**: Extending the benchmark to explicitly measure group fairness metrics alongside accuracy, providing a fairness-interpretability Pareto frontier.

### Relation to Interpretable ML Frameworks

- **InterpretML** (Microsoft): The EBM implementation used and the broader framework for comparing glass-box models
- **iModels** (Yu et al.): Unified API for rule-based interpretable models (RuleFit, BRL, FasterRisk, BRCG)
- **PySR** (Cranmer et al.): The leading open-source symbolic regression library
- **Christoph Molnar's IML Book**: The canonical reference for practitioner-oriented interpretable ML concepts that contextualizes this benchmark

---

*Documented: 2026-05-02 | xAI Subfield: Inherently Interpretable Models*
