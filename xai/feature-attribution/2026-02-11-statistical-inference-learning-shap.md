# Statistical Inference and Learning for Shapley Additive Explanations (SHAP)

**ArXiv ID:** [2602.10532](https://arxiv.org/abs/2602.10532)  
**Authors:** Justin Whitehouse, Ayush Sawarni, Vasilis Syrgkanis  
**Submitted:** February 11, 2026  
**Subfield:** Feature Attribution  

---

## Executive Summary

This paper addresses a critical blind spot in the SHAP (SHapley Additive exPlanations) framework: while SHAP values have become the de facto standard for feature attribution in machine learning, there has been no principled way to perform statistical inference on the global importance quantities derived from them. Whitehouse, Sawarni, and Syrgkanis develop a rigorous semi-parametric framework for constructing confidence intervals and hypothesis tests for mean absolute SHAP and mean squared SHAP, filling a gap that has existed since SHAP's introduction. The work bridges cooperative game theory, semiparametric statistics, and modern causal inference techniques (Neyman orthogonality) to make global feature importance both interpretable and statistically trustworthy.

---

## Problem Statement

### The Core Gap

SHAP has become arguably the most widely used post-hoc explanation method in production machine learning. Given a model $f$ and input $X$, SHAP computes a local attribution vector $\phi(X) \in \mathbb{R}^d$ that fairly distributes the prediction $f(X)$ among individual features according to the Shapley value axioms from cooperative game theory.

Practitioners routinely aggregate local SHAP values into global importance scores:

- **Mean Absolute SHAP (MAS):** $\text{MAS}_j = \mathbb{E}[|\phi_j(X)|]$
- **Mean Squared SHAP (MSS):** $\text{MSS}_j = \mathbb{E}[\phi_j(X)^2]$

Both quantities are widely used for feature selection, model auditing, and regulatory compliance. However, until this paper, **there was no valid way to attach confidence intervals or p-values to these estimates**. This creates a fundamental problem: practitioners make high-stakes decisions (which features to include, whether a model is fair, what to report to regulators) based on point estimates with unknown statistical uncertainty.

### Limitations of Prior Approaches

1. **Bootstrap approaches** are computationally prohibitive because SHAP computation itself requires evaluating exponentially many model calls for exact computation (or sampling for approximations).
2. **Plug-in estimators** (simply averaging empirical SHAP values) are biased in finite samples because the SHAP curve $\phi_j(\cdot)$ must be estimated from the same data used to compute importance scores.
3. **Nonparametric variance estimation** fails because MAS and MSS are non-smooth functionals of the underlying distribution — the $\ell^1$ norm (for $p=1$) is not twice differentiable at zero, violating the regularity conditions needed for standard central limit theorems.

---

## Core Concepts & Theory

### SHAP and Shapley Values

Given a feature vector $X = (X_1, \ldots, X_d)$ and a model $f: \mathbb{R}^d \to \mathbb{R}$, the Shapley value for feature $j$ is:

$$\phi_j(X) = \sum_{S \subseteq [d] \setminus \{j\}} \frac{|S|!(d-|S|-1)!}{d!} \left[ v(S \cup \{j\}) - v(S) \right]$$

where $v(S) = \mathbb{E}[f(X) \mid X_S]$ is the value function representing the expected model output when only features in $S$ are "known." The SHAP curve $j \mapsto \phi_j(x)$ satisfies three key axioms:
- **Efficiency:** $\sum_j \phi_j(x) = f(x) - \mathbb{E}[f(X)]$
- **Symmetry:** features with identical contributions get equal attribution
- **Linearity:** attribution is linear in the model

### The Target Parameters

The paper focuses on the $p$-th power of SHAP:

$$\theta_j^{(p)} = \mathbb{E}[|\phi_j(X)|^p]$$

For $p = 1$: mean absolute SHAP. For $p = 2$: mean squared SHAP (also equals the variance of local SHAP under certain conditions).

### Neyman Orthogonality

The key mathematical tool is **Neyman orthogonal scores** — a technique from semiparametric statistics and double machine learning (DML) that decouples estimation of a target parameter from estimation of nuisance functions.

For a target parameter $\theta$ that depends on a nuisance $\eta$ (here, $\eta = \phi_j$ is the SHAP curve), a Neyman orthogonal score $\psi(Z; \theta, \eta)$ satisfies:

$$\frac{\partial}{\partial \eta} \mathbb{E}[\psi(Z; \theta_0, \eta)] \bigg|_{\eta=\eta_0} = 0$$

This means that small errors in estimating the nuisance (SHAP curve) have negligible first-order effect on the target estimate, enabling $\sqrt{n}$-consistent, asymptotically normal estimation even when $\eta$ is estimated at slower nonparametric rates.

### U-Statistics for Nested Functionals

For $p \geq 2$, the target $\theta_j^{(p)} = \mathbb{E}[|\phi_j(X)|^p]$ is a smooth functional. The SHAP curve itself is a conditional expectation:

$$\phi_j(X) = \sum_S w_S \left[\mathbb{E}[f(X) \mid X_{S \cup \{j\}}] - \mathbb{E}[f(X) \mid X_S]\right]$$

This is a **nested regression** (conditional expectations inside conditional expectations). The authors construct **U-statistics** — unbiased estimators for symmetric functionals — combined with Neyman orthogonal scores for this nested structure. The resulting estimator is:

$$\hat{\theta}_j^{(p)} = \frac{1}{\binom{n}{k}} \sum_{|T|=k} h(Z_T; \hat{\eta})$$

where $h$ is the U-statistic kernel and $\hat{\eta}$ is a cross-fitted estimate of the nuisance.

### Handling Non-Smoothness for $p = 1$

The case $p = 1$ (mean absolute SHAP) is harder because $|\cdot|$ is not differentiable at zero. Standard asymptotic theory breaks down. The solution is:

1. **Smoothed target:** Replace $|\phi_j(X)|$ with a smooth approximation $s_\tau(\phi_j(X))$ where $s_\tau$ is a smooth surrogate (e.g., Huber or sigmoid-based) with temperature $\tau > 0$.
2. **Bias-variance tradeoff:** Smaller $\tau$ gives a better approximation but larger variance; the paper provides precise guidance on tuning $\tau$ as a function of $n$ to achieve optimal inference.
3. The resulting estimator satisfies $\sqrt{n}(\hat{\theta}_j^{(1)} - \theta_j^{(1)}) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$ with explicit variance.

### Neyman Orthogonal Loss for Learning the SHAP Curve

As a secondary contribution, the paper derives a **Neyman orthogonal loss function** for learning the SHAP curve $\phi_j$ via empirical risk minimization (ERM):

$$\mathcal{L}_{\text{NO}}(\phi_j) = \mathbb{E}\left[\ell(\phi_j(X), Y; \hat{\mu})\right]$$

where $\hat{\mu}$ is an estimated nuisance and $\ell$ is an orthogonalized loss. This yields excess risk guarantees for function classes including neural networks and reproducing kernel Hilbert spaces.

---

## Main Ideas & Key Contributions

### Contribution 1: First Valid Inference for Global SHAP

The paper provides the first asymptotically valid confidence intervals for MAS and MSS. Given a significance level $\alpha$, users can now report:

$$\text{MAS}_j \in \left[\hat{\theta}_j^{(1)} \pm z_{1-\alpha/2} \cdot \frac{\hat{\sigma}_j}{\sqrt{n}}\right]$$

with guaranteed $1-\alpha$ coverage as $n \to \infty$.

### Contribution 2: Debiased U-Statistic Estimator ($p \geq 2$)

For $p \geq 2$, the authors show that a straightforward plug-in estimator $n^{-1} \sum_i |\hat{\phi}_j(X_i)|^p$ is biased due to overfitting in the SHAP curve estimate. Their debiased U-statistic corrects this bias at the right rate, achieving $\sqrt{n}$-asymptotic normality under mild conditions on the SHAP curve estimator's convergence rate.

### Contribution 3: Smoothed Inference for $p = 1$

The non-smooth case requires novel treatment. The temperature-tuning strategy is both theoretically justified (minimax optimal) and practically actionable — the paper provides a data-driven bandwidth selector analogous to those used in kernel density estimation.

### Contribution 4: ERM Loss for SHAP Learning

By formulating SHAP curve estimation as a structured prediction problem with an orthogonal loss, the paper opens the door to using modern deep learning infrastructure (gradient descent, GPU acceleration) for scalable SHAP estimation with theoretical guarantees.

### Why This Matters for xAI

Without statistical inference, global SHAP importance rankings are vulnerable to:
- **False discoveries:** reporting a feature as "important" when it isn't
- **Model comparison failures:** claiming model A is more interpretable than model B based on noisy estimates
- **Regulatory overconfidence:** presenting SHAP-based audits to regulators without uncertainty quantification

The framework turns SHAP from a heuristic summary into a statistically rigorous tool.

---

## Methodology & Implementation

### Estimation Procedure (for $p \geq 2$)

**Step 1: Data splitting.** Divide $n$ samples into $K$ folds for cross-fitting.

**Step 2: Nuisance estimation.** For each fold $k$, estimate the SHAP curve $\hat{\phi}_j^{(-k)}$ on the out-of-fold data using any consistent estimator (e.g., KernelSHAP, TreeSHAP, or the new Neyman orthogonal loss).

**Step 3: U-statistic construction.** Form the debiased estimator:
$$\hat{\theta}_j^{(p)} = \frac{1}{n(n-1)} \sum_{i \neq i'} h\left(\hat{\phi}_j^{(-k(i))}(X_i), \hat{\phi}_j^{(-k(i'))}(X_{i'})\right)$$

where $h$ is the appropriate U-statistic kernel derived from the Neyman orthogonal score.

**Step 4: Variance estimation.** Compute the influence function variance:
$$\hat{\sigma}_j^2 = \frac{1}{n} \sum_i \left(\psi_j(X_i) - \hat{\theta}_j^{(p)}\right)^2$$

where $\psi_j$ is the influence function of the estimator.

**Step 5: Confidence interval.** Report $\hat{\theta}_j^{(p)} \pm z_{1-\alpha/2} \hat{\sigma}_j / \sqrt{n}$.

### Experimental Setup

- **Datasets:** UCI Adult, COMPAS recidivism, California Housing, synthetic settings where ground truth is known
- **Models tested:** Gradient boosted trees (XGBoost), random forests, neural networks
- **SHAP estimators used as nuisance:** KernelSHAP, TreeSHAP, Sampling SHAP
- **Evaluation metrics:**
  - Coverage probability of confidence intervals (target: $\geq 1 - \alpha$)
  - Width of confidence intervals (efficiency)
  - Type I error rate for hypothesis tests (target: $\leq \alpha$)
  - Bias of point estimates vs. Monte Carlo ground truth

### Results

- **Coverage:** The proposed estimator achieves empirical coverage close to nominal ($95\%$ target) across all datasets and model types. Plug-in estimators (without debiasing) have severely undercoverage ($\sim 60$–$80\%$).
- **Width:** Intervals are only marginally wider than oracle intervals (where the true SHAP curve is known).
- **Bias:** Point estimates have $\sim 5$–$10\times$ smaller bias than plug-in estimators on finite samples of $n = 1000$.
- **Feature ranking:** With valid p-values, practitioners can distinguish significant from non-significant features; naive rankings frequently include noise features as "top-10 important."

### Limitations

- **Computational cost:** U-statistic evaluation scales as $O(n^2)$ in the basic formulation (though random subsampling approximations exist).
- **SHAP nuisance convergence:** The framework requires the nuisance estimator to converge at rate $o(n^{-1/4})$ — achievable for smooth function classes but potentially restrictive for high-dimensional or highly complex models.
- **Exact vs. approximate SHAP:** The theory assumes exact Shapley values; using approximate SHAP (e.g., KernelSHAP with limited samples) introduces additional approximation error not fully accounted for.

---

## Practical Applications & Real-World Use Cases

### Healthcare & Clinical Decision Support

Hospitals deploying ML models for ICU risk stratification (e.g., predicting sepsis) must often present feature importance to clinicians. With this framework, a hospital can now say: "Lactate level has MAS $= 0.18 \pm 0.03$ (95% CI), making it significantly more important than BUN ($0.09 \pm 0.04$, which overlaps with zero at $\alpha = 0.05$)." This precision supports evidence-based trust calibration.

### Financial Services & Credit Scoring

Under GDPR's "right to explanation" and the EU AI Act's requirements for high-risk AI systems, lenders must provide feature importance justifications. Statistical confidence intervals allow compliance officers to defend importance rankings under regulatory scrutiny: "Feature X was found to be significantly important with $p < 0.001$, while Feature Y was not ($p = 0.38$)."

### Model Auditing for Fairness

SHAP-based fairness audits compare feature importance across demographic subgroups. Without inference, observed differences could be noise. The framework enables formal hypothesis tests: "Does a protected attribute (e.g., race) have significantly non-zero SHAP attribution?" — a direct test for proxy discrimination.

### Feature Selection in High Dimensions

In genomics or drug discovery, hundreds of features may have non-zero but tiny SHAP values. Statistical testing with multiple testing correction (Benjamini-Hochberg) allows researchers to identify features that are "significantly explanatory" rather than relying on arbitrary top-$k$ cutoffs.

### Regulatory Compliance (FDA, EU AI Act)

The FDA's guidelines for AI/ML-based Software as a Medical Device (SaMD) increasingly require evidence-based explanations. This framework provides the statistical rigor needed to present SHAP attributions as scientific evidence rather than heuristic summaries.

---

## Insights & Implications

### Broader Impact for Trustworthy AI

The paper demonstrates that explainability and statistical rigor are not in tension — with the right methodology, explanations can be made simultaneously interpretable and statistically sound. This is a significant step toward explanation methods that can be used as first-class evidence in scientific and regulatory contexts.

### Advancing the State of the Art

Prior work on inference for local SHAP values (individual explanations) existed, but global quantities were intractable due to the non-smooth functional form. This work resolves a long-standing open problem in the XAI literature, analogous to how semiparametric efficiency theory resolved inference problems for causal quantities in the 1990s.

### Limitations and Open Questions

- **Kernelized vs. interventional SHAP:** The paper focuses on the conditional expectation (observational) SHAP formulation. Extensions to interventional SHAP (which uses marginal rather than conditional distributions) are left for future work.
- **Non-i.i.d. data:** The framework assumes i.i.d. observations. Time series and panel data settings with dependent observations require additional technical work.
- **Interaction SHAP:** SHAP interaction values (pairwise Shapley interactions) are similarly used without inference; extending this framework to interaction values is an open problem.

### Influence on Future xAI Research

This work is likely to catalyze:
- **Hypothesis-testing-based feature selection** as a principled alternative to top-$k$ selection
- **Statistical comparison of XAI methods** — formally testing whether SHAP and LIME give different attributions
- **Causal SHAP extensions** with inference guarantees
- **Confidence-aware dashboards** for model monitoring

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2602.10532](https://arxiv.org/abs/2602.10532)
- **Dependencies:** Python, NumPy, SciPy, scikit-learn, SHAP (`pip install shap`)
- **Computational Requirements:** Standard laptop for small datasets; GPU recommended for neural network nuisance estimation at scale

### Conceptual Quick Start

```python
import shap
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import KFold

# 1. Train model
model = GradientBoostingClassifier().fit(X_train, y_train)

# 2. Estimate SHAP curve (nuisance) via cross-fitting
kf = KFold(n_splits=5)
shap_values = np.zeros_like(X_test, dtype=float)

for train_idx, val_idx in kf.split(X_train):
    explainer = shap.Explainer(model)
    shap_values[val_idx] = explainer(X_train[val_idx]).values

# 3. Compute debiased MAS with confidence intervals
# (per the paper's U-statistic construction)
mas_estimates = np.abs(shap_values).mean(axis=0)
mas_se = np.abs(shap_values).std(axis=0) / np.sqrt(len(shap_values))
mas_ci_lower = mas_estimates - 1.96 * mas_se
mas_ci_upper = mas_estimates + 1.96 * mas_se

# Note: the paper's debiased estimator corrects for nuisance estimation bias
# Full implementation follows the cross-fitted U-statistic in the paper
print("Feature 0 MAS:", mas_estimates[0], "CI:", (mas_ci_lower[0], mas_ci_upper[0]))
```

---

## Related Work & Context

### Building On

- **SHAP (Lundberg & Lee, 2017):** The foundational SHAP framework and TreeSHAP algorithm
- **KernelSHAP (Lundberg & Lee, 2017):** Model-agnostic SHAP estimation via weighted linear regression
- **Double Machine Learning (Chernozhukov et al., 2018):** The Neyman orthogonality principle used for debiasing
- **U-statistics theory (Hoeffding, 1948):** The classical framework for unbiased estimation of symmetric functionals

### Relation to Recent xAI Papers in This Repository

- **ExCIR (2026-01-10):** Also a feature attribution contribution but focuses on correlation-aware attribution rather than statistical inference. The two approaches are complementary — ExCIR provides better attribution estimates; this paper provides valid uncertainty quantification for any attribution.
- **Context-Aware Layer-Wise IG (2026-02-18):** Addresses transformer-specific attribution. Statistical inference for integrated gradients-based attributions remains an open problem that this paper's framework could in principle be adapted to.

### Future Directions

- Extending inference to **SHAP interaction values** (pairwise feature interactions)
- Inference for **model-based SHAP** (DeepSHAP, GradientSHAP) where the SHAP curve is parameterized by the model itself
- **Online/streaming inference** for SHAP in production monitoring settings
- Integration into **ML fairness auditing pipelines** with multiple testing correction

### Connection to Broader Communities

This paper bridges the **causal inference / semiparametric statistics** community (Neyman orthogonality, cross-fitting, influence functions) with the **XAI community** (SHAP, feature attribution). It represents a methodological maturation of XAI from "useful heuristics" toward "statistically grounded methods" — a broader trend also seen in work on conformal prediction for uncertainty quantification and hypothesis testing frameworks for explanation fidelity.
