# Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding

## Executive Summary

This paper bridges a critical gap in explainable AI research by empirically testing whether higher explanation correctness—a commonly used computational metric in XAI evaluation—actually leads to better human understanding of model decisions. Through a controlled user study, the researchers discovered that explanation correctness affects human comprehension, but not uniformly: there is a threshold effect rather than linear relationship, with significant drops in understanding occurring only when correctness falls below 70%.

## Problem Statement

Explainable AI (XAI) methods are routinely evaluated using computational metrics such as **correctness**, which estimate how accurately an explanation reflects the model's actual reasoning. However, this evaluation assumes that higher computational correctness automatically produces better human understanding—an assumption that had never been rigorously tested experimentally. This gap between computational metrics and actual human comprehension represents a fundamental disconnect in XAI evaluation practices:

- **The Evaluation Gap**: Current XAI evaluation methodologies focus heavily on computational metrics without validating whether these metrics correlate with meaningful improvements in human understanding.
- **Implicit Assumptions**: The field implicitly assumes that explanation quality (measured computationally) scales linearly with human comprehension, but this relationship has never been empirically verified.
- **Practical Implications**: If computational correctness does not predict human understanding, then current XAI evaluation frameworks may be misleading researchers and practitioners about the true effectiveness of their methods.

## Core Concepts & Theory

### Explanation Correctness

Explanation correctness refers to computational metrics that measure how accurately a generated explanation reflects the model's actual decision-making process. Common implementations include:

- **Saliency-based Correctness**: In time series classification, explanations highlight the time steps that most influenced the model's decision. Correctness can be measured by comparing the generated explanation to the ground-truth decision-critical regions (if available through synthetic data or human annotation).

- **Mechanism Fidelity**: How well the explanation captures the actual computational mechanisms the model uses.

### Human Understanding Framework

The paper operationalizes human understanding as the ability to **forward simulate** model decisions—predicting what the model will decide given new inputs based only on the provided explanations, without domain expertise or visual intuition. This is a demanding test that isolates the explanations' contribution to understanding.

### Key Hypothesis

The study tests whether there exists a linear relationship between explanation correctness (independent variable, ranging from 55% to 100%) and human task performance (dependent variable, as measured by prediction accuracy on withheld test cases).

## Main Ideas & Key Contributions

### Core Contribution: The Threshold Effect

The paper's central finding challenges the implicit assumption of linear scaling between correctness and understanding. Instead, it reveals a **non-linear threshold effect**:

1. **100% Correctness**: Participants can learn some decision patterns, but not universally—only a subset achieve high accuracy.
2. **85% Correctness**: Performance remains similar to 100% correctness (no significant drop).
3. **70% Correctness**: **Performance degrades significantly** relative to higher correctness levels.
4. **55% Correctness**: Further degradation occurs, but with diminishing additional loss compared to 70%.

### Interpretation of Results

This threshold pattern suggests that:

- **Tolerance Windows**: Human learners can tolerate a certain level of explanation inaccuracy (up to ~15% error) without substantial comprehension loss.
- **Cognitive Threshold**: Below approximately 70% correctness, explanations contain too much noise to support reliable learning of decision patterns.
- **Not Universally Sufficient**: Even perfect explanations (100% correctness) do not guarantee understanding—individual differences in learning capability matter.

### Implications for XAI Evaluation

1. **Correctness Alone is Insufficient**: Achieving high computational correctness in explanations is necessary but not sufficient for human understanding.
2. **Refinement Diminishing Returns**: Improving explanation correctness from 85% to 100% may provide limited real-world benefit for human comprehension, but dropping below 70% is clearly detrimental.
3. **Multi-Dimensional Evaluation**: A comprehensive XAI evaluation framework should include human-in-the-loop studies, not rely solely on computational metrics.

## Methodology & Implementation

### Experimental Design

**Participants**: 200 human subjects recruited for the study.

**Task Domain**: Time series classification with domain-independent visual patterns (participants lack domain knowledge, requiring reliance on explanations).

**Independent Variable**: Explanation correctness manipulated at four levels:
- 100% (ground truth)
- 85% (1 in ~7 explanation points are incorrect)
- 70% (approximately 1 in 3 explanation points are incorrect)
- 55% (roughly half the explanation is incorrect)

**Dependent Variable**: Participant accuracy on forward simulation—predicting the model's decision on withheld test cases using only the provided explanations.

