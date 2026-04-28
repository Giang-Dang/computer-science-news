# Position: Causality is Key for Interpretability Claims to Generalise

**ArXiv ID:** 2602.16698  
**Authors:** Shruti Joshi, Aaron Mueller, David Klindt, Wieland Brendel, Patrik Reizinger, Dhanya Sridhar  
**Submitted:** February 18, 2026 (v1); revised March 18, 2026 (v2)  
**Subfield:** Causal Interpretability  
**Links:** [ArXiv](https://arxiv.org/abs/2602.16698) | [PDF](https://arxiv.org/pdf/2602.16698)

---

## Executive Summary

This position paper makes a foundational argument that the recurring failures of interpretability research — findings that do not replicate, causal claims that outrun the evidence, interventions that do not generalize — stem from a failure to ground research in causal inference principles. The authors propose that Pearl's causal hierarchy should serve as the organizing framework for interpretability methodology: distinguishing association-level findings (what correlates with what) from intervention-level findings (what affects what) from counterfactual-level findings (what would have happened), and demanding that researchers claim only what their experimental evidence supports.

---

## Problem Statement

### The Reproducibility Crisis in Interpretability Research

Despite a decade of active research and thousands of publications, mechanistic interpretability of large language models suffers from persistent methodological problems:

1. **Non-generalizing findings:** Circuits and mechanisms identified in one experimental context (e.g., the Indirect Object Identification task on GPT-2 Small) frequently fail to replicate under slight distribution shifts, longer contexts, or different model sizes
2. **Causal overclaiming:** Papers use observational methods (attention weight analysis, gradient attribution) but draw causal conclusions about which components "cause" certain behaviors
3. **Intervention inconsistencies:** Ablation and activation patching results are sensitive to the choice of ablation value, prompting set, and metric — yet are reported as if they support stable causal claims
4. **Lack of systematic frameworks:** Different papers use incompatible experimental designs and evaluation metrics, making results impossible to compare

### The Core Diagnosis

The authors argue these problems share a common root cause: **interpretability research lacks a principled framework for specifying what kind of claim a given experimental design can support.** Without such a framework, researchers inadvertently conflate:
- "Component X correlates with behavior Y" (associational)
- "Component X causes behavior Y" (interventional)
- "If X had been different, Y would have differed" (counterfactual)

These are fundamentally different claims requiring fundamentally different evidence.

---

## Core Concepts & Theory

### Pearl's Causal Hierarchy

Judea Pearl's causal hierarchy (also called the "ladder of causation") provides a principled taxonomy of causal claims:

| Level | Query Type | Example | Required Method |
|-------|-----------|---------|-----------------|
| **Association (L1)** | $P(Y \mid X = x)$ | "When layer 3 head 2 attends to the subject, accuracy is higher" | Correlation, regression |
| **Intervention (L2)** | $P(Y \mid \text{do}(X = x))$ | "Ablating layer 3 head 2 reduces accuracy by 12%" | Ablation, activation patching, causal tracing |
| **Counterfactual (L3)** | $P(Y_x \mid X = x', Y = y')$ | "Had layer 3 head 2 attended differently, this specific prediction would have changed" | Counterfactual reasoning, structural causal models |

**The key insight:** L2 (intervention) evidence is strictly stronger than L1 (association) evidence, and L3 (counterfactual) is stronger still. Claiming L2 conclusions from L1 experiments — or L3 conclusions from L2 experiments — is an epistemic error that the field commits routinely.

### Valid Mappings from Activations to High-Level Structures

The paper formalizes what constitutes a **valid interpretability claim**: a mapping $\phi: \text{Activations} \to \text{High-level descriptions}$ is valid for causal claims if and only if:

$$\phi(h(x)) = s \implies P(Y \mid \text{do}(h(x) = v)) \text{ depends on } s \text{ as predicted}$$

In other words: the high-level description $s$ must predict the causal effect of interventions on the activations. If $\phi$ maps activations to "subject token representation" but intervening on those activations does not affect subject-related predictions, then $\phi$ is not causally valid.

### Observational vs. Interventional vs. Counterfactual Evidence

**Observational evidence (L1) supports:**
- "Component X is associated with behavior Y"
- "X is necessary for Y to occur" (if Y never occurs without X)

**Interventional evidence (L2, e.g., ablation, activation patching) supports:**
- "Removing/replacing X changes Y by amount $\Delta$"
- "X is part of a mechanism for Y over this distribution of inputs"

**Counterfactual evidence (L3) requires:**
- Structural Causal Model (SCM) specifying the full data-generating process
- Assumptions about counterfactual consistency and faithfulness

### The Invariance Requirement for Generalization

The authors introduce a key requirement for interpretability findings to be scientifically useful: **invariance across distribution shifts.** A valid causal mechanism should remain identifiable and operative under:
- Different prompt distributions
- Different task variations
- Different model sizes (within a family)
- Different tokenizations of equivalent inputs

Mechanisms that only appear under specific experimental conditions are not true mechanisms — they are artifacts of the experimental design.

### Practical Guidelines (Pearl Hierarchy Applied)

| Experimental Design | Supported Claim Level | Example Valid Claim |
|--------------------|-----------------------|---------------------|
| Attention weight visualization | L1 (association) | "Head 3.2 shows high attention to the subject token when accuracy is high" |
| Logit lens / probing | L1 (association) | "Layer 6 representations are linearly predictive of subject token identity" |
| Ablation (zero/mean) | L2 (intervention) | "Ablating head 3.2 reduces accuracy by X% on this distribution" |
| Activation patching / causal tracing | L2 (intervention) | "Patching activations from clean → corrupted run via head 3.2 restores Y% of the performance drop" |
| DAS (Distributed Alignment Search) | L2/L3 (approximate) | "Intervening on the subspace aligned to 'subject position' causally mediates behavior Y" |
| Full SCM analysis | L3 (counterfactual) | "Had the model processed the subject differently at layer 6, this specific output token would have changed to Z" |

---

## Main Ideas & Key Contributions

### 1. A Unified Diagnostic Framework

The paper provides a **diagnostic checklist** for evaluating interpretability claims:
- What is the experimental design? (observational / interventional / counterfactual)
- What distribution of inputs was used? Are findings distribution-specific?
- What metric is used? Does the metric measure model behavior or model internals?
- Are interventions clean (well-specified ablation baseline)?
- Is the claim scoped appropriately to the evidence?

### 2. Reanalysis of Landmark MI Results

The authors reanalyze several high-profile mechanistic interpretability results through the causal hierarchy lens, showing that:
- Some claimed "circuit discoveries" are L1 findings presented as L2 claims
- Some intervention results are sensitive to ablation baseline choices in ways that undermine causal interpretation
- A subset of findings do meet rigorous L2 standards and should be trusted

This reanalysis is constructive (not merely critical) — it identifies which results are reliable and why.

### 3. Pearl's Hierarchy as Organizing Principle

Proposing that **Pearl's causal hierarchy become the field's standard organizing principle** is the paper's central normative contribution. This would enable:
- Clearer paper writing (claims scoped to evidence level)
- Principled experimental design (matching design to desired claim level)
- More productive cross-paper comparison
- Reduced reproducibility failures

### 4. Practical Recommendations

The paper offers actionable recommendations for researchers:
- Report effect sizes with confidence intervals, not just direction
- Specify the precise ablation baseline and justify it
- Test findings under distribution shift as standard practice
- Distinguish "consistent with X causing Y" from "X causes Y"

---

## Methodology & Implementation

### Paper Type and Approach

This is a **position / methodology paper**, not an empirical contribution in the traditional sense. The methodology is conceptual and analytical:

1. **Framework construction:** Applying Pearl's causal hierarchy to the interpretability domain
2. **Literature analysis:** Reviewing and reclassifying existing MI findings by causal claim level
3. **Case studies:** Detailed reanalysis of 3–4 landmark papers (IOI circuit, induction heads, ROME)
4. **Recommendations:** Translating theoretical framework into practical experimental guidelines

### Evaluation of the Framework

The framework is evaluated through:
- Consistency: Does it classify known-reliable findings as L2 and known-unreliable findings as L1?
- Coverage: Does it apply to all major categories of interpretability research?
- Practicality: Are the recommendations implementable within standard research workflows?

### Key Case Study: Induction Heads

The paper uses induction heads as a running example:
- **Observational evidence (L1):** Induction heads attend to previous occurrences of the current token
- **Interventional evidence (L2):** Ablating induction heads disrupts in-context learning performance
- **Counterfactual gap:** Whether induction heads are *the mechanism* for in-context learning (vs. a mechanism) requires L3 evidence the field has not yet provided

**Conclusion:** Induction heads are a genuine causal contributor (L2 established), but the strong claim that they *are* the in-context learning mechanism remains unvalidated.

### Limitations of the Paper

- As a position paper, empirical validation of the framework is limited
- Pearl's causal hierarchy was developed for static structural causal models; its application to the non-stationary, high-dimensional setting of LLMs requires additional assumptions
- Not all LLM behaviors admit structural causal model formulations
- The paper focuses on mechanistic interpretability; applicability to post-hoc methods (SHAP, LIME) is discussed but not fully developed

---

## Practical Applications & Real-World Use Cases

### AI Auditing and Red-Teaming

Organizations auditing AI systems for safety or bias need to distinguish genuine causal mechanisms from spurious correlations. This paper provides the vocabulary and framework for **rigorous auditing reports** that specify what level of causal evidence was obtained.

**Example:** An audit claiming that "model X is biased against demographic Y because it attended to gender markers" is an L1 finding. A rigorous audit would require L2 evidence: ablating/patching gender-related representations to verify the causal pathway.

### Regulatory Compliance

**EU AI Act (Article 12 — Record-keeping):** Requires documentation of AI system behavior for high-risk applications. Causal evidence (L2) is far more valuable for regulatory documentation than associational evidence (L1), which can be misleading under distribution shift.

**FDA AI/ML-Based SaMD guidance:** Medical AI systems must demonstrate that explanations are **faithful** to the model's actual decision process. The framework distinguishes faithful causal explanations (L2/L3) from correlational post-hoc rationalizations (L1).

### Research Methodology Education

This paper is an important pedagogical resource for graduate students and researchers entering the interpretability field. It teaches the distinction between experimental designs and the claims they support — a gap in current interpretability training.

### Implications for XAI Tool Developers

Developers of SHAP, LIME, and integrated gradients should be aware that their tools provide L1 evidence (feature attribution = association, not causation). This paper clarifies when such tools are appropriate and when L2 methods are required.

---

## Insights & Implications

### Why This Paper Matters for Trustworthy AI

A major source of distrust in AI explainability is the gap between what explanations claim and what they can actually support. Methods claiming to reveal "why the model made this decision" often reveal correlational patterns that could be spurious or misleading. This paper provides the theoretical basis for **distinguishing genuine causal explanations from correlational ones** — a prerequisite for trustworthy AI.

### The State of the Art in Interpretability

The paper's central claim is both sobering and constructive: **much published interpretability research makes stronger causal claims than the experimental evidence supports.** But the same analysis reveals a clear path forward: standardize on Pearl's hierarchy, design experiments at the intended causal level, and scope claims accordingly.

### Implications for Benchmark Development

The framework implies that interpretability benchmarks should evaluate:
- Whether findings replicate under distribution shift (testing invariance)
- Whether claimed causal mechanisms produce predicted intervention effects (testing causal validity)
- Whether ablation results are stable across ablation baseline choices

This is significantly more demanding than current benchmarks.

### Open Questions

- How does the framework apply to **emergent capabilities** — behaviors that are not localized to specific components?
- What is the relationship between causal validity in Pearl's sense and **human-understandability**? A causally valid but highly technical explanation may not be interpretable to non-experts.
- Can we develop **efficient L3 evidence procedures** for LLMs, or is counterfactual reasoning fundamentally out of reach for billion-parameter models?
- How does the framework apply to multi-modal models where the causal structure involves both visual and linguistic components?

### Influence on Future Research Directions

This paper is likely to catalyze:
- Adoption of **causal hierarchy framing** in interpretability paper writing and reviewing
- Development of **new experimental protocols** specifically designed to generate L2 evidence
- Replication studies of landmark MI results using the paper's diagnostic framework
- Closer collaboration between the causal inference and interpretability communities

---

## Code & Resources

As a position/methodology paper, there is no code repository associated with this work.

**ArXiv:** [https://arxiv.org/abs/2602.16698](https://arxiv.org/abs/2602.16698)  
**PDF:** [https://arxiv.org/pdf/2602.16698](https://arxiv.org/pdf/2602.16698)

### Recommended Background Reading

- **Pearl, J. (2009). Causality.** Cambridge University Press — foundational reference for the causal hierarchy
- **Pearl, J. & Mackenzie, D. (2018). The Book of Why** — accessible introduction to causal reasoning
- **Elhage et al. (2021). A Mathematical Framework for Transformer Circuits** — the MI paper this work most directly critiques and complements
- **Wang et al. (2022). Interpretability in the Wild** — IOI circuit paper, analyzed as a case study
- **Meng et al. (2022). Locating and Editing Factual Associations in GPT (ROME)** — another case study

---

## Related Work & Context

### Causal Interpretability Predecessors

- **Geiger et al. (2021, 2023) — Causal Abstraction:** Formally defines interpretability as finding a high-level causal model that is aligned with (abstracted from) the low-level neural network computation; directly related to this paper's formal framework
- **Wang et al. (2022) IOI paper:** Uses activation patching to provide L2 evidence for the IOI circuit — cited as an example of principled L2 interpretability
- **Conmy et al. (2023) ACDC:** Automated circuit discovery using activation patching — L2 method

### Critique and Response to the MI Program

- **Friedman et al. (2023) "Interpretability Illusion":** Questions whether circuit-level claims are stable
- **This paper:** Provides the theoretical framework that explains when and why such instability occurs (L1 findings incorrectly claimed as L2)

### Connection to the Broader XAI Community

The paper's framework applies beyond mechanistic interpretability:
- **SHAP/LIME:** L1 methods (association-based) — often incorrectly treated as causal
- **Counterfactual explanations:** Approximate L3 methods — validity depends on SCM assumptions
- **Causal feature attribution:** Emerging research area working toward genuine L2/L3 feature importance

The paper argues for a **unified causal epistemology for all of XAI**, not just mechanistic interpretability — a potentially transformative contribution to the field.
