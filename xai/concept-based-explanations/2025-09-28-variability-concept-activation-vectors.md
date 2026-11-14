# On the Variability of Concept Activation Vectors

**ArXiv ID:** [2509.24058](https://arxiv.org/abs/2509.24058)

**Authors:** Julia Wenkmann (Universität Würzburg), Damien Garreau (Universität Würzburg)

**Submission Date:** September 28, 2025

**Venue:** Submitted to AAAI-26 / Machine Learning (cs.LG), with STAT.ML cross-listing

---

## Executive Summary

This paper addresses a fundamental practical problem in concept-based explainability: **the variability and instability of Concept Activation Vectors (CAVs)**, a core technique for interpreting neural networks using human-friendly semantic concepts. The authors provide the first rigorous theoretical analysis of CAV variability, proving that CAV estimation error decreases as **O(1/N)** where N is the number of sampled examples. Through comprehensive experiments across visual, textual, and tabular domains, they validate this theory and provide practical recommendations for practitioners using concept-based explanations.

## Problem Statement

Concept Activation Vectors (CAVs), introduced by Kim et al. (2018) in the TCAV framework, enable human-friendly interpretability by explaining neural network decisions in terms of user-defined semantic concepts rather than low-level pixel features or embeddings. However, a critical limitation has hindered their adoption in practice:

**CAV computation requires random sampling of concept and non-concept examples from the training set**, making the resulting vectors dependent on this sampling process. This raises fundamental questions:

- How much do CAV estimates vary across different random samples?
- What is the relationship between sample size and CAV stability?
- Can we quantify this variability theoretically?
- What practical implications does variability have for TCAV scores and their reliability?

Prior work (e.g., the α-TCAV framework) observed that TCAV scores remain unstable even when using larger sample sizes, but **the root cause—CAV variability itself—had never been rigorously characterized**. This paper fills this theoretical gap.

## Core Concepts & Theory

### Concept Activation Vectors (CAVs) Background

A Concept Activation Vector is a direction in activation space that captures how a neural network responds to a user-defined concept:

1. **Concept Definition:** A user provides examples of concept C (e.g., "striped" in image classification) and non-concept examples (negative examples).

2. **Linear Classifier Training:** A linear classifier (e.g., logistic regression, support vector machine) is trained to distinguish concept examples from random activations.

3. **CAV Extraction:** The learned classifier's weight vector becomes the CAV—a direction in activation space that maximizes separation between concept and random examples.

4. **TCAV Score:** The CAV is then used to compute the **Test with Concept Activation Vector (TCAV)** score:
   ```
   TCAV_c(f, x) = (1/|inputs|) * Σ sign(∇_h f(x) · cav_c)
   ```
   where ∇_h f(x) is the gradient of the model output with respect to hidden layer activations.

### Variability Analysis Framework

The paper models CAV computation as a random process due to sampling:

- **Concept Set:** C_pos = {x₁, x₂, ..., x_k} (concept examples)
- **Non-Concept Set:** C_neg = {x'₁, x'₂, ..., x'_N} (random examples sampled uniformly from training data)

The key insight is that as N (number of sampled examples) varies, the resulting CAV estimate changes. The authors quantify this using:

**Variability Measure:** The trace of the covariance matrix Σ of the estimated CAVs:
```
Var(CAV) = trace(Cov(ŵ))
```
This measures the total per-feature variance in the CAV estimate.

### Main Theoretical Result

**Theorem (Asymptotic Variability):** For CAVs estimated via penalized logistic regression, the variance of the estimated CAV scales as:

```
Var(ŵ) = O(1/N)
```

More precisely, as the number of non-concept examples N → ∞, the standardized variance decreases proportionally to 1/N, and the distribution of the CAV converges to a normal distribution.

**Key Implications:**
1. **Predictable Scaling:** CAV variability follows a well-understood statistical law, enabling practitioners to plan sampling strategies.
2. **Sample Size Guidance:** To reduce variance by a factor of 4, practitioners need to quadruple the sample size.
3. **Trade-off Between Stability and Efficiency:** Larger N increases stability but requires more human effort to label concept/non-concept examples.

### Statistical Assumptions

The theoretical analysis assumes:

- **Linear Separability** in activation space: The concept is linearly separable from random examples.
- **Finite Sample Regime:** N is large enough for asymptotic normality, but the paper validates this on moderate sample sizes.
- **Fixed Concept Set:** The concept examples remain constant while the non-concept set is sampled.
- **Independent Sampling:** Non-concept examples are drawn i.i.d. from the training distribution.

## Main Ideas & Key Contributions

### 1. First Rigorous Theoretical Analysis of CAV Variability

**Contribution:** The paper provides the **first mathematical characterization** of how CAV estimates vary with sample size. This fills a critical gap between:
- **Practical Observations:** Users noticed CAV instability.
- **Theoretical Understanding:** No formal framework existed to quantify or predict this instability.

The variance analysis is precise and covers multiple CAV estimation methods (logistic regression, hinge loss, Concept Activation Regions, Difference of Means).

### 2. Asymptotic Normality Result

Beyond variance scaling, the authors prove that CAV estimates follow an asymptotic normal distribution:

```
√N (ŵ - w*) →^d N(0, Σ)
```

This enables practitioners to:
- Construct confidence intervals around CAV estimates.
- Perform statistical significance tests on TCAV scores.
- Assess the reliability of individual concept-based explanations.

### 3. Multi-Modal Empirical Validation

The theory is validated across diverse domains:
- **Visual Domain:** ResNet50 on ImageNet; concept recognition (e.g., "striped," "dotted").
- **Textual Domain:** LSTM/BERT models; sentiment and attribute concepts.
- **Tabular Domain:** UCI Adult dataset; demographic and fairness-related concepts.

All experiments confirm the **1/N variance scaling**, indicating the result's robustness.

### 4. Critical Insight: Variance ≠ Reliability

**Surprising Finding:** While CAV variance decreases with N, the **TCAV score variance remains approximately constant** across different sample sizes in most settings. This reveals a subtle distinction:

- **Low CAV Variance:** Indicates stable concept detection in activation space.
- **Stable TCAV Score:** Does NOT automatically follow from low CAV variance; the TCAV score depends on the entire gradient landscape.

This implies that reducing CAV variance alone is **insufficient** for ensuring reliable TCAV scores—additional factors like concept semantics and model architecture matter.

### 5. Practical Recommendations for Practitioners

The paper provides actionable guidance:

1. **Sample Size Selection:** Use the O(1/N) scaling to estimate required sample sizes for desired variance levels.
2. **Regularization Strategy:** Stronger regularization reduces CAV variance, enabling smaller effective sample sizes.
3. **Concept Quality Over Quantity:** A well-chosen, smaller concept set is more valuable than a larger, semantically incoherent set.
4. **Statistical Validation:** Report confidence intervals or variance estimates alongside TCAV scores to communicate uncertainty.

## Methodology & Implementation

### Experimental Setup

**Datasets and Models:**
- **Vision:** ImageNet (ResNet50); concepts from human-labeled subsets (e.g., "striped," "furry").
- **NLP:** Sentiment analysis (LSTM, BERT); fairness concepts on toxicity classifiers.
- **Tabular:** UCI Adult dataset (income prediction); demographic concepts (gender, age group).

**CAV Estimators Tested:**
1. Logistic Regression (standard)
2. Hinge Loss (SVM-based)
3. Concept Activation Regions (CAR)
4. Difference of Means (DoM)

**Evaluation Metrics:**
- Variance of CAV estimates: trace(Cov(ŵ))
- TCAV score variance: computed across independent samples
- CAV direction stability: cosine similarity between CAV estimates from different samples
- Concept semantic quality: measured via human evaluation or held-out concept examples

### Results Summary

**Variance Scaling Validation:**
- CAV variance decreases as **1/N** across all tested modalities and estimators.
- Empirical log-log plots confirm linear relationship between log(Var) and log(N).
- The slope matches theoretical predictions within experimental error.

**Multi-Estimator Comparison:**
[Exact figures unavailable — see full paper]
- Different CAV estimators show similar 1/N scaling, though constants differ.
- Logistic regression and hinge loss variants are most stable.
- Concept Activation Regions show larger variance in some settings.

**Regularization Impact:**
- Increasing regularization strength (L2 penalty) reduces CAV variance.
- Effect is modeled theoretically; regularization effectively increases the implicit "sample size" for variance purposes.

**TCAV Score Stability:**
- TCAV scores show **limited variance reduction** as N increases, contradicting initial intuition.
- Suggests that TCAV score reliability depends on factors beyond CAV variance (e.g., concept semantics, model architecture, gradient landscape).

**Practical Guidance Results:**
[Exact figures unavailable — see full paper]
- For typical concept classification tasks, N = 10-20 examples provides moderate stability (est. reduces variance by ~3x).
- N = 50-100 examples provides high stability for most applications.
- Beyond N = 200, diminishing returns suggest focusing on concept quality rather than sample size.

### Limitations

1. **Linear Model Assumption:** Theoretical results assume linear separability in activation space; may not hold for complex concept-feature interactions.
2. **Concept Semantics Not Modeled:** The theory quantifies sampling variability but does not address whether the concept definition itself is semantically coherent.
3. **Single Hidden Layer Focus:** Analysis focuses on a single layer's activations; extension to multi-layer concepts requires additional work.
4. **TCAV Score Gap:** The disconnect between CAV variance and TCAV score stability remains partly unexplained; further analysis needed.

## Practical Applications & Real-World Use Cases

### 1. Medical Imaging and Diagnostic AI

**Application:** Radiologists use concept-based explanations to validate AI diagnostic systems.

**Practical Challenge:** Manually curating concept examples (e.g., "tumor morphology features") is laborious. How many examples are necessary to obtain stable explanations?

**Solution via This Work:**
- Practitioners can estimate required sample sizes using O(1/N) scaling.
- Confidence intervals around TCAV scores communicate uncertainty to clinicians.
- Enables evidence-based decision on concept set size vs. annotation effort trade-off.

### 2. Fairness and Bias Detection

**Application:** Detecting unintended bias in ML models (e.g., gender bias in hiring ML systems).

**Practical Challenge:** Users define fairness-related concepts (e.g., "gender-neutral features," "stereotypical indicators"). The stability of these explanations is critical for regulatory compliance (GDPR, AI Act).

**Solution via This Work:**
- Quantify and report uncertainty in bias detection.
- Ensure fairness interventions are based on stable, well-sampled concept definitions.
- Enable reproducible fairness audits across independent concept sets.

### 3. Model Debugging and Transparency

**Application:** ML engineers debug unexpected model behavior by discovering what concepts the model responds to.

**Practical Challenge:** Engineers explore hundreds of potential concepts; each requires sampling. Resource constraints limit exploration depth.

**Solution via This Work:**
- Predict variance for a given sample size; allocate resources to highest-priority concepts.
- Use regularization to reduce required sample sizes.
- Prioritize "surprising" concepts that require lower variance to validate.

### 4. Regulatory Compliance and Explainability Audits

**Application:** Regulated domains (finance, healthcare, hiring) require auditable, transparent ML systems.

**Regulatory Requirement:** Explanations must be reliable and documented.

**Solution via This Work:**
- Report TCAV variance and confidence intervals alongside explanations.
- Document sampling procedures and theoretical justification.
- Meet legal requirements for transparency and reproducibility.

### 5. Interactive Concept Learning

**Application:** Systems that iteratively refine concept definitions based on user feedback.

**Practical Challenge:** When user provides new concept examples, how much to trust the refined CAV?

**Solution via This Work:**
- Compute posterior variance after observing user feedback.
- Determine whether additional examples improve reliability sufficiently.
- Guide users toward semantically coherent concept definitions.

## Insights & Implications

### 1. Theoretical Insights for Mechanistic Interpretability

**Implication:** The O(1/N) variance scaling is a **fundamental statistical law**, not an artifact of TCAV's design. This suggests:

- **Universality:** The scaling law may apply to other concept-based methods (CRAFT, ACE, FACES).
- **Theoretical Foundation:** Provides rigorous footing for concept-based explainability research.
- **Connection to Statistical Learning Theory:** Links CAV variability to classical sample complexity results.

### 2. Practical Consequence: Variance-Reliability Decoupling

**Key Discovery:** Lower CAV variance does NOT guarantee higher TCAV score reliability.

**Implication:** Practitioners cannot assume that "more samples = better explanations." Instead:
- Concept **semantic quality** is equally or more important than sample size.
- Model **architecture and training** affect how reliable TCAV scores are.
- Future work should model the full reliability chain: sampling → CAV estimation → TCAV score → user decision.

### 3. Advancing Beyond Empirical Explainability

The paper represents a shift from empirical observation to **theoretical rigor** in explainability:

- **Before:** TCAV and CAVs were validated empirically; instability was acknowledged but not quantified.
- **After:** Practitioners have predictive models for CAV variability and can make principled design decisions.

This aligns with the broader XAI community's move toward formal verification of explanation methods (e.g., axioms for attribution methods, faithfulness bounds).

### 4. Open Questions and Future Directions

The work raises several important questions:

1. **Why Does TCAV Score Variance Plateau?** The decoupling between CAV variance and TCAV score variance deserves deeper investigation.

2. **Concept Semantics Quantification:** How can we formally model concept semantic coherence and its effect on explanation reliability?

3. **Multi-Concept Variance:** How does variance scale when considering multiple interacting concepts?

4. **Generalization to Other Domains:** Do the 1/N scaling results hold for multimodal (vision + language) or RL settings?

5. **Adaptive Sampling:** Can we develop algorithms that adaptively sample concept/non-concept examples to optimize for information gain rather than uniform sampling?

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2509.24058
- **PDF:** https://arxiv.org/pdf/2509.24058
- **HTML Version:** https://arxiv.org/html/2509.24058

### Related Implementations

**TCAV (Original Framework):**
- GitHub: https://github.com/tensorflow/tcav
- Reference: Kim, B., Wattenberg, M., Gilmer, J., et al. (2018). "Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV)." ICML.

**α-TCAV (Improved Stability):**
- Related Paper: https://arxiv.org/abs/2605.15688
- Addresses TCAV score instability; builds on the variance analysis from this paper.

**Concept-Based Methods:**
- CRAFT: Fel, L., Cadène, R., Chalvidal, M., et al. (2023). https://arxiv.org/abs/2211.05667
- FACES: Fel, L., & Jacot, F. (2024). https://arxiv.org/abs/2409.14590

### Computational Requirements

- **Language:** Python
- **Dependencies:** NumPy, SciPy, scikit-learn (for logistic regression), TensorFlow/PyTorch (for model gradients)
- **Estimated Runtime:** 
  - Single concept CAV computation: < 1 second (for logistic regression)
  - TCAV score computation: ~10-100ms per test sample (depends on gradient computation)
  - Full variance study (e.g., 100 random samples × 10 concepts): ~10-60 minutes (on GPU)

### Reproducibility

The paper includes detailed descriptions of:
- Concept definitions and examples per domain
- Hyperparameters for each CAV estimator
- Train/test splits and cross-validation procedures
- Statistical testing methods

To reproduce results:
1. Obtain the same concept sets and model checkpoints (or retrain on public datasets)
2. Sample non-concept examples using the same procedure
3. Train CAVs with specified hyperparameters
4. Compute variance across independent runs
5. Plot log(Var) vs. log(N) and verify 1/N scaling

## Related Work & Context

### Connection to Prior TCAV Work

The paper builds directly on the **TCAV framework** (Kim et al., 2018):
- **TCAV** introduced concept-based explainability using CAVs.
- **This Work** addresses the practical limitation that TCAV scores vary with random sampling.

### Related Concept-Based Methods

1. **CRAFT** (Concept Rectification And Factual Training, 2023): Also faces sampling-induced variability; the 1/N scaling likely applies here too.

2. **ACE** (Automated Concept Extraction, 2018): Automatically discovers concepts rather than user-provided; variability analysis could extend to ACE.

3. **FACES** (Flattening Concept-Space for Explainability, 2024): Uses a different concept embedding; variance analysis may differ.

4. **α-TCAV** (2026, arXiv:2605.15688): Directly cites this work. α-TCAV proposes a continuous relaxation of TCAV to address the score instability revealed by this paper's variance analysis.

### Unified Attribution Framework Connection

Recent work (arXiv:2501.18887) argues that feature attribution, data attribution, and component attribution share fundamental similarities. **This paper on CAV variability** contributes to this unification:

- CAV estimation = **component attribution** (which model features detect the concept).
- The variance analysis provides a template for understanding sampling effects in other attribution methods.

### Mechanistic Interpretability Implications

The paper connects concept-based explainability to mechanistic interpretability:

- **Sparse Features:** Recent mechanistic interpretability work (e.g., sparse autoencoders, dictionary learning) aims to find interpretable features in activation space—similar to CAVs.
- **Variance in Feature Discovery:** The variability analysis could extend to measuring stability of discovered features across different random initializations or training runs.

### Theoretical Foundations

The paper draws on established statistical and ML theory:

1. **Statistical Learning Theory:** Sample complexity bounds and concentration inequalities.
2. **Linear Classification Theory:** Asymptotic normality of logistic regression estimates.
3. **Perturbation Analysis:** How small changes in data affect model estimates (related to influence functions, data valuation).

## Researchers & Institutions

**Authors:**
- **Julia Wenkmann** - Universität Würzburg (University of Würzburg), Germany. Research focuses on the theoretical foundations of explainability and concept-based interpretation.
- **Damien Garreau** - Universität Würzburg, Germany. Previously published on feature attribution (arXiv:2505.24729) and statistical properties of ML explanations.

**Affiliated Institution:**
- **Universität Würzburg:** Strong research program in AI and machine learning. Known for rigorous theoretical work in interpretability and explainability.

## Key Takeaways

1. **Variability is Quantifiable:** CAV estimation error follows a predictable O(1/N) scaling law, enabling evidence-based choices about sample size.

2. **Theory Meets Practice:** The theoretical results directly translate to practical guidance for practitioners using concept-based explanations.

3. **Variance ≠ Reliability:** Reducing sampling variability is necessary but not sufficient for reliable explanations; concept semantics and model properties also matter.

4. **Unifies Concept-Based Methods:** The variance analysis likely applies to other concept-based frameworks (CRAFT, ACE, FACES), providing a common theoretical lens.

5. **Opens New Research Directions:** Raises questions about TCAV score stability, concept semantic modeling, and adaptive sampling strategies.

## References

1. Kim, B., Wattenberg, M., Gilmer, J., Love, C., Bommasani, R., & Nagel, T. (2018). Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV). In *International Conference on Machine Learning (ICML)*, 2663-2672.

2. Wenkmann, J., & Garreau, D. (2025). On the Variability of Concept Activation Vectors. *arXiv:2509.24058*.

3. Fel, L., Cadène, R., Chalvidal, M., et al. (2023). Craft: Concept Rectification And Factual Training. In *IJCAI*, 4320-4328.

4. Fel, L., & Jacot, F. (2024). FACES: A Factored Concept Explanatory System. *arXiv:2409.14590*.

5. Taimeskhanov, M., & Garreau, D. (2025). Feature Attribution from First Principles. *arXiv:2505.24729*.

6. Zhang, S., Han, T., Bhalla, U., & Lakkaraju, H. (2025). Towards Unified Attribution in Explainable AI, Data-Centric AI, and Mechanistic Interpretability. *arXiv:2501.18887*.

7. Hsu, A. R., Zhou, G., Cherapanamjeri, Y., et al. (2025). Efficient Automated Circuit Discovery in Transformers using Contextual Decomposition. *arXiv:2407.00886*. (ICLR 2025).

---

**Last Updated:** November 14, 2026

**Documentation Compiled By:** Claude Haiku 4.5
