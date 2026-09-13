# From Interpretability Methods to Interpretable Models

**Authors:** Julien Colin, Nuria Oliver, Thomas Serre  
**ArXiv ID:** 2609.05399  
**Submitted:** September 4, 2026  
**Categories:** Computer Vision and Pattern Recognition (cs.CV), Human-Computer Interaction (cs.HC)

## Executive Summary

This paper addresses a critical gap in explainable AI (xAI) research: while the field has developed a mature toolkit of interpretability methods (attribution, feature visualization, concept-based, circuit-based approaches), the focus has remained on building and comparing these methods rather than on the core question of whether our models are actually interpretable to humans. The authors argue for a fundamental shift in the field's focus—from developing interpretability methods to evaluating and improving model interpretability through human-centered evaluation frameworks.

## Problem Statement

The current state of explainable AI in computer vision presents a paradox: despite decades of research and a rich toolbox of interpretability techniques, there is limited systematic evaluation of whether models are actually interpretable to the humans who rely on them. Key challenges include:

1. **Method-Centric Focus**: The field has invested substantial effort in building and comparing interpretability methods (LIME, SHAP, saliency maps, attention mechanisms) but lacks rigorous evaluation of their actual impact on human understanding.

2. **Lack of Human-Centered Metrics**: Most interpretability research uses computational metrics that may not align with whether humans can actually understand what models learn and how they make decisions.

3. **Undefined "Interpretability"**: Without clear, measurable definitions of interpretability from a human perspective, it's difficult to assess progress or design models to be more interpretable.

4. **Foundation Model Paradox**: Recent findings suggest that foundation models may actually be *less* interpretable than supervised models, despite their superior performance on downstream tasks—a critical gap in understanding trade-offs between capability and interpretability.

5. **No Standardized Evaluation**: There is no agreed-upon benchmark or protocol for comparing the interpretability of different models and architectures.

## Core Concepts & Theory

### Psychophysics-Based Interpretability Framework

The paper proposes that interpretability should be measured through human-centered evaluation protocols inspired by psychophysics—classical methods for quantifying human perception and judgment. Two complementary dimensions are defined:

#### 1. Localizability
**Definition:** Can a human observer predict where a learned feature fires (activates) on a novel image after seeing examples of feature activations?

**Intuition:** This measures whether features correspond to spatially coherent, localized patterns in visual space—a prerequisite for human understanding. If a feature fires randomly across an image, it's harder to interpret.

**Implementation:** 
- Extract features via sparse autoencoders (a method for discovering interpretable features in neural networks)
- Show observers examples of images where the feature activates strongly
- Test whether they can accurately predict feature activation on new images
- Compute a chance-anchored scoring function (normalized 0-1 scale)

#### 2. Nameability
**Definition:** Can a human observer accurately describe what a learned feature represents after seeing examples of its activations?

**Intuition:** Interpretability requires not just spatial coherence but semantic meaning. A feature that activates on "furry textures" is more interpretable if humans can describe it that way consistently.

**Implementation:**
- Show observers visualizations of feature activations
- Ask them to write descriptions of what the feature represents
- Evaluate whether independent observers agree on the feature's semantic meaning
- Measure inter-observer agreement and semantic consistency

### Sparse Autoencoders for Feature Discovery

The framework relies on **sparse autoencoders** (SAEs), a technique for extracting interpretable features from neural network hidden activations:

- **Standard autoencoder**: Encodes and decodes information through a bottleneck, learning compressed representations
- **Sparse component**: Adds regularization to encourage learned features to be sparse (most features inactive at any time), reducing feature polysemy
- **Benefit**: Unlike individual neurons (which often represent multiple concepts), sparse features tend to align with human-understandable concepts

### Chance-Anchored Scoring

To compare interpretability across different models fairly:
- Define a baseline chance performance level (e.g., random guessing)
- Normalize all scores relative to this baseline (0-1 scale)
- Allows models with different output dimensions and training methods to be compared on a common scale
- Accounts for task difficulty variations

## Main Ideas & Key Contributions

### 1. Paradigm Shift: Methods → Models

**Core Argument:** The field has over-invested in building interpretability methods while under-investing in evaluating whether these methods actually help humans understand models.

**Implication:** Rather than continuing to develop new attribution methods or attention mechanisms, researchers should focus on measuring and improving model interpretability directly, and designing models to be inherently more interpretable.

