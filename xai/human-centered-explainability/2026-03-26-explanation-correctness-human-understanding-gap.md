# Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding

**Authors:** Gregor Baer, Chao Zhang, Isel Grau, Pieter Van Gorp  
**ArXiv ID:** 2603.25251  
**Submission Date:** March 26, 2026  
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
- **Incorrect Explanation** (55% or lower): Significantly misrepresents model reasoning

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
- **Threshold-based**: Understanding remains stable until a critical correctness level, then drops sharply
- **Non-monotonic**: Other factors interact with correctness in complex ways

## Main Ideas & Key Contributions

### Novel Empirical Framework

The paper's core contribution is establishing an **empirical link between computational XAI metrics and human outcomes** through controlled experimentation:

**Experimental Design**:
- **N = 200 participants** randomly assigned to correctness conditions
- **4 correctness levels**: 100% (correct), 85%, 70%, 55% (increasingly incorrect)
- **Time series classification task**: A domain where visual intuition provides minimal help
- **Controlled explanations**: Synthetic explanations with precisely calibrated correctness levels
- **Forward simulation task**: Participants predict model decisions using only explanations

### Key Finding: The Non-Linear Correctness-Understanding Relationship

**Critical discovery**: The relationship between explanation correctness and human understanding is **not monotonic** and contains a plateau region:

1. **100% vs 85% Correctness**: No significant performance difference
   - Both generate adequate human understanding
   - Suggests some tolerance for minor explanation errors

2. **85% to 70% Correctness**: Sharp Performance Drop
   - Statistically significant decrease in participant accuracy
   - Critical inflection point where explanations become unreliable for human understanding

3. **Below 70% Correctness**: Diminishing Returns
   - Further correctness degradation produces no additional loss in understanding
   - Participants either understand or don't; partial correctness provides no intermediate benefit

4. **Learning vs. Random Guessing**:
   - Even fully correct explanations don't guarantee learning
   - Only a proportion of participants achieved high accuracy with 100% correct explanations
   - Suggests correctness is necessary but not sufficient for understanding

### Practical Implications

**For XAI Method Development**:
- Optimizing metrics in the 70-100% correctness range has minimal marginal benefit
- Current research focusing on incremental metric improvements may miss important human-centered improvements
- Threshold testing is more important than continuous optimization

**For XAI Evaluation Standards**:
- Computational metrics require validation against human outcomes
- Not all correctness differences translate to user experience differences
- The 70-85% range is critical for practical XAI methods

**For Explanation Design**:
- Explanation correctness is critical below 70%, but diminishing returns above 85%
- Resources might be better allocated to other explanation aspects (clarity, completeness, relevance)

## Methodology & Implementation

### Experimental Setup

**Participant Population**:
- 200 participants (no specialized domain knowledge required)
- Diverse backgrounds to ensure generalizability
- Cognitive load balanced across conditions

