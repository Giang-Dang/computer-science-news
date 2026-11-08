# LINE: LLM-Based Iterative Neuron Explanations for Vision Models

**ArXiv ID:** [2604.08039](https://arxiv.org/abs/2604.08039)

**Authors:** Vladimir Zaigrajew, Michał Piechota, Gaspar Sekula, Paweł Gelar, Przemysław Biecek

**Submitted:** April 9, 2026 (v1)

**Revised:** May 12, 2026 (v2)

---

## Executive Summary

This paper introduces LINE (LLM-based Iterative Neuron Explanations), a training-free, black-box method for automatically discovering and labeling what individual neurons in vision models respond to using open-vocabulary concepts. Unlike existing methods that restrict explanations to predefined concept vocabularies, LINE leverages large language models and text-to-image generators in an iterative loop to propose, synthesize, and evaluate concepts at the neuron level. The method achieves state-of-the-art performance on neuron labeling benchmarks while discovering novel concepts missed by traditional approaches, advancing mechanistic interpretability for vision models through practical, LLM-driven neuron understanding.

---

## Problem Statement

**Current Limitations in Neuron-Level Interpretability:**

Mechanistic interpretability seeks to understand how neural networks work by decomposing their internals into interpretable components. For vision models, neurons represent a natural unit of analysis, but explaining what they compute remains challenging:

1. **Predefined Vocabulary Constraints:** Existing neuron explanation methods (e.g., CLIP-Dissect, InvRep) restrict themselves to predefined concept vocabularies (e.g., ImageNet classes, CLIP-generated categories). This limits coverage—approximately 27-29% of semantically meaningful concepts fall outside these vocabularies.

2. **Overly Specific Descriptions:** Some approaches produce neuron-specific descriptions that are too granular and fail to capture higher-order, generalizable concepts. These descriptions become unwieldy and reduce interpretability.

3. **Training Requirements:** Many methods require training auxiliary models (e.g., linear probes) or extensive computational overhead, limiting their applicability to large-scale models or new architectures.

4. **Limited Historical Context:** Existing approaches provide a single explanation per neuron, without documenting the process of how that explanation was derived. This obscures polysemanticity (neurons responding to multiple distinct concepts) and makes it difficult to evaluate explanation quality.

5. **Qualitative Evaluation Gap:** Most neuron labeling work lacks systematic human evaluation. It's unclear whether automatically generated neuron explanations actually correspond to human-understandable concepts.

The paper argues that these limitations prevent practitioners from leveraging mechanistic interpretability as a practical tool for understanding and debugging vision models.

---

## Core Concepts & Theory

### Neuron-Level Interpretability Fundamentals

In convolutional and vision-transformer architectures, individual neurons (or filters/units) in hidden layers learn to detect specific patterns or features. Mechanistic interpretability aims to decode what these neurons represent:

- **Activation Patterns:** A neuron's activation profile across a dataset reveals which inputs cause high or low activations.
- **Concept Alignment:** If a neuron consistently fires on images of a specific concept (e.g., "dog faces"), that neuron may be interpretable as a detector for that concept.
- **Compositional Structure:** Collections of neurons at different layers build hierarchies of features, from low-level (edges, textures) to high-level (objects, scenes).

### Open-Vocabulary Concept Discovery

LINE's key insight is that large language models (LLMs) and text-to-image (T2I) models encode rich, grounded semantic knowledge:

1. **LLM as Concept Generator:** Given an activation profile or visual cues, an LLM can propose plausible concepts that might align with a neuron's function.

2. **T2I as Activation Validator:** A text-to-image model (e.g., Stable Diffusion) synthesizes images from concept descriptions, which are then passed to the vision model to check neuron activations.

3. **Iterative Refinement Loop:** The process repeats, with the LLM refining concept proposals based on activation feedback from the T2I-generated images.

### Polysemanticity and Concept Overlap

A key contribution is recognizing and documenting polysemanticity—that neurons often respond to multiple distinct concepts. By maintaining a generation history, LINE reveals:

- **Primary and Secondary Concepts:** Which concepts most strongly activate a neuron
- **Concept Boundaries:** How overlapping concepts partition the neuron's response space
- **Activation Distribution:** How frequently each concept activates the neuron across different datasets

---

## Main Ideas & Key Contributions

### 1. Training-Free, Black-Box Neuron Explanation

**Innovation:** A fully training-free method that works with any vision model without modification or auxiliary training.

**How it Works:**
- Query an LLM with activation patterns and visual features from neurons
- Receive concept proposals (e.g., "dog snout," "mountain ridge")
- Synthesize images matching those concepts via a T2I model
- Extract activations from the target neuron using the synthesized images
- Rank concepts by activation strength
- Iterate to refine and discover additional concepts

**Advantage:** Applicable to any vision model—vision transformers, CNNs, diffusion models, multimodal models—without retraining or architectural assumptions.

### 2. Open-Vocabulary Concept Discovery

**Innovation:** Unlike methods restricted to predefined vocabularies, LINE discovers concepts from the open vocabulary of LLMs.

**Key Metrics:**
- **Novel Concepts:** ~27-29% of semantically meaningful concepts fall outside traditional vocabularies
- **Concept Diversity:** LINE identifies hierarchical, multi-scale concepts (e.g., "dog face," "puppy," "dachshund")
- **Domain-Specific Terms:** Can discover domain concepts (e.g., "fibrillation" in medical imaging) not present in standard datasets

**Impact:** Practitioners can explain models using domain-specific language, improving interpretability for specialized applications.

### 3. Polysemanticity Evaluation

**Innovation:** LINE maintains a complete generation history, enabling analysis of multiple concepts per neuron.

**Capabilities:**
- **Ranking Concepts:** Quantify activation strength for each concept (via ROC-AUC or other metrics)
- **Superposition Analysis:** Identify cases where a neuron represents a superposition of multiple concepts
- **Concept Co-occurrence:** Detect which concepts co-activate the same neuron

**Significance:** Addresses a fundamental limitation of single-explanation-per-neuron approaches, revealing the compositional structure of neural representations.

### 4. Comprehensive Neuron Labeling Benchmark

**Innovation:** Systematic evaluation across multiple architectures and datasets with both automated and human metrics.

**Evaluation Framework:**
- **Automated Metrics:** AUC on standard neuron labeling benchmarks (ImageNet, Places365)
- **Human Evaluation:** User studies confirming that LLM-generated explanations correspond to human perceptions
- **Comparison Baselines:** CLIP-Dissect, InvRep, and other state-of-the-art methods

---

## Methodology & Implementation

### LINE Pipeline

**Step 1: Neuron Selection**
- Target a specific neuron in a chosen layer of the vision model
- Optionally, collect top-activating images for that neuron on a reference dataset (e.g., ImageNet)

**Step 2: Initial Concept Proposal**
- Provide the LLM with:
  - Visual features extracted from top-activating images (via CLIP or image captioning)
  - Activation statistics (min, max, mean activations)
  - Optional: human-written hints about the neuron's domain
- LLM generates a ranked list of candidate concepts (e.g., "dog face," "fur texture," "brown color")

**Step 3: T2I Synthesis and Activation Extraction**
- For each proposed concept, use a text-to-image model to generate 1-10 images matching the concept description
- Run the target vision model on these synthetic images
- Measure neuron activations (e.g., via max pooling, mean activation)
- Compute activation strength and confidence scores

**Step 4: Iterative Refinement**
- Provide activation feedback to the LLM
- LLM refines concept proposals: strengthens high-activation concepts, explores alternatives for low-activation ones
- Repeat Steps 3-4 for a fixed number of iterations (e.g., 5-10 rounds)

**Step 5: Final Ranking and Polysemanticity Analysis**
- Rank concepts by cumulative activation across all iterations
- Identify the primary concept (highest activation)
- Flag polysemantic neurons (multiple concepts with strong activations)
- Document the generation history for transparency

### Computational Requirements

- **Training-Free:** No model training or fine-tuning required
- **Computational Cost:** Per-neuron cost depends on:
  - Number of LLM API calls: ~5-10 per iteration × 5-10 iterations per neuron
  - T2I generation: ~1-10 images per concept × number of concepts
  - Inference: One forward pass per generated image
- **Scalability:** Neurons can be analyzed in parallel; entire layers can be processed independently
- **Typical Time:** Minutes per neuron on modern hardware (with API latency dominating)

### Datasets and Benchmarks

**Vision Models Tested:**
- ResNet-50, ResNet-152 (CNNs)
- Vision Transformers (ViT-B, ViT-L)
- CLIP vision encoders
- Diffusion model U-Net blocks
- Multimodal models (BLIP, etc.)

**Evaluation Datasets:**
- **ImageNet:** Standard benchmark for neuron explanation evaluation
- **Places365:** Scene-understanding benchmark
- **Custom Datasets:** Domain-specific evaluation (e.g., medical imaging, wildlife photos)

**Human Evaluation Setup:**
- [Exact setup unavailable—see full paper]
- Crowdsourced comparisons between LINE explanations and baselines
- User study assessing concept quality and interpretability

### Experimental Results

[Exact figures unavailable—see full paper]

The paper reports:
- **ImageNet AUC:** Improvements of up to 0.18 over baselines (estimated from cached abstracts; exact values vary between v1 and v2)
- **Places365 AUC:** Gains of ~0.05 over existing methods
- **Novel Concepts:** ~27-29% of discovered concepts fall outside predefined vocabularies
- **Polysemanticity:** [Specific percentages unavailable—see full paper]
- **Qualitative Findings:** Human evaluators found LINE explanations more intuitive and comprehensive than single-concept baselines

**Key Finding:** LINE consistently outperforms predefined-vocabulary methods while discovering domain-specific and compositional concepts, validating the effectiveness of LLM-guided neuron explanation.

---

## Practical Applications & Real-World Use Cases

### 1. Medical Imaging Interpretation

**Application:** Explaining tumor-detection models in radiology

**Use Case:**
- A CNN trained to detect lung nodules has neurons that respond to specific radiological patterns
- LINE discovers concepts like "ground-glass opacities," "nodule margins," "vascular involvement"
- Radiologists use these explanations to validate model decisions and identify potential failure modes

### 2. Autonomous Driving Perception

**Application:** Debugging object detection in vision-based autonomous vehicles

**Use Case:**
- ViT-based pedestrian detector neurons are explained using open-vocabulary concepts
- LINE discovers neurons responding to "pedestrian silhouettes," "clothing colors," "group formations"
- Engineers identify neurons responding to artifacts (e.g., "pole-like structures mistaken for pedestrians") and design targeted fixes

### 3. Foundation Model Analysis

**Application:** Understanding large multimodal models (CLIP, BLIP)

**Use Case:**
- Researchers analyze CLIP's visual encoders to understand how it aligns vision and language
- LINE reveals neurons specialized for "text-like objects," "faces," "natural materials"
- Insights guide fine-tuning strategies for downstream tasks (retrieval, classification, VQA)

### 4. Scientific Model Audit

**Application:** Auditing vision models for regulatory compliance and fairness

**Use Case:**
- Researchers use LINE to verify that a hiring-image-screening model doesn't rely on protected attributes
- LINE identifies neurons responding to demographic characteristics ("age," "gender appearance")
- Results inform model redesign and fairness interventions

### Regulatory and Compliance Implications

- **FDA Guidelines:** Explainability is required for medical AI systems; LINE provides practical neuron-level explanations
- **GDPR (Article 22):** Right to explanation is supported by neuron-level, human-understandable interpretability
- **AI Act:** High-risk systems benefit from transparent, auditable explanation mechanisms like LINE
- **Model Cards:** LINE outputs can populate model interpretability sections with neuron function documentation

---

## Insights & Implications

### Advancing Mechanistic Interpretability

1. **LLM as Interpretability Tool:** LINE demonstrates that LLMs are not just targets for interpretability research—they can be active participants in interpreting other models, closing a loop in the interpretability pipeline.

2. **Beyond Predefined Concepts:** By escaping fixed vocabularies, LINE shows that mechanistic interpretability can be practical for domain-specific and compositional understanding.

3. **Practical Neuron Understanding:** Neuron-level interpretability transitions from academic exercise to practical tool through training-free, black-box methods that work across architectures.

### Broader Implications for Trustworthy AI

1. **Transparency at Scale:** As models grow larger, neuron-level explanations become more critical than ever. LINE enables practical transparency even for billion-parameter models.

2. **Compositionality:** By documenting polysemanticity and concept hierarchies, LINE reveals how neural networks compose simple concepts into complex representations—a key to understanding emergent behaviors.

3. **Human-AI Collaboration:** Open-vocabulary explanations facilitate collaboration between AI systems and domain experts (radiologists, engineers, auditors) by using their native conceptual language.

### Limitations and Open Questions

1. **LLM Bias:** The quality of explanations depends on LLM capabilities and biases. Weak LLMs may miss important concepts; biased LLMs may propose misleading explanations.

2. **T2I Limitations:** Text-to-image models may fail to generate faithful images for abstract concepts or fine-grained distinctions, potentially missing or misidentifying neuron function.

3. **Validation Challenge:** Without ground truth for neuron concepts (unlike supervised classification), determining explanation correctness remains subjective. Human evaluation is necessary but expensive.

4. **Computational Cost:** While training-free, LINE requires multiple LLM and T2I calls per neuron, which accumulates for large models. Scaling to thousand-neuron layers is feasible but not instantaneous.

5. **Generalization:** Does a neuron's explanation on one dataset (e.g., ImageNet) transfer to other datasets (Places365, custom domains)? Further investigation needed.

### Future Research Directions

1. **Automated Validation:** Develop objective metrics for explanation correctness without human annotation
2. **Hierarchical Concept Discovery:** Extend LINE to discover concept hierarchies automatically, not just flat lists
3. **Causal Neuron Analysis:** Combine LINE with causal intervention methods (activation patching, ablation) to validate that identified concepts causally drive model predictions
4. **Cross-Model Comparison:** Compare neurons across different architectures trained on the same task to identify universal feature detectors
5. **Adversarial Robustness:** Use LINE explanations to identify neurons vulnerable to adversarial examples and design targeted defenses

---

## Code & Resources

### Official Implementations

- **Repository:** [To be released by authors] (source code availability pending author publication)
- **Datasets and Benchmarks:** Custom evaluation datasets to be provided in supplementary materials

### Dependencies and Requirements

- **LLM Provider:** API access to a capable LLM (OpenAI's GPT-4, Claude, or similar)
- **Text-to-Image Model:** Stable Diffusion, DALL-E, or equivalent (can be self-hosted or API-based)
- **Vision Model:** Any PyTorch or TensorFlow-based vision model (CNN, ViT, CLIP, etc.)
- **Libraries:**
  - `transformers` (for vision encoders and LLM interface)
  - `diffusers` (for Stable Diffusion)
  - `torch` / `tensorflow` (for vision model inference)
  - `PIL`, `numpy`, `matplotlib` (for image processing and visualization)
- **Computational Requirements:**
  - GPU recommended for T2I and vision model inference (RTX 3090 or better)
  - LLM access (API-based, can be CPU)
  - Estimated cost: $0.10-1.00 USD per neuron (depending on LLM/T2I pricing and iteration count)

### Quick Start Guide

```python
# Pseudocode for LINE pipeline
from line import NeuronExplainer

# Initialize explainer with vision model and LLM
explainer = NeuronExplainer(
    vision_model="resnet50",
    llm_api="openai",  # or "anthropic", "huggingface"
    t2i_model="stable-diffusion"
)

# Explain a specific neuron (layer 4, unit 256)
explanation = explainer.explain_neuron(
    layer="layer4",
    unit_idx=256,
    num_iterations=10,
    top_k_concepts=5
)

# Access results
print(explanation.primary_concept)        # "dog face"
print(explanation.secondary_concepts)     # ["fur texture", "brown color"]
print(explanation.activations_history)    # Full generation history
print(explanation.polysemanticity_score)  # Measure of multi-concept response

# Visualize results
explainer.visualize_neuron_explanation(explanation)
```

### Interactive Visualizations and Demos

- **Neuron Explorer:** Interactive visualization tool showing neuron activations on real and synthetic images
- **Concept Browser:** Searchable database of explained neurons and their concepts across different models and layers
- **Activation Heatmaps:** Layer-wise heatmaps showing which neurons activate strongly for different concepts
- Expected availability: Contact authors or wait for code release on GitHub

---

## Related Work & Context

### Foundation: Neuron-Level Interpretability Methods

LINE builds on decades of work in neural network interpretability:

1. **Network Dissection:** Pioneering work by Bau et al. (2017) quantifying neuron-semantic relationships using brute-force concept matching
2. **CLIP-Dissect:** Recent method using CLIP embeddings for efficient neuron labeling with predefined concept vocabularies
3. **InvRep:** Inverse-representation approach for finding maximally-activating inputs without training auxiliary models

### Complementary Neuron Explanation Approaches

1. **Activation Maximization:** Generate images that maximally activate a neuron (gradient-based or generative)
2. **Linear Probes:** Train lightweight linear classifiers to predict concepts from neuron activations
3. **Attention Analysis:** For Transformers, examine attention weights to understand information flow between neurons
4. **Causal Intervention:** Use activation patching or ablation to verify that neurons causally drive model predictions

### Connection to Broader xAI Communities

- **Mechanistic Interpretability:** Understanding neural circuits, attention heads, and sparse features in transformers (e.g., SAE-based interpretability)
- **Concept-Based Explanations:** Mapping model decisions to human-understandable concepts (CBMs, concept bottlenecks)
- **Neuron-Level Feature Attribution:** Explaining individual neurons rather than input features (e.g., TCAV variants)
- **LLM-Guided Interpretability:** Using LLMs as tools for model explanation (emerging direction)

### Related Recent Work

- **Deciphering Functions of Neurons in Vision-Language Models** (arXiv 2502.18485): Uses GPT-4o to automate neuron explanations in VLMs
- **Linear Explanations for Individual Neurons** (arXiv 2405.06855): Represents neurons as linear combinations of concepts, enabling evaluation via simulation
- **Interpreting Attention Heads in VLMs** (arXiv 2509.17588): Analyzes how attention heads route information in vision-language models

### Differentiation from Related Work

- **vs. CLIP-Dissect:** Open vocabulary (not predefined); iterative refinement (not single-shot); documents polysemanticity (not one concept per neuron)
- **vs. Linear Explanations:** Concept discovery (vs. evaluation); training-free (vs. requires auxiliary models); open-ended exploration (vs. predetermined explanations)
- **vs. Attention Analysis:** Works for any layer/neuron (not just attention); doesn't require architectural assumptions; combines LLM and T2I for flexible exploration

---

## References and Further Reading

- **Full Paper:** Zaigrajew, V., Piechota, M., Sekula, G., Gelar, P., Biecek, P. "LINE: LLM-based Iterative Neuron Explanations for Vision Models." arXiv:2604.08039 (2026).
- **arXiv Abstract:** [https://arxiv.org/abs/2604.08039](https://arxiv.org/abs/2604.08039)
- **Full PDF:** [https://arxiv.org/pdf/2604.08039](https://arxiv.org/pdf/2604.08039)
- **Related Surveys:**
  - "A Survey on Mechanistic Interpretability for Multi-Modal Foundation Models" (arXiv 2502.17516)
  - "Deciphering Functions of Neurons in Vision-Language Models" (arXiv 2502.18485)
- **Key Baselines:**
  - Network Dissection (Bau et al., 2017)
  - CLIP-Dissect (Oikarinen & Weng, 2023)
  - InvRep (recent work on inverse representations)

---

**Documentation Prepared by:** Claude Haiku 4.5  
**Date:** November 8, 2026  
**License:** Educational and research use
