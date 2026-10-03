# Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding

**ArXiv ID:** [2603.25251](https://arxiv.org/abs/2603.25251)  
**Authors:** Gregor Baer, Chao Zhang, Isel Grau, Pieter Van Gorp  
**Submitted:** March 26, 2026

**Research Institution:** University collaboration  

## Executive Summary

This empirical study challenges a fundamental assumption in explainable AI: that higher computational correctness of explanations automatically leads to better human understanding of AI model decisions. Through a rigorous user study with 200 participants manipulating explanation correctness at multiple levels, the paper reveals a nuanced and non-linear relationship between explanation correctness and human comprehension, demonstrating that current XAI evaluation metrics may not reliably predict human understanding outcomes.

## Problem Statement

### The Assumption-Reality Gap in XAI Evaluation

Explainable AI (XAI) methods are routinely evaluated using computational metrics such as **correctness**, **fidelity**, and **faithfulness**, which measure how accurately an explanation reflects the model's actual decision-making process. The field implicitly assumes a causal link: that higher correctness automatically translates to better human understanding and more informed decision-making.

However, this critical assumption has never been rigorously tested with controlled levels of correctness variation. The gap between computational evaluation and human outcomes represents a fundamental blind spot in XAI research:

- **Computational metrics** measure algorithmic properties in isolation
- **Human understanding** depends on cognitive factors, prior knowledge, presentation format, and individual differences
- **No empirical validation** exists linking these two domains quantitatively

### Limitations in Prior Approaches

Previous research has acknowledged the importance of human-centered evaluation but has not systematically isolated the effect of explanation correctness while controlling for other variables. Additionally:

1. **Functional metrics assumed reliable**: Researchers optimize XAI methods for computational metrics without verifying they align with human outcomes
2. **No ground truth for unsupervised problem**: The inherent unsupervised nature of XAI makes validation challenging
3. **Methodological limitations**: Earlier human studies typically tested single correctness levels rather than exploring the relationship continuously
4. **Domain-specific confounds**: Previous studies often involved domain experts with specialized knowledge, limiting generalizability

## Core Concepts & Theory

### Explanation Correctness and Faithfulness

**Definition**: Correctness (also called *faithfulness* or *fidelity*) captures how accurately an explanation reflects the model's true reasoning process.

**Key Distinction**:
- **Correct Explanation** (100%): Perfectly represents how the model makes decisions
- **Partially Correct Explanation** (70%, 85%): Contains errors or omissions
- **Lowest Tested Correctness** (55%): The lowest correctness condition used in this study

### The Forward Simulation Framework

The study employs **forward simulation** as the human understanding task: participants receive an AI model's explanation and must predict the model's decision on unseen instances **without relying on domain knowledge or visual intuition**.

This approach isolates the effect of explanation quality from domain expertise, making it a rigorous test of whether explanations actually convey the model's decision logic.

### Theoretical Foundations

The research builds on three key theoretical perspectives:

1. **Cognitive Fidelity Theory**: How well an explanation captures mental models of system behavior (Norman, 1988)
2. **Information Processing Theory**: Human capacity to process and integrate explanation information
3. **Explanation and Learning Theory**: How explanation correctness affects knowledge acquisition and mental model formation

### The Correctness-Understanding Relationship

The paper tests whether this relationship is:
- **Linear**: Each percentage point of correctness loss uniformly reduces understanding
- **Threshold-based hypothesis**: Effects may emerge after inaccuracies exceed a tolerance level; this study does not locate that level precisely
- **Non-monotonic**: Other factors interact with correctness in complex ways

## Main Ideas & Key Contributions

The study tests whether functional explanation correctness predicts human understanding. Correctness is manipulated at 100%, 85%, 70%, and 55%, while understanding is measured through forward simulation.

Accuracy is lower at 70% and 55% than with fully correct explanations. The comparison between 85% and 100% is inconclusive, and reducing correctness from 70% to 55% does not establish an additional decline. This is consistent with a threshold pattern, but does not locate a precise threshold.

Fully correct explanations also produce a bimodal distribution of understanding. Some participants accurately predict decisions while describing the wrong rule, showing why a single measure of understanding is incomplete.

## Methodology & Implementation

The between-participants study has 200 participants. Synthetic time-series data and a simulated classifier provide a known decision rule, allowing explanation correctness to be controlled without estimating it from a trained model. Participants predict the simulated AI's decisions from feature-attribution-style explanations.

The task reduces reliance on pre-existing domain knowledge. Forward-simulation accuracy is the principal outcome; descriptions of the inferred decision pattern and self-reported ratings provide complementary evidence. The tested correctness levels are study conditions, not deployment requirements.

## Practical Applications & Real-World Use Cases

The findings motivate evaluating explanations with users as well as computational metrics. For a new domain, measure whether intended users can predict decisions and describe the decision rule, and examine variation between users.

The study does not establish clinical, financial, or regulatory correctness thresholds. Its synthetic task also limits direct transfer to domain experts and real-world decisions.

## Insights & Implications

Explanation correctness contributes to understanding, but optimizing it alone does not ensure that users understand a model. The results support measuring human outcomes directly and reporting individual differences alongside aggregate accuracy.

The inconclusive 85%-versus-100% comparison is not evidence of equivalence. Further studies would be needed to locate any threshold and test whether the relationship transfers to other explanation formats and domains.

## Code & Resources

- [Primary paper](https://arxiv.org/abs/2603.25251)
- [Full text](https://arxiv.org/html/2603.25251)

Consult the full text for methods and experimental settings.

## Related Work & Context

### Connections to Related XAI Papers

This work directly relates to and extends:

1. **Explanation Fidelity/Faithfulness Research**
   - Builds on: Work proving faithfulness metrics disagree with each other
   - Extends: Now shows computational metrics may not align with human outcomes
   - Related: "A Comprehensive Study on Fidelity Metrics for XAI" (2401.10640)

2. **Human-Centered XAI Evaluation**
   - Complements: Studies showing "evaluation gap" between metrics and user studies
   - Differs from: Most prior work that tested binary explanation presence/absence
   - Aligns with: Growing emphasis on human validation of XAI methods

3. **Explanation Correctness and Formalization**
   - Related: "Explainable AI needs formalization" (2409.14590) - proposes formal definitions
   - This paper: Provides empirical validation of why formalization matters

4. **Cognitive Aspects of Explanations**
   - Related: "Diagnosing AI Explanation Methods with Folk Concepts of Behavior" - how humans conceptualize systems
   - This paper: Shows correctness affects cognitive understanding
   - Connection: Suggests human mental models require sufficiently accurate explanations

### Position in XAI Taxonomy

**Classification**:
- **Type**: Human-centered XAI evaluation
- **Focus**: Bridging computational metrics and human outcomes
- **Methodology**: Controlled experimental user study
- **Scope**: Feature attribution and correctness specifically

**Related XAI Communities**:

1. **XAI Evaluation & Metrics**
   - Challenges: Metric-outcome misalignment hypothesis
   - Contribution: Empirical test of metric validity

2. **Human-Centered AI**
   - Aligns with: HCI approaches to explainability
   - Contributes: Quantitative evidence for human considerations

3. **Trustworthy AI**
   - Connects to: Trust requires reliable explanations
   - Implication: Trust correlates with explanation correctness above thresholds

### Future Research Directions

This work opens several research pathways:

1. **Threshold Identification Research**
   - Determine correctness thresholds for different domains, user groups, and tasks
   - Develop predictive models of threshold locations

2. **Beyond Correctness**
   - What other explanation dimensions have similar threshold behaviors?
   - How do dimensions interact (e.g., correctness × clarity)?

3. **Individual Differences**
   - Predict who will benefit from high-correctness explanations
   - Personalize explanation correctness based on user needs

4. **Mechanistic Understanding**
   - Why does the 70-85% transition occur?
   - What cognitive processes explain the plateau effect?

### Broader XAI Evolution

This paper marks a shift from **metric-centric** to **outcome-centric** XAI research:
- Previous era: "Can we measure explanation quality?"
- Current era: "Do our measurements predict real-world outcomes?"
- This work advances: Empirical validation of XAI metrics as outcome predictors

## Related Concepts in xAI Subfields

- **Feature Attribution Methods**: LIME, SHAP (explanation generation)
- **Explanation Evaluation**: Fidelity, faithfulness metrics (what this paper tests)
- **Human-Centered XAI**: User studies, cognitive science approaches
- **Transparency & Trust**: How explanation quality affects human trust decisions
- **Regulatory Compliance**: GDPR, AI Act requirements for meaningful explanations

---

**Document Version**: 2026-09-20  
**Status**: Comprehensive overview of published empirical research  
**Last Updated**: Initial documentation from ArXiv preprint