### 2. Two Complementary Approaches to Model Interpretability

The paper proposes two research directions:

**Approach A: Characterize Model Representations**
- Use existing interpretability tools to understand what different models learn and represent
- Compare representations across architectures, training methods, and model families
- Identify which design choices improve representation interpretability

**Approach B: Measure Human-Interpretable Representations**
- Evaluate whether humans can actually understand model features and predictions
- This requires human evaluation and psychophysics-based protocols
- Often neglected in the literature, but arguably more important

### 3. Psychophysics Provides Scientific Framework

**Innovation:** Applying psychophysics methods from psychology/neuroscience to systematically measure human interpretability:
- **Localizability** and **nameability** are concrete, measurable dimensions
- Chance-anchored scoring provides fair cross-model comparison
- Framework is reproducible and testable
- Grounded in how humans actually perceive and categorize visual information

### 4. Empirical Finding: Capability ≠ Interpretability

Early results from related work (Colin et al., 2026 - "Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models"):

**Key Findings:**
- Foundation models (CLIP, DINOv2, etc.) are **consistently less interpretable** than supervised models despite better performance on downstream tasks
- Interpretability is an **independent, measurable dimension** of representation quality
- Interpretability can be **predicted by**:
  - Feature activation **locality** (spatial coherence of feature activations)
  - **Semantic alignment** with human concepts (coarse-grained alignment, not fine-grained details)
- This suggests: improved capability through scaling/foundation models may come at the cost of interpretability

### 5. Sparse Autoencoders as Feature Extraction Method

**Why SAEs Matter:**
- Extract features that align better with human concepts than raw neurons
- Reduce polysemy (one neuron = multiple concepts) and synonymy (one concept = multiple neurons)
- Scale to large models and high-dimensional layers
- Provide a principled alternative to attention-based or gradient-based attribution methods

## Methodology & Implementation

### Experimental Framework

**Phase 1: Feature Discovery**
1. **Data Collection:** Choose a trained neural network (CNN, vision transformer, foundation model)
2. **SAE Training:** Train sparse autoencoders on the activations of target layers
3. **Feature Extraction:** Recover interpretable features (sparse, disentangled dimensions)
4. **Feature Visualization:** Generate or select image patches that maximally activate each feature

**Phase 2: Human Evaluation**

**Localizability Protocol:**
1. Show human observers 10-15 exemplar images where a feature strongly activates
2. Highlight the regions of activation (using attention maps or gradients)
3. Show novel test images and ask: "Where does this feature activate on this new image?"
4. Measure prediction accuracy on held-out test set
5. Normalize score: (Accuracy - Chance) / (Max Possible - Chance)

**Nameability Protocol:**
1. Show human observers a subset of images with strong feature activations
2. Ask: "What does this feature represent? Please write a description in 1-2 sentences."
3. Collect descriptions from multiple observers (typical: 3-5 per feature)
4. Measure inter-observer agreement:
   - Exact match: Do observers write nearly identical descriptions?
   - Semantic agreement: Do descriptions capture the same semantic concept?
5. Compute consistency score based on agreement level

### Datasets & Models

**Models Tested** [Exact figures unavailable — see full paper]:
- Standard CNNs (ResNet, EfficientNet)
- Vision Transformers (ViT)
- Foundation models (CLIP, DINOv2, BLIP)
- Self-supervised models (SimCLR, MoCo)

**Metrics:**
- Localizability score (0-1): Human ability to predict where features fire
- Nameability score (0-1): Human agreement on feature semantic meaning
- Inter-observer agreement: Fleiss' kappa or Krippendorff's alpha
- Composite interpretability: Weighted combination of localizability and nameability

### Evaluation Results

**Key Findings** [Exact figures unavailable — see full paper]:

1. **Foundation Models Are Less Interpretable:**
   - Models like CLIP and DINOv2 achieve high downstream task performance
   - Yet their learned features are harder for humans to localize and name
   - Suggests: scaling and self-supervised objectives may optimize for capability at the expense of interpretability

2. **Feature Locality Predicts Interpretability:**
   - Models with spatially coherent features (high locality) have better human interpretability
   - Simple architectural metrics (e.g., average activation density) correlate with interpretability
   - Implication: Can design models for interpretability by encouraging locality

