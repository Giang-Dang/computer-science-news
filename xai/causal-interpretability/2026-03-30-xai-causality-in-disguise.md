# Position: Explainable AI is Causality in Disguise

**ArXiv ID:** [2603.28597](https://arxiv.org/abs/2603.28597)  
**Authors:** Amir-Hossein Karimi  
**Date:** March 30, 2026  
**Subfield:** Causal Interpretability  
**Keywords:** causal models, XAI foundations, structural causal models, counterfactuals, ground truth for explanations

---

## Executive Summary

This position paper makes a bold foundational claim: the persistent fragmentation and contradictions in Explainable AI — conflicting metrics, failed sanity checks, unresolved robustness debates — all stem from a single root cause: XAI methods lack a proper ground truth. The author argues that this ground truth *does* exist and is the **causal model** governing the system under study. By formally proving that causal models are both necessary and sufficient for answering any XAI query, the paper provides a unifying theoretical foundation for the entire field.

---

## Problem Statement

The XAI field has produced hundreds of methods yet remains deeply fragmented:
- LIME, SHAP, Integrated Gradients, Grad-CAM, attention explanations — they often *disagree* on which features matter
- Sanity checks fail: many XAI methods produce similar explanations regardless of model weights
- Metrics conflict: faithfulness, robustness, and human-alignment metrics yield contradictory rankings
- The community relies on "surveys of surveys" without consensus on what a correct explanation even is

**The core diagnosis:** This chaos arises because XAI methods are answers in search of a question. Without a formally defined notion of the *correct* explanation, every method is equally valid — and equally arbitrary.

**The central claim:** The correct answer to any XAI query is uniquely determined by the **structural causal model (SCM)** governing the data-generating process. Existing XAI methods are therefore implicitly approximating causal inference, but without acknowledging it — hence "causality in disguise."

---

## Core Concepts & Theory

### Structural Causal Models (SCMs)

An SCM is a tuple $\mathcal{M} = \langle \mathbf{U}, \mathbf{V}, \mathcal{F}, P(\mathbf{U}) \rangle$ where:
- $\mathbf{U}$: exogenous (background) variables
- $\mathbf{V}$: endogenous (observed) variables
- $\mathcal{F}$: structural functions $V_i = f_i(\text{Pa}(V_i), U_i)$
- $P(\mathbf{U})$: distribution over exogenous variables

SCMs support three levels of Pearl's **Ladder of Causation**:
1. **Association** (seeing): $P(Y | X = x)$ — standard statistical dependence
2. **Intervention** (doing): $P(Y | do(X = x))$ — effect of forcing X to value x
3. **Counterfactual** (imagining): $P(Y_{X=x} | X = x', Y = y')$ — what Y would be if X had been x, given it was x'

### XAI Queries as Causal Queries

The paper formalizes a taxonomy showing every standard XAI question maps to a causal query:

| XAI Question | Causal Formulation | Ladder Level |
|---|---|---|
| Which features matter for this prediction? | $\frac{\partial}{\partial x_i} P(Y \| do(X_i = x_i))$ | Intervention |
| What minimal change reverses the decision? | $\arg\min_{x'} \|x' - x\|$ s.t. $Y_{X=x'} \neq y$ | Counterfactual |
| Is this model fair? | $P(Y_{X_s=s} = y) = P(Y_{X_s=s'} = y)$ for all $s, s'$ | Counterfactual |
| Why did the model predict y? | $P(Y=y \| do(X=x))$ given observed $P(Y=y \| X=x)$ | Association + Intervention |

### Necessity and Sufficiency Theorem

The paper's main theoretical result:

**Theorem 1 (Necessity):** For any well-posed XAI query $Q$ about a system generating data from SCM $\mathcal{M}$, the answer to $Q$ requires knowledge of $\mathcal{M}$.

**Theorem 2 (Sufficiency):** Given $\mathcal{M}$, any XAI query $Q$ can be answered precisely.

*Corollary:* XAI methods that do not account for the causal structure of the data-generating process are answering a different (typically ill-posed) question.

### Why Existing Methods Are "Causality in Disguise"

- **SHAP** computes Shapley values over feature subsets — this is an intervention-level quantity $P(Y | do(X_S = x_S))$ but applied to a statistical model rather than the causal graph
- **LIME** fits a local linear approximation — approximates the partial derivative of an interventional distribution
- **Counterfactual explanations** are explicitly counterfactual queries but rarely constrain to the correct SCM's counterfactual distribution

All these methods reach for causal concepts but ground them in observational or purely correlational statistics — causing all the downstream problems (feature correlation issues, distribution shift failures, robustness inconsistencies).

---

## Main Ideas & Key Contributions

### 1. A Unified Theoretical Foundation for XAI

For the first time, the paper provides a **proof** that the XAI ground truth problem is not fundamentally unsolvable — it simply requires causal models. This reframes all prior work as approximations to causal inference under varying assumptions about the SCM.

### 2. Classification of XAI Methods by Causal Assumption

The paper introduces a taxonomy:
- **Rung-1 XAI** (associational): standard feature importance, attention weights
- **Rung-2 XAI** (interventional): SHAP, LIME, Integrated Gradients (when correctly applied)
- **Rung-3 XAI** (counterfactual): algorithmic recourse, counterfactual explanations

Higher-rung methods require stronger causal assumptions and produce more meaningful explanations — but existing methods rarely acknowledge which rung they operate at.

### 3. Diagnosis of XAI Failure Modes

The framework explains *why* XAI sanity checks fail:
- Methods operating at Rung-1 will produce identical explanations for two models with the same marginal distributions, even if their causal mechanisms differ
- This is not a bug in the method — it's correct behavior for a Rung-1 query, which should not distinguish causally distinct models

### 4. A Research Agenda

The paper concludes with a research roadmap:
1. Develop SCM estimation methods scalable to deep learning systems
2. Build XAI evaluation benchmarks with known ground-truth SCMs
3. Reinterpret existing XAI literature through the causal lens
4. Integrate causal structure discovery into XAI toolkits

---

## Methodology & Implementation

This is primarily a **theoretical position paper** with formal proofs rather than empirical experiments. The methodology is axiomatic:

1. Define a formal language for XAI queries
2. Show equivalence to queries in Pearl's causal hierarchy
3. Prove necessity: for any XAI query, construct a pair of SCMs that give identical observational distributions but different correct answers
4. Prove sufficiency: given the SCM, provide an algorithm for answering any query

### Supporting Examples

The paper illustrates each theorem with concrete examples:
- **Healthcare**: Why did the model deny insurance? (Rung-2 vs. Rung-3 yield different, both defensible answers)
- **Hiring**: Is the model discriminating? (Rung-1 says no; Rung-3 may say yes)
- **Autonomous driving**: What would have happened if the pedestrian had not been there? (Rung-3 only)

### Relationship to Interventional XAI

The paper connects to the intervention-based interpretability literature:
- **Activation patching** (used in mechanistic interpretability) is a Rung-2 operation: it answers "what would the output be if this activation had been produced by the clean input?"
- **ROME/MEMIT knowledge editing** is a Rung-2 intervention on the model's internal SCM

---

## Practical Applications & Real-World Use Cases

### Legal and Regulatory Compliance

GDPR's "right to explanation" and the EU AI Act's transparency requirements both require explanations of automated decisions. This paper argues these requirements are implicitly asking for **counterfactual (Rung-3) explanations** — which require causal models. Current XAI methods providing Rung-1 answers to Rung-3 questions may not satisfy regulatory intent.

**Concrete implication:** Regulators and auditors should demand that XAI methods specify which causal rung they operate at and whether the assumed causal structure is validated.

### Healthcare AI

Medical decisions require counterfactual reasoning ("would this patient have survived without intervention X?"). Current feature attribution methods cannot reliably answer this — they provide associational importance scores, not causal effect estimates.

### Financial Credit Scoring

FCRA and ECOA require "adverse action notices" explaining credit denials. The paper argues these must be counterfactual explanations (what would have changed the decision?) grounded in a causal model of creditworthiness.

### Autonomous Systems

Safety analysis of autonomous vehicles requires counterfactual queries: "would the accident have occurred if the sensor had detected the obstacle 0.1 seconds earlier?" These are Rung-3 queries requiring SCMs of the physical environment and control system.

---

## Insights & Implications

### A Paradigm Shift for XAI Research

If the community adopts this framework, it would:
1. End debates about which XAI method is "better" without specifying the query type
2. Force explicit declaration of causal assumptions in every paper
3. Shift evaluation from "is this explanation human-interpretable?" to "does this explanation match the ground-truth causal effect?"

### The SCM Estimation Challenge

The main practical barrier is that SCMs are rarely known and hard to estimate from data. The paper acknowledges this but argues it is the *right* problem to work on, rather than inventing new XAI methods that avoid the causal question.

### Relationship to Mechanistic Interpretability

Mechanistic interpretability (MI) in deep learning is, from this perspective, an attempt to discover the **SCM of the model itself** — the causal graph over computations. Activation patching, path patching, and circuit analysis are all Rung-2 interventions on the model's internal causal graph. This positions MI as the highest-quality form of XAI, provided the model's internal SCM is a faithful representation of the task-relevant causal structure.

### Open Questions
- How do we efficiently estimate SCMs for high-dimensional input spaces?
- How do we handle non-parametric SCMs (neural networks as structural functions)?
- What is the computational complexity of answering Rung-3 queries at scale?
- When is it acceptable to give Rung-1 answers to Rung-3 questions (i.e., under what assumptions do they coincide)?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2603.28597](https://arxiv.org/abs/2603.28597)
- **Related Tools:**
  - [DoWhy](https://github.com/py-why/dowhy) — Python library for causal inference
  - [CausalML](https://github.com/uber/causalml) — Causal ML toolkit by Uber
  - [EconML](https://github.com/py-why/EconML) — Causal effect estimation
  - [Causal Discovery Toolbox](https://github.com/FenTechSolutions/CausalDiscoveryToolbox)

### Implementing the Framework
```python
import dowhy
from dowhy import CausalModel

# Define causal graph
causal_graph = """
digraph {
    X1 -> Y;
    X2 -> Y;
    X1 -> X2;  # X1 causes X2 (confounds naive attribution)
}
"""

model = CausalModel(data=df, treatment="X1", outcome="Y", graph=causal_graph)

# Rung-2: interventional effect
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

# Rung-3: counterfactual
counterfactual = model.refute_estimate(estimate, method_name="placebo_treatment_refuter")
```

---

## Related Work & Context

### Foundational Causal Inference
- **Pearl (2009)**: Causality — the foundational text for SCMs
- **Peters, Janzing, Schölkopf (2017)**: Elements of Causal Inference
- **Schölkopf et al. (2021)**: Toward Causal Representation Learning

### XAI Papers the Position Responds To
- **Ribeiro et al. (2016)**: LIME — local linear approximation (Rung-1/2 conflation)
- **Lundberg & Lee (2017)**: SHAP — Shapley values without causal grounding
- **Wachter et al. (2017)**: Counterfactual explanations — Rung-3 intent, but often implemented without SCMs

### Supporting Causal XAI Work
- **Janzing et al. (2020)**: Feature relevance quantification via causal tools
- **Heskes et al. (2020)**: Causal Shapley values
- **Karimi et al. (2021)**: Algorithmic recourse under causal models

### Where This Leads

This paper is a call to action. The follow-up research agenda involves:
1. Building benchmark SCMs for XAI evaluation
2. Developing scalable counterfactual inference for neural networks
3. Revisiting existing XAI methods with explicit causal assumptions declared
4. Connecting causal XAI to the AI Act's transparency requirements

---

*Sources:*
- [arxiv.org/abs/2603.28597](https://arxiv.org/abs/2603.28597)