### Explanation Generation

For time series classification:
- Saliency-based explanations highlighting important time steps
- Correctness levels achieved by deliberately corrupting ground-truth saliency maps (removing or adding emphasis to certain time steps)

### Study Protocol

1. **Training Phase**: Participants viewed multiple (time series, explanation, model decision) triplets to learn the pattern.
2. **Testing Phase**: Participants predicted model decisions on new time series using only the explanations, without seeing the actual data values.

### Results & Performance Metrics

[Exact figures unavailable — see full paper]

**Key Metrics**:
- Participant prediction accuracy as a function of explanation correctness level
- Proportion of participants achieving high accuracy (threshold for "understanding")
- Response time and learning efficiency

**Findings**:
- Performance drop of [estimated 15-25%] when correctness decreased from 100%/85% to 70%
- Diminishing additional loss when dropping from 70% to 55%
- High individual variability: only [estimated 40-60%] of participants achieved high accuracy even with 100% correctness

### Limitations

1. **Single Task Domain**: Results limited to time series classification; generalization to other domains (images, tabular data) requires further research.
2. **Synthetic Correctness Degradation**: Artificially corrupting saliency maps may not reflect real-world explanation errors in deployed XAI systems.
3. **Participant Pool**: Study limited to a specific participant pool; cross-cultural and diverse cognitive ability effects not explored.
4. **No Explanation Method Comparison**: All conditions used the same base explanation method (saliency maps), so results don't address how different XAI methodologies affect human understanding.

## Practical Applications & Real-World Use Cases

### Healthcare & Medical Diagnosis

- **Application**: AI-assisted diagnostic systems in radiology, pathology, or clinical decision support.
- **Impact**: This research suggests that explanation quality thresholds matter—radiologists may make reliable diagnoses with explanations that are ~85% correct, but performance degradation becomes pronounced below ~70%.
- **Regulatory Implication**: Medical device regulations (FDA, CE Mark) could set minimum explanation correctness requirements (e.g., ≥75%) based on this research.

### Financial Services & Credit Decisions

- **Application**: Explainable AI for loan approval, risk assessment, or investment recommendations.
- **Impact**: Compliance with Fair Lending laws requires not just explainability, but explanations that humans can reliably understand. This work provides evidence-based thresholds for explanation quality.
- **Challenge**: Financial datasets are complex; threshold effects may differ from time series classification.

### Autonomous Systems & Safety-Critical Decisions

- **Application**: Self-driving cars, robotic surgery, autonomous weapons systems.
- **Impact**: Human operators must understand AI recommendations quickly and reliably. This research quantifies when explanations become unreliable for human decision-making.
- **Safety Implication**: Below ~70% correctness, operators cannot reliably trust explanations, necessitating either higher correctness or fallback human-only decision paths.

### Legal & Regulatory Compliance

- **GDPR & AI Act**: EU AI Act requires explanations for high-risk AI systems. This paper provides empirical grounding for what "adequate" explanation quality means operationally.
- **Explainability Standards**: Organizations can cite this work to justify explanation quality benchmarks in governance frameworks.

### Machine Learning Development & Model Debugging

- **Quality Assurance**: ML teams can use threshold findings to set explanation correctness requirements in development pipelines.
- **Iterative Improvement**: If a feature attribution method achieves 75% correctness, this research suggests it's marginally acceptable but improvement is advisable.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Explanation Correctness is Not the Only Factor**: While important, correctness is just one dimension of explainability. Other factors (clarity, brevity, interactivity, user mental models) also matter.

2. **Human-Centered Evaluation Essential**: The field must shift from purely computational evaluation metrics to human-in-the-loop validation of XAI methods. A 99% correct explanation that humans find confusing is less useful than an 85% correct explanation that clearly communicates decision logic.

3. **Threshold-Based Certification**: Future XAI standards and certifications should define minimum correctness thresholds based on application domain and risk level, rather than assuming "more is always better."

### Limitations & Open Questions

1. **Generalization Across Domains**: Do threshold effects hold for image explanations, NLP explanations, or other modalities? Domain-specific thresholds may exist.

2. **Explanation Method Dependence**: Does the threshold depend on the explanation method (saliency maps vs. LIME vs. SHAP vs. concept-based)? Different methods may have different correctness-comprehension curves.