3. **Supervised Models More Interpretable:**
   - Models trained on supervised objectives (ImageNet classification) produce more interpretable features
   - Self-supervised models achieve better zero-shot performance but lower interpretability
   - Trade-off can be quantified: interpretability scores vs. downstream task performance

4. **Semantic Alignment Matters:**
   - Features that align with human-recognizable concepts (e.g., "dog faces," "wheels") are more interpretable
   - High-level layers show better semantic alignment than low-level layers
   - Coarse-grained alignment (broad category recognition) is more robust than fine-grained details

### Limitations of the Approach

1. **Human Evaluation Costs**: Psychophysics protocols require recruiting and compensating human observers; expensive to scale to many models and layers

2. **Context Dependency**: Interpretability may vary by task and application domain; evaluated on image classification, may not generalize to other domains (NLP, RL, medical imaging)

3. **Feature Extraction Choice**: Results depend on feature extraction method (sparse autoencoders chosen here); different methods may yield different interpretability measurements

4. **Task-Specificity**: Interpretability for classification may not predict interpretability for other visual reasoning tasks (object detection, scene understanding)

5. **Sparse Autoencoder Training**: SAE training is itself a complex process requiring careful hyperparameter tuning; instability could affect feature discovery

## Practical Applications & Real-World Use Cases

### Critical Applications for Model Interpretability

#### 1. **Medical Imaging & Healthcare**
- **Challenge**: Regulatory bodies (FDA) require explainability for clinical decision support systems
- **Application**: Radiologists need to understand *why* a model flagged a potential tumor
- **Interpretability Method**: Localizability ensures radiologists can verify that the model attends to the correct anatomical region; nameability ensures they understand what visual pattern the model learned
- **Benefit**: Builds clinician trust; supports clinical validation; helps detect dataset biases

#### 2. **Autonomous Systems & Robotics**
- **Challenge**: Safety-critical decisions must be auditable and understandable
- **Application**: Autonomous vehicle perception systems, industrial robots making real-time decisions
- **Interpretability Method**: Human interpretability testing reveals whether models learn robust, semantic features or spurious correlations
- **Benefit**: Identifies failure modes; improves robustness to distribution shifts

#### 3. **High-Stakes Policy & Legal Decisions**
- **Challenge**: Decisions affecting individuals (loan approvals, hiring, criminal justice) must be explainable to stakeholders and regulators
- **Application**: Computer vision for automated identity verification, document classification
- **Interpretability Method**: Nameability ensures decision-makers understand what visual features the model uses
- **Benefit**: Regulatory compliance (GDPR, AI Act, Fair Lending regulations)

#### 4. **Scientific Discovery & Neuroscience**
- **Challenge**: Understanding what neural networks learn, particularly as models scale
- **Application**: Using vision models as models of biological vision; interpretable models aid neuroscience research
- **Interpretability Method**: Psychophysics protocols borrowed from neuroscience; direct bridge between artificial and biological vision
- **Benefit**: Accelerates understanding of both biological and artificial intelligence

### Regulatory & Compliance Implications

**EU AI Act**: Requires high-risk AI systems to be interpretable and subject to human oversight
- Models evaluated with this framework can provide quantitative interpretability metrics to regulators
- Demonstrates that developers have measured and validated model interpretability

**FDA Medical Device Approval**: Requires understanding of AI model logic
- Localizability testing provides evidence that models attend to clinically relevant features
- Nameability demonstrates clinical acceptability of learned features

**Data Privacy & Bias Auditing**: 
- Interpretable features make it easier to audit for unwanted biases or artifacts
- Can detect models learning spurious patterns correlated with protected attributes

### Implementation Challenges

1. **Computational Cost**: Sparse autoencoder training + human evaluation is expensive
   - Mitigate: Focus evaluation on critical model decisions or high-stakes applications
   - Consider: Automated proxies for interpretability that correlate with human judgments

2. **Scalability**: Evaluating every model and layer is infeasible
   - Mitigate: Develop efficient scoring methods; sample representative layers and features
   - Focus: Evaluate models at deployment time for high-stakes applications

3. **Generalization Across Domains**: Interpretability measured on ImageNet may not transfer to medical imaging
   - Mitigate: Domain-specific evaluation protocols; task-specific feature extraction
   - Recommendation: Evaluate interpretability in the target application domain

