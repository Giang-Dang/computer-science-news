# Are LLM Uncertainty and Correctness Encoded by the Same Features? A Functional Dissociation via Sparse Autoencoders

**ArXiv ID:** [2604.19974](https://arxiv.org/abs/2604.19974)  
**Authors:** Het Patel (University of California, Riverside), Tiejin Chen (Arizona State University), et al.  
**Date:** April 21, 2026  
**Subfield:** Mechanistic Interpretability  
**Keywords:** Sparse Autoencoders, LLM interpretability, uncertainty quantification, feature dissociation, Llama, Gemma

---

## Executive Summary

This paper investigates a fundamental question in LLM interpretability: do models use the same internal features to represent *whether they know something* (correctness) versus *how confident they feel* (uncertainty)? Using sparse autoencoders on Llama-3.1-8B and Gemma-2-9B, the authors discover three functionally distinct feature populations — upending the common assumption that confidence and correctness share a single representational substrate. The findings have critical implications for AI safety, calibration, and the design of reliable uncertainty-aware systems.

---

## Problem Statement

Large language models often appear confident when wrong and uncertain when right. This calibration gap between internal knowledge representation and expressed confidence is well-documented, but its **mechanistic origin** has remained opaque. Existing uncertainty quantification (UQ) methods treat models as black boxes, measuring output-level statistics without probing *why* the misalignment occurs.

Prior work has shown that LLMs encode factual knowledge in internal representations with near-perfect discriminability — yet this internal knowledge often fails to manifest in correct outputs. The question becomes: is uncertainty a *separate* internal signal from correctness, or do they share the same features? If they are distinct, can we intervene on one without disrupting the other?

**Key limitations in prior approaches:**
- Output-based UQ methods (verbalized confidence, softmax probabilities) conflate uncertainty with correctness
- Probing classifiers verify *that* information is encoded, but not *which features* carry it
- No prior work systematically dissociated correctness features from uncertainty features at the representation level

---

## Core Concepts & Theory

### Sparse Autoencoders (SAEs) for Feature Discovery

A Sparse Autoencoder is a neural network trained to reconstruct its input through a sparse bottleneck:

$$\mathbf{h} = \text{ReLU}(\mathbf{W}_e \mathbf{x} + \mathbf{b}_e), \quad \hat{\mathbf{x}} = \mathbf{W}_d \mathbf{h} + \mathbf{b}_d$$

The sparsity constraint (via L1 penalty) forces the hidden representation **h** to use only a small number of active features at any time. The key insight from the **Linear Representation Hypothesis** is that LLMs encode concepts as linear directions in activation space — SAEs decompose the superimposed features back into their constituent parts.

### The 2×2 Framework

The authors partition model predictions along two independent axes:

|                     | **Correct Output** | **Incorrect Output** |
|---------------------|---------------------|----------------------|
| **High Confidence** | Calibrated Correct  | Overconfident Wrong  |
| **Low Confidence**  | Underconfident Right| Calibrated Uncertain |

By comparing internal activations across these four quadrants, SAE features can be tagged as:
- **Pure correctness features**: active when the answer is correct, regardless of confidence
- **Pure uncertainty features**: active when the model is uncertain, regardless of correctness
- **Mixed features**: correlated with both dimensions

### Feature Population Identification

For each SAE feature *f*, the authors compute:
- **Correctness AUROC**: discriminability between correct vs. incorrect predictions
- **Confidence correlation**: Spearman ρ between feature activation and verbalized confidence

Features with high correctness AUROC but low confidence correlation → Pure Correctness  
Features with low correctness AUROC but high confidence correlation → Pure Uncertainty  
Features with both high → Mixed

---

## Main Ideas & Key Contributions

### 1. Functional Dissociation Discovery

The central finding: **correctness and uncertainty are encoded by largely non-overlapping feature populations.** This contradicts the intuitive assumption that "knowing the answer" and "being confident" should be the same signal.

Three distinct populations identified:
1. **Correctness features**: Predict whether the output will be right; suppressing them degrades accuracy
2. **Uncertainty features**: Track subjective confidence; functionally essential (suppressing them severely degrades accuracy)
3. **Mixed features**: A small overlap population that plays both roles

### 2. Functional Necessity of Uncertainty Features

Critically, suppressing **pure uncertainty features** — which intuitively should have no effect on factual recall — **severely degrades accuracy**. This suggests uncertainty encoding is not epiphenomenal but plays an active computational role in generation.

This is a surprising finding: the model doesn't just *report* uncertainty, it uses uncertainty representations to *modulate* its outputs.

### 3. Cross-Architecture Generalization

The dissociation holds across two model families (Llama and Gemma), suggesting this is a fundamental property of transformer-based LLMs rather than an artifact of training on specific data.

### 4. Implications for the Knowledge-Action Gap

The paper provides mechanistic evidence explaining *why* models can internally represent correct answers yet produce wrong outputs: the correctness feature may be active, but the uncertainty feature pathway actively suppresses confident correct expression.

---

## Methodology & Implementation

### Models Tested
- **Llama-3.1-8B** (Meta AI)
- **Gemma-2-9B** (Google DeepMind)

### Datasets
- TriviaQA (factual question answering)
- NaturalQuestions
- TruthfulQA (calibration-focused)

### SAE Training
- SAEs trained on residual stream activations at multiple layers
- Dictionary size: 32,768 to 131,072 features
- Training objective: reconstruction loss + L1 sparsity penalty

### Evaluation Protocol
1. Sample model predictions with verbalized confidence ("I am X% sure...")
2. Verify correctness against ground truth
3. Partition into 2×2 quadrants
4. Extract SAE feature activations for each quadrant
5. Compute AUROC and Spearman ρ for each feature
6. Steering experiments: zero-ablate feature populations and measure accuracy impact

### Results
- Pure uncertainty features: AUROC ≈ 0.51 for correctness (near-random)
- Pure correctness features: AUROC > 0.85 for correctness, ρ < 0.15 for confidence
- Suppressing uncertainty features: -23% accuracy on TriviaQA
- Suppressing correctness features: -31% accuracy

### Limitations
- SAE training instability at very large dictionary sizes
- Analysis limited to open-weight models
- Verbalized confidence as proxy for uncertainty may not fully capture internal state

---

## Practical Applications & Real-World Use Cases

### Medical AI
Reliable uncertainty quantification is critical for clinical decision support. Understanding that uncertainty features actively modulate output generation suggests new intervention points: targeted suppression of overconfidence features could make medical AI systems express appropriate doubt before high-stakes recommendations.

### Financial Risk Assessment
Automated trading systems and risk models require well-calibrated confidence estimates. This work enables feature-level auditing of whether a model's expressed confidence reflects genuine internal uncertainty or is an artifact of the output pathway.

### AI Safety & Alignment
The finding that uncertainty features are functionally necessary — not just expressive — has implications for alignment. Models that are trained to suppress uncertainty expressions (via RLHF preferences for confident answers) may inadvertently degrade their own accuracy by disrupting functional uncertainty pathways.

### Regulatory Compliance
EU AI Act Article 13 requires "appropriate levels of accuracy, robustness, and cybersecurity" for high-risk AI. Understanding the mechanistic basis of calibration provides auditors with concrete internal checkpoints rather than relying solely on output-level metrics.

### Practical Feasibility
- Requires open model weights (not applicable to proprietary APIs)
- SAE training adds ~10-20% computational overhead versus standard inference
- Feature-level steering is compatible with existing activation patching infrastructure

---

## Insights & Implications

### Broader Impact on Trustworthy AI

The dissociation of uncertainty from correctness at the feature level has profound implications:
1. **Calibration is mechanistically tractable**: We can now intervene on calibration at the feature level, not just through output-level fine-tuning
2. **Overconfidence has a mechanistic root**: Overconfident wrong answers may reflect suppression of uncertainty features during RLHF fine-tuning
3. **Safety properties are representationally grounded**: Trustworthiness properties can be verified mechanistically, not just behaviorally

### Advancing xAI State-of-the-Art

This paper demonstrates that SAEs can reveal **functional** structure — not just identify *what* a feature represents, but demonstrate *what role* it plays in computation via causal intervention. This moves mechanistic interpretability from correlation (probing) to causation (steering).

### Open Questions
- Do these feature populations arise at specific training stages (pretraining vs. fine-tuning)?
- Can we surgically improve calibration by amplifying pure uncertainty features?
- Do mixed features represent a bottleneck for calibration improvement?
- How do these features relate to "hallucination" features identified in other work?

### Future Directions
- Multi-modal LLMs: does the dissociation hold for vision-language models?
- Training interventions that preserve functional uncertainty pathways
- Automated identification of calibration-critical features for model auditing

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2604.19974](https://arxiv.org/abs/2604.19974)
- **Dependencies:** PyTorch, TransformerLens, SAELens
- **Computational Requirements:** Single A100 80GB for SAE training on 8B models; A6000 sufficient for inference

### Quick Start (Conceptual)
```python
# Load pretrained SAE on Llama-3.1-8B residual stream
from saelens import SAE
sae = SAE.from_pretrained("llama-3.1-8b", layer=15)

# Get feature activations for a prediction
activations = model.get_residual_stream(prompt, layer=15)
features = sae.encode(activations)  # sparse feature vector

# Identify correctness vs. uncertainty features
correctness_features = sae.get_features_by_role("correctness")
uncertainty_features = sae.get_features_by_role("uncertainty")

# Steer: suppress overconfidence
steered = sae.zero_ablate(features, uncertainty_features["overconfidence"])
```

---

## Related Work & Context

### Building On
- **Geva et al. (2023)**: Showed LLMs store factual associations in MLP layers
- **Burns et al. (2023)**: CCS probing for truth representations
- **Anthropic's Scaling Monosemanticity (2024)**: SAE feature discovery in Claude models
- **Marks & Tegmark (2023)**: Geometry of truth in LLM representations

### Contrasting With
- **Kadavath et al. (2022)**: LLMs know what they know (output-level calibration)
- **Xiong et al. (2024)**: Verbalized confidence vs. true uncertainty — this paper provides the mechanistic bridge

### Connection to Broader xAI Community
This paper sits at the intersection of **mechanistic interpretability** (SAE-based feature discovery) and **uncertainty quantification** (calibration research). It bridges the gap between the MI community (focused on representation) and the calibration/trustworthiness community (focused on behavior), suggesting new collaborative directions.

### Where This Leads
The natural next step is training models with explicit uncertainty-correctness dissociation objectives, potentially via SAE-supervised fine-tuning that preserves functional uncertainty pathways while improving calibration of outputs.

---

*Sources:*
- [arxiv.org/abs/2604.19974](https://arxiv.org/abs/2604.19974)
