# MIRA: A Score for Conditional Distribution Accuracy and Model Comparison

**ArXiv ID:** [2605.02014](https://arxiv.org/abs/2605.02014)  
**Authors:** Sammy Sharief, Justine Zeghal, Gabriel Missael Barco, Pablo Lemos, Yashar Hezaveh, Laurence Perreault-Levasseur  
**Date:** May 3, 2026  
**Field:** Machine Learning / Statistics

---

## Executive Summary

MIRA (Mass In Random Areas) is a novel sample-based scoring method for evaluating the accuracy of conditional probability distributions. It enables model comparison through direct posterior validation without computing intractable evidence, addressing a critical bottleneck in Bayesian inference and probabilistic modeling.

## Problem Statement

**Challenges in Model Evaluation:**

1. **Conditional Distribution Assessment:** Given only joint samples from a data-generating process, how can we evaluate whether a candidate conditional distribution accurately captures the true conditional distribution?

2. **Bayesian Model Comparison:** Computing model evidence (marginal likelihood) is computationally intractable for most realistic models, making standard Bayesian model comparison infeasible.

3. **Existing Limitations:**
   - Likelihood-based metrics only work when the model explicitly computes likelihoods
   - Evidence computation requires nested sampling or other expensive methods
   - No principled way to compare models when both model and ground truth are known only through samples

**Why This Matters:**
- Critical for evaluating generative models, variational autoencoders, and other complex probabilistic systems
- Enables systematic model comparison and hyperparameter selection
- Supports validation of learned distributions in scientific inference tasks

## Core Concepts & Theory

### Theoretical Foundation

**Principle of Distribution Equivalence:**
Two distributions are identical if and only if they assign equal probability mass to all regions of the sample space.

**MIRA Formulation:**
The MIRA statistic leverages this principle by evaluating probability mass in random regions:

1. **Random Region Selection:** Select a random region R from some reference distribution
2. **Mass Calculation:** Compute:
   - Probability mass assigned by candidate distribution: P_candidate(R)
   - Empirical probability mass from true data: P_true(R)
3. **Comparison:** Measure discrepancy between these masses

### Mathematical Framework

**MIRA Score Definition:**

For a candidate distribution q(·|x) and true samples {y_i}:

1. **Single Sample Evaluation:**
   - Generate random region R
   - Compute MIRA statistic: Δ = |P_q(R|x) - P_true(R|x)|

2. **Aggregated Score:**
   - Average MIRA statistic over multiple random regions and samples
   - Produces a scalar score where lower values indicate better distribution matching

### Key Properties

1. **Unbiased Estimation:** When candidate distribution matches true distribution, expected MIRA statistic is zero
2. **Uncertainty Quantification:** Provides confidence intervals and uncertainty estimates
3. **Sample Efficiency:** Works with finite samples without requiring asymptotic assumptions
4. **Theoretical Grounding:** Derived from fundamental principle of distribution equivalence

## Main Ideas & Key Contributions

### Core Contributions

1. **Novel Evaluation Metric:** MIRA provides first principled sample-based score for conditional distribution accuracy
2. **Practical Bayesian Model Comparison:** Enables model comparison through posterior validation, bypassing evidence computation
3. **Theoretical Guarantees:** Establishes theoretical properties and reference values for validation
4. **Broad Applicability:** Works with any probabilistic model that can generate samples

### Technical Innovations

1. **Reference Value Computation:** 
   - Derives analytical expressions for MIRA statistics
   - Establishes theoretical reference values when candidate matches true distribution
   - Enables hypothesis testing framework

2. **Uncertainty Quantification:**
   - Provides error bars and confidence intervals
   - Accounts for finite sample effects
   - Supports significance testing

3. **Computational Efficiency:**
   - Avoids expensive nested sampling
   - Scales well with dimension and sample size
   - Suitable for high-dimensional problems

## Methodology & Implementation

### Experimental Setup

**Benchmark Tasks:**

1. **Toy Problems:**
   - Gaussian distributions with known parameters
   - Simple mixture models
   - Controlled ground truth for validation

2. **Bayesian Inference Tasks:**
   - Bayesian linear regression
   - Hierarchical models
   - Posterior distribution evaluation

3. **Generative Model Evaluation:**
   - Variational autoencoders
   - Flow-based models
   - Other probabilistic models

### Key Results

**Validation on Toy Problems:**
- MIRA correctly identifies when distributions match
- Produces expected reference values matching theory
- Uncertainty estimates align with empirical variability

**Bayesian Model Comparison:**
- Consistent rankings with evidence-based methods (when computable)
- Superior computational efficiency
- Enables comparison of otherwise intractable models

**Scalability:**
- Works well in moderate to high dimensions
- Computation time grows linearly with sample size
- Suitable for real-world applications

### Implementation Details

**Algorithm:**
```
Input: 
  - Candidate distribution q(·|x)
  - True samples {y_i}
  - Number of random regions N
  
For each region R:
  - Draw region from reference distribution
  - Compute P_q(R|x)
  - Estimate P_true(R|x) from samples
  - Calculate MIRA statistic
  
MIRA_score = mean(|MIRA statistics|)
```

## Practical Applications & Real-World Use Cases

### Machine Learning Applications

1. **Generative Model Evaluation:**
   - Assess quality of VAE latent distributions
   - Compare different generative model architectures
   - Validate normalizing flows and autoregressive models

2. **Bayesian Neural Networks:**
   - Evaluate posterior approximations in variational inference
   - Compare different approximate inference schemes
   - Quantify posterior approximation quality

3. **Uncertainty Quantification:**
   - Validate uncertainty estimates in regression models
   - Assess confidence calibration in classification
   - Compare different uncertainty quantification methods

### Scientific Applications

1. **Parameter Inference:**
   - Bayesian inference in physics and astronomy
   - Validate learned posterior distributions
   - Compare inference methods without expensive evidence computation

2. **Model Selection:**
   - Choose between competing scientific models
   - Rank hypotheses based on posterior validation
   - Provide quantitative model comparison metrics

### Practical Advantages

1. **Computational:** Avoids expensive nested sampling or similar methods
2. **Practical:** Works with only samples, doesn't require likelihood computation
3. **Interpretable:** Provides intuitive scores and uncertainty estimates
4. **Flexible:** Applies to any probabilistic model

## Insights & Implications

### Theoretical Advances

1. **New Evaluation Framework:** Establishes principled approach to conditional distribution assessment
2. **Connection to Distribution Theory:** Links practical evaluation to fundamental principles of probability
3. **Bayesian Inference:** Enables practical Bayesian model comparison for complex models

### Implications for the Field

1. **Democratizing Bayesian Inference:** Makes Bayesian model comparison tractable for more practitioners
2. **Improving Generative Models:** Provides tools for systematic evaluation and comparison of generative models
3. **Scientific Inference:** Enables rigorous Bayesian inference in domains where evidence computation is intractable

### Limitations & Open Questions

1. **Region Selection:** Choice of reference distribution for regions affects results; systematic guidance needed
2. **Dimension Scalability:** While tested in moderate dimensions, extreme high-dimensional behavior unclear
3. **Computational Overhead:** Random region generation may be expensive for certain distributions
4. **Theoretical Bounds:** Finite-sample convergence rates could be characterized more precisely

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2605.02014](https://arxiv.org/abs/2605.02014)
- **HTML Version:** [https://arxiv.org/html/2605.02014](https://arxiv.org/html/2605.02014)
- **Official Implementation:** Expected to be released by authors
- **Documentation:** Full mathematical details in paper appendices

### Requirements

- NumPy/PyTorch for numerical computation
- Probabilistic programming framework (PyMC, Stan, or similar) for comparison
- Standard scientific computing stack

### Installation & Usage

Expected basic usage:
```python
from mira import compute_mira_score

score = compute_mira_score(
    candidate_distribution=q,
    true_samples=data,
    num_regions=1000
)
```

## Related Work & Context

### Prior Work on Distribution Evaluation

1. **Likelihood-Based Metrics:** Maximum likelihood, log-likelihood
2. **Distance Metrics:** Wasserstein distance, Maximum Mean Discrepancy
3. **Evidence Computation:** Nested sampling, thermodynamic integration

### Connection to Broader Research

1. **Bayesian Model Comparison:** Part of ongoing effort to make Bayesian inference more practical
2. **Generative Model Evaluation:** Complements existing metrics like FID, IS for image generation
3. **Probabilistic Inference:** Connects to research on variational inference and approximate Bayesian computation

### Potential Future Directions

1. **Adaptive Region Selection:** Learn optimal region distributions for better sensitivity
2. **Dimension-Adaptive Methods:** Develop techniques for extreme high dimensions
3. **Conditional Independence Testing:** Extend framework for testing conditional independence structures
4. **Online/Streaming Evaluation:** Adapt for streaming or online model comparison scenarios
5. **Comparison Bounds:** Establish finite-sample bounds for MIRA-based model selection

---

## Summary

MIRA provides a principled and practical solution to a fundamental problem in probabilistic machine learning: evaluating conditional distributions when only samples are available. By avoiding expensive evidence computation while maintaining theoretical guarantees, it enables systematic Bayesian model comparison and evaluation of generative models. This work has significant implications for making Bayesian inference and probabilistic modeling more practical and accessible.
