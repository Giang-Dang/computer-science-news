# Interpretability without Actionability: Mechanistic Methods Cannot Correct Language Model Errors Despite Near-Perfect Internal Representations

**ArXiv ID:** [2603.18353](https://arxiv.org/abs/2603.18353)  
**Authors:** Sanjay Basu, Sadiq Y. Patel, Parth Sheth, Bhairavi Muralidharan, Namrata Elamaran, Aakriti Kinra, John Morgan, Rajaie Batniji  
**Date:** March 18, 2026  
**Subfield:** Mechanistic Interpretability  
**Keywords:** mechanistic interpretability, activation steering, sparse autoencoders, clinical AI, knowledge-action gap, interpretability evaluation

---

## Executive Summary

This paper delivers a sobering empirical assessment of current mechanistic interpretability methods: despite LLMs encoding task-relevant knowledge with near-perfect discriminability in their internal representations (98.2% AUROC), existing methods for translating that internal knowledge into corrected outputs fall dramatically short — correcting at most 24% of errors while disrupting correct predictions at nearly the same rate. Tested in a clinical triage setting with physician-adjudicated data, the paper reveals a fundamental "knowledge-action gap" that current MI methods cannot bridge, with important implications for AI safety frameworks that assume interpretability enables error correction.

---

## Problem Statement

The mechanistic interpretability (MI) research program has produced impressive results showing that LLMs encode factual, semantic, and procedural knowledge in identifiable internal representations. The natural next step — and the implicit promise of MI for AI safety — is that this internal knowledge can be leveraged to **correct model errors without full retraining**.

This paper asks: **does MI actually deliver on this promise?**

The use case is high-stakes clinical triage:
- A model reviews clinical vignettes and must flag medical hazards
- The model misses dangerous conditions (false negatives) that could harm patients
- The model's *internal representations* correctly discriminate hazardous from benign cases with 98.2% AUROC
- The question: can MI methods use this internal knowledge to fix the missed hazards?

This is not a hypothetical concern — MI-based error correction is increasingly cited in AI safety proposals as a path toward auditable, correctable AI systems. If it doesn't work, those safety frameworks need revision.

---

## Core Concepts & Theory

### The Knowledge-Action Gap

The paper defines the **knowledge-action gap** formally:

$$\Delta_{KA} = \text{AUROC}_{\text{internal}} - \text{Sensitivity}_{\text{output}}$$

Where:
- $\text{AUROC}_{\text{internal}}$: discriminability of a linear probe trained on internal representations to separate correct vs. incorrect cases
- $\text{Sensitivity}_{\text{output}}$: recall of correct predictions at the output level

In the clinical setting studied: $\Delta_{KA} = 0.982 - 0.451 = 0.531$ — a 53 percentage-point gap.

### The Four MI Methods Tested

**1. Concept Bottleneck Steering (CBS) — Steerling-8B**
- Trains a concept bottleneck model on internal activations
- Uses concept activations to steer outputs toward desired predictions
- Implementation: Steerling-8B architecture

**2. Sparse Autoencoder Feature Steering (SAE-FS)**
- Trains SAEs to decompose residual stream activations
- Identifies features associated with "hazard" concepts
- Steers by adding/subtracting feature vectors

**3. Logit Lens with Activation Patching (LL-AP)**
- Uses logit lens to identify layers where hazard information emerges
- Patches activations from correct examples into incorrect example's forward pass
- Evaluates effect of patching on final output

**4. Truthfulness Separator Vector Steering (TSV) — Qwen 2.5 7B Instruct**
- Extracts a "truthfulness direction" from contrastive examples
- Applies this direction at inference to improve output faithfulness to internal representations

### Evaluation Metrics

For each MI method, the authors measure:
- **Corrected miss rate**: % of originally missed hazards that are now correctly detected
- **Disruption rate**: % of originally correct detections that are now missed due to steering
- **Net gain**: Corrected miss rate − Disruption rate
- **Statistical comparison to random perturbation**: p-value against a null model

---

## Main Ideas & Key Contributions

### 1. Empirical Falsification of MI-Based Error Correction

The paper's primary contribution is **empirically falsifying** the claim that mechanistic interpretability methods can reliably correct LLM errors. The results are striking:

| Method | Corrected Miss Rate | Disruption Rate | Net Gain | vs. Random (p) |
|---|---|---|---|---|
| Concept Bottleneck Steering | 20% | 53% | -33% | p=0.84 (N.S.) |
| SAE Feature Steering | 0% | 0% | 0% | N/A |
| Logit Lens + Activation Patching | 12% | 48% | -36% | p=0.61 (N.S.) |
| TSV Steering (high strength) | 24% | 6% | +18% | p=0.03 |

**Key finding:** Three of four methods are statistically indistinguishable from random perturbation. The best method (TSV) corrects only 24% of errors while leaving 76% uncorrected.

### 2. The SAE Null Effect Paradox

The SAE feature steering result is particularly noteworthy: despite identifying **3,695 statistically significant features** associated with hazard detection, steering on these features produces **zero effect** on output. This suggests a fundamental disconnect between the SAE feature space and the causal pathways governing output generation.

This parallels the findings in arXiv:2604.19974 (functional dissociation paper): just because a feature represents information doesn't mean that feature is causally upstream of the output.

### 3. The Precision-Recall Tradeoff Under Steering

All effective steering methods face a fundamental tradeoff: increasing steering strength to correct more misses inevitably disrupts correct detections. The paper shows this is not a parameter tuning issue but a structural property of the methods — there is no steering strength that achieves high correction with low disruption simultaneously.

### 4. Implications for AI Safety

Current AI safety frameworks (e.g., interpretability-based oversight proposals) implicitly assume that identifying internal knowledge representations is sufficient for correction. This paper shows it is not — the knowledge-action gap is a real obstacle, not a solved problem.

---

## Methodology & Implementation

### Clinical Dataset
- **400 physician-adjudicated clinical vignettes** from real ED (Emergency Department) cases
- 144 hazardous cases (conditions requiring urgent intervention)
- 256 benign cases
- Ground truth established by board-certified emergency physicians

### Models Evaluated
- **Steerling-8B** (Concept Bottleneck Steering)
- **Gemma-2 7B** / **Llama-3 8B** (SAE Feature Steering, Logit Lens)
- **Qwen 2.5 7B Instruct** (TSV Steering)

### Linear Probe Evaluation
- Trained on residual stream activations (layers 8, 16, 24)
- Best layer (layer 16) achieves 98.2% AUROC discriminating hazardous from benign cases
- This confirms the model *has* the relevant information internally

### SAE Training
- 3,695 features identified with significant correlation to hazard labels (FDR-corrected p < 0.05)
- Steering coefficients ranging from ±1 to ±10 tested
- Zero significant effect observed at any steering strength

### Statistical Analysis
- Comparison to random feature steering (10,000 bootstrap samples)
- McNemar's test for corrected vs. disrupted prediction counts
- Bootstrap confidence intervals for all reported rates

### Limitations
- Single clinical domain — generalization to other error-correction tasks unknown
- Binary (hazardous/benign) framing may miss nuanced triage decisions
- All models are 7-8B parameter range; results may differ for larger models
- Clinical vignettes are text-only; real clinical AI includes multimodal data

---

## Practical Applications & Real-World Use Cases

### Clinical AI Safety

The most direct implication: clinical AI systems **cannot be safely deployed** with MI-based error correction as a safety net. Current proposals for "interpretability-audited clinical AI" need to acknowledge that identifying internal representations does not enable reliable correction.

**Alternative safety approaches suggested by these findings:**
- Human-in-the-loop review for all high-stakes decisions
- Calibrated uncertainty quantification rather than post-hoc correction
- Targeted retraining on identified failure cases rather than activation steering

### AI Auditing Frameworks

Regulatory frameworks (EU AI Act, FDA AI/ML guidance) should distinguish between:
1. **Interpretability for understanding**: Feasible with current MI methods (probing, SAEs)
2. **Interpretability for correction**: NOT yet feasible with current MI methods

This suggests that compliance frameworks requiring "explainable and correctable AI" need to specify what level of correctability is achievable.

### Benchmark Setting

The clinical triage dataset and evaluation protocol constitute a valuable benchmark for future MI methods. Any new interpretability-for-correction method should demonstrate performance on this benchmark before claiming practical safety relevance.

---

## Insights & Implications

### The Representation-Causation Gap

The core finding reveals a deeper issue: **representations and causal mechanisms are not the same thing**. A high AUROC probe finding that a representation predicts task performance does not mean that representation is causally upstream of the output. The model might:
1. Use the information in a representation for one computation but not route it to the output
2. Have the information distributed across many features, making any single-feature intervention insufficient
3. Use context-dependent gating mechanisms that the representation probe doesn't capture

### Implications for Mechanistic Interpretability Research

The paper suggests MI research needs to explicitly distinguish:
- **Representational interpretability**: Understanding what information is encoded (currently advanced)
- **Causal interpretability**: Understanding how information flows to influence outputs (still nascent)

Advances in circuit analysis (identifying the causal computational pathways) may be necessary before MI-based error correction becomes viable.

### Advancing State-of-the-Art

The paper establishes a concrete evaluation standard that has been largely absent from MI research: **does understanding the model translate to being able to improve it?** This is a harder and more practically relevant bar than "can we identify a meaningful feature?"

### Open Questions
- What architectural properties would enable the knowledge-action gap to be bridged?
- Is the TSV method's partial success (24% correction) a ceiling or a lower bound for what's possible?
- Can multi-feature steering (addressing distribution of information) outperform single-feature steering?
- Does training explicitly on the knowledge-action gap reduce it?

### Impact on AI Safety Research

This paper should prompt a revision of AI safety frameworks that depend on interpretability-based oversight. The current state of MI does not support the assumption that internal representations can be used to reliably correct behavior — a conclusion that should inform policy, not just technical research.

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2603.18353](https://arxiv.org/abs/2603.18353)
- **Dataset:** Clinical vignettes (upon request from corresponding author)
- **Related Tools:**
  - [SAELens](https://github.com/jbloomAus/SAELens)
  - [TransformerLens](https://github.com/neelnanda-io/TransformerLens)
  - [Steerling](https://github.com/steerling/steerling-8b)

### Reproducing Key Experiments
```python
# Linear probe evaluation (establishing knowledge-action gap)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# Extract residual stream activations at layer 16
activations = extract_activations(model, clinical_vignettes, layer=16)

# Train linear probe
probe = LogisticRegression(max_iter=1000)
probe.fit(activations_train, labels_train)

# Evaluate on test set
probs = probe.predict_proba(activations_test)[:, 1]
auroc = roc_auc_score(labels_test, probs)
print(f"Internal AUROC: {auroc:.3f}")  # Expected: ~0.98

# Compare to model output sensitivity
predictions = model.predict(clinical_vignettes_test)
sensitivity = recall_score(labels_test, predictions)
print(f"Output sensitivity: {sensitivity:.3f}")  # Expected: ~0.45

print(f"Knowledge-action gap: {auroc - sensitivity:.3f}")  # Expected: ~0.53
```

---

## Related Work & Context

### Building On
- **Zou et al. (2023)**: Representation engineering — established that representations can be steered
- **Turner et al. (2023)**: Activation addition for behavior modification
- **Arditi et al. (2024)**: Refusal in LLMs is mediated by a single direction

### Contrasting With (optimistic MI work)
- **Meng et al. (2022)**: ROME — editing factual associations via activation patching (succeeds on simple factual queries)
- **Hernandez et al. (2023)**: Linearity of relational encoding (suggests richer intervention points)

### Related Empirical Critiques
- **Henighan et al. (2023)**: Limitations of mechanistic interpretability for safety
- **Casper et al. (2024)**: Critiques of interpretability-based oversight

### Where This Research Leads
1. Development of MI methods with explicit causal verification (not just correlational probing)
2. Multi-intervention strategies that address the distributed nature of knowledge
3. Training-time interventions to reduce the knowledge-action gap
4. Domain-specific benchmarks for MI evaluation beyond simple factual recall

---

*Sources:*
- [arxiv.org/abs/2603.18353](https://arxiv.org/abs/2603.18353)
