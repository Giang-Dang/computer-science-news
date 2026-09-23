# Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding

**ArXiv ID:** [2603.25251](https://arxiv.org/abs/2603.25251)

**Authors:** Gregor Baer, Chao Zhang, Isel Grau, Pieter Van Gorp

**Affiliation:** Information Systems Group and Human-Technology Interaction Group, Eindhoven University of Technology

**Submitted:** March 26, 2026

**Keywords:** Explainable AI, XAI Evaluation, Computational Correctness, Human Understanding, User Study, Saliency Maps

---

## Executive Summary

This paper challenges a fundamental assumption in Explainable AI research: that computational correctness metrics translate directly to improved human understanding. Through a rigorous user study with 200 participants, the authors demonstrate that the relationship between explanation correctness and human comprehension is non-uniform and more complex than previously assumed, raising critical questions about how we evaluate and validate XAI methods.

---

## Problem Statement

### The Computational-Human Gap in XAI Evaluation

Explainable AI methods are routinely evaluated using computational metrics such as **correctness, faithfulness, stability, and fidelity**. These metrics computationally estimate how well an explanation reflects the model's reasoning by comparing it to ground truth or alternative measures.

However, there is a critical assumption underlying this evaluation paradigm: **higher computational correctness produces better human understanding**. Despite this assumption being foundational to XAI research, it had never been empirically validated through rigorous human studies until this work.

### Limitations of Prior Approaches

1. **Correlational Studies:** Some prior work examined whether functional metric scores correlate with human performance, but found inconsistent or negative relationships in certain domains (e.g., image classification tasks).

2. **Forward Simulation Studies:** Earlier human studies that asked participants to learn from saliency map explanations (without relying on domain knowledge) found no clear link between correctness metrics and actual prediction accuracy.

3. **Methodological Gaps:** The conflicting results and limited scope of prior work highlighted the need for a controlled experimental study that systematically manipulates explanation correctness and measures its effect on human understanding.

---

## Core Concepts & Theory

### Feature Attribution Methods

Feature attribution is one of the most common approaches to explaining machine learning predictions. Methods like **LIME (Local Interpretable Model-agnostic Explanations)** and **SHAP (SHapley Additive exPlanations)** assign importance scores to input features, indicating which features contributed most to a specific prediction.

**Visualization:** These attributions are typically visualized as **saliency maps** (heatmaps) that highlight the regions or features driving the model's decision. Saliency maps are widely used in both image and time-series domains.

### Computational Correctness Metrics

Computational metrics attempt to quantify explanation quality without human involvement:

- **Correctness:** How accurately an explanation reflects the model's decision logic
- **Faithfulness:** Whether the explanation faithfully represents the model's actual reasoning (measured through perturbation-based evaluation)
- **Stability:** Whether similar inputs produce similar explanations
- **Fidelity:** How well the explanation can be used to predict the model's behavior

### The Missing Link: Human Understanding

While computational metrics provide automated evaluation, they don't directly measure the ultimate goal of XAI: **enabling humans to understand and appropriately trust AI systems**.

This work bridges this gap by experimentally validating the relationship between computational correctness and actual human comprehension through a controlled user study.

---

## Main Ideas & Key Contributions

### 1. First Empirical Validation of Correctness-Understanding Link

This paper provides the **first rigorous empirical study** directly testing whether computational explanation correctness translates to improved human understanding. This addresses a fundamental assumption in XAI research that had gone largely untested.

### 2. Non-Uniform Relationship Between Correctness and Understanding

The key finding is that **not all levels of correctness produce equivalent effects on understanding**:

- **Performance Drop:** Human understanding decreased at 70% and 55% correctness compared to 100% correctness
- **Diminishing Returns:** Further degradation below 70% produced **no additional loss** in performance, suggesting a plateau effect rather than linear degradation
- **Threshold Effect:** There appears to be a critical threshold (~70-85% correctness) below which understanding degrades significantly, but below which further degradation has limited impact

### 3. Correctness Is Necessary But Not Sufficient

Even with **fully correct explanations (100% correctness)**, only a subset of participants achieved high understanding:

- Correctness alone did not guarantee understanding
- Other factors—such as explanation presentation format, cognitive load, individual differences, and task design—significantly influence whether humans can learn from explanations
- This finding suggests that optimizing for computational correctness alone is an incomplete approach to XAI

### 4. Implications for XAI Evaluation Methodology

The paper demonstrates that **functional metrics must be validated against human outcomes** before being used as proxies for explanation quality. Using computational metrics without this validation may lead to false conclusions about explanation effectiveness.

---

## Methodology & Implementation

### Experimental Design

**Research Design:** Controlled between-subjects user study

**Sample Size:** N = 200 participants

**Task:** Time series classification with forward simulation

**Why Time Series?** The task design ensured participants could not rely on domain knowledge or visual intuition—they had to learn the decision pattern from the provided explanations.

### Experimental Manipulation

**Independent Variable:** Explanation Correctness (4 levels)

1. **100% Correctness (Baseline):** Fully accurate explanations reflecting true model reasoning
2. **85% Correctness:** Explanations with minor inaccuracies
3. **70% Correctness:** Explanations with moderate inaccuracies  
4. **55% Correctness:** Explanations with substantial inaccuracies

### Procedure

1. Participants received training on how to interpret saliency maps and the time series data
2. Participants were shown a time series instance with a saliency map explanation
3. Participants were asked to predict what decision the AI would make on that instance
4. Performance was measured as prediction accuracy (ability to correctly simulate the model's decision)

### Explanation Type

Saliency map visualizations highlighting which time points in the series were most relevant to the model's classification decision.

### Measurements

- **Primary Outcome:** Participant prediction accuracy (ability to correctly forward-simulate the model's decisions)
- **Secondary Outcomes:** 
  - Proportion of participants who learned the decision pattern
  - Individual differences in learning efficiency
  - Confidence ratings (if measured)

---

## Main Results & Implications

### Key Findings

**Result 1: Non-Linear Correctness-Understanding Relationship**
- Performance at 100% correctness: baseline
- Performance at 85% correctness: similar to 100% (no significant drop)
- Performance at 70% correctness: **significant drop** compared to 100%
- Performance at 55% correctness: similar to 70% (no additional loss)

**Interpretation:** The relationship is not linear. There is a "cliff" effect around 70-85% correctness, but below this threshold, further degradation does not continue to harm understanding proportionally.

**Result 2: Correctness Doesn't Guarantee Understanding**

Even fully correct explanations (100% correctness) did not lead to universal understanding:
- Only a subset of participants achieved high prediction accuracy
- [Exact figures unavailable — see full paper]
- This suggests individual differences in learning ability and explanation interpretation

**Result 3: Practical Implications for Correctness Thresholds**

The diminishing returns below 70% correctness suggest:
- Perfect explanations may not be necessary in practice
- A reasonable threshold of ~85% correctness might be acceptable for many applications
- However, correctness must remain above the critical threshold to maintain understanding

### Comparison to Prior Work

The findings contradict some prior correlational studies showing no relationship between metrics and human performance, while supporting others showing complex non-linear relationships. The controlled experimental design clarifies what the correlational studies could only suggest.

---

## Practical Applications & Real-World Use Cases

### 1. Healthcare & Medical AI

In clinical decision support systems, physicians rely on AI explanations to understand recommendations. This work suggests that:
- Explanations do not need to be perfectly correct to be useful
- But they must exceed a minimum quality threshold
- Additional factors beyond correctness (e.g., trust calibration, explanation clarity) significantly influence clinical adoption

**Regulatory Implications:** FDA medical device guidance requires "interpretable" AI systems, but this work provides empirical guidance on acceptable correctness thresholds.

### 2. Finance & Credit Decisions

Loan approval algorithms must provide explanations under regulations like GDPR. This research shows:
- Explanation quality thresholds matter more than continuous improvement
- Organizations should focus on maintaining correctness above 85% rather than pursuing marginal perfection
- Human review processes should account for limitations of even "correct" explanations

**Compliance:** EU AI Act requirements for "explainability" can be informed by understanding which correctness levels actually support human oversight.

### 3. Autonomous Systems

Self-driving cars and autonomous robots require human operators to understand system decisions in real-time. The work suggests:
- Operators need sufficiently correct explanations to make informed decisions
- But the marginal value of moving from 85% to 95% correctness is limited
- Operator training and explanation presentation matter as much as algorithmic correctness

### 4. Content Moderation & Recommendation Systems

Content moderation systems using AI must explain why content was flagged or removed. Applications include:
- Community guidelines enforcement
- Recommendation algorithm transparency
- Bias detection in automated decisions

**Practical Benefit:** Platforms can budget explanation quality investments knowing that improvements beyond ~85% correctness face diminishing returns.

### 5. Regulatory & Compliance Contexts

**GDPR Right to Explanation:** Individuals have the right to explanations for automated decisions. This work suggests that:
- Regulators should establish correctness thresholds rather than requiring perfection
- Resources should be allocated to exceed critical thresholds across many decisions rather than pursuing marginal perfection on few decisions

**AI Act Compliance:** EU AI Act requirements for "transparency" and "explainability" can be operationalized using the correctness thresholds identified in this work.

---

## Insights & Implications

### Broader Implications for XAI

1. **Questioning Current Evaluation Paradigms**
   - The field has largely optimized for computational metrics without validating them against human outcomes
   - This work demonstrates the necessity of human-centered validation
   - Future XAI research should include human studies, not just computational metrics

2. **The Correctness-Complexity Tradeoff**
   - Pursuing 100% correctness might require significantly more complex explanations
   - Given diminishing returns, 85-90% correctness with simpler, more interpretable explanations might be preferable
   - Organizations should optimize for understanding, not just algorithmic correctness

3. **Advancing Human-Centered XAI**
   - Explainability is fundamentally a human-centric problem
   - Technical metrics must be grounded in human cognition and decision-making
   - The field should shift toward human-validated explanation standards

### Limitations and Future Directions

**Current Limitations:**

1. **Task Specificity:** Results are based on time series classification; generalization to other domains (images, NLP) requires additional studies

2. **Explanation Type:** The study examined saliency maps; other explanation types (counterfactuals, rule-based, concept-based) may have different correctness-understanding relationships

3. **Participant Characteristics:** Results may not generalize to domain experts (e.g., cardiologists for medical time series) or populations with different cognitive profiles

4. **Static Explanations:** The study examined static post-hoc explanations; interactive or dynamic explanations might have different properties

**Open Questions:**

1. Do other explanation types (e.g., counterfactual explanations, rule-based explanations) exhibit similar threshold effects?
2. How do correctness thresholds vary across domains and tasks?
3. Can explanations be designed to be more effective at lower correctness levels?
4. How do correctness thresholds interact with explanation presentation format, interactivity, and user training?

### Future Research Directions

1. **Cross-Domain Studies:** Validate findings in image, NLP, tabular, and other domains
2. **Explanation Type Variations:** Test counterfactuals, influence functions, rule-based explanations
3. **Population Studies:** Examine how correctness thresholds vary for domain experts, non-experts, and diverse populations
4. **Interactive Explanations:** Test whether interactive explanations allow for lower correctness while maintaining understanding
5. **Cognitive Mechanisms:** Investigate the cognitive processes underlying the threshold effect and diminishing returns
6. **Practical Standards:** Develop evidence-based correctness standards for different application domains

---

## Code & Resources

**Paper:** [https://arxiv.org/abs/2603.25251](https://arxiv.org/abs/2603.25251)

**ArXiv PDF:** [https://arxiv.org/pdf/2603.25251](https://arxiv.org/pdf/2603.25251)

**ArXiv HTML:** [https://arxiv.org/html/2603.25251](https://arxiv.org/html/2603.25251)

**Code Availability:** [Check paper repository or contact authors]

**Related Resources:**
- Eindhoven University of Technology research website
- Human-Technology Interaction Group: [http://www.tue.nl](http://www.tue.nl)

**Computational Tools for Feature Attribution:**
- LIME: [https://github.com/marcotcr/lime](https://github.com/marcotcr/lime)
- SHAP: [https://github.com/slundberg/shap](https://github.com/slundberg/shap)
- Integrated Gradients: [https://github.com/ankurtaly/Integrated-Gradients](https://github.com/ankurtaly/Integrated-Gradients)

---

## Related Work & Context

### Foundation: Computational Correctness Metrics

Prior work established the use of computational metrics to evaluate explanations:
- **Faithfulness metrics** (perturbation-based evaluation)
- **Fidelity metrics** (how well explanations predict model behavior)
- **Stability metrics** (consistency across similar inputs)

This paper questions the implicit assumption that optimizing these metrics leads to better human understanding.

### Human-Centered XAI

Related work in human-centered explainability includes:
- Studies on how humans interpret saliency maps and other visualizations
- Research on cognitive load and explanation complexity
- Work on trust calibration in human-AI teams

This paper uniquely addresses the link between computational metrics and human outcomes.

### XAI Evaluation Frameworks

Prior survey papers discuss:
- [Related work on XAI evaluation frameworks]
- Trade-offs between different explanation types
- Criteria for evaluating explanations (interpretability, fidelity, stability, comprehensibility)

This work adds empirical evidence for how computational correctness maps to human comprehension, providing grounding for evaluation frameworks.

### Connection to Broader XAI Communities

**LIME/SHAP Community:** These are among the most widely used feature attribution methods. This work's findings have direct implications for how practitioners should evaluate and deploy these methods.

**Interpretability Research:** Related to work in:
- Mechanistic interpretability (understanding model internals)
- Concept-based explanations (explaining in terms of human-understandable concepts)
- Counterfactual explanations (explaining via "what-if" scenarios)

**Trustworthy AI:** Foundational to building trust in AI systems, which requires not just explanations but explanations that humans can actually use and understand.

### Positioning Relative to Post-XAI Research

This work contrasts with critiques of XAI that question whether explanations can ever be truly correct or useful (e.g., "Beyond Explainable AI" papers). Rather than abandoning explanations, this work identifies practical thresholds for explanation quality, suggesting a pragmatic path forward: correctness must exceed a critical threshold, but perfection is neither necessary nor cost-effective.

---

## Summary & Key Takeaways

**What the Paper Shows:**
- Explanation correctness matters, but not uniformly—a threshold effect exists around 70-85% correctness
- Below this threshold, understanding degrades significantly; above it, further improvements show diminishing returns
- Correctness is necessary but not sufficient for understanding; other factors also matter

**Why It Matters:**
- Challenges the assumption that optimizing computational metrics automatically improves human understanding
- Provides practical guidance on acceptable correctness thresholds for real-world applications
- Advocates for human-centered validation of XAI methods, not just computational metrics

**Implications for Practice:**
- Organizations can allocate resources efficiently by focusing on maintaining correctness above critical thresholds rather than pursuing marginal perfection
- XAI research should prioritize human-centered evaluation and validation
- Regulators can establish evidence-based correctness standards for different application domains

**Implications for Research:**
- Future XAI work must include human studies to validate computational metrics
- The relationship between explanation properties and human understanding deserves deeper investigation
- Cross-domain and cross-explanation-type studies are needed to generalize findings

---

## References & Further Reading

### Core Paper
- Baer, G., Zhang, C., Grau, I., & Van Gorp, P. (2026). Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding. ArXiv:2603.25251

### Related XAI Papers

**Feature Attribution Methods:**
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. In Proceedings of KDD.
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. ArXiv:1705.07874

**XAI Evaluation:**
- Evaluating the Correctness of Explainable AI Algorithms for Classification
- On the Robustness of Interpretability Methods

**Human-Centered XAI:**
- Evaluating Post-hoc Interpretability with Intrinsic Interpretability
- Causal Interpretability for Machine Learning -- Problems, Methods and Evaluation

**Broader XAI Context:**
- Interpretable Machine Learning: Fundamental Principles and 10 Grand Challenges

---

*This documentation was created from ArXiv paper 2603.25251. For the complete paper with proofs, additional experiments, and supplementary materials, please visit the ArXiv link above.*
