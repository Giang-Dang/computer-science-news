# SHLIME: Foiling Adversarial Attacks Fooling SHAP and LIME

**Paper**: SHLIME: Foiling adversarial attacks fooling SHAP and LIME  
**ArXiv ID**: [2508.11053](https://arxiv.org/abs/2508.11053)  
**Authors**: Sam Chauhan, Estelle Duguet, Karthik Ramakrishnan, Hugh Van Deventer, Jack Kruger, Ranjan Subbaraman  
**Published**: August 2025  
**Field**: Feature Attribution, Explainability Robustness, Fairness-aware XAI  

## Executive Summary

This paper addresses a critical vulnerability in widely-used post-hoc explanation methods (LIME and SHAP): they can be systematically deceived by adversarially-biased models to conceal harmful feature importance patterns. The authors propose SHLIME, a framework that employs ensemble configurations of LIME and SHAP to substantially improve robustness against bias concealment and enhance transparency in high-stakes machine learning systems where fairness is critical.

## Problem Statement

Post-hoc explanation methods like LIME (Local Interpretable Model-agnostic Explanations) and SHAP (SHapley Additive exPlanations) have become standard tools for assessing model bias and interpretability in high-stakes domains such as criminal justice, lending, and healthcare. However, recent research has demonstrated that these methods are vulnerable to adversarial manipulation:

1. **Adversarial Concealment**: Biased models can be crafted to fool LIME and SHAP by deflecting feature importance away from the actual discriminatory features toward spurious correlates
2. **Insufficient Detection**: Standard LIME and SHAP explanations alone cannot reliably detect when a model is deliberately hiding its biases
3. **Trust Gap**: This vulnerability undermines confidence in explainability-based fairness auditing, a key mechanism for governance and compliance

The paper builds upon the seminal work "Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods" (2019) and extends it with systematic defense mechanisms.

## Core Concepts & Theory

### LIME (Local Interpretable Model-agnostic Explanations)

LIME generates local linear approximations of a black-box model's behavior around a specific input. The methodology:

1. Sample perturbations of the input instance
2. Obtain predictions from the target model on these perturbed inputs
3. Weight each perturbed sample by its proximity to the original instance
4. Fit a weighted linear model to approximate local model behavior
5. Return feature coefficients as importance scores

**Strengths**: Model-agnostic, interpretable, fairly faithful locally  
**Limitations**: Expensive (requires many perturbations), unstable across different random seeds, sensitive to hyperparameters

### SHAP (SHapley Additive exPlanations)

SHAP provides theoretically-grounded feature importance through Shapley values from cooperative game theory:

1. For each feature, compute marginal contribution by comparing predictions with/without the feature
2. Average contribution over all possible orderings of features (coalitions)
3. This averaging yields Shapley values satisfying desirable axiomatic properties (efficiency, symmetry, dummy, additivity)

**Strengths**: Theoretically principled, model-agnostic, provides both positive and negative attributions  
**Limitations**: Computationally expensive for large feature spaces, relies on value function (how features are masked), can be manipulated through careful model design

### The Adversarial Attack on SHAP/LIME

An adversarially-biased classifier can:

1. Learn to make its decisions based on a sensitive feature (e.g., race in COMPAS)
2. Simultaneously learn spurious correlations with multiple other features
3. When SHAP/LIME applies perturbations, the correlation structure changes, and the model's explanations are based on these spurious features rather than the actual decision boundary
4. The explanation methods report the spurious features as important, effectively concealing the true source of bias

### Defense Strategy: Ensemble Approaches

SHLIME proposes aggregating multiple LIME/SHAP explanations to improve robustness:

1. **Multiple Perturbation Strategies**: Run LIME/SHAP with different random seeds, hyperparameter settings, or perturbation distributions
2. **Voting/Averaging**: Combine results across ensemble members using:
   - **Voting**: Consensus which features are "important"
   - **Averaging**: Average importance scores across ensemble members
3. **Outlier Detection**: Identify and flag instances where ensemble members strongly disagree
4. **Out-of-Distribution Detection**: Flag samples that fall outside the training distribution, making them more susceptible to adversarial concealment

## Main Ideas & Key Contributions

### 1. Systematic Evaluation Framework

The paper introduces a **modular testing framework** that enables:

- Systematic evaluation of different ensemble configurations
- Testing across classifiers with varying levels of bias (from unbiased to highly biased)
- Evaluation on multiple datasets with different sensitive attributes
- Out-of-distribution testing to understand generalization

This framework is more comprehensive than the single COMPAS experiment in prior work.

### 2. Ensemble Configurations for Robustness

The research evaluates multiple ensemble strategies:

1. **Seed Ensembles**: Multiple LIME/SHAP runs with different random seeds
2. **Hyperparameter Ensembles**: Varying perturbation distribution, kernel width, or number of samples
3. **Hybrid Ensembles**: Combining different perturbation strategies
4. **Voting vs. Averaging**: Different aggregation methods

**Key Finding**: Certain ensemble configurations substantially outperform single-method explanations in detecting biased features even when the model is adversarially constructed.

### 3. Replication and Extension of COMPAS Experiment

The authors replicate the original COMPAS recidivism prediction benchmark and extend it by:

- Testing on classifiers with varying degrees of adversarial concealment
- Evaluating ensemble configurations systematically
- Testing robustness of different ensemble aggregation strategies
- Assessing performance across multiple datasets (COMPAS, Communities & Crime, German Credit)

### 4. Practical Framework for Bias Detection

The framework identifies configuration combinations that:

- **Maintain High Recall**: Detect biased features reliably
- **Reduce False Positives**: Don't flag unimportant spurious features as important
- **Generalize Across Domains**: Work on different datasets and bias types

## Methodology & Implementation

### Experimental Design

**Datasets**:
1. **COMPAS**: Recidivism prediction with sensitive attribute (race)
2. **Communities and Crime**: Violent crime prediction with sensitive attribute (race)
3. **German Credit**: Credit scoring with sensitive attribute (gender)

Each dataset includes both unbiased and adversarially-constructed models.

**Classifier Types Tested**:
- Logistic regression (simple baseline)
- Random forests (nonlinear)
- Neural networks (complex decision boundaries)

**Models Evaluated**:
1. **Unbiased baseline**: Trained on full feature set, naturally non-discriminatory
2. **Naive biased**: Trained with sensitive feature, explicitly uses it for decisions
3. **Adversarial biased**: Constructed to maximize use of sensitive feature while making explanation methods report other features as important

### Evaluation Metrics

1. **Feature Importance Ranking**: Does LIME/SHAP report sensitive feature as most important?
2. **Bias Detection Rate**: What percentage of truly biased models are correctly identified?
3. **Robustness Score**: How consistent are results across different random configurations?
4. **Out-of-Distribution Detection**: Can the method flag when a test instance doesn't match training data distribution?

### Results [Exact figures unavailable — see full paper]

- **Single LIME/SHAP**: Can be systematically fooled by adversarial models, reporting spurious features as important
- **Simple Ensembles**: Moderate improvement through voting or averaging
- **Optimized Ensemble Configurations**: Identify configurations that substantially improve bias detection rates while maintaining consistency
- **Out-of-Distribution Samples**: Flagged as high-risk, recommendations to human auditors for additional scrutiny
- **Cross-Dataset Generalization**: Ensemble configurations that work well on COMPAS also show robustness on other fairness benchmarks

### Limitations Discussed in Paper

1. **Computational Cost**: Ensemble approaches require multiple explanations, increasing computational overhead
2. **Configuration Selection**: Optimal ensemble configuration may vary by domain and bias type
3. **Still Model-Agnostic**: Does not use internal model architecture or training data, limiting detection of sophisticated attacks
4. **Adversary Awareness**: An adversary knowing the defense mechanism could potentially design stronger attacks
5. **Human-in-Loop Required**: Framework recommends flagging uncertain cases for human review rather than fully automatic bias detection

## Practical Applications & Real-World Use Cases

### 1. Criminal Justice and Recidivism Prediction

**Application**: Risk assessment algorithms in sentencing and parole decisions (e.g., COMPAS in US courts)

**Problem**: Models may appear non-discriminatory through standard auditing but conceal racial bias in decision-making

**Solution**: SHLIME ensemble configurations can reliably detect when recidivism models are using protected characteristics, even when standard explanations report other features as important

**Regulatory Relevance**: Addresses concerns in US state regulations (Wisconsin, Kentucky) that mandate explainability of criminal risk assessment algorithms

### 2. Credit Scoring and Lending

**Application**: Automated credit decisions, loan approval, interest rate determination

**Problem**: Lending discrimination is illegal under Fair Lending laws, but explaining models through LIME/SHAP could miss subtle discrimination patterns

**Solution**: Ensemble-based explanation auditing provides more robust fairness assessment before deploying models in production

**Regulatory Relevance**: Complies with Equal Credit Opportunity Act (ECOA) requirements for fair lending practices; supports Fair Lending audits

### 3. Healthcare and Medical AI

**Application**: Diagnostic support systems, treatment recommendation, patient risk stratification

**Problem**: Medical devices must be auditable and explainable for FDA approval; biased explanations could mask healthcare disparities

**Solution**: SHLIME framework ensures healthcare AI auditing is more robust against adversarial concealment of treatment bias based on protected characteristics

**Regulatory Relevance**: FDA guidance on software as a medical device (SaMD) increasingly requires explainability; SHLIME improves audit robustness

### 4. Employment Screening and Hiring

**Application**: Automated resume screening, candidate ranking, hiring decision support

**Problem**: Employment discrimination law (Title VII) prohibits decisions based on protected characteristics; explanations alone don't guarantee detection

**Solution**: Ensemble explanation methods flag potentially discriminatory hiring models with higher reliability

**Regulatory Relevance**: Equal Employment Opportunity Commission (EEOC) guidance on algorithmic discrimination detection

### 5. Insurance Underwriting

**Application**: Risk assessment for insurance pricing and coverage decisions

**Problem**: Fair Insurance Practices Acts require non-discrimination, but traditional explanations may miss subtle bias

**Solution**: Ensemble-based auditing provides more robust fairness assessment

## Insights & Implications

### 1. Trustworthiness Requires Robustness

The paper demonstrates that explainability alone is insufficient for trustworthy AI:
- Even transparent explanations can be systematically manipulated
- Robustness of explanations matters as much as their interpretability
- Auditing procedures must assume adversarial scenarios

### 2. Ensemble Methods as Defense Mechanism

This is an underexplored direction in XAI:
- Just as ensemble learning improves model performance, ensemble explanations improve explanation robustness
- Diversity in explanation methods strengthens overall auditing
- Simple averaging/voting can provide meaningful improvements

### 3. Out-of-Distribution Detection as XAI Component

The framework highlights that explanation uncertainty (disagreement across ensemble members) is a valuable auditing signal:
- High explanation disagreement indicates potential vulnerabilities
- Out-of-distribution test instances need human review
- Uncertainty quantification in explanations matters for governance

### 4. Limitations of Post-Hoc Approaches

The paper reinforces fundamental limitations:
- Post-hoc methods cannot definitively prove a model isn't using protected features
- They rely on correlation structure in data, which adversaries can manipulate
- Inherently interpretable models may provide stronger guarantees than post-hoc auditing

### 5. Practical Governance Implications

For AI governance and compliance:
- Explainability alone cannot satisfy fairness requirements
- Ensemble-based auditing provides a practical middle ground between single-method audits and full model transparency
- Human-in-loop review of flagged instances remains necessary
- Configuration selection requires domain expertise and validation on representative test sets

## Code & Resources

### Official Implementation

- **GitHub Repository**: [To be confirmed from paper — check arXiv page]
- **Framework Status**: Academic research code (may require Python/scikit-learn environment)

### Dependencies

- Python 3.8+
- scikit-learn (for LIME and ensemble classifier implementations)
- SHAP library (for Shapley value computations)
- NumPy, Pandas (for data manipulation)
- Matplotlib (for visualization of explanations)

### Computational Requirements

- **CPU**: Sufficient for small-to-medium datasets (up to ~100K samples)
- **Memory**: 8GB+ recommended for larger feature spaces
- **Runtime**: Ensemble approaches are slower than single explanations (multiple LIME/SHAP runs required)

### Quick Start Guide

While the paper doesn't provide full code, the methodology is straightforward to implement:

1. Train a classifier on your fairness-critical domain
2. Generate LIME explanations with multiple random seeds
3. Generate SHAP explanations with multiple hyperparameter configurations
4. Aggregate importance scores through voting or averaging
5. Compare ensemble results vs. single-method results
6. Flag instances where ensemble members strongly disagree
7. Have human auditors review flagged instances for potential bias

### Interactive Demonstrations

The paper includes comparisons on COMPAS, Communities and Crime, and German Credit datasets. Researchers interested in reproducing results can:
- Download public versions of these datasets
- Implement ensemble logic in scikit-learn/SHAP
- Compare against single-method baselines

## Related Work & Context

### Foundation: The Original Adversarial Attack (2019)

"Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods" (Slack et al., 2019) first demonstrated that LIME and SHAP could be fooled by adversarially-constructed models. SHLIME builds directly on this finding by proposing defenses.

### Related Robustness Research

1. **Adversarial Explanations**: Other papers explore adversarial robustness of explanation methods (e.g., using evasion attacks)
2. **Certified Explanations**: Research on providing formal guarantees about feature importance
3. **Interpretation Attacks**: Broader work on attacking/defending interpretability methods

### Connection to XAI Communities

**LIME and SHAP Ecosystem**:
- This paper strengthens confidence in LIME/SHAP by addressing known vulnerabilities
- Complements other LIME/SHAP improvements (e.g., better kernel weighting, sampling strategies)
- Provides practical guidance for practitioners deploying LIME/SHAP in fairness audits

**Fairness-Aware ML Community**:
- Bridges explainability and fairness communities
- Practical application of fairness concepts (bias detection) using explanation tools
- Demonstrates that fairness auditing requires multiple complementary methods

**Mechanistic Interpretability Connection**:
- While SHLIME is post-hoc, it relates to mechanistic interpretability concerns:
  - If models can hide biases through explanation attacks, transparency requires looking beyond explanations
  - Internal model mechanisms (not just predictions/explanations) matter for true interpretability

### Future Research Directions

1. **Certified Ensemble Explanations**: Can we provide formal robustness guarantees for ensemble approaches?
2. **Adaptive Adversaries**: What happens when adversaries specifically target ensemble defenses?
3. **Model-Agnostic Improvements**: Can we design explanation methods inherently robust to adversarial manipulation?
4. **Inherently Interpretable Alternatives**: When might switching to glass-box models be preferable to post-hoc auditing?
5. **Uncertainty Quantification**: How can we better quantify explanation uncertainty in governance contexts?

### Broader Implications for Post-Hoc Explanations

This work is part of a growing recognition that post-hoc explanation methods have fundamental limitations:
- They cannot prove what a model is using, only what correlates with predictions
- Adversarial manipulation of data/models can fool explanations
- Ensemble and robustness approaches are a practical improvement but not a complete solution
- Governance and compliance may require layered approaches combining post-hoc, mechanistic, and inherently-interpretable methods

## References & Further Reading

- **Original LIME Paper**: Ribeiro et al., "Why Should I Trust You?" (2016)
- **Original SHAP Paper**: Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions" (2017)
- **Original Adversarial Attack**: Slack et al., "Fooling LIME and SHAP" (2019)
- **Related Robustness Work**: See comprehensive survey on explanation method robustness in XAI literature

---

**Paper Link**: [SHLIME on arXiv (2508.11053)](https://arxiv.org/abs/2508.11053)

**How to Cite**: Sam Chauhan, Estelle Duguet, Karthik Ramakrishnan, Hugh Van Deventer, Jack Kruger, Ranjan Subbaraman. "SHLIME: Foiling adversarial attacks fooling SHAP and LIME." arXiv preprint arXiv:2508.11053 (2025).
