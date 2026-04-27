# Explainability of Complex AI Models with Correlation Impact Ratio (ExCIR)

**ArXiv ID:** [2601.06701](https://arxiv.org/abs/2601.06701)  
**Authors:** Poushali Sengupta, Rabindra Khadka, Sabita Maharjan, Frank Eliassen, Yan Zhang, Shashi Raj Pandey, Pedro G. Lind, Anis Yazidi  
**Date:** January 10, 2026  
**Subfield:** Feature Attribution  
**Keywords:** ExCIR, correlation ratio, feature importance, SHAP limitations, LIME limitations, correlated features, scalable explainability

---

## Executive Summary

LIME and SHAP — the dominant post-hoc explainability methods — systematically misrank correlated features and scale poorly to high-dimensional data due to costly perturbation requirements. ExCIR (Explainability through Correlation Impact Ratio) introduces a theoretically grounded, efficient metric that correctly handles feature correlations by measuring the actual *correlation impact* of each feature on model outputs. Extended with an information-theoretic foundation via Canonical Correlation Analysis (CCA) and mutual information bounds, ExCIR enables multi-output and class-conditioned explainability at scale — addressing long-standing limitations of perturbation-based methods.

---

## Problem Statement

Modern AI models in production handle high-dimensional inputs (genomics with 50,000+ features, network security with millions of logs, financial risk models with thousands of variables). Current post-hoc XAI methods face critical limitations in these settings:

**SHAP limitations:**
- Exact Shapley value computation is exponential in number of features: $O(2^n)$
- Approximations (KernelSHAP, TreeSHAP) assume feature independence, producing systematically biased results when features are correlated
- Correlated features "split" importance between them, making both appear less important than the true causal feature
- Runtime: hours on datasets with >10K features

**LIME limitations:**
- Local linear approximation breaks for nonlinear models in high-dimensional spaces
- Neighborhood sampling without respecting feature correlations generates out-of-distribution samples
- Unstable: re-running on the same instance can produce different feature rankings

**The correlation problem (illustrated):**
Consider features $X_1$ (blood pressure) and $X_2$ (heart rate) with $\rho(X_1, X_2) = 0.85$. If the model uses $X_1$ causally, SHAP will attribute importance to both $X_1$ and $X_2$ due to correlation, misleading clinicians about which measurement actually matters.

**Research gap:** No existing method provides a theoretically grounded, efficient, correlation-aware attribution metric that scales to high-dimensional settings.

---

## Core Concepts & Theory

### Correlation Ratio (Classical Background)

The correlation ratio $\eta^2$ measures the proportion of variance in $Y$ explained by $X$:

$$\eta^2(Y|X) = \frac{\text{Var}(\mathbb{E}[Y|X])}{\text{Var}(Y)} = 1 - \frac{\mathbb{E}[\text{Var}(Y|X)]}{\text{Var}(Y)}$$

Unlike Pearson correlation, $\eta^2$ captures *any* functional relationship (not just linear), making it appropriate for complex nonlinear models.

### ExCIR: Correlation Impact Ratio

ExCIR extends the correlation ratio to account for interactions between features:

**Definition:** The ExCIR score for feature $i$ with respect to model output $\hat{Y}$ is:

$$\text{ExCIR}(X_i, \hat{Y}) = \eta^2(\hat{Y} | X_i) - \sum_{j \neq i} \omega_{ij} \cdot \eta^2(\hat{Y} | X_j) \cdot \rho^2(X_i, X_j)$$

where:
- $\eta^2(\hat{Y} | X_i)$: the marginal correlation ratio of $X_i$ with model output
- $\rho^2(X_i, X_j)$: squared Pearson correlation between features $i$ and $j$  
- $\omega_{ij}$: interaction weight (set to 1 by default; can be learned from data)

**Intuition:** The first term measures how much $X_i$ explains the model output. The second term *subtracts* the portion of that explanation that is redundant with correlated features $X_j$, ensuring each feature receives credit only for its *unique* contribution.

### Information-Theoretic Extension

The paper extends ExCIR with an information-theoretic foundation using Canonical Correlation Analysis (CCA):

**CCA-ExCIR:** Find the linear transformation $\mathbf{W}$ such that the canonical correlations between $\mathbf{X}$ and $\hat{\mathbf{Y}}$ (multi-output) are maximized:

$$\rho_{\text{canonical}} = \max_{\mathbf{w}_X, \mathbf{w}_Y} \text{corr}(\mathbf{w}_X^T \mathbf{X}, \mathbf{w}_Y^T \hat{\mathbf{Y}})$$

The ExCIR score in the CCA framework becomes:

$$\text{CCA-ExCIR}(X_i, \hat{\mathbf{Y}}) = \sum_{k=1}^{K} \rho_k^2 \cdot |w_{X,ki}|^2$$

where $\rho_k$ is the $k$-th canonical correlation and $w_{X,ki}$ is the $k$-th canonical direction weight for feature $i$.

**Mutual Information Bounds:** The authors prove that CCA-ExCIR provides upper and lower bounds on the true mutual information $I(X_i; \hat{\mathbf{Y}})$ under Gaussian assumptions, providing a formal connection between correlation-based attribution and information theory.

### Algorithmic Complexity

| Method | Time Complexity | Space Complexity |
|---|---|---|
| SHAP (exact) | $O(2^n)$ | $O(2^n)$ |
| KernelSHAP | $O(n^2 m)$ | $O(nm)$ |
| LIME | $O(nm)$ | $O(nm)$ |
| ExCIR | $O(n^2)$ | $O(n^2)$ |
| CCA-ExCIR | $O(n^3)$ | $O(n^2)$ |

For $n = 10,000$ features: SHAP is intractable, LIME takes hours, ExCIR runs in seconds, CCA-ExCIR in minutes.

---

## Main Ideas & Key Contributions

### 1. Theoretically Grounded Correlation Correction

ExCIR is the first feature attribution method with a formal correction for feature correlations derived from variance decomposition theory, rather than heuristics or independence assumptions.

### 2. Scalability to High-Dimensional Data

The $O(n^2)$ complexity makes ExCIR the first perturbation-free attribution method suitable for large-scale genomics, network security, and financial data where other methods are intractable.

### 3. Multi-Output Explainability

CCA-ExCIR naturally handles multi-output models (e.g., predicting multiple correlated risk scores simultaneously), producing feature attributions for each output component and across outputs.

### 4. Class-Conditioned Explainability

ExCIR can be conditioned on specific classes by restricting the correlation analysis to instances of that class, enabling contrastive explanations ("why did the model predict class A instead of class B?").

### 5. Stability Guarantees

Unlike LIME, ExCIR is deterministic (no random sampling) and provably stable: the same input always produces the same attribution. The paper proves a stability bound showing that ExCIR changes by at most $O(\epsilon)$ under $\epsilon$-perturbations of the input.

---

## Methodology & Implementation

### Experimental Setup

**Datasets:**
- UCI Adult Income (tabular, 15 features, binary classification)
- MIMIC-III clinical data (tabular, 200+ features, mortality prediction)
- Genomics (synthetic + real RNA-seq, 50,000 features, cancer classification)
- Network intrusion detection (KDD Cup 99, 41 features, multi-class)

**Models Tested:**
- Random Forests
- Gradient Boosting (XGBoost, LightGBM)
- Neural Networks (3-layer MLP, ResNet-tabular)
- Support Vector Machines

**Baseline Methods:**
- SHAP (KernelSHAP, TreeSHAP)
- LIME
- Permutation Importance
- Integrated Gradients (for neural networks)

### Evaluation Protocol

**Ground truth** established via:
1. **Synthetic data** with known causal structure (correlation-injected features clearly separate from causal features)
2. **Model-based ground truth**: TreeSHAP on tree models (exact for trees) as reference
3. **Human expert annotation** on clinical and network security datasets

**Metrics:**
- **Feature rank correlation** with ground truth (Spearman ρ)
- **Top-k precision** (% of true important features in top-k ranked)
- **Stability** (variance across 10 random seeds for stochastic methods)
- **Runtime** on increasing feature dimensions

### Key Results

| Method | Spearman ρ (correlated) | Top-5 Precision | Runtime (50K features) |
|---|---|---|---|
| KernelSHAP | 0.61 | 0.52 | N/A (intractable) |
| TreeSHAP | 0.79 | 0.74 | 15 min |
| LIME | 0.58 | 0.48 | 8.5 hours |
| Permutation Imp. | 0.71 | 0.66 | 2 hours |
| ExCIR (ours) | **0.88** | **0.85** | **18 seconds** |
| CCA-ExCIR (ours) | **0.91** | **0.89** | **4 minutes** |

### Limitations
- CCA-ExCIR assumes linear correlations between features (nonlinear correlations are handled only approximately)
- The $\omega_{ij}$ interaction weights in ExCIR require domain knowledge to set optimally (default=1 is a reasonable approximation)
- ExCIR measures correlation impact, not causal impact — the distinction matters when features are causally related in complex ways
- Continuous features only; categorical features require preprocessing

---

## Practical Applications & Real-World Use Cases

### Genomics and Precision Medicine

Gene expression datasets routinely have 20,000-50,000 features with strong correlations (co-expressed gene modules). Current XAI methods are intractable. ExCIR enables:
- Identifying driver genes vs. bystander genes in cancer classification
- Explaining patient stratification models to oncologists
- Meeting FDA guidance on AI/ML-based biomarker identification

### Network Security and Intrusion Detection

Network intrusion detection systems use hundreds of correlated traffic features (bytes sent/received, packet rates, connection durations are all correlated). ExCIR's correlation correction prevents false attribution to correlated-but-non-causal features.

### Financial Risk and Credit Scoring

Credit risk models combine correlated macroeconomic indicators, financial ratios, and market variables. ExCIR enables:
- Adverse action notices with correctly ranked feature importance
- Model risk management reports distinguishing genuine risk factors from correlation artifacts
- Fair lending analysis identifying which features drive disparate outcomes

### Real-Time Explainability

ExCIR's 18-second runtime on 50K features (vs. 8.5 hours for LIME) makes it the first method suitable for **real-time production explainability** — generating explanations while serving individual predictions without blocking pipelines.

### GDPR and EU AI Act Compliance

Article 22 GDPR requires explanations of automated decisions. ExCIR's stability guarantee (deterministic outputs) means the same explanation is provided each time a decision is reviewed, enabling consistent regulatory audits.

---

## Insights & Implications

### Rethinking Attribution Axioms

Standard XAI methods are evaluated against axioms from cooperative game theory (SHAP) or local linear approximation guarantees (LIME). ExCIR proposes a different axiomatic foundation based on variance decomposition and correlation theory, which may be more appropriate for correlated feature spaces that dominate real-world data.

### The Correlation-Causation Interface

ExCIR corrects for *linear* correlation confounding but not for nonlinear dependencies or causal confounding. This makes it a step in the right direction from the perspective of the "XAI is causality in disguise" framework (Karimi, 2026), but not a complete causal solution. A natural extension would integrate ExCIR with causal graph-based corrections.

### Scalability as a Missing XAI Property

The XAI literature has focused heavily on faithfulness and interpretability but relatively little on computational scalability. ExCIR's success on high-dimensional data suggests scalability should be treated as a first-class evaluation criterion in XAI benchmarks.

### Open Questions
- Can ExCIR's correlation correction be extended to handle nonlinear feature dependencies?
- How does ExCIR perform when the model itself is explicitly designed to exploit feature correlations?
- Is the CCA framework the right tool for multi-output attribution, or do other dimensionality reduction methods (KPCA, ICA) produce better attributions?
- Can ExCIR be combined with local approximation (like LIME) to get both scalability and locality?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2601.06701](https://arxiv.org/abs/2601.06701)
- **GitHub:** Check paper for repository link
- **Dependencies:** NumPy, SciPy, scikit-learn (minimal requirements)
- **Computational Requirements:** Single CPU core for n < 10K features; multi-core recommended for n > 10K

### Quick Start
```python
import numpy as np
from scipy.stats import spearmanr

def compute_excir(X, y_pred, feature_idx, omega=1.0):
    """
    Compute ExCIR score for feature at feature_idx.
    X: (n_samples, n_features)
    y_pred: (n_samples,) model predictions
    """
    n_features = X.shape[1]
    
    # Correlation ratio: eta^2(y_pred | X_i)
    def correlation_ratio(feature_values, target):
        categories = np.unique(np.round(feature_values, 2))  # discretize
        group_means = [target[np.round(feature_values, 2) == c].mean() 
                       for c in categories]
        group_sizes = [np.sum(np.round(feature_values, 2) == c) 
                       for c in categories]
        grand_mean = target.mean()
        ss_between = sum(n * (m - grand_mean)**2 
                        for n, m in zip(group_sizes, group_means))
        ss_total = np.sum((target - grand_mean)**2)
        return ss_between / ss_total if ss_total > 0 else 0
    
    eta_i = correlation_ratio(X[:, feature_idx], y_pred)
    
    # Correlation correction: subtract redundant contributions from correlated features
    correction = 0
    for j in range(n_features):
        if j != feature_idx:
            rho_sq = spearmanr(X[:, feature_idx], X[:, j])[0]**2
            eta_j = correlation_ratio(X[:, j], y_pred)
            correction += omega * eta_j * rho_sq
    
    return eta_i - correction

# Example usage
X = np.random.randn(1000, 50)
model_predictions = your_model.predict(X)

excir_scores = [compute_excir(X, model_predictions, i) for i in range(50)]
ranked_features = np.argsort(excir_scores)[::-1]
print("Top 5 most important features:", ranked_features[:5])
```

---

## Related Work & Context

### Building On
- **Pearson (1905)**: Correlation ratio — foundational concept
- **Hotelling (1936)**: Canonical Correlation Analysis
- **Owen (2014)**: Variance-based sensitivity analysis (Sobol' indices)
- **Adler & Taylor (2007)**: Random field theory for variance decomposition

### Contrasting With
- **Lundberg & Lee (2017)**: SHAP — game-theoretic attribution assuming feature independence
- **Ribeiro et al. (2016)**: LIME — local linear approximation
- **Janzing et al. (2020)**: Causal Shapley values — addresses causality but not scalability

### Connections to Broader XAI
ExCIR complements rather than replaces existing methods:
- For tabular data with correlated features at scale: ExCIR is the preferred choice
- For images/text where local perturbation is meaningful: SHAP/IG remain appropriate  
- For causal explanations: ExCIR provides correlation attribution; additional causal analysis needed

### Where This Leads
1. Nonlinear ExCIR using kernel methods for non-Gaussian feature distributions
2. Integration with causal discovery methods for causal ExCIR
3. Dynamic ExCIR for time series with temporally correlated features
4. Group ExCIR for attributing importance to sets of related features (e.g., gene modules, factor groups)

---

*Sources:*
- [arxiv.org/abs/2601.06701](https://arxiv.org/abs/2601.06701)
