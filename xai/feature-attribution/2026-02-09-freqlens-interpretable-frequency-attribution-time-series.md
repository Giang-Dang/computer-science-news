# FreqLens: Interpretable Frequency Attribution for Time Series Forecasting

**ArXiv ID:** 2602.08768  
**Submitted:** February 9, 2026  
**Accepted:** 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD 2026)  
**Authors:** Chi-Sheng Chen et al. (6 authors)  
**xAI Subfield:** Feature Attribution  

---

## Executive Summary

FreqLens is an interpretable time series forecasting framework that learns frequency bases directly from data and provides axiomatic guarantees on the quality of its frequency-level attributions. Unlike conventional approaches that either hardcode domain-specific frequencies or produce time-level saliency maps, FreqLens introduces a strictly additive frequency decomposition architecture whose per-frequency contributions provably satisfy four desirable axioms and are equivalent to Shapley values. This dual achievement — competitive forecasting accuracy alongside theoretically grounded interpretability — addresses a longstanding gap in transparent AI for sequential prediction tasks.

---

## Problem Statement

### The Interpretability Gap in Time Series Forecasting

Time series forecasting is foundational to high-stakes domains including energy grid management, traffic routing, climate modeling, and financial risk. Despite the impressive accuracy of modern deep forecasters (Transformers, linear models, graph networks), their internal decision-making processes remain opaque. Practitioners cannot answer fundamental questions such as:

- *Which periodicities (daily, weekly, seasonal) drive a prediction?*
- *Is the model exploiting spurious correlations instead of genuine periodic structure?*
- *When the model fails, was it because a dominant frequency pattern was disrupted?*

### Limitations of Prior xAI Approaches for Time Series

**Time-level attribution methods** (SHAP applied to raw time steps, Integrated Gradients, attention weights) assign importance scores to individual time steps or input tokens. While these techniques answer "which time point matters," they cannot answer "which periodic pattern matters" — a conceptually more natural question for forecasting tasks where periodic structure is the primary signal.

**Fixed-frequency decomposition methods** (Fourier transforms, wavelet decompositions, FEDformer, Autoformer) decompose signals using mathematically defined basis functions. These provide frequency-level structure, but the bases are fixed a priori and do not adapt to the dataset's actual periodicity. A model trained on a dataset with dominant 36-hour cycles cannot represent this with a standard FFT basis aligned to 24-hour increments.

**Heuristic frequency importance scores** used in some interpretable frequency models lack formal guarantees. A score defined as "energy at frequency k" may not reflect the actual contribution of that frequency to the final prediction, violating intuitive fairness properties.

FreqLens simultaneously addresses all three limitations: it learns frequencies from data, provides frequency-level (rather than time-level) attributions, and guarantees those attributions satisfy axiomatic properties.

---

## Core Concepts & Theory

### 1. Frequency Attribution — What It Means

For a forecaster F(x) = ŷ where x ∈ ℝ^T is the input window and ŷ ∈ ℝ^H is the forecast horizon, a **frequency attribution** is a mapping:

```
A : (x, {f_1, ..., f_K}) → (A_1, ..., A_K)
```

where A_k ∈ ℝ^H quantifies the contribution of the k-th learned frequency component to the prediction. The attribution is interpretable only if it satisfies certain desirable properties (axioms).

### 2. The Four Attribution Axioms

FreqLens introduces and satisfies a formal axiom system for frequency attribution — analogous to the Shapley axioms for tabular feature attribution:

**Axiom 1 — Completeness (Conservation)**
```
Σ_k A_k = ŷ_freq
```
The sum of all frequency attributions equals the frequency-based prediction component. No "unexplained" contribution exists — the attribution fully accounts for the model's frequency-derived output.

**Axiom 2 — Faithfulness (Non-Deception)**
If removing frequency f_k from the decomposition does not change the prediction, then A_k = 0. The attribution accurately reflects the actual causal role of each frequency; it cannot assign nonzero importance to an irrelevant component.

**Axiom 3 — Null-Frequency (Sparsity Respect)**
If frequency f_k is not present in the input signal (zero amplitude), its attribution must be zero. This prevents the model from attributing explanatory weight to phantom periodicities.

