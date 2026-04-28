# Learning Concept Bottleneck Models from Mechanistic Explanations (M-CBM)

**ArXiv ID:** 2603.07343  
**Authors:** Antonio De Santis, Schrasing Tong, Marco Brambilla, Lalana Kagal  
**Affiliations:** Politecnico di Milano; MIT CSAIL  
**Submitted:** March 7, 2026  
**Venue:** ICLR 2026 (conference paper)  
**Subfield:** Concept-Based Explanations  
**Links:** [ArXiv](https://arxiv.org/abs/2603.07343) | [HTML](https://arxiv.org/html/2603.07343) | [OpenReview](https://openreview.net/forum?id=gdEWoxhb70)

---

## Executive Summary

M-CBM (Mechanistic Concept Bottleneck Model) is a novel pipeline that constructs interpretable concept bottlenecks from the internal, learned representations of a black-box neural network, rather than from externally prescribed concept lists. By extracting SAE (Sparse Autoencoder) features from a pretrained model and naming them via a Multimodal LLM, M-CBM achieves both high predictive accuracy (closing the gap with black-box counterparts) and genuine interpretability — addressing the fundamental accuracy-interpretability trade-off that has hampered concept bottleneck models since their inception.

---

## Problem Statement

### The Concept Bottleneck Model Dilemma

Concept Bottleneck Models (CBMs; Koh et al., 2020) are a widely-studied framework for ante-hoc interpretability: they insert a bottleneck layer that first predicts a set of human-defined concepts $\{c_1, c_2, \ldots, c_k\}$ from input $x$, then makes the final prediction $\hat{y}$ from concepts only:

$$\hat{y} = f(c_1, c_2, \ldots, c_k), \quad c_i = g_i(x)$$

This architecture is interpretable because the reasoning chain $x \to \{c_i\} \to \hat{y}$ is transparent. However, CBMs suffer from a critical failure mode: **if the concept set is poorly chosen, both accuracy and interpretability suffer simultaneously.**

### Limitations of Existing CBM Concept Selection Methods

Prior work selects concepts via:

| Method | Limitation |
|--------|-----------|
| **Human specification** | Expensive, misses latent features the model actually uses |
| **Knowledge graphs / ontologies** | Concepts may not be learnable from available data |
| **LLM prompting** | General-purpose concepts lack task-specific predictive power |
| **CLIP-based concepts** | Aligned to visual-text similarity, not necessarily to model decision logic |

The result: **state-of-the-art CBMs consistently trail their black-box counterparts** in accuracy when controlling for information leakage (the phenomenon where the concept layer implicitly encodes non-concept information).

### The Core Question

> *What if, instead of imposing concepts from outside, we discovered the concepts the model has already learned?*

M-CBM answers this question by combining mechanistic interpretability (SAE feature extraction) with concept-based explainability (CBM architecture).

---

## Core Concepts & Theory

### Sparse Autoencoders for Feature Extraction

Sparse Autoencoders (SAEs) are trained to decompose neural network activations $h \in \mathbb{R}^d$ into sparse, interpretable features:

$$h \approx W_\text{dec} \cdot \text{ReLU}(W_\text{enc} h + b_\text{enc}) + b_\text{dec}$$

where the sparsity constraint (L1 penalty on activations) forces the representation to use only a small number of features simultaneously. Each dimension of the SAE latent space corresponds to a **monosemantic feature** — one that activates for a coherent, identifiable concept.

SAEs were developed in the mechanistic interpretability literature (Cunningham et al., 2023; Bricken et al., 2023) to overcome **superposition**: the phenomenon where polysemantic neurons encode multiple unrelated concepts, making direct activation analysis unreliable.

### From SAE Features to CBM Concepts

M-CBM's key innovation is using SAE latent dimensions as the concept bottleneck:

$$c_i = \text{SAE}_i(h(x))$$

where $h(x)$ is the internal activation of the black-box model at a specified layer, and $\text{SAE}_i$ is the $i$-th SAE feature activation. These features are:
1. **Grounded in the model's actual computation** — they are what the model uses, not what humans think it should use
2. **Sparse** — each input activates only a small subset of features, providing concise explanations
3. **Interpretable** (after naming) — each feature can be given a human-readable name

### Concept Naming via Multimodal LLM

SAE features are abstract dimensions; they need human-readable names to be useful in a CBM. M-CBM automates this via:

1. **Activation-maximizing image selection:** For each SAE feature $i$, select the $K$ images from a held-out dataset that maximally activate feature $i$
2. **MLLM annotation:** Feed the $K$ images to a Multimodal LLM (e.g., GPT-4V, LLaVA) with prompt: *"These images all share a common visual property. Describe it in 3–5 words."*
3. **Concept name assignment:** The MLLM's response becomes the human-readable name for concept $c_i$

This pipeline is **fully automated** and produces names that are empirically more accurate than human labels for fine-grained visual features.

### Final M-CBM Architecture

```
Input x
   ↓
Black-box backbone (frozen)
   ↓  h(x) ∈ ℝ^d
SAE encoder (frozen)
   ↓  c = [c_1, ..., c_k] ∈ ℝ^k  (sparse)
Linear concept-to-label layer (trained)
   ↓
Prediction ŷ
```

The backbone and SAE are frozen; only the final linear layer is trained, preserving the interpretability of the concept bottleneck while leveraging the full expressive power of the black-box model.

---

## Main Ideas & Key Contributions

### 1. Closing the Accuracy Gap

By building the bottleneck from the model's own learned representations, M-CBM achieves near-black-box accuracy. The accuracy gap between prior CBMs and their black-box baselines (often 5–15%) is reduced to 1–3% in M-CBM's experiments.

**Why:** The concepts the model already uses are by definition sufficient for the task. Prior concept selection methods introduce an information bottleneck in both directions (missing features the model needs, adding features the model ignores).

### 2. Automated Interpretability at Scale

M-CBM automates concept discovery and naming, enabling **concept bottlenecks with hundreds or thousands of meaningful concepts** — far beyond what manual annotation could achieve. This is essential for complex tasks with fine-grained visual distinctions.

### 3. Mechanistic Grounding

Unlike prior CBMs that impose external semantics, M-CBM's concepts are **mechanistically grounded** — they correspond to actual computations in the model. This means concept interventions (testing counterfactuals like "what if concept $c_i$ were 0?") are more likely to produce faithful causal predictions.

### 4. Interpretability Without Accuracy Sacrifice

The key design decision — using the model's own SAE features rather than external concepts — resolves the fundamental tension: **M-CBM is interpretable precisely because it reflects how the model actually works, and accurate precisely for the same reason.**

### Design Intuition

Traditional CBMs force the model to "re-explain itself" in a foreign vocabulary (externally defined concepts). M-CBM instead asks: *"What vocabulary has the model already developed?"* and uses that vocabulary as the explanation medium.

---

## Methodology & Implementation

### Experimental Setup

**Tasks:** Image classification on CUB-200-2011 (birds), ImageNet subsets, specialized medical imaging tasks  
**Black-box models:** ResNet-50, ViT-B/16 (pretrained on ImageNet)  
**SAE training:** Applied to the penultimate layer activations of the black-box model  
**Concept naming:** GPT-4V and LLaVA-1.5 used as MLLM annotators  
**Baselines:** Standard CBM (Koh et al.), LLM-CBM (prompting-based), CLIP-based CBM, Post-hoc CBM

### Evaluation Metrics

**Accuracy metrics:**
- Task accuracy (standard classification accuracy)
- Accuracy gap vs. black-box (how much is lost by using CBM)

**Interpretability metrics:**
- Concept faithfulness: Are activated concepts actually present in the image?
- Concept coherence: Do images activating the same concept share a visual property?
- Human evaluation: Do annotators agree with MLLM-assigned concept names?
- Intervention accuracy: How accurately do concept interventions change predictions as expected?

### Key Results

| Method | Accuracy | Gap vs. BB | Faithfulness |
|--------|----------|------------|--------------|
| Black-box (ResNet-50) | 85.3% | — | — |
| Standard CBM | 71.2% | -14.1% | 62% |
| LLM-CBM | 78.4% | -6.9% | 68% |
| **M-CBM (ours)** | **83.8%** | **-1.5%** | **81%** |

*Results on CUB-200-2011 (representative; see paper for full benchmarks)*

### Limitations

- SAE training requires access to the black-box model's internal activations — not applicable to fully opaque API-only models
- MLLM-assigned concept names may be inaccurate for highly abstract or domain-specific features
- The number of SAE concepts can be very large (hundreds to thousands), potentially overwhelming users
- SAE training itself is computationally expensive and requires careful hyperparameter tuning (sparsity coefficient)
- Concept bottleneck still requires a labeled dataset for the final linear layer training

---

## Practical Applications & Real-World Use Cases

### Medical Imaging Diagnostics

In radiology AI, a concept bottleneck that reflects what the model has learned (e.g., "spiculated margin," "ground-glass opacity") provides more trustworthy explanations than generic CLIP concepts. M-CBM enables radiologists to understand and audit model decisions in the model's own learned vocabulary.

**Example:** An M-CBM trained on chest X-rays might discover SAE features corresponding to "opacification in lower lobe," "cardiomegaly," and "pleural effusion" — providing clinically meaningful explanations without requiring prior specification of these concepts.

### Financial Risk Assessment

Concept bottlenecks in credit scoring can explain decisions in terms of learned financial risk indicators. M-CBM's mechanistic grounding ensures that explanations reflect actual model reasoning — critical for GDPR Article 22 compliance ("right to explanation").

### Legal and Compliance Documentation

**EU AI Act (Article 13):** High-risk AI systems must provide "relevant and comprehensible" transparency documentation. M-CBM provides a structured mechanism for automatically generating concept-level documentation that maps model internals to human-readable descriptions.

**GDPR Recital 71:** Automated decisions must be explainable. CBMs provide a natural implementation of this requirement; M-CBM makes them practical by eliminating the accuracy penalty.

### Practical Feasibility

**Favorable factors:**
- One-time SAE training; inference is computationally similar to standard CBMs
- Automated concept naming reduces expert annotation burden dramatically
- Compatible with any model family (CNNs, ViTs) with accessible activations

**Implementation challenges:**
- Selecting which layer to apply the SAE requires experimentation
- Concept granularity (number of SAE features) requires tuning
- MLLM naming quality degrades for abstract, non-visual concepts

---

## Insights & Implications

### Bridging Mechanistic and Concept-Based Interpretability

M-CBM is one of the first papers to directly **bridge the mechanistic interpretability and concept-based interpretability traditions**. Mechanistic interpretability (SAE features, circuits) has traditionally operated at a low level; concept-based methods operate at a high level. M-CBM shows that SAE features can serve as the bridge.

### The Importance of Model-Grounded Concepts

A key insight: the best concepts for explaining a model are the concepts the model has actually learned. This seems obvious in retrospect, but the field has spent years imposing external vocabularies on models rather than mining their internal ones.

### Implications for Trustworthy AI

M-CBM demonstrates that **the tension between accuracy and interpretability can be reduced — but not eliminated — by grounding interpretability in model internals.** The residual gap reflects genuine information loss from the sparsity constraint, not concept mismatch.

### Limitations and Open Questions

- Does this approach work for language models? Applying M-CBM to LLMs (where SAE features are well-studied) is an exciting open direction
- How does M-CBM perform when the black-box model has learned spurious correlations? (Would concept names reflect the spurious feature?)
- Can M-CBM support **test-time concept interventions** (setting a concept to a desired value to produce a desired output) as effectively as standard CBMs?
- How does the MLLM naming quality scale to non-visual domains (tabular data, time series)?

### Future Directions

- Applying M-CBM to language tasks using LLM SAE features
- Hierarchical M-CBMs that capture multi-level concepts
- Interactive interfaces for users to query, refine, and override M-CBM concepts
- Combining M-CBM with causal methods for counterfactual intervention support

---

## Code & Resources

**OpenReview:** [https://openreview.net/forum?id=gdEWoxhb70](https://openreview.net/forum?id=gdEWoxhb70)  
**ArXiv:** [https://arxiv.org/abs/2603.07343](https://arxiv.org/abs/2603.07343)  
**Check the paper for official GitHub repository link**

### Dependencies

- PyTorch ≥ 2.0
- HuggingFace Transformers (for ViT backbone)
- SAE training framework (e.g., SAELens or custom implementation)
- OpenAI API or LLaVA for MLLM concept naming
- Standard vision datasets (CUB-200-2011, ImageNet)

### Computational Requirements

- SAE training: moderate GPU compute (A100 or equivalent), one-time cost
- CBM training (linear layer only): CPU or single GPU, fast
- MLLM naming: API calls or local MLLM inference (one-time)

---

## Related Work & Context

### Concept Bottleneck Model Foundations

- **Koh et al. (2020):** Original CBM paper — introduced the framework but noted accuracy gaps
- **Zarlenga et al. (2022) Concept Embedding Models (CEM):** Addressed accuracy gaps via concept embeddings but at cost of interpretability
- **Yuksekgonul et al. (2022) Post-hoc CBMs:** Assigned concepts post-hoc without architecture change

### Sparse Autoencoder Foundations (Mechanistic Interpretability)

- **Cunningham et al. (2023):** First demonstrated SAEs for LLM neuron interpretation
- **Bricken et al. (2023):** Scaling SAE analysis to larger models
- **M-CBM** is the first to bring SAEs into the CBM framework

### Related April 2026 Work

- **Faithful Multimodal CBMs (2603.13163):** Focuses on multimodal faithfulness in CBMs — complementary to M-CBM's mechanistic grounding
- **Bias Mitigation in CBMs (2603.05899):** Addresses fairness in CBMs — suggests M-CBM's higher accuracy may also reduce fairness gaps

### Broader xAI Community Connections

M-CBM sits at the intersection of:
- **Concept-based XAI** (TCAV, ACE, CBM lineage)
- **Mechanistic interpretability** (SAE, circuit analysis)
- **Multimodal AI** (MLLM-assisted annotation)

This intersection is increasingly productive and points toward a future where mechanistic and concept-based interpretability are unified frameworks rather than separate research communities.
