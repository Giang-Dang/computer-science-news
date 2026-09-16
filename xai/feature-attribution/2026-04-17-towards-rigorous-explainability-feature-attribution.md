# Towards Rigorous Explainability by Feature Attribution

**Authors:** Olivier Létoffé, Xuanxiang Huang, Joao Marques-Silva

**ArXiv ID:** 2604.15898

**Publication Date:** April 17, 2026 (Last revised: May 27, 2026)

**Submission Link:** https://arxiv.org/abs/2604.15898

---

## Executive Summary

This paper critically examines the rigor of current feature attribution methods used in explainable AI (XAI), particularly challenging the widespread adoption of non-rigorous approaches like SHAP. The authors argue that for high-stakes applications, feature attribution must be grounded in formal, symbolic methods that provide verifiable and auditable explanations, rather than heuristic-based approaches that lack theoretical guarantees.

---

## Problem Statement

**Current Challenge:** Over the past decade, non-symbolic methods have dominated feature attribution in machine learning explainability. However, these approaches lack mathematical rigor and can systematically mislead human decision-makers, particularly in high-stakes domains such as healthcare, finance, and criminal justice where explainability is critical for regulatory compliance and ethical AI deployment.

**Key Limitations of Existing Approaches:**

1. **Non-rigorous approximations:** Methods like SHAP and LIME rely on heuristic approximations of Shapley values without formal guarantees on the quality of explanations.

2. **Lack of verifiability:** Non-symbolic methods cannot provide formal proofs of correctness or bounds on explanation error.

3. **Misleading confidence:** These methods create an illusion of rigor through mathematical formalism (e.g., Shapley values) while employing approximations that undermine their theoretical foundations.

4. **Absence of auditability:** It is difficult to trace how non-symbolic methods arrive at specific feature importance rankings, limiting their use in regulated industries.

5. **Scalability paradox:** While these methods claim to scale to high-dimensional problems, this scalability comes at the cost of rigorous guarantees.

---

## Core Concepts & Theory

### Symbolic vs. Non-Symbolic Methods

**Non-Symbolic XAI (Current Dominant Approach):**
- Relies on numerical approximations and heuristics
- Examples: SHAP (KernelSHAP, TreeSHAP), LIME, Integrated Gradients
- Characteristics:
  - Fast computation for complex models
  - Interpretable results through human intuition
  - Lack of formal guarantees
  - Prone to manipulation or misinterpretation

**Symbolic XAI (Rigorous Alternative):**
- Based on formal logic, constraint satisfaction, and formal verification
- Characteristics:
  - Provides mathematical proofs of correctness
  - Generates auditable, verifiable explanations
  - Can establish bounds and guarantees on explanation quality
  - Supports formal reasoning about model behavior

### Shapley Values in Feature Attribution

The paper examines Shapley values, which are theoretically sound in game theory but often misapplied in XAI:

**Theoretical Foundation:**
- Shapley values represent the marginal contribution of a feature to all possible coalitions of features
- Axioms: linearity, dummy player property, symmetry, and efficiency
- Originally designed for cooperative game theory, not neural network interpretation

**The SHAP Problem:**
- SHAP attempts to apply Shapley values to feature attribution but relies on approximations (KernelSHAP uses sampling, TreeSHAP simplifies to tree structures)
- These approximations break the axiomatic guarantees of Shapley values
- The approximation error is rarely quantified or bounded
- Users often treat approximate explanations as having the rigor of true Shapley values

### Formal Feature Importance in Symbolic Methods

Rigorous feature attribution can be formalized as:

1. **Feature Relevance:** A feature f is relevant for instance x if removing or modifying f changes the model's prediction for x by more than a threshold ε

2. **Minimal Explanations:** A set of features is minimal if no proper subset explains the same behavior with equivalent rigor

3. **Counterfactual Reasoning:** Rigorous methods construct valid counterfactuals by modifying features and formally verifying the resulting predictions

---

## Main Ideas & Key Contributions

