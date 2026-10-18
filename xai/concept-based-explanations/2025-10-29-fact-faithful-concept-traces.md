# FaCT: Faithful Concept Traces for Explaining Neural Network Decisions

**ArXiv ID:** [2510.25512](https://arxiv.org/abs/2510.25512)

**Authors:** Amin Parchami-Araghi, Sukrut Rao, Jonas Fischer, Bernt Schiele (Max Planck Institute for Informatics)

**Submission Date:** October 29, 2025

**Venue:** NeurIPS 2025 (Advances in Neural Information Processing Systems 38, pp. 122410–122453)

**Code:** Available at paper repository (released)

---

## Executive Summary

FaCT proposes an inherently interpretable neural network model that provides **faithful-by-design** concept-based explanations for image classification decisions. Unlike post-hoc explanation methods that add interpretability after training, FaCT integrates concept explanations directly into the model architecture using B-cos transforms and sparse autoencoders. The paper also introduces **C²-Score**, a new metric for evaluating concept consistency in concept-based models without requiring human annotations. This work addresses a critical gap in explainable AI: while post-hoc concept explanations are widely used, they are often not faithful to model decisions. FaCT ensures that concepts directly influence predictions and can be traced from input to output.

---

## Problem Statement

**The Challenge of Faithful Post-Hoc Concept Explanations:**

Post-hoc concept-based explanation methods (such as concept activation vectors, prototype networks, and other concept bottleneck approaches) face a fundamental challenge: **faithfulness**. These methods extract or generate concepts *after* a model is trained, but there is no guarantee that the extracted concepts actually explain how the model makes decisions. A post-hoc explanation might be *plausible* to humans but not *faithful* to the model's internal reasoning.

**Key Limitations in Prior Work:**

1. **Unfaithfulness:** Post-hoc concepts often fail to capture the actual features the model uses for prediction
2. **Lack of Mechanistic Understanding:** Most methods cannot trace how concepts flow through the network layers
3. **Evaluation Challenges:** Existing metrics for concept quality rely on human annotations of predefined object parts, which may not align with what the model actually learns
4. **Limited Traceability:** It's unclear how concepts at different layers contribute to final predictions

**Why This Matters:**

In high-stakes domains (healthcare, autonomous systems, finance), stakeholders need explanations they can trust. A plausible-sounding but unfaithful explanation could lead to misguided decisions or dangerous system deployments.

---

## Core Concepts & Theory

### **1. The Faithfulness-by-Design Philosophy**

FaCT takes a fundamentally different approach: instead of adding interpretability post-hoc, it **builds faithfulness into the architecture itself**. This ensures that:
- Concepts are inherent to model computation, not retrofitted
- Concept contributions to predictions can be verified mathematically
- Traceability from input features to output logits is guaranteed

### **2. B-cos Networks: Pixel-Level Explanations**

**B-cos (Basis Cosine) networks** provide pixel-level importance attribution by design:
- Each layer is implemented as a dynamic-linear transformation
- The model output can be written as: `output = Σᵢ wᵢ * f(xᵢ)` where wᵢ are importance weights for input features xᵢ
- This ensures that the model output is faithfully attributable to input pixels
- However, B-cos networks alone only explain *which pixels* matter, not *what concepts* the model uses

**Mathematical Intuition:**
- Traditional neural networks: `y = f(W·x + b)` (non-linear, difficult to attribute)
- B-cos networks: Designed to be decomposable, with attributions arising from network structure itself

### **3. Sparse Autoencoders (SAEs): Concept Discovery**

To bridge the gap between pixel-level importance and semantic concepts, FaCT adds **sparse autoencoders** at intermediate layers:

- **Role:** Decompose hidden activations into interpretable, sparse concept vectors
- **Why Sparse:** Sparsity encourages each neuron to represent a single, interpretable concept (steering towards monosemanticity)
- **Placement:** SAEs are inserted at intermediate layers (not just at the final output), allowing concept-tracing across network depth
- **Faithfulness Property:** Because the underlying B-cos network is already faithful, the concept decomposition inherits this faithfulness

**Key Mathematical Property:**
Since B-cos networks allow exact per-feature attribution, and SAEs decompose activations into sparse concepts, the framework enables:
- **Exact per-concept logit contributions:** For each concept, we can compute exactly how much it contributes to the output
- **Layer-wise traceability:** Concepts can be traced from early to later layers, showing concept composition

### **4. Concept Consistency Metric (C²-Score)**

**The Problem:** Existing concept metrics assume alignment with predefined human object parts (e.g., "dog nose," "wheel"). But models may learn concepts that don't match human categories.

**The Solution - C²-Score:**
- Uses a **foundation model (DINOv2)** as a semantic reference without human annotations
- Measures whether the set of images that maximally activate a concept have consistent semantic meaning in DINOv2 feature space
- **Formulation (conceptual):** For each concept, collect top-K images with highest activation, extract DINOv2 embeddings, compute cosine similarity variance. Lower variance = higher consistency = more interpretable concept.
- **Advantage:** Agnostic to human-defined concepts; evaluates whether a concept's activations cluster semantically

---

## Main Ideas & Key Contributions

### **1. Faithful Concept-Based Explanations**

**Core Innovation:** Combine B-cos networks with sparse autoencoders to create a model that provides concept explanations guaranteed to be faithful by design:
- Every concept's contribution to each logit can be computed exactly
- Concept contributions sum to the final prediction (no unexplained variation)
- Concepts are inherent to the model, not added post-hoc

### **2. Concept Traceability Across Layers**

Unlike methods that only provide final-layer concepts, FaCT enables:
- Inspection of concepts at *any layer* of the network
- Understanding of how low-level concepts compose into higher-level semantic meanings
- Verification that concept hierarchies align with human intuition

### **3. C²-Score: Universal Concept Evaluation Metric**

**Significance:** First metric that evaluates concept *semantic consistency* without human-annotated object parts.
- Applicable to any concept-based model (not just FaCT)
- Enables benchmarking and comparison across different interpretable models
- Has already been adopted by follow-up work (CFM, AnyBottle)

### **4. Competitive Performance**

Demonstrates that interpretability doesn't require sacrificing accuracy:
- Maintains competitive ImageNet accuracy compared to black-box baselines
- Shows that B-cos + SAE design is not fundamentally limited by faithfulness constraints

---

## Methodology & Implementation

### **Architecture Design**

**FaCT Model Structure:**

```
Input → B-cos Layer 1 → SAE₁ → B-cos Layer 2 → SAE₂ → ... → B-cos Output Layer
                                                                    ↓
                                                            Output Logits
```

1. **B-cos Foundation:** All layers are B-cos transforms (instead of standard ReLU convolutions)
   - Each B-cos layer: `z = Σ cos(aⁱ, w) * x²ⁱ` for anchors aⁱ and learned weights w

2. **Sparse Autoencoder Insertion:** At intermediate layer activations:
   - Encoder: Maps high-dimensional activations → sparse concept vectors
   - Dictionary: Learned set of basis concepts
   - Decoder: Reconstructs approximations of activations
   - Sparsity constraint: L0 or L1 penalty to enforce few active concepts per input

3. **Faithfulness Mechanism:**
   - For each input x and concept c, compute `logit_contrib_c(x) = w_c · concept_c(x)`
   - By B-cos property: `Σ_c logit_contrib_c(x) = actual_logit(x)`
   - This ensures 100% attribution completeness

### **Experimental Setup**

**Architectures Tested:**
- DenseNet-121 (on CIFAR-10, CIFAR-100, ImageNet)
- Tested with variants: different SAE dictionary sizes, different layer depths

**Datasets:**
- **CIFAR-10:** 60,000 images, 10 classes (validation)
- **CIFAR-100:** 60,000 images, 100 classes (for broader concept testing)
- **ImageNet:** 1.3M images, 1,000 classes (primary evaluation)

**Baseline Comparisons:**
- B-cos networks (without SAEs): pixel-level explanations only
- Concept Bottleneck Models (CBMs): post-hoc concept alignment
- Standard CNNs: black-box baselines

### **Evaluation Metrics**

**1. Concept Consistency (C²-Score):**
- Computed on ImageNet validation set
- For each concept, sample top-10 images with highest activation
- Extract DINOv2 features and measure semantic clustering
- [Exact numerical results: see full paper for specific percentages and comparisons]

**2. Faithfulness Verification:**
- Measure reconstruction accuracy: How well do concept contributions sum to actual logit?
- Should be ~100% by design (verify against floating-point precision)
- [Exact figures unavailable — see full paper]

**3. User Study Evaluation:**
- **Setup:** 460 questions distributed to 10 randomized groups
- **Sample:** 100 late-layer and 100 early-layer concepts from FaCT (DenseNet-121)
- **Baselines:** 30 late-layer and 30 early-layer B-cos channel concepts (concept ablation)
- **Procedure:** Presented top-10 images for each concept (with and without pixel-level attributions)
- **Result:** Users rated FaCT concepts significantly more interpretable than B-cos-only baselines
- [Exact interpretability scores: see Appendix E of full paper]

**4. ImageNet Classification Accuracy:**
- [Accuracy figures unavailable — see full paper]
- Claim: Competitive with standard CNNs (no significant performance penalty)

**5. Computational Overhead:**
- Added cost from SAE encoding/decoding during inference
- Training time comparison with baselines
- [Exact overhead metrics: see implementation section of paper]

### **Implementation Details**

**Training Protocol:**
- Standard supervised learning on classification task
- SAEs trained jointly with main network (end-to-end)
- Sparse loss: `L_sparse = λ·Σ_layers ||concept_activations||_0` (or L1 approximation)

**Hyperparameters:**
- Sparsity coefficient λ: tuned per dataset
- SAE dictionary size: varies (tested 100-1000 concepts)
- Learning rate, batch size: standard practices for image classification

**Code Release:**
- Official implementation available in PyTorch
- Includes pre-trained models on ImageNet, CIFAR
- SAE training utilities and C²-Score evaluation code

---

## Practical Applications & Real-World Use Cases

### **1. Medical Imaging & Diagnosis**

**Scenario:** Computer-aided diagnosis for X-ray or MRI analysis

**Application of FaCT:**
- Radiologist can inspect which anatomical concepts (e.g., "lung nodule", "bone density", "cardiac silhouette") a model uses
- Faithful concept tracing ensures that highlighted concepts actually influence diagnosis recommendation
- Can adjust model behavior by steering concepts if biases are detected
- Enables trust-building with clinical teams before deployment

**Regulatory Alignment:** FDA guidance on AI/ML in medical devices increasingly requires transparency. FaCT provides objective, mathematically-verifiable explanations.

### **2. Autonomous Vehicles & Perception Systems**

**Scenario:** Pedestrian detection and scene understanding from camera feeds

**Application of FaCT:**
- Extract concepts like "pedestrian silhouette", "uniform texture", "standing posture"
- Verify that model doesn't rely on spurious correlations (e.g., clothing color)
- When adverse events occur, audit which concepts were active at decision time
- Test robustness: steer concept activations to see if predictions become unreliable

**Safety Benefit:** Enables post-incident analysis and improvement of corner cases

### **3. Content Moderation & Fairness Auditing**

**Scenario:** Image classification for inappropriate content detection

**Application of FaCT:**
- Identify demographic concepts the model learns (face features, clothing, etc.)
- Measure how much these demographics contribute to blocking decisions
- Separate harmful-content concepts from demographic-bias concepts
- Ensure fairness by controlling demographic concept weights

**Compliance:** Supports GDPR Article 22 (right to explanation) and EU AI Act transparency requirements

### **4. Quality Assurance in Manufacturing**

**Scenario:** Visual inspection for manufacturing defects

**Application of FaCT:**
- Learn interpretable concepts for different defect types
- Technicians can verify that the model looks at relevant features (cracks, discoloration) not spurious ones
- Retraining: when new defect types emerge, can leverage existing concepts
- Debugging: when model fails, concept traces pinpoint which decision path broke

### **5. Ecological & Environmental Monitoring**

**Scenario:** Species recognition in camera trap images or satellite imagery

**Application of FaCT:**
- Scientists verify that model concepts match known biological features (plumage, body shape, habitat structure)
- Builds confidence in automated ecosystem surveys
- Detects when model fails on under-represented species (by inspecting their concept activations)

---

## Insights & Implications

### **Broader Impact on Trustworthy AI**

1. **Shift from Post-Hoc to Inherent Interpretability:**
   - FaCT demonstrates that faithful interpretability can be built *into* architectures without major accuracy loss
   - Challenges the assumption that "interpretable models are less accurate"
   - Aligns with Cynthia Rudin's call for interpretable models over black-box + explanation combinations

2. **Concept Quality Matters:**
   - C²-Score shows that not all learned concepts are meaningful
   - Even "faithful" post-hoc explanations might involve low-quality concepts
   - Opens path to automatically ranking and selecting high-quality concepts

3. **Mechanistic Understanding at Scale:**
   - By tracing concepts through layers, FaCT enables studying how neural networks compose features
   - Related to mechanistic interpretability but at semantic (not circuit) level
   - Could accelerate alignment research (understanding what concepts large models learn)

### **Limitations & Open Questions**

1. **Scalability to Very Large Models:**
   - Tested on DenseNet and ImageNet-scale; unclear how SAEs scale to billion-parameter models
   - Sparse autoencoders have computational cost; efficiency on transformers uncertain

2. **Concept Interpretability ≠ Human Interpretability:**
   - C²-Score measures semantic consistency via DINOv2, but doesn't guarantee concepts are *understandable* to non-experts
   - User study was limited (460 questions, 10 groups); larger user studies needed

3. **Defining "Faithfulness":**
   - FaCT ensures attributions sum to logits (mathematical faithfulness)
   - But logical faithfulness (explanations reveal causal reasoning) is harder to verify
   - Could SAEs find "explanation-seeking" concepts rather than causal ones?

4. **Interaction with Different Datasets:**
   - Concepts learned on ImageNet may not transfer to domain-specific datasets (medical imaging, etc.)
   - Unclear whether C²-Score generalizes to non-visual domains

5. **Adversarial Robustness:**
   - Does faithful concept attribution resist adversarial perturbations?
   - If adversarial examples flip concept activations, are explanations still trustworthy?

### **Future Research Directions**

1. **Temporal Concept Analysis:** Extend to video to understand how concepts evolve across frames
2. **Multi-Modal Concepts:** Apply B-cos + SAE approach to vision-language models
3. **Interactive Concept Refinement:** Let users correct concept labels during inference, updating model behavior
4. **Certified Concept Robustness:** Combine with formal verification to guarantee concept stability under perturbations
5. **Cross-Domain Concept Transfer:** Pre-train SAEs on large datasets, transfer concepts to specialized tasks

---

## Code & Resources

### **Official Implementation**

- **Repository:** Released alongside paper at NeurIPS 2025 (link in paper)
- **Language:** PyTorch
- **Dependencies:** PyTorch ≥ 1.10, DINOv2 (for C²-Score evaluation), standard CV libraries

### **Pre-trained Models**

- DenseNet-121 on ImageNet (FaCT + SAE)
- DenseNet-121 on CIFAR-10 and CIFAR-100
- Baseline B-cos models for comparison

### **Quick Start Guide**

1. Clone repository and install dependencies
2. Load pre-trained model: `model = load_model('fact_densenet121_imagenet.pth')`
3. Forward pass produces: `(logits, concepts)` where concepts are sparse activation vectors
4. Visualize concepts: Use provided scripts to extract top-K images per concept
5. Evaluate C²-Score: `evaluate_c2_score(model, val_dataloader)`

### **Evaluation Tools**

- C²-Score computation on custom datasets
- User study template (for reproducibility)
- Concept visualization utilities
- Faithfulness verification tools

### **Additional Resources**

- **Paper:** [arXiv:2510.25512](https://arxiv.org/abs/2510.25512)
- **NeurIPS Proceedings:** Advances in Neural Information Processing Systems 38
- **Related Projects:** Links to mechanistic interpretability and sparse autoencoders literature
- **Discussion Forum:** NeurIPS forum for questions/clarifications

---

## Related Work & Context

### **Connection to Concept-Based Explainability**

**Concept Bottleneck Models (CBMs):**
- Traditional CBMs (e.g., Koh et al. 2020) extract concepts post-hoc or require human annotation
- FaCT improves on CBMs by ensuring concepts are *faithful to model decisions* and *automatically discovered*

**Prototype Networks:**
- Methods like ProtoPNet learn image regions as prototypes
- FaCT goes further: prototypes (concepts) are explainable at every layer, not just final classification

**TCAV (Testing with Concept Activation Vectors):**
- TCAV tests whether user-defined concepts influence predictions
- FaCT replaces user-defined concepts with *automatically discovered* faithful concepts

**LIME & SHAP:**
- Local, feature-level explanations
- FaCT operates at semantic (concept) level, providing higher-level explanations

### **Connection to Mechanistic Interpretability**

**Circuits & Feature Abstractions:**
- Mechanistic interpretability (e.g., Anthropic's work on circuits) studies how neural networks compose atomic features
- FaCT studies composition at the semantic/conceptual level
- The two approaches are complementary: FaCT concepts could be decomposed further into circuits

**Sparse Autoencoders (SAEs):**
- SAEs have become central to mechanistic interpretability for finding interpretable features in activations
- FaCT integrates SAEs into a training-time interpretable architecture (not just post-hoc feature discovery)

### **Related xAI Paradigms**

1. **Inherent Interpretability:** FaCT is an inherently interpretable model (like COFRNET, interpretable additive models)
2. **Feature Attribution:** FaCT provides faithful attribution at both pixel and concept levels
3. **Concept-Based Methods:** FaCT advances the state-of-the-art in automatically learning and evaluating concepts
4. **Fairness in ML:** Faithful concept understanding is essential for auditing and mitigating bias

### **Broader xAI Ecosystem**

- **Theoretical Foundations:** Builds on Doshi-Velez & Kim's framework of interpretability (model-agnostic vs. intrinsic)
- **Evaluation Standards:** Contributes to the emerging consensus on what makes explanations "good" (faithfulness, completeness, consistency)
- **Community Adoption:** C²-Score already used by CFM and AnyBottle, indicating growing ecosystem acceptance

---

## Summary: Why FaCT Matters for xAI

**The Core Insight:** Post-hoc explanations, while useful, can hide the true decision logic of neural networks. FaCT demonstrates that we can build neural networks whose explanations are faithful *by design*, not by post-processing.

**Key Achievements:**
1. First inherently interpretable model combining B-cos networks with sparse autoencoders
2. Introduces C²-Score, a foundation-model-based metric for evaluating concept quality
3. Demonstrates competitive accuracy without sacrificing interpretability
4. Provides user-study evidence that concepts are more interpretable than prior methods
5. Opens path to mechanistic understanding at the semantic level

**Potential to Transform:** Healthcare AI, autonomous systems, high-stakes decision-making, and fairness auditing through mathematically-verifiable, human-understandable explanations.