4. **Observer Recruitment & Agreement**: Securing high-quality human judgments is challenging
   - Mitigate: Use crowd-sourcing platforms with quality control; establish inter-observer agreement thresholds
   - Consider: Domain expertise requirements (e.g., radiologists for medical images)

## Insights & Implications

### Shifting Paradigms in Explainable AI

1. **From Methods to Models**: The field should move beyond developing new attribution techniques and focus on building, training, and evaluating models to be inherently interpretable.

2. **Capability ≠ Interpretability**: Scaling and foundation models improve task performance but may sacrifice interpretability—a critical trade-off often overlooked in AI deployment.

3. **Psychophysics as Scientific Framework**: Rigorous, human-centered evaluation methods from psychology are essential to make interpretability a measurable, scientific property rather than a vague concept.

### Deeper Understanding of Vision Models

1. **Feature Representational Quality**: The interplay between localizability and nameability reveals the quality of learned representations across architectures.

2. **Architectural Implications**: Simple design choices (attention mechanisms, skip connections, layer normalization) may differentially affect interpretability—an underexplored design space.

3. **Self-Supervised Learning Trade-offs**: Self-supervised methods achieve broad transferability but at the cost of direct interpretability to humans—raises questions about whether human understanding is necessary for robust generalization.

### Future Directions for XAI Research

1. **Designing Interpretable Models Proactively**: Rather than post-hoc explanation, develop training objectives that encourage interpretable feature learning.
   - Possible approach: Regularize for feature locality and semantic alignment during training
   - Potential methods: Contrastive learning with human-aligned objectives

2. **Interpretability-Capability Pareto Frontiers**: Systematically characterize trade-offs between interpretability and task performance across architectures and training methods.
   - Question: Can we build models achieving both high capability and high interpretability?
   - Potential path: Pruning, distillation, or architectural innovations

3. **Cross-Domain Interpretability Benchmarks**: Develop standardized benchmarks for measuring interpretability in different domains (medical imaging, autonomous systems, robotics).

4. **Mechanistic Interpretability Integration**: Combine psychophysics-based human evaluation with mechanistic approaches (circuit analysis, causal intervention) for multi-level understanding.

5. **Interpretability-Aware Training Algorithms**: Develop learning algorithms that optimize for interpretability as a first-class objective, not an afterthought.

### Open Questions & Limitations

1. **Does Interpretability Matter for Robustness?** Are interpretable models more robust to adversarial examples and distribution shifts? 

2. **Human Interpretability vs. Task Performance:** Is there a fundamental trade-off, or can we achieve both? What are the conditions?

3. **Generalization of Psychophysics Protocols:** How well do these human evaluation methods transfer to other domains (text, audio, RL)?

4. **Scalability to Large Models:** As models continue to scale (billions of parameters), is the human evaluation approach even feasible?

## Code & Resources

### Official Implementation & Data

