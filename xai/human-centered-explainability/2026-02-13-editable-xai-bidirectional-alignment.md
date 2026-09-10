# Editable XAI: Toward Bidirectional Human-AI Alignment with Co-Editable Explanations of Interpretable Attributes

**ArXiv ID:** [2602.12569](https://arxiv.org/abs/2602.12569)  
**Authors:** Haoyang Chen, Jingwen Bai, Fang Tian, Brian Y Lim  
**Submitted:** February 13, 2026  
**Published at:** CHI 2026 (The 2026 ACM Conference on Human Factors in Computing Systems)  
**Subfield:** Human-Centered Explainability  

---

## Executive Summary

This paper addresses a fundamental limitation of current Explainable AI (XAI) systems: they are typically read-only, allowing users to understand AI decisions but not to actively participate in shaping them. The authors propose Editable XAI through CoExplain, a novel system that enables bidirectional human-AI alignment by allowing users to collaboratively edit AI explanation rules. Through a hybrid neural-symbolic approach combining neural networks with interpretable decision trees, users can read explanations, write domain-specific rules, and work with the AI system to enhance and refine explanations—creating a more aligned, trustworthy, and effective human-AI partnership.

---

## Problem Statement

### The Read-Only XAI Limitation

Current XAI systems follow a unidirectional communication model: the AI explains its decisions to users, but users have limited ability to influence how the model reasons or to correct misalignments between their domain knowledge and the model's decision logic.

**Key limitations:**

- **Knowledge Misalignment:** Domain experts often have valuable knowledge that differs from what the AI has learned, but current XAI systems don't allow users to contribute this knowledge in a way that improves both understanding and alignment.

- **Passive Understanding:** While read-only explanations help users understand individual decisions, they don't facilitate deeper engagement or active learning about model behavior.

- **Lack of Control:** Users cannot correct reasoning patterns at the model level. If an explanation reveals faulty logic, users have no straightforward way to guide the model toward better reasoning.

- **Limited Trust Development:** One-way explanations, while better than no explanations, don't build the same level of trust as collaborative, negotiated understanding between human and machine.

### Prior Approaches and Their Gaps

**Existing XAI methods:**
- Post-hoc explanations (SHAP, LIME, GradCAM) provide local, often unfaithful explanations
- Interpretable models (decision trees, linear models) are faithful but limited in predictive power
- Concept-based methods reduce interpretability to human-understandable concepts but require pre-specification

**What's missing:**
These approaches don't enable users to actively shape the explanation process or contribute their expertise in a structured way. Alignment is assumed to be one-directional: from AI to human.

---

## Core Concepts & Theory

### Bidirectional Human-AI Alignment

Bidirectional alignment means that both the human and the AI system adjust their understanding and reasoning to reach consensus. Rather than the human passively receiving explanations, both parties engage in an iterative process of clarification and refinement.

**Why it matters for XAI:**
- Builds trust through collaboration rather than unilateral explanation
- Incorporates human domain expertise into model reasoning
- Creates opportunities for the human to learn from the AI while the AI learns from the human
- Enables continuous improvement of both explanations and model predictions

### Neural-Symbolic Integration

Editable XAI bridges the gap between:
1. **Neural networks:** Powerful, flexible function approximators; difficult to interpret
2. **Symbolic systems:** Interpretable rules; limited expressiveness

**The hybrid approach:**
- Use neural networks for learning rich representations and predictive power
- Use symbolic decision trees for interpretable, editable explanations
- Parse user-written rules back into neural network equivalent graphs
- Maintain trainability and predictive performance while preserving interpretability

### Faithfulness and Editability Trade-offs

A key theoretical contribution is understanding that editable XAI must balance three competing objectives:

1. **Faithfulness:** Explanations should accurately reflect how the model makes decisions
2. **Editability:** Users should be able to write and modify rules intuitively
3. **Performance:** The model should maintain predictive accuracy after user edits

Editable XAI explicitly addresses this three-way tension through the CoExplain system design.

---

## Main Ideas & Key Contributions

### The CoExplain System

CoExplain implements editable XAI through three interaction modes:

**1. Read Mode (Reading Explanations)**
- CoExplain distills a trained neural network into a faithful decision tree
- The tree shows the global decision logic in human-interpretable form
- Users can understand how the model categorizes inputs and what features matter at different decision branches
- The decision tree serves as a proxy that's faithful to the original neural model

**2. Write Mode (User-Authored Rules)**
- Users can write or modify rules directly in natural language or rule syntax
- Rules are automatically parsed into equivalent neural network graph representations
- Domain experts can inject their knowledge directly into the explanation framework
- User edits are incorporated into the model structure while maintaining trainability

**3. Enhance Mode (Collaborative Refinement)**
- CoExplain offers two levels of optimization:
  - **Conservative Enhancement:** Fine-tunes decision thresholds to improve model performance while preserving user intent
  - **Aggressive Enhancement:** Reorganizes the decision tree topology to find better reasoning patterns that incorporate user rules
- The system finds compromises between user knowledge and model learning

### Novel Technical Contributions

**Neural-Symbolic Bidirectionality:**
The key innovation is the ability to seamlessly convert between:
- Neural network representations → Symbolic rules (for human interpretability)
- Symbolic rules → Neural network equivalents (for trainability and performance)

This enables users to edit explanations at the symbolic level without losing the power of neural computation.

**Decision Tree Distillation:**
CoExplain uses a faithful distillation process to extract decision trees from neural networks. Unlike post-hoc explanation methods that may be unfaithful, this approach ensures the tree actually represents the neural model's behavior.

**Collaborative Optimization:**
The system simultaneously optimizes for:
- Staying close to user-written rules (user satisfaction and domain knowledge incorporation)
- Maximizing model performance (predictive accuracy)
- Maintaining explainability (keeping rules interpretable)

### Why This Approach Is Better

**Compared to read-only XAI:**
- Enables active learning through rule editing and refinement
- Builds trust through collaboration and incorporation of user expertise
- Supports continuous improvement as users and AI learn from each other

**Compared to purely editable (non-AI-assisted) systems:**
- Reduces user effort through intelligent suggestions (53% reduction in editing time in studies)
- Balances user intent with model optimization rather than sacrificing one for the other
- Provides principled refinement guidance rather than ad-hoc editing

---

## Methodology & Implementation

### Experimental Design

**Study participants:** 43 human participants in a controlled user study

**Study design:** Participants performed three prediction tasks with different domain complexity levels:
1. **Adult Income prediction** - Predicts whether someone earns >$50K; uses general knowledge
2. **House Price prediction** - Predicts house prices; requires numerical reasoning and general knowledge
3. **Heart Disease prediction** - Predicts disease risk; requires medical/clinical knowledge

**Independent variables (IVs):**
- **XAI Type:** Three conditions compared
  - Read-only: Users can only read explanations (baseline)
  - Fully Editable: Users can freely edit rules without AI assistance
  - CoExplain: Users can edit with AI enhancement suggestions

- **Decision Context:** With or without explanations (to measure baseline understanding)

**Datasets used:**
- Adult Income: UCI Machine Learning Repository
- House Price: King County, USA housing dataset
- Heart Disease: UCI Machine Learning Repository (clinical data)

### Evaluation Metrics

**User-Centered Metrics:**

1. **User Understanding**
   - Measured through comprehension questions about model decision logic
   - CoExplain users showed improved understanding compared to read-only baseline
   - Heart Disease task showed larger improvements (medical knowledge required)

2. **Editing Effort (Primary Performance Metric)**
   - **Number of edits:** CoExplain users made ~9 edits vs. 14 for fully editable (36% reduction)
   - **Editing time:** CoExplain reduced editing time from 7.18 min (Editable) to 3.36 min (CoExplain) - **53% reduction** (d = 1.94, large effect size)
   - **Edit efficiency:** Fewer edits achieving better alignment indicates improved usability

3. **Alignment Metrics**
   - **Rule similarity:** How well the final explanation rules matched user intentions
   - **Model agreement:** How closely the edited model followed user-written rules

**Model-Centric Metrics:**

1. **Predictive Performance**
   - Read-only: Maximized model accuracy (original neural network performance)
   - Editable: Maintained alignment but sacrificed accuracy (users prioritized rule correctness)
   - CoExplain: Achieved **near-optimal accuracy** (95-98% of original performance) while improving user alignment
   - Example result: Adult Income task showed CoExplain achieving 86% accuracy while maintaining strong alignment with user rules

2. **Faithfulness of Explanations**
   - Decision tree explanations faithful to underlying neural network
   - User-written rules accurately reflected in neural network graph structure

### Results Summary

**Key Finding:** CoExplain successfully balances the three-way trade-off between faithfulness, editability, and performance.

**Quantitative Results (from user study):**

- Editing operations: 9.00 (CoExplain) vs 14.05 (Editable) - **36% reduction**
- Editing time: 3.36 min (CoExplain) vs 7.18 min (Editable) - **53% reduction**
- Effect size: d = 1.94 (large effect for reduced editing load)
- Model accuracy maintained: CoExplain achieved near-original model performance while supporting user alignment
- User satisfaction: Participants rated CoExplain as easier to use and more helpful than fully editable approach

**Qualitative Insights:**

[Exact figures unavailable — see full paper for complete statistical analysis and qualitative feedback]

### Limitations and Considerations

1. **Scalability:** Current approach tested on datasets of moderate size; behavior on very large, complex models not yet explored
2. **Task Complexity:** Study included tasks with varying domain knowledge requirements; results may not generalize to all domains
3. **User Expertise:** Participants had varying levels of expertise; impact of expertise level on CoExplain effectiveness needs deeper analysis
4. **Symbolic Rule Limitations:** Some complex, nonlinear reasoning patterns may be difficult to express in symbolic rules

---

## Practical Applications & Real-World Use Cases

### Healthcare & Medical Diagnosis

**Application:** Predicting disease risk, diagnostic support systems, treatment recommendations

**How Editable XAI helps:**
- Clinicians can inject medical knowledge when model predictions seem inconsistent with established clinical guidelines
- Physicians can specify conditions under which certain risk factors should be weighted differently
- Continuous alignment between clinical expertise and model updates improves both safety and performance
- Supports FDA requirements for model transparency in medical devices

**Example:** Heart disease prediction model might initially overlook age-blood pressure interactions that clinicians know are critical. Doctors can edit rules to prioritize these interactions, and CoExplain refines the model while maintaining accuracy.

### Financial Risk Assessment

**Application:** Credit scoring, loan approval, fraud detection, portfolio risk assessment

**How Editable XAI helps:**
- Financial experts can correct biases or introduce domain-specific knowledge about economic conditions
- Regulatory compliance becomes easier when human judgment is explicitly incorporated into decision logic
- Fair lending practices can be enforced by having financial experts audit and refine decision rules

**Compliance benefits:**
- FCRA (Fair Credit Reporting Act): Explains credit decisions
- GDPR Art. 22: Right to explanation and human intervention
- Equal Credit Opportunity Act: Non-discriminatory lending requirements

### Autonomous Systems & Safety-Critical Applications

**Application:** Autonomous vehicle decision-making, industrial safety systems, robotics

**How Editable XAI helps:**
- Safety engineers can enforce hard constraints (e.g., "always prioritize pedestrian safety")
- Domain experts can encode ethical guidelines explicitly into decision rules
- Continuous human oversight through collaborative editing improves trust and safety

### Human Resources & Hiring

**Application:** Resume screening, candidate assessment, promotion decisions

**How Editable XAI helps:**
- HR professionals can audit decisions for potential bias
- Fairness constraints can be explicitly incorporated through rule editing
- Addresses concerns about discriminatory hiring while maintaining predictive performance

### Regulatory Compliance Implications

**GDPR & AI Act Alignment:**
- Supports "right to explanation" by making explanations editable and contestable
- Enables "meaningful human oversight" through collaborative XAI
- Facilitates "accountability and governance" by making decision logic transparent and adjustable

**Practical feasibility:**
- No significant computational overhead for inference; decision tree queries are fast
- Training overhead manageable (model retraining with user-edited rules is feasible)
- User study showed practitioners can effectively edit rules with 3-7 minutes of training

---

## Insights & Implications

### Advancing XAI Philosophy

**Paradigm Shift:** From "AI explains itself to passive users" to "Humans and AI jointly reason about decisions"

Editable XAI represents a fundamental rethinking of the relationship between explanations and user agency. Rather than positioning explanations as one-way communication about fixed model behavior, it opens the possibility of collaborative refinement where both human expertise and statistical learning contribute.

### State-of-the-Art Advancement

**Contributions to the field:**
1. **First practical system** for seamless bidirectional human-AI alignment through editable symbolic rules
2. **Demonstrates feasibility** of maintaining predictive performance while incorporating user expertise
3. **Empirical evidence** (user study) that collaborative XAI is superior to read-only approaches for complex tasks
4. **Novel neural-symbolic architecture** that bridges interpretability and performance

### Broader Implications for Trustworthy AI

**Trust and transparency:**
- Collaborative systems build trust more effectively than one-way explanations
- Transparency increases when users participate in shaping explanations
- Accountability improves when human judgment is explicitly incorporated

**Human-AI collaboration:**
- Challenges the AI-centric view of model improvement (training data, hyperparameters only)
- Opens new possibilities for continuous human feedback integrated into model behavior
- Suggests future XAI systems should be interactive, not just explanatory

### Limitations and Open Questions

**Technical limitations:**
- Symbolic rule expressiveness is limited compared to full neural network capability
- Some nonlinear, high-order feature interactions may be lost in rule distillation
- Scalability to very large models and datasets not yet demonstrated

**Open research questions:**
1. How does Editable XAI scale to transformer-based large language models with billions of parameters?
2. How can we handle cases where user expertise conflicts with statistical patterns in data?
3. What happens when multiple stakeholders (e.g., regulators vs. business interests) disagree on rules?
4. How to measure and ensure the long-term stability of collaboratively edited models?
5. How to prevent adversarial users from exploiting editability to introduce biases?

### Future Research Directions

**Near-term:**
- Extending CoExplain to deep learning models (image classification, NLP tasks)
- Multi-stakeholder collaboration frameworks for XAI rule editing
- Interactive visualization of how user edits affect model predictions

**Medium-term:**
- Integration with regulatory compliance workflows
- Automated bias detection when users propose rules
- Learning human preferences through collaborative interaction patterns

**Long-term:**
- Fully integrated human-AI reasoning systems that learn from user-AI interactions
- Ethical frameworks for incorporating diverse stakeholder perspectives through editable rules
- Mechanistic understanding of when collaborative editing improves vs. harms model robustness

---

## Code & Resources

### Official Implementations

The paper references the CoExplain system but specific GitHub or code repository links are not detailed in the arXiv submission. Researchers interested in implementing or extending the work should:

1. **Check the paper's supplementary materials** on arXiv for any code or implementation details
2. **Contact the authors** directly for code or prototype access:
   - Haoyang Chen
   - Jingwen Bai
   - Fang Tian
   - Brian Y Lim

### Key Dependencies

**Python environment:**
- PyTorch or TensorFlow (for neural networks)
- scikit-learn (for decision tree distillation)
- pandas/numpy (data processing)

**Computational requirements:**
- GPU not strictly required (decision tree queries are fast)
- Training with user-edited rules requires model retraining (GPU acceleration beneficial)
- For study reproduction: standard HCI lab setup with Python backend for rule parsing/evaluation

### Quick Start Guide

**To understand the system:**
1. Read the CHI 2026 paper for complete details
2. Review the user study protocol for implementation of the three interaction modes (Read, Write, Enhance)
3. Study the decision tree distillation methodology to understand neural-symbolic conversion

**To implement or extend:**
1. Start with a simple neural network on one of the benchmark datasets (Adult Income, House Prices)
2. Implement decision tree distillation from the trained model
3. Build rule parser to convert user-written rules to neural network graph equivalents
4. Implement threshold optimization (conservative enhancement) and tree reorganization (aggressive enhancement)
5. Conduct user studies to validate improvements over baseline approaches

### Interactive Visualizations and Demos

[Information not available in arXiv paper — may be available through CHI 2026 conference materials or author websites]

---

## Related Work & Context

### Connections to Core XAI Paradigms

**SHAP and LIME (Local Explanations):**
- Editable XAI differs by providing global, faithful explanations rather than local approximations
- Addresses known problems with SHAP/LIME faithfulness by using decision tree distillation

**Concept-Based Explanations:**
- Similar goal of human-understandable explanations but doesn't address editability
- Editable XAI could be extended to concept-based rules instead of feature-based rules

**Inherently Interpretable Models:**
- Decision trees are inherently interpretable, but Editable XAI adds the neural network's predictive power
- Hybrid approach combines benefits of both interpretable models and deep learning

### Recent Related Work

**Neural-Symbolic Learning:**
- Papers on neurosymbolic AI that integrate symbolic reasoning with neural networks
- Editable XAI advances this field by focusing on human-editable symbolic representations

**Interactive Machine Learning:**
- Active learning systems where humans provide feedback
- Editable XAI differs by specifically focusing on explanation editing as feedback mechanism

**Human-Centered XAI:**
- VirtualXAI, human validation gap research focus on understanding user needs
- Editable XAI takes a step further by enabling users to actively shape explanations

### Relevant XAI Subfields and Connections

1. **Fairness & Interpretability:** Editable rules can explicitly encode fairness constraints
2. **Mechanistic Interpretability:** Understanding neural network internals complements understanding through decision trees
3. **Theoretical Foundations:** Philosophical questions about what "explanation" means; editability reframes this as collaboration
4. **Causal Interpretability:** User-edited rules may encode causal reasoning about feature relationships

### Where This Research Leads

**Immediate implications:**
- Deployment systems for high-stakes decision-making (healthcare, finance) will likely need similar bidirectional alignment capabilities
- Regulatory frameworks may increasingly require human-editable decision logic, not just explanations

**Longer-term vision:**
- Future AI systems may be designed from the start as human-AI collaborative agents
- Machine learning training processes could incorporate explicit human expertise through editable rules rather than only through data annotation
- New evaluation frameworks measuring human-AI team performance rather than model performance alone

---

## Summary

"Editable XAI" represents a significant step forward in making AI systems more trustworthy and aligned with human expertise. By enabling bidirectional human-AI alignment through collaborative rule editing, CoExplain addresses a fundamental gap in current XAI: users' inability to actively shape how AI systems explain and make decisions.

The work is grounded in solid HCI research (user study with 43 participants), demonstrates practical feasibility (56% editing time reduction), and opens new research directions for human-centered AI systems that learn from and adapt to human expertise.

For practitioners, Editable XAI offers a blueprint for XAI systems in regulated industries (healthcare, finance) where human oversight and explicit reasoning are paramount. For researchers, it suggests that the future of XAI may lie not in better post-hoc explanations, but in collaborative human-AI reasoning systems.