**Axiom 4 — Symmetry (Fairness)**
If two frequencies f_i and f_j are interchangeable — i.e., swapping their basis vectors does not change the prediction — then A_i = A_j. Symmetric contributions receive equal attribution.

**Theorem (Shapley Equivalence):** Under FreqLens's additive decomposition architecture, the per-frequency contribution A_k provably satisfies all four axioms and equals the Shapley value for a cooperative game where the K frequency components are "players" and the forecast is the "value function."

This result is significant: it means FreqLens's attributions inherit all the theoretical guarantees of Shapley values (the gold standard for feature attribution in tabular xAI) but applied in the frequency domain.

### 3. Shapley Values — Brief Primer

For a function f with N input features, the Shapley value φ_i measures each feature's marginal contribution averaged over all possible subsets:

```
φ_i(f, x) = Σ_{S ⊆ N\{i}} [|S|!(N-|S|-1)! / N!] × [f(S ∪ {i}) − f(S)]
```

The Shapley value is the unique allocation satisfying Efficiency (Completeness), Dummy (Null-feature), Symmetry, and Linearity axioms. FreqLens's frequency attributions are the Shapley values of a cooperative game where each frequency basis is a player — achieved at O(K) cost (no exponential enumeration) due to the model's exact additive structure.

---

## Main Ideas & Key Contributions

### Contribution 1: Learnable Frequency Discovery

Prior frequency-domain models require domain experts to specify the relevant frequencies (e.g., 24h for traffic, 8760h for annual energy patterns). FreqLens parameterizes frequency bases as:

```
f_k = sigmoid(θ_k) × f_max,  k = 1, ..., K
```

where θ_k are learned parameters and f_max is a hyperparameter upper bound. The sigmoid ensures valid frequencies in (0, f_max). The model learns the K most useful frequencies for prediction directly from the training data.

**Diversity Regularization:** Without regularization, all K learned frequencies would collapse to the single most dominant frequency. FreqLens adds a diversity loss:

```
L_diversity = Σ_{i≠j} exp(−|f_i − f_j| / τ)
```

This mutual repulsion penalty encourages the K frequencies to spread across the spectrum, discovering distinct periodic patterns rather than K near-copies of the dominant cycle.

### Contribution 2: Strict Additive Architecture

The architectural cornerstone of FreqLens is **strict additive decomposition**. The prediction is:

```
ŷ = Σ_{k=1}^{K} φ_k(x) + r(x)
```

where:
- φ_k(x) is the prediction contribution of frequency component k (computed independently)
- r(x) is a residual term capturing non-periodic structure

Because each φ_k operates independently and their contributions sum exactly to ŷ_freq, the attribution A_k = φ_k(x) is direct and exact — no approximation or sampling needed. This is what makes the Shapley equivalence hold at O(K) cost.

### Contribution 3: First Axiomatic Framework for Frequency Attribution

Before FreqLens, no paper had formalized what properties a "good" frequency attribution should satisfy. FreqLens contributes this theoretical foundation, enabling future work to evaluate and compare frequency attribution methods on principled grounds. This mirrors the historical impact of Shapley axioms on tabular feature attribution (SHAP, Integrated Gradients, etc.).

---

## Methodology & Implementation

### Architecture Overview

FreqLens consists of four sequential components:

```
Input x ∈ ℝ^T
       │
       ▼
┌─────────────────────────────────┐
│ 1. Learnable Frequency          │
│    Decomposition                │
│    x → {c_1(x), ..., c_K(x)}   │
│    (K sinusoidal components)    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ 2. Sparse Frequency Selection   │
│    Prune low-energy components  │
│    (soft thresholding)          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ 3. Axiomatic Attribution Head   │
│    φ_k(x) = g_k(c_k(x))        │
│    independent per-frequency    │
│    prediction module            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ 4. Residual Fusion              │
│    ŷ = Σ_k φ_k(x) + MLP(x)    │
└─────────────────────────────────┘
               │
               ▼
Output ŷ ∈ ℝ^H
```

**Component Details:**

1. **Learnable Frequency Decomposition:** Each frequency f_k (parameterized via sigmoid) generates a sinusoidal basis wave. The input x is projected onto each basis via learned amplitude and phase parameters: c_k(x) = A_k · sin(2π f_k · t + ψ_k).

