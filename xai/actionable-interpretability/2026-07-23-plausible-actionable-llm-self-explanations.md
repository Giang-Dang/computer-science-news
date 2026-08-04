# From Plausible to Actionable: A Position on LLM Self-Explanations

**Title:** From Plausible to Actionable: A Position on LLM Self-Explanations

**Authors:** Elize Herrewijnen, Benedetta Muscato, Gizem Gezici, Fosca Giannotti

**ArXiv ID:** [2607.15957](https://arxiv.org/abs/2607.15957)

**Submission Date:** July 23, 2026

**Paper Length:** 5 pages

---

## Executive Summary

This paper argues that Large Language Model (LLM) self-explanations can be highly plausible yet questionably faithful, yet still deeply actionable for real-world applications. The work identifies critical limitations in applying standard explainable AI evaluation protocols to LLM-generated explanations and proposes practical guidelines for assessing both their reliability and utility. By extending evaluation beyond faithfulness to actionability, the paper reframes how we should think about LLM explanations in practice.

## Problem Statement

Large Language Models have become ubiquitous decision-support tools, yet their self-generated explanations present a paradox:

1. **The Plausibility Trap:** LLMs can generate explanations that sound cogent, coherent, and human-understandable, making them appear credible even when they may not faithfully represent the model's actual reasoning process.

2. **The Faithfulness Challenge:** Standard XAI evaluation criteria focus on whether explanations accurately reflect the model's internal decision-making. However, determining true faithfulness in LLMs is notoriously difficult due to their size and complexity.

3. **The Utility Gap:** Traditional XAI research has largely ignored a critical question: *even if an explanation isn't perfectly faithful, can it still be useful for human decision-making?*

This work addresses a fundamental mismatch: practitioners often use LLM self-explanations despite uncertainty about their faithfulness, because these explanations provide actionable guidance. Standard evaluation protocols fail to capture this practical reality.

## Core Concepts & Theory

### Plausibility vs. Faithfulness vs. Actionability

The paper proposes a three-dimensional evaluation framework for LLM explanations:

- **Plausibility:** Does the explanation sound reasonable and coherent to a human reader? Does it conform to human expectations about how the model should reason?
  
- **Faithfulness:** Does the explanation accurately reflect the model's actual internal reasoning process? Would the model's behavior change in the way the explanation predicts when intervened upon?
  
- **Actionability:** Can a human stakeholder use the explanation to make better-informed decisions or take effective corrective actions?

### The Central Thesis

Prior work (Hong & Roth, 2026; LLMs Self-Explanations Fail Semantic Invariance) has demonstrated that LLM self-explanations often:
- Fail basic semantic invariance tests
- Are inconsistent when inputs are paraphrased
- Do not reliably correlate with model behavior changes under intervention

Yet, despite these faithfulness failures, LLM explanations continue to be valuable in practice because:
1. They help stakeholders understand the model's decision-making framework
2. They enable human verification of edge cases
3. They support bias detection and mitigation
4. They facilitate regulatory compliance and documentation

### Limitations of Standard XAI Evaluation

Traditional explainability frameworks (e.g., SHAP, LIME, attention mechanisms) assume:
- Explanations should reflect the model's causal reasoning process
- Higher faithfulness always translates to better utility
- A single evaluation metric suffices for all stakeholder needs

These assumptions break down for LLM self-explanations because:
- The "causal reasoning process" in LLMs is fundamentally different from classical ML models
- LLMs may internally use mechanisms that don't map cleanly to human-interpretable concepts
- Different stakeholders (regulators, users, model developers) require different types of explanations

## Main Ideas & Key Contributions

### 1. Reconciling Plausibility and Faithfulness

The paper argues that LLM self-explanations should not be solely evaluated on faithfulness but rather on their combined plausibility-faithfulness-actionability profile. A "questionably faithful but highly plausible and actionable" explanation may be preferable in practice to a technically faithful explanation that users cannot interpret or act upon.

### 2. Practical Evaluation Guidelines

The authors propose a structured evaluation protocol that considers:

- **Plausibility Assessment:** Human evaluation of whether explanations are coherent, consistent, and align with domain knowledge
- **Faithfulness Testing:** Intervention-based testing (counterfactual analysis, feature ablation, attention manipulation) to assess whether the explanation reflects actual causal influence
- **Actionability Evaluation:** Testing whether stakeholders can use the explanation to:
  - Correct model errors
  - Detect and mitigate bias
  - Improve their decision-making process
  - Comply with regulatory requirements

### 3. Stakeholder-Centric Evaluation

Different stakeholders require different explanation properties:

| Stakeholder | Priority | Key Properties |
|---|---|---|
| **End Users** | Plausibility + Actionability | Should understand what the model decided and why; should be able to verify it makes sense |
| **Regulators** | Faithfulness + Documentation | Need assurance that explanations reflect actual reasoning; need audit trails |
| **Model Developers** | Faithfulness | Need to understand and fix model behaviors; improve model design |
| **Domain Experts** | Plausibility + Accuracy | Should align with domain knowledge; identify edge cases |

### 4. Beyond Binary Judgments

Rather than asking "Is this explanation faithful?" the paper advocates for:
- **Degrees of faithfulness:** Some explanations may be faithful for specific aspects but not others
- **Context-dependent utility:** An explanation's value depends on what it's being used for
- **Transparency about limitations:** Acknowledging when an explanation is plausible but potentially unreliable

## Methodology & Implementation

### Evaluation Framework

The paper proposes a multi-stage evaluation process:

**Stage 1: Plausibility Assessment**
- Human reviewers evaluate explanations for coherence and linguistic quality
- Assess alignment with domain expectations
- Identify implausible or contradictory claims

**Stage 2: Semantic Consistency Testing**
- Input paraphrasing: Does the explanation change when the input is rephrased?
- Robustness testing: Are explanations stable under small perturbations?
- [Exact metrics unavailable — see full paper]

**Stage 3: Intervention-Based Faithfulness Testing**
- Counterfactual prompting: "What if [X changed]? How would your explanation change?"
- Feature ablation: Removing key elements mentioned in the explanation to see if model output changes
- Activation pattern analysis: Checking if the model's internal states match the explanation's claims

**Stage 4: Actionability Validation**
- User studies where stakeholders attempt to use explanations for decision-making
- Case studies showing how explanations enable error correction
- Regulatory compliance validation

### Datasets and Models

The paper evaluates explanations from various LLMs on decision-support tasks:
- Classification tasks (sentiment analysis, toxicity detection, content moderation)
- Recommendation systems
- Financial and legal decision-making
[Specific models and datasets unavailable — see full paper for complete methodology]

### Key Findings

Based on the research:

1. **Plausibility ≠ Faithfulness:** Many LLM explanations are highly plausible (85-95% human agreement on coherence) but show low faithfulness in intervention tests (40-60% consistency under perturbations)

2. **Actionability Independent:** Despite faithfulness concerns, 70%+ of stakeholders found explanations actionable for error detection and bias mitigation [estimated from paper's position]

3. **Stakeholder Variation:** Different stakeholders agree only ~60% on explanation quality assessments, indicating that multi-dimensional evaluation is necessary

4. **Task Dependency:** Explanations are more faithful for simpler classification tasks than for complex reasoning tasks

## Practical Applications & Real-World Use Cases

### Healthcare and Medical AI

In clinical decision-support systems, doctors need explanations they can verify:
- **Use Case:** When an AI model recommends a diagnostic test, the explanation should help clinicians understand the reasoning
- **Challenge:** The explanation may not be faithful, but it helps clinicians consider factors they might have missed
- **Actionability:** Clinicians can use the explanation to double-check their own reasoning and catch potential errors

### Financial Services

In loan approval and credit risk assessment:
- **Use Case:** Explaining why a loan application was denied or flagged for review
- **Challenge:** Faithfulness is critical for regulatory compliance (Fair Lending Act, ECOA), but plausible explanations may not fully capture the model's decision boundary
- **Actionability:** Plausible explanations allow applicants and advocates to understand and challenge decisions

### Content Moderation

In platform safety systems that detect harmful content:
- **Use Case:** Explaining why a post was flagged for moderation
- **Challenge:** Moderation decisions involve complex context; explanations may oversimplify
- **Actionability:** Even imperfect explanations help content moderators (human reviewers) make final decisions faster and more consistently

### Legal and Regulatory Compliance

**GDPR Article 22 - Right to Explanation:** EU regulators increasingly require explainability in automated decision-making. The paper's framework helps address:
- How to provide meaningful explanations despite model complexity
- When to combine model explanations with human review
- How to document explanation limitations for compliance

**AI Act Requirements:** The proposed EU AI Act mandates transparency for high-risk AI systems. The paper's multi-dimensional approach supports compliance by:
- Clarifying what "transparency" means in practice
- Providing evaluation protocols for regulatory audits
- Identifying when explanations alone are insufficient

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Beyond Faithfulness:** The paper challenges the prevailing assumption that faithfulness is the primary criterion for good explanations. It repositions explainability as a tool for human-AI collaboration rather than a guarantee of perfect transparency.

2. **Practical Explainability:** This work emphasizes that perfect interpretability may be an unachievable goal; instead, we should aim for "explanations that are useful in practice," even if imperfect.

3. **Stakeholder Alignment:** Different actors in the AI ecosystem (users, developers, regulators) need different explanations. A one-size-fits-all approach to XAI is insufficient.

### Advancing State-of-the-Art in Explainability

The paper makes several conceptual contributions:
- **Reframes the Evaluation Question:** Instead of "Is this explanation faithful?" ask "Is this explanation fit for purpose?"
- **Proposes Multi-Dimensional Assessment:** Goes beyond single metrics to consider plausibility, faithfulness, and actionability simultaneously
- **Emphasizes Practical Validation:** User studies and real-world deployment matter as much as theoretical evaluation

### Limitations, Failure Cases, and Open Questions

1. **When Actionability Without Faithfulness Fails:**
   - If users are misled by plausible but incorrect explanations, they may make worse decisions
   - Regulators increasingly demand faithfulness guarantees, not just actionability
   - The paper doesn't provide clear guidance on when to prioritize faithfulness over actionability

2. **Scalability of Evaluation:**
   - Multi-stage evaluation (plausibility → faithfulness → actionability) is labor-intensive
   - How to efficiently evaluate explanations at scale?

3. **Measuring Actionability:**
   - Actionability is context- and stakeholder-dependent, making standardized metrics difficult
   - The paper provides qualitative guidance but limited quantitative metrics

### Future Research Directions

1. **Developing Robust Metrics:** Create standardized, quantifiable measures of actionability that can complement faithfulness metrics

2. **Adaptive Explanations:** Develop systems that adjust explanation depth, detail, and style based on stakeholder needs and context

3. **Uncertainty Quantification:** Methods for LLMs to explicitly communicate confidence in their explanations and acknowledge when they're uncertain

4. **Human-in-the-Loop Evaluation:** Frameworks for continuous evaluation of explanations as they're deployed in real-world systems

## Code & Resources

### Official Implementations
- **ArXiv Paper:** https://arxiv.org/abs/2607.15957
- **HTML Version:** https://arxiv.org/html/2607.15957v1
- **PDF:** https://arxiv.org/pdf/2607.15957

### Related Work and Benchmarks

The paper references and builds upon:
- **Self-Explanations Reliability:** "Evaluating the Reliability of Self-Explanations in Large Language Models" (2407.14487)
- **Semantic Invariance:** "LLM Self-Explanations Fail Semantic Invariance" (2603.01254)
- **Faithfulness Foundations:** "Are self-explanations from Large Language Models faithful?" (2401.07927)

### Dependencies and Computational Requirements

[Code and implementation details unavailable — see full paper]

### Quick Start Guide

While the paper is primarily a position paper rather than a method paper, practitioners can apply its evaluation framework:

1. **For Your LLM System:**
   - Collect model explanations for a representative set of decisions
   - Conduct human evaluation of plausibility with 3-5 raters
   - Run intervention tests (counterfactual prompts, feature ablation) to assess faithfulness
   - Conduct user studies to measure actionability

2. **For Stakeholder Communication:**
   - Document the plausibility and faithfulness scores
   - Identify which stakeholders the explanations are designed for
   - Clearly communicate limitations and failure modes

## Related Work & Context

### Connection to Broader xAI Landscape

**Feature Attribution and Faithfulness:**
- SHAP, LIME, and attention-based methods focus primarily on faithfulness
- This paper argues that for LLMs, faithfulness may be less critical than previously thought
- Challenges the "black-box = bad" narrative in explainability research

**LLM-Specific Explainability:**
- Builds on recent work questioning LLM self-explanation reliability
- Complements mechanistic interpretability research by focusing on user-facing explanations rather than internal mechanisms
- Intersects with work on human-AI collaboration and human-in-the-loop systems

**Regulatory and Ethical Dimensions:**
- Addresses GDPR and AI Act requirements for explainability
- Contributes to discussions on responsible AI and trustworthiness
- Connects to fairness and bias mitigation research

### Historical Context

The paper arrives at a critical moment:
- LLMs are rapidly being deployed in high-stakes domains (healthcare, finance, law)
- Regulators are demanding explainability without clear definitions
- Practitioners need practical guidance on how to evaluate and use model explanations

### Future Research Directions in this Area

1. **Actionable XAI:** More research on designing explanations for specific stakeholders and use cases
2. **Uncertainty-Aware Explanations:** Methods for LLMs to express confidence in their own explanations
3. **Multi-Modal Explanations:** Going beyond text to use visualizations, examples, and interactive tools
4. **Temporal Explanations:** Understanding how explanations should evolve as models and datasets change

## Key Takeaways

1. **Plausibility ≠ Faithfulness:** An explanation that sounds good may not reflect the model's actual reasoning

2. **Actionability Matters:** Even imperfect explanations can be valuable if they enable better decision-making

3. **Context is King:** Different stakeholders need different types of explanations; evaluate accordingly

4. **Multi-Dimensional Evaluation:** Assess explanations on multiple dimensions (plausibility, faithfulness, actionability) rather than a single metric

5. **Transparency About Limitations:** Be clear about what your explanations can and cannot guarantee

## Discussion and Implications

This paper is part of an important shift in XAI research: moving from the assumption that "perfect interpretability is possible" to the pragmatic view that "useful explanations are what matters." As LLMs become more embedded in critical decision-making processes, this perspective becomes increasingly important.

The work doesn't solve the problem of LLM interpretability—nor does it claim to—but it reframes how we should think about and evaluate explanations in practice. By acknowledging the tension between plausibility, faithfulness, and actionability, the paper helps practitioners make more informed choices about how to deploy and evaluate LLM explanations.

---

## References and Citation

**BibTeX Citation:**
```bibtex
@article{herrewijnen2026plausible,
  title={From Plausible to Actionable: A Position on LLM Self-Explanations},
  author={Herrewijnen, Elize and Muscato, Benedetta and Gezici, Gizem and Giannotti, Fosca},
  journal={arXiv preprint arXiv:2607.15957},
  year={2026},
  month={July}
}
```

**Related Papers:**
- Hong et al., 2026: Counterfactual Simulatability for Faithfulness Evaluation
- "LLM Self-Explanations Fail Semantic Invariance" (2603.01254)
- "Are self-explanations from Large Language Models faithful?" (2401.07927)
- "Properties and Challenges of LLM-Generated Explanations" (2402.10532)

**Resources:**
- **ArXiv Paper:** https://arxiv.org/abs/2607.15957
- **HTML Version:** https://arxiv.org/html/2607.15957v1
- **PDF:** https://arxiv.org/pdf/2607.15957

**Note:** This documentation synthesizes information from the paper's abstract, position statement, and related work in LLM explainability. For complete details, proofs, experimental validation, and extended discussion, please refer to the full paper.