### 1. Critique of Non-Rigorous Feature Attribution

The paper provides a systematic critique showing that:
- SHAP's popularity has obscured fundamental theoretical problems
- Non-rigorous methods can produce consistent but incorrect explanations
- In high-stakes applications, the risk of relying on false confidence is unacceptable

### 2. Advocacy for Symbolic XAI Methods

The authors argue for transitioning to symbolic methods that:
- Provide formal proofs of explanation correctness
- Generate auditable decision trails
- Support regulatory compliance (GDPR, EU AI Act, etc.)
- Enable model improvement through formal analysis

### 3. Integration of Rigorous Methods

The paper outlines how symbolic XAI methods can:
- Identify provably important features
- Detect spurious correlations through formal analysis
- Verify fairness and robustness properties
- Support human-in-the-loop decision-making with formal guarantees

### 4. Bridging Theory and Practice

The contribution includes:
- Framework for evaluating rigor in feature attribution methods
- Comparison matrix of symbolic vs. non-symbolic approaches
- Practical recommendations for high-stakes applications
- Discussion of computational trade-offs

---

## Methodology & Implementation

### Research Approach

The paper employs:

1. **Theoretical Analysis:**
   - Formal examination of axioms and guarantees in different methods
   - Mathematical proofs of limitations in approximate methods
   - Characterization of error bounds in non-rigorous approaches

2. **Comparative Framework:**
   - Systematic comparison of symbolic and non-symbolic methods across dimensions:
     - Theoretical guarantees
     - Computational complexity
     - Scalability
     - Auditability
     - Practical applicability

3. **Literature Review:**
   - Comprehensive overview of rigorous XAI approaches
   - Historical context of symbolic methods in AI
   - Evolution of feature attribution methods

### Key Symbolic Methods Discussed

1. **Formal Verification Approaches:**
   - SAT/SMT-based methods for finding minimal explanations
   - Constraint satisfaction for feature importance ranking
   - Formal certificates of explanation correctness

2. **Causal Inference Methods:**
   - Causal graphs for establishing true feature importance
   - Counterfactual reasoning with formal guarantees
   - Structural equation modeling for verification

3. **Logic-Based Methods:**
   - Explainable rule extraction with formal guarantees
   - Decision tree extraction with verified fidelity
   - Knowledge representation for auditable reasoning

### Evaluation Framework

**Rigor Assessment Criteria:**

1. **Completeness:** Does the method identify all important features?
2. **Minimality:** Are explanations minimal without loss of fidelity?
3. **Provability:** Can the explanation be formally verified?
4. **Auditability:** Can a human or auditor trace the reasoning?
5. **Correctness:** Are the explanations provably correct?

[Exact figures unavailable — see full paper for specific experimental results]

---

## Practical Applications & Real-World Use Cases

### Healthcare

**Critical Application:** Medical diagnosis and treatment recommendations

- **Challenge:** Doctors need verifiable explanations of AI predictions for clinical decision-making
- **Rigorous Solution:** Symbolic methods can provide formal proofs that specific symptoms or test results directly influenced diagnosis
- **Regulatory Requirement:** FDA 21 CFR Part 11 requires auditable electronic records; formal XAI supports this compliance
- **Example:** An AI system recommending chemotherapy must formally prove which patient features (tumor size, biomarkers, genetic factors) justify the recommendation

### Finance & Credit Decisions

**Critical Application:** Loan approvals, fraud detection, risk assessment

- **Challenge:** Fair Lending Laws (ECOA, FHA) require explainable reasons for credit decisions
- **Rigorous Solution:** Formal methods can prove which factors actually caused a credit denial (not spurious correlations)
- **Regulatory Requirement:** GDPR Article 22 gives individuals right to explanation for automated decisions
- **Example:** If an AI denies credit, symbolic methods prove whether it was debt-to-income ratio or credit history, enabling auditable dispute resolution

### Criminal Justice

**Critical Application:** Risk assessment algorithms for sentencing and parole