2. **Sparse Frequency Selection:** A soft-threshold operator zeroes out components with amplitude below a learnable threshold, encouraging sparsity in the active frequency set. This prevents overfitting to noise frequencies.

3. **Axiomatic Attribution Head:** Each c_k(x) is independently passed through a small MLP g_k to produce φ_k(x) ∈ ℝ^H. The independence is crucial: φ_k depends only on frequency k's component, ensuring the attribution is causally grounded.

4. **Residual Fusion:** The residual branch r(x) = MLP(x) captures non-periodic signals (trends, sudden anomalies). The final prediction is the exact sum. For interpretability, the residual is treated as a single "aperiodic" attribution term.

### Experimental Setup

**Datasets (7 benchmarks):**

| Dataset | Domain | Channels | Frequency | Sequence Length |
|---------|--------|----------|-----------|-----------------|
| Weather | Meteorology | 21 | 10 min | 336 |
| Traffic | Road occupancy | 862 | 1 hour | 336 |
| Electricity | Power consumption | 321 | 1 hour | 336 |
| ETTh1/h2 | Energy transformer | 7 | 1 hour | 336 |
| ETTm1/m2 | Energy transformer | 7 | 15 min | 336 |

**Baselines:**
- PatchTST (patch-based Transformer)
- iTransformer (inverted Transformer for multivariate series)
- FEDformer (frequency-enhanced decomposed Transformer)
- Autoformer (auto-correlation Transformer)
- DLinear (simple decomposition linear baseline)

**Evaluation Metrics:**
- MSE (Mean Squared Error) and MAE (Mean Absolute Error) for forecasting accuracy
- Frequency discovery quality: whether learned f_k align with ground-truth dominant periodicities
- Attribution faithfulness: correlation between A_k and prediction change when removing frequency k

### Key Results

**Forecasting Accuracy:** FreqLens achieves competitive or superior MSE/MAE on Traffic and Weather compared to all baselines, with statistically significant improvements (5 independent runs, different random seeds reported with mean ± std).

**Frequency Discovery (Interpretability Quality):**
- On **Traffic**: All 5 independent runs discover the 24-hour daily cycle (11.8 ± 0.1h, 1.6% error) without any domain knowledge.
- On **Weather**: Discovers both 24-hour daily and 168-hour weekly periodicities from only a 16-hour input window — i.e., it infers cycles 10× longer than the input context from training data statistics.

This demonstrates that FreqLens learns genuine physical structure rather than spurious patterns, directly validating the meaningfulness of its attributions.

### Limitations

1. **Additive decomposition assumption:** Real-world time series sometimes exhibit multiplicative interactions between frequencies (e.g., amplitude modulation). The strict additive structure may underfit such signals.

2. **K selection sensitivity:** The number of frequency components K must be specified as a hyperparameter. Too few K miss important periodicities; too many K increase overfitting risk and make interpretations noisier.

3. **Residual opacity:** The residual MLP r(x) captures non-periodic structure but is itself a black box. For signals with dominant aperiodic components (e.g., trending financial data), the majority of prediction may be unexplained by frequency attributions.

4. **Computational cost:** Learning K independent frequency components with K separate attribution heads increases parameter count over single-model baselines, though the overhead is modest compared to Transformer-based methods.

5. **Evaluation of attribution quality:** The paper evaluates interpretability primarily through frequency discovery (do learned f_k match known ground-truth periods?). Direct human evaluation of whether practitioners find the frequency attributions useful is left for future work.

---

## Practical Applications & Real-World Use Cases

### Energy Grid Management

Smart grids predict electricity demand to balance supply. A grid operator using FreqLens could receive attributions like: "73% of today's peak demand forecast is driven by the 24-hour daily cycle, 18% by the 168-hour weekly pattern, and 9% by aperiodic spikes." This attribution enables operators to:
- Validate that the model is using genuine periodic demand patterns
- Detect when an anomalous aperiodic event (e.g., extreme weather) is dominating
- Explain predictions to regulators and auditors

### Traffic Management

