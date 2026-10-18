# GFGE: Unifying Explainable AI Methods Through an Interpretation Framework

**ArXiv ID:** [2610.05225](https://arxiv.org/abs/2610.05225)

**Authors:** Jinfeng Zhong

**Affiliation:** LIASD, Université Paris 8, 93200 Saint-Denis, France

**Publication Date:** October 4, 2026

**Status:** Recent preprint (under review)

---

## Executive Summary

This paper proposes GFGE (General Framework for Generating Explanations), a meta-framework that unifies diverse explainable AI methodologies under a common conceptual structure. Rather than proposing a new explanation method, GFGE provides a standardized way to organize, analyze, and compare how different XAI approaches work, addressing a critical need in the field for consistent definitions and operational structures across explanation paradigms.

---

## Problem Statement

The XAI field has developed numerous explanation methodologies—LIME, SHAP, counterfactual methods, concept-based explanations, and language-model-based explanations—yet lacks a unified theoretical framework to organize and compare them. This fragmentation creates several challenges:

1. **Inconsistent Terminology:** Different XAI papers use terms like "explanation," "interpretation," and "saliency" with varying definitions
2. **Methodological Silos:** There is no standardized way to combine or compare different explanation approaches
3. **Missing Quality Assurance:** It is unclear how to systematically verify the quality and faithfulness of diverse explanation methods
4. **Integration Difficulty:** Existing AI systems cannot easily combine intrinsic, post-hoc, and hybrid explanation techniques

Previous work (e.g., XAI surveys and handbooks) has argued that the field needs consistent definitions and frameworks, but no comprehensive operational structure has been proposed that encompasses all major XAI paradigms.

---

## Core Concepts & Theory

### The Interpret/Explain Schema (IES)

GFGE is grounded in the **Interpret/Explain Schema (IES)**, a foundational conceptual model derived from linguistic analysis, philosophy of explanation, cognitive science, and knowledge management. The IES describes how interpretation and explanation flow through the data–model–output pipeline:

1. **Sense-Reading (Interpretation):** An analyst examines evidence from the AI system and interprets what it means
2. **Communication:** The analyst selects and communicates a chosen account or explanation based on their interpretation
3. **Sense-Reading by Recipient:** The recipient (human, other system, or stakeholder) interprets the communicated explanation

This schema emphasizes that explanations are not objective facts about a model, but rather **communicative acts** where evidence is filtered, interpreted, and presented for understanding.

### The Five Roles Framework

GFGE instantiates the IES through five modular, role-typed operations:

1. **Data Interpretation:** Processing and understanding raw input data (e.g., tokenization, feature extraction, normalization)
2. **Model Interpretation:** Understanding how the model processes interpreted data (e.g., attention weights, layer activations, decision boundaries)
3. **Output Interpretation:** Making sense of model predictions (e.g., confidence scores, class probabilities, ranking)
4. **Post-hoc Analysis** (optional): Additional processing to explain model behavior (e.g., LIME surrogate fitting, SHAP value computation, generating counterfactuals)
5. **Aggregation:** Combining multiple evidence records into coherent, human-understandable explanations

These roles maintain distinct evidence requirements for **intrinsic explanations** (based on model structure alone), **post-hoc explanations** (from additional analysis), and **hybrid approaches** (combining both).

### Evidence Records & Operational Graphs

GFGE maintains **evidence records** that track:
- **Source:** Where the evidence comes from
- **Assumptions:** What preconditions must hold for the evidence to be valid
- **Limitations:** What the evidence cannot claim about the model
- **Dependencies:** How evidence records relate to one another

The framework represents explanation workflows as **operation graphs** where roles are nodes and dependencies are edges, creating a formal but flexible structure for describing XAI methods.

---

## Main Ideas & Key Contributions

### 1. Unifying Framework for Heterogeneous XAI Methods

GFGE is the first framework to standardize explanation workflows across different XAI paradigms. The key innovation is treating **all explanation methods through a common operational structure** (the five roles), while allowing method-specific instantiations for each role. This enables:

- **Comparative analysis** of different explanation approaches using consistent terminology
- **Hybrid explanations** that combine intrinsic and post-hoc methods systematically
- **Quality verification** by tracking evidence provenance and assumptions

### 2. Formal Treatment of Explanation Generation

Rather than treating explanation as a black box, GFGE makes the process explicit through role-typed operations. For example:

- **LIME** is instantiated as: Data Interpretation → Model Interpretation → Post-hoc Analysis (surrogate fitting) → Aggregation
- **SHAP** is instantiated as: Data Interpretation → Model Interpretation → Post-hoc Analysis (Shapley computation) → Aggregation
- **Concept-based methods** are instantiated as: Data Interpretation → Model Interpretation (concept detection) → Output Interpretation → Aggregation

### 3. Distinction Between Explanation Scope

GFGE formalizes the distinction between:
- **Local explanations:** Why did the model make this specific prediction?
- **Global explanations:** How does the model work in general?
- **Compositional explanations:** How do sub-components combine to produce outputs?

This distinction clarifies when methods like LIME (typically local) should be aggregated for global understanding, versus when methods like decision trees (often global) apply.

### 4. Evidence Tracking for Trustworthiness

By tracking evidence records through the five roles, GFGE enables:
- **Faithfulness verification:** Did post-hoc approximations preserve model behavior?
- **Assumption validation:** What preconditions must hold for an explanation to be valid?
- **Limitation disclosure:** What can this explanation legitimately claim about the model?

---

## Methodology & Implementation

### Framework Instantiation Across Seven XAI Methodologies

GFGE has been instantiated and validated across seven major explanation paradigms:

1. **Attribution Methods** (e.g., gradient-based, Shapley-based approaches)
   - Role focus: Model interpretation and post-hoc analysis
   - Evidence: Importance/contribution scores for input features

2. **Surrogate Methods** (e.g., LIME)
   - Role focus: Model interpretation → Post-hoc analysis (fitting simpler model)
   - Evidence: Local approximations of decision boundaries

3. **Counterfactual Methods** (e.g., generating alternative scenarios)
   - Role focus: Data interpretation → Post-hoc analysis (generation) → Output interpretation
   - Evidence: Minimal changes to produce different predictions

4. **Concept/Prototype Methods** (e.g., identifying prototypical examples)
   - Role focus: Model interpretation (concept detection) → Output interpretation
   - Evidence: Representative instances or discovered concepts

5. **Intrinsic Rule Methods** (e.g., decision trees, rule extraction)
   - Role focus: Model interpretation → Direct output mapping
   - Evidence: Explicit decision rules without post-hoc analysis

6. **Argumentation Methods** (e.g., logical argumentation-based explanations)
   - Role focus: Data interpretation → Model interpretation → Aggregation (logical reasoning)
   - Evidence: Logical premises and inference chains

7. **Language-Model Methods** (e.g., LLM-based explanation generation)
   - Role focus: All roles orchestrated through language model
   - Evidence: Natural language descriptions of model behavior

### Evaluation Approach

[Exact figures unavailable — see full paper]

This is a conceptual/theoretical framework paper focused on expressiveness rather than empirical performance. The evaluation primarily demonstrates:

- **Descriptive Expressiveness:** Can the framework accurately describe all seven XAI methodologies?
- **Conceptual Completeness:** Can intrinsic, post-hoc, and hybrid workflows all be represented?
- **Formal Consistency:** Are the five roles and IES sufficient for all major XAI paradigms?

No experimental performance comparisons, datasets, or statistical metrics are provided in this version.

### Limitations

The paper acknowledges that GFGE is a **conceptual framework**, not a software implementation or new algorithm. Limitations include:

- **No reference implementation:** Code is not yet available for practitioners
- **No empirical validation:** No datasets or benchmarks demonstrate practical benefits
- **Theoretical focus:** The framework's impact on real-world XAI deployments is unknown
- **Scope bounds:** Some emerging explanation paradigms (e.g., recent mechanistic interpretability methods) may require framework extensions

---

## Practical Applications & Real-World Use Cases

### Critical Application Domains

GFGE's unifying framework is particularly valuable for domains where explainability is legally or ethically mandated:

1. **Healthcare & Medical Diagnosis**
   - Use case: Comparing explanations from multiple AI diagnostic systems
   - Benefit: GFGE enables systematic evaluation of which explanation method (attribution, counterfactual, concept-based) best serves clinicians
   - Regulatory relevance: FDA guidance increasingly requires interpretability evidence

2. **Finance & Credit Decisions**
   - Use case: Documenting explanations for loan denials or credit scoring
   - Benefit: GFGE provides a standardized framework for compliance audits
   - Regulatory relevance: GDPR Article 22 and Fair Credit Reporting Act require explainability

3. **Legal & Judicial Systems**
   - Use case: Explaining AI-assisted sentencing recommendations or risk assessments
   - Benefit: GFGE enables systematic comparison of explanation faithfulness and completeness
   - Regulatory relevance: Courts increasingly scrutinize AI decision explanations

4. **Autonomous Systems & Robotics**
   - Use case: Explaining safety-critical decisions (e.g., collision avoidance)
   - Benefit: GFGE enables integration of intrinsic (model structure) and post-hoc (behavior analysis) explanations
   - Regulatory relevance: ISO/IEC standards for AI safety increasingly require explanation frameworks

### Concrete Example: Medical Diagnosis System

A hospital deploys an AI system to suggest diagnoses. GFGE enables the hospital to:

1. **Data Interpretation:** Explain how patient data (symptoms, test results) is encoded
2. **Model Interpretation:** Show which symptoms the model relies on most (via attribution)
3. **Output Interpretation:** Explain confidence scores and differential diagnoses
4. **Post-hoc Analysis:** Generate counterfactual explanations ("if symptom X were absent, diagnosis would change")
5. **Aggregation:** Synthesize evidence into a clinician-friendly report

The framework ensures all explanations are traceable, with documented assumptions and limitations.

### Regulatory & Compliance Implications

**GDPR (General Data Protection Regulation):**
- Article 22 requires "meaningful information about the logic" of automated decisions
- GFGE provides a systematic way to document and audit explanation quality

**EU AI Act:**
- High-risk AI systems must have "appropriate human oversight"
- GFGE enables systematic verification that explanations support human oversight

**FDA Guidance on AI/ML in Medical Devices:**
- FDA increasingly requires "explainability and interpretability evidence"
- GFGE provides a structured framework for demonstrating compliance

---

## Insights & Implications

### Implications for XAI Research & Practice

1. **Unification Across Paradigms:** GFGE shows that seemingly diverse XAI methods (LIME, SHAP, counterfactuals, concepts) can be systematically organized. This opens the door to:
   - **Hybrid explanations** that combine strengths of multiple methods
   - **Transparent comparison** of explanation quality across paradigms
   - **Principled selection** of explanation methods for specific use cases

2. **Closing the Terminology Gap:** By formalizing the Interpret/Explain Schema, the framework provides precise definitions of key XAI terms. This addresses a long-standing complaint that XAI papers use inconsistent terminology.

3. **Evidence-Centric Explainability:** GFGE's emphasis on evidence tracking (sources, assumptions, limitations) represents a shift toward **trustworthy explanations** that acknowledge their own boundaries.

4. **Operationalization of Explanation:** The five-role framework makes explanation generation explicit and auditable, which is essential for regulatory compliance and organizational trust in AI systems.

### Broader Implications for Trustworthy AI

1. **Explainability as Infrastructure:** GFGE positions explainability not as an add-on feature, but as a **core infrastructure component** for AI systems. Just as software requires version control and testing frameworks, AI systems should require explanation frameworks.

2. **Transparency Without Cargo Cult:** GFGE helps avoid "false transparency," where explanations give the appearance of understanding without actually providing valid evidence. By tracking assumptions and limitations, the framework promotes honest explanations.

3. **Scalability of Auditing:** As AI systems become more prevalent, manual explainability audits become infeasible. GFGE provides a formal basis for **automated explanation quality assurance**.

4. **Human-AI Collaboration:** By clarifying how different explanation methods serve different stakeholder needs (clinician, regulator, data scientist), GFGE supports better **human-AI collaborative workflows**.

### Limitations & Open Questions

1. **No Performance Data:** This preprint lacks empirical validation. Key questions remain:
   - Does GFGE actually improve explanation quality in practice?
   - Are there computational costs to systematic evidence tracking?
   - How much overhead does formal operation graph representation add?

2. **Implementation Challenges:** Critical implementation questions are unaddressed:
   - How can GFGE be implemented in existing ML frameworks?
   - What is the API design for specifying operation graphs?
   - How do we handle streaming or online explanations?

3. **Emerging Methods:** The paper may need extension for:
   - **Mechanistic interpretability** approaches (circuits, sparse features)
   - **Active explanation** systems that interact with users
   - **Group explanations** for cohorts rather than individuals

4. **Scope of "Explanation":** GFGE focuses on post-prediction explanations. It may not fully address:
   - Explanations of training data influence
   - Explanations of model robustness or failure modes
   - Explanations grounded in causal inference

### Future Research Directions

1. **Empirical Validation:** Future work should benchmark GFGE against existing XAI frameworks on real datasets and use cases.

2. **Software Implementation:** An open-source GFGE library would enable adoption and empirical testing.

3. **Integration with Model-Specific Methods:** Explore how GFGE integrates with recent advances in mechanistic interpretability and causal explanation.

4. **Multi-Stakeholder Explanations:** Extend GFGE to systematically generate different explanations for different stakeholders (clinician, patient, regulator).

5. **Adversarial Robustness:** Study whether GFGE explanations are robust to adversarial attacks or data perturbations.

---

## Code & Resources

### Official Resources

- **Paper:** [https://arxiv.org/abs/2610.05225](https://arxiv.org/abs/2610.05225)
- **HTML Version:** [https://arxiv.org/html/2610.05225](https://arxiv.org/html/2610.05225)
- **PDF:** [https://arxiv.org/pdf/2610.05225](https://arxiv.org/pdf/2610.05225)

### Code Availability

**Status:** No code or implementation currently available

- No GitHub repository is linked from the paper
- This is a conceptual framework presented as theory rather than software
- An implementation may be released by the author in the future

### Dependencies & Requirements

Since GFGE is presented as a conceptual framework rather than a software library:
- No specific programming language or dependencies are required for understanding the framework
- Future implementations would likely target Python (PyTorch, TensorFlow) for deep learning integration
- The framework itself is model-agnostic and could be implemented in any language

### Quick Start Guide

To understand and apply GFGE:

1. **Read the Core Framework:** Start with the Interpret/Explain Schema (IES) and Five Roles
2. **Map Your Method:** Identify which of the five roles your favorite XAI method uses (LIME, SHAP, etc.)
3. **Track Evidence:** For your explanations, document sources, assumptions, and limitations
4. **Compare Methods:** Use GFGE to systematically compare explanation approaches

---

## Related Work & Context

### Relationship to Classic XAI Methods

**LIME (Local Interpretable Model-Agnostic Explanations):**
- In GFGE terms: Data Interpretation → Model Interpretation (perturbed samples) → Post-hoc Analysis (surrogate model fitting) → Aggregation (local feature weights)
- Key insight: LIME provides local explanations of a surrogate model, not necessarily the original model
- GFGE enables systematic analysis of faithfulness gaps

**SHAP (SHapley Additive exPlanations):**
- In GFGE terms: Data Interpretation → Model Interpretation → Post-hoc Analysis (Shapley value computation) → Output Interpretation → Aggregation
- Key insight: SHAP provides feature importance through cooperative game theory
- GFGE clarifies that SHAP is both a local (instance-level) and global (feature-level) explanation method

**Attention Mechanisms (in Transformers):**
- In GFGE terms: Model Interpretation (attention visualization) → Optional Aggregation (across heads/layers)
- Caution: Attention weights are not explanations; they require careful evidence tracking and assumption disclosure
- GFGE emphasizes that attention interpretability has documented limitations

**Concept Activation Vectors (CAVs) & TCAV:**
- In GFGE terms: Model Interpretation (concept detection) → Output Interpretation (concept contribution) → Aggregation
- Key insight: Concepts must be defined and validated before use in explanations
- GFGE systematizes concept-based explanation workflows

### Positioning Within the XAI Landscape

**Comparison to Prior XAI Surveys:**
- Earlier surveys (e.g., 2021 "Explainable AI Handbook", 2025 "Explainable AI and LLMs") documented various methods but lacked operational unification
- GFGE addresses the gap by providing a formal framework for organizing XAI methodologies
- This is the first meta-framework to encompass intrinsic, post-hoc, and hybrid explanations under one structure

**Relationship to Mechanistic Interpretability:**
- Recent mechanistic interpretability work (circuits, sparse features, monosemanticity) focuses on understanding model internals
- GFGE's "Model Interpretation" role encompasses mechanistic approaches
- Future work may extend GFGE to more deeply integrate circuit analysis and neuron-level interpretability

**Relationship to Causal Inference & Explainability:**
- Causal explanation methods (do-calculus, causal graphs) may be integrated into GFGE's Post-hoc Analysis role
- GFGE could systematize the distinction between correlation-based (statistical) and causation-based explanations

**Relationship to AI Fairness:**
- Some fairness explanations (e.g., "why is this decision disparate?") can be represented through GFGE
- Future work could extend GFGE to fairness-specific explanation needs

### Key Communities & Standards

**LIME & SHAP Communities:**
- GFGE provides a unified framework that encompasses both LIME and SHAP, enabling dialogue across communities

**XAI Handbook & Standards Efforts:**
- GFGE contributes to the ongoing standardization of XAI terminology and workflows
- The five-role framework aligns with emerging standards for AI governance (NIST, ISO/IEC)

**Interpretability Research Community:**
- Papers on mechanistic interpretability, concept-based explanations, and causal inference can all be positioned within GFGE
- The framework enables better cross-community understanding and collaboration

**AI Governance & Regulation:**
- GFGE directly supports regulatory requirements (GDPR, EU AI Act, FDA guidance) by providing systematic explanation frameworks
- The evidence-tracking approach aligns with regulatory demands for audit trails and assumption disclosure

---

## Conclusion

GFGE represents a significant conceptual contribution to the XAI field by providing the first unified operational framework for diverse explanation methodologies. By formalizing the Interpret/Explain Schema and the five-role architecture, the paper addresses long-standing fragmentation in XAI research and practice.

While the framework is currently theoretical without empirical validation or software implementation, its potential impact is substantial:

- **For researchers:** GFGE provides a common language for comparing XAI methods and designing hybrid explanations
- **For practitioners:** The framework supports systematic explanation quality assurance and regulatory compliance
- **For AI governance:** The evidence-tracking approach enables transparent and auditable AI systems

Future work should focus on software implementation, empirical validation on real datasets, and integration with emerging interpretability paradigms. If GFGE achieves adoption as a standard explanability framework, it could significantly advance the field toward trustworthy, transparent, and compliant AI systems.

---

## References & Additional Resources

### Cited & Related Papers

- Earlier XAI frameworks and surveys referenced in GFGE (to be completed from paper)
- LIME: ["Why Should I Trust You?": Explaining the Predictions of Any Classifier](https://arxiv.org/abs/1602.04938)
- SHAP: [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874)
- Mechanistic Interpretability: [Mechanistic Interpretability for Neural Networks](https://arxiv.org/abs/2607.07316)

### Key XAI Resources

- **LIME GitHub:** https://github.com/marcotcr/lime
- **SHAP GitHub:** https://github.com/slundberg/shap
- **XAI Handbook:** Online resource for comprehensive XAI methodology overview
- **Interpretability Workshops:** Regular conferences (NeurIPS InterpML, ICML Interpretability Workshop)

### Regulatory & Standards References

- **GDPR Article 22:** Right to explanation for automated decision-making
- **EU AI Act:** Requirements for high-risk AI system transparency
- **FDA Guidance:** Requirements for AI/ML explainability in medical devices
- **NIST AI Standards:** Emerging standards for AI governance and interpretability

---

## Notes

- This documentation synthesizes information from the GFGE paper abstract, framework description, and XAI literature context
- As of October 4, 2026, this is a very recent preprint with no peer reviews, citations, or released code
- For complete mathematical formulations, detailed algorithm descriptions, and empirical results (once available), please refer to the full paper at https://arxiv.org/pdf/2610.05225
- The framework is model-agnostic and applicable across ML/AI domains; specific domain applications may vary

**Documentation Date:** October 9, 2026

**Status:** Paper is recent preprint; subject to updates as peer review and community feedback develops
