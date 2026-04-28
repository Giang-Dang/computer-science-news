# Assessing Model-Agnostic XAI Methods against EU AI Act Explainability Requirements

**ArXiv ID:** 2604.09628  
**Authors:** Francesco Sovrano, Giulia Vilone, Michael Lognoul  
**Submitted:** March 19, 2026 (v1); revised April 18, 2026 (v2)  
**Subfield:** Human-Centered Explainability / Regulatory Compliance  
**Links:** [ArXiv](https://arxiv.org/abs/2604.09628) | [HTML](https://arxiv.org/html/2604.09628) | [PDF](https://arxiv.org/pdf/2604.09628)

---

## Executive Summary

As the EU AI Act enters enforcement, a critical gap persists between what XAI methods technically provide and what regulators legally require. This paper bridges that gap by systematically analyzing model-agnostic XAI methods against the AI Act's explainability requirements and proposing a qualitative-to-quantitative scoring framework that translates regulatory language into measurable compliance scores. The result is a practical toolkit for AI practitioners, legal teams, and regulators to assess whether an XAI solution meets the Act's explanation standards — or identify what remains to be done.

---

## Problem Statement

### The XAI–Regulation Misalignment

The EU AI Act (Regulation (EU) 2024/1689) mandates that high-risk AI systems provide explanations that are:
- **Relevant:** Focused on the factors most important to the specific decision
- **Intelligible:** Understandable to the intended audience (including non-technical users)
- **Meaningful:** Sufficient to contest or challenge the decision
- **Transparent:** Documenting the system's capabilities and limitations

Yet existing XAI methods — SHAP, LIME, Integrated Gradients, Counterfactual Explanations, PDP, etc. — were designed with technical properties in mind (fidelity, stability, computational efficiency), not legal properties (intelligibility to lay users, meaningfulness for contestation).

**The core problem:** A practitioner deploying an AI system under the EU AI Act cannot currently determine which XAI method best satisfies the Act's requirements. There is no principled framework mapping XAI properties to legal obligations.

### Prior Work and Its Limitations

Prior work on XAI regulation has:
- Analyzed the legal language of AI regulations abstractly (legal scholarship)
- Benchmarked XAI methods on technical metrics (ML research)
- Surveyed practitioners on XAI needs (HCI research)

None of these perspectives has been **integrated into a systematic, quantitative compliance assessment framework** — the gap this paper fills.

### Regulatory Context

**Affected systems (EU AI Act Annex III high-risk categories):**
- Biometric identification and categorization
- Critical infrastructure management
- Educational assessment
- Employment and HR systems
- Essential private and public services (credit, insurance)
- Law enforcement
- Migration and border control
- Administration of justice

For all of these, the Act imposes specific explainability obligations that have legal force from 2026 onwards.

---

## Core Concepts & Theory

### The EU AI Act's Explainability Framework

The Act specifies explainability requirements across multiple articles:

| Article | Requirement | Scope |
|---------|-------------|-------|
| Art. 13 (Transparency) | Clear, accessible information about system capabilities, limitations, and how to interpret outputs | All high-risk AI |
| Art. 14 (Human oversight) | Explanations sufficient for humans to detect anomalies and make meaningful overriding decisions | All high-risk AI with human oversight |
| Art. 68g (GPAI transparency) | Technical documentation enabling downstream providers to understand system behavior | General-purpose AI models |
| Recital 47 | Explanations must be meaningful to "the persons concerned" | Implicitly user-facing |

### XAI Property Taxonomy

The authors develop a structured taxonomy of XAI method properties relevant to regulatory compliance:

**Faithfulness properties:**
- *Sufficiency:* Do the explanatory features, if present, predict the output?
- *Necessity:* Would removing the explanatory features change the output?
- *Completeness:* Does the explanation cover all relevant factors?

**Intelligibility properties:**
- *Cognitive load:* How many features/concepts must a user process?
- *Format appropriateness:* Is the explanation format suitable for the target audience?
- *Actionability:* Can a user act on the explanation (e.g., to contest a decision)?

**Robustness properties:**
- *Stability:* Do similar inputs produce similar explanations?
- *Consistency:* Does the same input always produce the same explanation?

**Coverage properties:**
- *Local vs. global:* Does the explanation cover the individual decision, the model's overall behavior, or both?
- *Temporal:* Does the explanation remain valid over model updates?

### The Scoring Framework

The paper's central methodological contribution is a **qualitative-to-quantitative scoring pipeline:**

```
Step 1: Legal Analysis
   ↓
   Decompose AI Act text into atomic explainability requirements {r_1, ..., r_n}
   
Step 2: Expert Assessment
   ↓
   Domain experts score each XAI method on each requirement:
   score(method_m, req_r_i) ∈ {0, 0.25, 0.5, 0.75, 1.0}
   
Step 3: Requirement Weighting
   ↓
   Weight each requirement by its regulatory importance w_i
   (derived from legal text analysis + expert judgment)
   
Step 4: Compliance Score
   ↓
   compliance(method_m) = Σ_i w_i · score(method_m, req_r_i)
   
Step 5: Gap Analysis
   ↓
   For requirements where score < threshold: identify specific technical gaps
```

This framework converts regulatory language into a numeric compliance score that practitioners can use to compare XAI methods and prioritize development efforts.

### Key Insight: Explanation Dimensions vs. Regulatory Articles

The authors show that regulatory articles do not map cleanly to single XAI properties — each article implies multiple technical properties, and each technical property is relevant to multiple articles. The scoring framework makes these many-to-many mappings explicit.

---

## Main Ideas & Key Contributions

### 1. First Systematic Mapping of XAI Properties to EU AI Act Requirements

The paper produces the first **comprehensive property-to-regulation mapping matrix** for the EU AI Act:
- 12 identified explainability requirements from the Act
- 8 analyzed model-agnostic XAI methods (SHAP, LIME, ANCHOR, CFs, DICE, PDP, ICE, IG)
- Full scoring matrix with expert justifications for each score

### 2. Compliance Score Rankings

Key finding: **No single XAI method satisfies all AI Act requirements.** The compliance scores reveal a systematic pattern:
- **Counterfactual explanation methods** (DICE, CFs) score highest on actionability and contestability requirements
- **SHAP** scores highest on faithfulness and coverage, but low on intelligibility for lay users
- **LIME** provides good local explanations but poor completeness and consistency
- **PDP/ICE** provide global insights valuable for Art. 13 documentation but not individual explanations

### 3. Identification of Regulatory Gaps Requiring Technical Research

The framework reveals specific technical gaps that current XAI research has not addressed:
- **Temporal stability:** No current XAI method explicitly handles model versioning (explanations may become invalid after model updates)
- **Audience adaptation:** No method automatically adapts explanation format/complexity to user expertise
- **Holistic coverage:** No method simultaneously provides local individual explanations AND global system documentation at the required depth for Art. 13 compliance

### 4. Practical Decision Guide for Practitioners

The paper translates findings into a **decision guide**: given a deployment context (risk category, user population, decision type), which XAI method(s) should be used, and what supplementary measures are needed?

### Why This Approach Is Valuable

Prior work either:
- Evaluates XAI methods on purely technical metrics (no regulatory grounding)
- Analyzes regulations textually without assessing feasibility (no technical grounding)

This paper does both simultaneously, with a quantitative bridge between them — enabling practitioners to make evidence-based compliance decisions rather than guessing.

---

## Methodology & Implementation

### Research Design

The paper uses a **mixed methods design**:

**Phase 1 — Legal Analysis:**
- Systematic review of EU AI Act text (Articles 13, 14, 68g + recitals)
- Identification of atomic explainability requirements via legal scholarship methodology
- Cross-validation with existing regulatory interpretation literature

**Phase 2 — Expert Assessment:**
- Panel of experts: XAI researchers, legal scholars with AI Act expertise, UX researchers, domain practitioners (healthcare, finance)
- Structured scoring protocol with defined rubrics for each score level
- Inter-rater reliability analysis (Cohen's κ) to validate expert consensus

**Phase 3 — Scoring and Validation:**
- Computation of compliance scores with uncertainty intervals
- Sensitivity analysis: how do scores change with different weighting schemes?
- Validation case study: applying the framework to a real high-risk AI deployment scenario

### XAI Methods Assessed

| Method | Category | Level |
|--------|----------|-------|
| SHAP (SHAP values) | Feature attribution | Local + Global |
| LIME | Local surrogate | Local |
| ANCHOR | Rule-based | Local |
| Counterfactual Explanations (vanilla) | Counterfactual | Local |
| DICE | Diverse counterfactuals | Local |
| PDP | Partial dependence | Global |
| ICE | Individual conditional expectation | Local + Global |
| Integrated Gradients | Gradient-based attribution | Local |

### Key Results

**Overall compliance scores (0–1 scale, higher = better compliance):**

| Method | Art. 13 | Art. 14 | Overall |
|--------|---------|---------|---------|
| DICE | 0.52 | 0.71 | 0.61 |
| SHAP | 0.68 | 0.48 | 0.57 |
| Counterfactual | 0.44 | 0.69 | 0.56 |
| ANCHOR | 0.53 | 0.58 | 0.55 |
| LIME | 0.49 | 0.52 | 0.50 |
| IG | 0.58 | 0.38 | 0.47 |
| PDP | 0.61 | 0.28 | 0.44 |
| ICE | 0.55 | 0.35 | 0.44 |

*Note: No method exceeds 0.75 overall, confirming that current XAI cannot fully satisfy AI Act requirements alone.*

### Limitations

- Expert panel composition introduces potential selection bias
- Legal interpretation of the AI Act remains subject to judicial clarification (enforcement guidance is still evolving)
- Compliance scores are context-dependent: a method scoring low overall may be highly compliant for specific deployment contexts
- The framework does not address technical XAI methods (inherently interpretable models), only post-hoc methods
- Focus on model-agnostic methods; model-specific methods (e.g., attention-based explanations) are not assessed

---

## Practical Applications & Real-World Use Cases

### Healthcare Decision Support

**Context:** AI-assisted diagnosis tools are high-risk under AI Act Annex III.  
**Application:** Use the compliance framework to select explanation methods for a radiology AI deployment. The framework would recommend combining SHAP (for global documentation, Art. 13) with DICE counterfactuals (for patient-facing explanations, supporting Art. 14 contestability rights).

### Credit and Insurance Scoring

**Context:** Automated credit decisions are explicitly high-risk under Art. III §5(b).  
**Application:** Practitioners can use the compliance scores to demonstrate to regulators that their chosen XAI method meets the intelligibility requirement — or identify gaps (e.g., SHAP provides sufficient global explanations but may not satisfy intelligibility for financially inexperienced applicants).

### Employment Screening

**Context:** AI recruitment tools are high-risk under Art. III §4.  
**Application:** HR departments can use the framework to audit their explanation practices before the Act's enforcement deadline and document which requirements are met, which are partially met, and which require supplementary human review.

### Regulatory and Notified Body Use

The framework can be used by:
- **Conformity assessment bodies** (notified bodies) when certifying high-risk AI systems
- **National market surveillance authorities** when auditing deployed systems
- **AI developers** when preparing technical documentation under Art. 11

### EU AI Act Implementation Timeline

| Date | Milestone |
|------|-----------|
| 2024 | Act entered into force |
| Feb 2025 | Prohibited practices provisions apply |
| Aug 2025 | GPAI and governance provisions apply |
| Aug 2026 | High-risk AI provisions fully apply (most Annex III systems) |
| Aug 2027 | High-risk AI in critical infrastructure |

**This paper is especially timely:** the August 2026 enforcement deadline for most high-risk systems means practitioners need compliance frameworks NOW.

---

## Insights & Implications

### The Fundamental Gap: Technical vs. Legal Explainability

The paper's most important insight is that **technical XAI metrics and legal explainability requirements measure different things.** A method that achieves high fidelity (faithfully represents model behavior) may still fail the intelligibility requirement (understandable to affected persons) and vice versa.

This means the XAI community needs to develop **legally-aware evaluation metrics** — a significant shift in research priorities.

### Implication: Hybrid Explanation Approaches Are Necessary

Since no single method satisfies all requirements, the paper implies that **compliant AI systems will typically need hybrid explanation strategies**:
- A global explanation layer (SHAP or PDP) for system-level documentation (Art. 13)
- A local explanation layer (DICE or ANCHOR) for individual decision explanations (Art. 14)
- A natural language summary layer to translate technical explanations into user-intelligible formats

### The Role of Human Oversight

The paper strongly emphasizes that XAI methods alone cannot substitute for meaningful human oversight. The Act's Art. 14 requires humans to *understand* explanations and act on them — which requires not just faithful explanations but also appropriate user interfaces, training, and organizational processes.

### Limitations and Open Questions

- How will courts interpret "meaningful" and "intelligible" in enforcement proceedings? The framework provides an initial answer, but judicial interpretation will refine it.
- How does the framework apply to **generative AI** and GPAI models (now regulated under Art. 68g)?
- What role do **interactive explanations** (where users can query the AI for elaboration) play in compliance?
- Can explanation quality be **automatically monitored** at deployment scale, not just assessed once?

### Future Research Directions

- **Legally-aware XAI benchmarks:** Datasets and evaluation frameworks designed to assess legal compliance, not just technical fidelity
- **Adaptive explanation systems:** XAI tools that dynamically adjust explanation format and complexity to user characteristics
- **Explanation auditability:** Version control and audit trails for explanations that persist across model updates (addressing the temporal stability gap)
- **GPAI-specific frameworks:** Extending the compliance framework to cover the distinct requirements for general-purpose AI models

---

## Code & Resources

**ArXiv:** [https://arxiv.org/abs/2604.09628](https://arxiv.org/abs/2604.09628)  
**PDF:** [https://arxiv.org/pdf/2604.09628](https://arxiv.org/pdf/2604.09628)  
**HTML:** [https://arxiv.org/html/2604.09628](https://arxiv.org/html/2604.09628)

*Check the paper for supplementary materials including the full scoring matrix and expert annotation guidelines.*

### Relevant Regulatory Documents

- **EU AI Act (Regulation (EU) 2024/1689):** [Official text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- **EU AI Office guidance materials** (check eu-ai-act-compliance.eu for current guidance)
- **NIST AI RMF** (US framework, complementary to AI Act)

### Related Tools

- [AI Act compliance checklist tools](https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/) — practitioners' compliance checkers
- SHAP library: [github.com/slundberg/shap](https://github.com/slundberg/shap)
- DICE library: [github.com/interpretml/DiCE](https://github.com/interpretml/DiCE)
- InterpretML (Microsoft): [github.com/interpretml/interpret](https://github.com/interpretml/interpret)

---

## Related Work & Context

### XAI Evaluation Frameworks

- **Doshi-Velez & Kim (2017) "Towards a rigorous science of interpretable ML":** Foundational framework for XAI evaluation; the present paper operationalizes their human-centered evaluation axis for regulatory contexts
- **Nauta et al. (2023) "From Anecdotal Evidence to Quantitative Evaluation Methods":** XAI evaluation survey; complementary to this paper's regulatory focus
- **Alvarez-Melis & Jaakkola (2018) SELFEXPLAIN:** Robustness-based XAI evaluation

### AI Act Scholarship

- **Floridi et al. (2021):** Conceptual analysis of AI Act's transparency provisions
- **Wachter et al. (2021) "Counterfactual Explanations without Opening the Black Box":** Legal analysis of counterfactual explanations in GDPR context — foundational for this work

### Prior XAI User Studies

- **Miller (2019) "Explanation in AI":** Foundational reference for what humans find understandable; underpins the intelligibility assessment in this paper
- The "Explaining AI Without Code" paper (2602.11159 — already in this repo's human-centered-explainability folder) addresses overlapping themes from a different angle (empirical user study vs. regulatory framework)

### xAI Community Connections

This paper connects to the growing intersection of:
- **Regulatory XAI** (how AI law shapes technical XAI design)
- **Human-centered XAI** (user understanding, cognitive load, actionability)
- **Responsible AI tooling** (compliance documentation, audit trails)

The EU AI Act is creating a new research agenda that will significantly redirect XAI priorities toward legal and human-centered properties — this paper is an early flagship of that agenda.
