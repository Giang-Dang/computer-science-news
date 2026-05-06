# Seeing Through Circuits: Faithful Mechanistic Interpretability for Vision Transformers

**ArXiv ID:** 2604.14477  
**Publication Date:** April 2026  
**Authors:** Research team from Max Planck Institute for Informatics and collaborating institutions  
**Field:** Mechanistic Interpretability, Vision Transformers, Model Transparency

## Executive Summary

This paper introduces **Visual Circuit Discovery (Vi-CD)**, the first edge-based circuit discovery method for vision transformers, enabling identification of sparse, faithful computational subgraphs that explain class-specific predictions. By extending mechanistic interpretability from language models to vision transformers, this work advances our ability to understand and manipulate the internal mechanisms of visual neural networks, achieving up to 10x sparsity improvements over prior neuron-based approaches.

## Problem Statement

While mechanistic interpretability has made significant advances in large language models through circuit discovery—identifying task-specific computational graphs formed by connections between model components—vision transformers have largely remained opaque. Prior circuit discovery work in vision models focused only on neuron-level interpretability (identifying important individual neurons), which:

1. **Misses compositional structure:** Neuron-based approaches cannot capture how information flows through networks via specific learned connections
2. **Lacks sparsity:** Neuron-level circuits typically require retaining more model components to maintain task performance
3. **Limits practical applications:** Without understanding edge-level connections, mechanistic steering (targeted manipulation of model behavior) becomes infeasible for vision models

This paper addresses a fundamental gap: Can we apply edge-based circuit discovery—which has proven successful for language models—to the visual domain?

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

**Mechanistic interpretability** aims to understand neural networks by reverse-engineering their internal computational mechanisms. Rather than treating models as black boxes, it decomposes them into interpretable units and their interactions.

**Circuits** are sparse subgraphs of a neural network that perform specific computational tasks. A circuit consists of:
- **Nodes:** Model components (neurons, attention heads, residual stream positions)
- **Edges:** Weighted connections representing information flow
- **Task-specificity:** Circuits are defined relative to a particular input or output

### Circuit Discovery Methodology

Traditional circuit discovery uses **activation patching** (also called causal tracing):

1. **Forward pass:** Run the input through the full network and record all activations
2. **Patch operation:** Replace activations of a specific component with those from a different input
3. **Measure impact:** Compare the output before and after patching to quantify the component's importance
4. **Iterative refinement:** Identify which components significantly affect the target output

### Challenges in Vision Transformers

Vision transformers differ fundamentally from language models:
- **Spatial structure:** VTs operate on 2D grid of image patches, making information flow less sequential
- **Attention patterns:** Visual attention is inherently 2D and spatially distributed
- **Feature hierarchy:** VTs learn multi-scale feature representations
- **Computational density:** More complex interactions between spatial and semantic dimensions

### Vi-CD: Visual Circuit Discovery Algorithm

**Sequential Activation Patching with Inpainting:**

```
1. Input: Image x, target logit l (class of interest)
2. Forward pass: Obtain all intermediate activations A = [a_0, a_1, ..., a_L]
3. For each component (head, neuron, or layer):
   a) Create corrupted version: x_corrupt ← inpaint(x) or random noise
   b) Forward pass on corrupted image: A_corrupt ← forward(x_corrupt)
   c) Replace specific component: A_patched[i] ← A_corrupt[i]
   d) Complete forward pass: logit_patched ← forward_with_patch(A_patched)
   e) Calculate importance: importance[i] ← |logit - logit_patched|
4. Identify edges with high importance scores
5. Refine circuit by removing low-importance edges
6. Output: Sparse circuit C ⊂ Network edges
```

**Key innovation:** Using inpainted corruptions (realistic image variations) rather than random noise preserves spatial structure and leads to more faithful circuits.

### Sparsity vs. Faithfulness Trade-off

Vi-CD balances two critical metrics:
- **Faithfulness:** Recovered circuits retain full prediction accuracy on held-out examples
- **Sparsity:** Circuits use < 10% of model edges while maintaining performance

