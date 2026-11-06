# Causality is Key for Interpretability Claims to Generalise

**ArXiv ID:** [2602.16698](https://arxiv.org/abs/2602.16698)

**Authors:** Shruti Joshi, Aaron Mueller, David Klindt, Wieland Brendel, Patrik Reizinger, Dhanya Sridhar

**Submission Date:** February 18, 2026 (revised March 18, 2026)

**Venue:** Position Paper

---

## Executive Summary

This position paper establishes a foundational framework for organizing and validating interpretability claims using Pearl's causal hierarchy. It addresses a critical problem in XAI research: interpretability findings often outrun their evidence, with researchers making causal or counterfactual claims that are only supported by observational data. By grounding interpretability research in causal inference principles, this work provides a methodological tool to help researchers avoid common pitfalls and ensure their claims match the evidence they possess.

## Problem Statement

Interpretability research on large language models and neural networks has generated important insights into model behavior, yet suffers from recurring and fundamental issues:

1. **Evidence-Claim Mismatch**: Research frequently reports findings using causal language (e.g., "this circuit causes the model to do X") when the underlying data only supports associational claims (e.g., "this circuit is correlated with X").

2. **Reproducibility Concerns**: Interpretability claims often fail to generalize across prompts, contexts, or model variants, suggesting that the mechanisms discovered are not as robust as claimed.

3. **Lack of Methodological Standards**: The field lacks a principled way to distinguish between:
   - What we can observe about model activations
   - What we can infer from interventions (like ablations)
   - What would occur under counterfactual conditions

4. **Scope Creep in Mechanistic Interpretability**: Mechanistic interpretability research frequently makes claims about individual instances ("if we ablate this circuit on this specific prompt, the output would differ") when their evidence only supports population-level claims ("ablating this circuit changes outputs across many prompts").

These problems undermine the trustworthiness of interpretability findings and hinder the field's ability to build reliable, general theories of model behavior.

## Core Concepts & Theory

### Pearl's Causal Hierarchy: A Framework for Interpretability Claims

The paper leverages **Pearl's causal ladder**, a foundational concept from causal inference that organizes statistical questions into three levels:

#### **Rung 1: Association (Observational)**
- **What we can ask**: "What is P(Y|X=x)?" – the probability of an outcome given an observation
- **What evidence supports it**: Passive observation of model activations and outputs
- **In interpretability**: Correlations between neurons/circuits and model behavior. Example: "This attention head frequently attends to subject tokens when the model outputs gendered pronouns."
- **Limitation**: Correlation does not imply causation. The circuit might be epiphenomenal (a side effect, not a cause).

#### **Rung 2: Intervention (Causal)**
- **What we can ask**: "What is P(Y|do(X=x))?" – what happens to Y if we *intervene* to set X to a specific value?
- **What evidence supports it**: Active manipulation of the system (ablations, activation patching, weight perturbations)
- **In interpretability**: Claims about how edits to model components affect behavior. Example: "When we ablate this attention head, the model's accuracy on gendered pronoun prediction drops by 15%."
- **Key insight**: Ablations and patching support interventional claims about *population-level* behavior (averaged across many prompts), but they do NOT support individual-level counterfactuals.
- **Limitation**: Interventions tell us what happens on average across the data, not what would have happened for a specific, unobserved counterfactual scenario.

#### **Rung 3: Counterfactuals (Causal)**
- **What we can ask**: "What would Y have been if we had set X differently, given that we observed specific values in this instance?" This is the hardest question.
- **What evidence supports it**: Controlled experiments with ground truth, strong causal models, or extensive domain knowledge
- **In interpretability**: Claims about what *would have happened* in an unobserved scenario. Example: "If we had NOT ablated this circuit, the model would have given the correct answer on this specific input."
- **Challenge**: Without controlled supervision (knowing what the model would have output under counterfactual conditions), counterfactual claims are largely unverifiable.

### The Interpretability Claim Ladder in Practice

The authors illustrate how interpretability researchers commonly mix these levels:

1. **Observational finding** (Rung 1): We observe that a particular neuron is active during sentiment classification tasks.
2. **Unjustified leap to intervention** (Rung 2): Researchers claim the neuron is *responsible for* sentiment classification.
3. **Unjustified leap to counterfactual** (Rung 3): Researchers claim the model "would have failed" sentiment classification without this neuron.

Only Rung 1 evidence (correlation) is sufficient to support the observational claim. Rung 2 claims require ablation or patching experiments. Rung 3 claims are rarely justifiable without controlled supervision.

### Causal Representation Learning

The paper also discusses how causal representation learning can help specify which variables can be recovered from model activations and under what assumptions. This extends the framework to address how interpretability researchers identify the "right" variables to study and what properties those variables must satisfy.

## Main Ideas & Key Contributions

### 1. **A Methodological Framework for Grounding Interpretability Claims**
The central contribution is providing a principled way to evaluate whether an interpretability study's evidence matches its claims. Rather than relying on intuition or informal conventions, researchers can now use Pearl's causal hierarchy to ask: "What level of evidence do I have, and what level of claim can I legitimately make?"

### 2. **Diagnosing Common Pitfalls**
The paper identifies systematic mismatches between evidence and claims in existing interpretability research:
- Population-level interventional evidence (e.g., "ablating circuit X reduces accuracy by 15% on average") is often reported as individual-level counterfactual claims ("without this circuit, the model would output Y instead of X").
- Associational findings are presented with causal language.

### 3. **Implications for Mechanistic Interpretability**
A key tension highlighted: mechanistic interpretability often aims to explain individual instances ("why did the model output this specific token for this prompt?"), but most evidence is only strong enough to support population-level claims. This is a fundamental scope limitation, not a bug in the methodology.

### 4. **Bridging Causal Inference and Interpretability**
The paper establishes that causal inference—a mature field with well-developed tools and theory—can directly inform interpretability research. It suggests that interpretability researchers should:
- Explicitly state their estimand (what quantity are they trying to estimate?)
- Specify their intervention class (what kinds of changes are they considering?)
- Match their claims to the causal rungs their evidence supports

## Methodology & Implementation

This is a **position paper** rather than an empirical study, so it does not present novel algorithms or a new interpretability method. Instead, it provides a framework for evaluating existing approaches. The methodology consists of:

### 1. **Theoretical Framework Development**
The authors systematically map Pearl's three-rung causal hierarchy onto interpretability research:
- Rung 1 ↔ Correlational analysis of activations
- Rung 2 ↔ Ablation studies and activation patching
- Rung 3 ↔ Counterfactual claims (rarely supported)

### 2. **Case Study Analysis**
The paper analyzes existing interpretability research to identify mismatches. For example:
- Studies that find a circuit is active during specific tasks (Rung 1) but claim it "causes" behavior (Rung 2 or 3)
- Ablation studies (Rung 2) that are reported as if they provide counterfactual guarantees (Rung 3)

### 3. **Causal Representation Learning Discussion**
The framework extends to discuss how representation learning can identify the "right" variables to study and what guarantees can be provided about recoverability.

### Evaluation Approach
Rather than empirical metrics, the paper evaluates interpretability research through logical consistency: Does the evidence support the claim? This meta-level evaluation requires:
- Clear statement of what is being claimed
- Explicit documentation of what evidence is available
- A check: does the evidence level match the claim level?

## Practical Applications & Real-World Use Cases

### 1. **Steering AI Interpretability Research Standards**
As interpretability research becomes more critical for AI safety and deployment, having clear standards for claims prevents misleading conclusions. For example:
- **Healthcare AI**: Claiming a model's decision is caused by a particular feature (Rung 2) when only correlation exists (Rung 1) could lead to inappropriate medical interventions.
- **Legal AI**: Court systems may require counterfactual claims ("the model would have decided differently without this demographic info"), but current evidence only supports Rung 1-2 claims.

### 2. **Mechanistic Interpretability for Large Language Models**
Recent mechanistic interpretability work on LLMs (circuits, attention head functions, etc.) often makes strong claims about individual instances. This framework helps researchers:
- Recognize that their ablation studies support population-level claims
- Develop new methods to move to Rung 3 if counterfactual guarantees are needed
- Focus interventional studies where they provide the strongest evidence

### 3. **Model Auditing and Certification**
As AI systems face regulatory scrutiny (GDPR, EU AI Act, FDA requirements), auditors need a principled way to evaluate interpretability claims:
- Can we verify that a model's decisions are explained by certain features? (Rung 1-2, often achievable)
- Can we guarantee the model would behave differently under counterfactual conditions? (Rung 3, rarely achievable)
- What interventions are necessary and sufficient to change model behavior? (Rung 2, testable)

### 4. **Fairness and Bias Investigation**
In fairness research, practitioners need to know:
- Are demographic features *correlated* with model outputs? (Rung 1)
- If we intervene to remove demographic information, do predictions change? (Rung 2)
- Would the model have decided differently for a specific individual if their demographic features were different? (Rung 3, hard to answer without counterfactual data)

### 5. **Model Debugging and Improvement**
When debugging model failures, teams need to distinguish:
- What features correlate with failures (Rung 1) → suggests where to look
- What components cause failures (Rung 2) → ablate to improve
- What would have prevented the failure for this specific case? (Rung 3) → requires synthetic or counterfactual data

## Insights & Implications

### For the Interpretability Field

1. **Raises Standards for Rigor**: The framework establishes that interpretability research should be as rigorous about causal claims as medical research. Many published claims would not survive scrutiny under this standard.

2. **Identifies a Research Gap**: Moving interpretability from Rung 2 to Rung 3 (supporting counterfactual claims) is an open research challenge. Current methods are largely insufficient. This could motivate new work.

3. **Shifts Expectations**: Rather than claiming mechanistic interpretability "explains" individual model decisions, researchers might more modestly claim it identifies circuits that correlate with or causally influence behavior at the population level.

4. **Connects to Causal Representation Learning**: The paper bridges mechanistic interpretability (a model-centric approach) with causal representation learning (a representation-centric approach), suggesting these fields should inform each other.

### For Trustworthy AI

1. **Regulatory Implications**: Regulators and auditors can use this framework to distinguish between different types of interpretability claims and their evidential support. A feature importance ranking (Rung 1-2) is fundamentally different from a counterfactual guarantee (Rung 3).

2. **Trust Calibration**: Users and stakeholders can better calibrate their trust in AI systems by understanding what an interpretability study actually supports. A correlation finding is not a causal explanation.

3. **Safety and Alignment**: For AI safety and alignment research, this framework clarifies what kinds of interpretability guarantees are possible and what additional work is needed to achieve stronger guarantees.

### Limitations and Open Questions

1. **Population vs. Individual Claims**: Most current evidence is population-level (averaged over prompts), but many practical applications need individual-level guarantees. The paper acknowledges but does not resolve this gap.

2. **Causal Assumptions**: Pearl's hierarchy assumes a well-specified causal model. In practice, for complex systems like neural networks, specifying the correct causal model is itself an open problem.

3. **Computational Cost of Interventions**: Moving to Rung 2 (interventions) often requires expensive ablation studies. The paper doesn't address practical trade-offs between evidence strength and computational cost.

4. **Counterfactual Identification**: While the paper clearly states that Rung 3 claims are hard to verify, it doesn't provide practical guidance on when counterfactual identifiability might be achievable or what additional assumptions are needed.

5. **Representation Learning Gaps**: The discussion of causal representation learning is brief; the paper doesn't fully develop how to identify the "right" variables for interpretability studies.

## Code & Resources

This is a position paper focused on theory and methodology rather than implementation. However, related resources include:

### Official Resources
- **ArXiv Paper**: https://arxiv.org/abs/2602.16698
- **HTML Version**: https://ar5iv.labs.arxiv.org/html/2602.16698
- **PDF**: https://arxiv.org/pdf/2602.16698

### Follow-up Work
The paper has inspired follow-up research applying this framework:
- **"From Observation to Intervention: A Causal Audit of Expert Importance in Mixture-of-Experts Models"** (arXiv:2606.10703) applies the causal hierarchy to audit whether claims about expert importance in MoE models are justified by their evidence.

### Related Causal Inference Resources
- **Judea Pearl's Causal Inference Book**: "The Book of Why" and formal works on causal inference
- **Do-Calculus and Causal Identification**: Pearl's foundational work on identifying causal effects
- **Causal Representation Learning**: Papers on learning representations that support causal reasoning

### Datasets and Code (Not Available from This Paper)
[No primary implementation or datasets provided — the paper is theoretical]

## Related Work & Context

### Relationship to Mechanistic Interpretability
This paper directly addresses the methodological foundation of mechanistic interpretability research (circuits, attention head functions, polysemanticity, etc.). It argues these fields need to be more careful about the claims they make. The framework validates when mechanistic interpretability findings are most robust (population-level interventional claims) and identifies gaps (individual-level counterfactuals).

### Connection to Feature Attribution Methods
Feature attribution methods (LIME, SHAP, Integrated Gradients) operate primarily at Rung 1-2 of the hierarchy. This paper helps these methods' users understand what their outputs represent: correlations or population-level causal effects, not individual-level counterfactual guarantees.

### Causal Interpretability Communities
- **Causal Abstraction Framework**: Recent work (arXiv:2410.20161) on causal abstraction in model interpretability builds on similar ideas about grounding interpretability in causal inference.
- **Causal Deep Learning**: Research on learning causal models from data complements this framework by providing methods to discover causal structure.
- **Concept-Based Explanations**: Concept-based XAI methods can be mapped onto this hierarchy: identifying concepts (Rung 1), testing if concept ablations change outputs (Rung 2), or making counterfactual claims about concepts (Rung 3).

### Position Papers in XAI
The paper joins a recent wave of position papers re-examining XAI foundations:
- **"Interpretability Can Be Actionable"** (arXiv:2605.11161): Proposes that interpretability should be evaluated by actionability rather than solely by explanation quality
- **"Beyond Explainable AI (XAI)"** (arXiv:2602.24176): Argues for a paradigm shift beyond current XAI approaches
- **"Explainable AI is Causality in Disguise"** (arXiv:2603.28597): Similar position that XAI must be grounded in causal reasoning

### Future Research Directions

1. **Moving to Rung 3**: How can interpretability research develop methods that support individual-level counterfactual claims? This likely requires synthetic data, fine-grained causal models, or new theoretical approaches.

2. **Representation Learning**: How can we identify the "right" level of abstraction for interpretability? The paper hints this requires causal representation learning but leaves it underdeveloped.

3. **Methodological Guidelines**: How should practitioners balance evidence strength (moving up the hierarchy) against computational cost? The paper doesn't provide decision-making guidance.

4. **Scope and Generalization**: Under what conditions do Rung 2 findings generalize across prompts, models, and domains? This is crucial for building robust interpretability science.

5. **Integration with Safety**: How does this framework inform AI safety and alignment research? Preliminary work suggests it's relevant, but the connection is underexplored.

## Summary

"Causality is Key for Interpretability Claims to Generalise" provides a rigorous, theoretically grounded framework for evaluating interpretability research. By mapping Pearl's causal hierarchy onto interpretability claims, it establishes clear standards for what evidence justifies what conclusions. The paper identifies systematic failures in current practice (claims outrunning evidence) and sets a higher bar for future work. While it is primarily a position paper, it has immediate methodological value for researchers seeking to ground their claims and for auditors and regulators evaluating AI systems. The framework also identifies important gaps—particularly the difficulty of supporting individual-level counterfactual claims—that could motivate future research directions.
