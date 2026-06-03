# Interpretability Can Be Actionable: Shifting Evaluation Criteria in Explainable AI Research

**[ArXiv ID](https://arxiv.org/abs/2605.11161):** 2605.11161  
**Authors:** Hadas Orgad, Fazl Barez, Tal Haklay, Isabelle Lee, Marius Mosbach, Anja Reusch, Naomi Saphra, Byron Wallace, Sarah Wiegreffe, Eric Wong, Ian Tenney, Mor Geva  
**Submitted:** May 11, 2026  
**Subfield:** Actionable Interpretability  
**Keywords:** Evaluation Criteria for Explainable AI, Real-World Impact

---

## Executive Summary

This position paper challenges a fundamental assumption in interpretability research: that explaining neural network behavior is inherently valuable. The authors argue that interpretability research should be evaluated not by methodological novelty, but by **actionability**—the extent to which insights enable concrete decisions and interventions beyond interpretability research itself. The paper identifies critical barriers preventing real-world impact and proposes a framework for actionable interpretability with evaluation criteria aligned with practical outcomes, with specific applications in model editing, safety audits, and representation learning.

---

## Problem Statement

Despite explosive growth in explainable AI (xAI) and interpretability research over the past decade, there is mounting evidence that most of this work has not translated into tangible real-world impact. Interpretability research has become increasingly disconnected from practical applications:

- **Publication-Driven Incentives**: The field incentivizes novel methods and techniques over practical utility. Papers are evaluated on technical contribution and empirical results within narrow benchmarks, not on whether the insights drive meaningful decisions.

- **Misaligned Goals**: Most interpretability papers focus on *explaining* model behavior without considering whether those explanations are sufficiently concrete for actionable use or whether they've been validated through real-world deployment.

- **Validation Gap**: The field lacks a unified framework for evaluating whether interpretability insights actually lead to better outcomes when applied to real problems. Traditional metrics like faithfulness, completeness, or fidelity say little about practical utility.

- **Methodological Limits**: Interpretability methods often fail to generalize beyond their specific settings (e.g., across random seeds, input perturbations, or model architectures), limiting their actionable value for practitioners.

- **The Impact Paradox**: At the ICML 2025 Workshop on Actionable Interpretability, at least 21.8% of submitted papers were explicitly flagged by reviewers as insufficiently actionable—yet these same papers would likely be accepted at mainstream venues.

The central thesis is clear: **the missing ingredient is not better interpretability methods, but a shift in how the field evaluates and incentivizes research. We need evaluation criteria that prioritize actionability over explanation elegance.**

---

## Core Concepts & Theory

### What is Actionable Interpretability?

Actionable interpretability is defined as interpretability that enables concrete decisions and interventions in real-world applications. It differs from traditional interpretability in two critical dimensions:

#### 1. **Concreteness**

A concrete interpretation is one that:
- **Specifies what to change**: Not just "this feature matters" but "adjusting this feature in this way produces this outcome"
- **Is implementable**: The insight can be translated into actionable steps (e.g., model editing, retraining procedures, deployment strategies)
- **Provides clear targets**: Interpretations must identify specific parameters, weights, neurons, or layers that can be modified or monitored
- **Enables intervention**: The explanation should make clear which components of the system can be controlled or adjusted

**Example of non-concrete interpretation**: "The model uses spurious correlations to make predictions" (what does this tell you to do?)  
**Example of concrete interpretation**: "The model's output can be steered by modifying the activation patterns in layer 7, neurons 42-56, which encode spurious features. Masking these features during inference reduces dataset bias by 23%"

#### 2. **Validation**

An actionable interpretation requires validation that the proposed action actually achieves its intended outcome:
- **Intervention testing**: Does modifying the identified component actually change the model's behavior as predicted?
- **Outcome measurement**: Does the intervention improve performance on metrics that matter (accuracy, fairness, safety, generalization)?
- **Generalization evidence**: Do insights hold across different seeds, input distributions, model sizes, or architectures?
- **User validation**: Do practitioners actually find the interpretation useful and act on it?

---

### The Actionability Framework

The paper proposes evaluating interpretability research along these two dimensions:

| Dimension | Question | Example |
|-----------|----------|---------|
| **Concreteness** | Does the interpretation specify what to change and how? | "Boost this neuron to improve toxicity detection" ✓ vs. "The model relies on semantic features" ✗ |
| **Validation** | Does changing the identified component actually work? | Empirical tests showing intervention effectiveness ✓ vs. Claims without validation ✗ |

**Benchmark Integration**: Rather than evaluating interpretability methods in isolation, performance should be measured against practical ML baselines (prompting, fine-tuning, standard approaches) using domain-specific metrics (accuracy, safety benchmarks, audit passing rates, etc.).

---

## Main Ideas & Key Contributions

### 1. **Redefining the Evaluation Paradigm for Interpretability**

The paper's core contribution is a fundamental shift in how interpretability research should be evaluated:

**Traditional Approach** (still dominant):
- Novel method + Empirical validation on XAI benchmarks = Publication
- Success = High faithfulness scores, novel technical approach, explanation quality

**Proposed Approach** (actionable interpretability):
- Concrete insight + Real-world validation + Measurable outcome = Valuable research
- Success = Whether practitioners use insights to make better decisions, whether it improves real-world systems

This is not about dismissing interpretability—it's about holding interpretability research to a higher standard: **does it actually help?**

### 2. **Identification of Five Domains Where Interpretability Drives Actionable Outcomes**

The paper identifies specific application domains where interpretability has proven or can prove genuinely actionable:

#### **Domain 1: Model Editing & Feature Steering**
- **Application**: Modifying model behavior without full retraining
- **Concrete methods**: Using mechanistic insights (e.g., MLP key-value stores, sparse autoencoders, cross-attention patterns) to surgically edit model parameters
- **Example**: Disabling specific toxic features identified through interpretability to reduce harmful outputs
- **Validation**: Testing that edits achieve intended behavior change without unintended side effects

#### **Domain 2: Safety & Security Auditing**
- **Application**: Identifying safety risks and vulnerabilities in deployed systems
- **Concrete methods**: Activating specific attention patterns to probe for hidden capabilities, analyzing internal representations for deceptive behaviors
- **Example**: Anthropic's safety audit of Claude using internal activation analysis
- **Validation**: Confirming that identified risks correlate with observed unsafe behaviors

#### **Domain 3: Representation Finetuning**
- **Application**: Improving model generalization and robustness through interpretability-informed design
- **Concrete methods**: Modifying learned representations based on insights into what the model learns
- **Example**: Steering feature learning away from dataset artifacts identified through mechanistic analysis
- **Validation**: Demonstrating improved performance on out-of-distribution data or robustness benchmarks

#### **Domain 4: Data Quality & Curation**
- **Application**: Identifying and fixing training data issues through model behavior analysis
- **Concrete methods**: Using interpretability to diagnose why models fail on specific examples
- **Example**: Discovering that spurious features in training data drive model errors
- **Validation**: Showing that data fixes improve performance on held-out test sets

#### **Domain 5: Regulatory Compliance & Governance**
- **Application**: Meeting legal and regulatory requirements for AI explainability
- **Concrete methods**: Demonstrating that model decisions satisfy regulatory criteria (GDPR transparency, AI Act requirements, FDA standards)
- **Example**: Using mechanistic interpretability to prove that a medical diagnosis system doesn't rely on protected attributes
- **Validation**: Documented evidence that interpretability requirements are met and maintained

### 3. **Analysis of Barriers to Actionable Interpretability**

The paper identifies systematic barriers preventing the field from achieving actionability:

**Barrier 1: Incentive Misalignment**
- Academic publications reward technical novelty over impact
- Reviewers rarely penalize papers for lacking real-world validation
- The metrics that matter for publication (faithfulness scores, complexity) often don't correlate with actionability

**Barrier 2: Methodological Fragmentation**
- Interpretability insights often fail to generalize across:
  - Random seeds (results are brittle)
  - Model architectures (insights specific to one architecture)
  - Model scales (what's true for small models may not be true for large models)
  - Input distributions (findings on one dataset may not transfer)
- This fragmentation makes it impossible for practitioners to trust interpretability findings for real applications

**Barrier 3: Deployment Challenges**
- Even when interpretability insights are concrete, integrating them into production systems is challenging
- Sparse autoencoders, circuit analysis, and other mechanistic methods are computationally expensive
- The field lacks standardized tools and APIs for practitioners to implement interpretability-based interventions

**Barrier 4: Expertise Requirements**
- Actionable interpretability often requires deep technical knowledge (understanding transformers, mechanistic circuits, SAE activation patterns)
- This limits adoption by practitioners without specialized expertise
- There's a gap between what researchers can interpret and what practitioners can understand and act on

**Barrier 5: Evaluation Methodology**
- The field uses weak proxies for real-world impact (faithfulness metrics, user studies on toy problems)
- There's no standardized way to evaluate whether interpretability actually improves outcomes
- Success metrics vary widely across papers, making it impossible to compare approaches

---

## Methodology & Implementation

### How Actionable Interpretability is Evaluated

Rather than proposing a single new interpretability method, the paper establishes a framework for evaluating any interpretability approach:

#### **Step 1: Concreteness Assessment**
- [ ] Does the interpretation identify specific, modifiable components of the system?
- [ ] Can a practitioner act on the interpretation without additional interpretation?
- [ ] Are there clear implementation instructions or code?
- [ ] Can the interpretation be translated into engineering decisions?

#### **Step 2: Implementation & Validation**
- [ ] Is the proposed intervention implementable given computational constraints?
- [ ] Does the intervention achieve its stated goal (validated empirically)?
- [ ] Does the intervention generalize across:
  - [ ] Different random seeds?
  - [ ] Different model sizes?
  - [ ] Different architectures?
  - [ ] Different input distributions?
- [ ] Are there unintended side effects?

#### **Step 3: Comparative Evaluation**
- [ ] How does the interpretability-based intervention compare to simpler baselines?
  - [ ] Prompting?
  - [ ] Fine-tuning?
  - [ ] Existing engineering solutions?
- [ ] Is the added complexity of interpretability justified by improved outcomes?

#### **Step 4: Real-World Deployment**
- [ ] Has the approach been tested in real deployment scenarios?
- [ ] Do practitioners actually use the interpretability insights?
- [ ] Is there measurable impact on business/safety/performance metrics?
- [ ] Is the approach maintainable and updatable?

### Case Studies: Where Interpretability Succeeded

The paper provides examples of genuinely actionable interpretability:

**Case Study 1: Sparse Autoencoders for Feature Steering**
- **Interpretability Finding**: Sparse autoencoders can disentangle learned features into interpretable components
- **Action Taken**: Use SAE features as intervention targets for model steering
- **Validation**: Demonstrated that steering via SAE features can control specific behaviors (truthfulness, toxicity, knowledge)
- **Real-World Impact**: Being integrated into mechanistic interpretability workflows

**Case Study 2: Mechanistic Circuit Analysis for Model Editing**
- **Interpretability Finding**: Specific attention heads and MLP weights are responsible for particular behaviors
- **Action Taken**: Surgically edit these components to change model behavior
- **Validation**: Tested across multiple models and behaviors (toxicity, gender bias, knowledge control)
- **Real-World Impact**: Used in production systems for behavior modification

**Case Study 3: Safety Auditing via Activation Analysis**
- **Interpretability Finding**: Hidden capabilities can be detected through internal activation patterns
- **Action Taken**: Proactively identify and mitigate hidden or unsafe behaviors before deployment
- **Validation**: Demonstrated correlation between activation patterns and unsafe behaviors
- **Real-World Impact**: Deployed in safety evaluation pipelines for large language models

---

## Practical Applications & Real-World Use Cases

### 1. **Healthcare & Medical AI**
**Challenge**: Clinicians need to understand why a diagnosis recommendation is made for regulatory compliance (FDA, clinical oversight)

**Actionable Interpretability**: Rather than just explaining which features the model considered, provide specific:
- Patient characteristics that drove the decision
- Evidence-based reasoning grounded in medical literature
- Confidence calibration showing when the model is uncertain
- Actionable recommendations for clinicians to verify findings

**Real-World Impact**: Interpretability insights used to validate diagnostic recommendations against clinical knowledge and to flag edge cases requiring human review

---

### 2. **Finance & Credit Decisions**
**Challenge**: Fair lending regulations (FCRA, ECOA, CRA) require explainability for credit decisions

**Actionable Interpretability**: Beyond attribution scores, provide:
- Specific factors affecting creditworthiness
- Changes required for applicants to improve scores
- Evidence that model doesn't use protected attributes
- Audit trails for regulatory compliance

**Real-World Impact**: Interpretability findings used to ensure regulatory compliance and improve model fairness through targeted interventions

---

### 3. **Safety-Critical Autonomous Systems**
**Challenge**: Self-driving vehicles must explain safety-critical decisions (object detection, path planning)

**Actionable Interpretability**: Rather than post-hoc explanations, use interpretability to:
- Identify which features drive safety decisions
- Detect and correct for dataset biases (e.g., overrepresentation of highway scenarios)
- Stress-test model robustness in corner cases
- Validate that safety constraints are actually learned

**Real-World Impact**: Interpretability-driven testing catches safety vulnerabilities before deployment

---

### 4. **Content Moderation at Scale**
**Challenge**: Content moderation systems must explain why content was removed (user appeals, policy documentation)

**Actionable Interpretability**: Shift from general explanations to:
- Identifying specific harmful content patterns the model detected
- Generating targeted feedback for content creators
- Auditing model decisions for consistency and bias
- Steering the model to reduce false positives

**Real-World Impact**: Reduced false positives, improved user trust, faster appeals resolution

---

### 5. **AI Alignment & Control**
**Challenge**: As AI systems become more capable, we need mechanisms to ensure alignment with human values

**Actionable Interpretability**: Use mechanistic interpretability to:
- Identify and steer values-relevant features in large language models
- Detect deceptive or reward-gaming behaviors
- Modify learned goals to align with human preferences
- Audit alignment through safety-critical behavior tests

**Real-World Impact**: Interpretability becomes a critical tool for long-term AI safety and alignment

---

### Regulatory & Compliance Implications

**GDPR (General Data Protection Regulation)**
- Requires "explanation" of algorithmic decisions affecting individuals
- Actionable interpretability satisfies this by identifying actual factors influencing decisions
- Enables "right to explanation" through concrete, understandable interpretations

**AI Act (EU)**
- Requires "transparency" and "explainability" for high-risk AI systems
- Actionable interpretability translates abstract transparency into verifiable safety properties
- Supports conformity assessments and audits

**FDA Regulations**
- Requires interpretability for medical AI devices
- Actionable interpretability enables clinicians to understand and verify recommendations
- Supports clinical validation and post-market surveillance

---

## Insights & Implications

### What This Paper Reveals About the State of Interpretability Research

1. **The Field Is Adrift**: The disconnect between interpretability publications and real-world impact is structural, not incidental. The academic incentive structure actively discourages actionability.

2. **Method Proliferation Without Validation**: The field has developed dozens of interpretability techniques (LIME, SHAP, attention visualization, sparse autoencoders, circuit analysis) but rarely validates whether they help practitioners.

3. **Generalization is Harder Than We Thought**: Many interpretability findings are brittle—they don't hold across seeds, scales, or architectures. This fragility makes them unsuitable for real-world deployment.

4. **Interpretability ≠ Control**: Understanding a model doesn't automatically mean you can change it. The paper emphasizes that actionability requires both explanation AND a mechanism for intervention.

### Broader Implications for Trustworthy AI

**Implication 1: Trustworthiness Through Intervention**
Traditional approaches to AI trustworthiness focus on post-hoc auditing and evaluation. Actionable interpretability flips this: trustworthiness comes from the ability to intervene and control AI systems, not just explain them.

**Implication 2: Interpretability as Infrastructure**
Rather than treating interpretability as an add-on academic field, the paper argues it should be core infrastructure in AI development. Like testing, documentation, and version control, interpretability should be embedded in the development pipeline.

**Implication 3: The Rise of Mechanistic Interpretability**
For interpretability to be actionable, it must enable interventions. This requires mechanistic understanding (sparse autoencoders, circuit analysis) rather than post-hoc attribution methods. The field should invest more heavily in mechanistic approaches.

**Implication 4: Towards Interpretability Engineering**
Just as software engineering is distinct from computer science, there's a need for "interpretability engineering"—the discipline of designing systems that are interpretable by construction, with clear intervention mechanisms built in.

---

## Limitations & Open Questions

### Limitations of Actionable Interpretability Framework

1. **Incomplete Metrics**: The paper identifies two dimensions (concreteness and validation) but doesn't specify quantitative metrics for assessing them. How do we measure "concreteness"? What constitutes sufficient validation?

2. **Domain Specificity**: The framework may not apply equally across all AI domains. Fairness auditing has clearer metrics than artistic AI applications.

3. **Computational Cost**: Actionable interpretability (especially mechanistic approaches like sparse autoencoders) is computationally expensive. The paper doesn't adequately address scalability to billion-parameter models.

4. **Generalization Across Scales**: While the paper emphasizes generalization, achieving it is extremely difficult. Insights about small models (100M parameters) often fail for large models (70B+ parameters).

5. **User-Centric Evaluation**: The paper calls for validation through user action but provides limited guidance on how to conduct these evaluations. What counts as evidence of "actionability"?

---

### Open Research Questions

1. **How do we identify interventions systematically?** Once we understand a model, how do we efficiently discover which modifications achieve desired outcomes?

2. **Can interpretability scale to frontier models?** Current mechanistic interpretability methods don't scale well to very large models. How can we make mechanistic understanding tractable?

3. **How do we handle interpretability-accuracy tradeoffs?** Sometimes the most actionable interpretation (simple rules) is less accurate than black-box predictions. How should practitioners navigate this?

4. **How do we standardize "actionability"?** Different domains need different actionability standards. Can we develop generalizable criteria?

5. **What is the relationship between interpretability and robustness?** Does understanding a model make it more robust? Does interpretability help with out-of-distribution generalization?

---

## Code & Resources

### Official Resources

- **arXiv Paper**: https://arxiv.org/abs/2605.11161
- **PDF**: https://arxiv.org/pdf/2605.11161
- **HTML Version**: https://arxiv.org/html/2605.11161v1

### Related Mechanistic Interpretability Tools & Libraries

**Sparse Autoencoder Training & Analysis**
- [Anthropic's SAE Lens](https://github.com/jbloomAus/SAELens) - Tools for training and interpreting sparse autoencoders in language models
- [Neel Nanda's SAE Research](https://github.com/neelnanda-io/sae_vis) - SAE visualization and analysis tools
- [OpenAI's Transformer Circuits Library](https://github.com/OpenAI/transformer-circuits) - For circuit discovery and analysis

**Model Editing & Intervention**
- [ROME (Rank-One Model Editing)](https://github.com/kmeng01/rome) - Efficient model editing through identified parameter updates
- [Mechanistic Knobs](https://github.com/cybershiptrooper/mlr-probing-language-models) - Feature steering via sparse autoencoder activations
- [AlphaPave SAE Steering](https://github.com/anthropics/alignment-research-dataset) - Model control through SAE feature steering

**Circuit Analysis & Mechanistic Interpretation**
- [Neel Nanda's Circuit Analysis](https://github.com/neelnanda-io/TransformerLens) - TransformerLens library for mechanistic interpretability
- [Tracing and Attribution](https://github.com/redwoodresearch/interp) - Tools for activation tracing and attribution

### Relevant Research Surveys & Position Papers

- "Locate, Steer, and Improve" (arXiv:2601.14004) - Comprehensive survey on actionable mechanistic interpretability
- "Interpretability without Actionability" (arXiv:2603.18353) - Discusses the gap between understanding and intervention
- "From Insights to Actions" (arXiv:2406.12618) - Analysis of interpretability research impact on NLP

---

## Related Work & Context

### How This Paper Positions Within xAI Research

**Traditional xAI Approaches** (LIME, SHAP, attention visualization):
- **Strength**: Provide intuitive, human-understandable explanations
- **Limitation**: Often fail to enable concrete interventions; high computational cost; stability issues under distributional shift
- **This paper's critique**: These methods optimize for explanation quality, not actionability

**Mechanistic Interpretability** (circuit analysis, sparse autoencoders):
- **Strength**: Enable concrete, model-specific interventions; reveal actual computational mechanisms
- **Limitation**: Computational expense; limited scalability; requires deep technical expertise
- **This paper's contribution**: Positions mechanistic interpretability as the path toward actionable understanding

**Concept-Based Methods** (concept activation vectors, concept bottleneck models):
- **Strength**: Bridge between human concepts and model internals
- **Limitation**: Concept selection is subjective; requires labeled concept datasets
- **This paper's perspective**: Actionable interpretability often requires concept-based understanding combined with mechanistic access

### Related Position Papers & Critiques

**"Interpretability without Actionability" (arXiv:2603.18353)**
- Argues that mechanistic interpretability alone isn't sufficient for control
- Shows that even perfect internal representations don't guarantee actionable interventions
- Complements this paper by identifying intervention failure modes

**"Actionable Interpretability Must Be Defined in Terms of Symmetries" (arXiv:2601.12913)**
- Proposes that actionability should be mathematically grounded in symmetry principles
- Suggests frameworks for systematically identifying intervenable components

**"Locate, Steer, and Improve" (arXiv:2601.14004)**
- Practical survey of current actionable mechanistic interpretability methods
- Categorizes research into localization (finding relevant components) and steering (intervention)
- Demonstrates real applications of actionable interpretability in LLMs

### Broader xAI Research Directions

**Shift Toward Engineering**:
- Move from interpretability as academic research toward interpretability as engineering discipline
- Integration of interpretability into development pipelines and deployment processes

**Fusion of Mechanistic & Concept-Based Approaches**:
- Combining circuit analysis (mechanistic) with human-understandable concepts
- Using sparse autoencoders to identify human-relevant features automatically

**Interpretability for Safety & Alignment**:
- Recognition that interpretability is critical for long-term AI safety
- Use of mechanistic interpretability as a tool for value alignment and control

---

## Key Takeaways

1. **Interpretability ≠ Actionability**: A clear explanation of what a model does is not the same as being able to change its behavior or outcomes.

2. **Two Dimensions Matter**: Actionable interpretability requires both *concreteness* (identifying what to change) and *validation* (proving the change works).

3. **Barriers Are Structural**: The field's disconnect from real-world impact isn't due to lack of methods—it's due to misaligned incentives and fragmented evaluation criteria.

4. **Five Domains Show Promise**: Model editing, safety auditing, representation learning, data curation, and regulatory compliance have proven or potential for actionable interpretability.

5. **Mechanistic Interpretability is Essential**: Post-hoc attribution methods alone cannot achieve actionability; mechanistic understanding (sparse autoencoders, circuits) is necessary for real intervention.

6. **The Field Needs Evaluation Standards**: Without standardized metrics and benchmarks for actionability, the field will continue to optimize for the wrong objectives.

7. **This is a Call to Action**: For researchers and practitioners, this paper argues for a fundamental shift in how we approach, evaluate, and fund interpretability research—from academic rigor to practical impact.

---

## Sources & Further Reading

- [arXiv:2605.11161 - Interpretability Can Be Actionable](https://arxiv.org/abs/2605.11161)
- [arXiv:2601.14004 - Locate, Steer, and Improve: Practical Survey of Actionable Mechanistic Interpretability](https://arxiv.org/abs/2601.14004)
- [arXiv:2603.18353 - Interpretability without Actionability](https://arxiv.org/abs/2603.18353)
- [arXiv:2601.12913 - Actionable Interpretability Must Be Defined in Terms of Symmetries](https://arxiv.org/abs/2601.12913)
- [arXiv:2404.14082 - Mechanistic Interpretability for AI Safety: A Review](https://arxiv.org/abs/2404.14082)
- ICML 2025 Workshop on Actionable Interpretability: https://sites.google.com/view/actionable-interp-icml25/home