This is achieved through iterative edge pruning with validation on causally important edges.

## Main Ideas & Key Contributions

### 1. **First Edge-Based Circuit Discovery for Vision Transformers**

Prior work only identified important neurons in vision models. Vi-CD introduces the first method to discover edges (specific connection pathways) in visual networks, mirroring the success of edge-based circuits in language model interpretability.

**Why this matters:** Edges capture *how* information flows through the network, not just *which* components are involved.

### 2. **Class-Specific Circuit Discovery**

Vi-CD recovers distinct circuits for different classification tasks:
- Different output classes activate completely different computational pathways
- Circuits for similar objects (e.g., "dog" vs. "cat") share common sub-circuits for shared visual features
- This enables fine-grained understanding of what different parts of the network compute

### 3. **Exceptional Sparsity and Faithfulness**

On ViT-B/32 trained on ImageNet:
- Recovers **near-perfect accuracy (≥99%)** while retaining **< 10% of edges**
- For comparison, neuron-level methods (EAP-IG) require > 25% of components for similar accuracy
- Sparsity improvement: **2-10x over prior work**

### 4. **Mechanistic Steering Capability**

The discovered circuits enable targeted model manipulation:
- **Attack defense:** Deactivating specific circuits prevents adversarial attacks (e.g., typographic perturbations in CLIP)
- **Behavior correction:** Suppressing misclassification circuits can correct confusions between visually similar classes
- **Model control:** Selectively activate/deactivate edges to steer model decisions with surgical precision

This is the first demonstration of mechanistic steering in vision transformers.

### 5. **Scalability to Large-Scale Models**

Demonstrated on:
- Supervised ViT-B trained on ImageNet (86M parameters)
- OpenCLIP ViT-B/32 (multimodal, 86M parameters)
- Method scales to even larger vision models

### 6. **Robustness to Adversarial Attacks**

Applied Vi-CD to understand and defend against:
- **Typographic attacks on CLIP:** Small text overlays that fool vision-language models
- **Adversarial perturbations:** Model-specific attacks designed to cause misclassification
- Identified that deactivating 2-3 specific circuits can completely block these attacks

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
1. **ViT-B/32 on ImageNet:** Standard supervised vision transformer
   - Architecture: 12 transformer blocks, 12 attention heads per block
   - Trained on 1M ImageNet images across 1000 classes
   
2. **OpenCLIP ViT-B/32:** Contrastive vision-language model
   - Trained on 400M image-text pairs from LAION dataset
   - Aligned visual and textual representations

**Circuit Discovery Pipeline:**

| Step | Method | Details |
|------|--------|---------|
| 1. Baseline | Forward pass | Record all 144 attention heads × 12 layers = 1,728 attention heads |
| 2. Patching | Activation patching | Replace head/neuron activations with inpainted corruptions |
| 3. Measurement | Logit difference | Δlogit = \|logit_original - logit_patched\| |
| 4. Ranking | Importance scoring | Sort components by impact on target logit |
| 5. Refinement | Iterative pruning | Remove low-importance edges while maintaining faithfulness |

### Evaluation Metrics

**Faithfulness Metrics:**
- **Accuracy preservation:** Percentage of original accuracy maintained on validation set
- **Logit preservation:** KL divergence between original and circuit output distributions
- **Out-of-distribution robustness:** Circuit performance on ImageNet-C, ImageNet-A (adversarial subsets)

**Sparsity Metrics:**
- **Edge ratio:** Percentage of edges retained (target: < 10%)
- **Parameter count:** Percentage of model parameters needed for inference
- **Computational cost:** FLOPs reduction from circuit compression

**Interpretability Metrics:**
- **Circuit coherence:** Do discovered edges form semantically meaningful pathways?
- **Concept alignment:** Do circuits correspond to human-interpretable visual features?

### Results and Performance

**Classification Performance:**

