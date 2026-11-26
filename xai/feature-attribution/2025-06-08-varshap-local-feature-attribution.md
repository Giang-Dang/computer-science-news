# VARSHAP: Addressing Global Dependency Problems in Explainable AI with Variance-Based Local Feature Attribution

**ArXiv ID:** [2506.07229](https://arxiv.org/abs/2506.07229)

**Authors:** Mateusz Gajewski, Mikołaj Morzy, Adam Karczmarz, Piotr Sankowski

**Submission Date:** June 8, 2025

**Primary Source:** Gajewski, M., Morzy, M., Karczmarz, A., & Sankowski, P. (2025). VARSHAP: Addressing global dependency problems in explainable AI with variance-based local feature attribution. *arXiv:2506.07229*.

---

## Executive Summary

VARSHAP is a novel model-agnostic local feature attribution method that addresses a critical limitation in existing feature importance techniques: their susceptibility to global data distribution shifts. By grounding feature importance in prediction variance reduction rather than raw prediction changes, VARSHAP provides more stable and locally faithful explanations while maintaining the theoretical rigor of the Shapley value framework. This work advances the state-of-the-art in feature attribution by offering practitioners a more robust alternative to SHAP and LIME for understanding local model behavior.

---

## Problem Statement

### Limitations of Existing Feature Attribution Methods

Feature attribution methods like **SHAP (SHapley Additive exPlanations)** and **LIME (Local Interpretable Model-agnostic Explanations)** have become fundamental tools in explainable AI. However, they suffer from significant limitations:

1. **Global Dependency Problem**: SHAP's attributions often depend heavily on the global data distribution. When a model's underlying distribution shifts (e.g., due to domain adaptation, data drift, or class imbalance), SHAP values can change dramatically, even when the local model behavior at a specific point remains relatively stable.

2. **Failure to Capture Local Behavior**: Both SHAP and LIME can fail to accurately capture the true local sensitivity of a model at specific input points. Their global context can obscure which features actually matter locally.

3. **Instability Under Distribution Shift**: In scenarios with heterogeneous data distributions or when dealing with imbalanced datasets, conventional attribution methods may produce inconsistent explanations.

4. **Limited Robustness**: LIME and SHAP exhibit varying robustness properties, particularly in the presence of slight input perturbations, making them unreliable for safety-critical applications.

### Why This Matters

In practice, practitioners need explanations that:
- Remain stable when the data distribution changes
- Truly reflect local model behavior at the point being explained
- Provide robust and consistent attributions across similar inputs
- Maintain theoretical guarantees (like Shapley axioms)

SHAP's global dependence means its explanations can be misleading precisely when you most need reliable, localized insights—when your data or deployment context shifts away from the training distribution.

---

## Core Concepts & Theory

### Shapley Values: Foundation and Limitation

The **Shapley value** is a concept from cooperative game theory that provides a theoretically sound way to fairly distribute a payoff among players. In the context of feature attribution:
- Each feature is a "player"
- The model's prediction on a sample is the "payoff"
- Shapley values decompose the prediction into per-feature contributions

The Shapley value φ_i for feature i satisfies four desirable axioms:
1. **Efficiency**: Contributions sum to the prediction (minus baseline)
2. **Symmetry**: Interchangeable features receive equal attribution
3. **Dummy (Null Player)**: Features that don't influence predictions get zero attribution
4. **Additivity**: For combined games, attributions combine linearly

However, Shapley values are typically computed by marginalizing over all possible coalition orderings, which forces integration over the **global data distribution**. This is where SHAP's global dependency emerges.

### VARSHAP: Variance Reduction as the Core Metric

**Key Innovation**: Instead of measuring feature importance by how much a feature changes the model's prediction, VARSHAP measures how much a feature **reduces prediction variance** under perturbation.

#### Mathematical Formulation

For a feature set S and a point x, the variance-based importance is defined as:

```
V(S, x) = E[Var(ŷ(x, S) | x_S)]
```

where:
- ŷ(x, S) represents predictions when features in S are known and others are sampled
- The variance is computed over the distribution of unknown features
- x_S denotes the known features at point x

The VARSHAP attribution for feature i is then computed as:

```
φ_i^VAR = Σ_{S ⊆ N\{i}} (|N| - |S| - 1)! |S|! / |N|! × [V(S ∪ {i}, x) - V(S, x)]
```

This follows the Shapley framework but uses variance reduction instead of prediction change.

#### Why Variance?

The authors argue from first principles that **variance is the only metric satisfying intuitive and desirable axioms for local feature attribution**:

1. **Locality**: It measures how much a feature reduces local uncertainty, not global impact
2. **Independence**: For additive models with independent features, VARSHAP isolates each feature's true contribution
3. **Stability**: Variance-based measures are inherently more stable under distribution shifts because they depend on local behavior, not global context
4. **Robustness**: Perturbations affecting prediction variance are more fundamental than those affecting raw predictions

### Relationship to SHAP and LIME

| Aspect | SHAP | LIME | VARSHAP |
|--------|------|------|---------|
| **Framework** | Shapley values | Local linear approximation | Shapley values |
| **Importance Metric** | Prediction change | Local regression weight | Variance reduction |
| **Model Agnostic** | Yes | Yes | Yes |
| **Global Dependence** | High (integrates over data distribution) | Moderate (depends on sampling) | Low (focuses on local variance) |
| **Axioms** | Satisfies Shapley axioms | No formal axioms | Satisfies Shapley axioms + robustness |
| **Computational Cost** | Moderate to high | Low to moderate | Moderate |

---

## Main Ideas & Key Contributions

### 1. **Theoretical Contribution: Variance as the Right Metric**
The paper makes a principled theoretical argument that variance reduction, not prediction change, is the appropriate measure of feature importance in a local context. This is backed by an axiomatic framework showing that variance is the unique metric satisfying desirable properties for local interpretability.

### 2. **Practical Algorithm: Variance-Based Shapley Computation**
VARSHAP provides a computationally tractable algorithm to compute variance-based Shapley values. The method is model-agnostic, requiring only access to the model's predictions.

**Algorithm Steps**:
1. For a point x to explain, define features as "known" (those being explained) and "unknown"
2. For different subsets S of unknown features, compute the variance of predictions as unknown features are sampled
3. Use Shapley decomposition to attribute the total variance reduction to individual features
4. Approximate using Monte Carlo sampling when exact computation is intractable

### 3. **Robustness to Distribution Shift**
VARSHAP is inherently resilient to changes in the global data distribution. Because it measures local variance rather than global prediction changes, it remains stable when:
- The data distribution shifts (domain adaptation)
- Class imbalance changes
- Population demographics change

### 4. **Linear Model Special Case**
For additive models with independent features, VARSHAP reduces to a closed-form solution where each feature's attribution precisely equals its contribution to the output variance. This provides an interpretable baseline and theoretical validation.

### 5. **Empirical Validation on Robustness**
The paper demonstrates that VARSHAP variants significantly outperform SHAP (KernelSHAP) and LIME in robustness metrics, particularly:
- **LocalLipschitzEstimate**: Lower variance in explanations under small input perturbations
- **MaxSensitivity**: Reduced maximum change in attributions
- **RelativeInputStability**: More stable across similar inputs

---

## Methodology & Implementation

### Experimental Setup

**Models Tested**: Neural networks and other black-box classifiers across various architectures

**Evaluation Framework**: The paper employs a comprehensive evaluation suite inspired by LATEC (Local Explainability Testing and Comparison), including:

#### Faithfulness Metrics
- **FaithfulnessCorrelation**: How well feature removal correlates with attribution magnitude
- **FaithfulnessEstimate**: Direct measure of explanation faithfulness
- **MonotonicityCorrelation**: Whether more important features show monotonic increase in importance

#### Robustness Metrics
- **LocalLipschitzEstimate**: Stability of explanations under small input perturbations
- **MaxSensitivity**: Maximum change in feature attributions under perturbation
- **RelativeInputStability**: Relative stability across similar input samples

#### Complexity Metrics
- **Sparseness**: Whether important features form a sparse set
- **Complexity**: Overall complexity of explanation
- **EffectiveComplexity**: Complexity weighted by feature importance

### Experimental Results

**Comparative Performance** (median ranks across all metrics; lower is better):

| Method | Mean Rank | Rank Range | Specialization |
|--------|-----------|-----------|-----------------|
| VARSHAP (σ=0.6) | 3.39 | σ=0.6 | Strong robustness |
| VARSHAP (σ=1.0) | 3.64 | σ=1.0 | Balanced |
| KernelSHAP | 4.86 | Variable | Moderate faithfulness |
| LIME | 5.51-5.81 | High variance | Weak across metrics |

**Key Findings**:

1. **Robustness Excellence**: VARSHAP variants consistently rank top in robustness metrics, indicating stable explanations under input perturbations [Exact figures unavailable — see full paper]

2. **Faithfulness Competitive**: While KernelSHAP may lead on specific faithfulness metrics (e.g., FaithfulnessCorrelation), VARSHAP is competitive overall and leads in MonotonicityCorrelation

3. **Consistency Across Datasets**: Unlike SHAP, VARSHAP provides consistent attribution values across different data distributions. Example: for the test point [0,0], VARSHAP and LIME provided stable values across two datasets, while SHAP showed inconsistency

4. **Stability Under Perturbation**: VARSHAP's variance-based approach yields significantly more stable explanations when inputs are slightly perturbed, crucial for real-world deployment

### Implementation Considerations

**Approximation Methods**:
- Monte Carlo sampling for intractable exact computations
- Coalition sampling for efficiency in high-dimensional settings

**Computational Complexity**:
- Similar to SHAP (O(2^n) in exact form for n features)
- Practical approximations scale better with high-dimensional data

**Model Requirements**:
- Black-box access only (predictions required)
- No model-specific assumptions
- Works with neural networks, tree ensembles, linear models, etc.

---

## Practical Applications & Real-World Use Cases

### 1. **Healthcare and Clinical Decision Support**
- **Challenge**: Models making treatment recommendations must be stable across patient populations with different demographics, comorbidities, and regional factors
- **VARSHAP Solution**: Provides consistent explanations for which features (symptoms, test results, vital signs) drive predictions, even when patient demographics shift
- **Regulatory Benefit**: FDA and clinical governance bodies require robust, stable explanations for critical decisions; VARSHAP's theoretical guarantees provide stronger evidence

### 2. **Credit Risk and Loan Underwriting**
- **Challenge**: Financial institutions must explain credit decisions consistently across economic cycles and changing market conditions
- **VARSHAP Solution**: Attribution values remain stable as economic conditions shift, reducing claims of unfair lending practices due to shifting model explanations
- **Compliance**: Satisfies interpretability requirements under GDPR Right to Explanation and Fair Lending laws

### 3. **Autonomous Systems and Safety-Critical Applications**
- **Challenge**: Self-driving vehicles, medical robots, and autonomous systems must provide reliable, stable explanations of decisions under varying environmental conditions
- **VARSHAP Solution**: Robust attributions ensure that explanations of safety-critical actions don't fluctuate with minor environmental changes
- **Certification**: Facilitates certification and audit trails required for deployment

### 4. **Fraud Detection and Anomaly Detection**
- **Challenge**: Detection models must adapt to evolving fraud patterns while maintaining stable explanations
- **VARSHAP Solution**: Distinguishes between legitimate model adaptation (evolving fraud detection) and unstable explanations, providing analysts with clearer signals
- **Interpretability**: Security teams get consistent insights into which features trigger fraud alerts

### 5. **Domain Adaptation and Transfer Learning**
- **Challenge**: Models deployed in new domains may have shifted feature distributions; practitioners need to understand what changed
- **VARSHAP Solution**: VARSHAP's local variance focus reveals which features are truly important in the new domain, independent of global distribution shifts
- **Debugging**: Helps identify overfitting or inappropriate feature shifts when models underperform in new domains

### 6. **Model Monitoring and Data Drift Detection**
- **Challenge**: Detecting when model behavior has changed requires stable explanations as a baseline
- **VARSHAP Solution**: Sudden changes in VARSHAP attributions (but not SHAP) can indicate genuine model behavior changes rather than distribution shifts
- **Operations**: Improves alert quality and reduces false positives in model monitoring systems

---

## Insights & Implications

### Theoretical Insights

1. **Locality Beats Globality for Interpretability**: The paper demonstrates that focusing on local variance rather than global prediction changes yields more meaningful, stable explanations. This challenges the dominance of globally-integrated approaches in explainability.

2. **Variance as a Fundamental Concept**: By establishing variance reduction as the axiomatic foundation for local attribution, the work elevates interpretability from heuristic to principled science.

3. **Shapley Values Can Be Localized**: The work shows that Shapley values, traditionally defined with respect to a global distribution, can be meaningfully adapted to local contexts while maintaining their theoretical properties.

### Implications for XAI Research

1. **Moving Beyond SHAP**: While SHAP is powerful, this work highlights that one-size-fits-all approaches have limitations. Future XAI may benefit from multiple attribution methods for different contexts (global influence vs. local robustness).

2. **Robustness as a Design Principle**: VARSHAP elevates robustness to design principle rather than afterthought. Future interpretability methods should prioritize stability under realistic deployment conditions.

3. **Distribution Shift Awareness**: The xAI community should systematically evaluate methods' behavior under distribution shift, following VARSHAP's example.

### Limitations and Open Questions

1. **Computational Overhead**: VARSHAP's variance computation adds overhead compared to simple LIME. For real-time applications, approximation quality vs. speed trade-offs need careful tuning.

2. **Interpretability of Variance**: While variance is theoretically principled, practitioners may find it less intuitive than SHAP's "if feature wasn't there" framing. Communication challenges remain.

3. **Non-Additive Models**: Like all additive attribution methods, VARSHAP may struggle with highly non-additive feature interactions. The variance metric may not capture these well.

4. **High-Dimensional Scaling**: As feature dimension increases, approximation quality may degrade. Research needed on efficient scaling to 10,000+ feature settings.

5. **Baseline Selection**: Like other local methods, VARSHAP requires defining what "perturbation distribution" to sample from. Principled baseline selection remains an open problem.

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [2506.07229 - Full PDF](https://arxiv.org/pdf/2506.07229)
- **ArXiv HTML**: [Interactive HTML Version](https://arxiv.org/html/2506.07229v1)
- **Alternative Rendering**: [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2506.07229)

### Implementation and Related Tools

**Related Methods**:
- **SHAP (Shapley Additive exPlanations)**: [Python package](https://github.com/shap/shap) - Foundational global Shapley value method
- **LIME (Local Interpretable Model-agnostic Explanations)**: [GitHub](https://github.com/marcotcr/lime) - Local linear approximation method
- **FastSHAP**: [GitHub](https://github.com/iancovert/fastshap) - Efficient Shapley value approximation
- **LATEC Framework**: Referenced evaluation framework for local explainability metrics

### Computational Requirements

Based on the paper's methodology:
- **Language**: Likely Python (standard for ML research)
- **Dependencies**: NumPy, SciPy for mathematical operations; PyTorch or TensorFlow for model evaluation
- **Hardware**: Standard CPU sufficient for small-to-medium datasets; GPU recommended for large-scale experiments
- **Memory**: Moderate (comparable to SHAP implementations)
- **Training/Computation Time**: Similar to KernelSHAP for approximation-based approaches [Exact figures unavailable — see full paper]

### Deployment Considerations

1. **Installation**: Code availability pending author release (check ArXiv or GitHub upon publication)
2. **Model Integration**: Model-agnostic, works with any predictive model (sklearn, TensorFlow, PyTorch, XGBoost, etc.)
3. **Scalability**: Approximation algorithms enable scaling to moderate dimensions; exact computation limited by exponential coalition space
4. **Parameter Tuning**: 
   - σ (perturbation std dev): Controls explanation variance; paper explores σ=0.6, 1.0
   - Sampling strategy: Number of coalitions for Monte Carlo approximation
   - Baseline distribution: How to sample "unknown" features

---

## Related Work & Context

### Position in the XAI Landscape

VARSHAP sits at the intersection of several important xAI traditions:

1. **Shapley-Based Methods**: Inherits the theoretical rigor of SHAP while addressing its global dependency problem
2. **Local Interpretability**: Aligns with LIME's focus on local behavior but with stronger theoretical guarantees
3. **Robustness-Aware XAI**: Part of a growing trend emphasizing explanation stability and reliability

### Related Papers and Connections

**Foundation and Critique**:
- **SHAP (Lundberg & Lee, 2017)**: Seminal work on Shapley-based explanations; VARSHAP builds on but critiques its global nature
- **LIME (Ribeiro et al., 2016)**: Local linear approximations; VARSHAP competes directly on robustness
- **Evaluating Local Explainability Metrics**: Related 2026 work on benchmarking local explainability methods

**Complementary Directions**:
- **WeightedSHAP (2022)**: Another approach to improving SHAP; offers different trade-offs than VARSHAP
- **Fairness in Attribution**: How to ensure feature attributions are fair across demographics; VARSHAP's stability helps here
- **XAI Benchmarking**: Growing literature on evaluating explanation methods (e.g., XAI-Arena framework)

### Broader Research Communities

1. **Local Interpretability Community**: VARSHAP contributes to understanding what "local" should mean and how to achieve it rigorously

2. **Robustness in ML**: Connects to broader literature on model robustness and adversarial examples; interpretability should be robust like predictions

3. **Causal Interpretability**: While VARSHAP is non-causal, its local variance focus aligns with causal approaches' emphasis on what actually matters for a specific instance

4. **Model Monitoring and MLOps**: Practical adoption likely in production ML monitoring pipelines, alongside other explainability tools

### Future Research Directions

1. **Variance-Based Causal Attribution**: Combining variance perspective with causal inference for even richer explanations

2. **Interactive Explanations**: Using VARSHAP's local variance to guide users toward feature combinations that most affect predictions

3. **Adversarial Robustness**: Testing VARSHAP against adversarial examples to validate claimed robustness

4. **Dimension Reduction**: Applying dimensionality reduction before VARSHAP for high-dimensional data

5. **Temporal Dynamics**: Extending VARSHAP to time-series data and sequential decisions

6. **Multi-Task Learning**: How VARSHAP behaves in multi-task settings where features matter differently for different targets

---

## Conclusion

VARSHAP represents a meaningful advance in feature attribution by grounding local interpretability in the intuitive notion of variance reduction rather than global prediction changes. By maintaining Shapley value axioms while focusing on local robustness, it offers practitioners a theoretically principled and empirically robust alternative to SHAP and LIME.

The paper's key contribution—establishing that variance, not prediction change, is the right metric for local feature attribution—opens new research directions in locally-grounded, distribution-robust explainability. For practitioners in safety-critical domains, healthcare, finance, and ML operations, VARSHAP's robustness to distribution shift and stability under perturbation address real-world pain points that SHAP and LIME leave unresolved.

As the ML community increasingly recognizes that explanations must be as robust as predictions, VARSHAP positions variance-based methods at the frontier of trustworthy, interpretable AI.

---

## References

1. Gajewski, M., Morzy, M., Karczmarz, A., & Sankowski, P. (2025). VARSHAP: Addressing global dependency problems in explainable AI with variance-based local feature attribution. *arXiv:2506.07229*.

2. Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *NeurIPS* (pp. 4765–4774).

3. Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?" Explaining the predictions of any classifier. In *KDD* (pp. 1135–1144).

4. Evaluating Local Explainability Metrics for Machine Learning Models. (2026). *arXiv:2605.27618*.

5. XAI-Arena: Can LLMs Assess the Quality of XAI Explanations? *arXiv:2609.09428*.

6. Beyond single-model XAI: aggregating multi-model explanations for enhanced trustworthiness. *arXiv:2510.11164*.

---

## Appendix: Quick Reference

**Paper Identity**: VARSHAP | arXiv:2506.07229 | June 2025
**xAI Subfield**: Feature Attribution / Local Interpretability
**Key Metric**: Variance Reduction
**Main Competition**: SHAP, LIME
**Theoretical Framework**: Shapley Values + Local Variance
**Practical Strength**: Robustness under distribution shift
**Limitations**: Interpretability of variance metric, computational overhead, high-dimensional scaling