- **Challenge:** Algorithmic bias in criminal justice has severe consequences (wrongful imprisonment)
- **Rigorous Solution:** Formal verification can prove that protected attributes (race, gender) do not influence predictions
- **Regulatory/Ethical Requirement:** Equal Protection Clause and state AI transparency laws demand verifiable fairness
- **Example:** A recidivism prediction system must formally demonstrate that incarceration rate is based on behavior patterns, not demographic factors

### Autonomous Systems & Safety

**Critical Application:** Self-driving car behavior, robot decision-making

- **Challenge:** Safety-critical decisions require formal guarantees about system behavior
- **Rigorous Solution:** Symbolic methods provide formal certificates that safety properties are maintained
- **Regulatory Requirement:** ISO 26262 (functional safety) for automotive systems demands traceable, verifiable reasoning
- **Example:** If an autonomous vehicle's AI brakes suddenly, formal methods prove whether it detected an actual obstacle (feature importance) versus spurious input anomalies

### Compliance & Auditing

**Common Regulatory Framework Requirements:**
- GDPR Right to Explanation (Articles 13-22)
- EU AI Act (Transparency and Human Override Requirements)
- FDA Software as a Medical Device (SaMD) guidance
- NIST AI Risk Management Framework
- SOX and financial reporting standards

**Advantage of Rigorous Symbolic Methods:**
- Generate audit trails that survive regulatory scrutiny
- Provide formal proofs of non-discrimination
- Enable demonstrable traceability of model decisions
- Support compliance certifications and attestations

---

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Rigor as a Foundation:** Trustworthy AI requires rigorous, verifiable foundations. Non-symbolic heuristics cannot serve as the basis for high-stakes decisions.

2. **Paradigm Shift Needed:** The field must move beyond the current emphasis on interpretability-through-intuition toward formal guarantees of correctness.

3. **Regulatory Alignment:** Future AI regulations will increasingly demand formal verification and auditability, favoring symbolic methods.

4. **Research Direction:** The convergence of formal methods, constraint solving, and causal inference offers a path forward for rigorous XAI.

### Limitations and Open Questions

1. **Scalability Challenges:** Symbolic methods scale differently than neural networks; finding minimal explanations for high-dimensional data remains computationally hard (NP-hard in many cases).

2. **Model Complexity:** Complex neural networks may not have sparse symbolic explanations; some models may be fundamentally uninterpretable.

3. **Ground Truth Problem:** Even symbolic methods cannot explain what ground truth is; they can only explain the model's behavior, not whether that behavior is correct.

4. **User Acceptance:** Non-technical users may find formal symbolic explanations less intuitive than numeric feature importance scores.

5. **Approximation Trade-offs:** Practical systems often require approximations; the paper acknowledges that perfect rigor and perfect scalability may be incompatible.

### Failure Cases and Future Directions

**When Rigorous Methods May Struggle:**
- Very-high-dimensional data with sparse explanations
- Models trained on biased data (garbage-in-garbage-out)
- Safety properties that are inherently difficult to formalize

**Future Research Directions:**
- Hybrid methods combining symbolic rigor with neural network scalability
- Formal verification of model training procedures, not just inference
- Integration of causal reasoning with formal verification
- Standardization of rigor metrics for XAI methods

---

## Code & Resources

### Implementation and Availability