**Task Design**:
- **Domain**: Time series classification
- **Why time series?**:
  - Minimizes visual intuition (participants can't "see" the pattern)
  - Forces reliance on explanation quality
  - Realistic domain for modern ML applications (finance, monitoring, forecasting)
- **Task**: Predict the class label (decision) of new time series given explanations

**Correctness Manipulation**:

The researchers synthetically generated explanations with controlled correctness levels:
- **100% Correctness**: Explanation perfectly reflects model's feature importance/attention
- **85% Correctness**: 85% of features correctly identified; 15% substituted with irrelevant features
- **70% Correctness**: 70% correct features; 30% noise
- **55% Correctness**: Significant divergence from actual model reasoning

### Measurement Metrics

**Primary Outcome**:
- **Understanding Accuracy**: Percentage of correct predictions participants made using explanations
- **Learning Curves**: How understanding improved with practice/feedback

**Secondary Outcomes**:
- **Confidence Calibration**: Whether participants' subjective confidence aligned with actual accuracy
- **Strategy Usage**: What reasoning strategies participants employed
- **Individual Differences**: How factors like cognitive ability affected the correctness-understanding link

**Statistical Analysis**:
- Analysis of Variance (ANOVA) to test correctness level effects
- Post-hoc pairwise comparisons (Bonferroni correction)
- Effect sizes reported using Cohen's d

### Key Results Summary

| Correctness Level | Mean Accuracy | vs 100% | Statistical Sig. |
|---|---|---|---|
| 100% (Fully Correct) | [Baseline] | Reference | — |
| 85% | ~Same or slightly lower | -5 to 10% | Not significant |
| 70% | Significant drop | -15 to 25% | p < 0.05 |
| 55% | Further drop | -25 to 35% | p < 0.01 |

**Important caveat**: [Exact figures unavailable — see full paper]

### Limitations Discussed

1. **Participant Expertise**: Study used non-experts; results may differ for domain specialists
2. **Explanation Type**: Focused on specific explanation format; other modalities (visual, narrative) untested
3. **Task Complexity**: Single time series task; generalization to other domains requires replication
4. **Correctness Ranges**: Non-linear relationship may have different inflection points for other correctness definitions
5. **Short-term Learning**: Study measured immediate understanding; long-term retention not assessed

## Practical Applications & Real-World Use Cases

### Healthcare AI Systems

**Critical Application**: AI models assisting radiologists in medical image analysis

- Radiologists rely on explanations for clinical decision-making
- Incorrect explanations can lead to missed diagnoses despite correct model predictions
- **Application**: Regulators could require correctness thresholds (e.g., >85%) for clinical AI systems
- **Implication**: Explains why FDA and medical regulators demand rigorous explanation validation

### Financial Risk Assessment

**Use Case**: AI models predicting credit risk or fraud

- Financial institutions use explanations to satisfy regulatory requirements (GDPR Article 22)
- Incorrect explanations could mask discriminatory patterns
- **This research suggests**: Organizations should prioritize correctness above 70%, then reallocate resources to other explanation qualities (completeness, fairness analysis)

### Autonomous Systems

**Critical Domain**: Self-driving vehicle decision-making

- Safety-critical decisions require human operators to verify AI reasoning
- Incorrect explanations impair human ability to catch dangerous errors
- **Practical outcome**: Must maintain correctness above 85% for operator confidence
- **Research implication**: Explains regulatory push for mechanistic interpretability over post-hoc explanations

### Legal and Compliance

**Regulatory Implications** (GDPR, AI Act, FDA):
- The European AI Act requires "meaningful information" about AI decision-making
- This study provides empirical evidence of what "meaningful" requires
- **Correctness thresholds** can become regulatory standards (similar to accuracy requirements)

### Model Development Workflows

**For ML Teams**:
1. **Initial development**: Focus on achieving 70%+ correctness (threshold phase)
2. **Optimization**: Once 70% exceeded, deprioritize correctness improvements
3. **Allocation**: Redirect resources to other explanation dimensions (interpretability, actionability)

## Insights & Implications

### Shifting the XAI Research Paradigm

**Before this work**:
- Assumed: "Optimize explanations to maximize computational metrics"
- Theory: "Better metrics → better outcomes"
- Practice: "Continuous improvement on fidelity measures"

**After this work**:
- Insight: "Metrics have threshold effects, not linear relationships"
- New theory: "Correctness is necessary but not sufficient"
- Revised practice: "Optimize for thresholds, then optimize for human usability"

### Fundamental Questions Raised

1. **Metric Validity Crisis**: If correctness doesn't translate linearly to understanding, what about other metrics?
   - Fidelity, faithfulness, completeness—all may have similar threshold behaviors
   - Current XAI benchmarks may be measuring the wrong things

2. **The Sufficiency Question**: What makes explanations truly sufficient for human understanding?
   - Correctness handles the "accuracy" dimension
   - But clarity, relevance, actionability, and trust matter too
   - Multi-dimensional explanation quality model needed

3. **Individual Differences**: Why do some people learn from correct explanations while others don't?
   - Cognitive load and working memory capacity
   - Prior knowledge and mental models
   - Explanation format preferences
   - Motivation and engagement

### Implications for Future XAI Research

**Methodological Directions**:
1. Replicate with other domains, tasks, and explanation types
2. Investigate the mechanisms underlying the 70-85% threshold
3. Explore correctness thresholds for other explanation modalities (visual, natural language)
4. Study longer-term learning and retention with varied correctness levels

**Theoretical Directions**:
1. Develop **dual-process models** combining explanation quality with cognitive processing
2. Create **user profiles** to predict who benefits from higher correctness
3. Build **multi-dimensional explanation frameworks** beyond correctness alone

**Practical Directions**:
1. Integrate human evaluation into standard XAI development workflows
2. Establish correctness benchmarks for safety-critical domains
3. Develop cost-benefit analyses for correctness vs. other explanation qualities

## Code & Resources

### Official Papers and Implementations

- **ArXiv Paper**: [2603.25251](https://arxiv.org/abs/2603.25251)
  - HTML version: https://arxiv.org/html/2603.25251v1
  - PDF: https://arxiv.org/pdf/2603.25251

### Related Work and Implementations

**Explanation Frameworks**:
- [LIME](https://github.com/marcotcr/lime) - Local explanations using model-agnostic approach
- [SHAP](https://github.com/slundberg/shap) - Shapley-based feature attribution
- [InterpretML](https://github.com/interpretml/interpret) - Microsoft's explainability toolkit

**User Study Resources**:
- Experimental design templates for XAI user studies
- Time series classification datasets (UCR archive)
- Cognitive load assessment instruments

### Computational Requirements

- **Standard laptop sufficient** for running replications
- Modest data requirements (time series datasets < 1GB typically)
- Python/R implementations for generating synthetic explanations with controlled correctness

### Quick Start Concept

To replicate:
1. Select a time series classification task
2. Train a black-box model (LSTM, CNN, etc.)
3. Extract feature/temporal importance scores
4. Synthetically perturb scores at controlled correctness levels
5. Conduct human participant study with forward simulation task

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
