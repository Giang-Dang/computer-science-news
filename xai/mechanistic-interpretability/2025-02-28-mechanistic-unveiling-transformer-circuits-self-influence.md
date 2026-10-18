# Mechanistic Unveiling of Transformer Circuits: Self-Influence as a Key to Model Reasoning

**Authors:** Lin Zhang, Lijie Hu, Di Wang  
**ArXiv ID:** [2502.09022](https://arxiv.org/abs/2502.09022)  
**Submission Date:** February 28, 2025  
**Published:** Findings of the Association for Computational Linguistics: NAACL 2025 (Pages 1387–1404)  
**DOI:** 10.18653/v1/2025.findings-naacl.76

---

## Executive Summary

This paper introduces SICAF (Self-Influence Circuit Analysis Framework), a novel mechanistic interpretability framework that combines automated circuit discovery with self-influence functions to trace and analyze the reasoning processes of transformer models. By integrating circuit analysis—which identifies the computational subgraph responsible for specific behaviors—with self-influence scores that measure token importance across layers, the authors provide a human-interpretable view of how language models solve reasoning tasks. Experiments on GPT-2 using the Indirect Object Identification (IOI) task demonstrate that the identified circuits are sparse (containing only 1-2% of edges) yet retain 85%+ model performance, revealing that key reasoning operations are concentrated in early and final layers.

---

## Problem Statement

Understanding how transformer models perform reasoning has long been a challenge in mechanistic interpretability. While recent advances in circuit discovery have identified which parts of a model are responsible for specific behaviors, these methods often provide limited insight into *how* the model uses those circuits to reason through problems step-by-step.

**Key limitations in prior work:**
- **Circuit discovery alone** identifies *which* parameters matter, but doesn't clearly reveal the *sequence of reasoning steps* the model follows
- **Lack of temporal perspective:** Traditional circuit analysis typically focuses on end-to-end behavior without tracking how importance shifts across layers
- **Interpretability gap:** Even with identified circuits, it remains unclear how a human can intuitively understand the model's reasoning process
- **Limited evaluation:** Most mechanistic interpretability work focuses on simple synthetic tasks or narrow behaviors; scaling to complex reasoning remains open

This paper addresses these gaps by proposing a framework that layers self-influence analysis on top of circuit discovery, providing both *which parameters matter* (circuits) and *when and how they matter* (self-influence across layers).

---

## Core Concepts & Theory

### Circuit Discovery in Transformers

A **circuit** in a neural network is a computational subgraph—a subset of parameters and connections—that is necessary and sufficient for the model to exhibit a specific behavior. In transformers, circuits typically span multiple layers and attention heads.

**Edge Attribution Patching (EAP):** The paper uses EAP and its variants to discover circuits:
- **EAP:** A gradient-based method that efficiently identifies edges (weight matrices and attention connections) important for a target behavior by patching (zeroing) gradients
- **EAP-IG (Integrated Gradients variant):** Integrates attribution scores along a path between clean and corrupted inputs, addressing gradient suppression issues
- **EAP-IG-KL:** Extends EAP-IG using KL divergence as the importance metric, capturing broader changes in output distribution

### Self-Influence Functions

Self-influence measures how much a model's internal representations respond to a specific input token. Mathematically, it quantifies the degree to which changing an intermediate representation affects the model's behavior:

Self-Influence(token, layer) = |∂output / ∂hidden_state(token, layer)|

By computing self-influence scores for each token across all layers of a discovered circuit, the framework reveals:
1. **Which tokens are critical** at different reasoning stages
2. **Where in the network** key computational steps occur
3. **How importance evolves** through the reasoning process

### Mechanistic Interpretability Framework

The SICAF pipeline operates in three stages:

1. **Circuit Identification:** Use EAP/EAP-IG/EAP-IG-KL to identify a minimal subgraph responsible for the target task
2. **Self-Influence Computation:** For each sample, compute per-token self-influence scores across all layers in the identified circuit
3. **Reasoning Inference:** Analyze how self-influence patterns differ across layers to infer the model's step-by-step reasoning process

The key insight is that **self-influence patterns across layers reveal the temporal dynamics of reasoning**—which tokens matter most at which computational stages.

---

## Main Ideas & Key Contributions

### 1. **SICAF: A Novel Mechanistic Interpretation Framework**

The core innovation is the systematic combination of circuit discovery and self-influence analysis. While prior work focused on either identifying what parameters matter (circuits) OR understanding individual neurons/layers in isolation, SICAF unifies both perspectives to provide a coherent mechanistic story.

**Why this matters:** Circuit discovery identifies sparse, faithful computational structures, but SICAF adds the *interpretability dimension* by showing how those circuits actually implement reasoning through layer-wise token importance dynamics.

### 2. **Revealing Layer-Wise Reasoning Patterns**

A key finding is that reasoning-critical tokens show distinct self-influence patterns:

- **EAP method:** Shows concentrated importance in early layers (e.g., layer 4) and later layers (e.g., layers 10-11)
- **EAP-IG method:** Distributes importance more evenly across layers with peaks in early layers
- **Interpretation:** Early layers likely handle initial feature extraction and query/key separation; later layers aggregate and produce the final output

This layer-wise analysis provides granularity that raw circuit metrics alone cannot capture.

### 3. **Validation on IOI Task**

The Indirect Object Identification (IOI) task is a well-studied benchmark in mechanistic interpretability:

**Task:** Given "When John and Mary went to the store, John gave a bag to Mary. She gave..." predict "Mary" (referring to the object of the first sentence, not the subject).

**Circuit characteristics [Exact figures unavailable — see full paper]:**
- Identified circuits are extremely sparse: 1-2% of model parameters
- Remarkably faithful: retain 85%+ of GPT-2's performance even with 98%+ of parameters ablated
- Reveal interpretable sub-circuits aligned with human understanding of the reasoning process

### 4. **Comparative Analysis of Attribution Methods**

The paper systematically compares three circuit-discovery methods:

- **EAP:** Faster, but may miss near-zero gradients in some critical features
- **EAP-IG:** More robust to gradient suppression, produces more faithful circuits under parameter constraints
- **EAP-IG-KL:** Broader sensitivity but potentially less stable

By analyzing self-influence under each method, the paper shows that **EAP-IG provides the best balance between circuit fidelity and layer-wise interpretability**.

### 5. **Mechanistic Understanding of Reasoning**

Perhaps most importantly, the paper demonstrates that self-influence patterns can reveal *human-interpretable reasoning steps*:

- The model doesn't perform reasoning in a black-box way; instead, its circuits show structured, interpretable reasoning paths
- Different tokens (subjects, objects, verbs) play distinct roles at different layers
- The concentration of influence in early and final layers aligns with intuitions about attention flow

---

## Methodology & Implementation

### Experimental Setup

**Model:** GPT-2 (small, 12-layer transformer)  
**Task:** Indirect Object Identification (IOI)  
**Baseline:** Finetuned GPT-2 on synthetic IOI examples  

**Data:** Synthetic IOI sentences of the form: "When [A] and [B] went to [place], [A] gave a [object] to [B]. She gave..." (predict [B])

### Circuit Discovery Process

1. **Define target behavior:** Predicting the indirect object (the second person mentioned) in the IOI task
2. **Compute importance scores** using EAP/EAP-IG/EAP-IG-KL to identify critical edges
3. **Extract minimal circuit:** Threshold edges by importance to create a sparse subgraph
4. **Validate circuit:** Verify that ablating non-circuit edges maintains performance ([Exact numbers unavailable — see full paper])

### Self-Influence Analysis

For each input sentence and discovered circuit:

1. Compute forward pass with activations at all layers within the circuit
2. For each token and layer, compute the gradient of the loss w.r.t. the hidden state
3. Aggregate into self-influence scores: I(token, layer) = |∂loss / ∂h(token, layer)|
4. Visualize self-influence as a heatmap: tokens × layers

### Evaluation Metrics

**Circuit Quality:**
- **Sparsity:** Percentage of edges retained (lower is better)
- **Faithfulness:** Model performance with circuit intact, non-circuit edges ablated (higher is better, [Exact percentages unavailable — see full paper])
- **Minimality:** Comparison of circuits under parameter constraints (EAP-IG superior)

**Interpretability:**
- **Layer concentration:** Do reasoning operations cluster in interpretable layer ranges?
- **Token relevance:** Do important tokens (names, objects) show expected importance patterns?
- **Human alignment:** Do identified circuits match human intuitions about IOI reasoning? (approximate observation: yes for the compared methods)

### Limitations

1. **Limited to small models:** Experiments on GPT-2 only; scalability to larger transformers (GPT-3 scale) unclear
2. **Single task:** Evaluation on IOI; generalization to other reasoning tasks not demonstrated [Exact figures unavailable — see full paper]
3. **Circuit stability:** Recent work shows EAP-IG circuits shift when task definition is paraphrased, raising questions about the robustness of SICAF's reasoning interpretations
4. **Self-influence scope:** Limited to the discovered circuit; interactions outside the circuit not captured

---

## Practical Applications & Real-World Use Cases

### 1. **Understanding LLM Reasoning in Safety-Critical Domains**

**Application:** Autonomous systems, medical diagnosis  
**Use Case:** If an LLM makes a critical reasoning error (e.g., misidentifying a key entity in a medical scenario), SICAF can pinpoint exactly which layers and tokens led to the error, enabling targeted debugging.

**Regulatory angle:** Under proposed AI regulations (EU AI Act, FDA guidelines), explainability of model reasoning is increasingly required. SICAF provides mechanistic traceability that goes beyond post-hoc explanations.

### 2. **Model Compression and Optimization**

**Application:** Efficient inference  
**Use Case:** The discovery that reasoning circuits are sparse (1-2% of parameters) motivates structured pruning: retain circuit parameters, aggressively prune non-circuit components. SICAF guides which parameters are truly necessary for specific reasoning tasks, enabling task-specific model compression.

### 3. **Detecting and Mitigating Adversarial Attacks**

**Application:** Robustness and security  
**Use Case:** By understanding the exact computational pathway a model uses for reasoning, defenders can:
- Identify which layers are vulnerable to adversarial perturbations
- Design robust training objectives that protect critical reasoning circuits
- Detect when inputs trigger out-of-distribution reasoning patterns

### 4. **Debugging Model Behavior**

**Application:** Model development and improvement  
**Use Case:** When a model fails on a reasoning task, SICAF reveals:
- Which layers contributed to the failure
- Whether the error stems from early feature extraction or late aggregation
- Whether the model is using expected or unexpected computational pathways

### 5. **Compliance and Explainability**

**Regulatory context:** GDPR, HIPAA, FDA AI guidelines increasingly demand interpretability of automated decision-making.

**SICAF's value:** Unlike black-box post-hoc explanations (LIME, SHAP), SICAF provides mechanistic traceability—documenting the exact computation the model used, layer by layer. This stronger form of explainability may be increasingly required for high-stakes decisions.

### Implementation Considerations

- **Computational cost:** Circuit discovery (especially EAP-IG) is computationally expensive; may not scale to very large models without optimization
- **Expertise required:** Interpreting self-influence patterns requires familiarity with transformer mechanics; not accessible to non-ML practitioners
- **Task specificity:** Circuits are task-specific; reasoning in novel domains may require new circuit analysis

---

## Insights & Implications

### 1. **Transformers Have Interpretable, Sparse Reasoning Circuits**

A striking finding is that GPT-2 solves the IOI task using only ~1-2% of its parameters, and these circuits are interpretable. This suggests that:

- **Sparsity as a principle:** If sparse circuits suffice, the model isn't fundamentally entangling reasoning with other capabilities
- **Interpretability is possible:** The relative simplicity of reasoning circuits makes mechanistic understanding achievable
- **Future architectures:** Designing models to naturally produce interpretable circuits could improve both explainability and efficiency

### 2. **Layer-Wise Reasoning is a General Principle**

The observation that important tokens cluster in early and final layers suggests a general principle:

- **Early layers:** Decompose input into meaningful features (identifying subjects, objects, relationships)
- **Middle layers:** Propagate information and perform intermediate computations
- **Final layers:** Aggregate features and produce output

This aligns with findings in vision transformers and other domains, suggesting a universal transformer reasoning pattern.

### 3. **Self-Influence Adds Interpretability Dimension to Circuits**

While circuit discovery identifies *which* parameters matter, self-influence answers *when and how* they matter. This distinction is crucial:

- **Circuits alone:** "These 2% of parameters are necessary"
- **Circuits + self-influence:** "These parameters matter because token X is important at layer Y, and here's why"

The additional interpretability dimension may be essential for building trust in AI systems.

### 4. **Implications for Mechanistic Interpretability Research**

- **Scalability:** Can SICAF scale to GPT-3 or larger models? Early indications are mixed (circuit discovery is expensive)
- **Robustness:** Recent work showing that circuits shift under paraphrasing raises questions about the stability of SICAF's interpretations
- **Universality:** Does SICAF reveal general reasoning principles, or task-specific quirks?

### 5. **Limitations and Open Questions**

- **Beyond IOI:** The IOI task is well-studied but relatively simple. How does SICAF perform on more complex multi-step reasoning?
- **Circuit interactions:** SICAF focuses on the identified circuit; interactions between circuit and non-circuit parameters are not fully captured
- **Generalization:** Circuits discovered on one distribution (synthetic IOI examples) may not transfer to naturally-occurring text

---

## Code & Resources

### Official Implementations & Repositories
- **ArXiv paper:** [2502.09022 on arxiv.org](https://arxiv.org/abs/2502.09022)
- **ACL Anthology:** [DOI 10.18653/v1/2025.findings-naacl.76](https://aclanthology.org/2025.findings-naacl.76/)
- **PDF:** [Direct PDF link](https://arxiv.org/pdf/2502.09022)

### Related Tooling & Dependencies

The paper builds on established mechanistic interpretability libraries:

- **TransformerLens** (GitHub: `TransformerLensOrg/TransformerLens`): Essential library for mechanistic interpretability of transformers, providing hooks into intermediate activations
- **CircuitsViz:** Visualization tools for circuit analysis
- **EAP implementation:** The paper likely extends existing EAP implementations from prior circuit-discovery work

### Dependencies and Requirements

[Exact dependencies unavailable — see full paper for implementation details]

Common requirements for mechanistic interpretability work:
- PyTorch (recent version with autograd support)
- NumPy, SciPy
- Matplotlib/Plotly for visualization
- Weights & Biases (W&B) for experiment tracking (common in ML research)

### Quick Start (Reconstructed from methodology)

1. **Load GPT-2 and target task:** Finetuned model on IOI task
2. **Discover circuit using EAP-IG:** Run circuit discovery with importance threshold
3. **Compute self-influence:** For each input and discovered circuit, compute per-token importance across layers
4. **Visualize:** Generate heatmaps showing token importance distributions
5. **Interpret:** Analyze patterns to infer reasoning steps

### Interactive Visualizations

[Details unavailable — likely included in paper appendix or supplementary materials]

---

## Related Work & Context

### Prior Circuit Discovery Methods

**Automatic Circuit Discovery (ACDC)** (Conmy et al., 2023): One of the first methods to algorithmically find circuits; uses a greedy edge-removal approach. SICAF builds on ACDC's insights but uses gradient-based methods (EAP) for efficiency.

**Edge Attribution Patching (EAP)** (Wang et al.): A gradient-based circuit discovery method that efficiently identifies important edges. SICAF uses EAP and its variants directly.

**Activation Patching & Causal Analysis** (Nanda et al.): Studies causal effects of individual neurons/attention heads; provides complementary perspective to circuit-level analysis.

### Self-Influence and Attribution Functions

**Influence Functions** (Koh & Liang, 2017): Classic work on tracing model predictions to training data. Self-influence is a variant applied to internal representations rather than training examples.

**Integrated Gradients** (Sundararajan et al., 2017): Attribution method combining gradients along paths; used as a variant (EAP-IG) in this paper.

**Layer-wise Relevance Propagation (Bach et al.)**: Another approach to understanding layer-wise importance; SICAF provides a more direct, empirically-grounded alternative.

### Mechanistic Interpretability Community

**Transformer Circuits Initiative** (Anthropic, Distill): Pioneering work on understanding transformers mechanistically, including studies of induction heads, copy suppression circuits, and other phenomena. SICAF contributes to this broader research direction.

**IOI Task**: Standard benchmark in mechanistic interpretability, introduced by multiple papers studying how transformers handle indirect object identification.

### Broader xAI Landscape

- **Concept-Based Explanations (TCAV, ACE):** Focus on human-interpretable concepts rather than individual features
- **Counterfactual Explanations:** "What if we changed X?" approach; mechanistic circuits provide a mechanistic alternative
- **Faithfulness in Explanations:** Growing literature on ensuring explanations truly reflect model behavior; circuit-based explanations are inherently more faithful

### Future Research Directions

1. **Scaling mechanistic interpretability:** Can SICAF methods scale to GPT-3 or larger? Preliminary indications suggest computational bottlenecks at current scales
2. **Multi-task reasoning:** Beyond IOI, how do models solve complex, multi-step reasoning problems?
3. **Circuit composition:** Do complex tasks compose multiple circuits, and if so, how do they interact?
4. **Natural distribution:** How do circuit findings on synthetic tasks transfer to natural language?
5. **Robustness & stability:** Addressing the finding that circuits shift under paraphrasing; understanding circuit universality

---

## Summary

"Mechanistic Unveiling of Transformer Circuits: Self-Influence as a Key to Model Reasoning" advances mechanistic interpretability by combining circuit discovery with self-influence analysis to provide human-interpretable views of model reasoning. The SICAF framework reveals that transformers solve reasoning tasks using sparse, interpretable circuits, with key operations concentrated in early and final layers. By tracking token importance across layers, the paper moves beyond identifying *which* parameters matter to understanding *how* they contribute to reasoning. While current evaluation is limited to GPT-2 and the IOI task, the framework provides a template for understanding reasoning in larger models and more complex tasks. As AI systems increasingly handle safety-critical decisions, such mechanistic understanding is essential for building trust and ensuring explainability.

---

## References & Citation

**Citation (BibTeX):**
```bibtex
@inproceedings{zhang2025mechanistic,
  title={Mechanistic Unveiling of Transformer Circuits: Self-Influence as a Key to Model Reasoning},
  author={Zhang, Lin and Hu, Lijie and Wang, Di},
  booktitle={Findings of the Association for Computational Linguistics: NAACL 2025},
  pages={1387--1404},
  year={2025},
  doi={10.18653/v1/2025.findings-naacl.76}
}
```

**Related Papers & Further Reading:**
- [Transformer Circuits Initiative papers](https://distill.pub/) — Foundational mechanistic interpretability work
- [Edge Attribution Patching (EAP)](https://arxiv.org/abs/2310.10348) — Circuit discovery method used in this paper
- [Automatic Circuit Discovery (ACDY)](https://arxiv.org/abs/2304.14997) — Predecessor to modern circuit discovery
- [IOI Task & Related Work](https://arxiv.org/abs/2202.12576) — Original IOI study in mechanistic interpretability