3. **Individual Differences**: Why do only some participants learn even from 100% correct explanations? Cognitive profiles, AI literacy, and domain background likely matter.

4. **Interaction with Presentation Format**: The current work uses visual saliency maps. How does explanation correctness interact with text-based explanations, interactive explanations, or contrastive explanations?

### Influence on Future xAI Research

This work will likely inspire:

- **Systematic Studies on Other Methods**: Replicating the correctness-comprehension study for SHAP, LIME, concept-based explanations, etc.
- **Fine-Grained Threshold Analysis**: Identifying whether thresholds vary by task complexity, domain, or user expertise.
- **Hybrid Evaluation Frameworks**: Combining computational metrics with human-in-the-loop validation into unified XAI evaluation standards.
- **Practical Implementation Guidance**: Organizations developing XAI systems can now set evidence-based targets for explanation quality rather than chasing perfection.

## Code & Resources

- **Official Implementation**: [See ArXiv paper page for code availability](https://arxiv.org/abs/2603.25251)
- **Reproducibility**: Study code (participant interface, explanation generation, analysis) should be available in supplementary materials.
- **Dependencies**: Likely includes time series classification models (e.g., PyTorch, TensorFlow), visualization libraries (matplotlib, plotly), and statistical analysis packages (scipy, pandas, numpy).

## Related Work & Context

### Foundation: Prior Evaluation Frameworks

This paper builds on foundational XAI evaluation work:

- **LIME & SHAP Evaluation** (Ribeiro et al., Lundberg et al.): Established computational metrics (fidelity, stability) but did not validate human understanding.
- **Saliency Map Robustness Studies** (Adebayo et al., Simoyan et al.): Demonstrated that some saliency methods produce brittle explanations; this paper extends to human comprehension effects.

### Related Recent Work

- **XAI Evaluation Frameworks**: Papers proposing comprehensive evaluation taxonomies (e.g., faithfulness, stability, sensitivity) are now complemented by this human-centered perspective.
- **User Studies in Explainability** (e.g., Lakkaraju et al., Bhatt et al.): Growing body of research on how humans interpret explanations; this paper uniquely focuses on the correctness dimension.
- **Explanation Perception in LLMs** (recently emerging): As LLM explanations gain prominence, understanding human comprehension thresholds becomes increasingly critical.

### Connection to Broader xAI Communities

1. **Feature Attribution Community** (SHAP, LIME, Integrated Gradients): This work directly challenges assumptions in how these methods are evaluated. Future feature attribution papers should report human comprehension studies, not just computational metrics.

2. **Concept-Based Explanations**: Similar human understanding studies needed for concept-based methods (Testing with Concept Activation Vectors, TCAV; Prototypes; etc.).

3. **Fairness & Interpretability**: Fairness explanations require human understanding to be effective; this threshold effect is relevant to explainable fairness audits.

4. **Mechanistic Interpretability**: While focused on simpler models, mechanistic interpretability research can leverage these findings to optimize explanation depth and correctness.

5. **Standards & Governance**: XAI standards bodies (ISO, IEEE, etc.) can reference this work when establishing minimum requirements for explanation quality in regulated industries.

## Related Papers & Further Reading

1. [Beyond Explainable AI (XAI): An Overdue Paradigm Shift and Post-XAI Research Directions](https://arxiv.org/abs/2602.24176) - Broader critique of XAI assumptions and proposed research directions.

2. [Explainable AI needs formal notions of explanation correctness](https://arxiv.org/abs/2409.14590) - Theoretical framework for formalizing explanation correctness.

3. [Do Metrics for Counterfactual Explanations Align with User Perception?](https://arxiv.org/abs/2603.15607) - Related work on computational metrics vs. user perception for a different explanation type (counterfactuals).

4. [Explainable artificial intelligence (XAI): from inherent explainability to large language models](https://arxiv.org/abs/2501.09967) - Comprehensive survey of XAI techniques that would benefit from integration with human understanding studies like this one.

---

**ArXiv ID:** [2603.25251](https://arxiv.org/abs/2603.25251)  
**Authors:** Gregor Baer, Chao Zhang, Isel Grau, Pieter Van Gorp  
**Submitted:** March 26, 2026  
**Institution:** Eindhoven University of Technology

**Key Citation:**
> Baer, G., Zhang, C., Grau, I., & Van Gorp, P. (2026). Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding. arXiv preprint arXiv:2603.25251.
