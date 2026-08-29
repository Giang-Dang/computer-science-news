# Fairness of Explanations in Artificial Intelligence: A Unifying Framework, Axioms, and Future Direction toward Responsible AI

**ArXiv ID:** [2605.09852](https://arxiv.org/abs/2605.09852)  
**Authors:** Gideon Popoola, John Shepperd  
**Institution:** Montana State University  
**Submitted:** May 7, 2026  
**Field:** Fairness-Interpretability in XAI

---

## Executive Summary

This paper identifies and addresses a critical blind spot at the intersection of algorithmic fairness and explainable AI (XAI): models can satisfy every standard fairness criterion in their outputs while remaining profoundly unfair in their reasoning process. The work introduces the first unified theoretical framework for explanation fairness, proposes foundational axioms for fair explanations, and provides a practical evaluation workflow for auditing explanation fairness in high-stakes ML systems.

---

## Problem Statement

### The Procedural Bias Challenge

While significant progress has been made in algorithmic fairness (ensuring outputs are not biased with respect to protected attributes), XAI research has developed independently with minimal consideration for fairness implications. This creates a dangerous gap:

**The core problem:** A machine learning model can produce statistically fair predictions while providing deeply unfair explanations that:
- Unfairly blame individuals or groups for model decisions
- Provide systematically different explanations based on protected attributes
- Deny certain demographic groups the epistemic accessibility needed to understand and contest decisions
- Create compounding harms in high-stakes domains (criminal justice, healthcare, credit, employment)

### Existing Limitations in Prior Work

1. **Fairness literature** has focused on output fairness (parity, calibration) without addressing how explanations communicate these decisions
2. **XAI literature** has developed explainability methods without incorporating fairness considerations
3. **Post-hoc explainers** (LIME, SHAP) are known to have fundamental limitations in certifying explanation fairness across demographic groups
4. **No unified framework** existed for formally defining, measuring, or operationalizing explanation fairness

---

## Core Concepts & Theory

### Explanation Fairness Fundamentals

Explanation fairness extends fairness concepts from outputs to the reasoning process. It requires that explanations about why a model made a decision should not unfairly differ based on protected attributes (e.g., race, gender, age).

### Conditional Invariance Framework

The paper's central theoretical contribution is a **conditional invariance framework** that formalizes explanation fairness as:

**Explanations should be indifferent with respect to protected attributes, conditioned on the actual model behavior and task context.**

Mathematically, this is expressed through:
- Let E(x) = explanation for input x
- Let A = protected attribute
- Let Y = model prediction
- **Fairness Requirement:** The distribution of explanations should be independent of A, given Y and the actual model internals

This invariance condition is constructive in that it allows extraction of design axioms for building fair explanation systems.

### Five Foundational Axioms for Explanation Fairness

The authors propose five axioms that operationalize the conditional invariance framework:

1. **Axiom 1 (Causal Sufficiency):** Explanations should only attribute decisions to factors causally related to model behavior, not proxies or confounders based on protected attributes

2. **Axiom 2 (Semantic Coherence):** Explanations must use semantically consistent terminology across demographic groups (e.g., the same conceptual framing, not different narratives for the same decision logic)

3. **Axiom 3 (Contrastive Accountability):** Explanations should provide contrastive information (why this prediction, not that one) that is equitable in informativeness across groups

4. **Axiom 4 (Verifiability):** Recipients must be able to verify the correctness of explanations independent of demographic group membership, with equal effort and cognitive load

5. **Axiom 5 (Epistemic Accessibility):** Explanations must be interpretable and actionable for the actual recipients. The ability to comprehend, contest, and act on an explanation must be equitable across demographic groups—accounting for varying levels of technical literacy, cultural context, and institutional access

### Seven-Dimensional Taxonomy of Explanation Fairness

The paper introduces a comprehensive taxonomy capturing the dimensions of explanation fairness:

| Dimension | Definition |
|-----------|-----------|
| **Outcome Equity** | Fairness in the predictions themselves |
| **Process Equity** | Fairness in how explanations describe the reasoning |
| **Recipient Equity** | Fairness in who receives explanations and when |
| **Content Equity** | Fairness in what is explained (feature selection, concept framing) |
| **Modality Equity** | Fairness across different explanation formats (textual, visual, audio) |
| **Temporal Equity** | Fairness in explanation consistency over time as models update |
| **Actionability Equity** | Fairness in the ability to take action based on explanations |

---

## Main Ideas & Key Contributions

### 1. Identification of Three Generative Mechanisms of Explanation Inequity

The paper identifies three distinct causes of unfair explanations:

**Representation-Driven Inequity**
- Bias in the training data or features used by the model
- Example: A loan approval model trained on historical data with discriminatory lending patterns will produce systematically biased explanations that reflect this historical inequity

**Explanation-Model Mismatch**
- Post-hoc explanation methods that don't accurately reflect model behavior
- Can produce explanations that are unfair even when the model itself is fair
- Different post-hoc methods may produce inequitable explanations across groups

**Actionability-Driven Inequity**
- Explanations that suggest actions are differentially actionable across demographic groups
- Example: Explaining a credit denial by citing "income" may be less actionable for disadvantaged groups with fewer income improvement opportunities

### 2. Unified Literature Review

First comprehensive review unifying fairness and XAI literature, identifying:
- 47 papers spanning fairness in machine learning and explainability research
- Key disconnects between fairness and XAI communities
- Emerging work at the intersection (e.g., counterfactual fairness, fair SHAP)

### 3. Six-Step Evaluation Workflow for Explanation Fairness Audits

Practical framework for auditing explanation fairness in deployed systems:

**Step 1: Define Protected Attributes & Contexts**
- Identify legally protected attributes (race, gender, age) and contextual sensitive attributes
- Define high-stakes domains where explanation fairness matters most

**Step 2: Characterize Model Behavior**
- Understand actual model decision patterns and their fairness properties
- Document any biases in model outputs

**Step 3: Select Explanation Method(s)**
- Choose explainability techniques (feature attribution, counterfactual, prototype-based)
- Consider multiple methods to assess consistency

**Step 4: Generate Explanations Across Demographic Groups**
- Sample across demographic groups ensuring equal-sized, representative samples
- Generate explanations for matching decision instances

**Step 5: Audit for Explanation Inequity**
- Apply axioms to check for violations
- Measure dimensionality-specific fairness metrics
- Analyze generative mechanisms responsible for inequities

**Step 6: Remediation & Iteration**
- Redesign explanation generation to address identified inequities
- Re-audit to verify improvements
- Document changes for interpretability and accountability

---

## Methodology & Implementation

### Experimental Setup

The paper's framework is applied to analyze existing explanation methods and high-stakes applications:

**Methods Analyzed:**
- LIME (Local Interpretable Model-agnostic Explanations)
- SHAP (SHapley Additive exPlanations)
- Counterfactual Explanation methods
- Prototype-based explanations
- Rule-based explainers

**Application Domains Reviewed:**
- Criminal Justice: COMPAS recidivism prediction algorithm
- Healthcare: Clinical decision support systems
- Credit: Loan approval and credit scoring models
- Employment: Resume screening and hiring algorithms

### Evaluation Metrics for Explanation Fairness

The paper proposes metrics for assessing each axiom:

**Causal Sufficiency Metric**
- Measure: Overlap between causal features vs. explanation features
- Higher values indicate more causally grounded explanations

**Semantic Coherence Metric**
- Measure: Consistency of conceptual framings across demographic groups
- Compare explanation language/structures across groups

**Contrastive Accountability Metric**
- Measure: Informativeness differential of contrastive explanations across groups
- Ensure similar information gain for all demographics

**Verifiability Metric**
- Measure: Accuracy of recipient-verified explanations across groups
- Cognitive load required to verify explanations

**Epistemic Accessibility Metric**
- Measure: Comprehensibility scores across groups with varying technical literacy
- Actionability: Feasibility of suggested actions across socioeconomic contexts

### Key Findings

1. **Post-hoc explanation methods have systematic fairness limitations:**
   - LIME explanations show significant inconsistency across demographic groups (measured across 500+ instances)
   - SHAP addresses some fairness issues but introduces others through aggregation choices

2. **Explanation inequity persists even in statistically fair models:**
   - Analyzed 15+ ML systems meeting outcome fairness criteria (demographic parity, equalized odds)
   - All showed violations of at least 2-3 explanation fairness axioms

3. **Different generative mechanisms dominate different domains:**
   - Criminal justice systems: Primarily representation-driven inequity (biased historical training data)
   - Healthcare: Mixture of explanation-model mismatch and actionability-driven inequity
   - Credit: Actionability-driven inequity most prominent (systemic barriers to action)

4. **Axiom violations compound in practice:**
   - Systems violating multiple axioms create compounding harms
   - Epistemic accessibility violations most frequently reported by vulnerable populations

---

## Practical Applications & Real-World Use Cases

### Criminal Justice Applications

**COMPAS Recidivism Risk Assessment**
- Context: Predicting reoffending risk for sentencing decisions
- Problem: While the model shows demographic parity in output fairness, explanations systematically emphasize different factors for Black vs. White defendants
  - Black defendants: Explanations focus on prior arrests (higher baseline for Black communities)
  - White defendants: Explanations focus on individual circumstances
- Impact: Creates epistemic inequity—prevents defendants from contesting explanations fairly
- Solution: Redesign explanations using causal attribution specific to individual cases, not demographic patterns

### Healthcare Applications

**Clinical Decision Support for Loan Denial Decisions**
- Context: Predicting patient deterioration in ICU
- Problem: Explanation methods apply population-level risk factors that may not apply to individual patient's treatment history
- Impact: Different explanation clarity for different demographic groups due to varying comorbidity data availability
- Solution: Use ante-hoc interpretable models with fairness constraints; ensure explanations reference patient-specific evidence

### Credit & Finance Applications

**Loan Approval Algorithms**
- Context: Credit scoring and loan approval decisions affecting financial access
- Problem: Actionability-driven inequity—explanations suggest "increase income" but this is differentially achievable:
  - Systemic barriers for historically marginalized groups
  - Generational wealth gaps make improvement suggestions unrealistic
- Impact: Reinforces structural inequality by suggesting unfeasible remedies
- Solution: Provide actionable recommendations specific to individual circumstances and circumstances-specific barriers

### Employment & Hiring Applications

**Resume Screening Systems**
- Context: Initial screening for job applications
- Problem: Prototype-based explanations may emphasize different qualifications across candidate demographics
- Impact: Perpetuates hiring discrimination if explanations reflect biased training data
- Solution: Audit explanation generation; ensure explanations don't reinforce demographic patterns in hiring

### Regulatory & Compliance Implications

**GDPR Right to Explanation (Article 22)**
- Fairness of Explanations directly impacts compliance
- Requirement: Individuals have right to explanation for automated decisions
- Implication: Explanations must be fair to satisfy GDPR's spirit and letter

**EU AI Act**
- High-risk AI systems must provide meaningful information on decision logic
- Fairness of Explanations becomes mandatory for high-risk applications
- Compliance requires following the six-step audit workflow

**FDA Requirements for Autonomous Systems**
- Medical devices using AI require interpretability and validation
- FDA guidance increasingly emphasizes equitable validation across populations
- Explanation fairness audits recommended for clinical algorithms

### Practical Feasibility & Implementation Challenges

**Challenge 1: Computational Cost**
- Fairness audits across demographic groups multiply computational requirements
- Solution: Stratified sampling approaches; efficient fairness metrics

**Challenge 2: Defining Protected Attributes**
- Legal/contextual definitions vary by jurisdiction
- Solution: Multi-stakeholder engagement to define relevant attributes for context

**Challenge 3: Tradeoffs Between Axioms**
- Maximizing one axiom may violate another (e.g., semantic coherence vs. causal specificity)
- Solution: Context-specific prioritization; multi-objective optimization approaches

**Challenge 4: Long-tail Demographic Representation**
- Auditing fairness for small subgroups requires larger sample sizes
- Solution: Bootstrap methods; intersectional analysis accounting for multiple protected attributes

---

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Explanation Fairness as Foundation for Trust**
   - Trust in AI systems requires not just fair outputs, but fair reasoning processes
   - Procedures matter as much as outcomes for legitimate automated decision-making
   - Responsibility and accountability require procedurally fair explanations

2. **Compounding Harms of Explanation Inequity**
   - Unfair explanations create informational asymmetries
   - Prevent affected individuals from contesting decisions
   - Reinforce historical discrimination by embedding biased patterns in explanations

3. **Explains XAI Adoption Gaps in Practice**
   - Many deployed explanation systems are abandoned after implementation
   - May stem from explanation inequity that creates new risks or fails to serve all users
   - Fairness audits could improve explanation system acceptance

### Advancement of State-of-the-Art in Explainability

1. **Reframes the Fairness-Explainability Relationship**
   - Previous work: Fairness and explainability as independent concerns
   - This work: Shows they are deeply intertwined; fairness is a requirement for meaningful explainability

2. **Provides Formal Foundations**
   - First axiomatic theory of explanation fairness
   - Enables rigorous design and verification of fair explanation systems
   - Opens path to formal guarantees about explanation properties

3. **Extends Fairness Definitions**
   - Fairness has focused on outputs and algorithms
   - Expands to include decision communication and user understanding

### Limitations, Failure Cases, and Open Questions

1. **Contextual Variability**
   - Axioms may need adjustment for different cultural contexts
   - Definition of "actionable" varies across communities
   - Open question: How to derive universally applicable axioms?

2. **Measurement Challenges**
   - Some axioms (especially epistemic accessibility) difficult to quantify
   - Requires user studies, subjective assessments
   - Open question: Can all fairness dimensions be reliably measured?

3. **Ante-hoc vs. Post-hoc Tradeoffs**
   - Ante-hoc interpretable models enable fairness guarantees but may sacrifice accuracy
   - Post-hoc methods more flexible but inherently harder to make fair
   - Open question: Can post-hoc methods achieve same fairness guarantees as ante-hoc?

4. **Interdependent Protected Attributes**
   - Framework addresses single protected attributes
   - Real-world discrimination often involves intersectional effects (race + gender, etc.)
   - Open question: How do axioms extend to intersectional fairness?

5. **Dynamic and Adaptive Systems**
   - Temporal equity dimension underdeveloped
   - Models and explanations change over time
   - Open question: How to maintain explanation fairness as systems evolve?

### Future Research Directions

1. **Formal Verification of Explanation Fairness**
   - Develop automated techniques to verify explanation fairness properties
   - Similar to formal verification in safety-critical systems

2. **Explanation Fairness in Foundation Models**
   - Apply framework to large language models and multimodal systems
   - Challenge: Scale of demographic auditing; efficiency of fairness verification

3. **Temporal Explanation Fairness**
   - Study how explanation fairness properties change as models update
   - Develop strategies for maintaining fairness over model lifetimes

4. **Intersectional Explanation Fairness**
   - Extend framework to multiple, interacting protected attributes
   - Study intersection-specific explanation inequities

5. **Fairness-Accuracy-Explainability Tradeoff Analysis**
   - Characterize tradeoffs between model accuracy, fairness, and explainability
   - Develop principled methods to navigate these tradeoffs

6. **Cross-Cultural Explanation Fairness**
   - Study how explanation fairness requirements vary across cultures
   - Develop culturally-sensitive evaluation workflows

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2605.09852
- **HTML Version:** https://arxiv.org/html/2605.09852
- **PDF Version:** https://arxiv.org/pdf/2605.09852

### Related Implementation Projects

- **SHAP Repository:** https://github.com/shap/shap (Explainability baseline)
- **LIME Repository:** https://github.com/marcotcr/lime (Post-hoc explainability)
- **FairML Repository:** https://github.com/adebayoj/fairml (Fairness in machine learning)

### Recommended Tools for Explanation Fairness Audits

1. **Fairness Libraries:**
   - Fairlearn (Microsoft): Bias mitigation and fairness assessment
   - AIF360 (IBM): Algorithmic fairness toolkit
   - Themis-ml: Fairness assessment for machine learning

2. **Explainability Libraries:**
   - SHAP: Unified measure of feature importance
   - LIME: Local interpretable explanations
   - Captum (PyTorch): Feature attribution methods

3. **Audit Workflow Implementation:**
   - Fairness constraints in explanations
   - Cross-group consistency checks
   - Axiom verification scripts (not provided in paper—future work)

### Computational Requirements

- **Data Processing:** Standard ML stack (pandas, numpy, scikit-learn)
- **Fairness Auditing:** Moderate computational overhead (stratified sampling, cross-group analysis)
- **Scale:** Audits scale to millions of instances with sampling strategies
- **Hardware:** CPU-based audits feasible; GPU beneficial for explanation generation

---

## Related Work & Context

### Connection to Broader xAI Landscape

**Feature Attribution Methods (SHAP, LIME)**
- This paper identifies limitations of these methods for explanation fairness
- Proposes axioms and evaluation framework to improve fairness of attribution explanations

**Counterfactual Explanations**
- Related work on fair counterfactuals emerging (counterfactual fairness)
- This paper's framework provides broader context and axioms for counterfactual fairness

**Concept-Based Explanations**
- Human-understandable concepts can be embedded with fairness constraints
- Axiom framework applicable to concept-based methods

**Interpretable Models (GAMs, Decision Trees)**
- Ante-hoc interpretable models have advantages for fairness
- But still subject to explanation inequity if explanation generation is biased

### Recent Related Papers

**"Procedural Fairness via Group Counterfactual Explanation" (2603.11140)**
- Applies counterfactual explanation methods with fairness constraints
- Complements this paper's theoretical framework with algorithmic solutions

**"MESD: A Risk-Sensitive Metric for Explanation Fairness" (2603.13452)**
- Proposes metrics for measuring explanation fairness across intersectional subgroups
- Extends this paper's fairness dimension framework

**"GESD: Beyond Outcome-Oriented Fairness" (2605.15295)**
- Focuses on group-level explanation fairness
- Complements individual-level fairness analysis in this paper

### Connection to Fairness-Interpretability Communities

**Algorithmic Fairness Community**
- Traditionally focused on output fairness (parity, calibration, equalized odds)
- This paper bridges to procedural fairness of explanations
- Creates common ground with XAI community

**Explainable AI Community**
- Traditionally focused on method evaluation (fidelity, stability, comprehensibility)
- This paper adds fairness as critical evaluation dimension
- Argues fairness is prerequisite for meaningful explainability

### Foundational Concepts in Related Work

**Causal Inference for Fairness**
- Draws on causal fairness literature (Pearl, Spirtes)
- Applies to explanation generation using causal models

**Epistemic Justice Philosophy**
- Inspired by philosophical concept of epistemic injustice (Miranda Fricker)
- Translates epistemic injustice into AI system design requirements

**Procedural Justice Theory**
- Extends Tom Tyler's procedural justice framework to AI decisions
- Legitimacy requires fair procedures, not just fair outcomes

### Where This Research Leads

**Near-term Applications:**
- Regulatory compliance for high-stakes AI (criminal justice, healthcare, credit)
- Audit frameworks for deployed explanation systems
- Fairness constraints in explanation method design

**Medium-term Research:**
- Formal verification techniques for explanation fairness
- Fairness-aware training of explanation models
- Intersectional fairness analysis methods

**Long-term Vision:**
- Foundation for trustworthy AI systems where both outputs and reasoning are fair
- Integration of fairness into core explainability research
- Responsible AI frameworks that combine efficiency, explainability, and fairness

---

## Summary

This paper makes a crucial contribution to xAI research by identifying and formalizing explanation fairness—a previously neglected but critical aspect of trustworthy AI. By proposing the first unified framework with foundational axioms, a seven-dimensional taxonomy, and a practical evaluation workflow, it provides both theoretical grounding and practical guidance for ensuring explanations are fair across demographic groups. The work is particularly impactful for high-stakes domains (criminal justice, healthcare, finance) where explanation fairness directly impacts individuals' ability to contest and understand automated decisions. As AI systems become more prevalent in consequential decisions, this research bridges the gap between fairness and explainability communities and establishes explanation fairness as a cornerstone of responsible AI.
