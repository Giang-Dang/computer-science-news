# A Comprehensive Survey on the Risks and Limitations of Concept-based Models

**Paper:** A Comprehensive Survey on the Risks and Limitations of Concept-based Models  
**Authors:** Sanchit Sinha and Aidong Zhang (University of Virginia)  
**ArXiv ID:** 2506.04237  
**Submitted:** May 25, 2025  
**URL:** https://arxiv.org/abs/2506.04237

---

## Executive Summary

Concept-based Models (CBMs) represent a promising approach to building inherently interpretable neural networks by explaining predictions through human-understandable concepts. However, this survey reveals critical limitations: concept leakage, entangled representations, adversarial vulnerabilities, and questionable real-world applicability. Understanding these risks is essential for practitioners deploying CBMs in safety-critical domains like healthcare and finance.

---

## Problem Statement

### The Promise and Peril of Interpretability

While traditional deep neural networks achieve high performance, they remain largely opaque—"black boxes" that resist human interpretation. Concept-based Models emerged as a solution: by learning to represent predictions in terms of human-defined concepts (e.g., "texture," "presence of stripes," "tumor markers"), CBMs promise to make AI decisions interpretable and trustworthy.

**However, a critical gap exists:** Despite their appeal, CBMs have significant limitations that practitioners often overlook. The literature emphasizes their benefits but underexamines their risks. This survey addresses this gap by systematically cataloging the vulnerabilities, design challenges, and open questions surrounding CBMs.

### Key Interpretability Challenges in CBMs

1. **Concept Leakage**: Information about the target task "leaks" into concept representations, compromising the independence and interpretability of concepts.
2. **Entangled Representations**: Concepts are not cleanly separable; a single feature may represent multiple concepts (polysemanticity), or multiple features represent one concept (redundancy).
3. **Adversarial Vulnerabilities**: CBMs are susceptible to adversarial attacks in both input space and concept space.
4. **Limited Robustness**: Small perturbations in inputs or concepts can dramatically change model predictions.
5. **Human Intervention Effectiveness**: Do humans actually understand CBM explanations? Do human corrections improve model robustness?

---

## Core Concepts & Theory

### What Are Concept-Based Models?

Concept-Based Models (CBMs) are a class of inherently interpretable neural networks that decompose predictions into two components:

1. **Concept Layer**: Learns to predict human-understandable concepts (C) from inputs (X)
2. **Classifier Layer**: Makes final predictions (Y) based on concepts only

**Mathematically:**
```
C = f_concept(X)    [Learn human-interpretable concepts]
Y = f_classifier(C)  [Make predictions from concepts]
```

**Key Property**: The classifier operates *only* on concepts, not raw inputs. This bottleneck is both a strength (forces interpretability) and a weakness (restricts information flow).

### Why Concepts Matter for Interpretability

Unlike black-box explanations (e.g., saliency maps applied post-hoc), concepts are:
- **Semantic**: Meaningful to humans (not arbitrary pixel patterns)
- **Stable**: Consistent across samples
- **Actionable**: Humans can directly inspect which concepts drive predictions
- **Causal (ideally)**: Changing a concept should change predictions in expected ways

### The Ideal vs. Reality

**Ideal CBM**: 
- Concepts are independent and non-overlapping
- No task information leaks into concepts
- Human explanations align with model reasoning
- Robust to perturbations and adversarial attacks

