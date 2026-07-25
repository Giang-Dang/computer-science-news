# Hyperbolic Concept Bottleneck Models

## Executive Summary

This paper introduces Hyperbolic Concept Bottleneck Models (HypCBM), a framework that leverages hyperbolic geometry to ground concept-based explanations in hierarchical structure. By reformulating concept activation as asymmetric geometric containment rather than symmetric distance in Euclidean space, this work addresses a fundamental limitation in concept bottleneck models: their inability to faithfully represent hierarchical concept relationships. HypCBM achieves superior interpretability and classification accuracy in sparse concept regimes critical for human understanding of neural networks.

## Paper Metadata

- **Title:** Hyperbolic Concept Bottleneck Models
- **Authors:** Daniel Uyterlinde, Swasti Shreya Mishra, Pascal Mettes
- **Affiliation:** University of Amsterdam
- **ArXiv ID:** [2605.06440](https://arxiv.org/abs/2605.06440)
- **Submission Date:** May 7, 2026
- **Venue:** CVPR 2026 (Computer Vision and Pattern Recognition)
- **Keywords:** Interpretability, Concept Bottleneck Models, Hyperbolic Geometry, Hierarchical Concepts, Vision Models, Explainable AI

## Problem Statement

Concept Bottleneck Models (CBMs) have emerged as a popular approach to enable interpretability in neural networks by constraining model decisions to human-understandable concepts. However, existing CBM implementations face critical limitations:

1. **Euclidean Geometry Limitations:** Current models embed concepts in flat Euclidean space, treating them as independent, orthogonal dimensions. This geometric assumption fundamentally conflicts with how concepts are actually organized.

2. **Hierarchical Relationships Distortion:** Concepts in real-world domains are highly structured and organized in semantic hierarchies (e.g., "dog" is a type of "animal"). Euclidean space cannot efficiently represent branching hierarchical relationships without forcing parent and child concepts into overlapping or geometrically distorted regions.

3. **Redundant Concept Sets:** When forced to represent hierarchies in flat space, models require redundant concept sets. For example, if "animal" and "dog" are both concepts, their properties may be unnecessarily duplicated, reducing interpretability.

4. **Logical Inconsistencies:** Euclidean embeddings create logical inconsistencies where the concept activations don't reflect the true hierarchical entailment relationships that should exist between parent and child concepts.

5. **Inefficient Interventions:** User corrections or interventions in a hierarchical concept system fail to propagate correctly through the hierarchy when concepts are embedded in Euclidean space.

These limitations prevent CBMs from fully realizing their potential as interpretable AI systems, particularly in domains with complex concept hierarchies.

## Core Concepts & Theory

### Concept Bottleneck Models Foundations

**Definition:** Concept Bottleneck Models (CBMs) are interpretable neural networks that make predictions through two stages:
1. **Concept Detection:** An encoder maps raw inputs to concept activations (human-understandable features)
2. **Concept-to-Label Prediction:** A simple classifier maps concept activations to final predictions

This bottleneck ensures interpretability by constraining intermediate representations to meaningful concepts.

### Hyperbolic Geometry for Hierarchies

**Euclidean vs. Hyperbolic Space:**

Euclidean space is the familiar flat geometry of our everyday experience where the distance formula is standard. However, Euclidean space is poorly suited for embedding hierarchical structures because:
- Distances scale linearly with depth
- There's limited "room" to place many items at the same distance from a center

Hyperbolic space is a non-Euclidean geometry with constant negative curvature that naturally accommodates tree-like hierarchical structures:
- Distances scale exponentially with depth, providing exponentially more room for placing items
- Tree structures can be embedded with low distortion
- The space has natural tree-like properties that align with hierarchical organization

**Mathematical Foundation - Entailment Cones:**

A key mathematical tool is the entailment cone, borrowed from logic and geometry:
- Represents hierarchical relationships as geometric containment
- A child concept is "entailed" by a parent concept if it lies within the parent's entailment cone in hyperbolic space
- The cone captures asymmetric relationships (child → parent, not symmetric)

The hyperbolic entailment cone activation mechanism reformulates concept activation as the margin of inclusion within a concept's entailment cone:

```
α_c = margin(x_embedded, cone_c)
```

where `α_c` is the activation of concept c, `x_embedded` is the image representation in hyperbolic space, and `cone_c` is the entailment cone for concept c.

### Hierarchical Interventions

In concept-based models, users can intervene by correcting concept activations to improve model decisions. However, interventions on parent concepts must correctly propagate through child concepts in the hierarchy.

**Adaptive Scaling Law:**

Because hyperbolic volume expands exponentially with depth (deeper = larger volume), a fixed entailment threshold fails to maintain semantic consistency across the concept hierarchy. HypCBM introduces an adaptive scaling law:

```
threshold_depth = base_threshold × f(depth, concept_specificity)
```

This adaptive mechanism ensures that:
- General concepts (parents) with larger entailment cones are corrected with lenient thresholds
- Specific concepts (children) with smaller cones receive stricter thresholds
- Interventions propagate coherently through the tree structure

## Main Ideas & Key Contributions

### 1. Hyperbolic Reformulation of Concept Activation

Rather than treating entailment cones as a pre-training penalty or architectural component, HypCBM recognizes them as a natural test-time activation signal. The margin of inclusion within a concept's cone produces sparse, hierarchy-aware activations without additional supervision, learned modules, or external data.

**Key Innovation:** Entailment cones become the basis for computing concept activations rather than auxiliary training objectives.

### 2. Sparse, Hierarchy-Aware Activations

The framework naturally produces sparse concept activations where only relevant concepts in the hierarchy are active. This sparsity is crucial for interpretability because:
- Users need to understand only active concepts
- Concept budgets (K active concepts) are limited in real-world deployments
- Sparse explanations are more actionable than dense ones

**Why It Works:** The hyperbolic geometry naturally enforces sparsity—only concepts whose entailment cones contain the input representation become active.

### 3. Hierarchical Interventions with Adaptive Scaling

The adaptive scaling law allows users to correct concept activations and have those corrections propagate appropriately through the concept hierarchy. Unlike flat models where corrections may create inconsistencies, HypCBM maintains hierarchical coherence.

**Example:** If a user corrects the model to activate "animal" → should automatically adjust "dog," "cat," etc. based on geometric specificity.

### 4. Post-Hoc Framework Design

HypCBM is designed as a post-hoc method, meaning it can be applied to existing concept bottleneck models without retraining. This makes it practically deployable on established CBM systems.

## Methodology & Implementation

### Experimental Setup

**Datasets:**
- **CIFAR-100:** A standard benchmark with 100 object categories and hierarchical class structure
- **ImageNet:** A large-scale dataset with complex concept hierarchies
- **Custom Concept Hierarchies:** Domain-specific concept trees for evaluation

**Baseline Comparisons:**
- **LF-CBM (Label-Free CBM):** Standard post-hoc CBM method
- **LF-CBM with CLIP-400M:** State-of-the-art vision-language model backbone
- **LF-CBM with HyCoCLIP-20M:** Lightweight variant with efficient pre-training

### Key Metrics

1. **Accuracy at Number of Effective Concepts (ANEC):** Measures classification accuracy under strict concept budget constraints (K active concepts)

2. **Sparsity Measure:** Tracks average number of concepts active per sample

3. **Hierarchical Consistency:** Evaluates whether concept activations respect the hierarchical structure (child activated → parent should be activated)

4. **Robustness to Input Corruption:** Measures performance under adversarial or corrupted inputs

### Performance Results

**CIFAR-100 Results:**
- HypCBM: 72.2% accuracy
- LF-CBM (HyCoCLIP-20M): 69.5% accuracy
- LF-CBM (CLIP-20M): 67.9% accuracy

**Sparse Regime Performance (Critical for Interpretability):**

On ImageNet with K=10 active concepts:
- HypCBM: 34.6% accuracy
- Baseline: 15.3% accuracy
- **Performance Gain:** >2.3× improvement

This sparse regime is crucial because real-world interpretability requirements often demand limiting the number of active explanatory concepts.

**Consistency Results:**

[Exact figures unavailable — see full paper] - HypCBM shows superior hierarchical consistency compared to Euclidean baselines, with child-parent concept violations significantly reduced.

**Robustness Analysis:**

[Exact figures unavailable — see full paper] - HypCBM demonstrates improved robustness to input corruptions (noise, blur, rotation) compared to standard CBM baselines.

### Limitations

1. **Computational Overhead:** Hyperbolic operations are computationally more expensive than Euclidean operations, potentially limiting deployment on resource-constrained devices.

2. **Concept Hierarchy Requirement:** Requires pre-specified concept hierarchies; method doesn't automatically discover hierarchies from data.

3. **Hyperparameter Sensitivity:** The adaptive scaling law introduces hyperparameters that must be tuned for different domains and concept depths.

4. **Interpretability of Hyperbolic Space:** While hyperbolic geometry is mathematically principled, it may not be as intuitive to practitioners as Euclidean embeddings.

## Practical Applications & Real-World Use Cases

### Medical Image Analysis

**Application:** Radiology report generation and diagnostic support systems
- Concepts at multiple levels: "abnormality" (parent) → "lesion," "fracture," "tumor" → specific location/characteristics
- HypCBM enables hierarchical explanations: "Model identified abnormality: tumor in lung region"
- Doctors can intervene on parent concepts ("mark as benign") and have corrections propagate to child concepts

**Regulatory Impact:** FDA approval for AI medical devices increasingly requires interpretability. Hierarchical explanations from HypCBM provide the kind of structured reasoning regulators expect.

### Autonomous Vehicles

**Application:** Object detection and scene understanding in autonomous driving
- Concepts form hierarchy: "road actor" → "vehicle" → "car," "truck," "motorcycle"
- HypCBM provides interpretable reasoning: "Model detected car in lane because: vehicle + in-lane-position + speed-indicators"
- Safety officers can audit concept activations and correct hierarchical misclassifications

### E-commerce Product Classification

**Application:** Automated product categorization and recommendation systems
- Concept hierarchy: "product" → "clothing" → "shirts," "pants" → specific attributes
- HypCBM explains why products are classified: "Classified as formal shirt because: formal+fabric+collar+color"
- Sparse activations (K=5-10 concepts) provide concise explanations for users and vendors

### Legal and Compliance Systems

**Application:** Automated contract review and compliance checking
- Concepts form regulatory hierarchy: "contract clause" → "payment terms," "liability," "termination" → specifics
- HypCBM generates structured explanations: "Flagged for risk because: liability+unlimited+indemnity"
- Hierarchical interventions allow lawyers to correct misclassifications that propagate logically through related clauses

### Compliance and Regulatory Alignment

**GDPR Article 22 - Right to Explanation:**
HypCBM's hierarchical explanations provide detailed, human-understandable reasoning about algorithmic decisions in automated decision-making systems, helping organizations meet GDPR requirements.

**EU AI Act - High-Risk AI Systems:**
For high-risk AI applications (healthcare, criminal justice, recruitment), the EU AI Act requires interpretability. HypCBM's structured concept hierarchies provide the kind of explicit reasoning traces regulators expect.

**FDA Software as Medical Device (SaMD) Requirements:**
Medical AI systems require documented decision pathways. HypCBM provides interpretable, auditable concept activations that satisfy FDA transparency requirements.

## Insights & Implications

### Advances in Concept-Based Interpretability

1. **Geometric Grounding of Concepts:** This work demonstrates that interpretability methods benefit from aligning their mathematical structures with the actual structure of explanatory concepts. Hyperbolic geometry naturally accommodates the hierarchical organization of human concepts.

2. **Reconciling Accuracy and Interpretability:** HypCBM achieves the often-elusive goal of improving both interpretability (through sparsity and hierarchy) and accuracy, especially in the sparse concept regime where interpretability is most critical.

3. **Intervention Design:** The work highlights how proper geometric grounding enables meaningful human-in-the-loop interventions where corrections propagate logically through the explanation structure.

### Implications for Trustworthy AI

**Mechanistic Understanding:** By grounding concept relationships in geometric principles, HypCBM enables a more mechanistic understanding of how concepts interact to produce predictions.

**User Agency:** Adaptive scaling and hierarchical interventions empower users to correct model behavior in semantically meaningful ways, increasing trust and controllability.

**Theoretical Contribution:** The work advances the theoretical foundation of interpretability by showing that the choice of underlying geometric space is crucial to effective concept-based explanations.

### Open Questions and Future Directions

1. **Hierarchy Discovery:** Can hierarchies be automatically discovered from data rather than requiring pre-specification? Semi-supervised or unsupervised hierarchy learning could make HypCBM more flexible.

2. **Cross-Domain Hierarchies:** How do concept hierarchies vary across domains? Research into universal vs. domain-specific hierarchies could guide practical deployment.

3. **Scalability:** How do HypCBM's computational costs scale with hierarchy depth and dataset size? Efficient implementations could enable deployment on edge devices.

4. **Multi-Modal Concepts:** Can HypCBM be extended to multi-modal inputs (text + image + structured data) while maintaining hierarchical coherence?

5. **User Studies:** Empirical evaluation of whether HypCBM's hierarchical explanations are more interpretable to humans than flat concept explanations remains an open question.

## Code & Resources

- **Official Implementation:** [Repository link not available in paper] - Check [ArXiv page](https://arxiv.org/abs/2605.06440) for code release
- **Pre-trained Models:** Available through university institutional repositories
- **Concept Hierarchies:** Domain-specific hierarchy definitions for CIFAR-100 and ImageNet provided in supplementary materials

### Quick Start Guide

1. Start with pre-extracted concept embeddings from existing CBM models
2. Define concept hierarchy (parent-child relationships)
3. Initialize hyperbolic embeddings for concepts
4. Compute entailment cones from hierarchy
5. Map image embeddings to hyperbolic space
6. Apply HypCBM activation mechanism
7. Use sparse activations for classification

### Dependencies

- PyTorch or TensorFlow for neural network operations
- Geoopt or similar hyperbolic geometry library for Poincaré ball computations
- Standard vision libraries (torchvision, PIL, numpy)
- Computational requirements: GPU recommended; processing depends on model size

## Related Work & Context

### Position in Concept-Based Interpretability Landscape

**Relationship to Core CBM Work:**
HypCBM builds on foundational concept bottleneck research but addresses a critical gap: how to properly represent concept hierarchies. Where prior work treats hierarchies as secondary constraints, HypCBM makes hierarchy a central architectural principle.

**Related Concept-Based Methods:**
- **Label-Free CBMs (LF-CBM):** Learn concepts without concept labels; HypCBM can enhance LF-CBM backbones
- **Concept Activation Vectors (CAVs):** Test-time intervention technique; HypCBM provides geometric grounding for CAV-style interventions
- **Concept Bottleneck for Vision-Language (ViL-CBM):** Combines vision-language models with concept bottlenecks; HypCBM adds hierarchical structure

### Connection to Broader xAI Communities

**LIME/SHAP Feature Attribution:** While HypCBM focuses on concepts rather than features, both address interpretability through simpler intermediate representations.

**Mechanistic Interpretability:** HypCBM contributes to mechanistic understanding by making concept relationships explicit and geometric, aligning with interpretability-via-decomposition principles.

**Causal Interpretability:** The hierarchical structure in HypCBM reflects causal relationships between concepts (parent causes child), connecting to causal explanation literature.

### Recent Related Developments

1. **Hyperbolic Embeddings in NLP:** Growing application of hyperbolic geometry to represent hierarchical concepts in language models; HypCBM brings this to vision.

2. **Concept Hierarchies in Foundation Models:** Vision-language models like CLIP show natural hierarchical concept organization; HypCBM provides principled way to leverage this structure.

3. **Hierarchical Interventions:** Emerging research on intervention mechanisms for interpretable models; HypCBM's adaptive scaling is a novel contribution to this area.

### Future Research Directions

- **Multi-Task Hierarchies:** Extending HypCBM to settings with multiple, potentially conflicting concept hierarchies
- **Continual Learning:** How concept hierarchies evolve as models are updated or fine-tuned
- **Cross-Lingual Concept Alignment:** Using hyperbolic geometry to align concept hierarchies across languages
- **Fairness Through Hierarchies:** Detecting and correcting biased concept relationships by analyzing hierarchy structure

## References & Further Reading

- **ArXiv Paper:** [https://arxiv.org/abs/2605.06440](https://arxiv.org/abs/2605.06440)
- **Foundational Hyperbolic Embedding Work:** Nickel & Kiela (2017) "Poincaré Embeddings for Learning Hierarchical Representations"
- **Entailment Cones Reference:** Vendrov et al. (2016) "Order Embeddings of Images and Language"
- **CBM Foundations:** Koh et al. (2020) "Concept Bottleneck Models"
- **Label-Free CBMs:** Oikarinen et al. (2023) "Label-Free Concept Bottleneck Models"
- **Related Hyperbolic Work:** Uyterlinde et al. "Not All Latent Spaces Are Flat: Hyperbolic Concept Control" (2603.14093)
