# RoSHAP: A Distributional Framework and Robust Metric for Stable Feature Attribution

## Executive Summary

This paper addresses a critical but underexplored limitation of SHAP and other feature attribution methods: their instability and stochastic variation across different training runs, random seeds, and model configurations. RoSHAP proposes a distributional framework that models the uncertainty inherent in feature attribution and introduces a robust ranking criterion that rewards features exhibiting stability alongside strength and activity. This advancement is significant for xAI because it improves the reliability and trustworthiness of widely-deployed feature attribution methods, making them more suitable for high-stakes decision-making.

## Problem Statement

Feature attribution measures like SHAP have become foundational tools in explainable AI for understanding model behavior and supporting data-driven decisions. However, a persistent problem undermines their practical utility: **feature attributions are not stable across different experimental conditions**. 

Specifically, feature attribution values and rankings can vary substantially depending on:
- Different train-test splits
- Different random seeds during model training
- Different hyperparameter configurations
- Different model-fitting procedures

This stochastic variation creates a fundamental challenge: practitioners cannot confidently rely on feature rankings produced by a single model run, as the results may change substantially if the model is retrained or evaluated under slightly different conditions. This uncertainty propagates to downstream applications such as feature selection, where selecting features based on unstable attributions can lead to poor generalization.

Prior SHAP-based methods treat feature attribution as a deterministic quantity, ignoring this inherent variability. Consequently, current xAI practices provide no principled way to assess or mitigate attribution instability—a critical gap for trustworthy AI systems.

## Core Concepts & Theory

### Feature Attribution and SHAP Fundamentals

Feature attribution methods estimate the contribution of each input feature to a model's prediction. SHAP (SHapley Additive exPlanations) is a unified framework based on game theory that computes the average marginal contribution of each feature across all possible coalitions of features.

The SHAP value for feature $i$ is defined as:
$$\phi_i(x) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(n-|S|-1)!}{n!} \left[ f(S \cup \{i\}) - f(S) \right]$$

where:
- $N$ is the set of all features
- $S$ is a subset of features not including $i$
- $f(S)$ represents the model prediction with only features in $S$

While SHAP provides a theoretically grounded measure of feature importance, it is computed on a single trained model, producing a single deterministic attribution value per feature.

### The Distributional Perspective

RoSHAP's key insight is that feature attribution should be viewed as a **random variable** rather than a fixed quantity. When a model is trained with different random seeds or data splits, the resulting SHAP values follow a distribution:

$$\Phi_i \sim \text{Distribution of SHAP values across multiple runs}$$

By characterizing this distribution, we can:
1. Quantify the **stability** of attribution estimates
2. Distinguish between features with consistently high attributions (reliable) and those with variable attributions (unreliable)
3. Construct attribution rankings that account for both magnitude and stability

### Distribution Estimation via Bootstrap and Kernel Density Estimation

RoSHAP estimates the distribution of SHAP values through a two-stage procedure:

**Stage 1: Bootstrap Resampling**
- Perform $B$ independent model training runs, each with a different random seed or data split
- For each run $b = 1, \ldots, B$, compute SHAP values $\{\phi_i^{(b)}\}_{i=1}^n$ for all features
- Collect the empirical samples: $\{\phi_i^{(1)}, \phi_i^{(2)}, \ldots, \phi_i^{(B)}\}$

**Stage 2: Kernel Density Estimation (KDE)**
- For each feature $i$, estimate the probability density function using KDE:
$$\hat{f}_i(\phi) = \frac{1}{B h} \sum_{b=1}^B K\left(\frac{\phi - \phi_i^{(b)}}{h}\right)$$

where $K$ is a kernel function (typically Gaussian) and $h$ is the bandwidth parameter.

### Gaussian Approximation

A key theoretical contribution is proving that under mild regularity conditions, the **aggregated feature attribution** converges to a Gaussian distribution:

$$\bar{\Phi}_i = \frac{1}{B}\sum_{b=1}^B \phi_i^{(b)} \approx \mathcal{N}(\mu_i, \sigma_i^2)$$

This asymptotic normality result significantly reduces computational cost: instead of requiring expensive kernel density estimation on each feature's full distribution, practitioners can parameterize the distribution using only the mean $\mu_i$ and variance $\sigma_i^2$.

### The RoSHAP Criterion

RoSHAP combines three components into a single robust ranking criterion:

1. **Activity ($A_i$)**: The proportion of nonzero attribution values across the $B$ runs
   $$A_i = \frac{1}{B} \sum_{b=1}^B \mathbb{1}[\phi_i^{(b)} \neq 0]$$