| Model | Dataset | Full Accuracy | Circuit Accuracy | Edge Retention |
|-------|---------|---------------|-----------------|-----------------|
| ViT-B | ImageNet | 86.2% | 85.8% | 8.9% |
| ViT-B | ImageNet-C | 54.3% | 53.1% | 9.2% |
| OpenCLIP | ImageNet | 82.1% | 81.7% | 7.5% |

**Attack Defense Results:**

For typographic attacks on CLIP (intentional text overlays):
- Baseline CLIP accuracy under attack: 12% (severe misclassification)
- Deactivating top-3 important circuits for attacks: 89% accuracy restoration
- Shows circuits isolate attack-specific computation

**Circuit Composition Analysis:**

- Average circuit size: ~150 edges for 1000-way classification
- Edges span all 12 transformer layers (information needs to flow through depth)
- Attention heads show specialization: early layers focus on texture, later layers on semantic content

### Limitations and Failure Cases

1. **Computational cost:** Circuit discovery requires thousands of forward passes; full circuit discovery on large models (~1B parameters) remains expensive

2. **Inpainting quality:** Results depend on quality of corrupted images; poor inpainting misses circuits

3. **Class imbalance:** Rare classes may have harder-to-identify circuits due to fewer training examples

4. **Generalization:** Circuits discovered on ImageNet may not fully transfer to other visual domains (medical imaging, satellite imagery)

5. **Attention-head granularity:** Mechanistic steering works at head-level; sub-head circuits remain opaque

## Practical Applications & Real-World Use Cases

### 1. **Medical Imaging and Healthcare**

**Application:** Understanding diagnostic AI decisions
- **Challenge:** Radiologists need to understand how AI systems identify tumors or anomalies for regulatory compliance (FDA approval)
- **Solution:** Vi-CD discovers circuits responsible for detecting specific pathologies
- **Impact:** Enables explainable clinical AI, builds trust in automated diagnosis, meets regulatory requirements (21 CFR Part 11)

**Example:** Circuit for detecting breast cancer in mammograms could be validated independently to ensure it focuses on medically relevant features, not demographic artifacts.

### 2. **Autonomous Vehicle Perception**

**Application:** Certifying perception systems for self-driving cars
- **Challenge:** Vision systems must be interpretable for safety certification (ISO 26262, autonomous vehicle regulations)
- **Solution:** Identify circuits for detecting pedestrians, traffic signs, lane markings
- **Impact:** Enables auditing of what visual features trigger driving decisions

**Example:** Discover that pedestrian-detection circuit unexpectedly includes "people-shaped shadows" as a trigger; fix this before deployment.

### 3. **Fairness and Bias Detection**

**Application:** Auditing vision systems for demographic bias
- **Challenge:** Vision models can exhibit racial, gender, or age bias in classification
- **Solution:** Identify circuits that encode demographic information; deactivate them to reduce bias
- **Impact:** Build fair, trustworthy vision systems for hiring, lending, criminal justice

**Example:** Discover circuit that processes skin tone; deactivate to ensure hiring AI doesn't discriminate based on ethnicity.

### 4. **Content Moderation and Safety**

**Application:** Understanding harmful content detection
- **Challenge:** Content platforms use vision AI for moderation; decisions must be auditable
- **Solution:** Circuits reveal what visual features trigger content flags
- **Impact:** Improve moderation accuracy, reduce false positives/negatives

**Example:** Discover moderation circuit focuses on anatomical features; refine to distinguish art/medical content from harmful material.

### 5. **Model Robustness and Defense**

**Application:** Defending against adversarial attacks
- **Challenge:** Vision models are vulnerable to adversarial perturbations
- **Solution:** Identify and deactivate circuits exploited by attacks
- **Impact:** Build inherently more robust models

**Example:** Typographic attacks on CLIP (text overlays causing misclassification) can be prevented by suppressing specific circuits.

### Regulatory and Compliance Implications