Road occupancy sensors in cities show strong periodic patterns (rush hours, weekends). FreqLens applied to traffic forecasting can reveal whether a prediction of high congestion is primarily driven by the regular morning commute cycle or by a superimposed irregular pattern (event, weather). This distinction matters for dynamic traffic signal control decisions.

### Predictive Maintenance in Manufacturing

Industrial equipment vibrations carry frequency signatures of specific failure modes (bearing wear at ~150 Hz, imbalance at rotational frequency). A FreqLens-based anomaly forecaster can attribute upcoming failure predictions to specific frequency anomalies, directing maintenance crews to investigate the physically relevant failure mode.

### Climate Modeling

Climate models depend on seasonal, annual, and ENSO cycles. FreqLens applied to regional temperature or precipitation forecasting can quantify each periodicity's contribution to a prediction, helping climate scientists validate whether a model relies on physically meaningful cycles or artifacts of the training data.

### Financial Time Series

Treasury yield curves exhibit cycles driven by monetary policy cycles (~4-year), business cycles (~7-year), and short-term liquidity patterns. Frequency attribution enables risk managers to explain to compliance teams which market cycles drive a bond price forecast, addressing BCBS model transparency requirements.

### Regulatory & Compliance Context

**EU AI Act (2024–2026):** High-risk AI systems (energy, transportation, financial infrastructure) require meaningful explanations of outputs. FreqLens's frequency attributions offer a natural explanation format for sequential prediction systems: "the forecast is X primarily because periodicity Y was detected at amplitude Z."

**GDPR Right to Explanation:** For automated decision-making systems using time series inputs (fraud detection based on transaction sequences, medical monitoring), frequency attributions provide a concise, human-readable rationale grounded in periodic structure.

**FDA Software as Medical Device (SaMD):** Medical AI systems processing physiological time series (ECG, EEG) must demonstrate transparency. Frequency attribution aligns with clinical intuition — cardiologists and neurologists already think in terms of signal frequencies (heart rate variability, alpha waves).

---

## Insights & Implications

### Broader Implications for Trustworthy AI

FreqLens demonstrates that it is possible to build models that are simultaneously competitive at prediction and theoretically principled in their explanations — resolving the common accuracy/interpretability tradeoff at the architectural level. This is a significant contribution to the "interpretable by design" research direction, as opposed to post-hoc explanation methods that may be unfaithful to the model's actual computations.

The Shapley equivalence result establishes a concrete bridge between the tabular feature attribution literature (SHAP, Integrated Gradients) and the time series frequency domain — suggesting future unification of attribution frameworks across data modalities.

### Advancing State-of-the-Art in Explainability

The formalization of four frequency attribution axioms (Completeness, Faithfulness, Null-Frequency, Symmetry) creates a rigorous benchmark for comparing any future frequency-domain interpretability method. Just as Shapley axioms enabled systematic evaluation and comparison of tabular attribution methods, the FreqLens axiom system provides the same foundation for sequential data attribution.

### Limitations & Open Questions

1. **Multivariate attribution:** The current framework attributes predictions to frequency components of the input signal. For multivariate time series, it does not decompose attribution across *both* frequency and channel dimensions simultaneously.

2. **Causal vs. correlational attribution:** Frequency attribution describes which periodicities correlate with the forecast, but does not distinguish causal mechanisms from spurious correlations induced by confounders in training data.

3. **Distribution shift:** If the dominant frequencies shift at test time (a new periodic event emerges), the learned frequency bases may no longer be optimal, and attributions could be misleading.

4. **Granularity of residual:** The aperiodic residual is unexplained. For applications requiring full attribution coverage, a secondary interpretation layer over r(x) would be needed.

### Future Research Directions

- Extending axiomatic frequency attribution to non-stationary signals (time-varying frequencies)
- Combining frequency attribution with causal discovery to separate genuine periodic drivers from correlational artifacts
- Human-in-the-loop evaluation studies: do domain experts (grid operators, clinicians) find frequency attributions actionable?
- Hierarchical frequency attribution: attributing across nested periodicities (seconds → minutes → hours → days)

---

## Code & Resources

- **ArXiv Paper:** https://arxiv.org/abs/2602.08768
- **ArXiv HTML:** https://arxiv.org/html/2602.08768
- **Venue:** ACM KDD 2026 (32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining)