2. **Strength ($R_i$)**: The median magnitude of nonzero attributions
   $$R_i = \text{median}(|\phi_i^{(b)}| : \phi_i^{(b)} \neq 0)$$

3. **Stability ($S_i$)**: A measure of consistency quantified through the coefficient of variation (ratio of standard deviation to mean)
   $$S_i = \frac{\sigma_i}{\bar{\Phi}_i} \text{ (lower is more stable)}$$

The final RoSHAP score combines these three components:
$$\text{RoSHAP}_i = A_i \cdot R_i \cdot f(S_i)$$

where $f(S_i)$ is a penalty function that decreases with higher variability. Features are ranked by RoSHAP scores, prioritizing those that are simultaneously active, strong, and stable.

## Main Ideas & Key Contributions

### 1. Formalizing Attribution Stability as a Distributional Problem

The paper's primary contribution is **reframing feature attribution instability as a statistical problem** requiring distributional characterization. Rather than viewing SHAP as producing a single correct answer, RoSHAP recognizes that attribution estimates are subject to empirical and model-fitting variability—a perspective that aligns with how statisticians treat model-dependent estimates.

### 2. Practical Distribution Estimation Framework

RoSHAP provides a practical, computationally efficient method to estimate SHAP distributions through bootstrap resampling and kernel density estimation. The Gaussian approximation further reduces computational overhead, making the approach scalable to moderate-to-large feature sets.

### 3. Robust Feature Ranking Criterion

The three-component RoSHAP criterion (activity, strength, stability) represents a principled way to rank features that goes beyond raw attribution magnitude. By incorporating stability as an explicit criterion, RoSHAP identifies features whose importance is **reliably confirmed across different model training runs**—a critical property for trustworthy feature selection.

### 4. Theoretical Validation

The paper provides asymptotic analysis proving that the aggregated SHAP values converge to a Gaussian distribution under reasonable regularity conditions. This theoretical foundation justifies the practical computational simplifications employed in the framework.

### 5. Comparative Analysis with Single-Run Attribution

Extensive experiments demonstrate that RoSHAP significantly outperforms standard single-run SHAP in identifying truly important features, particularly in scenarios with high model training variability or when feature importance is heterogeneous.

## Methodology & Implementation

### Experimental Setup

The paper evaluates RoSHAP on:
- **Simulated datasets**: Controlled scenarios where ground truth feature importance is known
- **Real-world datasets**: Benchmarks from UCI Machine Learning Repository and other sources
- **Different model architectures**: Linear models, tree-based models (XGBoost), neural networks

### Models and Datasets Tested

Key experimental settings include:
- Datasets with varying numbers of features (10 to 1000+ features)
- Different sample sizes to test scalability
- Multiple model types to assess generalizability
- Simulations with known signal-noise structures to validate recovery

### Evaluation Metrics for Attribution Stability

1. **Feature Recovery Accuracy**: Percentage of true signal features correctly identified by each method
2. **False Positive Rate**: Proportion of noise features incorrectly ranked as important
3. **Ranking Correlation**: Spearman correlation between rankings from different model runs
4. **Stability Score**: Variance of feature rankings across multiple runs

### Key Results

[Exact figures unavailable — see full paper]

The experiments demonstrate that:
- RoSHAP achieves higher feature recovery rates than standard SHAP across diverse settings
- The stability component of RoSHAP criterion is effective at filtering out unstable features
- Models built using RoSHAP-selected features achieve comparable predictive performance to full-feature models while using substantially fewer predictors (e.g., achieving similar accuracy with 30-50% of original features)
- The computational overhead of RoSHAP is moderate, with bootstrap estimation feasible for practical datasets

### Practical Feasibility and Limitations

**Advantages:**
- Minimal modifications needed to existing SHAP implementations
- Bootstrap-based approach is parallelizable
- Gaussian approximation enables computational efficiency
- Applicable to any SHAP variant (TreeSHAP, DeepSHAP, KernelSHAP)

**Limitations:**
- Requires multiple model training runs, increasing computational cost compared to single-run SHAP
- Performance depends on the number of bootstrap samples $B$; larger $B$ provides more stable estimates but increases computation
- Assumes that attribution instability primarily arises from training variability; other sources of uncertainty (e.g., model misspecification) may not be captured
- The three-component criterion (activity, strength, stability) involves hyperparameter choices that may require tuning for different applications

## Practical Applications & Real-World Use Cases

### Healthcare and Clinical Risk Prediction

In clinical decision-support systems, physicians rely on model explanations to understand why a model flagged a patient as high-risk. Unstable features in attribution can lead to:
- Inconsistent explanations across model retraining cycles
- Loss of clinician confidence in the model
- Potential non-compliance with FDA requirements for explainable AI in medical devices

