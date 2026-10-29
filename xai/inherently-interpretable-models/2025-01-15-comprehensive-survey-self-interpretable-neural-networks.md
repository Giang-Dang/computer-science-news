# A Comprehensive Survey on Self-Interpretable Neural Networks

**ArXiv ID:** [2501.15638](https://arxiv.org/abs/2501.15638)

**Authors:** Yang Ji, Ying Sun, Hui Xiong, and 8 co-authors

**Submission Date:** January 2025 (revised March 2025)

**Venue:** Proceedings of the IEEE, Vol. 113, Issue 8, Pages 783-813, 2025  
**DOI:** 10.1109/JPROC.2025.3635153

---

## Executive Summary

This comprehensive survey examines **self-interpretable neural networks (SINNs)**—models designed to be inherently interpretable rather than requiring post-hoc explanations. As black-box deep learning models dominate critical applications (healthcare, autonomous driving, finance), the fragility of post-hoc explanation methods has spurred renewed interest in neural architectures that expose their reasoning through their structural design. This survey provides a systematic taxonomy of five major families of self-interpretable approaches, discusses their applications across diverse domains, and identifies open challenges for future research in building trustworthy, transparent AI systems.

---

## Problem Statement

### The Interpretability Crisis in Deep Learning

Traditional post-hoc interpretability methods—such as LIME, SHAP, and attention visualization—attempt to explain decisions made by pre-trained neural networks. However, these approaches face fundamental limitations:

1. **Robustness and Fidelity Issues:** Post-hoc explanations often lack robustness to small input perturbations and may fail to faithfully represent the model's true decision-making process. For example, saliency maps can be sensitive to different random seeds or model initializations.

2. **Inherent Contradiction:** Post-hoc methods analyze models after training, potentially introducing artifacts or explanations that don't reflect the actual mechanisms learned by the network.

3. **Stakeholder Requirements:** Mission-critical domains (healthcare, law, finance) increasingly require not just *why* a model made a decision, but confidence that the explanation mechanism itself is sound and verifiable.

4. **Regulatory Pressure:** The EU AI Act, FDA guidance on AI in medical devices, and other regulations mandate explainability for high-risk AI systems, creating pressure for built-in interpretability rather than retrofit explanations.

### The Self-Interpretable Alternative

Self-interpretable neural networks (SINNs) address these challenges by designing models where interpretability is **built into the architecture from the ground up**. Rather than explaining a black box, SINNs make the model itself white (or gray) box—the model's structure and parameters directly encode interpretable concepts or patterns.

---

## Core Concepts & Theory

### What Are Self-Interpretable Neural Networks?

SINNs are neural network architectures where:
- **Model structure encodes interpretability:** The architecture itself constrains what the model can learn and how it makes decisions, forcing interpretable representations.
- **Predictions follow interpretable pathways:** The computations from input to output can be traced through human-understandable concepts, rules, prototypes, or attribution mechanisms.
- **Explanations are intrinsic:** Rather than probing the model post-hoc, the explanation is an inherent byproduct of the forward pass.

**Key distinction:** If a standard neural network is a black box that we try to interpret afterward, a SINN is designed so that the box itself is transparent.

### Fundamental Principles

1. **Structural Constraints:** SINNs impose architectural constraints that limit model expressiveness but increase interpretability. This creates a trade-off between accuracy and interpretability.

2. **Concept Externalization:** Many SINNs explicitly extract or enforce the use of human-understandable **concepts** as intermediate representations, rather than learning opaque distributed embeddings.

3. **Decision Path Transparency:** The model's decision can be traced back through a sequence of interpretable steps (e.g., feature importance scores, concept activations, prototype matching, rule firings).

4. **Model-Agnostic vs. Architecture-Specific:** Some SINN approaches are model-agnostic (can be applied to any architecture), while others require custom architectures designed from scratch.

---

## Taxonomy of Self-Interpretable Methods

The survey organizes self-interpretable neural networks into **five major families**, each with distinct mechanisms for achieving interpretability:

### 1. **Attribution-Based Methods**

**Concept:** Model outputs are decomposed as a sum (or other aggregate) of feature attributions, where each attribution score represents the contribution of a specific input feature to the final prediction.

**Key Idea:** If a model's prediction can be expressed as:
```
Output = f(x) = bias + Σ(attribution_i * feature_i)
```

Then the model becomes interpretable by inspecting the attribution scores.

**Example Techniques:**
- **Integrated Gradients:** Attributes predictions to input features by integrating gradients along a straight-line path from a baseline to the input.
- **Layer-wise Relevance Propagation (LRP):** Decomposes a network's prediction by propagating relevance scores backward through layers.
- **DeepLIFT:** Explains predictions by comparing activations to reference activations at each neuron.

**Advantages:**
- Provides per-feature importance scores
- Can apply to any differentiable model
- Computationally tractable

**Limitations:**
- Still operates on learned embeddings; may not be intuitive
- Attribution scores depend heavily on the baseline or reference point chosen
- Can suffer from gradient saturation in deep networks

---

### 2. **Function-Based Methods**

**Concept:** The model learns to decompose its decision function into a sum of interpretable basis functions, where each function has a clear semantic meaning.

**Key Idea:** If a model's output can be expressed as:
```
Output = f(x) = Σ(g_i(x_i))
```

where each function g_i is interpretable (e.g., monotonic, smooth, or visually simple), then the model is inherently interpretable.

**Example Techniques:**
- **Generalized Additive Models (GAMs):** Learn additive functions where f(x) = c + Σ(g_i(x_i)). Each g_i is a learned univariate function (spline) showing the effect of feature x_i on the output.
- **Neural Additive Models (NAM):** Use small neural networks as the basis functions g_i, allowing more expressiveness than traditional GAMs while maintaining additivity.
- **Kolmogorov-Arnold Networks (KAN):** Parameterize the Kolmogorov-Arnold representation using learnable spline functions, achieving both interpretability and expressiveness.

**Advantages:**
- Entire decision logic can be visualized
- Maintains human-interpretable function composition
- Theoretically grounded (based on Kolmogorov-Arnold theorem for KAN)

**Limitations:**
- Restrictive assumption of additivity; some phenomena are inherently non-additive
- May sacrifice accuracy on complex tasks
- Requires careful design of basis functions

---

### 3. **Concept-Based Methods**

**Concept:** Models learn or use explicit high-level **concepts** (rather than raw features) as intermediate representations. Decisions are made by combining activations over these concepts.

**Key Idea:** Rather than learning arbitrary embeddings, the model learns representations for human-defined concepts (e.g., "has whiskers," "is furry," "is striped" for a cat classifier), and the final prediction is based on these concept activations:
```
Output = decoder(concept_activations)
```

**Example Techniques:**
- **Concept Bottleneck Models (CBMs):** Use a bottleneck layer containing explicit concept activations. The model first predicts concept labels from the image, then predicts the final label from concepts.
- **Testing with Concept Activation Vectors (TCAV):** Uses concept vectors in embedding space to measure the importance of user-defined concepts to model predictions.
- **Concept Activation Vectors for neural networks (CAVs):** Learns directions in the network's activation space that correspond to human-understandable concepts.

**Advantages:**
- Enables user-in-the-loop interpretability; humans can modify concept definitions
- Allows for human-guided model debugging and debiasing
- Interpretations align with human reasoning

**Limitations:**
- Requires human annotation of concepts
- Bottleneck design limits information flow, which can reduce accuracy
- Concept definitions may be subjective or domain-specific

---

### 4. **Prototype-Based Methods**

**Concept:** The model makes predictions by comparing inputs to learned **prototypes** (representative examples) from the training data. A prediction is made by finding the nearest or most similar prototypes.

**Key Idea:** Interpretability comes from showing which training examples ("prototypes") the model used to make its decision:
```
Output = classify_based_on(similarity_to_prototypes)
```

**Example Techniques:**
- **Case-Based Reasoning (CBR):** Store representative training examples and make predictions based on similarity to cases.
- **Prototype Networks:** Learn a embedding space where prototypes are clustered, and new inputs are classified based on proximity to these prototypes.
- **ProtoPNet (Prototypical Part Network):** Identifies which parts of an image are similar to learned prototypes, providing visual explanations.

**Advantages:**
- Explanations are concrete (show actual or learned examples)
- Easy for humans to understand ("this input is similar to that training example")
- Can incorporate domain knowledge into prototypes

**Limitations:**
- May require storing or computing similarity to many prototypes (scalability)
- Prototype selection and learning can be challenging
- Not all decisions can be well-represented by similarity to exemplars

---

### 5. **Rule-Based Methods**

**Concept:** The model learns explicit **rules** (e.g., "If feature A > threshold AND feature B < threshold, then predict Y") that govern its predictions.

**Key Idea:** Decisions are made by firing interpretable rules:
```
if (condition_1 AND condition_2 AND ... ) then predict Y with confidence Z
```

**Example Techniques:**
- **Decision Trees and Tree Ensembles:** Learned decision paths are inherently interpretable as rules.
- **Symbolic Reasoning Models:** Learn rule sets that explain predictions, often using reinforcement learning or evolutionary algorithms.
- **Neural Symbolic Integration:** Combine neural networks with symbolic rule systems for interpretability.
- **Attention-Based Rule Learning:** Use attention mechanisms to learn which rules (or rule components) are most relevant.

**Advantages:**
- Rules are naturally expressible in human language
- Easy to audit and verify
- Can incorporate domain knowledge as rule constraints

**Limitations:**
- Rule complexity can explode for high-dimensional data
- Learning accurate rules is NP-hard in general
- Rules may be brittle to distribution shift

---

## Main Ideas & Key Contributions

### 1. **Systematic Taxonomy for SINNs**

The survey's primary contribution is organizing the fragmented literature on self-interpretable models into a unified taxonomy. Rather than treating "interpretable ML" as a monolithic category, the paper clarifies that different architectures achieve interpretability through fundamentally different mechanisms:

- **Attribution-based:** Decompose predictions into feature contributions
- **Function-based:** Use additive or decomposable functions
- **Concept-based:** Explicitly represent high-level concepts
- **Prototype-based:** Leverage similarity to examples
- **Rule-based:** Extract symbolic decision rules

This taxonomy helps researchers understand trade-offs and choose appropriate methods for their applications.

### 2. **Motivation: The Robustness Problem with Post-Hoc Methods**

The survey emphasizes a critical issue: post-hoc explanation methods (LIME, SHAP) can be brittle and unreliable. The paper argues that self-interpretable models address this by embedding interpretability into the architecture, making explanations an inherent property rather than a retrofit.

### 3. **Cross-Domain Applicability**

Unlike interpretability surveys focused on a single domain, this work demonstrates that self-interpretable principles apply across:
- **Computer Vision:** Image classification, object detection, medical imaging
- **Natural Language Processing:** Text classification, machine translation, question answering
- **Graph Neural Networks:** Node classification, link prediction
- **Reinforcement Learning:** Policy interpretability, value function visualization

### 4. **Evaluation Metrics for Self-Interpretability**

The survey catalogs metrics for evaluating whether a model is truly interpretable:
- **Fidelity:** Do the interpretable components actually explain the model's behavior?
- **Sparsity:** Are explanations concise and minimal?
- **Stability:** Are explanations consistent across similar inputs?
- **Human Alignment:** Do explanations match human reasoning?
- **Completeness:** Do interpretations account for the full decision?

---

## Methodology & Implementation

### Scope and Organization

**Data Collection:** The authors conducted a comprehensive literature review, curating papers from:
- Major ML conferences (NeurIPS, ICML, ICLR, IJCAI, KDD)
- Journal publications in top venues
- ArXiv preprints on interpretability

**Taxonomy Construction:** Methods were grouped based on their core mechanism for achieving interpretability, with emphasis on:
- Architectural design choices
- Whether interpretability is enforced vs. learned
- Scalability and practical feasibility

### Evaluation Framework

The survey evaluates each family of methods along multiple dimensions:

| Dimension | Attribution | Function | Concept | Prototype | Rule |
|-----------|-------------|----------|---------|-----------|------|
| **Accuracy-Interpretability Trade-off** | Moderate | High (depends on function class) | Moderate-High | Moderate | High |
| **Scalability** | Good | Moderate | Moderate | Challenging | Challenging |
| **Human Interpretability** | Moderate | High | High | Very High | Very High |
| **Theoretical Grounding** | Strong | Strong | Moderate | Moderate | Strong |
| **Handling Non-Additivity** | Good | Poor | Good | Moderate | Good |

### Applications and Domains

**Computer Vision Applications:**
- Medical image classification (interpretability critical for clinical adoption)
- Self-driving car perception systems
- Facial recognition (with bias mitigation)

**NLP Applications:**
- Sentiment analysis with concept-based explanations
- Machine translation with interpretable alignment
- Clinical note analysis for healthcare

**Graph Neural Networks:**
- Node classification with prototype learning
- Knowledge graph reasoning with rule extraction

**Reinforcement Learning:**
- Policy interpretability for autonomous agents
- Value function decomposition

### Results and Performance Metrics

[Exact figures unavailable — see full paper]

The survey includes comparative analyses showing:
- Accuracy vs. interpretability trade-offs across different SINN families
- Computational efficiency comparisons
- Benchmark results on standard datasets (ImageNet, MNIST, text classification benchmarks)
- Human evaluation studies measuring interpretability

**Key Finding:** Self-interpretable models can achieve competitive accuracy with black-box models on many tasks, though with notable exceptions in complex domains.

---

## Practical Applications & Real-World Use Cases

### 1. **Healthcare and Medical Diagnosis**

**Challenge:** Hospitals require interpretable models for diagnostic support systems. A neural network that achieves 95% accuracy is useless if doctors cannot trust or understand its reasoning.

**SINN Application:**
- Concept-based models in medical imaging: A model learns to predict diagnoses based on explicit radiological concepts (e.g., "presence of nodule," "air bronchogram," "pleural effusion") rather than abstract features.
- Benefit: Radiologists can verify whether the model is reasoning about the right clinical features.
- Impact: Increased clinical trust, easier regulatory approval (FDA considerations), ability to catch model errors that don't align with medical knowledge.

**Example:** A concept bottleneck model for lung disease classification learns that certain diseases require activation of specific concepts. If a prediction relies on a concept that clinicians know is irrelevant, the error can be caught and corrected.

### 2. **Financial Decision-Making**

**Challenge:** Loan approval systems, credit scoring, and trading algorithms must be explainable under financial regulations (e.g., Fair Lending Laws, Dodd-Frank Act).

**SINN Application:**
- Function-based (GAM/NAM) models for credit scoring: Each input feature (income, debt-to-income ratio, credit history) has a learned function showing its nonlinear contribution to the final score.
- Benefit: Regulators and applicants can understand exactly how each variable affects the decision.
- Impact: Improved compliance, ability to demonstrate fairness (e.g., gender-blind credit decisions).

### 3. **Autonomous Vehicles and Safety-Critical Systems**

**Challenge:** In autonomous driving, black-box decisions about steering, braking, and path planning are unacceptable. Regulators and insurers demand interpretability.

**SINN Application:**
- Rule-based and prototype-based models for perception and planning: The model can explain its decisions in terms of detected objects, traffic rules, and learned driving scenarios.
- Benefit: Enables safety verification and debugging of corner cases.
- Impact: Faster certification, better incident analysis, improved public trust.

### 4. **Criminal Justice and Recidivism Prediction**

**Challenge:** Algorithms used to assess bail, sentencing, and parole recommendations have been shown to embed racial bias. Interpretability is essential for fairness auditing.

**SINN Application:**
- Concept-based and rule-based models for risk assessment: Decisions are based on explicit, auditable concepts (criminal history, employment status, ties to community) rather than opaque learned patterns.
- Benefit: Makes it easier to detect and remove biased decision rules.
- Impact: More equitable criminal justice outcomes, reduced algorithmic bias.

### 5. **Environmental Science and Climate Modeling**

**Challenge:** Understanding which variables drive climate models' predictions is crucial for policy-making.

**SINN Application:**
- Function-based models (e.g., KAN) for climate prediction: Each input variable (CO₂ concentration, sea surface temperature, solar radiation) has a learned function showing its contribution to future climate.
- Benefit: Scientists can validate whether the model learned physically plausible relationships.
- Impact: Improved confidence in model predictions, better alignment with domain knowledge.

### Regulatory & Compliance Implications

- **EU AI Act:** Mandates "explainability" for high-risk AI systems (Articles 13-15). Self-interpretable models naturally satisfy this requirement.
- **FDA Guidance:** Medical device software increasingly requires interpretable algorithms. The FDA's 2023 guidance encourages transparent, verifiable ML.
- **Fair Lending Regulations:** Financial institutions must explain adverse decisions to applicants. Interpretable models simplify compliance.
- **GDPR Right to Explanation:** EU citizens have a right to explanations of automated decisions. SINNs provide built-in explanations.

### Implementation Challenges

1. **Accuracy Trade-offs:** For some complex tasks, interpretable models significantly underperform black-box models. Practitioners must weigh accuracy against interpretability.

2. **Concept Annotation Cost:** Concept-based methods require human experts to define and annotate concepts, which is expensive and may be subjective.

3. **Scalability:** Prototype-based and rule-based methods scale poorly to high-dimensional data or large training sets.

4. **Domain Specificity:** Self-interpretable architectures are often designed for specific domains and may not transfer well across tasks.

---

## Insights & Implications

### 1. **Paradigm Shift: From Post-Hoc to Built-In Interpretability**

The survey documents a fundamental shift in how the community thinks about interpretability:
- **Old paradigm:** Train a black-box model, then develop post-hoc methods to explain it.
- **New paradigm:** Design architectures where interpretability is built-in from the start.

This shift reflects growing awareness that post-hoc explanations, while useful, cannot fully overcome the fundamental challenges of explaining opaque models.

### 2. **Trade-offs Are Unavoidable**

The survey highlights that **there is no free lunch** in interpretable ML:
- Models that are more interpretable often sacrifice accuracy
- Highly expressive models (like deep neural networks) tend to be less interpretable
- The choice of interpretation method (attribution vs. concept vs. rule) reflects different value judgments about what "interpretable" means

**Implication:** Practitioners must explicitly choose what matters most for their application (accuracy, interpretability, fairness, speed) and design accordingly.

### 3. **Interpretability Requires Multidisciplinary Collaboration**

Developing effective self-interpretable models requires input from:
- **ML researchers:** Designing architectures and learning algorithms
- **Domain experts:** Defining concepts, validating rules, ensuring domain alignment
- **Human factors researchers:** Evaluating whether explanations actually improve human understanding
- **Ethicists and policymakers:** Ensuring that interpretability serves justice and transparency goals

**Implication:** Interpretability research increasingly sits at the intersection of ML, HCI, cognitive science, and ethics.

### 4. **Evaluation of Interpretability Remains Unsolved**

While the survey catalogs metrics for evaluating interpretability (fidelity, sparsity, stability), a fundamental challenge remains: **How do we measure whether an explanation is truly useful to humans?**

Recent work shows that metrics like fidelity don't always correlate with human understanding. More research is needed on human-centered evaluation of interpretability.

### 5. **Self-Interpretable Models Are Not a Panacea**

The survey makes clear that SINNs are not always the right choice:
- For vision tasks with enormous feature complexity (ImageNet), self-interpretable models may sacrifice too much accuracy
- For tasks where accuracy is paramount and interpretability secondary, black-box models may be more appropriate
- For emerging domains where no interpretable architecture has been developed, post-hoc methods remain necessary

**Implication:** The future of trustworthy AI likely involves a mix of interpretable models (for high-stakes decisions), explainable models (combining interpretable components with learned modules), and carefully audited black-box models where appropriate.

---

## Limitations and Open Questions

### Limitations of Current Approaches

1. **Limited Expressiveness:** Each SINN family sacrifices some model expressiveness for interpretability. Achieving both remains an open problem.

2. **Domain-Specific Designs:** Most self-interpretable approaches are tailored to specific domains (vision, NLP, tabular) and don't transfer across domains.

3. **Human Validation:** Few SINN papers include rigorous human studies validating whether explanations actually improve user understanding and decision-making.

4. **Scalability:** As models grow larger and datasets grow richer, maintaining interpretability while scaling becomes increasingly challenging.

### Future Research Directions

1. **Hybrid Approaches:** Combining interpretable and opaque components in complementary ways (e.g., interpretable feature extraction followed by black-box decision-making).

2. **Automated Concept Discovery:** Developing methods to automatically discover human-aligned concepts without manual annotation.

3. **Adversarial Robustness of Explanations:** Ensuring that explanations are robust to adversarial perturbations—they should not be "gamed" to provide false justifications.

4. **Continuous Interpretability:** Moving beyond discrete concepts/rules to continuous notions of interpretability that better capture nuanced decision-making.

5. **Theory of Interpretability:** Developing formal frameworks for defining and measuring interpretability, grounded in information theory and cognitive science.

---

## Code & Resources

### Official Implementation & GitHub Resources

- **Authors' Awesome List:** [yangji721/Awesome-Self-Interpretable-Neural-Network](https://github.com/yangji721/Awesome-Self-Interpretable-Neural-Network)
  - Curated collection of papers, code, and datasets for self-interpretable neural networks
  - Organized by method family and application domain
  - Actively maintained with new papers added regularly

### Key Implementation Libraries

- **PyTorch GAM/NAM:** [ExplainableML/pytorch-gam](https://github.com/ExplainableML/pytorch-gam) - Reference implementations of Generalized Additive Models and Neural Additive Models
- **Concept Bottleneck Models:** Multiple implementations available on GitHub for CBMs in vision and NLP
- **Interpretable ML Library:** [interpretml/interpret](https://github.com/interpretml/interpret) - Unified API for interpretable models (GAMs, decision trees, rule sets)
- **SHAP Library (for concept-based):** [shap/shap](https://github.com/shap/shap) - Also includes kernel SHAP for global concepts

### Computational Requirements

- **Training:** Depends on model family; self-interpretable models are generally less computationally expensive than deep networks
- **Inference:** Similarly efficient to standard neural networks (no overhead for generating explanations)
- **GPU:** Not strictly necessary for most self-interpretable approaches, though beneficial for large-scale concept-based models

### Quick Start Guide

1. **For Vision Tasks:** Start with Concept Bottleneck Models (CBM) using pre-trained image encoders (ResNet, ViT)
2. **For Tabular Data:** Use Generalized Additive Models (GAMs) or Neural Additive Models (NAM) for immediate interpretability
3. **For NLP:** Implement concept-based attention mechanisms or rule-based classifiers on top of pre-trained embeddings
4. **For Critical Applications:** Consider hybrid approaches combining self-interpretable components with selective use of black-box modules

---

## Related Work & Context

### Relationship to Other Interpretability Research

**Self-Interpretable vs. Post-Hoc Methods:**
- Post-hoc methods (LIME, SHAP, attention visualization) explain already-trained models
- Self-interpretable methods design interpretability into the model architecture
- **Key difference:** SINNs provide guarantees about interpretability; post-hoc methods are approximations

**Self-Interpretable vs. Intrinsically Interpretable:**
- "Intrinsically interpretable models" often refers to simple, limited-capacity models (linear models, shallow decision trees)
- "Self-interpretable" is broader: includes complex, high-capacity models that decompose their decisions into understandable components

**Connection to Mechanistic Interpretability:**
- Mechanistic interpretability aims to understand internal mechanisms of neural networks (circuits, attention heads, neurons)
- Self-interpretability designs models so mechanisms are human-understandable from the start
- Overlap: Both seek to understand how models make decisions

**Connection to Fairness & Robustness:**
- Interpretability often enabler of fairness (can detect and remove biased rules)
- Some self-interpretable models inherently more robust (e.g., rule-based models less vulnerable to adversarial examples than deep networks)

### Broader XAI Communities and Related Work

**Key Related Concepts:**
- **Concept Activation Vectors (CAVs):** Foundational work on human-defined concepts in neural networks
- **LIME (Local Interpretable Model-Agnostic Explanations):** Post-hoc method that learns local rule approximations
- **SHAP:** Game-theoretic approach to attribution; also used in concept-based settings
- **Attention Mechanisms:** Often treated as explanations, though recent work questions their reliability
- **Saliency Maps and Grad-CAM:** Visual explanation methods for deep networks

### Evolution of Thinking in XAI

1. **Early Days (2010s):** Focus on saliency maps and attention as explanations
2. **Post-Hoc Era (2016-2020):** Development of model-agnostic methods (LIME, SHAP) to explain black-box models
3. **Interpretability-by-Design Era (2020-present):** Growing recognition that post-hoc methods are fundamentally limited; shift toward architectures with built-in interpretability

This survey sits at the forefront of this transition, comprehensively documenting the emerging landscape of self-interpretable approaches.

---

## Discussion & Author Positioning

The authors position self-interpretable neural networks as a necessary evolution beyond both "simple but limited" interpretable models and "powerful but opaque" black-box models:

> "Post-hoc interpretability methods, while useful for initial model inspection, cannot overcome the fundamental problem that explanations are generated after the fact and may not accurately reflect model behavior. Self-interpretable architectures, by contrast, ensure that interpretability is woven into the fabric of model design. The challenge ahead is not whether we should build interpretable models, but which design choices best balance accuracy, interpretability, and computational efficiency for each domain." 
> 
> — Implied position of the survey

---

## Conclusion

**"A Comprehensive Survey on Self-Interpretable Neural Networks"** provides the most comprehensive taxonomy to date of methods for building neural networks that are interpretable by design. As regulatory requirements for AI explainability grow and applications in high-stakes domains expand, understanding different approaches to self-interpretable design becomes essential for both researchers and practitioners.

The survey's five-family taxonomy (attribution-based, function-based, concept-based, prototype-based, rule-based) offers a clear organizing principle for thinking about interpretability trade-offs and helps practitioners choose appropriate methods for their applications. By documenting the strengths, limitations, and application contexts of each approach, the paper makes a significant contribution to the emerging field of human-centered, trustworthy AI.

---

## Metadata

- **Paper URL:** https://arxiv.org/abs/2501.15638
- **PDF:** https://arxiv.org/pdf/2501.15638
- **HTML Version:** https://arxiv.org/html/2501.15638v2
- **GitHub Resource:** https://github.com/yangji721/Awesome-Self-Interpretable-Neural-Network
- **Published Venue:** Proceedings of the IEEE, Vol. 113, Issue 8, Pages 783-813, 2025
- **DOI:** 10.1109/JPROC.2025.3635153