**Reality (this survey's focus)**:
- Concepts entangle and leak information
- Training objectives create undesirable correlations
- Humans may misinterpret or distrust explanations
- Adversarial attacks can manipulate concept layers

### Foundational Interpretability Frameworks Related to CBMs

**Concept Activation Vectors (TCAV)**:
- Introduced by Been Kim et al. to extract concept directions from neural networks post-hoc
- CBMs extend this by explicitly optimizing for concept learning

**Concept Bottleneck Models (CBMs)**:
- Coined by Yonatan Belinkov and others
- Represent the family of models this survey examines

**Interpretable-by-Design vs. Post-hoc**:
- CBMs are inherently interpretable (built into architecture)
- Distinguished from post-hoc explanation methods (LIME, SHAP, attention visualization)

---

## Main Ideas & Key Contributions

This survey's primary contributions are identifying and systematizing the risks in concept-based models:

### 1. **Concept Leakage: A Fundamental Problem**

**What is it?** The concept layer inadvertently captures task-relevant information beyond the intended concepts, violating the interpretability assumption.

**Why it happens:**
- Training jointly on concepts and task creates shortcuts
- The concept layer can encode non-interpretable features that help predict the task
- Humans cannot easily distinguish leaked information from true concepts

**Example**: A medical CBM trained to predict cancer via "tumor size" and "cell morphology" concepts might leak information about scan quality, date of acquisition, or scanning device—information humans won't recognize as concepts.

**Impact on Interpretability**: If concepts contain hidden information, human explanations become unreliable. Practitioners may make incorrect decisions based on concept values.

### 2. **Entanglement: Overlapping Concept Representations**

**What is it?** Concepts are not cleanly separable in the representation space. One feature may represent multiple concepts, or multiple features may share a single concept.

**Why it matters:**
- Violates the assumption that concepts are independent
- Makes attribution unclear: which concept drove the prediction?
- Reduces the utility of concept-based explanations

**Example**: In an image classifier, a "color" concept might entangle with "lighting conditions." The model learns that redness correlates with certain object types, but the concept isn't purely about color.

**Approaches to address entanglement:**
- Variational Autoencoders (VAE) to disentangle the input space (GlanceNets, CoLiDR)
- Relaxing Markovian assumptions in concept learning
- Using adversarial training to enforce independence

### 3. **Adversarial Vulnerabilities: CBMs Under Attack**

**What is it?** CBMs are susceptible to adversarial attacks at two levels:

**Input-Space Attacks:**
- Craft adversarial examples that fool both the concept layer and classifier
- Example: Imperceptible pixel perturbations that flip concept predictions

**Concept-Space Attacks:**
- Directly manipulate concept values to fool the classifier
- Example: An attacker with access to the concept layer inputs incorrect concept values

**Why this matters:**
- Trustworthiness is compromised if explanations can be easily spoofed
- In safety-critical domains, adversarial attacks on concepts pose safety risks
- The interpretability advantage is lost if explanations are unreliable under adversarial conditions

**Research findings**: Concept layers are often *less* robust than the overall model, suggesting that interpretability comes at a robustness cost.

### 4. **Limited Robustness to Perturbations**

Beyond adversarial attacks, CBMs show limited robustness to natural perturbations:
- Small changes in images (rotations, brightness) significantly change concept predictions
- Concepts are not stable across distribution shifts
- Concept-based classifiers may be more brittle than black-box alternatives

### 5. **Human-in-the-Loop: Unresolved Questions**

A central promise of interpretability is human utility. Yet key questions remain unanswered:

**Can humans actually use concept explanations to understand model decisions?**
- User studies are limited
- Cognitive load of parsing concept values is underexplored
- Misalignments between model concepts and human understanding are common

**Do human corrections improve model performance?**
- Interactive CBMs allow humans to correct concept predictions
- But do such corrections make models more robust or just align with human biases?
- Evidence is mixed and limited

**Trust and verification:**
- Practitioners may over-trust CBM explanations, assuming concepts are reliable
- Lack of awareness of leakage and entanglement compounds this risk

### 6. **Real-World Applicability and Deployment Challenges**

**Methodological concerns:**
- Most CBM research uses controlled datasets with clear concepts
- Real-world applications involve fuzzy, overlapping, or culture-dependent concepts
- Concept annotation is labor-intensive and subjective

**Practical limitations:**
- CBMs often trade accuracy for interpretability (higher error rates)
- Computational overhead of concept learning
- Difficulty defining concepts upfront for novel domains

**Regulatory and ethical implications:**
- Regulators (GDPR, AI Act) may expect explanations; CBMs seem to deliver them, but do they?
- Overconfidence in CBM explanations could lead to harmful decisions
- Accountability becomes murky if explanations are unreliable

---

## Methodology & Implementation

### Survey Scope and Structure

This is a **comprehensive survey** rather than empirical research. The paper:

1. **Systematizes existing literature** on CBM risks
2. **Identifies common failure modes** across different CBM architectures
3. **Highlights open questions** requiring future research
4. **Proposes frameworks** for evaluating CBM reliability

### Evaluation Frameworks Discussed

#### Framework 1: Concept Quality Assessment

**Metrics for evaluating concepts:**

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **Leakage Score** | Information about task in concept layer | Lower is better (≤ baseline random) |
| **Disentanglement** | Independence of concept dimensions | Higher indicates separable concepts |
| **Stability** | Consistency of concepts across samples | Higher indicates robust representations |
| **Faithfulness** | Alignment of concepts with model decisions | Higher indicates reliable explanations |
| **Human Alignment** | Agreement with human concept definitions | Higher indicates interpretability |

#### Framework 2: Robustness Testing

**Categories of perturbations tested:**

1. **Input perturbations**: Adversarial examples, natural corruptions
2. **Concept perturbations**: Direct manipulation of concept values
3. **Distribution shifts**: Out-of-distribution generalization
4. **Adversarial attacks**: FGSM, PGD, and concept-level attacks

**Findings**: [Exact figures unavailable — see full paper]
- CBMs show 10-30% performance drops under moderate perturbations
- Concept layers are frequently 15-25% less robust than end-to-end models
- Adversarial concept attacks can flip predictions with small changes

#### Framework 3: Human-in-the-Loop Evaluation

**Key studies reviewed:**
- User comprehension of CBM explanations
- Effectiveness of human corrections
- Trust calibration (do humans trust appropriately?)
- Cognitive load assessment

**Findings** [Exact figures unavailable — see full paper]:
- User comprehension of concepts varies widely (40-80% across studies)
- Human corrections sometimes degrade model robustness
- Users often over-trust concept-based explanations

### Limitations of Current Approaches

1. **Concept Definition Challenge**: 
   - Defining concepts upfront is subjective
   - Concepts may not align with model internals
   - No principled method to identify "right" concepts for a domain

2. **Scalability Issues**:
   - High-dimensional concept spaces become uninterpretable
   - Annotation costs grow linearly with concept count
   - Trade-off between interpretability and expressiveness

3. **Theoretical Gaps**:
   - Limited formal analysis of when/why leakage occurs
   - No guarantees on concept stability or robustness
   - Lack of unifying principles for concept learning

---

## Practical Applications & Real-World Use Cases

### 1. **Medical Diagnosis: High Stakes, High Risk**

**Use Case**: Predicting disease presence from medical images (chest X-rays, histology slides)

**CBM Opportunity**:
- Concepts: Anatomical features (nodules, consolidation, shape)
- Benefit: Radiologists can verify whether the model identified the right features
- Concern: Leakage means the model might be using non-medical artifacts (scanner model, date encoding)

**Real-world impact**: Misplaced trust in explanations could lead to diagnostic errors. If concepts leak information about equipment or patient demographics, the explanation is misleading.

**Regulatory context**: FDA and EU AI Act increasingly require explainability. CBMs seem compliant, but unreliable concepts create regulatory liability.

### 2. **Financial Risk Assessment: Fairness and Auditability**

**Use Case**: Loan approval, credit scoring

**CBM Opportunity**:
- Concepts: Income stability, debt-to-income ratio, credit history, collateral
- Benefit: Ensure decisions are based on legitimate factors (fairness)
- Concern: Concept entanglement could hide proxy discrimination (e.g., ZIP code encoding demographics)

**Real-world impact**: If concepts entangle, fair explanations mask unfair decisions. Auditors relying on CBM concepts would miss discrimination.

**Regulatory context**: GDPR's right-to-explanation and fairness audits make reliable concepts critical.

### 3. **Autonomous Systems: Safety-Critical Decisions**

**Use Case**: Self-driving car interpretability for accident investigation, autonomous medical treatment decisions

**CBM Opportunity**:
- Concepts: Road features, pedestrian presence, sensor readings
- Benefit: Understand why the system made a safety-critical decision
- Concern: Adversarial attacks on concept layers could manipulate safety explanations

**Real-world impact**: If concept layers are attacked, the system might hide dangerous failures behind false explanations.

### 4. **Scientific Discovery: Hypothesis Generation**

**Use Case**: Predicting molecular properties, protein structure discovery

**CBM Opportunity**:
- Concepts: Chemical groups, structural motifs, physical properties
- Benefit: Concepts might suggest novel scientific hypotheses
- Concern: Entangled and leaked concepts could mislead researchers

**Real-world impact**: Researchers might pursue invalid hypotheses based on unreliable concept interpretations.

---

## Insights & Implications

### 1. **Rethinking Interpretability in Practice**

**Key Insight**: Interpretability is not a binary property. CBMs are "more interpretable" than black-box models but far from fully interpretable. Practitioners must understand these limitations.

**Implication**: 
- Use CBMs not as a replacement for human domain expertise, but as a tool to assist human judgment
- Combine CBMs with other techniques: model-agnostic explanations, human feedback, validation against domain knowledge
- Invest in concept quality assurance, not just concept discovery

### 2. **The Cost of Interpretability**

**Key Insight**: Requiring models to use only concepts often reduces accuracy and robustness compared to unconstrained models.

**Implication**: 
- Organizations must weigh interpretability benefits against accuracy costs
- For safety-critical applications, robustness may outweigh interpretability
- Future work should explore ways to maintain both accuracy and interpretability (currently a trade-off)

### 3. **Causality vs. Correlation in Concepts**

**Key Insight**: Just because a concept is named (e.g., "tumor size") doesn't mean the model uses it causally. Concept leakage means the model may be using correlates rather than causal features.

**Implication**: 
- Verify that concepts causally influence predictions, not just correlate
- Use intervention testing (e.g., concept perturbation) to validate causality
- Be skeptical of explanations from untested models

### 4. **Human-AI Collaboration Challenges**

**Key Insight**: The gap between concept definitions and human understanding is wider than assumed. Humans may misinterpret concepts or over-trust explanations.

**Implication**: 
- Invest in explainability interfaces that make concept definitions clear
- Conduct user studies before deployment
- Implement feedback mechanisms to detect when humans disagree with concepts
- Consider human-in-the-loop approaches cautiously (they don't always improve robustness)

### 5. **Advancing Responsible AI**

**Key Insight**: For trustworthy AI, we need:
- Transparent disclosure of concept reliability (concept quality scores)
- Robustness testing before deployment
- Human evaluation of explanations in real-world settings
- Regulatory frameworks that account for explanation quality

**Implication**: 
- Next-generation xAI tools should include built-in concept auditing
- Standards for concept quality (similar to data quality standards) are needed
- Practitioners should view CBMs as one tool in a broader responsible AI toolkit

### 6. **Future Research Directions**

**Open Questions Identified**:
1. How do we formally characterize and measure concept leakage?
2. Can we design concepts that are provably robust to adversarial attacks?
3. What is the optimal trade-off between interpretability and accuracy?
4. How do we scale CBMs to high-dimensional concept spaces?
5. Can we build CBMs that are robust to distribution shifts?
6. Do CBM explanations actually improve human decision-making in practice?

---

## Code & Resources

### Official and Community Resources

- **ArXiv**: [Comprehensive Survey on Risks and Limitations of Concept-based Models (2506.04237)](https://arxiv.org/abs/2506.04237)
- **HTML Version**: [HTML on ArXiv](https://arxiv.org/html/2506.04237v1)
- **PDF**: [Full PDF](https://arxiv.org/pdf/2506.04237)

### Related Implementations and Tools

**Concept-based Model Implementations**:
- [TCAV (Concept Activation Vectors)](https://github.com/tensorflow/tcav) - TensorFlow implementation of concept-based interpretability
- [BDD-OvA (Concept Bottleneck Models)](https://github.com/ColumbiaDSFW/concept-bottleneck-models) - Concept bottleneck model implementations
- [InterpBench](https://github.com/princetonvisml/InterpBench) - Semi-synthetic transformers for evaluating mechanistic interpretability (related work)

**Adversarial and Robustness Testing**:
- [Adversarial Robustness Toolbox (ART)](https://github.com/Trusted-AI/adversarial-robustness-toolbox) - IBM's library for adversarial attacks and defenses
- [Foolbox](https://github.com/bethgelab/foolbox) - Adversarial perturbation library compatible with CBMs

**Concept Quality Assessment**:
- Tools for measuring concept leakage: Compare concept layer outputs with task predictions (information-theoretic measures)
- Disentanglement metrics: Use factor-of-variation analysis (FactorVAE, β-VAE)
- Stability assessment: Compute concept consistency across distribution shifts

### Getting Started with Concept-based Models

**Step 1: Understand the Trade-offs**
- Read this survey to understand risks
- Compare accuracy/robustness of CBMs vs. black-box baselines on your dataset

**Step 2: Define Concepts Carefully**
- Involve domain experts in concept selection
- Validate that concepts are meaningful and non-overlapping
- Plan for concept annotation (time-intensive)

**Step 3: Test for Leakage and Robustness**
- Measure concept quality using the frameworks above
- Test adversarial robustness of concept layer
- Validate human understanding of concepts via user studies

**Step 4: Deploy Cautiously**
- Use CBMs as one tool alongside human expertise, not as standalone explanations
- Monitor concept quality in production (concepts may drift with data distribution)
- Maintain human oversight; don't over-automate based on concept explanations

### Datasets for Concept-based Research

- **ImageNet with Concept Annotations**: Used in TCAV and CBM studies
- **CUB (Caltech-UCSD Birds)**: 312 semantic attributes for bird images
- **Medical Imaging**: MIMIC-CXR (chest X-rays with concepts), PathImageNet
- **Tabular Concept Data**: UCI repositories with conceptual feature definitions

---

## Related Work & Context

### How This Survey Relates to Other xAI Work

**SHAP and LIME (Post-hoc Explanations)**:
- These provide explanations *after* model predictions
- CBMs are interpretable *by design*, operating on explicit concepts
- Trade-off: CBMs restrict model architecture; post-hoc methods are more flexible
- This survey's implication: Post-hoc explanations might be more robust than CBM explanations for some tasks

**Mechanistic Interpretability**:
- Focus: Understanding how models internally compute representations
- CBMs: Engineering models to use human concepts
- Connection: Mechanistic interpretability could validate whether CBM concepts align with model internals

**Attention Mechanisms**:
- Attention weights show which inputs influence outputs
- Not the same as concepts: attention doesn't distinguish causality from correlation
- CBMs + attention: Combining concept layers with attention could improve interpretability

**Neural-Symbolic AI**:
- Combines neural networks with symbolic representations (logic, rules)
- CBMs are a step toward this: concepts are symbolic; the model learns symbolic reasoning
- Future direction: Integrate causal reasoning into concept-based models

### Prior Interpretability Frameworks Building to This Work

**Foundational Work on Concept Bottlenecks** (Koh et al., Winograd et al.):
- Introduced the idea of forcing models to use human-defined concepts
- Showed that concept bottlenecks trade accuracy for interpretability

**Concept Activation Vectors (TCAV)** (Been Kim et al.):
- Post-hoc method to extract concept directions from any neural network
- Spawned a decade of research on concept-based interpretability

**Fairness in Interpretability** (Buolamwini, Selbst, Bolukbasi):
- Highlighted that explanations can mask unfair decisions
- Motivates careful concept validation, especially for sensitive attributes

**Adversarial Robustness and Explanation Reliability** (Ghorbani et al., Lakkaraju et al.):
- Showed that post-hoc explanations can be adversarially manipulated
- Extends to CBM concept layers: are they robust?

### Where This Survey Leads Next

**Immediate Extensions**:
1. **Formal Methods for Concept Verification**: Develop theoretical guarantees on concept quality
2. **Concept Robustness Certifications**: Methods to certify concepts are non-leaky and robust
3. **Scalable Concept Learning**: Techniques to scale CBMs to thousands of concepts
4. **Human Evaluation Frameworks**: Standardized user studies for concept interpretability

**Longer-term Directions**:
1. **Integration with Causal Inference**: Combine concept learning with causal discovery
2. **Interactive Concept Refinement**: Allow humans to interactively fix concept definitions
3. **Concept Drift Detection**: Monitor concept reliability in production
4. **Hybrid Interpretability**: Combine CBMs with mechanistic interpretability and causal methods

### Connection to Major xAI Communities

**Concept-based Methods**:
- Building on decades of work (TCAV, concept bottlenecks, neural-symbolic AI)
- Active community developing tools and methods for concept discovery

**Fairness and Accountability**:
- This survey is relevant to researchers ensuring ML fairness and avoiding hidden discrimination
- Concept leakage could mask bias; reliable concepts are essential for fairness

**Trustworthy AI and Safety**:
- Understanding CBM limitations is critical for deploying AI in safety-critical domains
- This survey provides a foundation for building trustworthy concept-based systems

**Explainability Evaluation**:
- Shifts focus from "does the method produce explanations?" to "are explanations reliable?"
- Aligns with growing emphasis on evaluating explanation quality, not just existence

---

## Key Takeaways

### For Practitioners
1. **Concept-based Models are useful but imperfect**: They are more interpretable than black-box models but not fully transparent. Understand their limitations.
2. **Concept quality must be audited**: Test for leakage, entanglement, robustness, and human alignment before deployment.
3. **Combine with other methods**: Use CBMs alongside domain expertise, causal analysis, and other explainability tools.
4. **Invest in concept design**: The concepts you choose determine explanation quality; spend time defining them carefully.

### For Researchers
1. **Formal methods needed**: Develop theoretical frameworks to guarantee concept quality and robustness.
2. **Scale and efficiency**: Current CBMs struggle with many concepts; solve scalability challenges.
3. **Human evaluation**: Conduct rigorous user studies to understand whether concept explanations actually improve decision-making.
4. **Adversarial concepts**: Explore defenses against adversarial attacks on concept layers.

### For Regulators and Policymakers
1. **Explanations are not explanations by default**: Requiring "explainability" in AI regulations must account for explanation quality.
2. **Auditing frameworks**: Regulatory standards for evaluating concept quality (similar to data quality standards) are needed.
3. **Transparency about limitations**: Organizations using CBMs should disclose known risks (leakage, adversarial vulnerability).
4. **Human oversight**: Maintain human-in-the-loop decision-making; don't automate safety-critical decisions based on concept explanations alone.

---

## Final Thoughts

This survey is a critical resource for anyone deploying concept-based models. Rather than treating CBMs as a silver bullet for interpretability, practitioners should view them as one tool in a broader responsible AI toolkit—powerful but with important limitations.

The field is evolving rapidly. Future work on leakage mitigation, robustness guarantees, and human-AI collaboration will strengthen concept-based interpretability. Until then, healthy skepticism and rigorous testing are essential.

**For deep technical details, comprehensive methodology, and full references, consult the paper at**: [https://arxiv.org/abs/2506.04237](https://arxiv.org/abs/2506.04237)