RoSHAP's stability-focused ranking helps identify clinical features whose importance is **consistently confirmed**, providing more reliable guidance for treatment decisions.

### Finance and Credit Scoring

Credit models are frequently retrained on new data to maintain performance. Without accounting for attribution stability, credit explanations can shift dramatically, confusing applicants and creating compliance issues under fair lending regulations.

RoSHAP ensures that features ranked as important for credit decisions remain consistently important across model retraining cycles, supporting regulatory compliance (FCRA, Dodd-Frank) and interpretability requirements.

### Autonomous Systems and Safety-Critical Applications

In autonomous vehicles and robotics, model interpretability is essential for safety validation. Unstable feature importance can indicate brittle learned patterns that may fail under distribution shift.

RoSHAP's stability measure provides a safety signal: features with high RoSHAP scores are more likely to represent robust learned relationships, while unstable features warrant additional scrutiny.

### Regulatory Compliance and AI Governance

**GDPR Right to Explanation**: Article 22 of GDPR grants individuals the right to obtain meaningful explanations of automated decisions. RoSHAP strengthens this by providing stable, reliable attributions that better reflect true model behavior.

**AI Act Requirements**: The EU AI Act requires high-risk AI systems to maintain detailed documentation of model behavior. RoSHAP's distributional framework provides this documentation: practitioners can report not just which features drive predictions, but the confidence/stability of those attributions.

**FDA Medical Device Regulation**: The FDA expects explainable AI in medical devices to produce **consistent** explanations. RoSHAP directly addresses this requirement by filtering for attribution stability.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Attribution Instability is a Real and Solvable Problem**: RoSHAP validates that feature attribution variability across model training runs is a genuine phenomenon affecting practical xAI deployments. The paper demonstrates this is not merely a statistical artifact but has real consequences for feature selection and model interpretation.

2. **Stability as a Core XAI Criterion**: The paper elevates stability to a first-class consideration in feature attribution, alongside magnitude. This shifts the xAI paradigm from "which features are most important" to "which features are reliably important"—a more actionable question for practitioners.

3. **Distributional Thinking in XAI**: RoSHAP exemplifies a broader trend toward characterizing uncertainty in model explanations rather than treating them as point estimates. This aligns with growing recognition that interpretability methods are themselves statistical estimators subject to uncertainty.

### Advancing State-of-the-Art Explainability

1. **Post-Hoc Attribution Robustness**: While prior work focused on improving attribution fidelity and computational efficiency, RoSHAP addresses a complementary axis: **robustness of attributions to training variability**. This fills a gap in the xAI toolkit.

2. **Bridging Explainability and Robustness**: By incorporating stability, RoSHAP connects feature attribution to broader robustness research, suggesting that trustworthy explanations require robustness guarantees.

3. **Practical Rigor**: The paper demonstrates how statistical rigor (Gaussian approximation, asymptotic theory) can be brought to bear on practical xAI problems without sacrificing scalability.

### Limitations and Open Questions

1. **Multiple Runs Requirement**: RoSHAP requires $B$ model training runs, which is computationally expensive. While the paper provides efficiency improvements through Gaussian approximation, the fundamental cost remains higher than single-run SHAP. Future work could explore efficient estimation from fewer runs or from gradient information.

2. **Sources of Variability**: The paper focuses on variability from training randomness and data splits. Other sources of attribution instability—e.g., arising from model misspecification or feature multicollinearity—may not be adequately captured.

3. **Hyperparameter Sensitivity**: The RoSHAP criterion combines activity, strength, and stability through a weighting scheme. The optimal weighting may be problem-dependent, requiring tuning for different domains.

4. **Generalization to Other Attribution Methods**: While the paper focuses on SHAP, it would be valuable to explore whether the distributional framework applies effectively to other attribution methods (e.g., integrated gradients, attention-based explanations).

### Future Research Directions

1. **Efficient Stability Estimation**: Develop methods to estimate attribution stability from a single model run using techniques like influence functions or Hessian information.

2. **Uncertainty Quantification**: Extend RoSHAP to provide confidence intervals or credible regions for feature importance, formalizing the notion of "uncertain attributions."

3. **Domain-Specific Stability Criteria**: Tailor stability measures for specific domains (e.g., prioritizing stability of rare events in imbalanced datasets).

4. **Integration with Active Learning**: Use RoSHAP's stability scores to guide active learning, prioritizing training on features with high attribution stability.

## Code & Resources

### Official Implementation

