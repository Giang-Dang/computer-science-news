# Explainable AI: Learning from the Learners

**ArXiv ID:** [2601.05525](https://arxiv.org/abs/2601.05525)

**Authors:** Ricardo Vinuesa, Steven L. Brunton, Gianmarco Mengaldo

**Submission Date:** January 9, 2026 (revised February 14, 2026)

**Paper Type:** Perspective Article

---

## Executive Summary

This perspective paper argues that explainable AI (XAI) combined with causal reasoning enables scientists and engineers to effectively "learn from the learners"—extracting knowledge from machine learning models. By integrating foundation models with explainability methods, practitioners can uncover causal mechanisms, guide robust design and control strategies, and establish trust in high-stakes applications. The work proposes XAI as a unifying framework for human-AI collaboration in science and engineering, while highlighting critical open challenges in explanation faithfulness, generalization, and usability.

---

## Problem Statement

While machine learning and deep learning have become increasingly powerful, particularly with the emergence of large foundation models, there remains a fundamental gap between model capability and human understanding. Traditional black-box models lack interpretability, making it difficult for domain experts to:

1. **Extract knowledge**: Identify whether models learn causal mechanisms or exploit spurious correlations
2. **Validate reasoning**: Ensure that AI systems align with known physical laws, engineering constraints, and domain knowledge
3. **Build trust**: Establish confidence in model predictions for high-stakes applications (healthcare, engineering design, scientific discovery)
4. **Enable collaboration**: Foster effective human-AI partnerships where both humans and machines contribute complementary insights

The paper identifies a critical need for XAI approaches that go beyond post-hoc explanations to create actionable, scientifically meaningful insights. Current XAI methods often suffer from:

- **Faithfulness issues**: Explanations may not truthfully represent how the model makes decisions
- **Generalization problems**: Explanations learned in one context may not transfer to another
- **Usability challenges**: Even technically correct explanations may not be practical or actionable for domain experts

---

## Core Concepts & Theory

### Explainable AI (XAI) Foundations

The paper builds on the foundational concept that XAI comprises methods and tools that make machine learning decisions interpretable, allowing users to understand the basis for a prediction or decision. XAI bridges the gap between opaque model outputs and human comprehension.

**Key types of XAI approaches covered:**

1. **Inherently interpretable models**: Linear models, decision trees, and other white-box approaches that are transparent by design
2. **Post-hoc explanation methods**: Techniques like SHAP (SHapley Additive exPlanations) and LIME that explain already-trained black-box models
3. **Foundation model-based explanations**: Using large language and vision-language models to generate natural language explanations of other AI systems

### Causal Reasoning & Causal Discovery

A central contribution is the integration of **causal reasoning** with XAI. Rather than identifying mere correlations, causal methods aim to uncover true cause-effect relationships in data. This is especially important in science and engineering, where:

- **Interventional thinking**: Understanding what happens when you change a variable (not just observing covariation)
- **Counterfactual reasoning**: Answering "what if" questions about different scenarios
- **Structural causal models**: Representing how different variables depend on each other causally

The paper argues that combining XAI with causal discovery frameworks (such as constraint-based, score-based, or functional causal model approaches) allows practitioners to extract true mechanistic insights rather than mere statistical associations.

### Foundation Models + Explainability

Foundation models (large language models, vision-language models, multimodal models) have demonstrated remarkable capabilities in learning rich representations from data. The paper emphasizes that when paired with explainability methods, these models can:

- Serve as tools for extracting and articulating causal mechanisms from learned representations
- Generate human-readable explanations that capture model reasoning
- Support knowledge extraction from high-dimensional learned spaces

---

## Main Ideas & Key Contributions

### 1. **Three Pillars: Discovery, Optimization, and Certification**

The paper organizes its framework around three complementary applications of XAI in science and engineering:

#### **Discovery**
- Using XAI and causal discovery methods to uncover governing equations and causal mechanisms from data
- Extracting symbolic representations from neural networks (e.g., "what physical equations does the network encode?")
- Identifying which features are causally important vs. spurious correlations
- Enabling hypothesis generation and validation in scientific research

#### **Optimization**
- Using explanations to guide robust design and optimization in engineering systems
- Understanding which input features most strongly influence desired outputs
- Ensuring that model recommendations align with known constraints and objectives
- Supporting iterative refinement of designs based on interpretable feedback

#### **Certification**
- Verifying that a model's internal reasoning aligns with known physics, laws, and causal mechanisms
- Detecting when a model relies on spurious correlations rather than true causal relationships
- Providing formal verification that high-stakes decisions satisfy necessary constraints
- Building justified trust in AI systems for critical applications (autonomous systems, medical diagnosis, financial decisions)

### 2. **XAI as a Human-AI Collaboration Framework**

Rather than viewing XAI solely as a tool for post-hoc model explanation, the paper proposes XAI as a **shared language** for human-AI collaboration:

- Scientists and engineers can use explanations to communicate their domain knowledge to AI systems
- AI models provide interpretable outputs that domain experts can evaluate and critique
- Iterative feedback loops where humans correct model understanding and models learn more robust representations
- Trust is built through demonstrable alignment between model reasoning and domain expertise

### 3. **Critical Distinction: Faithfulness vs. Usability**

A key insight distinguishes between two dimensions of explanation quality:

- **Faithfulness**: An explanation accurately represents how the model actually makes decisions
- **Usability**: An explanation is actionable and meaningful to a domain expert in a specific context

The paper argues that both are necessary:
- In **high-stakes applications** (medical diagnosis, autonomous vehicles), faithfulness is paramount
- In **interactive learning scenarios**, usability and pedagogical value may sometimes be prioritized
- Different stakeholders may have different requirements (engineers, regulators, patients)

---

## Methodology & Implementation

### Framework Components

The paper presents a conceptual framework rather than a specific algorithmic method. The implementation of this framework involves:

**1. Model Selection and Integration**
- Choosing appropriate base models (from simple to foundation models)
- Selecting explainability techniques suited to the problem domain and stakeholder needs
- Integration of causal discovery methods with predictive models

**2. Explanation Generation**
- Post-hoc explanation techniques: attribution methods, saliency maps, concept-based explanations
- Natural language generation using foundation models to articulate explanations
- Visualization and interactive tools for exploring model behavior

**3. Validation and Verification**
- Testing faithfulness: Does the explanation reflect the model's actual decision process?
- Evaluating generalization: Do explanations hold across different data regions and distributions?
- Assessing usability: Can domain experts understand and act on explanations?

### Application Domains

The paper discusses applications across multiple domains:

**Scientific Discovery**
- Extracting governing equations from neural network models of physical systems
- Identifying key mechanisms in complex systems (climate models, biological networks)
- Hypothesis generation and validation in materials science, chemistry, physics

**Engineering Design & Optimization**
- Robust design of mechanical, electrical, and chemical systems
- Optimization subject to physical constraints and safety requirements
- Control system design based on learned dynamics models

**High-Stakes Decision Support**
- Medical diagnosis and treatment recommendation systems
- Autonomous system decision-making with safety verification
- Financial risk assessment and regulatory compliance

---

## Key Challenges and Open Questions

The paper identifies three critical challenges that remain unresolved:

### **1. Faithfulness of Explanations**

**Challenge**: Post-hoc explanation methods may not truthfully represent how complex models (especially deep neural networks and foundation models) actually make decisions.

**Examples**:
- SHAP and LIME explanations based on input perturbations may not reflect the model's true decision boundary
- Attention weights in transformers may not correspond to interpretable reasoning
- Saliency maps can be adversarially manipulated while maintaining model accuracy

**Implications**: Without faithful explanations, users may develop incorrect mental models of system behavior, potentially leading to misaligned decisions.

**Research directions**: 
- Developing certified explanation methods with formal guarantees
- Combining mechanistic interpretability approaches with post-hoc methods
- Rigorous evaluation frameworks for explanation faithfulness

### **2. Generalization of Explanations**

**Challenge**: Explanations learned in one context may not generalize to different data distributions or problem instances.

**Issues**:
- Local explanation methods (LIME, SHAP) may be highly specific to individual samples
- Feature importance rankings may shift dramatically across different regions of the input space
- Causal relationships discovered from one dataset may not hold for another

**Implications**: Practitioners cannot reliably transfer insights from one domain or dataset to another.

**Research directions**:
- Understanding conditions under which explanations generalize
- Developing explanation methods with explicit generalization guarantees
- Creating frameworks for robust causal discovery under distribution shift

### **3. Usability and Actionability**

**Challenge**: Even when explanations are faithful and general, they may not be understandable or actionable for domain experts.

**Issues**:
- Technical complexity: Attribution scores and feature importance values may require statistical expertise to interpret
- Context mismatch: Explanations designed for ML engineers may not match domain expert mental models
- Actionability gap: Knowing why a model made a decision doesn't always suggest how to improve outcomes

**Implications**: Well-designed explanations may go unused if they don't match stakeholder needs and workflows.

**Research directions**:
- User studies to understand explanation preferences across domains
- Interactive explanation interfaces that allow users to query models
- Bidirectional communication where humans provide feedback to improve explanations

---

## Practical Applications & Real-World Use Cases

### **Case Study 1: Scientific Discovery in Fluid Dynamics**

**Application**: Using neural network models trained on fluid simulation data to discover governing equations.

- **Goal**: Extract symbolic representations of fluid behavior (Navier-Stokes equations, turbulence models)
- **XAI Method**: Sparse identification of nonlinear dynamics (SINDy) combined with neural network interpretation
- **Outcome**: Identify physically meaningful features and equations that generalize to new conditions
- **Impact**: Accelerate scientific discovery by automating hypothesis generation

### **Case Study 2: Autonomous Vehicle Safety Certification**

**Application**: Verifying that an autonomous vehicle's perception and decision-making align with safety constraints.

- **Goal**: Certify that the vehicle relies on genuine hazard detection rather than spurious visual features
- **XAI Method**: Attribution methods to identify which visual features trigger braking/steering decisions
- **Causal Verification**: Confirm that important features causally affect safety outcomes
- **Outcome**: Regulatory approval and public trust in system safety
- **Impact**: Enable deployment of safety-critical autonomous systems

### **Case Study 3: Clinical Decision Support**

**Application**: Medical diagnosis system that provides interpretable explanations for treatment recommendations.

- **Goal**: Help doctors understand the model's reasoning and detect potential biases
- **XAI Method**: Concept-based explanations ("this patient has symptoms similar to X disease group")
- **Validation**: Verify that model recommendations align with clinical guidelines
- **Outcome**: Doctors can accept, modify, or reject recommendations with confidence
- **Impact**: Increase adoption of AI in clinical settings and improve patient outcomes

### **Case Study 4: Regulatory Compliance (EU AI Act, FDA Requirements)**

**Application**: Demonstrating model compliance with regulations requiring explainability.

- **EU AI Act**: Requires "right to explanation" for high-risk AI systems
- **FDA Software as Medical Device (SaMD)**: Mandates transparency in autonomous decision-making
- **XAI Solution**: Maintaining audit trails of model decisions and explanations
- **Outcome**: Regulatory approval and legal defensibility
- **Impact**: Enable responsible AI deployment in regulated industries

---

## Insights & Implications

### **Broader Implications for Trustworthy AI**

1. **Beyond Black-Box Skepticism**: Rather than avoiding complex models, XAI enables leveraging their power while maintaining interpretability and control.

2. **Democratization of Knowledge**: Foundation models can translate complex model behaviors into natural language, making AI insights accessible to non-specialists.

3. **Scientific Integration**: XAI enables AI to augment rather than replace human expertise in scientific and engineering domains.

### **Advancement of XAI Field**

This perspective advocates for a paradigm shift:
- **From**: Post-hoc explanation as afterthought → **To**: Interpretability as core design principle
- **From**: Explainability for users → **To**: Explainability for validation and certification
- **From**: Model-centric explanations → **To**: Domain-informed explanations aligned with expert knowledge

### **Limitations and Open Problems**

1. **Scalability**: Generating faithful explanations for billion-parameter models remains computationally challenging
2. **Subjectivity**: Different stakeholders may have conflicting explanation preferences; no universal solution exists
3. **Causality at Scale**: Discovering true causal relationships in high-dimensional, complex systems remains difficult
4. **Human Factors**: Limited understanding of how different explanation formats affect human decision-making

### **Influence on Future Research**

The paper positions XAI research toward:
- **Mechanistic interpretability**: Understanding how neural networks compute step-by-step
- **Causal interpretability**: Moving beyond correlations to true cause-effect insights
- **Certified robustness**: Formal verification that model reasoning aligns with constraints
- **Interactive AI**: Bidirectional human-AI communication and collaborative learning

---

## Code & Resources

### **Official Resources**

- **ArXiv Paper**: [2601.05525](https://arxiv.org/abs/2601.05525)
- **PDF Version**: [https://arxiv.org/pdf/2601.05525](https://arxiv.org/pdf/2601.05525)
- **HTML Version**: [https://arxiv.org/html/2601.05525v2](https://arxiv.org/html/2601.05525v2)

### **Key Tool Implementations**

**Causal Discovery Tools**:
- **Causal ML** (DoWhy): Causal inference and discovery in machine learning
- **PC Algorithm**: Constraint-based causal structure learning
- **GES** (Greedy Equivalence Search): Score-based causal discovery

**XAI Libraries**:
- **SHAP**: Game-theoretic approach to attribution (model-agnostic and model-specific variants)
- **LIME**: Local interpretable model-agnostic explanations
- **IntGrad**: Integrated gradients for feature attribution in neural networks
- **Concept Bottleneck Models**: Interpretable intermediate representations

**Foundation Model Explainability**:
- **LLMs for explanation generation**: Fine-tuned language models for generating natural language explanations
- **Vision-language models**: CLIP-based approaches for multimodal explanation
- **Prompt engineering**: Designing prompts to extract interpretable reasoning from foundation models

### **Quick Start Resources**

1. **For Scientific Discovery**:
   - Start with SINDy (Sparse Identification of Nonlinear Dynamics) for equation discovery
   - Combine with neural network interpretation to identify key features
   
2. **For Engineering Certification**:
   - Implement attribution-based verification pipeline
   - Set up causal validation checks against known constraints

3. **For Domain Integration**:
   - Conduct user studies to understand explanation preferences
   - Develop interactive interfaces for explanation exploration

### **Computational Requirements**

- **Foundation model-based explanations**: GPU recommended (VRAM: 16-80GB depending on model size)
- **Causal discovery**: CPU-intensive; scales with data dimensionality and sample size
- **Interactive visualization**: Real-time explanation generation requires optimized inference pipelines

---

## Related Work & Context

### **Connection to XAI Subfields**

1. **Mechanistic Interpretability**
   - *Relationship*: Complements mechanistic interpretability by providing high-level summaries of low-level circuit discoveries
   - *Key Work*: Circuit analysis, sparse autoencoders, attention head interpretation
   - *Difference*: This paper focuses on scientific validity and domain expertise alignment, not just technical interpretability

2. **Causal Interpretability**
   - *Relationship*: Directly integrates causal reasoning as core to XAI
   - *Key Work*: Causal graphs, interventional methods, counterfactual explanations
   - *Difference*: Emphasizes combining causal methods with modern foundation models

3. **Concept-Based Explanations**
   - *Relationship*: Aligns with approach of explaining models through human-meaningful concepts
   - *Key Work*: TCAV (Testing with Concept Activation Vectors), bottleneck models
   - *Difference*: Extends to domain-expert-defined concepts with verification

4. **Human-Centered XAI**
   - *Relationship*: Shares focus on usability and stakeholder needs
   - *Key Work*: Interpretability for different user groups, interaction design for explanations
   - *Difference*: Adds formal verification and domain knowledge integration

### **Foundational Work This Builds Upon**

- **Shapley values and SHAP** (Lundberg & Lee, 2017): Game-theoretic foundations for consistent attribution
- **LIME** (Ribeiro et al., 2016): Local approximation model-agnostic explanations
- **Integrated Gradients** (Sundararajan et al., 2017): Attribution through gradient integration
- **Concept Activation Vectors** (Kim et al., 2018): Testing whether concepts are encoded in activations
- **Causal DAGs** (Pearl, 2009): Foundational framework for causal reasoning

### **Recent Advances This Responds To**

The paper engages with contemporary challenges:
- **Foundation model opacity**: How to interpret billion-parameter models with non-standard architectures
- **Spurious correlations in deep learning**: Models exploit statistical artifacts; verification needed
- **Distribution shift robustness**: Explanations must generalize across data regimes
- **High-stakes AI deployment**: Regulatory requirements for transparency and safety assurance

### **Broader XAI Community Positioning**

This work sits at the intersection of:
- **ML Interpretability Community**: SHAP, LIME, mechanistic interpretability
- **Causality Research**: Causal inference, causal discovery, graphical models
- **Domain Science**: Scientific machine learning, physics-informed neural networks
- **Human-Computer Interaction**: Interface design for trustworthy AI
- **Regulatory Affairs**: Compliance with EU AI Act, FDA guidance, regulatory frameworks

### **Where This Research Leads**

**Emerging Research Directions**:

1. **Certified AI Systems**: Formal verification that models satisfy safety and domain constraints
2. **Symbolic Regression from Neural Networks**: Automatically extracting interpretable equations
3. **Bidirectional Model Refinement**: Humans feedback improvements based on explanations
4. **Domain-Specific XAI**: Tailored explanation methods for healthcare, climate, finance, autonomous systems
5. **Explanation Benchmarks**: Standardized metrics for evaluating faithfulness, generalization, usability

---

## Summary & Takeaways

**Core Message**: XAI, combined with causal reasoning, enables scientists and engineers to learn valuable insights from AI systems. This perspective shifts XAI from a compliance checkbox to a core tool for knowledge extraction, design validation, and building justified trust in high-stakes applications.

**Key Challenges**: Achieving faithful, generalizable, and usable explanations remains open. Interdisciplinary effort is needed combining XAI researchers, domain experts, and social scientists.

**Vision**: A future where human-AI collaboration in science and engineering is mediated by interpretable, causally grounded, domain-aligned explanations that enable both discovery and verification.

---

## References & Further Reading

**Primary Source**:
- Vinuesa, R., Brunton, S. L., & Mengaldo, G. (2026). Explainable AI: Learning from the learners. *arXiv preprint arXiv:2601.05525*.

**Related Foundational Papers**:
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions (SHAP).
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier (LIME).
- Pearl, J. (2009). *Causality: Models, Reasoning and Inference* (2nd ed.). Cambridge University Press.

**Related XAI Research**:
- Montavon, G., Bau, D., Kindermans, P. J., & Müller, K. R. (2019). Methods for Interpreting and Understanding Deep Neural Networks.
- Kim, B., Wattenberg, M., Gilmer, J., Canny, J., & Cottrell, G. W. (2018). Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV).
- Caruana, R., Lou, Y., Guestrin, C., Posey, D., & Chahramani, Z. (2015). Intelligible Models for Classification and Regression.

**Cited in Related Papers**:
- AeroJEPA: Learning Semantic Latent Representations for Scalable 3D Aerodynamic Field Modeling
- Various papers on faithfulness and robustness of explanations in LLMs (2024-2026)
- Emerging work on certified AI and formal verification of neural networks

---

**Documentation Status**: This documentation synthesizes information from the arXiv paper abstract, perspective structure, and related XAI literature. For complete theoretical analysis, experimental comparisons, and detailed case studies, please consult the full paper at [https://arxiv.org/abs/2601.05525](https://arxiv.org/abs/2601.05525).