### Dependencies & Computational Requirements

Based on the paper's experimental setup:
- **Framework:** PyTorch (standard deep learning stack)
- **Hardware:** GPU recommended (experiments run on standard research GPU hardware)
- **Datasets:** Standard benchmark datasets (ETT, Weather, Traffic, Electricity) available from the Time Series Library (TSlib) repository
- **Baselines code:** Compatible with the TSlib/Time-Series-Library codebase commonly used for evaluation in the time series forecasting community

### Reproducing Results

The paper reports results averaged over 5 independent runs with different random seeds, providing mean ± std for statistical robustness. To reproduce:
1. Use the standard TSlib benchmark datasets (freely downloadable)
2. Configure K (number of frequency components) per dataset according to ablation guidelines in the paper
3. Run with diversity regularization weight τ as specified in the hyperparameter table
4. Compare MSE/MAE against reported baselines (PatchTST, iTransformer, FEDformer, Autoformer, DLinear)

---

## Related Work & Context

### Building On Prior xAI Work

**SHAP (Lundberg & Lee, 2017):** FreqLens's Shapley equivalence result directly inherits SHAP's theoretical guarantees. Unlike SHAP applied to raw time steps, FreqLens computes Shapley-equivalent attributions in the frequency domain at exact O(K) cost — avoiding the exponential complexity of general Shapley computation.

**Integrated Gradients (Sundararajan et al., 2017):** Both methods satisfy an efficiency/completeness axiom. However, Integrated Gradients produces time-level attributions by integrating gradients along an interpolation path, while FreqLens produces frequency-level attributions through exact architectural decomposition.

**LIME (Ribeiro et al., 2016):** Post-hoc approximation that fits a local linear surrogate. FreqLens is fundamentally different — its attributions are exact (not approximations) and are derived from the model's own internal structure (intrinsic interpretability).

### Related Frequency-Domain Forecasting Work

**FEDformer (Zhou et al., 2022):** Uses frequency-enhanced components but with fixed Fourier bases and no attribution framework. FreqLens's learnable bases and axiomatic attributions directly extend this line of work.

**Autoformer (Wu et al., 2021):** Auto-correlation mechanism implicitly identifies periodicity but does not provide explicit frequency attribution. FreqLens makes this implicit structure explicit and attributable.

**TimeKAN (2025):** KAN-based frequency decomposition learning; shares the "learn frequency bases" objective but lacks the axiomatic attribution framework.

**FreDN (2025):** Spectral disentanglement for time series via learnable frequency decomposition — closely related architecture but no formal attribution guarantees.

### Connection to Broader xAI Communities

**Mechanistic Interpretability:** FreqLens shares the "interpretable by design" philosophy — building transparent internal structure rather than explaining post-hoc. The additive decomposition architecture is reminiscent of feature-additive models (GAMs, EBMs) but applied in the frequency domain.

**Feature Attribution Literature:** The Shapley equivalence result connects FreqLens to the extensive tabular SHAP literature, potentially enabling transfer of SHAP-based tools (visualization, interaction detection) to frequency attribution settings.

**Concept-Based Explanations:** Learned frequency components can be viewed as "frequency concepts" — interpretable mid-level representations. This opens a connection to concept-based explanation methods (TCAV, concept bottleneck models) applied to sequential data.

**Unified Attribution Frameworks:** The 2025 paper "Towards Unified Attribution in XAI, Data-Centric AI, and Mechanistic Interpretability" (arXiv:2501.18887) argues that perturbation, gradient, and linear approximation techniques share fundamental similarities across attribution types. FreqLens's frequency-domain Shapley values fit naturally into this unification framework, suggesting that frequency attribution is not a separate silo but part of a broader attribution theory.

---

*Sources:*
- [FreqLens ArXiv Abstract](https://arxiv.org/abs/2602.08768)
- [FreqLens ArXiv HTML](https://arxiv.org/html/2602.08768)
- [Time Series Analysis in Frequency Domain Survey](https://arxiv.org/abs/2504.07099)
- [Towards Unified Attribution in XAI](https://arxiv.org/abs/2501.18887)
