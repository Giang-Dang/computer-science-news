# Attention-Guided Saliency Maps for Interpreting Visualization Literacy in Vision-Language Models

**ArXiv ID:** [2607.16105](https://arxiv.org/abs/2607.16105)

**Authors:** Maeve Hutchinson, Abderrahmane Wassim Mehdaoui, Pranava Madhyastha

**Submitted:** July 17, 2026

**Venue:** IEEE VIS 2026

---

## Executive Summary

This paper addresses a critical gap in explainability for vision-language models (VLMs) by introducing a lightweight, gradient-free saliency attribution method specifically designed for understanding how VLMs interpret data visualizations. The authors propose aggregating attention across all transformer heads and layers to create visual saliency maps that reveal which image regions a VLM attended to when generating text answers to chart questions. This work advances explainability for visualization understanding in VLMs, enabling practitioners to verify whether model predictions are grounded in relevant visual features rather than spurious patterns.

---

## Problem Statement

### The Challenge

Vision-language models are increasingly deployed for analytical tasks requiring interpretation of data visualizations—charts, graphs, and scientific figures. However, unlike traditional feature attribution methods for image classification, there is limited understanding of how VLMs read structured visual data and generate explanations. The core interpretability challenge is:

- **Opacity in multimodal reasoning:** When a VLM answers a chart question, it is unclear which visual elements (axes, data marks, legends) it actually attended to.
- **Faithfulness of attention:** Prior work on attention visualization has shown that attention weights can be redistributed without significantly changing model outputs, raising questions about whether attention maps truly reflect causal contributions.
- **Lack of domain-specific tools:** Existing saliency methods (e.g., Grad-CAM) are computationally expensive for transformer-based VLMs and not tailored to chart question-answering (QA) tasks.

### Limitations in Prior Work

1. **Gradient-based methods (Attention-Guided Grad-CAM):** Slow to compute for large models; require backpropagation through the full network.
2. **Naive attention visualization:** Raw attention weights lack spatial grounding and may not correlate with model output.
3. **Evaluation gaps:** Most post-hoc explanation methods lack rigorous evaluation of whether saliency maps actually explain the model's behavior.

---

## Core Concepts & Theory

### Saliency Maps for Vision-Language Models

Saliency maps visualize which input features (pixels, image patches) a model attends to when making predictions. For transformers processing images and text:

- **Visual tokens:** An image encoder (e.g., Vision Transformer) converts an image into a sequence of patch embeddings. A VLM's language model then generates text tokens, each influenced by specific visual patches.
- **Attention as proxy for importance:** While imperfect, attention weights indicate which tokens a layer consults. By aggregating attention across heads and layers, we can approximate the importance of each input region.

### Gradient-Free Aggregation

The paper contrasts gradient-free attention aggregation with gradient-based methods:

```
Gradient-Free: attention_saliency(image) = Σ(attention weights over all heads/layers)
Gradient-Based: saliency(image) = gradient_norm(output, image)
```

**Advantages of gradient-free:**
- No backpropagation needed; faster inference.
- Interpretable: directly uses learned attention weights.
- Suitable for post-hoc analysis without model modification.

---

## Main Ideas & Key Contributions

### 1. **Attention Aggregation for VLM Chart Understanding**

The core method aggregates the language model's attention over visual tokens across all transformer heads and layers, then maps this aggregation onto the vision encoder's patch grid. For a chart question, each generated token (e.g., "The", "highest", "value") receives a saliency map showing which chart regions influenced it.

**Algorithm (simplified):**
1. Given an image and query (e.g., "What is the highest data value?"), forward pass through VLM.
2. For each generated output token, extract attention weights from the language model over the visual patch tokens.
3. Sum attention weights across all heads and layers.
4. Project the summed attention back onto the image coordinate space (via the vision encoder's patch grid).
5. Visualize as a heatmap overlaid on the chart.

### 2. **Lightweight Computational Design**

The method requires only a single forward pass, avoiding gradient computation. This makes it practical for interactive applications and large-scale evaluation.

### 3. **Validation via Deletion Testing**

To verify that saliency maps actually reflect causal importance, the authors use **deletion-based faithfulness evaluation:**

- **Procedure:** Progressively remove patches in order of saliency rank (highest saliency first).
- **Expectation:** Model accuracy should drop sharply if deletion targets important patches.
- **Finding:** Reported that accuracy drops quickly when removing top-ranked pixels, validating the causal connection between saliency scores and model behavior.

---

## Methodology & Implementation

### Experimental Setup

**VLMs Evaluated:** 
- Open-source: ChartGemma (3B, fine-tuned for chart QA), Janus (1B and 7B)
- Closed-source: GPT-4o, Gemini 1.5 Pro

**Datasets:**
- **Mini-VLAT:** A 12-item shortened form of the Visualization Literacy Assessment Test (VLAT). Preserves psychometric properties of the full 53-item test while reducing completion time by ~80%. Includes 12 diverse chart types.
- **VLAT:** The full 53-item benchmark covering varied chart types (bar, line, scatter, pie) and reasoning tasks (direct reading, interpolation, reasoning).

**Evaluation Metrics:**
- **Deletion-based faithfulness:** Area Under the Curve (AUC) of accuracy vs. deletion rank. Higher AUC indicates stronger saliency-output alignment.
- **Literacy task accuracy:** Percentage correct on chart QA tasks.

### Key Experimental Results

[Exact figures unavailable — see full paper]

However, the authors report:
- **Faithfulness validation:** Saliency maps demonstrate causal connection to model outputs via deletion tests (sharp accuracy drops upon removing high-saliency patches).
- **Visualization grounding:** The generated saliency maps align with chart structure (e.g., localizing to data marks when answering about values, to axes when identifying scales).
- **Model differences:** Different models show varying attention patterns; some models focus on labels while others rely more on visual marks.
- **Limitation:** Some saliency maps show partially plausible or spurious attention, suggesting that attention, while useful, captures only part of the reasoning process.

### Practical Implications

The method enables practitioners to:
- **Audit model decisions:** Verify that a model's chart answer is grounded in relevant regions.
- **Identify failure modes:** Detect when models attend to misleading or irrelevant visual elements.
- **Debug generalization:** Understand whether models generalize via robust features or chart artifacts.

---

## Practical Applications & Real-World Use Cases

### 1. **Accessibility and Verification in Data Analytics**

Vision-language models are deployed in analytics platforms to help users understand data. Saliency maps provide:
- **Blind and low-vision users:** Detailed grounding of model explanations ("The model looked at this bar" rather than abstract descriptions).
- **Data literacy:** Transparent evidence that models perform chart reasoning correctly, not by memorizing spurious patterns.

### 2. **Scientific Figure Interpretation**

In research contexts, VLMs are used to extract insights from figures. Explainability ensures:
- **Reproducibility:** Researchers can verify that models focus on relevant plot elements.
- **Limitation awareness:** Salient but misleading visual elements (e.g., decorative chart backgrounds) can be identified and corrected.

### 3. **Regulatory and Compliance Applications**

Under regulations like the EU AI Act, models must provide explanations for high-stakes decisions:
- **Fairness audits:** Saliency maps reveal whether models treat data from different demographic groups equally.
- **Robustness validation:** Deletion tests provide evidence of causal importance, supporting regulatory compliance claims.

### 4. **Interactive Visualization Tools**

Lightweight gradient-free saliency maps enable real-time interactive debugging:
- **Hover-to-explain:** As users explore visualizations, tools can show saliency maps for model predictions.
- **Comparison tools:** Side-by-side saliency maps for different models or prompt variations.

---

## Insights & Implications

### Broader Contributions to Explainability

1. **Attention aggregation as a practical method:** Demonstrates that simple, interpretable aggregation of learned attention weights can provide faithful explanations without gradient computation. This reduces the barrier to adoption in practice.

2. **Visualization literacy as an explainability testbed:** Chart QA is a well-defined, human-evaluable task with standardized benchmarks (VLAT, Mini-VLAT). This creates a rigorous setting for developing and validating explanation methods.

3. **Gradient-free alternatives matter:** Shows that computational efficiency and simplicity are features, not bugs. Practitioners often prefer interpretable, fast methods over complex ones.

### Limitations and Open Questions

1. **Attention ≠ Causation:** While deletion tests validate saliency maps, attention mechanisms may not fully capture causal relationships. Attention can be redistributed or masked without changing outputs (polysemanticity, attention redundancy).

2. **Architectural dependence:** The method assumes a specific ViT-LLM architecture where visual tokens are distinct and traceable. Generalization to other architectures (e.g., unified visual embeddings) is unclear.

3. **Partial faithfulness:** Some models exhibit attention patterns that partially align with ground truth reasoning. The paper acknowledges cases where saliency maps are "only partially plausible," suggesting the method captures incomplete explanations.

4. **Evaluation rigor:** While deletion tests provide one form of validation, they don't address whether saliency maps align with human interpretations of what models should attend to.

### Future Research Directions

- **Multimodal explanations:** Extending saliency maps to explain reasoning across text, image, and structured data (e.g., table captions, data schemas).
- **Mechanistic integration:** Combining saliency maps with mechanistic interpretability to understand not just which patches are attended to, but what features they compute.
- **Human-centered evaluation:** Comparing model saliency maps to human eye-tracking or reasoning explanations to ground explainability in human understanding.
- **Prompt sensitivity:** Studying how saliency maps vary with prompt wording, enabling practitioners to design prompts that elicit reliable, focused attention.

---

## Code & Resources

### Official Implementation

- **ArXiv page:** [2607.16105](https://arxiv.org/abs/2607.16105)
- **Code availability:** Check the arXiv abstract page for linked repositories (no specific GitHub URL confirmed in search results).

### Related Benchmarks and Tools

- **Mini-VLAT & VLAT:** Standardized visualization literacy benchmarks.
  - Reference: Li et al., "Visualization Literacy of Multimodal Large Language Models: A Comparative Study" (arXiv 2407.10996)
- **ChartGemma:** 3B VLM fine-tuned for chart QA; used in evaluation.
- **Possible related visualization tools:** uw-insight-lab/Probing-Vis-Literacy-of-VLMs on Hugging Face Spaces (third-party, not confirmed as official implementation).

### Quick Start Guide

[Exact setup unavailable — see full paper]

Typical usage:
1. Load a VLM (e.g., ChartGemma, LLaVA).
2. Provide an image (chart) and query.
3. Forward pass; extract language-model attention over visual tokens.
4. Aggregate attention across heads and layers.
5. Normalize and project onto image coordinates.
6. Visualize as heatmap overlay.

### Computational Requirements

- **Inference:** Single forward pass (no gradient computation).
- **Speed:** Faster than Grad-CAM variants due to no backpropagation.
- **Memory:** Depends on model size; lightweight due to no gradient graphs.

---

## Related Work & Context

### Prior Saliency and Attribution Methods for VLMs

1. **Attention-Guided Grad-CAM (AG-CAM):**
   - Weights attention by gradients to produce saliency maps.
   - Dong & Crisan (arXiv 2504.05445) adapted this to chart QA, demonstrating it on ChartGemma, Janus, LLaVA.
   - **Difference:** This paper's method is gradient-free, simpler, and faster.

2. **Eye-Tracking Guided Attention (ChartGaze):**
   - Uses human eye-tracking data to supervise attention learning.
   - EMNLP 2025 work by [authors not confirmed] shows that attention supervision produces sharper, more human-aligned maps.
   - **Relation:** Orthogonal approach; could be combined with saliency aggregation.

### Visualization Literacy and VLM Reasoning

- **VLAT and derivatives:** Standardized benchmarks measuring how well humans and models understand visualizations.
- **Li et al. (2407.10996):** Comparative study of GPT-4o, Claude 3 Opus, Gemini 1.5 Pro on VLAT/Mini-VLAT; shows models struggle with misleading visual elements.
- **Pandey & Ottley:** "Benchmarking Visual Language Models on Standardized Visualization Literacy Tests"—reports that models (Claude, GPT-4, Gemini) reach ~60-70% accuracy on VLAT but fail on critical-thinking tasks.

### Feature Attribution and Explainability Surveys

- **Broader field:** Feature attribution (SHAP, LIME, integrated gradients) has evolved to address faithfulness, computational cost, and interpretability. This work applies these lessons to the VLM + charts domain.
- **Recent critique:** "Faithfulness Metrics Don't Measure Faithfulness" (arXiv 2605.24) argues that standard metrics (deletion, insertion) may not fully validate explainability—relevant to this work's deletion-test validation.

### Vision Transformer Interpretability

- **ViT attention visualization:** Line of work studying attention in Vision Transformers (e.g., "Interpreting Transformers Through Attention Head Intervention," arXiv 2601.04398).
- **This work's contribution:** Bridges ViT attention research with multimodal (VLM) interpretability, focusing on the language model's cross-modal attention rather than just vision-encoder self-attention.

---

## Key Takeaways

1. **Gradient-free saliency is practical:** For VLMs, simple attention aggregation can provide faithful, interpretable explanations without expensive gradient computation.

2. **Visualization literacy is a testbed for explainability:** Standardized, human-evaluable tasks (VLAT, Mini-VLAT) provide rigorous evaluation settings for explanation methods.

3. **Multimodal attention matters:** Understanding how language models attend to visual features is critical for trustworthy VLM deployment in high-stakes domains.

4. **Deletion testing validates alignment:** While imperfect, deletion-based faithfulness evaluation provides evidence that saliency maps capture causal relationships.

5. **Human-centered evaluation is essential:** Further work combining saliency maps with human eye-tracking and reasoning studies will strengthen explainability claims.

---

## Discussion Questions & Further Reading

- How do gradient-free attention aggregation methods compare to learned attention attribution weights in terms of faithfulness and human interpretability?
- Can saliency maps from different VLM architectures (e.g., CLIP-based vs. learned early fusion) be meaningfully compared and aligned?
- How can practitioners detect and mitigate cases where models learn spurious, partially-faithful attention patterns?
- What role should human-centered evaluation play in validating explanation methods for multimodal models?

---

## References & Links

- **Paper:** [ArXiv: 2607.16105](https://arxiv.org/abs/2607.16105)
- **Venue:** IEEE VIS 2026
- **Related Work:**
  - Dong & Crisan (arXiv 2504.05445): "Probing the Visualization Literacy of Vision Language Models: the Good, the Bad, and the Ugly"
  - Li et al. (arXiv 2407.10996): "Visualization Literacy of Multimodal Large Language Models: A Comparative Study"
  - "Faithfulness Metrics Don't Measure Faithfulness" (arXiv 2605.24)
  - "Interpreting Transformers Through Attention Head Intervention" (arXiv 2601.04398)