- **GDPR Right to Explanation:** Circuits provide transparent reasoning for automated decisions (required for certain uses)
- **AI Act (EU):** High-risk AI systems must be explainable; Vi-CD enables compliance
- **FDA 21 CFR Part 11:** Medical device AI must be validated; circuit discovery supports regulatory validation
- **Algorithmic Accountability:** Enables auditing of what visual features drive model decisions

## Insights & Implications

### Broader Impact on Trustworthy AI

1. **Transparency at Scale:** Demonstrates that even large vision models (billions of parameters) can be meaningfully interpreted without distillation or approximation

2. **Mechanistic Understanding:** Shows that visual cognition, like language processing, decomposes into interpretable computational circuits—a fundamental advance in understanding neural computation

3. **Certifiability:** Makes AI systems certifiable for safety-critical domains (medical imaging, autonomous vehicles, financial services)

### Advancement of xAI State-of-the-Art

**Before Vi-CD:**
- Vision transformer interpretability limited to neuron importance / attention visualizations
- No understanding of how information routes through models
- No capability for mechanistic steering in vision models

**After Vi-CD:**
- Can identify sparse, faithful circuits in large vision transformers
- Can explain predictions through specific computational pathways
- Can surgically modify model behavior by manipulating identified circuits

**Conceptual Impact:**
- Unifies interpretability research across modalities (language, vision)
- Establishes that circuit discovery is fundamental technique, not language-specific phenomenon
- Opens new research directions in multimodal mechanistic interpretability

### Limitations and Open Questions

1. **Computational Efficiency:** Circuit discovery remains expensive; need faster methods for real-time applications

2. **Theoretical Understanding:** Why do these specific circuits emerge? What determines circuit structure? Mechanistic interpretability lacks formal theory

3. **Generalizable Circuits:** Can circuits discovered on one distribution transfer to others? (e.g., ImageNet to medical imaging)

4. **Fine-Grained Circuits:** Can we discover circuits at sub-head granularity? Current approach limited to attention head level

5. **Multimodal Integration:** How do circuits in vision-language models integrate across modalities?

### Future Research Directions

1. **Scaled Mechanistic Interpretability:** Apply to billion-parameter models with efficient discovery algorithms

2. **Hierarchical Circuits:** Identify meta-circuits (compositions of circuits) for higher-level reasoning

3. **Causal Circuits:** Move beyond correlation to causal analysis—which circuits causally control which behaviors?

4. **Transfer Learning Circuits:** Understand how circuits change when fine-tuning models on new tasks

5. **Intermodal Circuits:** Discover circuits in multimodal models (vision-language, audio-visual) that integrate information across modalities

6. **Interpretable Model Design:** Use circuit insights to design inherently interpretable vision transformers

## Code & Resources

### Official Implementation

- **ArXiv Paper:** https://arxiv.org/abs/2604.14477
- **HTML Version:** https://arxiv.org/html/2604.14477
- **Code Repository:** Likely available on authors' GitHub pages (check Max Planck Institute for Informatics repository pages)

### Dependencies and Requirements

**Core Libraries:**
```
pytorch >= 2.0
torchvision >= 0.16
transformers >= 4.30
timm >= 0.9.0  # For Vision Transformer models
open_clip >= 2.20  # For OpenCLIP models
PIL >= 9.0  # Image processing
numpy, scipy, matplotlib
```

**Computational Requirements:**
- **GPU:** High-end GPU (A100, H100, or equivalent) for full circuit discovery
- **Memory:** 40GB+ VRAM for ViT-B models
- **Storage:** 500GB+ for ImageNet and intermediate activations
- **Time:** Circuit discovery for single model: 48-72 hours on single A100

### Quick Start Guide

```python
# 1. Load pretrained ViT model
import timm
model = timm.create_model('vit_base_patch32_224', pretrained=True)

# 2. Prepare input image
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])
img = transform(Image.open('image.jpg')).unsqueeze(0)

# 3. Run circuit discovery (pseudocode)
from vi_cd import VisualCircuitDiscovery
vcd = VisualCircuitDiscovery(model)
circuit = vcd.discover_circuit(img, target_class=3)  # Dog class

# 4. Evaluate sparsity and faithfulness
accuracy = vcd.evaluate_circuit(circuit, test_dataset)
sparsity = vcd.compute_sparsity(circuit)
```