**Official Implementations:**
- Paper repository and code links: [See ArXiv page for author's GitHub]
- Related symbolic XAI tools: 
  - SAT/SMT solvers (Z3, CVC5) for formal verification
  - Symbolic reasoning libraries

### Related Symbolic XAI Frameworks

1. **Formal Verification Tools:**
   - Z3 Theorem Prover (Microsoft Research)
   - CVC5 SMT Solver
   - ABC (A System for Sequential Synthesis and Verification)

2. **Causal Inference Libraries:**
   - DoWhy (Microsoft, causal inference)
   - CausalML (Uber, causal ML methods)

3. **Rule Extraction and Symbolic Methods:**
   - LIME alternatives with formal guarantees
   - Symbolic knowledge extraction tools

### Dependencies & Computational Requirements

**Typical Requirements for Symbolic Methods:**
- SMT Solver library (often free/open-source)
- Constraint programming solver
- Moderate memory for symbolic reasoning (depends on problem complexity)
- CPU-intensive (symbolic methods trade speed for rigor)

**Scalability Notes:**
- Symbolic methods work best for medium-sized datasets and models
- For very large models, approximations or hybrid approaches may be necessary
- Research ongoing on efficient symbolic reasoning for neural networks

### Quick Start Guide

1. **Understanding the Approach:**
   - Review the paper for theoretical foundations
   - Study symbolic XAI frameworks (SAT/SMT-based)

2. **Practical Implementation:**
   - Start with formal verification of simpler decision models
   - Progress to symbolic methods for complex models
   - Use hybrid approaches combining symbolic and neural methods

3. **Evaluation:**
   - Compare symbolic explanations with approximate methods
   - Measure rigor gains vs. computational costs
   - Assess explanation utility for target stakeholders

---

## Related Work & Context

### Connection to Other XAI Research

**Relationship to SHAP and LIME:**
- This paper provides critical analysis of these widely-used but non-rigorous methods
- Builds on earlier formal critiques by Marques-Silva and others
- Complements emerging work on approximate explanation error bounds

**Broader XAI Landscape:**
- Positions symbolic XAI as complementary to mechanistic interpretability research
- Connects to growing interest in formal verification for AI
- Relates to fairness and robustness certification work

### Historical Context of Symbolic Methods

1. **Roots in Classical AI:** Symbolic reasoning traces to knowledge-based systems and expert systems of the 1980s-90s
2. **Formal Verification Heritage:** Builds on decades of software verification research
3. **Modern Revival:** Recent progress in SAT/SMT solving and constraint programming enables scaling

### Prior Work This Paper Builds Upon

- **Marques-Silva et al.** on formal feature importance and explainability
- **Montúfar et al.** on neural network expressiveness and verification
- **Pearl and Mackie** on causal models and counterfactual reasoning
- **European AI regulations** driving demand for formal explainability

### Where This Research Leads Next

**Emerging Directions:**

1. **Hybrid Methods:** Combining neural network speed with symbolic rigor through:
   - Neural-symbolic integration
   - Distillation of neural models into interpretable symbolic forms
   - Formal verification of neural network approximations

2. **Scalable Symbolic XAI:**
   - Research on efficient symbolic reasoning for modern architectures
   - Constraint programming advances for high-dimensional problems
   - Approximation methods with formal error bounds

3. **Regulatory Integration:**
   - EU AI Act compliance through symbolic methods
   - GDPR-compliant explanation systems with formal verification
   - Standardized rigor metrics for regulatory assessment

4. **Foundational Research:**
   - Theoretical work on the limits of explainability
   - Formal characterization of which models are interpretable
   - Mathematical framework for comparing explanation quality

---

## Key Takeaways

1. **Current non-rigorous methods** (SHAP, LIME) lack theoretical guarantees and can mislead in high-stakes applications
2. **Symbolic methods** provide formal verifiability and auditability required by regulations and high-stakes domains
3. **The rigor-scalability trade-off** is fundamental; perfect rigor and perfect scalability may be incompatible
4. **Regulatory pressure** (GDPR, EU AI Act, FDA) will increasingly favor rigorous, formally verifiable approaches
5. **Hybrid methods** combining symbolic reasoning with neural network efficiency represent a promising future direction

---

## References & Further Reading

- **ArXiv Paper:** https://arxiv.org/abs/2604.15898
- **Related Surveys:** Papers on formal verification in ML and symbolic XAI methods
- **Regulatory Context:** GDPR, EU AI Act, FDA guidance on AI explainability
- **Foundational Work:** Shapley values in game theory and economics; Causal inference literature