- **ArXiv Page:** https://arxiv.org/abs/2609.05399
- **Full Paper PDF:** https://arxiv.org/pdf/2609.05399
- **Code Repository:** [Status: Check paper and authors' websites — code availability not confirmed in abstract]
- **Dataset & Evaluation Protocols:** [Likely available upon request or as supplementary material]

### Related Work & Tools

- **Sparse Autoencoders for Interpretability:** [2405.12677] Scaling Monosemanticity: Analyzing and Interpreting Large-Scale Language Models Using the Distributed Alignment Search (arXiv)
- **Foundation Model Interpretability:** Related paper "Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models" (arXiv 2605.20337)
- **Psychophysics in Vision Science:** Classic frameworks for measuring human perception and discrimination

### Dependencies & Computational Requirements

**Required Libraries** (estimated from related work):
- PyTorch or TensorFlow for neural network operations
- Scikit-learn for statistical analysis
- Matplotlib/Plotly for visualizations
- Standard computer vision libraries (OpenCV, PIL/Pillow)

**Computational Resources** [Exact figures unavailable — see full paper]:
- GPU acceleration highly recommended for sparse autoencoder training
- Human evaluation studies require recruited observers (crowd-sourcing platforms)
- Typical budget: weeks to months for comprehensive evaluation depending on number of models and features

### Quick Start

1. **Install dependencies** from requirements.txt (to be confirmed from paper)
2. **Select neural network model** for evaluation
3. **Train sparse autoencoders** on layer activations
4. **Generate feature visualizations** (or use attention-based methods)
5. **Recruit human observers** (e.g., via Amazon Mechanical Turk, Prolific, or custom interface)
6. **Run localizability protocol**: Observers predict feature activation on test images
7. **Run nameability protocol**: Observers describe feature semantic meaning
8. **Compute scores**: Normalize using chance-level baselines; aggregate across observers
9. **Compare interpretability across models** using generated metrics

## Related Work & Context

### Complementary Interpretability Approaches

**1. Attribution & Gradient-Based Methods:**
- LIME (Local Interpretable Model-Agnostic Explanations)
- SHAP (SHapley Additive exPlanations)
- Integrated Gradients
- *Relationship*: These are post-hoc methods that explain individual predictions; the new framework evaluates *model-level* interpretability, orthogonal to explaining single predictions

**2. Concept-Based Explanations:**
- TCAV (Testing with Concept Activation Vectors)
- ACE (Automated Concept-based Explanations)
- CBM (Concept Bottleneck Models)
- *Relationship*: Use human-defined or automatically discovered concepts; the new framework grounds concepts in human perception via psychophysics

**3. Circuit-Based Analysis:**
- Feature attribution through circuit analysis
- Mechanistic interpretability: Understanding how circuits implement functions
- *Relationship*: Focuses on computational mechanisms; complementary to measuring human-perceived interpretability

**4. Recent xAI Surveys & Meta-Research:**
- Papers questioning the alignment between interpretability methods and human understanding
- Studies showing poor generalization of saliency maps and attention visualizations
- *Relationship*: This work directly addresses gaps identified in prior meta-research

### Position Within xAI Research Community

**Standing:** Bridges cognitive science (psychophysics) and interpretability research, bringing empirical rigor to human-centered evaluation.

**Impact on Subfields:**
- **Feature Attribution**: Shifts focus from developing new methods to evaluating whether features are interpretable
- **Human-Centered XAI**: Provides quantitative, reproducible methods for human evaluation
- **Model Design**: Informs architectural and training choices for improving interpretability
- **Mechanistic Interpretability**: Complements circuit analysis with human evaluation

### Prior Work This Paper Builds On

1. **Sparse Autoencoders & Monosemanticity:**
   - [2404.16612] "Scaling and evaluating sparse autoencoders" — Technical foundations for SAE training

2. **Human Interpretability Studies:**
   - [1912.05011] "A psychophysics approach for quantitative comparison of interpretable computer vision models" — Early work using psychophysics for interpretability

3. **Foundation Model Analysis:**
   - [2605.20337] "Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models" — Detailed psychophysics study of foundation models

4. **Surveys on Interpretability Evaluation:**
   - Various surveys documenting the maturity of interpretability methods and gaps in evaluation

### Where This Research Leads

**Short-term (1-2 years):**
- Standardized psychophysics protocols for vision model evaluation
- Interpretability benchmarks for comparing models and architectures
- Integration with regulatory compliance frameworks

**Medium-term (2-5 years):**
- Interpretability-aware training algorithms and loss functions
- Multi-modal interpretability evaluation (vision + language)
- Causal and mechanistic explanations anchored in human-interpretable features

**Long-term (5+ years):**
- AI systems designed from the ground up for human interpretability
- Convergence of human psychology, neuroscience, and AI; mutual validation
- Regulatory standards for interpretability measurement in high-stakes domains

## References & Further Reading

### Key Papers Cited/Related

- Colin, J., Goetschalckx, L., Oliver, N., & Serre, T. (2026). Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models. *arXiv preprint arXiv:2605.20337*.

- "Scaling and evaluating sparse autoencoders." *arXiv preprint arXiv:2404.16612*.

- "A psychophysics approach for quantitative comparison of interpretable computer vision models." *arXiv preprint arXiv:1912.05011*.

- Simonyan, K., & Zisserman, A. (2014). Very deep convolutional networks for large-scale image recognition. *ICLR*.

- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. *CVPR*.

### Recommended Reading Order

1. Start here: This paper ("From Interpretability Methods to Interpretable Models")
2. Detailed empirical study: "Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models"
3. Technical foundations: Recent sparse autoencoder scaling papers
4. Broader context: Surveys on interpretability evaluation and human-centered XAI

---

**Last Updated:** 2026-09-11  
**Paper Submitted to arXiv:** September 4, 2026
