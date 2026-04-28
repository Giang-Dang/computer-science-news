# Analyzing Fairness of Neural Network Prediction via Counterfactual Dataset Generation

**ArXiv ID:** 2602.10457  
**Authors:** Brian Hyeongseok Kim, Jacqueline L. Mitchell, Chao Wang  
**Submitted:** February 11, 2026  
**Subfield:** Fairness Interpretability / Counterfactual Explanations  
**Links:** [ArXiv](https://arxiv.org/abs/2602.10457) | [HTML](https://arxiv.org/html/2602.10457)

---

## Executive Summary

This paper introduces a novel perspective on AI fairness analysis: instead of asking "what input change would change this prediction?" (counterfactual inputs), it asks "what training data change would produce a different prediction?" (counterfactual datasets). By constructing the smallest possible alterations to training label sets that would flip a model's prediction on a specific test instance, the method traces how label bias in training data propagates through the learning algorithm to affect individual predictions — providing a principled, mechanistically grounded approach to fairness interpretability.

---

## Problem Statement

### The Gap Between Observational Fairness and Causal Explanations

Current fairness analysis methods suffer from a critical limitation: they measure *statistical disparities* in model outputs (e.g., different acceptance rates across demographic groups) but cannot explain *why* these disparities exist at the level of the training data and learning process. This gap between observation and explanation has several harmful consequences:

1. **Misleading interventions:** Practitioners who observe disparate outputs may apply post-processing bias corrections that do not address root causes in the training data
2. **Regulatory inadequacy:** Laws like GDPR Art. 22 and the EU AI Act require meaningful explanations of automated decisions; statistical parity metrics do not constitute such explanations
3. **Limited accountability:** Without knowing which training examples drive biased predictions, it is impossible to hold data collection or labeling processes accountable

### Counterfactual Input Explanations — Not Enough

The dominant paradigm in counterfactual XAI asks: *"What is the smallest change to input $x$ that would change the model's prediction?"* These "algorithmic recourse" methods (Wachter et al., DICE, CARLA) are useful for individual users but have a fundamental limitation:

**They treat the model as fixed and explain what the user should change, not what the system should change.**

For fairness, the opposite question is more appropriate: *"What training data change should the system make to produce fair outcomes?"*

### What This Paper Tackles

The paper addresses: *Given a neural network classifier trained on dataset $D$ and a test instance $x^*$ with prediction $\hat{y}$, what is the minimum-change alternative training dataset $D'$ (differing from $D$ only in a bounded number of training labels) such that a model retrained on $D'$ would produce a different prediction on $x^*$?*

This is the **counterfactual dataset** — the smallest training data change that would have led to a different outcome.

---

## Core Concepts & Theory

### Formal Problem Definition

Let:
- $D = \{(x_i, y_i)\}_{i=1}^{n}$ be the training dataset with features $x_i$ and labels $y_i$
- $f_D: \mathcal{X} \to \mathcal{Y}$ be a model trained on $D$
- $x^*$ be a test instance with prediction $\hat{y} = f_D(x^*)$

The **counterfactual dataset problem** is:

$$D^* = \arg\min_{D'} |D \triangle D'| \quad \text{s.t.} \quad f_{D'}(x^*) \neq \hat{y}$$

where $|D \triangle D'|$ is the number of training labels changed (the symmetric difference restricted to label changes only).

In words: find the closest alternative training dataset (measured by number of label flips) that produces a different prediction on $x^*$.

### Why Label Changes?

Changing features would be physically unrealistic (you cannot retroactively change what someone's income was). But **labels represent human judgments** (loan approvals, hiring decisions, medical diagnoses) that are subject to bias, error, and social context — and are the most plausible source of systematic unfairness.

A small counterfactual dataset (requiring few label changes) indicates that the prediction is **fragile to label bias**: a small amount of biased labeling could have caused this particular outcome. A large counterfactual dataset indicates robustness.

### The Influence Function Connection

The paper's approach is inspired by influence functions (Koh & Liang, 2017), which measure how upweighting a training example affects model predictions:

$$\frac{\partial \hat{y}}{\partial \epsilon_i} \approx \nabla_\theta f_D(x^*) \cdot H_\theta^{-1} \cdot \nabla_\theta \ell(x_i, y_i, \theta)$$

where $H_\theta$ is the Hessian of the training loss. However, influence functions have well-known limitations for deep neural networks (non-convex loss, approximate Hessian inversion). The authors develop a **label-flip-specific influence approximation** that avoids full Hessian computation while maintaining sufficient accuracy for ranking training examples.

### Heuristic Label Ranking Algorithm

The full combinatorial search over all possible label-flip subsets is NP-hard. The paper introduces an efficient heuristic:

**Algorithm: Counterfactual Dataset Search**

```
Input: Model f_D, test instance x*, budget k
Output: Set of k training examples to flip

1. Compute influence score s_i for each training example i:
   s_i = ∇_θ f_D(x*) · H_θ^{-1} · ∇_θ ℓ(x_i, y_i, θ)
   (approximated via layer-wise propagation)

2. Rank training examples by |s_i| (magnitude of influence)

3. Greedily select top-k examples with highest influence

4. Flip labels of selected examples: y_i → 1 - y_i

5. Retrain model on modified dataset D'

6. Verify: f_{D'}(x*) ≠ f_D(x*)?
   - If yes: return selected examples (counterfactual dataset found)
   - If no: expand k and repeat
```

### Fairness Interpretation of Counterfactual Datasets

The counterfactual dataset provides fairness interpretability in two ways:

**Individual fairness:** If a small counterfactual dataset exists for test instance $x^*$, then $x^*$'s outcome is **highly sensitive to label bias** — a fairness concern. If the counterfactual dataset is concentrated on examples from the same demographic group as $x^*$, this suggests group-level label bias is driving the prediction.

**Group fairness:** Aggregate analysis across many test instances from a demographic group can identify which training examples are consistently influential — revealing systematic labeling biases that affect the group as a whole.

---

## Main Ideas & Key Contributions

### 1. Novel Fairness Analysis Paradigm

The counterfactual dataset framework offers a fundamentally different lens on fairness:
- **From:** "This model discriminates against group G" (statistical observation)
- **To:** "This model discriminates because training examples $\{e_3, e_47, e_128\}$ were labeled biasedly, and fixing those labels would have produced a fair outcome for instance $x^*$"

This enables **targeted, actionable fairness interventions** at the training data level.

### 2. Tracing Label Bias Propagation

The method makes explicit the causal pathway from training data labels to individual predictions — addressing a fundamental gap in fairness explainability. No prior method could answer: "Which specific training examples drive this unfair prediction?"

### 3. Efficient Heuristic with Strong Empirical Performance

The greedy influence-based heuristic typically finds small counterfactual datasets (few label flips required) efficiently, without exhaustive search. Across 1,100+ test cases on 7 fairness datasets, the method consistently identifies small, focused sets of influential training examples.

### 4. Interpretability-Fairness Synthesis

By combining counterfactual explanation methodology (from XAI) with influence function analysis (from training data interpretability) and applying it to fairness (from ML fairness), M-CBM synthesizes three previously disconnected research areas into a unified framework.

### Why This Approach Is Better

| Approach | What it reveals | Limitation |
|----------|-----------------|-----------|
| Disparate impact metrics | Group-level statistical disparity | No causal explanation |
| Counterfactual inputs (DICE, CARLA) | What user should change | Treats model as fixed; user-level |
| Data influence functions | Which training examples affect general performance | Not targeted to fairness or individual decisions |
| **Counterfactual datasets (this work)** | Which training labels drive a specific unfair prediction | Computationally intensive; requires retraining |

---

## Methodology & Implementation

### Experimental Setup

**Models:** Feedforward neural networks (3-layer MLPs with ReLU activations)  
**Scale:** 1,100+ test cases evaluated  
**Datasets:** 7 standard fairness benchmarks:

| Dataset | Domain | Protected attribute |
|---------|--------|---------------------|
| Adult Income | Finance | Gender, Race |
| COMPAS | Criminal justice | Race |
| German Credit | Finance | Gender, Age |
| Bank Marketing | Finance | Age |
| Communities & Crime | Socioeconomic | Race |
| Dutch Census | Socioeconomic | Gender |
| Law School | Education | Race |

### Evaluation Metrics

**Primary:**
- **Counterfactual dataset size:** Number of label flips required (smaller = higher vulnerability to label bias)
- **Flip success rate:** Fraction of test cases where a counterfactual dataset is found within budget $k$
- **Demographic concentration:** Are influential training examples disproportionately from one demographic group?

**Secondary:**
- **Runtime:** Wall-clock time for counterfactual dataset search
- **Influence ranking quality:** Correlation between influence scores and actual impact (ablation study)

### Key Results

- Average counterfactual dataset size: 3–8 label flips across datasets (remarkably small)
- Success rate within $k=10$ label flips: 72–89% across datasets
- Demographically concentrated influential examples: found in 61% of test cases on COMPAS, confirming racial label bias
- Runtime: seconds per test case after one-time influence precomputation

### Limitations

- Requires **retraining** to verify counterfactual dataset efficacy — computationally expensive for large models
- The greedy heuristic may miss the minimum-size counterfactual dataset (optimal solution is NP-hard)
- Evaluated only on **feedforward neural networks**; extension to deep architectures (CNNs, transformers) requires further work
- Influence function approximation assumes approximately convex local loss landscape — less reliable for very deep networks
- Does not handle **feature bias** (bias encoded in features, not labels)

---

## Practical Applications & Real-World Use Cases

### Criminal Justice: COMPAS Recidivism Tool

The COMPAS recidivism prediction tool has been widely criticized for racial disparities. The counterfactual dataset method can:
1. Identify specific cases where small label changes would have flipped predictions
2. Reveal which historical cases' labels are driving current predictions
3. Support legal challenges to specific automated decisions (showing that a small number of biased prior cases drove the outcome)

**Legal application:** In jurisdictions where defendants can challenge algorithmic decisions, counterfactual dataset evidence provides specific, traceable grounds for appeal.

### Credit Scoring and Loan Decisions

For a denied loan application, the counterfactual dataset shows:
- How many historical loan applications would need to have different outcomes (labels) to produce an approval
- Whether those applications are concentrated in the same demographic group (suggesting systemic bias)
- Which specific historical records are most influential (enabling data audits)

**Regulatory application:** Under GDPR Art. 22 and the EU AI Act, individuals have rights regarding automated decisions. Counterfactual datasets provide the training-data-level explanation that current methods cannot.

### Employment and Hiring AI

HR AI tools that screen resumes or rank candidates can be audited using counterfactual datasets:
- Identify training data (historical hiring decisions) that drives unfair outcomes
- Quantify how sensitive current recommendations are to historical biases
- Prioritize data relabeling or augmentation efforts

### Healthcare Diagnostic Tools

In clinical decision support, counterfactual datasets can reveal whether diagnostic recommendations are sensitive to historical labeling errors (e.g., systematic underdiagnosis in certain patient populations) — enabling targeted data quality improvements.

### Regulatory Implications

**GDPR Art. 22 + Recital 71:** Automated decisions must be explainable. Counterfactual datasets provide training-data-level explanations that can be used to contest decisions — a richer accountability mechanism than feature attribution.

**EU AI Act Art. 10 (Data governance):** Requires that high-risk AI training data be "relevant, representative, free of errors and complete." Counterfactual dataset analysis provides a quantitative measure of training data quality from a fairness perspective.

**US Equal Credit Opportunity Act (ECOA):** Requires adverse action notices explaining credit denials. Counterfactual dataset evidence could support more mechanistically honest adverse action notices.

---

## Insights & Implications

### Training Data as the Root Cause of Bias

The paper's central insight is that **bias in model predictions often traces directly to specific labeled training examples.** This shifts responsibility from the model to the data — and, ultimately, to the human labelers and institutions that generated the labels. This has profound implications for accountability.

### Fragility of Fair Predictions

The finding that average counterfactual datasets require only 3–8 label flips is alarming: it means that **a very small number of biasedly labeled training examples can systematically affect predictions on specific test cases.** This argues for much higher scrutiny of training data labeling quality, especially for protected attributes.

### Interpretability-Fairness Unification

This paper demonstrates that **the goals of interpretability and fairness can be productively unified:** making predictions more explainable (in terms of training data) simultaneously makes fairness analysis more actionable. The counterfactual dataset is simultaneously an interpretability artifact and a fairness audit tool.

### Limitations and Open Questions

- Can the method be extended to large neural networks (transformers) where influence function approximation is less reliable?
- How does the framework handle multiple competing biases (racial AND gender bias simultaneously)?
- Can counterfactual dataset size serve as a **fairness regularization objective** during training?
- How do counterfactual datasets relate to **data poisoning** attacks (which also involve targeted training label changes)?

### Future Research Directions

- **Scalability:** Extending to large language models and vision transformers
- **Multi-source bias:** Handling simultaneous bias from multiple protected attributes
- **Proactive debiasing:** Using counterfactual dataset analysis during data collection to identify and correct potential biases before training
- **Formal guarantees:** Developing theoretical bounds on counterfactual dataset size under distributional assumptions
- **Interactive tools:** Building practitioner-facing interfaces for counterfactual dataset auditing

---

## Code & Resources

**ArXiv:** [https://arxiv.org/abs/2602.10457](https://arxiv.org/abs/2602.10457)  
**HTML:** [https://arxiv.org/html/2602.10457](https://arxiv.org/html/2602.10457)

*Check the paper for any associated code repository.*

### Required Dependencies

- PyTorch ≥ 2.0 (model training and retraining)
- NumPy, SciPy (influence function computation)
- AIF360 or Fairlearn (fairness dataset loading and metrics)
- scikit-learn (baseline comparisons)

### Computational Requirements

- **One-time cost:** Influence score computation (requires one backward pass per training example)
- **Per-case cost:** Greedy selection (fast) + model retraining (moderately expensive for neural networks)
- **Overall:** Tractable for datasets up to ~100K examples; scaling to millions requires approximation

### Related Fairness Tools

- **AIF360 (IBM):** [github.com/Trusted-AI/AIF360](https://github.com/Trusted-AI/AIF360) — standard fairness metrics and algorithms
- **Fairlearn (Microsoft):** [fairlearn.org](https://fairlearn.org) — fairness assessment and mitigation
- **CARLA:** [github.com/carla-recourse/CARLA](https://github.com/carla-recourse/CARLA) — counterfactual recourse (input-level; contrasts with this paper's training-data approach)
- **SHAP:** [github.com/slundberg/shap](https://github.com/slundberg/shap) — feature attribution for individual decisions

---

## Related Work & Context

### Counterfactual Explanation Foundations

- **Wachter, Mittelstadt & Russell (2017):** Foundational counterfactual explanation paper (input-level) — this paper is a direct extension to the training data level
- **DICE (Mothilal et al., 2020):** Diverse counterfactual explanations — operates at input level; complementary to training-data counterfactuals
- **CARLA (Pawelczyk et al., 2021):** Benchmarks counterfactual recourse methods

### Data Influence Functions

- **Koh & Liang (2017):** "Understanding Black-box Predictions via Influence Functions" — the technical foundation for this paper's influence ranking
- **Ilyas et al. (2022) DataModels:** An alternative approach to quantifying training data influence; conceptually related

### Fairness Interpretability

- **Fairness indicators (Pfohl et al.):** Disparate impact measurement — statistical, not causal
- **Counterfactual fairness (Kusner et al., 2017):** Causal fairness definition; this paper provides a practical method for finding causal training data effects
- **DANCE (already in this repo's causal-interpretability folder):** Counterfactual explanations with causal constraints — complements this paper's training-data-level approach

### Connection to Data-Centric AI

This paper aligns with the **data-centric AI movement** (Andrew Ng et al.) that argues improving data quality is more impactful than improving model architecture. Counterfactual dataset analysis provides a principled tool for identifying *which specific data quality improvements* (label corrections) would most improve fairness outcomes.

### Where This Research Leads

The counterfactual dataset framework opens research directions connecting:
- **Data poisoning / robustness:** Adversarial label flipping to degrade fairness
- **Active learning for fairness:** Prioritizing relabeling based on counterfactual dataset analysis
- **Federated fairness:** Identifying biased data sources in federated learning without central data access
- **Differential privacy + fairness:** How privacy constraints affect the ability to compute counterfactual datasets
