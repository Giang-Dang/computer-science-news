# Mechanistic Interpretability of Fine-Tuned Vision Transformers on Distorted Images: Decoding Attention Head Behavior for Transparent and Trustworthy AI

## Executive Summary

This paper applies mechanistic interpretability techniques to understand how Vision Transformers (ViTs) process visual information when fine-tuned on spectrogram images containing extraneous, non-task-relevant features (such as axis labels, titles, and color bars). By analyzing individual attention heads across layers, the work reveals differential contributions of transformer components to task performance and provides insights into mechanisms for transparent and trustworthy vision-based AI systems.

**Paper Details:**
- **Title:** Mechanistic Interpretability of Fine-Tuned Vision Transformers on Distorted Images: Decoding Attention Head Behavior for Transparent and Trustworthy AI
- **Author:** Nooshin Bahador
- **ArXiv ID:** [2503.18762](https://arxiv.org/abs/2503.18762)
- **Submitted:** March 24, 2025
- **Length:** 15 pages with 8 figures
- **Subject Areas:** Machine Learning (cs.LG); Artificial Intelligence (cs.AI)

---

## Problem Statement

### Current Challenges in Vision Transformer Interpretability

While Vision Transformers have achieved state-of-the-art performance on many computer vision tasks, their internal mechanisms remain largely opaque. Traditional feature visualization and attribution methods provide limited insights into *how and why* specific architectural components (attention heads, layers) contribute to predictions. This opacity creates challenges for:

1. **Model Debugging:** Identifying which components are responsible for spurious correlations or artifacts
2. **Safety and Robustness:** Understanding whether models rely on task-relevant features or irrelevant contextual information
3. **Trustworthiness:** Establishing confidence in predictions when task-relevant and task-irrelevant information coexist
4. **Transfer Learning:** Understanding what features are learned during fine-tuning on distorted or contaminated data

### Specific Motivation: Distorted Spectrograms

The paper focuses on an especially relevant scenario: vision models fine-tuned on distorted 2D spectrogram images containing extraneous visual elements (axis labels, color bars, titles). This situation mirrors real-world challenges where:
- Training data contains metadata or annotations
- Images are preprocessed with variable formatting
- Models must ignore contextual or visual "noise" to focus on actual signal content

Understanding how ViTs handle such distractions is critical for deploying them in safety-critical domains like audio classification (speech, environmental sounds) or signal processing.

---

## Core Concepts & Theory

### Mechanistic Interpretability Framework

Mechanistic interpretability aims to reverse-engineer neural networks by studying individual components (neurons, attention heads, layers) and their causal contributions to model behavior. Unlike post-hoc explanation methods (LIME, SHAP, saliency maps) that approximate models after training, mechanistic approaches intervene on the network to measure direct causal effects.

**Key Techniques Used:**

1. **Attention Head Analysis:**
   - Examine attention weight distributions across layers
   - Visualize which spatial regions (or features) each head attends to
   - Measure how strongly each head focuses on task-relevant vs. extraneous features

2. **Ablation Studies:**
   - Systematically remove (ablate) individual attention heads
   - Measure the change in model performance (e.g., MSE loss increase)
   - Quantify the causal contribution of each head to the task

3. **Layer-wise Contribution Assessment:**
   - Compare early layers (processing low-level visual features) vs. deeper layers (processing semantic information)
   - Determine which layers are most critical for task performance
   - Identify redundancy and specialization within the architecture

### Vision Transformer Architecture

Vision Transformers (ViTs) divide images into non-overlapping patches, embed them as sequences, and process them through multi-head self-attention layers:

```
Input Image
    ↓
Patch Embedding (e.g., 16×16 patches)
    ↓
Linear Projection + Positional Encoding
    ↓
Multi-Head Self-Attention Layer 1
    ↓
Feed-Forward Layer 1
    ↓
... (repeat for multiple layers)
    ↓
Classification Head (e.g., MSE loss for regression)
```

Each attention head in a multi-head attention layer learns to weight relationships between patches. By studying which patches (or regions) each head attends to, we gain insight into the visual features the model considers important.

### Extraneous Features in Spectrograms

A spectrogram is a time-frequency representation of a signal. A typical 2D spectrogram image contains:
- **Task-relevant content:** The frequency and temporal patterns of the underlying signal (e.g., audio pitch, frequency characteristics)
- **Extraneous features:** Axis labels, color bars, titles, frame borders

The model should rely on the frequency-time patterns, not the axis labels. By systematically adding extraneous features, we create a controlled test of whether ViTs robustly focus on task-relevant information.

---

## Main Ideas & Key Contributions

### 1. **Differential Layer Contributions**

The paper's central finding is that attention heads exhibit layer-dependent importance:

- **Early Layers (1-3):** Show minimal task impact. Ablation studies reveal that removing heads from early layers increases MSE loss by only ~0.11% (σ=0.09%), indicating these heads focus on low-level or redundant visual features.

- **Deep Layers (e.g., Layer 6):** Show significantly higher task importance. Ablating heads from deeper layers increases loss by ~0.34% (σ=0.02%), demonstrating these heads perform critical computations for the final prediction.

**Interpretation:** Early layers may process patch-level details (patch boundaries, local color variations) and extraneous visual elements (e.g., axis text). Deeper layers synthesize this information to extract task-relevant frequency-time patterns.

### 2. **Mechanistic Understanding of Vision Transformer Specialization**

By studying attention weight patterns and ablation impacts, the paper reveals that:
- Different heads specialize in different aspects of the input
- Redundancy exists across heads (multiple heads perform similar roles)
- The architecture exhibits a clear hierarchy: low-level feature extraction (early) → semantic synthesis (deep)

### 3. **Implications for Robustness and Debiasing**

Understanding which heads process extraneous features enables:
- **Targeted interventions:** Suppress or regularize early-layer attention to distractors
- **Robustness testing:** Systematically vary extraneous features and monitor model stability
- **Debiasing:** Identify and mitigate reliance on spurious correlations

### 4. **Practical Mechanistic Tools**

The authors provide:
- Python packages for extracting and visualizing attention maps
- Code for conducting layer-wise ablation studies
- Synthetic datasets for reproducible experiments

This democratizes mechanistic interpretability research beyond large language models (where it is more common) to vision models.

---

## Methodology & Implementation

### Experimental Setup

**Task:** Chirp Localization from Spectrograms
- **Dataset:** 100,000 synthetic 2D spectrogram images
- **Signal Type:** Chirps (frequency-swept sinusoids) with known start and end frequencies
- **Extraneous Elements:** Synthetic axis labels, color bars, frame borders
- **Prediction Target:** Exact chirp frequency range (regression task, evaluated with MSE loss)

**Model Architecture:**
- **Base Model:** Vision Transformer (ViT-B or similar size)
- **Fine-tuning:** Trained on the synthetic spectrogram dataset
- **Input Resolution:** Standard spectrogram resolution (e.g., 224×224 or 256×256 patches)

### Ablation Methodology

For each of the N attention heads in the model:

1. Remove the head from the architecture
2. Forward pass all test samples through the ablated model
3. Measure MSE loss: **ΔLoss_head_i = Loss_ablated - Loss_baseline**
4. Compute statistics: mean (μ) and standard deviation (σ) of per-sample loss increases

This provides a direct causal measure: "How much does this specific head contribute to reducing the task loss?"

### Evaluation Metrics

1. **Mean Loss Increase (μ):** Average task performance degradation when head is removed
2. **Standard Deviation (σ):** Variability of the loss increase across test samples
3. **Relative Importance:** Layer-wise aggregation to compare early vs. deep layer contributions
4. **Attention Map Visualization:** Qualitative inspection of which spatial regions heads attend to

### Results Summary

**Key Quantitative Findings:**

| Layer Group | Mean Loss Increase (μ) | Std Dev (σ) | Interpretation |
|-------------|----------------------|-------------|------------------|
| Early (1-3) | ~0.11% | ~0.09% | Minimal task impact; likely redundant or noise-focused |
| Deep (5-6)  | ~0.34% | ~0.02% | Critical for task; consistent across samples |

**Qualitative Findings:**

- Early-layer attention heads spread weight across patches with no clear spatial focus, suggesting processing of low-level features or extraneous elements
- Deep-layer heads show concentrated attention on frequency-time regions with task-relevant patterns
- Some heads in mid-layers specialize in spatial relationships between patches

### Limitations

1. **Synthetic Data:** Experiments use synthetic spectrograms; behavior on real-world audio spectrograms may differ (shift to real data needed for deployment)
2. **Single Task:** Evaluated only on chirp localization; generalizability to other spectrogram tasks (speech recognition, environmental sound classification) unexplored
3. **Single Model Architecture:** Only ViT studied; how findings transfer to other vision architectures (CNNs, Swin Transformers, etc.) unclear
4. **Lack of Theoretical Grounding:** While empirical results are clear, mechanistic explanations of *why* layers specialize remain interpretive rather than theoretical
5. **Computational Cost:** Ablation studies require N+1 forward passes (expensive for large models); scalability to massive transformers unclear

---

## Practical Applications & Real-World Use Cases

### 1. **Audio Processing and Signal Classification**

**Domain:** Speech recognition, environmental sound classification, bioacoustic monitoring

**Application:**
- Audio spectrograms often contain artifacts (background noise, preprocessing metadata, frame borders)
- Understanding which model components focus on actual acoustic content vs. artifacts improves robustness
- Mechanistic insights enable selective regularization of early layers to suppress attention to noise

**Example:** A speech recognition model fine-tuned on data where spectrograms include variable axis labels should ignore those labels. Mechanistic interpretability identifies which heads process label information, enabling targeted debiasing.

### 2. **Medical Imaging and Diagnostic Systems**

**Domain:** X-ray, MRI, ultrasound image analysis

**Application:**
- Medical images often contain metadata (patient IDs, timestamps, scanner calibration marks)
- Models must focus on diagnostic features, not metadata
- Mechanistic understanding helps verify that models ignore non-clinical artifacts
- Supports regulatory requirements (FDA clearance) by providing transparency into what the model "sees"

**Example:** A ViT-based lung lesion detector should ignore frame borders and timestamps in X-ray images. Ablation studies confirm that early-layer heads focusing on borders contribute negligibly to predictions.

### 3. **Quality Control and Robustness Testing**

**Domain:** Manufacturing, autonomous systems, industrial applications

**Application:**
- Ensure models are robust to irrelevant variations in image formatting or capture conditions
- Identify which components are sensitive to extraneous features
- Design training curricula or data augmentation to suppress such sensitivities

**Example:** A quality control system inspecting manufactured parts should ignore variations in lighting, camera angle labels, or timestamp overlays. Mechanistic interpretability reveals whether early layers fall prey to these factors.

### 4. **Model Debugging and Bias Mitigation**

**Domain:** Fairness, debiasing, explainability audits

**Application:**
- When models exhibit unexpected behavior (e.g., spurious correlations, dataset biases), mechanistic analysis identifies which components are responsible
- Enables targeted interventions: regularize, prune, or retrain specific layers
- Supports auditing efforts for trustworthy AI deployment

**Example:** If a facial recognition model exhibits gender or race bias, mechanistic analysis can identify which layers or heads are sensitive to demographic attributes, enabling precise mitigation strategies.

### 5. **Regulatory and Compliance Requirements**

**Standards:** FDA 21 CFR Part 11 (software validation), EU AI Act (transparency requirements), GDPR (explainability for automated decisions)

**Relevance:**
- Mechanistic interpretability provides algorithmic transparency required by regulators
- Supports "opening the black box" claims in medical device applications
- Demonstrates rigorous understanding of model internals, increasing confidence in safety and robustness
- Enables post-hoc validation: verify that models learned interpretable, domain-relevant features

---

## Insights & Implications

### 1. **Vision Transformers Show Clear Hierarchical Structure**

The differential layer contributions mirror findings from mechanistic interpretability studies of language models (e.g., sparse autoencoders in LLMs). Vision transformers also exhibit:
- **Low-level feature processing** in early layers
- **Semantic synthesis** in middle layers  
- **Task-specific refinement** in deep layers

This suggests mechanistic interpretability as a unifying framework across modalities.

### 2. **Robustness and Interpretability Are Intertwined**

Models that cleanly separate task-relevant from task-irrelevant features are both:
- **More interpretable:** We can understand why predictions are made
- **More robust:** Less susceptible to dataset artifacts or adversarial perturbations

Mechanistic analysis thus serves dual purposes: transparency and safety.

### 3. **Early Layers May Be "Artifact Processors"**

The finding that early layers have minimal task impact suggests they may be:
- Processing extraneous visual information (axis labels, frames)
- Serving as filters or feature normalizers
- Redundant or over-parameterized

**Future Direction:** Pruning or regularizing early-layer heads could improve model efficiency and robustness without sacrificing performance.

### 4. **Limitation: Synthetic Data Gap**

While synthetic spectrograms enable controlled experiments, real-world spectrogram data (from actual audio) may exhibit different properties. Future work should:
- Validate findings on real audio spectrograms (speech, music, environmental sounds)
- Study task transfer: Do layer contributions remain consistent across different audio classification tasks?
- Investigate fine-tuning dynamics: How do layer contributions change during training?

### 5. **Broader Impact on Mechanistic Interpretability**

This work extends mechanistic interpretability beyond language models to vision models, suggesting:
- **Generality of techniques:** Attention-based analysis works across modalities
- **Scalability:** Methods can be applied to vision transformers of various scales
- **Practical utility:** Mechanistic tools support real deployment challenges (robustness, fairness, compliance)

### Open Questions

1. How do findings generalize to fine-tuned models in other domains (medical imaging, remote sensing)?
2. Can mechanistic insights inform architectural design of more robust vision transformers?
3. How do layer contributions shift during adversarial training or on out-of-distribution data?
4. Can early-layer pruning improve efficiency without harming robustness?

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** [2503.18762 - Mechanistic Interpretability of Fine-Tuned Vision Transformers](https://arxiv.org/abs/2503.18762)
  - [PDF Version](https://arxiv.org/pdf/2503.18762)
  - [HTML Version](https://arxiv.org/html/2503.18762v1)

- **ResearchGate:** [(PDF) Mechanistic Interpretability of Fine-Tuned Vision Transformers on Distorted Images](https://www.researchgate.net/publication/390142791_Mechanistic_Interpretability_of_Fine-Tuned_Vision_Transformers_on_Distorted_Images_Decoding_Attention_Head_Behavior_for_Transparent_and_Trustworthy_AI)

### Implementation Resources

**Available from Authors:**
- Python packages for attention map extraction
- Ablation study code and evaluation scripts
- Pre-trained Vision Transformer on synthetic spectrograms
- Synthetic spectrogram dataset (100,000 samples)

**Dependencies (Estimated):**
- PyTorch (neural network framework)
- Timm (Vision Transformer implementations)
- NumPy, Matplotlib (numerical computing, visualization)
- Standard scientific Python stack

**Computational Requirements:**
- GPU recommended for forward passes and ablation studies
- Ablation study: ~N+1 forward passes (where N = number of heads)
- For ViT-B: ~12 layers × 12 heads = 144 ablations per sample

### Quick Start (Conceptual)

```python
import torch
from vit_model import ViT

# Load trained model
model = ViT.from_pretrained("vit_spectrogram")

# Extract attention weights for a sample
sample = spectrogram_dataset[0]
with torch.no_grad():
    attention_maps = model.get_attention_maps(sample)
    # Shape: (num_layers, num_heads, num_patches, num_patches)

# Ablate a single head and measure loss impact
model_ablated = model.clone()
model_ablated.layers[layer_idx].heads[head_idx].disabled = True
loss_ablated = compute_loss(model_ablated, sample)
loss_delta = loss_ablated - loss_baseline

print(f"Loss increase from ablating Layer {layer_idx}, Head {head_idx}: {loss_delta:.2%}")
```

### Related Tools and Libraries

1. **TransformerLens** (mechanistic interpretability for language models; vision extensions emerging)
2. **Captum** (PyTorch interpretability library with attention analysis tools)
3. **ViT-Lens** (vision transformer visualization and analysis toolkit)

---

## Related Work & Context

### Connection to Broader Mechanistic Interpretability Research

This paper builds on a growing body of mechanistic interpretability work, traditionally focused on language models:

1. **Sparse Autoencoders for LLMs** (Bricken et al., Dunefsky et al.)
   - Decompose transformer activations into interpretable features
   - Vision transformer extensions emerging but less explored
   - Current work studies attention heads directly (complementary to feature-level analysis)

2. **Circuit Analysis** (Anthropic, Redwood Research)
   - Identify subsets of weights/activations critical for specific behaviors
   - Current work applies ablation methodology to vision domain

3. **Causal Tracing and Intervention Studies** (Meng et al., Fineberg et al.)
   - Systematically modify model internals to measure causal effects
   - Current work adapts intervention to vision architecture (attention head ablation)

### Related Vision Transformer Interpretability Work

1. **"Seeing Through Circuits" (Spring 2025 work)**
   - Extends mechanistic interpretability circuits to vision transformers
   - Focuses on identifying sub-circuits responsible for specific visual behaviors

2. **"Sparse but not Simpler: A Multi-Level Interpretability Analysis of Vision Transformers"** (2603.15919)
   - Multi-level analysis combining neuron-level, head-level, and layer-level interpretation
   - Overlapping motivation but broader scope than current paper

3. **Vision Transformer Attention Pattern Analysis** (various works)
   - Visualize and understand what patches attention heads focus on
   - Current work extends beyond visualization to quantitative ablation studies

### Connection to Feature Attribution and Saliency Methods

Unlike traditional post-hoc explanation methods:
- **LIME, SHAP:** Model-agnostic approximations (slower, less precise)
- **Gradient-based saliency:** Sensitive to noise, gradient saturation issues
- **Mechanistic ablation (current approach):** Direct intervention on model components, ground-truth causal effects

**Trade-off:** Mechanistic approaches require white-box model access and computational cost but provide clearer causal insights.

### Future Research Directions

1. **Scale to Real Data:** Validate on natural image/audio datasets (ImageNet, AudioSet, speech corpora)
2. **Layer Pruning and Efficiency:** Use ablation insights to design pruned, efficient vision transformers
3. **Cross-Domain Transfer:** How do layer contributions change when transferring from synthetic to real data, or across different vision tasks?
4. **Adversarial Robustness:** Do mechanistically robust layers (those focusing on task-relevant features) remain robust under adversarial attacks?
5. **Foundation Model Analysis:** Apply to large vision-language models (CLIP, BLIP) where mechanistic transparency is critical for trustworthy deployment

---

## Summary

This paper advances mechanistic interpretability for vision transformers by:

1. Providing empirical evidence that ViT layers exhibit differential task contributions
2. Introducing ablation-based quantification of head importance
3. Revealing that early layers are largely redundant or process task-irrelevant features
4. Demonstrating practical tools for analyzing vision model internals
5. Laying groundwork for more transparent, robust, and debuggable vision systems

**Impact:** Opens mechanistic interpretability research to the vision domain, supporting trustworthy AI deployment in safety-critical applications (medical imaging, autonomous systems, etc.).

---

## References

### Primary Source
- Bahador, N. (2025). [Mechanistic Interpretability of Fine-Tuned Vision Transformers on Distorted Images: Decoding Attention Head Behavior for Transparent and Trustworthy AI](https://arxiv.org/abs/2503.18762). *arXiv preprint arXiv:2503.18762*.

### Related Mechanistic Interpretability Papers
- Bricken, T., et al. (2023). [Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](https://arxiv.org/abs/2301.00378).
- Meng, K., et al. (2023). [Locating and Editing Factual Associations in Transformers](https://arxiv.org/abs/2202.05262).
- Cammarata, N., et al. (2020). [Curve Detectors](https://distill.pub/2019/computing-receptive-fields/).

### Vision Transformer Papers
- Dosovitskiy, A., et al. (2021). [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929).
- Liu, Z., et al. (2021). [Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030).

### Explainability and Robustness
- Ribeiro, M. T., et al. (2016). ["Why Should I Trust You?": Explaining the Predictions of Any Classifier](https://arxiv.org/abs/1602.04938) (LIME).
- Lundberg, S. M., & Lee, S. I. (2017). [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874) (SHAP).
