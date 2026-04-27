# Interpretable and Steerable Concept Bottleneck Sparse Autoencoders

**ArXiv ID:** [2512.10805](https://arxiv.org/abs/2512.10805)  
**Authors:** Akshay Kulkarni, Tsui-Wei Weng (UC San Diego), Vivek Narayanaswamy, Shusen Liu, Wesam A. Sakla, Kowshik Thopalli (Lawrence Livermore National Laboratory)  
**Date:** December 13, 2025  
**Subfield:** Concept-Based Explanations  
**Keywords:** Concept Bottleneck Models, Sparse Autoencoders, LVLMs, image generation, steerability, interpretability metrics

---

## Executive Summary

Sparse Autoencoders (SAEs) have emerged as a powerful mechanistic interpretability tool for LLMs, but applying them to Large Vision-Language Models (LVLMs) and image generation reveals a critical gap: most SAE neurons are either uninterpretable, unsteerable, or both. This paper introduces **Concept Bottleneck Sparse Autoencoders (CB-SAE)**, which augment standard SAEs with a lightweight concept bottleneck layer aligned to user-defined concepts, improving interpretability by ~32% and steerability by ~14% while maintaining reconstruction quality. The method enables practical concept-level control over LVLMs and image generation models.

---

## Problem Statement

Sparse Autoencoders have shown promise for decomposing LLM internal representations into interpretable features, but their application to **vision-language models** and **image generation** faces fundamental challenges:

**Problem 1 — Low interpretability rate:**
When SAEs are trained on LVLM activations, systematic analysis reveals that ~60-70% of SAE neurons activate for incoherent or semantically meaningless patterns. Existing SAE training objectives optimize for reconstruction quality and sparsity, but not interpretability.

**Problem 2 — Low steerability rate:**
Even interpretable neurons (those that activate for recognizable concepts) often fail to steer model behavior when their activations are manipulated. Suppressing a "cat" feature may not remove cats from generated images; amplifying a "blue sky" feature may not consistently add sky.

**Problem 3 — User concept alignment:**
Users typically have *specific* concepts they want to understand and control (e.g., "age of subjects in generated images", "presence of text in scenes", "artistic style"). Standard SAEs learn features from data statistics, not from user-defined concept sets — desired concepts are often absent.

**The key insight:** SAEs and Concept Bottleneck Models (CBMs) are complementary: SAEs learn data-driven features in superimposed activation spaces; CBMs constrain representations to user-defined concepts. CB-SAE combines the strengths of both.

---

## Core Concepts & Theory

### Standard Sparse Autoencoders

A standard SAE decomposes activation $\mathbf{x} \in \mathbb{R}^d$ into:
$$\mathbf{h} = \text{TopK}(\mathbf{W}_e \mathbf{x} + \mathbf{b}_e), \quad \hat{\mathbf{x}} = \mathbf{W}_d \mathbf{h} + \mathbf{b}_d$$

TopK ensures sparsity by keeping only the $k$ largest activations. The dictionary columns $\mathbf{W}_d[:, i]$ are candidate "features" in the model's representation space.

### Concept Bottleneck Models (CBMs)

A CBM (Koh et al., 2020) inserts a human-interpretable concept layer $\mathbf{c} \in \mathbb{R}^m$ between input and output:
$$\mathbf{c} = g_\phi(\mathbf{x}), \quad \hat{y} = f_\theta(\mathbf{c})$$

CBMs are interpretable because predictions depend only on recognized concepts. However, traditional CBMs:
- Require large labeled concept datasets
- Suffer from information bottleneck (concepts must capture all task-relevant information)
- Are not compatible with pre-trained models without full retraining

### CB-SAE: Concept Bottleneck Sparse Autoencoders

CB-SAE adds a concept bottleneck to the SAE latent space in three steps:

**Step 1 — Prune low-utility neurons:**
Define combined utility score for each neuron $i$:
$$U_i = w_1 \cdot \text{Interp}(i) + w_2 \cdot \text{Steer}(i)$$

where $\text{Interp}(i)$ is the interpretability score (CLIP-based semantic consistency) and $\text{Steer}(i)$ is the steerability score (AUROC of behavior change under steering). Neurons with $U_i < \tau$ are pruned.

**Step 2 — Concept bottleneck augmentation:**
For a user-provided concept set $\mathcal{C} = \{c_1, ..., c_m\}$, add concept neurons $\mathbf{c} \in \mathbb{R}^m$ alongside the pruned SAE neurons:

$$\mathbf{h}_{\text{CB-SAE}} = [\mathbf{h}_{\text{pruned}}; \mathbf{c}]$$

Each concept neuron $c_j$ is trained to correlate with a CLIP-based concept score:
$$\mathcal{L}_{\text{concept}} = \sum_{j=1}^m \text{BCE}(c_j, \text{CLIP-score}(c_j, \mathbf{x}))$$

**Step 3 — End-to-end fine-tuning:**
Fine-tune the combined CB-SAE encoder with:
$$\mathcal{L} = \underbrace{\|\mathbf{x} - \hat{\mathbf{x}}\|_2^2}_{\text{reconstruction}} + \lambda_1 \|\mathbf{h}\|_1 + \lambda_2 \mathcal{L}_{\text{concept}}$$

### Interpretability and Steerability Metrics

The paper introduces two novel metrics:

**Interpretability Score:**
$$\text{Interp}(i) = \frac{1}{|S_i|} \sum_{\mathbf{x} \in S_i} \text{CLIP-sim}(\text{VQ-descriptor}(\mathbf{x}), \text{max-activating-text}(i))$$

where $S_i$ is the top-20 activating inputs for neuron $i$ and VQ-descriptor extracts visual-semantic descriptions.

**Steerability Score:**
$$\text{Steer}(i) = \text{AUROC}\left(\Delta \text{CLIP-score}(c_i) \mid \text{steer}(i, \alpha)\right)_{\alpha \in \{-2, -1, 0, 1, 2\}}$$

Measures whether adding/subtracting the neuron's feature direction consistently changes CLIP's alignment with the neuron's concept.

---

## Main Ideas & Key Contributions

### 1. Systematic Diagnosis of SAE Deficiencies for Vision

Before proposing CB-SAE, the paper conducts a systematic empirical analysis of standard SAE failures on LVLMs (LLaVA-1.5, InstructBLIP, Stable Diffusion 3):
- 67% of neurons: both low interpretability and low steerability
- 21% of neurons: interpretable but not steerable
- 5% of neurons: steerable but not interpretable
- Only 7% of neurons: both interpretable and steerable

This diagnosis motivates the CB-SAE design directly.

### 2. Concept-Level User Control

CB-SAE enables intuitive concept-level control: users specify concepts in natural language ("smiling face", "baroque architecture", "night scene"), and CB-SAE provides both:
- **Interpretation**: which concepts are active in a given input/generation
- **Steering**: how to modify activations to add/remove specific concepts

### 3. Post-Hoc Compatibility

CB-SAE is a **post-hoc** framework — it does not require retraining the LVLM or image generation model. It is applied to a frozen pretrained model, making it practical for production deployment.

### 4. Improving Both Metrics Simultaneously

Previous approaches that improve interpretability (e.g., concept-supervised training) often degrade steerability and vice versa. CB-SAE is the first approach to improve both simultaneously:
- +32.1% interpretability (measured by CLIP-based interpretability score)
- +14.5% steerability (measured by AUROC of concept-conditioned steering)

---

## Methodology & Implementation

### Models Evaluated
- **LVLMs**: LLaVA-1.5-7B, InstructBLIP-7B, LLaVA-1.6-13B
- **Image Generation**: Stable Diffusion 3, FLUX-dev

### Baseline SAEs
- Standard TopK SAE (Gao et al., 2024)
- Anthropic's JumpReLU SAE (Rajamanoharan et al., 2024)
- OpenAI's scaling SAE

### Concept Sets Used
- COCO semantic concepts (80 categories)
- User-defined safety concepts (NSFW content, violence indicators)
- Artistic style concepts (photorealistic, impressionist, anime)
- Demographic concepts (age, gender expression, apparent emotional state)

### Training Details
- Pruning threshold $\tau$: 5th percentile of combined utility score
- Concept bottleneck neurons: 256 (added to ~8K pruned SAE neurons)
- Fine-tuning: 10K steps, AdamW, lr=3×10⁻⁴
- Training data: 100K LAION images + model-generated activations

### Ablation Studies
| Variant | Interp ↑ | Steer ↑ | Recon ↓ |
|---|---|---|---|
| Standard SAE | 0.42 | 0.38 | 0.91 |
| + Pruning only | 0.53 | 0.41 | 0.94 |
| + Concepts only | 0.62 | 0.43 | 0.93 |
| CB-SAE (full) | **0.74** | **0.52** | **0.93** |

### Limitations
- Concept set design requires user effort; poorly chosen concepts reduce effectiveness
- CLIP-based interpretability metric may not capture all types of semantic coherence
- Pruning reduces total dictionary size, potentially missing rare important features
- Evaluation metrics are novel and not yet standardized in the community

---

## Practical Applications & Real-World Use Cases

### Content Moderation for Image Generation

Image generation APIs (DALL-E, Midjourney, Stable Diffusion APIs) need reliable content safety controls. CB-SAE enables:
- Concept-level detection of safety-relevant features before image generation
- Real-time suppression of NSFW concept directions during generation
- Explainable rejection: "Generation blocked because [specific safety concept] was active"

### Healthcare Imaging AI

Radiology AI systems using vision-language models for report generation need concept-level explanations. CB-SAE allows:
- Defining clinical concepts (cardiomegaly, pneumonia, pleural effusion)
- Attributing findings in reports to specific visual concept activations
- Steering models to be more detailed about specific clinical features

### Advertising and Brand Safety

Brand safety tools need to detect contextually inappropriate content placement. CB-SAE enables concept-level detection of brand-unsafe contexts (violence, political content, competitor products) in video and image content.

### Educational Tools

Personalized learning platforms using AI-generated educational content can use CB-SAE to:
- Verify that generated examples contain pedagogically appropriate concepts
- Steer content generation toward specific learning objectives
- Explain why content is deemed appropriate/inappropriate

### EU AI Act Compliance

High-risk AI systems under the EU AI Act must demonstrate transparency. CB-SAE provides concept-level audit trails for LVLM and image generation decisions, enabling the "technical documentation" requirements of Article 11.

---

## Insights & Implications

### The Interpretability-Steerability Connection

The paper reveals a previously underappreciated problem: interpretability and steerability are correlated but distinct properties, and SAE training doesn't guarantee either. This has implications for all mechanistic interpretability work — a feature that's been identified and interpreted may not be usefully steerable, which limits practical applications of MI.

### Concept Supervision as an Amplifier

The success of concept-supervised neurons alongside data-driven neurons suggests a **hybrid approach** is optimal: data-driven features capture the full distribution, while concept-supervised features ensure the most important (user-relevant) concepts are well-represented and controllable.

### Post-Hoc Concept Engineering

CB-SAE demonstrates that concept-level control doesn't require building CBMs from scratch — it can be retrofitted to existing models. This significantly lowers the barrier to deploying interpretable AI in production.

### Implications for AI Safety

The NSFW concept control application demonstrates that SAE-based steering could be an efficient safety mechanism — not requiring model fine-tuning (which is expensive and may degrade capabilities) but instead applying lightweight concept suppression at inference time.

### Open Questions
- Can CB-SAE scale to 70B+ parameter models without prohibitive computational cost?
- How does concept set design quality affect downstream steerability?
- Can CB-SAE capture abstract or compositional concepts (not just visual categories)?
- Does concept bottleneck augmentation affect the model's underlying capabilities?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2512.10805](https://arxiv.org/abs/2512.10805)
- **GitHub:** [https://github.com/Trustworthy-ML-Lab/CB-SAE](https://github.com/Trustworthy-ML-Lab/CB-SAE)
- **Dependencies:** PyTorch, HuggingFace Transformers/Diffusers, CLIP, SAELens
- **Computational Requirements:** 2×A100 80GB for LVLM SAE training; 4×A100 for Stable Diffusion 3

### Quick Start
```bash
git clone https://github.com/Trustworthy-ML-Lab/CB-SAE
pip install -r requirements.txt
```

```python
from cb_sae import ConceptBottleneckSAE, ConceptSet

# Define concept set
concepts = ConceptSet([
    "smiling person",
    "outdoor scene",
    "text in image",
    "nighttime",
    "professional attire"
])

# Load pretrained CB-SAE for LLaVA-1.5-7B
cb_sae = ConceptBottleneckSAE.from_pretrained(
    model_name="llava-1.5-7b",
    concept_set=concepts,
    layer=15
)

# Interpret an image
from PIL import Image
image = Image.open("example.jpg")
concept_activations = cb_sae.get_concept_activations(image)
print("Active concepts:", concept_activations.top_concepts(k=5))

# Steer image generation
from diffusers import StableDiffusion3Pipeline
pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3")

steered_image = cb_sae.steered_generate(
    pipe,
    prompt="a person at work",
    add_concepts=["smiling person", "professional attire"],
    remove_concepts=["nighttime"],
    alpha=2.0
)
steered_image.save("steered_output.jpg")
```

---

## Related Work & Context

### Concept Bottleneck Models
- **Koh et al. (2020)**: Original CBMs for image classification
- **Shao et al. (2021)**: Concept Bottleneck Models with intervention
- **Oikarinen et al. (2023)**: Label-free CBM using LLMs for concept generation

### Sparse Autoencoders
- **Elhage et al. (2022)**: Toy models of superposition
- **Bricken et al. (2023)**: Monosemanticity with one-layer transformers
- **Gao et al. (2024)**: Scaling and evaluating sparse autoencoders

### Mechanistic Interpretability for Vision
- **Nguyen et al. (2016)**: Multifaceted feature visualization
- **Olah et al. (2020)**: Zoom In — circuits in vision models
- **Hernandez et al. (2022)**: Natural language descriptions of neural features

### Where This Leads
1. **Hierarchical CB-SAE**: Concepts at multiple levels of abstraction (edges → textures → objects → scenes)
2. **Cross-modal concept alignment**: Ensuring concept neurons respond equivalently to text and image inputs
3. **Concept-based model editing**: Replacing concept neurons to change model behavior on concept-level tasks
4. **Safety auditing tools**: CB-SAE as a component of LVLM safety certification workflows

---

*Sources:*
- [arxiv.org/abs/2512.10805](https://arxiv.org/abs/2512.10805)
- [github.com/Trustworthy-ML-Lab/CB-SAE](https://github.com/Trustworthy-ML-Lab/CB-SAE)
