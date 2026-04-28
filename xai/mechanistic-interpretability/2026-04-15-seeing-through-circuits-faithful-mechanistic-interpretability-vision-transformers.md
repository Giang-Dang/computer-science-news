# Seeing Through Circuits: Faithful Mechanistic Interpretability for Vision Transformers

**ArXiv ID:** [2604.14477](https://arxiv.org/abs/2604.14477)  
**Authors:** Nina Żukowska, Wolfgang Stammer, Bernt Schiele, Jonas Fischer  
**Submission Date:** April 15, 2026  
**Subfield:** Mechanistic Interpretability — Circuit Discovery for Vision Models

---

## Executive Summary

This paper introduces **Vi-CD (Visual Circuit Discovery)**, the first edge-based circuit discovery method for Vision Transformers (ViTs). Inspired by computational graph-based mechanistic interpretability developed for large language models, Vi-CD recovers class-specific circuits that are up to 10× sparser than prior approaches while remaining faithful to model behavior. Beyond passive analysis, the discovered circuits enable **mechanistic steering** — targeted interventions on circuit edges — demonstrated by reducing typographic attack success rates in CLIP by more than 90%, offering a direct pathway from interpretability to AI safety.

---

## Problem Statement

### The Interpretability Gap in Vision Models

Mechanistic interpretability has made significant inroads into understanding language models through **circuit analysis** — identifying the minimal subgraph of a neural network responsible for a specific capability. However, vision models have lagged behind: prior circuit discovery methods for Vision Transformers relied exclusively on **neuron-based circuits**, which identify *what* information is encoded in specific neurons but cannot explain *how* that information flows and routes through the complex attention wiring of the network.

### Limitations of Prior Approaches

1. **Neuron-only granularity:** Prior ViT interpretability methods (e.g., DINO attention maps, attention rollout) visualize which patches are attended to, but do not reveal the causal computation graph connecting those observations to the output.
2. **Faithfulness concerns:** Many saliency-based methods in vision (Grad-CAM, integrated gradients) correlate with model behavior without causally validating that the highlighted regions drive the decision.
3. **Dense circuits:** Existing automated circuit discovery approaches (e.g., ACDC) tend to produce large, overlapping circuits across tasks that are hard to interpret in isolation.
4. **No transfer from LLM methods:** Edge-based circuit analysis — which captures both node activations AND the edges (attention weights) routing information — had not been adapted to the ViT architecture.

### Why This Matters

Vision models underpin high-stakes systems: autonomous vehicles, medical imaging AI, content moderation. Without understanding *how* a ViT routes visual evidence to its output, we cannot verify alignment between model reasoning and human judgment, nor correct failures in a principled way.

---

## Core Concepts & Theory

### Vision Transformers and the Residual Stream

A Vision Transformer (ViT) processes an image by:
1. Dividing it into fixed-size patches and projecting each to an embedding (patch tokens)
2. Prepending a special `[CLS]` token that aggregates global information
3. Passing the sequence through L transformer blocks, each containing multi-head self-attention (MHSA) and a feed-forward network (FFN)

The **residual stream** formulation (Elhage et al., 2021) is key: each block adds its output to the residual stream rather than replacing it. This means information accumulates additively, and we can trace how specific computations contribute to the final `[CLS]` token used for classification.

Formally, the output of block l is:
```
x^(l) = x^(l-1) + MHSA^(l)(x^(l-1)) + FFN^(l)(x^(l-1))
```

### Circuits as Computational Subgraphs

A **circuit** is a subgraph of the full computation graph that is sufficient to explain a model behavior, defined by:
- **Nodes:** attention heads, MLP layers, or individual neurons
- **Edges:** the flow of information between nodes via the residual stream

In language models, circuits have been identified for tasks like indirect object identification, greater-than comparisons, and factual recall. Vi-CD extends this framework to vision.

### The Vi-CD Method

Vi-CD discovers circuits through **edge attribution patching (EAP)**, adapted for ViTs:

**Step 1 — Clean and Corrupted Forward Passes:**
- Run a *clean* forward pass on an image of class C (e.g., a cat image)
- Run a *corrupted* forward pass on a structurally similar but class-different image (e.g., a dog image) to establish a baseline

**Step 2 — Attribution via Activation Patching:**
For each edge (i → j) in the computational graph:
```
attribution(i→j) = E[f_logit(patch_{i→j}(clean, corrupt)) - f_logit(corrupt)]
```
Where `patch_{i→j}` replaces the activation at node j's input from node i with the corrupted value. A high attribution means that edge carries class-specific information.

**Step 3 — Thresholding:**
Apply a sparsity threshold τ to retain only the top-k% most attributed edges, forming the class circuit C_k.

**Step 4 — Faithfulness Validation:**
Evaluate the retained circuit by measuring how well it alone (with all other edges ablated) recovers the model's original output logit for class C. A faithful circuit satisfies:
```
|f_logit(x; full_model) - f_logit(x; circuit)| < ε
```

### Circuit Steering

Once a circuit is identified, Vi-CD enables **mechanistic steering** by amplifying or suppressing specific circuit edges. For typographic attack defense, steering deactivates edges in the "text-reading circuit" that CLIP uses to be fooled by superimposed text labels.

---

## Main Ideas & Key Contributions

### 1. First Edge-Based Circuits for ViTs

Vi-CD is the **first method to apply edge-level circuit analysis to Vision Transformers**, closing the gap between language model mechanistic interpretability and vision model interpretability. Prior ViT circuit work was limited to identifying important neurons (nodes), ignoring the routing structure between them.

### 2. 10× Sparser Circuits

Compared to neuron-based baselines, Vi-CD circuits are up to 10× sparser — meaning they use far fewer model components to explain a given classification behavior. This sparsity:
- Makes circuits more human-interpretable (fewer components to trace)
- Reduces noise from non-essential computations
- Enables clearer causal attribution

### 3. Scalability to Large-Scale Models

Vi-CD scales to **ViT-B/16** (86M parameters) and **OpenCLIP** (vision encoder of large multimodal models), demonstrating that the method is practical for production-scale vision architectures, not just toy models.

### 4. Mechanistic Steering for Safety

The discovered circuits are not merely descriptive — they are **actionable**. Steering experiments demonstrate:
- **Typographic attack defense:** Reducing attack success rates by **>90%** in CLIP by intervening on the text-processing subcircuit identified through Vi-CD
- **Safety violation reduction:** Halving safety violations on the **RoCOCO benchmark** without degrading general model performance
- This serves as causal validation: if steering a circuit produces predicted effects, the circuit captures a genuine mechanism

### 5. Separating "What" from "How"

By focusing on edges (information routing), Vi-CD separates:
- *What* information is encoded (answerable by probing/linear classifiers)
- *How* that information flows to produce the output (answerable by circuit analysis)

This distinction is crucial for mechanistic understanding — knowing that layer 8 encodes "fur texture" is less useful than knowing which heads route that information to the classification output.

---

## Methodology & Implementation

### Models Evaluated

| Model | Architecture | Scale | Task |
|-------|-------------|-------|------|
| ViT-B/16 (ImageNet) | ViT-Base, patch 16 | 86M params | Classification |
| OpenCLIP ViT-B/32 | CLIP vision encoder | 87M params | Zero-shot + typographic attack defense |

### Datasets Used

- **ImageNet-1K:** Standard classification benchmark; circuits extracted per class
- **TinyImageNet:** Smaller validation set for ablation studies  
- **RoCOCO:** Benchmark for measuring safety violations in vision-language models
- **Typographic Attack Dataset:** Custom images with superimposed misleading text labels

### Evaluation Metrics

**Faithfulness:**
```
Faithfulness = 1 - |logit(full_model) - logit(circuit_only)| / |logit(full_model) - logit(ablated)|
```
A faithfulness of 1.0 means the circuit fully accounts for the model's output; 0.0 means it captures nothing beyond the ablated baseline.

**Sparsity:** Number of edges in circuit / Total edges in model (lower is more interpretable)

**Attack Success Rate (ASR):** Fraction of typographic attacks successfully fooling the model (lower after steering = better defense)

### Results

| Method | Faithfulness | Sparsity | ASR (pre-steering) | ASR (post-steering) |
|--------|-------------|---------|-------------------|-------------------|
| Neuron-based circuits | 0.82 | 12.4% | 67% | 41% |
| Vi-CD (ours) | **0.89** | **1.3%** | 67% | **6%** |

Vi-CD circuits are ~10× sparser while achieving higher faithfulness, and mechanistic steering reduces the attack success rate from 67% to 6%.

### Limitations

1. **Computational cost:** Running EAP requires multiple forward passes per edge attribution; scaling to very large ViTs (ViT-L, ViT-H) requires optimization
2. **Circuit overlap:** For fine-grained classes (e.g., dog breeds), circuits may share many edges, making class-specific analysis harder
3. **Static circuits:** Circuits are extracted at test time for a fixed input distribution; out-of-distribution inputs may activate different subgraphs
4. **Ground truth circuits:** Unlike algorithmic tasks in LLMs, there is no ground-truth circuit for real-world image classification to validate against

---

## Practical Applications & Real-World Use Cases

### 1. AI Safety: Defending Against Typographic Attacks

**Problem:** CLIP-based models are vulnerable to typographic attacks — physical or digital overlays of misleading text on images (e.g., writing "iPod" on an apple) that cause misclassification. This is a known adversarial risk in multimodal AI systems.

**Vi-CD Solution:** By identifying the subcircuit responsible for processing text tokens in CLIP's vision encoder and using mechanistic steering to suppress it during inference, typographic attack success drops from 67% → 6% with no general performance degradation.

**Real-world relevance:** Content moderation systems, autonomous vehicles (adversarial road signs), medical AI (watermarked scans).

### 2. Model Debugging & Quality Assurance

Industrial deployment of vision models requires understanding *why* a model fails on certain inputs. Vi-CD enables engineers to:
- Extract the circuit for a specific failure class
- Identify which edges are miscalibrated
- Make targeted corrections without full retraining

### 3. Regulatory Compliance (EU AI Act, GDPR)

The EU AI Act (2024) requires "high-risk AI systems" to provide documentation of their internal reasoning. Circuit-level explanations offer a formal, auditable representation of model behavior that goes beyond post-hoc saliency maps.

### 4. Medical Imaging AI

In pathology, radiology, and dermatology AI systems, Vi-CD can identify *which visual pathways* the model uses to detect a disease marker. If those pathways correspond to clinically valid features (rather than spurious artifacts), the model can be certified for clinical use.

### 5. Foundation Model Analysis

As CLIP and similar foundation models underpin diverse downstream tasks, understanding their visual processing circuits enables:
- Transfer learning analysis (which circuits generalize vs. specialize)
- Alignment verification (do circuits correspond to human-defined concepts?)

---

## Insights & Implications

### For Trustworthy AI

Vi-CD represents a methodological step toward **verifiable AI**: models whose decisions can be traced to specific, auditable computational subgraphs. This is distinct from post-hoc explanations (e.g., Grad-CAM), which may not faithfully reflect the model's actual computation.

### Paradigm: From Observation to Intervention

The combination of circuit discovery + mechanistic steering embodies a **causal paradigm** for interpretability:
1. *Observe* correlational evidence (which regions/heads activate for class C)
2. *Hypothesize* a circuit (the minimal subgraph that causally drives class C)
3. *Intervene* to validate (steering confirms causality by producing predicted effects)
4. *Act* (apply steering for model correction or safety enforcement)

### Bridge Between LLM and Vision Interpretability

LLM mechanistic interpretability (e.g., Anthropic's circuit-finding work, induction heads) has been more developed than vision model interpretability. Vi-CD directly transfers these methods to ViTs, enabling cross-domain insights. For example, "induction head"-like circuits may exist in ViTs for texture repetition or spatial pattern recognition.

### Open Questions

1. **Universality:** Are similar circuits shared across ViT architectures (ViT vs. Swin vs. DeiT)?
2. **Emergent circuits:** Do more capable ViTs develop more modular circuits?
3. **Dynamic circuits:** Can circuits be tracked as a model is fine-tuned?
4. **Human alignment:** Do Vi-CD circuits correspond to human-described visual concepts?

---

## Code & Resources

- **Official Implementation:** [github.com/nina-zukowska/vi-cd](https://github.com/nina-zukowska/vi-cd) *(check paper for updated URL)*
- **ArXiv Paper:** [arxiv.org/abs/2604.14477](https://arxiv.org/abs/2604.14477)
- **Related Codebase:** Built on [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) for activation patching infrastructure

### Computational Requirements

- GPU: 1× NVIDIA A100 (40GB) for ViT-B/16 circuit extraction
- Circuit extraction time: ~2-4 hours per class on ImageNet-1K
- Inference with steering: negligible overhead over standard inference

### Quick Start (Conceptual)

```python
from vi_cd import CircuitDiscovery

# Load a pretrained ViT
model = load_pretrained_vit("ViT-B/16")

# Initialize circuit discovery
cd = CircuitDiscovery(model, task="classification")

# Extract circuit for "tabby cat" class
circuit = cd.discover_circuit(
    clean_images=cat_images,
    corrupted_images=dog_images,
    target_class="tabby_cat",
    sparsity_threshold=0.01  # keep top 1% of edges
)

# Evaluate faithfulness
faithfulness = cd.evaluate_faithfulness(circuit, test_images)

# Apply mechanistic steering (e.g., to suppress text processing)
steered_model = cd.apply_steering(model, circuit, suppression_factor=0.5)
```

---

## Related Work & Context

### Building Upon

- **ACDC (Conmy et al., 2023):** Automated circuit discovery for LLMs — Vi-CD adapts this to vision architectures
- **Edge Attribution Patching (Syed et al., 2023):** The EAP algorithm that Vi-CD extends
- **Attention Rollout (Abnar & Zuidema, 2020):** Earlier ViT interpretability; Vi-CD supersedes it with causal validation
- **Transformers Circuit Hypothesis (Elhage et al., 2021):** The theoretical framework of residual stream + attention heads as circuit components

### Related 2025-2026 Papers

- **Mechanistic Interpretability of Fine-Tuned ViTs on Distorted Images** (2503.18762): Analyzes attention head behavior in fine-tuned ViTs, complementary to Vi-CD's circuit approach
- **Counting Circuits in VLMs** (2603.18523, this repo): Applies circuit analysis to multimodal models for visual reasoning
- **Dyslexify: A Mechanistic Defense Against Typographic Attacks** (2508.20570): Independently develops mechanistic defense against typographic attacks, converging with Vi-CD's application

### Broader xAI Context

Vi-CD sits at the intersection of:
- **Mechanistic Interpretability:** Circuit analysis as a tool for understanding model computation
- **AI Safety:** Steering as a tool for mitigating specific failure modes
- **Computer Vision Interpretability:** Extending beyond saliency maps to causal analysis

The paper is a significant contribution to the emerging field of **vision model mechanistic interpretability**, which will become increasingly important as ViTs replace CNNs in safety-critical applications.
