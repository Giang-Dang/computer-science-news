# Faithfulness Metrics Don't Measure Faithfulness: A Meta-Evaluation with Ground Truth

**ArXiv ID:** [2605.25052](https://arxiv.org/abs/2605.25052)  
**Authors:** Yoav Gur-Arieh (Tel Aviv University), Ana Marasović (University of Utah), Mor Geva (Tel Aviv University)  
**Date:** May 24, 2026  
**Subfield:** Feature Attribution

---

## Executive Summary

This paper delivers a critical wake-up call to the xAI community by conducting the first systematic evaluation of faithfulness metrics using ground-truth labels. The authors demonstrate that most widely-used faithfulness metrics for chain-of-thought (CoT) explanations perform near chance, exhibiting strong prediction biases and poor generalization across settings. They introduce BonaFide, a benchmark of 3,066 labeled CoTs across 13 diverse tasks and 10 language models, establishing a foundation for future work in developing reliable faithfulness evaluation methods.

---

## Problem Statement

### The Faithfulness Challenge in XAI

Large language models generate chain-of-thought (CoT) explanations—step-by-step reasoning traces that purport to explain their decision-making process. However, a fundamental question remains unanswered: **Do these CoT explanations faithfully represent the model's actual computations?**

Since the rise of mechanistic interpretability and post-hoc explanation methods like LIME and SHAP, the xAI community has proposed numerous **faithfulness metrics** to assess whether an explanation truly reflects a model's internal reasoning. These metrics have become standard evaluation tools in interpretability research, driving methodological choices and claims about explanation quality.

### Critical Gap in Current Approaches

Despite their ubiquity, a crucial limitation exists: **no one knows if these metrics actually measure faithfulness.** The core problem is that model internals are not directly observable, making it impossible to verify whether an explanation is truly faithful without ground-truth labels of the model's actual computations.

This creates a circular problem:
- Faithfulness metrics are designed to evaluate explanations
- We cannot directly observe model computations to verify accuracy
- Therefore, we cannot validate whether the metrics themselves are reliable
- Yet the field treats these metrics as gold standards

### Prior Work Limitations

Previous work has identified specific challenges with faithfulness evaluation:
- Metrics may conflate different notions of faithfulness
- Sensitivity to input distribution imbalances
- Trade-offs between explanation conciseness and comprehensiveness
- Poor transferability across different tasks and models

However, none of these prior studies could definitively establish **whether the metrics themselves are valid instruments** for measuring faithfulness.

## Core Concepts & Theory

### Defining Faithfulness in Context

**Faithfulness** for chain-of-thought reasoning is defined as: the degree to which an explanation (CoT) accurately represents the computations that produced the model's prediction.

This definition operates at two levels:

1. **CoT-Level Faithfulness:** Whether the entire chain of reasoning faithfully represents the model's overall computational process
2. **Step-Level Faithfulness:** Whether individual reasoning steps accurately reflect intermediate model computations

### The Ground Truth Problem

A key insight of this work is that ground truth for faithfulness can be partially recovered from task design. The authors leverage the principle that:

**If a task's output structure makes certain intermediate computations necessary to produce correct results, then we can infer which computations must have occurred.**

For example, in a counting task where the model must count objects to answer correctly, observing a correct answer implies the counting computation occurred. By carefully designing tasks where the mapping between outputs and required computations is clear, the authors can derive ground-truth faithfulness labels.

### The Metrics Landscape

The paper evaluates prominent faithfulness metrics falling into categories:

1. **Perturbation-Based Metrics:** Measure impact of removing or modifying explanation components
2. **Gradient-Based Metrics:** Compute gradients to assess influence of reasoning steps
3. **Model-Based Metrics:** Train auxiliary models to predict faithfulness
4. **Task-Specific Metrics:** Designed for particular reasoning types (e.g., counting, multi-hop)

### Mathematical Framework

Faithfulness metrics are evaluated using:

- **AUROC (Area Under the Receiver Operating Characteristic Curve):** Primary metric for assessing discrimination between faithful and unfaithful explanations
- **Bias Analysis:** Measuring systematic preference for certain prediction types
- **Transfer Performance:** Evaluating metric reliability across different task/model combinations
- **Computational Cost:** Tracking the number of forward passes required

## Main Ideas & Key Contributions

### Contribution 1: Revised Faithfulness Definition

The paper provides a rigorous definition of faithfulness specifically tailored to chain-of-thought settings, distinguishing it from mere explanation quality or coherence. This definition clarifies that faithfulness is fundamentally about correspondence between explanation and internal computation, not about surface-level plausibility.

### Contribution 2: Ground-Truth Labeling Methodology

The authors developed an **automated labeling pipeline** that constructs ground-truth faithfulness labels by:

1. **Task Design:** Creating tasks where outputs partially determine required computations
2. **Backward Inference:** Deducing which intermediate steps must have occurred based on correctness
3. **Label Verification:** Cross-checking labels across multiple examples and models

This methodology makes the previously unobservable internal computations partially observable through clever task design.

### Contribution 3: The BonaFide Benchmark

The core contribution is **BonaFide**, a comprehensive benchmark containing:

- **3,066 labeled chains of thought** with ground-truth faithfulness labels
- **13 diverse tasks** spanning difficulty and reasoning type:
  - Fact verification
  - Multi-hop reasoning
  - Object counting
  - Analogy completion
  - Numerical reasoning
  - And others
- **10 different language models** enabling cross-model evaluation
- **Dual-level annotations**: Both CoT-level and step-level faithfulness labels

### Contribution 4: Systematic Metric Evaluation

Using BonaFide, the authors conduct the first large-scale evaluation of faithfulness metrics with ground truth:

**Key Findings:**

1. **Near-Chance Performance:** Most metrics perform barely better than random (AUROC ~0.50), meaning they cannot reliably distinguish faithful from unfaithful explanations

2. **Best Metric Performance:**
   - CoT-level: Best metric achieves ~0.70 AUROC (significantly better than chance but far from reliable)
   - Step-level: Best metric reaches only ~0.59 AUROC (marginal improvement over random)

3. **Strong Prediction Biases:** Metrics exhibit systematic preferences for certain types of predictions, including:
   - Bias toward predicting faithfulness on certain task types
   - Imbalanced sensitivity to different kinds of errors
   - Overfitting to specific model characteristics

4. **Poor Generalization:** Metrics trained/calibrated on one set of tasks fail to transfer to others, suggesting they're capturing task-specific patterns rather than genuine faithfulness

5. **Degradation on Longer Traces:** Performance degrades significantly on longer chains of thought, raising questions about scalability

6. **Prohibitive Computational Cost:** Many metrics require 10-100+ forward passes per example, making them impractical for large-scale deployment

### Contribution 5: Implications for the Field

The paper reveals that the current practice of using faithfulness metrics as evaluation standards is fundamentally problematic. This raises critical questions:

- How reliable are published claims about explanation quality if the metrics are flawed?
- Which metric should be used, given that none are reliable?
- Are current evaluation practices creating false confidence in explanations?

## Methodology & Implementation

### Task Design for Ground Truth

The researchers selected 13 tasks with the property that correct outputs imply specific computations:

**Example 1 - Counting:** "Count the objects in the image. Answer: 7"
- Implies the model performed counting
- An unfaithful CoT claiming to count but reaching the number via other means would be detectable

**Example 2 - Multi-hop Reasoning:** Tasks requiring chain of logical inferences
- Correct answers imply all intermediate steps were executed
- Missing or incorrect intermediate reasoning would prevent correct final answers

**Example 3 - Fact Verification:** Tasks verifying facts about entities
- Correct verification implies appropriate fact retrieval occurred
- Spurious reasoning leading to correct answers would be identifiable

### Model Evaluation

The study evaluated CoTs from 10 models:
- Various sizes of language models
- Different architectures
- Different training approaches

This diversity ensures findings generalize beyond any single model class.

### Annotation Pipeline

For each CoT:
1. Determine if the final output is correct
2. Based on task requirements and correctness, infer which computations must have occurred
3. Compare inferred computations against the explicit steps in the CoT
4. Assign binary faithfulness labels (faithful/unfaithful) at both CoT and step levels

### Metric Evaluation Protocol

For each metric, the researchers:

1. **Compute metric scores** on all 3,066 examples
2. **Compute AUROC** against ground-truth labels
3. **Analyze prediction biases** using calibration curves
4. **Test transfer** across task and model combinations
5. **Measure computational cost** by counting forward passes

[Exact figures unavailable — see full paper] for detailed per-metric breakdowns and statistical significance tests.

## Practical Applications & Real-World Use Cases

### Impact on Interpretability Research

The findings have immediate implications for how interpretability research is conducted and evaluated:

**1. Explanation Method Evaluation**
- Papers claiming their explanation method is "more faithful" based on metrics now face credibility questions
- Researchers must be more cautious about using faithfulness metrics as primary evidence
- Alternative evaluation approaches become urgent

**2. Mechanistic Interpretability**
- Methods claiming to have "found faithful decompositions" based on faithfulness metrics need re-evaluation
- Sparse autoencoders, circuit analysis, and other mechanistic interpretability approaches often rely on faithfulness metrics
- The reliability of these claims is now in question

**3. LLM Transparency and Safety**
- If CoT explanations cannot be reliably verified as faithful, their value for safety and transparency is reduced
- Organizations deploying LLMs for high-stakes decisions (healthcare, legal, finance) cannot rely on CoTs as reliable explanations
- New approaches to model transparency are needed

### Regulatory and Compliance Implications

**GDPR and Right to Explanation:**
- European regulations require "meaningful explanations" for automated decisions
- If CoT explanations cannot be verified as faithful, they may not satisfy regulatory requirements
- Organizations may need alternative approaches to demonstrate explainability compliance

**AI Act Compliance:**
- The EU AI Act requires transparency and explainability for high-risk AI systems
- Unreliable faithfulness metrics undermine compliance claims
- Better evaluation methods are necessary for regulatory adherence

**FDA Guidance for AI/ML in Healthcare:**
- FDA increasingly requires validated explanation methods for ML in clinical settings
- Poor faithfulness metric performance raises concerns about explanation validation
- Medical device manufacturers must reconsider explanation strategies

### Domain-Specific Applications

**1. Healthcare**
- Diagnostic decision support systems rely on explanations for clinical adoption
- If explanations cannot be verified as faithful, clinician trust is undermined
- More rigorous explanation validation becomes essential

**2. Finance**
- Loan approval and credit scoring systems face scrutiny for fairness and interpretability
- Untrustworthy faithfulness metrics weaken transparency claims
- Alternative approaches to explanation validation are needed

**3. Legal Systems**
- Predictive sentencing and risk assessment tools require explainability
- Unreliable explanations undermine the legitimacy of algorithmic decisions
- Judicial systems need trustworthy explanation methods

**4. Autonomous Systems**
- Self-driving vehicles and autonomous decision-making require transparent reasoning
- Chain-of-thought explanations cannot be trusted without reliable validation
- Safety-critical applications need more robust explanation approaches

## Insights & Implications

### Fundamental Findings

1. **The Metric Crisis:** The field has been operating under the assumption that faithfulness metrics are reliable, when in fact most are not. This represents a fundamental methodological crisis in interpretability research.

2. **Trade-offs and Complexity:** The failure of faithfulness metrics suggests that faithfulness itself is more complex than previously understood. Single metrics cannot capture the multifaceted nature of faithful explanations.

3. **Transferability Problem:** The poor transfer across tasks and models reveals that "faithfulness" may not be a universal property. What counts as faithful in one context may not transfer to another.

4. **The Computation Problem:** Faithfulness fundamentally requires access to ground truth about internal computations. Without this ground truth (which is difficult to obtain at scale), reliable evaluation remains elusive.

### Implications for XAI Research

**1. Rethinking Evaluation Methodology**
- The field must move beyond single-metric evaluation
- Multiple complementary evaluation approaches are needed
- Ground truth is essential but expensive to obtain

**2. Advancing Explanation Methods**
- Rather than relying on potentially unreliable metrics, explanation methods should be evaluated through:
  - User studies measuring human understanding
  - Task performance with explanations
  - Adversarial robustness
  - Consistency across model variants

**3. Mechanistic Interpretability Opportunities**
- The failure of CoT faithfulness metrics argues for mechanistic interpretability approaches
- Understanding actual model computations through techniques like:
  - Sparse autoencoders for disentangling representations
  - Activation patching to measure causal influence
  - Circuit analysis to identify computational structures
- These methods bypass the need for CoT explanations

**4. Hybrid Approaches**
- Combining mechanistic interpretability (internal analysis) with post-hoc explanations (user-facing)
- Using mechanistic insights to validate or improve post-hoc explanations
- Developing explanation methods grounded in actual model computations

### Open Questions and Future Research

1. **Better Metrics:** What properties should a faithfulness metric have? Can we design metrics that are more robust and generalizable?

2. **Efficient Ground Truth:** How can we obtain ground-truth faithfulness labels more efficiently? Can task design be systematized?

3. **Multi-Aspect Faithfulness:** Should we evaluate different aspects of faithfulness separately (logical consistency, completeness, accuracy)?

4. **Model-Agnostic vs. Model-Specific:** Should metrics be tailored to specific model architectures, or can universal metrics work?

5. **Computational Tradeoffs:** How can we develop efficient metrics that don't require excessive forward passes?

## Code & Resources

### Official Resources

- **BonaFide Benchmark:** Available at [Hugging Face Collections](https://huggingface.co/collections/yoavgurarieh/bonafide)
  - Contains 3,066 labeled chains of thought
  - Includes evaluation code and metric implementations
  - Organized by task type and model
  - Full ground-truth annotations

- **Evaluation Code:** Released with the paper
  - Scripts for computing AUROC against ground truth
  - Metric implementations for comparison
  - Task data and label generation pipeline

### Required Dependencies

- PyTorch or similar deep learning framework
- Language model inference capabilities (transformers library)
- Standard ML evaluation libraries (scikit-learn for AUROC computation)
- Python 3.8+

### Quick Start Guide

1. Download BonaFide benchmark from Hugging Face
2. Load ground-truth faithfulness labels
3. Compute your metric scores on CoTs
4. Evaluate AUROC using the provided scripts
5. Compare against published baseline metrics

### Interactive Resources

- The paper includes detailed tables comparing metric performance across:
  - Task types
  - Model sizes
  - Reasoning trace lengths
  - Prediction bias analysis

## Related Work & Context

### Connection to Feature Attribution Literature

Faithfulness evaluation has roots in feature attribution research:

- **LIME (Local Interpretable Model-agnostic Explanations):** Pioneered local explanation methods but recognized the need for faithfulness validation
- **SHAP (SHapley Additive exPlanations):** Addresses some faithfulness concerns through game theory but still relies on empirical validation
- **Integrated Gradients:** Gradient-based attribution claiming certain theoretical guarantees

This work challenges the assumption that metrics can reliably validate these methods.

### Relationship to Mechanistic Interpretability

The paper's findings support growing interest in mechanistic interpretability:

- **Sparse Autoencoders:** Decompose learned representations into interpretable features
- **Activation Patching:** Causally intervenes on internal activations to measure influence
- **Circuit Analysis:** Identifies specific computational structures in neural networks

These approaches don't rely on potentially unreliable CoT metrics, instead directly examining internal computations.

### Connection to Human-Centered XAI

The limitations revealed by this work support increased emphasis on:

- **User Studies:** Validating explanations through human understanding
- **Behavioral Metrics:** Measuring whether explanations improve human decision-making
- **Cognitive Load Analysis:** Assessing explainability impact on human cognition
- **Domain Expert Evaluation:** Using subject matter experts to validate explanations

### Broader XAI Research Directions

This work contributes to emerging discussions about:

1. **Explanation Standardization:** Need for formal standards for what constitutes a valid explanation
2. **Interdisciplinary Approaches:** Combining insights from cognitive science, HCI, and philosophy
3. **Regulatory Alignment:** Ensuring explanation methods meet legal and regulatory requirements
4. **Multi-Modal Explanations:** Developing explanation approaches beyond text (visual, interactive, etc.)

### Position in the Faithfulness Evaluation Timeline

**Prior to 2023:** Faithfulness metrics proposed without systematic validation

**2023-2025:** Growing recognition of metric limitations through case studies

**May 2026:** This paper provides first large-scale systematic evaluation

**Expected Future:** Development of more reliable evaluation methods, shift to mechanistic interpretability, hybrid approaches

## Discussion and Future Outlook

### Why This Matters Beyond Academia

The implications of unreliable faithfulness metrics extend far beyond interpretability research:

- **Trust in AI Systems:** If explanations cannot be verified, public trust in AI is undermined
- **Deployment Decisions:** Organizations may unknowingly deploy AI systems with untrustworthy explanations
- **Liability and Accountability:** Legal liability for AI failures increases without reliable transparency
- **Scientific Integrity:** Published research claims may be based on unreliable validation methods

### A Call for Methodological Reform

This paper advocates for fundamental changes in how the interpretability community validates explanation methods:

1. **Prioritize Ground Truth:** Invest in methods to obtain ground-truth labels
2. **Embrace Uncertainty:** Acknowledge limitations of current metrics
3. **Diversify Evaluation:** Use multiple complementary approaches
4. **Validate with Humans:** Complement metrics with user studies
5. **Mechanistic First:** Consider mechanistic approaches before post-hoc explanations

### The Path Forward

The field faces a choice:

**Option A - Metric Improvement:** Continue developing better faithfulness metrics
- Requires systematic ground truth (expensive)
- May face fundamental limitations (generalization issues)
- Gradual progress expected

**Option B - Mechanistic Turn:** Shift focus to mechanistic interpretability
- Directly examines computations rather than relying on CoT
- Avoids metric validation problems
- More aligned with recent research trends

**Option C - Hybrid Approach:** Combine mechanistic insights with improved metrics
- Use mechanistic understanding to inform better metrics
- Validate metrics against mechanistic findings
- Most promising long-term direction

## Conclusion

This paper delivers a critical message to the interpretability research community: **we have been relying on evaluation methods that do not reliably measure what they claim to measure.** While the findings are sobering, they open new research directions and force the field to confront fundamental methodological questions.

The BonaFide benchmark provides the first ground-truth foundation for evaluating faithfulness metrics, enabling future work to develop more reliable approaches. However, the immediate implication is clear: claims about explanation faithfulness based on existing metrics should be viewed with skepticism.

The path forward requires methodological innovation, a shift toward mechanistic interpretability, increased reliance on human validation, and a recognition that explanation quality is multifaceted and cannot be reduced to a single metric.

For practitioners deploying AI systems in high-stakes domains, this work underscores the importance of:
- Not relying solely on faithfulness metrics for validation
- Combining multiple evaluation approaches
- Involving domain experts in explanation validation
- Considering mechanistic interpretability methods
- Remaining transparent about explanation limitations

The failure of faithfulness metrics is not the end of the interpretability story—it's an opportunity to build more reliable approaches to understanding AI systems.
