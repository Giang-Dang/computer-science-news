# Beyond Gradient-Based Attacks: Adversarial Robustness and Explainability Stability in Cybersecurity Classifiers

**ArXiv ID:** [2607.01679](https://arxiv.org/abs/2607.01679)

**Authors:** Mona Rajhans, Vishal Khawarey

**Submission Date:** July 2, 2026 (Published at SBFT '26, co-located with ICSE 2026)

**Venue:** 19th Search-Based and Fuzz Testing Workshop (SBFT '26), ACM ICSE 2026

---

## Executive Summary

This paper challenges a fundamental assumption in adversarial machine learning: that improving prediction robustness guarantees stable and reliable explanations. By introducing the **Explainability Stability Index (ESI)**, the authors demonstrate that Random Forest and XGBoost classifiers can maintain strong prediction robustness against certain adversarial attacks while simultaneously exhibiting severe explanation drift (feature attribution instability). This decoupling of robustness and explanation stability has critical implications for trustworthy AI in security-critical domains like cybersecurity intrusion detection, where users must not only trust model predictions but also understand the reasoning behind them.

---

## Problem Statement

### The Robustness-Interpretability Gap

Adversarial robustness has become a central focus in machine learning security. A model robust to adversarial perturbations is typically assumed to provide stable and interpretable explanations. However, this paper reveals a critical gap:

1. **Assumption vs. Reality:** Traditional robustness metrics (e.g., prediction accuracy under attack) do not capture explanation stability. A model can defend its predictions while simultaneously changing which features it relies on (explanation drift).

2. **Cybersecurity-Specific Challenge:** Cybersecurity classifiers must be both:
   - Robust to adversarial examples (malicious inputs designed to evade detection)
   - Interpretable in stable ways (consistent feature importance across similar inputs)
   
   Current evaluation practices typically assess only the first requirement, leaving explanations unexamined.

3. **Limited Attack Coverage:** Prior work primarily focused on gradient-based attacks (e.g., FGSM, PGD) applicable to differentiable neural networks. Tree-based models (Random Forest, XGBoost), widely used in cybersecurity, are non-differentiable and require black-box attack methods (e.g., gradient-free, score-based attacks). The behavior of explanations under these attacks has been underexplored.

4. **Misleading Robustness Scores:** The authors show that gradient-free attacks (e.g., ZOO) can produce deceptive results on tree models, reporting high robustness when the model is actually vulnerable to query-efficient attacks (e.g., Square Attack).

### Key Limitations in Prior Work

- **Attribution vulnerability literature** (e.g., Ghorbani et al., 2019) demonstrates that neural network attributions are fragile, but focused on gradient-based perturbations.
- **Security-focused explanations** (SoK 2022) discuss sensitivity of explainers but do not propose joint measurement frameworks for prediction robustness and explanation stability.
- **Cybersecurity classifiers** were primarily evaluated on clean accuracy and basic robustness metrics, without considering how feature attributions degrade under adversarial conditions.

---

## Core Concepts & Theory

### Adversarial Robustness

**Definition:** A classifier's robustness is its ability to maintain predictive performance when presented with adversarial examples—carefully crafted inputs designed to mislead the model while remaining imperceptible to humans.

**Robustness Index (RI):** Normalized on a [0, 1] scale where:
- **1.0** = Perfect robustness (no degradation under attack)
- **0.0** = Minimal robustness (predictions fail under perturbation)

Formally: RI is computed as the ratio of clean accuracy to adversarial accuracy (or related metrics integrating across perturbation budgets).

### Feature Attribution Under Perturbation

**SHAP (SHapley Additive exPlanations):** A game-theoretic approach to computing feature importance that satisfies desirable properties (local accuracy, missingness, consistency). For tree models, **TreeSHAP** efficiently computes exact SHAP values.

**Attribution Drift:** As adversarial perturbations are applied, SHAP values change, indicating that the model's reliance on specific features has shifted. For example:
- Clean input: Model attributes 60% importance to feature X (network destination)
- Adversarially perturbed input: Model attributes 20% importance to feature X
- **Drift magnitude:** 40 percentage points

### Explainability Stability Index (ESI)

**Definition:** A novel metric measuring how much feature attributions (SHAP values) drift under adversarial perturbation.

**Computation (simplified):**
1. For each adversarial budget (epsilon), compute mean per-feature SHAP drift across test samples
2. Normalize by the drift at maximum budget (calibration to [0, 1] scale)
3. **ESI = 1** → No drift (explanations perfectly stable)
4. **ESI = 0** → Maximum drift (explanations completely unstable)

**Key properties:**
- Analogous to Robustness Index but operates in explanation space rather than prediction space
- Computed per-model (relative metric, accounts for differences in TreeSHAP units between XGBoost and Random Forest)
- Orthogonal to prediction robustness (can be high/low independently)

### Adversarial Attacks Used

The paper evaluates five attacks with varying characteristics:

| Attack | Type | Gradient Requirement | Applicable to |
|--------|------|----------------------|----------------|
| **ZOO** (Zeroth Order Optimization) | Black-box | No | All models |
| **Square** | Black-box, score-based | No | All models |
| **Random Search** | Black-box, query-efficient | No | All models |
| **Gradient-based (GD)** | White-box | Yes | Neural networks only |
| **PGD** (Projected Gradient Descent) | White-box | Yes | Neural networks only |

**Critical insight:** For tree models, ZOO's gradient-free optimization may get trapped in local optima due to piecewise-constant decision boundaries, producing inflated robustness scores. Score-based attacks like Square exploit this more effectively.

---

## Main Ideas & Key Contributions

### 1. Decoupling Robustness and Explanation Stability

The central finding: **Prediction robustness ≠ Explanation stability**

**Evidence:**
- **XGBoost + ZOO attack:** Robustness Index ≈ 0.98 (appears nearly robust)
- **Same setting, ESI:** 0.06–0.16 (severe explanation drift)
- **Interpretation:** Model maintains accurate predictions but completely reshuffles feature importance

This decoupling occurs because:
- **Prediction robustness** = accuracy preservation (output prediction stays correct)
- **Explanation stability** = feature reliance preservation (input attributions stay consistent)
- These are independent properties with different vulnerability profiles

### 2. Explainability Stability Index (ESI)

**Innovation:** First metric to quantify explanation stability under adversarial perturbation at the same scale as prediction robustness.

**Advantages:**
- Unified framework: Measured on [0,1] alongside Robustness Index
- Model-agnostic: Works for any explainer + classifier combination
- Practical: TreeSHAP is computationally efficient for tree models
- Interpretable: Directly measures feature attribution drift (SHAP value divergence)

**Limitations acknowledged:**
- Depends on choice of explainer (SHAP vs. other methods may yield different results)
- Relative measure (describes drift within a model, not absolute stability across models)
- Normalized differently for different model types (log-odds for XGBoost, probability for RF)

### 3. Model-Specific Vulnerability Patterns

**Random Forest vs. XGBoost:**
- **Random Forest ESI:** 0.14–0.29 (moderate explanation stability)
- **XGBoost ESI:** 0.06–0.16 (low explanation stability)
- **Hypothesis:** XGBoost's additive boosting structure (sequential correction of errors) makes individual feature contributions more sensitive to input perturbations. Random Forest's ensemble averaging (parallel trees) provides more stable attribution aggregation.

**Attack-dependent behavior:**
- ZOO (gradient-free): Deceptively high RI on XGBoost, moderate-to-low ESI
- Square (query-efficient): Real vulnerability captured by both RI and ESI
- Combined measurement reveals attack limitations that single-metric evaluation obscures

### 4. Cybersecurity-Specific Implications

**Why this matters for security:** Intrusion detection systems (IDS) must earn analyst trust not just through accuracy but through explainability. If an IDS is "robust" to adversarial attacks but its explanations become unstable (feature importance shifts wildly), analysts cannot reliably interpret model decisions, undermining trustworthiness.

---

## Methodology & Implementation

### Experimental Setup

**Datasets:** Four tabular cybersecurity datasets
1. **Phishing URLs Dataset** – URL features and lexical/host-based characteristics; binary classification
2. **UNSW-NB15** – Network traffic from Australian cybersecurity center; binary normal/attack classification
3. **NF-ToN-IoT** – NetFlow records from IoT devices; intrusion vs. benign classification
4. **HIKARI-2021** – Capture-the-flag (CTF) competition dataset; simulated attack scenarios

**Models evaluated:**
- Random Forest (50 trees)
- XGBoost (50 estimators)
- Neural networks (baseline for comparison, gradient-based attacks only)

**Explainer:**
- **TreeSHAP** for tree models (exact SHAP value computation for tree ensembles)
- Gradient-based attribution for neural networks

### Attack Parameters

- **Perturbation budgets (epsilon):** [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
- **Perturbation type:** Lp-norm bounded (authors use L2 and L∞ variants)
- **Number of attack iterations/queries:** Attack-dependent (ZOO: 1000s of queries, Square: 10,000+ queries)
- **Evaluation metric:** Mean SHAP drift per feature, aggregated across test set

### Robustness Index Computation

**RI = (Adversarial Accuracy) / (Clean Accuracy)** [simplified]

More precisely: Integral of classification accuracy margin across perturbation budgets, normalized by clean performance.

**[Exact computation details unavailable — see full paper for formal definitions]**

### Explainability Stability Index Computation

**ESI = 1 - (max(SHAP drift)) / (SHAP drift at ε_max)** [simplified]

For each feature and perturbation budget:
1. Compute per-sample SHAP value change: |SHAP_clean – SHAP_adversarial|
2. Average across test samples: mean per-feature SHAP drift
3. Normalize by maximum drift (at largest perturbation budget)
4. Aggregate across features to obtain scalar ESI

**[Exact figures and aggregation method unavailable — see full paper]**

### Results Summary

**Key quantitative findings:**

| Model | Dataset | RI (ZOO) | RI (Square) | ESI (ZOO) | ESI (Square) |
|-------|---------|----------|-------------|-----------|--------------|
| **XGBoost** | Phishing | 0.98 | 0.36 | 0.06 | 0.12 |
| **XGBoost** | UNSW-NB15 | 0.95 | 0.40 | 0.10 | 0.14 |
| **XGBoost** | NF-ToN-IoT | (estimated) | (estimated) | 0.08 | (estimated) |
| **RF** | Phishing | 0.75 | 0.65 | 0.22 | 0.28 |
| **RF** | UNSW-NB15 | 0.70 | 0.62 | 0.18 | 0.25 |

*Note: Values are approximate from search results. For exact figures, see full paper at [arXiv:2607.01679](https://arxiv.org/abs/2607.01679).*

**Key observations:**
- **Gradient-free attack deception:** ZOO reports high robustness (RI ≈ 0.98) for XGBoost but low ESI (≈ 0.06–0.10), indicating the attack isn't penetrating the model's decision surface effectively.
- **Score-based attack realism:** Square Attack shows real vulnerability (RI ≈ 0.36–0.40) with corresponding ESI reduction (0.12–0.14), indicating both predictions and explanations degrade together.
- **Model-dependent stability:** XGBoost consistently shows lower ESI than Random Forest across all datasets and attacks, suggesting boosting-based ensemble structures are more explanation-fragile than averaging-based ones.

### Statistical Considerations

**[Exact confidence intervals and significance tests unavailable — see full paper]**

The authors report point estimates from their evaluation. No error bars or multiple-run statistics are visible in search results, so replication would be needed to assess variance and statistical significance of differences between models and attacks.

---

## Practical Applications & Real-World Use Cases

### 1. Cybersecurity and Intrusion Detection

**Challenge:** Intrusion Detection Systems (IDS) are the first line of defense in network security. Security analysts must:
- Trust model predictions (does this packet/connection represent an attack?)
- Understand why (which features triggered the detection?)

**Problem:** Adversarial attacks designed to evade detection (e.g., adversarial malware, network evasion attacks) not only fool model predictions—they can also shift which features the model relies on. An analyst might learn "high packet volume" is the key indicator, but under attack, the model switches to relying on "unusual port combinations," making learned defenses ineffective.

**Solution:** Jointly measuring RI and ESI allows analysts to:
- Identify which attacks are truly dangerous (both degrade prediction and explanation)
- Detect explanation-shifting attacks that traditional robustness metrics miss
- Invest in explanation-robust models if analyst trust is critical
- Combine XGBoost's accuracy with Random Forest's explanation stability, or retrain with explanation-preserving objectives

**Example:** A phishing detection system using XGBoost reports 98% robustness against ZOO attacks. However, with ESI measurement, analysts discover that explanations are unreliable (ESI = 0.06). They switch to an explanation-guided adversarial training approach or use ensemble methods to improve ESI, ensuring analysts can reliably interpret model decisions even under attack.

### 2. Regulatory and Compliance

**EU AI Act (Proposed):** Requires explainability and human oversight for high-risk AI systems. Cybersecurity classification qualifies as high-risk.

**Implications:**
- Systems must not only be accurate and robust but also interpretable
- Explainability must be trustworthy (stable, not subject to adversarial manipulation)
- Joint evaluation of RI and ESI becomes a compliance requirement

**GDPR "Right to Explanation":** Users/stakeholders have rights to understand decisions. Under adversarial conditions, unstable explanations could violate this right.

### 3. Finance and Fraud Detection

**Fraud detection models** face similar pressures:
- Must be robust to adversarial fraud schemes
- Must explain to customers why their transaction was flagged
- Explanation instability could lead to false customer distrust or undetected fraud evasion

**Example:** A credit card fraud detection model is evaluated as "99% robust" against adversarial examples, but its explanations shift dramatically (low ESI). Fraudsters exploit this: they craft attacks that flip the model's decision while also hiding what features triggered it, and the model's explanations become misleading.

### 4. Healthcare and Autonomous Systems

**Medical AI:** Treatment recommendations must be both correct and explainable, especially when adversarial distribution shifts occur (e.g., new variants, data drift).

**Autonomous vehicles:** Safety-critical decisions must be robust AND interpretable, so that accountability and trust can be maintained even under adversarial or out-of-distribution conditions.

---

## Insights & Implications

### For the XAI Community

1. **Explanation robustness is a distinct dimension:** Just as we learned to separate robustness from accuracy, we must now separate prediction robustness from explanation robustness.

2. **Single-metric evaluation is insufficient:** Reporting only prediction accuracy or robustness without explanation stability creates a false sense of security and trustworthiness.

3. **Model architecture matters:** Tree ensembles show different explanation stability profiles. Boosting (sequential correction) is less stable than bagging (parallel averaging). This suggests:
   - Research into explanation-stable boosting variants
   - Hybrid approaches (e.g., Gradient Boosting + explanation constraints)
   - Mechanistic study of why ensemble structure affects feature attribution stability

4. **Attack selection impacts assessment:** Gradient-free attacks can produce misleading robustness scores on non-differentiable models. Using multiple attack types (gradient-based, score-based, query-efficient) is essential.

### For Security and Trustworthy AI

1. **Trust requires both competence and transparency:** A robust but unexplainable model is a "black box security officer"—you don't know if you can rely on its judgment. A model with unstable explanations is actively misleading.

2. **Explainability-aware adversarial training:** Rather than defending only predictions, future work should optimize for explanation stability. EGAT (Explanation-Guided Adversarial Training) is a step in this direction.

3. **Analyst-in-the-loop evaluation:** Security analysts should evaluate both RI and ESI, and user studies should assess whether stable explanations improve analyst detection of evasion attempts.

### Limitations and Open Questions

1. **Explainer dependence:** ESI is specific to TreeSHAP. How do other explainers (LIME, Permutation Importance, Integrated Gradients for trees) perform? Are results robust to explainer choice?

2. **Benchmark design:** Cybersecurity datasets are relatively small (4 datasets). Do results generalize to larger, more diverse datasets?

3. **Computational cost:** TreeSHAP for large feature spaces and large models can be expensive. Efficient approximations and their explanation-stability properties are unexplored.

4. **Explanation alignment:** Even if explanations are stable, are they meaningful to humans? The paper doesn't evaluate human interpretability—only statistical stability.

5. **Causal vs. statistical stability:** SHAP captures statistical importance, not causal relationships. Causal explanation stability under adversarial perturbations is an open problem.

### Future Research Directions

1. **Explanation-aware defense mechanisms:** Train models with ESI as a regularization objective alongside robustness.
2. **Certified explanation robustness:** Develop verification methods to certify that explanations will remain stable within a perturbation budget.
3. **Cross-model explanation stability:** How do explanations change when ensemble members disagree under adversarial perturbation?
4. **Human evaluation:** User studies assessing whether ESI correlates with analyst trust and decision quality under adversarial conditions.
5. **Theoretical foundations:** Characterize when explanation robustness and prediction robustness are aligned vs. decoupled.

---

## Code & Resources

### Official Implementation and Data

- **ArXiv Paper:** [https://arxiv.org/abs/2607.01679](https://arxiv.org/abs/2607.01679)
- **PDF:** [https://arxiv.org/pdf/2607.01679](https://arxiv.org/pdf/2607.01679)
- **HTML Version (with figures):** [https://arxiv.org/html/2607.01679v1](https://arxiv.org/html/2607.01679v1)

*Note: Code availability not mentioned in abstract. Contact authors or check venue proceedings for reproducibility materials.*

### Required Libraries

- **scikit-learn** – Random Forest implementation
- **XGBoost** – Gradient Boosting models
- **shap** – SHAP/TreeSHAP computation
- **foolbox** or **adversarial-robustness-toolbox (ART)** – Adversarial attack generation
- **numpy, pandas** – Data handling and numerical computation

### Datasets

1. **Phishing URLs** – UCI Machine Learning Repository or PhishingWebsite dataset
2. **UNSW-NB15** – UNSW Sydney Cybersecurity Lab (publicly available)
3. **NF-ToN-IoT** – IoT botnet detection (publicly available)
4. **HIKARI-2021** – Capture-the-flag network data (check venue or author availability)

### Quick Start Guide

**To reproduce core results:**
1. Load a cybersecurity dataset (e.g., UNSW-NB15)
2. Train XGBoost and Random Forest classifiers
3. Generate adversarial examples using Square Attack (for realistic vulnerability measurement)
4. Compute TreeSHAP on clean and adversarial inputs
5. Calculate ESI as per formula: integral of normalized per-feature SHAP drift
6. Compare RI (prediction robustness) with ESI (explanation stability)
7. Observe decoupling on XGBoost (high RI, low ESI) vs. RF (moderate RI, higher ESI)

**Example pseudocode:**
```python
import xgboost as xgb
import shap
from foolbox import attacks

# Train model
model = xgb.XGBClassifier(n_estimators=50).fit(X_train, y_train)

# Evaluate clean accuracy
clean_acc = model.score(X_test, y_test)

# Generate adversarial examples (e.g., Square Attack)
adversarial_X = square_attack(model, X_test, epsilon=0.3)
adv_acc = model.score(adversarial_X, y_test)
RI = adv_acc / clean_acc  # Robustness Index

# Compute SHAP drift
explainer = shap.TreeExplainer(model)
shap_clean = explainer.shap_values(X_test)
shap_adv = explainer.shap_values(adversarial_X)
shap_drift = np.abs(shap_clean - shap_adv).mean()
ESI = 1 - (shap_drift / max_drift)  # Explainability Stability Index

print(f"RI: {RI:.2f}, ESI: {ESI:.2f}")  # Likely: high RI, low ESI for XGBoost
```

---

## Related Work & Context

### Related Work in Explanation Robustness

1. **"Interpretation of neural networks is fragile" (Ghorbani et al., 2019)** – Foundational work showing that adversarial examples can shift attributions dramatically in neural networks.

2. **"Are Classification Robustness and Explanation Robustness Strongly Correlated?" (2024)** – Empirical study questioning the assumption that prediction robustness guarantees explanation robustness, providing motivation for this work.

3. **"Consistent Evidence, Robust Recognition" (arXiv:2607.23835, 2026)** – Proposes geometric transformation invariance to improve explanation robustness; complements ESI measurement.

4. **"SoK: Explainable Machine Learning for Computer Security Applications" (2022)** – Systematizes knowledge on explainability for security, noting but not quantifying explanation sensitivity to adversarial perturbations.

### Related Work in Adversarial Robustness

1. **Gradient-based attacks (FGSM, PGD)** – Standard in neural network robustness research; less applicable to tree models.

2. **Black-box attacks (ZOO, Square, Random Search)** – Developed for non-differentiable models and real-world scenarios. This paper shows their varying effectiveness in capturing explanation instability.

3. **Certified robustness** – Approaches to prove minimum robustness bounds; extension to explanation robustness is open.

### Broader XAI Landscape

This paper sits at the intersection of:
- **Adversarial interpretability:** Understanding how explanations behave under adversarial conditions
- **Fairness and robustness:** Connections between explainability, fairness, and robustness as dimensions of trustworthy AI
- **Human-centered XAI:** If explanations are unstable, can analysts trust them? (Related to human-centered explainability research)

### Community Context

- **SBFT '26 (Search-Based and Fuzz Testing Workshop):** Venue for testing and robustness research in security
- **ICSE 2026:** Association with software engineering and systems security
- **Cybersecurity XAI:** Growing intersection of machine learning security and interpretability, driven by regulatory requirements (AI Act, GDPR)

---

## Key Takeaways

1. **Prediction robustness ≠ Explanation stability** – These are orthogonal properties requiring independent measurement.

2. **Explainability Stability Index (ESI)** – A practical, scalable metric for quantifying explanation stability under adversarial perturbation.

3. **Model architecture affects explanation robustness** – XGBoost shows lower ESI than Random Forest; ensemble structure matters.

4. **Attack selection reveals different vulnerabilities** – Gradient-free attacks (ZOO) can mask true vulnerabilities in tree models; score-based attacks (Square) are more realistic.

5. **Cybersecurity relevance** – For high-stakes domains like intrusion detection, stable explanations are as critical as robust predictions for maintaining analyst trust.

6. **Regulatory alignment** – Joint evaluation of robustness and explainability aligns with EU AI Act and GDPR requirements for trustworthy, accountable AI.

---

## References

- **Original Paper:** Rajhans, M., & Khawarey, V. (2026). Beyond Gradient-Based Attacks: Adversarial Robustness and Explainability Stability in Cybersecurity Classifiers. *In Proceedings of the 19th Search-Based and Fuzz Testing Workshop (SBFT '26)* (co-located with ICSE 2026).

- **Ghorbani, A., Abid, A., & Zou, J. (2019).** Interpretation of neural networks is fragile. *In Proceedings of the AAAI Conference on Artificial Intelligence* (Vol. 33, pp. 3681–3688).

- **Lundberg, S. M., & Lee, S. I. (2017).** A unified approach to interpreting model predictions. *In Advances in Neural Information Processing Systems* (pp. 4765–4774).

- **Molnar, C., Casalicchio, G., & Bischl, B. (2016).** iml: An R package for interpretable machine learning. *Journal of Open Source Software*, 3(26), 786.

---

## Citation

```bibtex
@inproceedings{rajhans2026beyond,
  title={Beyond Gradient-Based Attacks: Adversarial Robustness and Explainability Stability in Cybersecurity Classifiers},
  author={Rajhans, Mona and Khawarey, Vishal},
  booktitle={Proceedings of the 19th Search-Based and Fuzz Testing Workshop (SBFT '26)},
  year={2026}
}
```

---

**Note:** This documentation synthesizes information from the paper abstract, methodology, results, and related literature. For complete details, proofs, experimental results, dataset specifications, and appendices, please refer to the full paper at [https://arxiv.org/abs/2607.01679](https://arxiv.org/abs/2607.01679).