### Interactive Visualizations and Demos

- **Attention Visualization:** Interactive tools to explore which image regions each circuit focuses on
- **Circuit Comparison:** Visualize differences between circuits for different classes
- **Mechanistic Steering Demo:** Web interface to activate/deactivate circuits and observe output changes

## Related Work & Context

### Evolution of Circuit Discovery

**Language Models (Antecedent Work):**
- **Induction Heads (2022):** First mechanistic circuits identified in transformers for in-context learning
- **Causal Tracing (2021):** Foundational technique for circuit discovery via activation patching
- **Circuits in Transformers (2023):** Comprehensive analysis of interpretable circuits in GPT-2

**Vision Models (Context):**
- **Neuron-level analysis:** Prior work identified important neurons in CNNs and ViTs using attribution methods
- **Attention Visualization:** Attention heatmaps provide coarse spatial understanding but miss edge-level computation
- **Feature Visualization:** Activations show what neurons encode but don't reveal routing/flow

### Prior Interpretability Approaches for Vision

| Approach | Limitation | Vi-CD Advantage |
|----------|-----------|-----------------|
| Attention maps | No causal reasoning | Causal edge identification |
| Neuron importance | Coarse granularity | Fine-grained edge-level circuits |
| Feature visualization | Isolated unit analysis | Compositional pathway understanding |
| Gradient attribution | Shallow interpretation | Deep circuit structure |

### Relationship to Related xAI Communities

**LIME/SHAP Legacy:**
- Post-hoc local explanation methods; Vi-CD provides mechanistic (ante-hoc) explanations
- LIME/SHAP model-agnostic; Vi-CD white-box requiring model access
- Different use case: Vi-CD for researcher understanding; LIME/SHAP for end-user explanations

**Concept-Based Methods:**
- Identify high-level concept importance; Vi-CD identifies low-level computational structure
- Complementary approaches: concept methods answer "what," circuits answer "how"

**Causal Interpretability:**
- Causal graphs model causal relationships; circuits are learned computational pathways
- Potential integration: use circuit structure as basis for causal reasoning

**Fairness & Robustness:**
- Bias detection/mitigation: circuits enable targeted debiasing through selective deactivation
- Adversarial robustness: understanding circuits of adversarial vulnerability enables better defenses

### Where This Leads Next

1. **Scaling to Billion-Parameter Models:** Will circuit discovery remain tractable at 1B+ parameters?

2. **Multimodal Mechanistic Interpretability:** How do circuits differ in vision-language models? Can we discover shared circuits across modalities?

3. **Theoretical Foundations:** Develop mathematical framework explaining why circuits have observed structure

4. **Circuit Editing for Safety:** Use circuits as manipulation target for aligning large vision models without retraining

5. **Emergent Computation Theory:** Does circuit analysis reveal how emergence occurs in neural networks?

## Summary

"Seeing Through Circuits: Faithful Mechanistic Interpretability for Vision Transformers" represents a significant advance in explainable AI by extending edge-based circuit discovery—previously successful in language models—to the visual domain. Through the Vi-CD method, researchers demonstrate that vision transformers decompose into sparse, faithful circuits that perform specific computational tasks. This enables not only unprecedented understanding of how visual neural networks make decisions but also practical applications like mechanistic steering to defend against adversarial attacks and remove bias.

The work's implications extend far beyond academic interpretability: it enables certification of vision AI for medical imaging, autonomous vehicles, and other safety-critical domains; supports regulatory compliance with GDPR and the AI Act; and provides tools for auditing fairness and robustness. By unifying mechanistic interpretability across modalities, this research advances the larger goal of trustworthy, transparent AI systems.

The outstanding challenges—scaling to larger models, theoretical understanding of why circuits emerge, and handling distribution shift—point to exciting future research directions that will further strengthen the foundation of interpretable AI.