- **Repository**: [RobustSHAP on GitHub](https://github.com/Lanxin-Xiang/RobustSHAP)
- **License**: Check repository for details
- **Language**: Python

### Dependencies and Requirements

[Exact requirements unavailable — see full paper and GitHub repository]

Typical requirements likely include:
- Python 3.7+
- NumPy and SciPy for numerical computation
- scikit-learn for machine learning utilities
- SHAP library for base feature attribution computation
- Optional: XGBoost, PyTorch, or TensorFlow for model training

### Quick Start Guide

General workflow (see repository for detailed code examples):

1. **Install RoSHAP**: Clone repository and install dependencies
2. **Prepare data**: Load your dataset and train initial model
3. **Run bootstrap loop**: Train model $B$ times with different random seeds
4. **Compute SHAP values**: Calculate SHAP attributions for each model run
5. **Fit distributions**: Use KDE to estimate feature attribution distributions
6. **Rank features**: Compute RoSHAP scores and obtain robust feature rankings

### Interactive Resources

The GitHub repository likely includes:
- Jupyter notebooks demonstrating RoSHAP on benchmark datasets
- Visualizations of attribution distributions
- Comparisons with standard SHAP on real and synthetic data
- Code for reproducing results from the paper

## Related Work & Context

### Connection to SHAP and Feature Attribution Evolution

RoSHAP builds directly on SHAP (Lundberg & Lee, 2017), one of the most influential xAI methods. While SHAP provided a theoretically-grounded, unified framework for feature attribution, RoSHAP extends SHAP by addressing its implicit assumption of attribution determinism.

The paper positions itself within the lineage of SHAP improvements:
- **TreeSHAP** (Lundberg et al., 2020): Efficient SHAP computation for tree-based models
- **FastSHAP** (Jethani et al., 2021): Accelerated SHAP via model distillation
- **RoSHAP** (2026): **Robust** SHAP accounting for training variability

### Prior Work on Attribution Instability

While attribution instability has been noted in the literature (e.g., works on adversarial robustness of saliency maps), systematic treatment of training-induced SHAP variability is limited. RoSHAP is among the first to formally characterize and mitigate this specific problem.

### Broader Context in Interpretability Research

RoSHAP connects to several broader themes:

1. **Robustness of Explanations**: Growing recognition that explanations must be robust to perturbations and variability, not just faithful to a single model instance (cf. work on adversarial examples and explanation robustness).

2. **Uncertainty in XAI**: An emerging research direction exploring uncertainty quantification in model explanations (e.g., Bayesian approaches to attribution, distributional uncertainty in saliency maps).

3. **Feature Selection Reliability**: Classic feature selection research has long emphasized stability of rankings across cross-validation folds. RoSHAP adapts this statistical wisdom to the xAI domain.

### Relationship to Related Concepts

**Causal Feature Attribution**: While RoSHAP focuses on computational stability, causal interpretability methods (e.g., work on causal SHAP) address stability in a different sense—ensuring attributions correspond to causal relationships. These are complementary approaches.

**Model Multiplicity and Interpretability**: The related problem of how different equally-good models produce different explanations (Ghorbani et al., 2020) motivated distribution-based thinking in explanations, which RoSHAP formalizes.

**Mechanistic Interpretability**: While RoSHAP operates at the post-hoc level, mechanistic interpretability research on internal neural network representations also emphasizes stability and consistency of learned features.

### Position in the xAI Community

RoSHAP makes a targeted contribution to the feature attribution subcommunity, complementing:
- **LIME community**: Methods for local linear approximations
- **Shapley-based community**: Various SHAP improvements and variants
- **Concept-based methods**: Higher-level explanations through learned concepts
- **Causal inference community**: Causal and counterfactual explanations

## Key Takeaways

1. **SHAP values are unstable**: Feature attribution scores vary substantially across different model training runs, a phenomenon underexplored in prior xAI work.

2. **Stability matters**: Practitioners should prioritize features whose importance is **consistently confirmed** across different training conditions, not just those with high magnitude attributions.

3. **Distributional approach is practical**: Modeling feature attribution distributions via bootstrap resampling and KDE is computationally feasible and provides actionable insights for feature selection.

4. **RoSHAP as a tool**: The RoSHAP criterion combining activity, strength, and stability provides a principled way to rank features for robust interpretation and reliable feature selection.

5. **Implications for high-stakes AI**: In domains like healthcare, finance, and autonomous systems, RoSHAP's stability-focused rankings provide more trustworthy explanations aligned with regulatory requirements.

---

**ArXiv ID**: 2605.15154  
**Publication Date**: May 14, 2026  
**Authors**: Lanxin Xiang, Liang Shi, Youhui Ye, Boyu Jiang, Dawei Zhou, and Feng Guo  
**GitHub Repository**: https://github.com/Lanxin-Xiang/RobustSHAP
