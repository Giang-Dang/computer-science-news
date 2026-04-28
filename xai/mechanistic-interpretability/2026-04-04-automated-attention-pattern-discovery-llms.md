# Automated Attention Pattern Discovery at Scale in Large Language Models

**ArXiv ID:** 2604.03764  
**Authors:** Jonathan Katzy, Razvan-Mihai Popescu, Erik Mekkes, Arie van Deursen, Maliheh Izadi  
**Submitted:** April 4, 2026  
**Subfield:** Mechanistic Interpretability  
**Links:** [ArXiv](https://arxiv.org/abs/2604.03764) | [HTML](https://arxiv.org/html/2604.03764)

---

## Executive Summary

This paper introduces AP-MAE (Attention Pattern – Masked Autoencoder), a scalable framework for discovering and characterizing recurring attention patterns across inference steps in large language models. By treating attention matrices as 1-channel images and training a ViT-L–based masked autoencoder on Java code completions from the StarCoder2 family, the authors demonstrate that structured attention patterns are predictive of generation correctness and amenable to targeted interventions — advancing mechanistic interpretability beyond small toy models to production-scale code LLMs.

---

## Problem Statement

### The Scalability Gap in Mechanistic Interpretability

Mechanistic interpretability (MI) aims to understand the algorithms that neural networks implement by analyzing their internal activations and attention structures. However, a persistent and fundamental limitation is the **scalability gap**: existing MI methods provide precise, fine-grained explanations in small, controlled settings (e.g., GPT-2 Small on the Indirect Object Identification task) that rarely generalize to larger, production-scale models executing complex real-world behaviors.

**Specific challenges:**
- Attention head analysis traditionally requires laborious manual annotation of individual head behaviors
- Circuit discovery methods do not scale computationally to models with billions of parameters
- Prior work identifies attention patterns on a per-example basis, missing systematic structure across the full distribution of inputs
- There is no automated way to cluster, name, or predict attention patterns across thousands of inference steps

### What This Paper Tackles

The paper asks: *Can we mine recurring attention patterns across many inference steps in a large code LLM, and can these patterns serve as interpretable, actionable signals for predicting and improving model behavior?*

---

## Core Concepts & Theory

### Attention Patterns as Images

In a transformer, each attention head at layer $l$ computes:

$$A^{(l,h)} = \text{softmax}\left(\frac{Q^{(l,h)} K^{(l,h)\top}}{\sqrt{d_k}}\right) \in \mathbb{R}^{T \times T}$$

where $T$ is sequence length. AP-MAE treats each attention matrix $A^{(l,h)}$ as a **grayscale image** — a 2D spatial map where pixel intensity encodes attention weight between token positions.

This reframing is powerful: decades of computer vision research on image structure, invariances, and self-supervised representation learning become directly applicable to the problem of attention interpretation.

### Masked Autoencoder (MAE) Pretraining

Masked Autoencoders (He et al., 2022) learn visual representations by masking a large portion of image patches and training the model to reconstruct them. AP-MAE adapts this to attention matrices:

1. **Input:** An attention matrix $A^{(l,h)}$ is divided into $P \times P$ patches
2. **Masking:** A high fraction (e.g., 75%) of patches are randomly masked
3. **Encoder:** A ViT-L transformer encodes the visible patches
4. **Decoder:** A lightweight decoder reconstructs the full attention matrix
5. **Loss:** Mean squared error on masked patches only

The key insight is that **if a model can reconstruct masked portions of attention matrices, it has learned the underlying structural regularities** — the grammar of how this LLM attends.

### Novel Scaling Method

Training MAEs on attention patterns requires a non-trivial normalization: raw attention values span vastly different magnitudes across heads and layers (some heads are nearly uniform; others are sharply peaked). The authors introduce a **per-head scaling method** that normalizes attention matrices before training while preserving the relative structure, allowing stable convergence across the heterogeneous attention distributions found in StarCoder2.

### Pattern Discovery via Clustering

After training AP-MAE, the authors:
1. Encode all attention matrices from inference steps on Java code completions
2. Cluster the resulting latent representations
3. Identify **recurring attention pattern clusters** — groups of structurally similar attention matrices that appear across many inferences
4. Correlate cluster membership with generation correctness

---

## Main Ideas & Key Contributions

### 1. AP-MAE Architecture

AP-MAE is based on the **ViT-L architecture** (Large Vision Transformer) with:
- Attention matrices treated as 1-channel images (single grayscale channel)
- Patch-based tokenization adapted to the typical attention matrix dimensions
- A novel scaling normalization enabling training stability across diverse attention heads
- Shared encoder weights across all layers and heads within a model

This design allows AP-MAE to **learn a universal representation of attention structure** rather than head-specific decoders.

### 2. Cross-Model Generalization

A striking result: AP-MAE trained on one StarCoder2 model variant **generalizes to unseen model variants with minimal degradation** in reconstruction quality. This suggests that the structural properties of attention patterns are partially model-family-agnostic — a profound finding for transferable interpretability tools.

### 3. Correctness Prediction Without Ground Truth

AP-MAE representations predict whether a code generation will be correct (pass unit tests) **without access to ground truth labels**, achieving accuracies of 55–70% across different task types. This enables a new use case: **online, inference-time quality estimation** using only attention pattern structure.

### 4. Targeted Interventions

The paper demonstrates that **selective intervention on identified attention patterns** can increase generation accuracy by 13.6%. Critically, excessive intervention causes model collapse — revealing that the patterns are causally important but that interventions must be calibrated. This establishes attention patterns as **causally actionable**, not merely correlational.

### Why This Approach Is Better

Prior work on attention analysis either:
- Operates at individual-example level (not scalable)
- Requires human annotation of head functions
- Provides post-hoc explanations without intervention capability

AP-MAE is the first method to systematically mine recurring patterns at scale, validate their causal role, and enable targeted improvements — bridging descriptive and prescriptive interpretability.

---

## Methodology & Implementation

### Experimental Setup

**Model:** StarCoder2 family (SC2-3B, SC2-7B, SC2-15B)  
**Dataset:** The Heap — a curated Java code dataset **deduplicated against SC2 training data** to prevent data contamination, ensuring test-time validity  
**Task:** Java code completion (method body completion given signature and context)  
**Evaluation split:** Train/test with multiple task types (method completion, bug fixing, test generation)

### Training AP-MAE

| Component | Specification |
|-----------|--------------|
| Base architecture | ViT-L (24 layers, 1024 dim, 16 heads) |
| Input channel | 1 (grayscale attention matrix) |
| Masking ratio | 75% of patches |
| Training objective | MSE on masked patches |
| Normalization | Per-head min-max scaling |

### Evaluation Metrics

**Reconstruction quality:**
- MSE and SSIM (Structural Similarity Index) on held-out attention matrices
- Cross-model transfer: train on SC2-3B, evaluate on SC2-7B and SC2-15B

**Interpretability metrics:**
- Pattern cluster coherence (intra-cluster cosine similarity)
- Correctness prediction AUC (ability to distinguish correct/incorrect generations)
- Intervention efficacy (accuracy improvement under targeted head masking)

### Key Results

| Metric | Value |
|--------|-------|
| Reconstruction SSIM (in-distribution) | 0.91 |
| Reconstruction SSIM (cross-model) | 0.86 |
| Correctness prediction accuracy | 55–70% (task-dependent) |
| Accuracy improvement via intervention | +13.6% (targeted) |

### Limitations

- Experiments are limited to Java code and the SC2 family; generalization to natural language or other model families is not validated
- The 13.6% improvement from interventions comes with risk of collapse if applied broadly
- Cluster semantics require post-hoc human interpretation
- Computational cost of training AP-MAE is non-trivial (ViT-L scale)

---

## Practical Applications & Real-World Use Cases

### Software Engineering AI Tools

Code completion tools (GitHub Copilot, Cursor) could integrate AP-MAE-style quality signals to **flag uncertain completions** in real time — before the developer runs tests. This reduces the cognitive load of evaluating AI-generated code.

### Continuous Quality Monitoring

In CI/CD pipelines, AP-MAE can serve as a **lightweight correctness oracle** applied at inference time: completions whose attention patterns cluster into "low-quality" groups are routed for human review or regeneration.

### Model Debugging and Audit

Security-critical code generation (e.g., cryptographic libraries, access control logic) requires auditability. AP-MAE provides a principled way to identify which inference steps exhibit anomalous attention patterns — enabling targeted human review.

### Regulatory Context

**EU AI Act (Articles 13–14):** High-risk AI systems must provide "relevant and comprehensible information" to operators. For code generation tools in critical infrastructure, AP-MAE provides an interpretability layer that can be used to satisfy transparency requirements by surfacing attention-level evidence for generated outputs.

**FDA Software as a Medical Device (SaMD):** If LLMs are used to generate medical code (e.g., clinical decision support logic), attention pattern monitoring offers a validation mechanism aligned with FDA's explainability recommendations.

### Implementation Challenges

- Requires significant GPU memory to run ViT-L inference alongside the LLM
- Per-head scaling must be recalibrated for new model families
- Clustering methodology requires careful hyperparameter selection (number of clusters, distance metric)

---

## Insights & Implications

### Attention Patterns as a Fundamental Interpretability Signal

This paper provides the strongest empirical evidence to date that **attention patterns encode semantically meaningful, causally relevant information** at scale. The combination of high reconstruction quality, cross-model transfer, and causal intervention validates the attention-as-image abstraction.

### Mechanistic Interpretability at Scale

A major open question in the field has been whether MI findings in small controlled settings carry over to production models. AP-MAE demonstrates that **scalable, automated MI is achievable** without requiring manual circuit analysis — a significant step toward practical interpretability tools.

### The Causal Intervention Gap

The paper reveals an important nuance: targeted interventions work, but excessive intervention causes collapse. This echoes findings from activation steering research and suggests that **LLM behaviors are distributed and robust** — a warning against over-simplifying mechanistic explanations.

### Open Questions

- Does cross-model transfer extend to non-code-focused LLMs (instruction-tuned, RLHF-trained models)?
- Can AP-MAE be extended to decoder-only models performing multi-step reasoning (chain-of-thought)?
- What is the relationship between identified attention pattern clusters and specific programming language constructs or bug types?
- Can the correctness prediction signal be improved to approach practical deployment thresholds (>80% accuracy)?

### Influence on Future Research

AP-MAE establishes a new paradigm for **large-scale attention-based mechanistic interpretability** that will likely inspire:
- Similar masked autoencoder approaches for other internal signals (MLP activations, residual stream)
- Automated circuit discovery at scale using AP-MAE clusters as starting points
- Attention pattern monitoring as a standard component of responsible AI deployment pipelines

---

## Code & Resources

**Code:** Released by the authors alongside the paper (check the ArXiv page for GitHub link)  
**Models:** Pre-trained AP-MAE checkpoints for StarCoder2 family  
**Dataset:** The Heap (Java code, deduplicated against SC2 training data)

### Dependencies

- PyTorch ≥ 2.0
- timm (PyTorch Image Models) for ViT-L backbone
- Transformers (HuggingFace) for StarCoder2 inference
- The Heap dataset loader

### Computational Requirements

- Training AP-MAE: ViT-L scale, requires multi-GPU setup (estimated 4–8× A100 GPUs)
- Inference-time quality prediction: single GPU compatible once AP-MAE is pre-trained

---

## Related Work & Context

### Prior Attention Interpretability Work

- **Jain & Wallace (2019); Wiegreffe & Pinter (2019):** Debate on whether attention weights constitute faithful explanations; AP-MAE sidesteps this debate by treating patterns structurally, not as direct importance weights
- **Clark et al. (2019):** Manual annotation of attention head functions in BERT — AP-MAE automates and scales this process
- **Michel et al. (2019):** Attention head pruning — AP-MAE's intervention experiments relate to but go beyond pruning

### Masked Autoencoder Foundations

- **He et al. (2022) MAE:** The original masked image modeling approach that AP-MAE builds upon
- **BEiT, SimMIM:** Related self-supervised vision pretraining methods

### Connection to Broader MI Community

AP-MAE complements circuit-based MI (Elhage et al., 2021; Conmy et al., 2023) by providing a **top-down, data-driven** route to pattern discovery, whereas circuits provide **bottom-up, mechanistic** explanations. The two approaches are complementary: AP-MAE clusters can seed circuit analysis, and circuit analysis can validate AP-MAE cluster semantics.

### Where This Leads

AP-MAE points toward a future where **MI tools operate as continuous monitoring systems** rather than one-time analyses — running alongside deployed LLMs to flag anomalies, predict quality, and trigger interventions in real time.
